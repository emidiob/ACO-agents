// Selection is active only inside the editor frame. The normal application stays interactive.
if(window.parent!==window){
  let selecting=true;
  addEventListener('message',event=>{if(event.origin===location.origin&&event.source===parent&&event.data?.kind==='aco-mode')selecting=event.data.selecting;});
  document.addEventListener('click',event=>{if(!selecting)return;const el=event.target.closest('[data-aco-edit]');if(!el)return;event.preventDefault();event.stopImmediatePropagation();parent.postMessage({kind:'aco-select',key:el.getAttribute('data-aco-edit'),text:el.textContent,classes:el.getAttribute('class')||''},location.origin);},true);
}
