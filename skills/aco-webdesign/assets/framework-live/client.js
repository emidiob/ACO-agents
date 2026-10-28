import probe from './browser-probe.mjs';
import {collectRuntime,inspectTypography} from './runtime-review.mjs';
// Selection is active only inside the editor frame. The normal application stays interactive.
if(window.parent!==window){
  let selecting=false,profiling=false;
  addEventListener('message',event=>{if(event.origin===location.origin&&event.source===parent&&event.data?.kind==='aco-mode')selecting=event.data.selecting;});
  addEventListener('message',async event=>{if(event.origin!==location.origin||event.source!==parent||event.data?.kind!=='aco-profile'||profiling)return;profiling=true;try{const report=await collectRuntime({expectedHz:event.data.expectedHz});parent.postMessage({kind:'aco-profile-result',report},location.origin);}catch(error){parent.postMessage({kind:'aco-profile-result',error:error.message},location.origin);}finally{profiling=false;}});
  addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==parent||event.data?.kind!=='aco-audit')return;parent.postMessage({kind:'aco-audit-snapshot',snapshot:probe()},location.origin);});
  document.addEventListener('click',event=>{if(!selecting)return;const el=event.target.closest('[data-aco-edit]');if(!el)return;event.preventDefault();event.stopImmediatePropagation();parent.postMessage({kind:'aco-select',key:el.getAttribute('data-aco-edit'),text:el.textContent,classes:el.getAttribute('class')||'',typography:inspectTypography(el)},location.origin);},true);
}
