/* Original ACO component behaviors. No network calls or framework dependencies. */
(() => {
  const all = (q, root=document) => Array.from(root.querySelectorAll(q));
  const on = (q, event, fn) => all(q).forEach(el => el.addEventListener(event, e => fn(el,e)));
  on('[data-catalog-search]', 'input', el => all('.example').forEach(section => { section.hidden=!section.querySelector('h2').textContent.toLowerCase().includes(el.value.toLowerCase()); }));
  on('[data-open]', 'click', el => document.getElementById(el.dataset.open).showModal());
  on('[data-counter]', 'click', el => {const out=el.querySelector('output');out.value=String(+out.value+1);});
  on('[data-zoom]', 'click', el => {const out=el.parentElement.querySelector('output');out.value=Math.max(50,Math.min(200,parseInt(out.value)+Number(el.dataset.zoom)))+'%';});
  on('[data-files]', 'change', el => {el.closest('label').nextElementSibling.value=Array.from(el.files).map(f=>f.name).join(', ') || 'No files selected';});
  on('[data-step]', 'click', el => {
    const root=el.closest('[data-carousel]'),slides=all('[data-slide]',root),current=slides.findIndex(s=>!s.hidden),next=(current+Number(el.dataset.step)+slides.length)%slides.length;
    slides.forEach((s,i)=>{s.hidden=i!==next;});root.querySelector('output').value=`${next+1} / ${slides.length}`;
  });
  on('[data-copy]', 'click', async el => {const out=el.parentElement.querySelector('output');try{await navigator.clipboard.writeText(el.parentElement.querySelector('code').textContent);out.value='Copied';}catch{out.value='Clipboard unavailable. Select and copy the code manually.';}});
  all('[data-filter-list]').forEach(root=>{
    const input=root.querySelector('input'),buttons=all('li button',root),out=root.querySelector('output');
    const visible=()=>buttons.filter(b=>!b.parentElement.hidden);
    input.addEventListener('input',()=>{buttons.forEach(b=>{b.parentElement.hidden=!b.textContent.toLowerCase().includes(input.value.toLowerCase());});out.value=visible().length ? `${visible().length} options` : 'No matches';});
    root.addEventListener('keydown',e=>{const list=visible(),i=list.indexOf(document.activeElement);if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(list.length)list[(i+(e.key==='ArrowDown'?1:-1)+list.length)%list.length].focus();}if(e.key==='Escape'){input.value='';buttons.forEach(b=>{b.parentElement.hidden=false;});out.value='';input.focus();}});
    buttons.forEach(b=>b.addEventListener('click',()=>{input.value=b.textContent;out.value=`Selected ${b.textContent}`;}));
  });
  all('[data-menu]').forEach(root=>{
    const trigger=root.querySelector('button'),panel=root.querySelector('div'),buttons=all('button',panel),out=root.querySelector('output');
    const set=(open,focus=false)=>{panel.hidden=!open;trigger.setAttribute('aria-expanded',String(open));if(focus)(open?buttons[0]:trigger).focus();};
    trigger.addEventListener('click',()=>set(panel.hidden));
    if(panel.id.startsWith('context-menu'))root.addEventListener('contextmenu',e=>{e.preventDefault();set(true,true);});
    root.addEventListener('keydown',e=>{if(e.key==='Escape'){set(false,true);e.preventDefault();}if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();set(true);let i=buttons.indexOf(document.activeElement);i=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length;buttons[i].focus();}});
    buttons.forEach(b=>b.addEventListener('click',()=>{out.value=`Selected ${b.textContent}`;set(false,true);}));
    document.addEventListener('pointerdown',e=>{if(!root.contains(e.target))set(false);});
    root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget))set(false);});
  });
  on('[data-direction] button','click',el=>{const p=el.parentElement.querySelector('p');p.dir=p.dir==='rtl'?'ltr':'rtl';});
  on('[data-validation]','submit',(el,e)=>{e.preventDefault();el.querySelector('output').value='Valid email address';});
  on('[data-otp]','input',el=>{el.value=el.value.replace(/\D/g,'').slice(0,6);el.closest('label').nextElementSibling.value=el.value.length===6?'Code complete':`${el.value.length} of 6 digits`;});
  all('.tooltip,.hover-card').forEach(root=>{
    root.addEventListener('keydown',e=>{if(e.key==='Escape')root.classList.add('dismissed');});
    root.addEventListener('pointerleave',()=>root.classList.remove('dismissed'));
    root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget))root.classList.remove('dismissed');});
  });
  on('[data-messages] form','submit',(form,e)=>{e.preventDefault();const root=form.closest('[data-messages]'),log=root.querySelector('[role=log]'),input=form.querySelector('input'),p=document.createElement('p');p.textContent=input.value;log.append(p);log.scrollTop=log.scrollHeight;input.value='';input.focus();});
  all('[data-pagination]').forEach(root=>{let page=1;const buttons=all('button',root);const update=()=>{root.querySelector('output').value=`Page ${page} of 5`;buttons[0].disabled=page===1;buttons[1].disabled=page===5;};buttons.forEach(b=>b.addEventListener('click',()=>{page=Math.max(1,Math.min(5,page+Number(b.dataset.pageStep)));update();}));update();});
  on('[data-questionnaire]','submit',(form,e)=>{e.preventDefault();form.querySelector('output').value='Selected: '+form.querySelector('input:checked').value;});
  on('[data-resize] input','input',el=>{el.closest('[data-resize]').querySelector('.split').style.gridTemplateColumns=`${el.value}% 1fr`;});
  on('[data-sidebar] button','click',el=>{const nav=el.parentElement.querySelector('nav');nav.hidden=!nav.hidden;el.setAttribute('aria-expanded',String(!nav.hidden));});
  on('[data-range]','input',el=>{el.closest('label').nextElementSibling.value=el.value;});
  on('[data-toast] > button','click',el=>{const row=document.createElement('p'),dismiss=document.createElement('button');row.append(document.createTextNode('Changes saved. '));dismiss.textContent='Dismiss';dismiss.addEventListener('click',()=>{row.remove();el.focus();});row.append(dismiss);el.parentElement.querySelector('[role=status]').append(row);});
  on('[data-sort] button','click',el=>{const table=el.closest('table'),head=el.closest('th'),asc=head.getAttribute('aria-sort')!=='ascending',col=+el.dataset.column,body=table.tBodies[0];all('th',table).forEach(h=>h.setAttribute('aria-sort','none'));head.setAttribute('aria-sort',asc?'ascending':'descending');Array.from(body.rows).sort((a,b)=>a.cells[col].textContent.localeCompare(b.cells[col].textContent,undefined,{numeric:true})*(asc?1:-1)).forEach(row=>body.append(row));});
  all('[data-tabs]').forEach(root=>{const tabs=all('[role=tab]',root);const select=tab=>{tabs.forEach(t=>{const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!active;});};tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>select(tab));tab.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const next=tabs[e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length];select(next);next.focus();}});});});
  on('[data-count]','input',el=>{el.closest('label').nextElementSibling.value=`${el.value.length} / ${el.maxLength}`;});
  on('[data-toggle]','click',el=>el.setAttribute('aria-pressed',String(el.getAttribute('aria-pressed')!=='true')));
  on('[data-toggle-group] button','click',el=>all('button',el.parentElement).forEach(b=>b.setAttribute('aria-pressed',String(b===el))));
})();
