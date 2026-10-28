/* Original ACO effect renderer: one bounded animation loop, no external dependencies. */
(() => {
  const reduced=matchMedia('(prefers-reduced-motion: reduce)'),states=[];
  const chars=Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789');
  const seed=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};
  document.querySelectorAll('[data-effect]').forEach((stage,index)=>{
    const text=stage.querySelector('.effect-text'),canvas=stage.querySelector('canvas'),kind=stage.dataset.effect;
    const state={stage,text,canvas,ctx:canvas?.getContext('2d'),kind,elapsed:0,paused:false,visible:true,duration:Number(stage.dataset.duration)||2400,original:text?.textContent||'',index,ripples:[],point:[0,0]};
    if(text&&['word-reveal','text-wave'].includes(kind)){
      text.setAttribute('aria-label',state.original);text.textContent='';
      (kind==='word-reveal'?state.original.split(/(\s+)/):Array.from(state.original)).forEach(c=>{const span=document.createElement('span');span.textContent=c;span.setAttribute('aria-hidden','true');text.append(span);});
    } else if(text&&['typewriter','text-scramble','count-up'].includes(kind)){
      const accessible=document.createElement('span');accessible.className='sr-only';accessible.textContent=kind==='count-up'?'1000':state.original;stage.append(accessible);text.setAttribute('aria-hidden','true');
    }
    if(kind==='magnetic-button'&&text){const button=document.createElement('button');button.className=text.className;button.textContent=text.textContent;text.replaceWith(button);state.text=button;button.addEventListener('click',()=>{button.textContent=button.textContent==='Selected' ? state.original : 'Selected';button.setAttribute('aria-pressed',String(button.textContent==='Selected'));});}
    if(canvas){const resize=()=>{const r=stage.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);canvas.width=Math.max(1,Math.round(r.width*d));canvas.height=Math.max(1,Math.round(r.height*d));state.width=r.width;state.height=r.height;state.ctx.setTransform(d,0,0,d,0,0);};new ResizeObserver(resize).observe(stage);resize();}
    new IntersectionObserver(entries=>{state.visible=entries[0].isIntersecting;},{rootMargin:'80px'}).observe(stage);
    stage.addEventListener('pointermove',e=>{const r=stage.getBoundingClientRect();state.point=[e.clientX-r.left-r.width/2,e.clientY-r.top-r.height/2];if(kind==='pointer-spotlight'&&!reduced.matches&&!state.paused){stage.style.setProperty('--x',(e.clientX-r.left)+'px');stage.style.setProperty('--y',(e.clientY-r.top)+'px');}});
    stage.addEventListener('pointerleave',()=>{state.point=[0,0];stage.style.removeProperty('--x');stage.style.removeProperty('--y');});
    stage.addEventListener('click',e=>{if(kind==='ripple-field'&&!reduced.matches&&!state.paused){const r=stage.getBoundingClientRect();state.ripples.push({x:e.clientX-r.left,y:e.clientY-r.top,t:state.elapsed});state.ripples=state.ripples.slice(-12);}});
    stage.addEventListener('keydown',e=>{if(kind==='ripple-field'&&(e.key==='Enter'||e.key===' ')){e.preventDefault();if(!reduced.matches&&!state.paused)state.ripples.push({x:state.width/2,y:state.height/2,t:state.elapsed});}});
    const article=stage.closest('article');article.querySelector('[data-replay]').addEventListener('click',()=>{state.elapsed=0;state.ripples=[];state.paused=false;article.querySelector('[data-pause]').setAttribute('aria-pressed','false');});
    article.querySelector('[data-pause]').addEventListener('click',e=>{state.paused=!state.paused;e.currentTarget.setAttribute('aria-pressed',String(state.paused));});states.push(state);
  });
  function draw(s,staticMode){
    const t=staticMode?0:s.elapsed/1000,p=staticMode?1:Math.min(1,s.elapsed/s.duration),eased=1-(1-p)**3;
    if(s.text){
      if(s.kind==='word-reveal')Array.from(s.text.children).forEach((span,i)=>{const amount=staticMode?1:Math.min(1,Math.max(0,(p-i/(s.text.children.length+2))*(s.text.children.length+2)/3));span.style.transform=`translateY(${(1-amount)*35}px)`;span.style.opacity=String(amount);});
      if(s.kind==='text-scramble')s.text.textContent=Array.from(s.original).map((c,i)=>c===' '||p>=i/s.original.length?c:chars[Math.floor(seed(i+Math.floor(t*20))*chars.length)]).join('');
      if(s.kind==='count-up')s.text.textContent=Math.round(1000*eased).toLocaleString();
      if(s.kind==='typewriter')s.text.textContent=Array.from(s.original).slice(0,Math.ceil(p*s.original.length)).join('');
      if(s.kind==='text-wave')Array.from(s.text.children).forEach((span,i)=>span.style.transform=`translateY(${staticMode?0:Math.sin(t*3-i*.45)*8}px)`);
      if(s.kind==='gradient-text')s.text.style.backgroundPosition=`${(t*25)%200}% 50%`;
      if(s.kind==='perspective-tilt')s.text.style.transform=staticMode?'none':`rotateX(${-s.point[1]*.08}deg) rotateY(${s.point[0]*.08}deg)`;
      if(s.kind==='magnetic-button')s.text.style.transform=staticMode?'none':`translate(${Math.max(-20,Math.min(20,s.point[0]*.12))}px,${Math.max(-15,Math.min(15,s.point[1]*.12))}px)`;
      return;
    }
    const c=s.ctx,w=s.width,h=s.height;if(!c)return;c.clearRect(0,0,w,h);c.lineWidth=1;c.strokeStyle='#95bff8';c.fillStyle='#a4cdff';
    if(s.kind==='particle-field'){
      const points=Array.from({length:36},(_,i)=>[(seed(i)*w+t*(8+seed(i+90)*15))%w,(seed(i+200)*h+Math.sin(t+i)*8+h)%h]);
      points.forEach(([x,y],i)=>{c.beginPath();c.arc(x,y,2,0,Math.PI*2);c.fill();for(let j=i+1;j<points.length;j++){const [a,b]=points[j],distance=Math.hypot(a-x,b-y);if(distance<70){c.globalAlpha=(1-distance/70)*.5;c.beginPath();c.moveTo(x,y);c.lineTo(a,b);c.stroke();c.globalAlpha=1;}}});
    }else if(s.kind==='flow-lines'){
      for(let row=0;row<14;row++){c.beginPath();for(let x=0;x<=w;x+=5){const y=h*row/14+Math.sin(x*.018+t+row*.3)*20;c.lineTo(x,y);}c.stroke();}
    }else if(s.kind==='orbit-system'){
      for(let i=0;i<6;i++){const rx=25+i*20,ry=12+i*10,angle=t*(.3+i*.09)+i;c.globalAlpha=.35;c.beginPath();c.ellipse(w/2,h/2,rx,ry,0,0,Math.PI*2);c.stroke();c.globalAlpha=1;c.beginPath();c.arc(w/2+Math.cos(angle)*rx,h/2+Math.sin(angle)*ry,4,0,Math.PI*2);c.fill();}
    }else if(s.kind==='ripple-field'){
      const waves=staticMode?[{x:w/2,y:h/2,t:-1000}]:s.ripples;s.ripples=s.ripples.filter(r=>s.elapsed-r.t<2500);
      waves.forEach(r=>{const age=staticMode?1:(s.elapsed-r.t)/1000;c.globalAlpha=Math.max(0,1-age/2.5);c.beginPath();c.arc(r.x,r.y,age*85,0,Math.PI*2);c.stroke();});c.globalAlpha=1;c.font='14px system-ui';c.fillText('Click or press Enter',16,h-16);
    }else if(s.kind==='noise-field'){
      for(let y=0;y<h;y+=5)for(let x=0;x<w;x+=5){const n=seed(x+y*w+Math.floor(t*8));c.fillStyle=`rgb(${Math.round(n*100+60)} ${Math.round(n*100+60)} ${Math.round(n*100+60)})`;c.fillRect(x,y,5,5);}
    }else if(s.kind==='aurora-field'){
      ['#5ab8b099','#656acb99','#be82b299'].forEach((color,i)=>{const x=w*(.25+i*.25)+Math.sin(t*.4+i)*40,y=h/2+Math.cos(t*.3+i)*30,g=c.createRadialGradient(x,y,0,x,y,w*.55);g.addColorStop(0,color);g.addColorStop(1,'transparent');c.fillStyle=g;c.fillRect(0,0,w,h);});
    }else if(s.kind==='dot-wave'){
      for(let y=16;y<h;y+=20)for(let x=16;x<w;x+=20){const radius=2+2*(Math.sin(x*.035+y*.02-t*2)+1)/2;c.beginPath();c.arc(x,y,radius,0,Math.PI*2);c.fill();}
    }
  }
  let previous=performance.now();function frame(now){const delta=Math.min(50,now-previous);previous=now;if(!document.hidden)states.forEach(s=>{if(!s.visible)return;if(!s.paused&&!reduced.matches)s.elapsed+=delta;if(!s.paused||reduced.matches)draw(s,reduced.matches);});requestAnimationFrame(frame);}requestAnimationFrame(frame);
})();
