/** Original ACO development bridge. Uses Vite's server and ordinary framework HMR. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const assets=path.dirname(fileURLToPath(import.meta.url));
const digest=text=>crypto.createHash('sha256').update(text).digest('hex');
const escaped=text=>text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;').replaceAll('{','&#123;').replaceAll('}','&#125;').replaceAll('\\','&#92;');
const extensions=new Set(['.jsx','.tsx','.vue','.html']);
const excluded=new Set(['node_modules','dist','build','coverage','vendor']);
// Conservative lexical map: expression-generated JSX is intentionally not editable.
function literalStarts(source,format){
  const starts=new Set(),stack=[];let i=0,limit=source.length,markup=format==='.html'||format==='.vue';
  if(format==='.vue'){const template=/<template(?:\s[^>]*)?>/.exec(source);if(!template)return starts;i=template.index+template[0].length;limit=source.lastIndexOf('</template>');if(limit<i)return starts;}
  function quoted(at){const q=source[at++];while(at<limit){if(source[at]==='\\'){at+=2;continue;}if(source[at++]===q)return at;}return limit;}
  function expression(at){let depth=1;at++;while(at<limit&&depth){const c=source[at];if(c==='"'||c==="'"||c==='`'){at=quoted(at);continue;}if(source.startsWith('/*',at)){const end=source.indexOf('*/',at+2);at=end<0?limit:end+2;continue;}if(source.startsWith('//',at)){const end=source.indexOf('\n',at+2);at=end<0?limit:end+1;continue;}if(c==='{')depth++;if(c==='}')depth--;at++;}return at;}
  while(i<limit){
    if(source.startsWith('<!--',i)){const end=source.indexOf('-->',i+4);i=end<0?limit:end+3;continue;}
    if(!markup&&!stack.length){
      if(source[i]==='"'||source[i]==="'"||source[i]==='`'){i=quoted(i);continue;}
      if(source.startsWith('//',i)){const end=source.indexOf('\n',i+2);i=end<0?limit:end+1;continue;}
      if(source.startsWith('/*',i)){const end=source.indexOf('*/',i+2);i=end<0?limit:end+2;continue;}
      if(source[i]==='/'){let end=i+1;while(end<limit){if(source[end]==='\\'){end+=2;continue;}if(source[end++]==='/')break;}i=end;continue;}
    }
    if(stack.length&&source[i]==='{'){i=expression(i);continue;}
    const tag=/^<(\/?)([A-Za-z][\w.-]*|)(?=[\s/>])/.exec(source.slice(i));
    if(!tag){i++;continue;}
    if(!markup&&!stack.length&&!/(?:=>|return|\(|=|\?|:)\s*$/.test(source.slice(0,i))){i++;continue;}
    let end=i+tag[0].length;for(;end<limit;end++){if(source[end]==='"'||source[end]==="'"){end=quoted(end)-1;continue;}if(source[end]==='{'){end=expression(end)-1;continue;}if(source[end]==='>')break;}
    if(end>=limit)break;
    if(tag[1])stack.pop();else{
      starts.add(i);const name=tag[2];
      if(['script','style'].includes(name)){const close=source.indexOf('</'+name,end);i=close<0?limit:source.indexOf('>',close)+1;continue;}
      if(source[end-1]!=='/'&&!['img','input','br','hr','meta','link','area','base','embed','param','source','track','wbr'].includes(name))stack.push(name);
    }
    i=end+1;
  }
  return starts;
}
const alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
function vlq(number){let value=number<0?-number*2+1:number*2,result='';do{let digit=value%32;value=Math.floor(value/32);if(value)digit|=32;result+=alphabet[digit];}while(value);return result;}
function insertionMap(source,file,edits){
  const lengths=new Map(edits.map(edit=>[edit.at,edit.text.length]));
  let originalLine=0,originalColumn=0,previousLine=0,previousColumn=0,generatedColumn=0,lastGenerated=0,line=[],lines=[];
  // A segment for every original character keeps JSX compiler diagnostics exact after injection.
  for(let i=0;i<source.length;i++){
    generatedColumn+=lengths.get(i)||0;
    if(source[i]==='\n'){lines.push(line.join(','));line=[];originalLine++;originalColumn=0;generatedColumn=0;lastGenerated=0;continue;}
    line.push(vlq(generatedColumn-lastGenerated)+'A'+vlq(originalLine-previousLine)+vlq(originalColumn-previousColumn));
    lastGenerated=generatedColumn;previousLine=originalLine;previousColumn=originalColumn;generatedColumn++;originalColumn++;
  }
  lines.push(line.join(','));return {version:3,sources:[file],sourcesContent:[source],names:[],mappings:lines.join(';')};
}
export class SourceProject {
  constructor(root){this.root=fs.realpathSync(root);this.undo=[];this.redo=[];this.automatic=new Map();}
  file(relative){
    if(typeof relative!=='string'||path.isAbsolute(relative)||relative.split(/[\\/]/).some(p=>p==='..'||p.startsWith('.')||excluded.has(p)))throw Error('Source path is not allowed');
    const file=path.join(this.root,relative);
    if(!extensions.has(path.extname(file)))throw Error('Unsupported source format');
    let part=this.root;for(const segment of relative.split(path.sep)){part=path.join(part,segment);if(fs.lstatSync(part).isSymbolicLink())throw Error('Symlink source is not allowed');}
    if(fs.realpathSync(file)!==file||!fs.statSync(file).isFile())throw Error('Invalid source file');return file;
  }
  read(relative){const file=this.file(relative);if(fs.statSync(file).size>2000000)throw Error('Source exceeds 2 MB');const raw=fs.readFileSync(file),source=raw.toString('utf8');if(!Buffer.from(source,'utf8').equals(raw))throw Error('Source must be valid UTF-8');return {file,source,hash:digest(source)};}
  files(directory=this.root){return fs.readdirSync(directory,{withFileTypes:true}).flatMap(entry=>{if(entry.name.startsWith('.')||excluded.has(entry.name)||entry.isSymbolicLink())return [];const full=path.join(directory,entry.name);return entry.isDirectory()?this.files(full):extensions.has(path.extname(full))?[path.relative(this.root,full)]:[];});}
  instrument(relative,source){
    const record=this.read(relative);
    // Only map actual file bytes. Other plugins may produce virtual/transformed modules.
    if(record.source!==source||source.length>500000)return null;
    for(const [key,binding] of this.automatic)if(binding.file===relative)this.automatic.delete(key);
    const edits=[];
    for(const start of literalStarts(source,path.extname(relative))){
      if(edits.length>=256)break;
      const match=/^<([a-z][\w-]*)\b/.exec(source.slice(start));if(!match)continue;
      const key='aco-auto-'+digest(relative+':'+record.hash+':'+start).slice(0,24),at=start+match[0].length;
      const marker=' data-aco-edit="'+key+'"';
      const virtual=source.slice(0,at)+marker+source.slice(at);
      let node;try{node=this.locate(virtual,key,path.extname(relative));}catch{continue;}
      // An explicit marker remains authoritative. Only literal leaf elements are auto-bound.
      if(/\bdata-aco-edit\s*=/.test(source.slice(start,node.end-marker.length+1))||/[<>{}]/.test(node.content)||!node.content.trim())continue;
      this.automatic.set(key,{file:relative,hash:record.hash,key,start,at,marker});edits.push({at,text:marker});
    }
    if(!edits.length)return null;
    let code=source;for(const edit of edits.sort((a,b)=>b.at-a.at))code=code.slice(0,edit.at)+edit.text+code.slice(edit.at);
    return {code,map:insertionMap(source,relative,edits)};
  }
  automaticNode(record,key){
    const binding=this.automatic.get(key);if(!binding)return null;
    if(binding.file!==path.relative(this.root,record.file)||binding.hash!==record.hash)throw Error('Automatic binding changed; reselect the element');
    const {at,marker}=binding,virtual=record.source.slice(0,at)+marker+record.source.slice(at);
    const node=this.locate(virtual,key,path.extname(record.file));
    return {...node,end:node.end-marker.length,close:node.close-marker.length,opening:node.opening.replace(marker,'')};
  }
  locate(source,key,format='.jsx'){
    if(!/^[a-zA-Z][\w-]{0,79}$/.test(key))throw Error('Invalid editable key');
    const marker=new RegExp('\\bdata-aco-edit\\s*=\\s*(["\'])'+key+'\\1','g');const found=[...source.matchAll(marker)];
    if(found.length!==1)throw Error('Editable key must occur exactly once in its source file');
    const offset=found[0].index,start=source.lastIndexOf('<',offset),open=source.slice(start,offset);
    if(!literalStarts(source,format).has(start)||start<0||!/^<[a-z][\w-]*(?:\s[^<>]*)?$/.test(open))throw Error('Use a literal marker on a native element');
    const tag=/^<([a-z][\w-]*)/.exec(open)[1];let end=offset+found[0][0].length,quote='',depth=0;
    for(;end<source.length;end++){const c=source[end];if(quote){if(c==='\\'){end++;continue;}if(c===quote)quote='';continue;}if(c==='"'||c==="'"){quote=c;continue;}if(c==='{')depth++;if(c==='}')depth--;if(c==='>'&&depth===0)break;}
    if(end>=source.length||source[end-1]==='/')throw Error('Select an element with a closing tag');
    const close=source.indexOf('</'+tag,end+1);if(close<0)throw Error('Closing tag missing');
    const content=source.slice(end+1,close);return {start,end,close,tag,content,opening:source.slice(start,end+1)};
  }
  resolve(key){if(this.automatic.has(key)){const binding=this.automatic.get(key),record=this.read(binding.file);this.automaticNode(record,key);return {file:binding.file,hash:binding.hash,key};}if(typeof key!=='string'||!/^[a-zA-Z][\w-]{0,79}$/.test(key))throw Error('Invalid editable key');const matches=[];for(const file of this.files()){const record=this.read(file);if(!record.source.includes(key))continue;try{this.locate(record.source,key,path.extname(file));matches.push({file,hash:record.hash,key});}catch(error){if(record.source.includes('data-aco-edit')&&new RegExp('data-aco-edit\\s*=\\s*["\']'+key+'["\']').test(record.source))throw error;}}
    if(matches.length!==1)throw Error(matches.length?'Editable key is duplicated across files':'No literal source binding found');return matches[0];}
  write(file,expected,next){if(fs.readFileSync(file,'utf8')!==expected)throw Error('Source changed externally; reselect the element');const temporary=path.join(path.dirname(file),'.aco-'+crypto.randomBytes(10).toString('hex'));try{fs.writeFileSync(temporary,next,{flag:'wx',mode:fs.statSync(file).mode});fs.renameSync(temporary,file);}finally{if(fs.existsSync(temporary))fs.unlinkSync(temporary);}}
  apply(request){
    const record=this.read(request.file);if(request.hash!==record.hash)throw Error('Source changed; reselect before editing');
    const node=this.automaticNode(record,request.key)||this.locate(record.source,request.key,path.extname(record.file)),value=request.value;
    if(typeof value!=='string'||value.length>20000)throw Error('Invalid value');let next;
    if(request.kind==='text'){
      if(/[<>{}]/.test(node.content))throw Error('Dynamic or nested text must be edited in the source editor');
      next=record.source.slice(0,node.end+1)+escaped(value)+record.source.slice(node.close);
    }else if(request.kind==='class'){
      if(!/^[\w\s:\-\[\]#.%/!(),]+$/.test(value)&&value!=='')throw Error('Unsupported class value');
      const attr=/\s(className|class)\s*=\s*(["'])(.*?)\2/s,existing=attr.exec(node.opening);
      if(/\s(?:className|class)\s*=\s*(?:\{|[^"'\s])/.test(node.opening)||/\s(?::class|v-bind:class)\s*=/.test(node.opening))throw Error('Dynamic classes must be edited in source');
      const name=path.extname(record.file)==='.vue'||path.extname(record.file)==='.html'?'class':'className';
      const opening=existing?node.opening.replace(attr,` ${existing[1]}="${escaped(value)}"`):node.opening.slice(0,-1)+` ${name}="${escaped(value)}">`;
      next=record.source.slice(0,node.start)+opening+record.source.slice(node.end+1);
    }else throw Error('Unsupported edit');
    if(Buffer.byteLength(next)>2000000)throw Error('Edited source exceeds 2 MB');
    this.write(record.file,record.source,next);this.undo.push({file:request.file,before:record.source,after:next});this.undo=this.undo.slice(-50);this.redo=[];return {saved:true,hash:digest(next),file:request.file};
  }
  history(direction){if(!['undo','redo'].includes(direction))throw Error('Invalid history operation');const from=this[direction],to=this[direction==='undo'?'redo':'undo'];if(!from.length)throw Error('No '+direction+' available');const item=from.at(-1);this.write(this.file(item.file),direction==='undo'?item.after:item.before,direction==='undo'?item.before:item.after);from.pop();to.push(item);return {saved:true,file:item.file};}
}
export function auditSnapshot(snapshot){
  if(!snapshot||snapshot.schema!==2||!Array.isArray(snapshot.elements)||snapshot.elements.length>5000)throw Error('Expected at most 5000 measured DOM elements');
  const directory=fs.existsSync(path.join(assets,'audit'))?path.join(assets,'audit'):path.resolve(assets,'../../scripts');
  const process=spawnSync('python3',['-c',"import sys,json;sys.path.insert(0,sys.argv[1]);from audit_design import audit;print(json.dumps(audit(json.load(sys.stdin))))",directory],{input:JSON.stringify(snapshot),encoding:'utf8',timeout:10000,maxBuffer:4000000});
  if(process.error)throw Error('Design review needs Python 3: '+process.error.message);
  if(process.status!==0)throw Error('Design review failed: '+(process.stderr||'invalid measurements').slice(-500));
  return JSON.parse(process.stdout);
}
export default function acoLive({automatic=true}={}){
  let project,base='/',queue=Promise.resolve();const token=crypto.randomBytes(32).toString('hex');
  return {name:'aco-source-live',apply:'serve',enforce:'pre',
    configResolved(config){if(config.server.host&&!['127.0.0.1','localhost','::1'].includes(config.server.host))throw Error('ACO Live requires a loopback Vite host');if(!config.base.startsWith('/'))throw Error('ACO Live requires a local base path');project=new SourceProject(config.root);base=config.base.endsWith('/')?config.base:config.base+'/';},
    transform(source,id){if(!automatic||id.includes('?')||!extensions.has(path.extname(id)))return null;const relative=path.relative(project.root,id);try{return project.instrument(relative,source);}catch{return null;}},
    transformIndexHtml(){return [{tag:'script',attrs:{type:'module',src:base+'__aco/client.js'},injectTo:'body'}];},
    configureServer(server){server.middlewares.use((req,res,next)=>{
      const prefix=base+'__aco/',url=new URL(req.url,'http://localhost');if(!url.pathname.startsWith(prefix))return next();
      const host=req.headers.host||'',remote=req.socket.remoteAddress||'';
      if(!/^(?:localhost|127\.0\.0\.1|\[::1\])(?::\d+)?$/.test(host)||!['127.0.0.1','::1','::ffff:127.0.0.1'].includes(remote)){res.writeHead(403);res.end();return;}
      const route=url.pathname.slice(prefix.length),send=(status,data,type='application/json')=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(typeof data==='string'?data:JSON.stringify(data));};
      if(req.method==='GET'&&route==='live'){send(200,fs.readFileSync(path.join(assets,'editor.html'),'utf8').replaceAll('ACO_TOKEN',token).replaceAll('ACO_BASE',base),'text/html; charset=utf-8');return;}
      if(req.method==='GET'&&['client.js','editor.js','runtime-review.mjs','browser-probe.mjs'].includes(route)){send(200,fs.readFileSync(path.join(assets,route),'utf8'),'text/javascript');return;}
      if(req.method!=='POST'||req.headers['x-aco-token']!==token||!['http://'+host,'https://'+host].includes(req.headers.origin)){send(403,{error:'Rejected request'});return;}
      let raw='',size=0;req.on('data',chunk=>{size+=chunk.length;if(size>(route==='audit'?2000000:30000)){req.destroy();return;}raw+=chunk;});
      req.on('end',()=>{queue=queue.then(()=>{try{const data=JSON.parse(raw),result=route==='audit'?auditSnapshot(data.snapshot):route==='resolve'?project.resolve(data.key):route==='edit'?project.apply(data):['undo','redo'].includes(route)?project.history(route):null;if(!result)throw Error('Unknown operation');send(200,result);}catch(e){send(409,{error:e.message});}});});
    });}
  };
}
