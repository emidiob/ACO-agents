#!/usr/bin/env python3
"""Serve a local static project with reversible, source-backed text and style editing."""
import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
import tempfile
from pathlib import Path
import re
import secrets
import threading
from urllib.parse import unquote, urlsplit

ASSETS=Path(__file__).resolve().parents[1]/'assets/live'
PROPERTIES={'color','background-color','font-size','font-weight','line-height','letter-spacing','padding','margin','border-radius','max-width','gap','text-align'}
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Nodes(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False);self.source=source;self.rows=[];self.stack=[]
        self.lines=[0]
        self.lines += [m.end() for m in re.finditer('\n',source)]
        self.feed(source)
    def source_offset(self):
        line,col=self.getpos();return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        start=self.source_offset();end=start+len(self.get_starttag_text());attrs=dict(attrs)
        row={'tag':tag,'start':start,'open_end':end,'end':None,'close':None,'children':0,'attrs':attrs}
        if self.stack:self.stack[-1]['children']+=1
        self.rows.append(row)
        if tag not in VOID:self.stack.append(row)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.stack.pop()
    def handle_endtag(self,tag):
        if self.stack and self.stack[-1]['tag']==tag:
            row=self.stack.pop();row['close']=self.source_offset();row['end']=self.source.find('>',row['close'])+1
    def editable(self):
        return [r for r in self.rows if r['close'] is not None and r['tag'] not in {'html','head','body','script','style','title','textarea','select','option','svg','path'}]

class Project:
    def __init__(self,root):
        root=Path(root).expanduser().absolute()
        if any(p.is_symlink() for p in (root,*root.parents)):raise ValueError('Use a canonical project path without symlinks')
        self.root=root.resolve(strict=True);self.lock=threading.RLock();self.undo=[];self.redo=[]
        if not self.root.is_dir():raise ValueError('Project must be a directory')
    def path(self,relative):
        if not isinstance(relative,str):raise ValueError('Expected a relative path')
        rel=Path(relative)
        if rel.is_absolute() or '..' in rel.parts or any(p.startswith('.') for p in rel.parts):raise ValueError('Path not allowed')
        path=self.root/rel
        if any(p.is_symlink() for p in (path,*path.parents)):raise ValueError('Symlink not allowed')
        if not path.resolve().is_relative_to(self.root) or not path.is_file():raise ValueError('File not found')
        return path
    def write(self,path,raw):
        # Replace atomically on the same volume and preserve source permissions.
        mode=path.stat().st_mode
        fd,name=tempfile.mkstemp(prefix='.aco-edit-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as stream:
                stream.write(raw);stream.flush();os.fsync(stream.fileno())
            os.chmod(name,mode);os.replace(name,path)
        finally:
            if os.path.exists(name):os.unlink(name)
    def files(self):
        found=[]
        for directory,dirs,files in os.walk(self.root,followlinks=False):
            dirs[:]=[d for d in dirs if not d.startswith('.') and d not in {'node_modules','vendor'} and not (Path(directory)/d).is_symlink()]
            for name in files:
                if name.startswith('.') or Path(name).suffix.lower() not in {'.html','.htm'}:continue
                relative=str((Path(directory)/name).relative_to(self.root))
                try:self.path(relative)
                except ValueError:continue
                found.append(relative)
        return sorted(found)
    def read(self,relative):
        p=self.path(relative)
        if p.suffix.lower() not in {'.html','.htm'}:raise ValueError('Editing requires a static HTML file')
        raw=p.read_bytes()
        if len(raw)>2_000_000:raise ValueError('HTML exceeds editor size limit')
        return p,raw.decode('utf-8'),hashlib.sha256(raw).hexdigest()
    def preview(self,relative):
        with self.lock:
            _,source,digest=self.read(relative);nodes=Nodes(source).editable();changes=[]
            for i,row in enumerate(nodes):changes.append((row['open_end']-1,f' data-aco-node="{i}"'))
            for at,value in reversed(changes):source=source[:at]+value+source[at:]
            config=json.dumps({'file':relative,'hash':digest}).replace('<','\\u003c')
            return source+f'<script>window.__ACO_PREVIEW__={config};</script><script src="/__aco/preview.js"></script>'
    def apply(self,request):
        with self.lock:
            p,source,digest=self.read(request['file'])
            if request['hash']!=digest:raise ValueError('Source changed; reload before editing')
            nodes=Nodes(source).editable();index=request['node']
            if type(index) is not int or index<0 or index>=len(nodes):raise ValueError('Invalid node')
            row=nodes[index];kind=request['kind'];value=request['value']
            if not isinstance(value,str) or len(value)>20000:raise ValueError('Invalid value')
            if kind=='text':
                if row['children']:raise ValueError('Text editing is limited to leaf elements; edit nested markup in source')
                next_source=source[:row['open_end']]+escape(value,quote=False)+source[row['close']:]
            elif kind=='style':
                prop=request['property']
                if prop not in PROPERTIES or not re.fullmatch(r'[\w\s#.,()%+\-/]+',value) or re.search(r'url|expression|var\(',value,re.I):raise ValueError('Unsupported CSS property or value')
                opening=source[row['start']:row['open_end']]
                style=row['attrs'].get('style','')
                # Simple declarations only; do not silently damage complex existing styles.
                if any(x in style for x in ('/*','url(', '"', "'")):raise ValueError('Complex inline style must be edited in source')
                declarations={}
                for part in style.split(';'):
                    if not part.strip():continue
                    if ':' not in part:raise ValueError('Malformed existing inline style')
                    k,v=part.split(':',1);declarations[k.strip().lower()]=v.strip()
                declarations[prop]=value
                style='; '.join(k+': '+v for k,v in declarations.items())
                if 'style' in row['attrs']:
                    pattern=r'\sstyle\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+)'
                    opening,count=re.subn(pattern,' style="'+escape(style,quote=True)+'"',opening,count=1,flags=re.I)
                    if count!=1:raise ValueError('Cannot safely locate style attribute')
                else:opening=opening[:-1]+' style="'+escape(style,quote=True)+'">'
                next_source=source[:row['start']]+opening+source[row['open_end']:]
            else:raise ValueError('Unsupported edit kind')
            before=source.encode();after=next_source.encode()
            if len(after)>2_000_000:raise ValueError('Edited HTML exceeds size limit')
            if p.read_bytes()!=before:raise ValueError('Source changed; reload before editing')
            # Backups remain in memory for this session; source changes are immediate.
            self.write(p,after);self.undo.append((p,before,after));self.undo=self.undo[-50:];self.redo.clear()
            return {'saved':True,'hash':hashlib.sha256(after).hexdigest()}
    def history(self,direction):
        with self.lock:
            source,target=(self.undo,self.redo) if direction=='undo' else (self.redo,self.undo)
            if not source:raise ValueError('No '+direction+' available')
            p,before,after=source[-1];expected,result=(after,before) if direction=='undo' else (before,after)
            self.path(str(p.relative_to(self.root)))
            if p.read_bytes()!=expected:raise ValueError('Source changed externally; history was not applied')
            self.write(p,result);source.pop();target.append((p,before,after));return {'saved':True}

def server(project,port=0):
    token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def respond(self,status,body,kind='application/json'):
            raw=body if isinstance(body,bytes) else body.encode();self.send_response(status)
            self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
        def allowed(self):
            return self.headers.get('Host')==f'127.0.0.1:{self.server.server_port}'
        def do_GET(self):
            if not self.allowed():self.respond(403,'{}');return
            path=unquote(urlsplit(self.path).path)
            try:
                if path=='/__aco/':
                    text=(ASSETS/'editor.html').read_text().replace('ACO_SESSION_TOKEN',token)
                    self.respond(200,text,'text/html; charset=utf-8');return
                if path in ('/__aco/preview.js','/__aco/editor.js'):
                    self.respond(200,(ASSETS/path.rsplit('/',1)[-1]).read_bytes(),'text/javascript; charset=utf-8');return
                if path=='/__aco/files':
                    files=project.files()
                    self.respond(200,json.dumps(files));return
                relative=path.lstrip('/') or 'index.html';p=project.path(relative)
                if p.suffix.lower() in ('.html','.htm'):self.respond(200,project.preview(relative),'text/html; charset=utf-8')
                elif p.suffix.lower() in {'.css','.js','.mjs','.json','.svg','.png','.jpg','.jpeg','.webp','.gif','.woff','.woff2'}:self.respond(200,p.read_bytes(),mimetypes.guess_type(p.name)[0] or 'application/octet-stream')
                else:self.respond(403,'{}')
            except (ValueError,OSError,UnicodeError):self.respond(404,'{"error":"Not available"}')
        def do_POST(self):
            origin=f'http://127.0.0.1:{self.server.server_port}'
            if not self.allowed() or self.headers.get('Origin')!=origin or self.headers.get('X-ACO-Token')!=token:self.respond(403,'{}');return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=30000:raise ValueError('Invalid request size')
                data=json.loads(self.rfile.read(length));path=urlsplit(self.path).path
                if path=='/__aco/edit':result=project.apply(data)
                elif path in ('/__aco/undo','/__aco/redo'):result=project.history(path.rsplit('/',1)[-1])
                else:raise ValueError('Unknown operation')
                self.respond(200,json.dumps(result))
            except (ValueError,OSError,KeyError,TypeError) as e:self.respond(409,json.dumps({'error':str(e)}))
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--project',type=Path,required=True);parser.add_argument('--port',type=int,default=0);args=parser.parse_args()
    try:
        httpd=server(Project(args.project),args.port)
        print(f'ACO Live: http://127.0.0.1:{httpd.server_port}/__aco/',flush=True);httpd.serve_forever()
    except KeyboardInterrupt:pass
    except (ValueError,OSError) as e:parser.exit(2,str(e)+'\n')
