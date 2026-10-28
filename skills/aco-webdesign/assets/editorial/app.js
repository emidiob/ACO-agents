const filters=[...document.querySelectorAll('[data-filter]')];
filters.forEach(button=>button.addEventListener('click',()=>{
 filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 let count=0;document.querySelectorAll('[data-kind]').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.kind!==button.dataset.filter;if(!card.hidden)count++;});
 document.querySelector('#results').textContent=`${count} ${count===1?'story':'stories'}`;
}));
const dialog=document.querySelector('#note');let opener;
function openNote(button,title,copy){opener=button;document.querySelector('#dialog-title').textContent=title;document.querySelector('#dialog-copy').textContent=copy;dialog.showModal();}
document.querySelector('#open-note').addEventListener('click',e=>openNote(e.currentTarget,'A note from the editor','This local prototype explores typography, pacing and original illustration. Stories are fictional previews; there is no publishing backend.'));
document.querySelectorAll('[data-story]').forEach(button=>button.addEventListener('click',()=>openNote(button,button.dataset.story,'This is a fictional story preview in the ACO editorial example. Replace it with the actual article and a real content route in your project.')));
document.querySelector('#close-note').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>opener?.focus());
