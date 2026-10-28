import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import acoLive,{SourceProject} from '../skills/aco-webdesign/assets/framework-live/aco-vite.mjs';
function fixture(t,source,filename='App.jsx'){const root=fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()),'aco-source-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));fs.writeFileSync(path.join(root,filename),source);return new SourceProject(root);}
test('React source edit preserves surrounding code and escapes literal braces',t=>{const p=fixture(t,'export default () => <main><h1 data-aco-edit="hero">Hello</h1><p>{value}</p></main>');const binding=p.resolve('hero');p.apply({...binding,kind:'text',value:'<Hello> {name}'});assert.match(p.read('App.jsx').source,/&lt;Hello&gt; &#123;name&#125;/);assert.match(p.read('App.jsx').source,/<p>{value}<\/p>/);p.history('undo');assert.equal(p.read('App.jsx').hash,binding.hash);p.history('redo');assert.match(p.read('App.jsx').source,/&#123;/);});
test('Vue binding and literal classes',t=>{const p=fixture(t,'<script setup>const value=1</script><template><h1 data-aco-edit="hero" class="old">Hello</h1></template>','App.vue');p.apply({...p.resolve('hero'),kind:'class',value:'new large'});assert.match(p.read('App.vue').source,/class="new large"/);});
test('rejects dynamic content, nested markup and dynamic classes',t=>{for(const source of ['<h1 data-aco-edit="hero">{name}</h1>','<h1 data-aco-edit="hero"><b>Hello</b></h1>']){const p=fixture(t,'export default () => '+source);assert.throws(()=>p.apply({...p.resolve('hero'),kind:'text',value:'No'}),/Dynamic or nested/);}const p=fixture(t,'export default () => <h1 data-aco-edit="hero" className={classes}>Hello</h1>');assert.throws(()=>p.apply({...p.resolve('hero'),kind:'class',value:'new'}),/Dynamic classes/);});
test('rejects markers in strings and comments',t=>{for(const source of ["const example = '<h1 data-aco-edit=\"hero\">Hello</h1>';",'// <h1 data-aco-edit="hero">Hello</h1>','/* <h1 data-aco-edit="hero">Hello</h1> */', 'const example=/<h1 data-aco-edit="hero">Hello<\\/h1>/;']){const p=fixture(t,source);assert.throws(()=>p.resolve('hero'),/literal marker/);}});
test('detects stale edits and stale history',t=>{const p=fixture(t,'export default () => <h1 data-aco-edit="hero">Hello</h1>');const binding=p.resolve('hero');p.apply({...binding,kind:'text',value:'Changed'});assert.throws(()=>p.apply({...binding,kind:'text',value:'Stale'}),/Source changed/);fs.appendFileSync(p.file('App.jsx'),'\n// external');assert.throws(()=>p.history('undo'),/changed externally/);});
test('rejects duplicate bindings, outside files and symlinks',t=>{const p=fixture(t,'export default () => <h1 data-aco-edit="hero">Hello</h1>');fs.copyFileSync(p.file('App.jsx'),path.join(p.root,'Other.jsx'));assert.throws(()=>p.resolve('hero'),/duplicated/);assert.throws(()=>p.read('../other.jsx'),/not allowed/);fs.symlinkSync(p.file('App.jsx'),path.join(p.root,'Link.jsx'));assert.throws(()=>p.read('Link.jsx'),/Symlink/);});
test('development only plugin refuses public host',()=>{const plugin=acoLive();assert.equal(plugin.apply,'serve');assert.throws(()=>plugin.configResolved({root:'.',base:'/',server:{host:'0.0.0.0'}}),/loopback/);});

test('HTTP bridge authenticates edits and binds mutations to the same origin',async t=>{
  const http=await import('node:http');const project=fixture(t,'export default () => <h1 data-aco-edit="hero">Hello</h1>');const plugin=acoLive();plugin.configResolved({root:project.root,base:'/',server:{host:'127.0.0.1'}});let middleware;plugin.configureServer({middlewares:{use:fn=>middleware=fn}});
  const server=http.createServer((req,res)=>middleware(req,res,()=>{res.writeHead(404);res.end();}));await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));t.after(()=>new Promise(resolve=>server.close(resolve)));const origin='http://127.0.0.1:'+server.address().port;
  const html=await(await fetch(origin+'/__aco/live')).text(),token=/token:'([a-f0-9]{64})'/.exec(html)[1];
  assert.equal((await fetch(origin+'/__aco/resolve',{method:'POST',body:'{"key":"hero"}'})).status,403);
  const headers={'Content-Type':'application/json','Origin':origin,'X-ACO-Token':token};const binding=await(await fetch(origin+'/__aco/resolve',{method:'POST',headers,body:'{"key":"hero"}'})).json();assert.equal(binding.file,'App.jsx');
  const response=await fetch(origin+'/__aco/edit',{method:'POST',headers,body:JSON.stringify({...binding,kind:'text',value:'Saved through HTTP'})});assert.equal(response.status,200);assert.match(project.read('App.jsx').source,/Saved through HTTP/);
  assert.equal((await fetch(origin+'/__aco/undo',{method:'POST',headers:{...headers,Origin:'https://other.example'},body:'{}'})).status,403);
});

test('automatic React mapping edits original bytes without persisting instrumentation',t=>{
  const source='export default () => <main><h1>Hello</h1><p>{name}</p><p>World</p></main>',p=fixture(t,source);
  const result=p.instrument('App.jsx',source),keys=[...result.code.matchAll(/data-aco-edit="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(keys.length,2);assert.equal(result.map.sourcesContent[0],source);
  p.apply({...p.resolve(keys[0]),kind:'text',value:'Changed'});
  assert.equal(p.read('App.jsx').source,source.replace('Hello','Changed'));
  assert.throws(()=>p.resolve(keys[1]),/changed/);
  const refreshed=p.instrument('App.jsx',p.read('App.jsx').source);assert.match(refreshed.code,/Changed/);
  p.history('undo');assert.equal(p.read('App.jsx').source,source);
});
test('automatic Vue mapping respects explicit bindings and dynamic text',t=>{
  const source='<template><main><h1 class="old">Hello</h1><p>{{name}}</p><p data-aco-edit="manual">Keep</p></main></template>',p=fixture(t,source,'App.vue');
  const result=p.instrument('App.vue',source),key=/data-aco-edit="(aco-auto-[^"]+)"/.exec(result.code)[1];
  assert.equal([...result.code.matchAll(/aco-auto-/g)].length,1);
  p.apply({...p.resolve(key),kind:'class',value:'new'});assert.equal(p.read('App.vue').source,source.replace('class="old"','class="new"'));
  assert.equal(p.resolve('manual').file,'App.vue');
});
test('automatic bindings exclude examples, comments, virtual sources and unsafe paths',t=>{
  const source='const sample = "<h1>Example</h1>"; /* <h2>Comment</h2> */ export default () => <p>Actual</p>',p=fixture(t,source);
  const result=p.instrument('App.jsx',source);assert.equal([...result.code.matchAll(/aco-auto-/g)].length,1);
  assert.equal(p.instrument('App.jsx',source+'\n'),null);
  assert.throws(()=>p.instrument('../Outside.jsx',source),/not allowed/);
  const plugin=acoLive({automatic:false});plugin.configResolved({root:p.root,base:'/',server:{host:'127.0.0.1'}});assert.equal(plugin.transform(source,p.file('App.jsx')),null);
});

test('frame summary distinguishes expected refresh rates and rejects invalid inputs',async()=>{
  const {summarizeFrames}=await import('../skills/aco-webdesign/assets/framework-live/runtime-review.mjs');
  const normal=summarizeFrames([16.67,16.67,16.67],60);assert.equal(normal.over_budget,0);assert.equal(normal.estimated_missed_refreshes,0);
  const stalled=summarizeFrames([16.67,50,16.67],60);assert.equal(stalled.over_budget,1);assert.equal(stalled.estimated_missed_refreshes,2);
  assert.equal(summarizeFrames([8.33,8.33,16.67],120).estimated_missed_refreshes,1);
  assert.equal(summarizeFrames([]).median_ms,null);assert.throws(()=>summarizeFrames([1],0),/refresh rate/);
});

test('rendered audit uses the native predicates and exposes missing measurements',async()=>{
  const {auditSnapshot}=await import('../skills/aco-webdesign/assets/framework-live/aco-vite.mjs');
  const result=auditSnapshot({schema:2,elements:[{index:0,tag:'p',text:'Low contrast',color:'#aaaaaa',effectiveBackground:'#ffffff',fontSize:16}],viewport:{width:1000,height:700}});
  assert.ok(result.findings.some(f=>f.rule==='text-contrast'));assert.ok(result.not_evaluated.some(f=>f.id==='runtime-error'));
  assert.throws(()=>auditSnapshot({schema:2,elements:Array(5001).fill({})}),/5000/);
});
