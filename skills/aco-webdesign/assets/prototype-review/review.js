const config=JSON.parse(document.querySelector('#config').textContent),nav=document.querySelector('#variants'),previews=document.querySelector('#previews'),width=document.querySelector('#width');
const frames=[],buttons=[],notes=[];let selected=0,comparison=false;
function render(){
  frames.forEach((frame,i)=>{frame.closest('article').hidden=!comparison&&selected!==i;frame.style.width=width.value==='fluid'?'100%':width.value+'px';buttons[i].setAttribute('aria-pressed',String(selected===i));});
  document.querySelector('#rationale').textContent=config.variants[selected].rationale||'';
  previews.classList.toggle('comparison',comparison);document.querySelector('#compare').setAttribute('aria-pressed',String(comparison));
}
config.variants.forEach((variant,i)=>{
  const button=document.createElement('button');button.textContent=variant.name;button.onclick=()=>{selected=i;render();};nav.append(button);buttons.push(button);
  const article=document.createElement('article'),heading=document.createElement('h2'),scroll=document.createElement('div'),frame=document.createElement('iframe'),link=document.createElement('a');
  heading.textContent=variant.name;frame.title=variant.name;frame.src=variant.url;frame.setAttribute('sandbox','allow-scripts allow-forms allow-same-origin allow-modals allow-downloads');frame.referrerPolicy='no-referrer';
  link.textContent='Open prototype';link.href=variant.url;link.target='_blank';link.rel='noopener';scroll.className='frame-scroll';scroll.append(frame);article.append(heading,link,scroll);previews.append(article);frames.push(frame);
});
width.onchange=render;document.querySelector('#compare').onclick=()=>{comparison=!comparison;render();};
document.querySelector('#record').onclick=()=>{const input=document.querySelector('#note'),text=input.value.trim();if(!text){document.querySelector('#status').textContent='Write an observation first.';return;}const entry={variant:config.variants[selected].name,width:width.value,text,recorded_at:new Date().toISOString()};notes.push(entry);const li=document.createElement('li');li.textContent=entry.variant+' · '+entry.width+' · '+text;document.querySelector('#notes').append(li);input.value='';document.querySelector('#status').textContent='Observation recorded in this session.';};
document.querySelector('#download').onclick=()=>{const blob=new Blob([JSON.stringify({schema:1,variants:config.variants,notes},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='aco-prototype-review.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
render();
