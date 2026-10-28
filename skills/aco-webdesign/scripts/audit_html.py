#!/usr/bin/env python3
"""Limited static HTML checks; does not run scripts, CSS or an accessibility tree."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.nodes = []; self.stack = []
    def handle_starttag(self, tag, attrs):
        node = {'tag':tag,'attrs':dict(attrs),'line':self.getpos()[0],'text':'','parents':list(self.stack)}
        self.nodes.append(node)
        if tag not in VOID: self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID: self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:self.stack = self.stack[:i];break
    def handle_data(self, data):
        for node in self.stack: node['text'] += data

def audit(path):
    path = Path(path)
    if path.suffix.lower() not in ('.html','.htm'):raise ValueError('Supply static/rendered .html, not JSX or a source template')
    doc = Document();doc.feed(path.read_text(encoding='utf-8'));doc.close();findings=[];nodes=doc.nodes
    def add(code, message, node=None):
        findings.append({'file':str(path),'line':node['line'] if node else 1,'severity':'review','code':code,'message':message})
    def tags(tag):return [n for n in nodes if n['tag']==tag]
    ids = {}
    for n in nodes:
        value=n['attrs'].get('id')
        if value:
            if value in ids:add('duplicate-id','ID repeats: '+value,n)
            ids[value]=n
    def named(n):
        a=n['attrs']
        if (a.get('aria-label') or '').strip():return True
        refs=(a.get('aria-labelledby') or '').split()
        if refs and all(ref in ids and ids[ref]['text'].strip() for ref in refs):return True
        if n['text'].strip():return True
        return any(x['tag']=='img' and (x['attrs'].get('alt') or '').strip()
                   and any(parent is n for parent in x['parents']) for x in nodes)
    if not any((n['attrs'].get('lang') or '').strip() for n in tags('html')):add('document-lang','Missing document language')
    if not any(n['text'].strip() for n in tags('title')):add('document-title','Missing page title')
    if not any(n['attrs'].get('name')=='viewport' for n in tags('meta')):add('viewport','Missing viewport metadata')
    if not tags('main'):add('main-landmark','No native main landmark; review document structure')
    if len(tags('h1'))!=1:add('primary-heading','Review page heading hierarchy; expected one primary h1 for this check')
    labels={n['attrs'].get('for') for n in tags('label') if n['text'].strip()}
    for n in nodes:
        a=n['attrs'];tag=n['tag']
        if tag=='img' and 'alt' not in a:add('image-alt','Image has no alt attribute',n)
        if tag in ('button','a') and not named(n):add('control-name','Control has no statically detectable name',n)
        if tag=='a' and (a.get('href') or '').strip() in ('','#'):add('placeholder-link','Link has no real destination',n)
        if tag in ('input','select','textarea') and a.get('type','text') not in ('hidden','submit','reset','button'):
            wrapped=any(p['tag']=='label' and p['text'].strip() for p in n['parents'])
            explicit=bool((a.get('aria-label') or '').strip());refs=(a.get('aria-labelledby') or '').split()
            labelled=bool(refs) and all(x in ids and ids[x]['text'].strip() for x in refs)
            if not (wrapped or explicit or labelled or (a.get('id') and a['id'] in labels)):
                add('field-label','Form field has no statically detectable label',n)
    return {'status':'findings' if findings else 'no_static_findings','findings':findings,'browser_verified':False,
            'limits':'Static HTML only; no JS/CSS execution, contrast, performance, visual or complete accessibility assessment.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=Path)
    try:
        result=audit(p.parse_args().file);print(json.dumps(result,indent=2));raise SystemExit(bool(result['findings']))
    except (OSError,ValueError) as error:p.exit(2,str(error)+'\n')
