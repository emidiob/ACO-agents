"""Standalone browser comparison board: user chooses; approval is never inferred."""
from __future__ import annotations
from pathlib import Path
import base64,html,json,mimetypes
from .core import digest

VALID_IMAGE={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.gif':'image/gif'}

def board(packet):
    if not isinstance(packet,dict):raise ValueError('Input must be object')
    title=str(packet.get('title','Visual directions'))
    variants=packet.get('variants')
    if not isinstance(variants,list) or not 2<=len(variants)<=6:raise ValueError('Need 2–6 variants')
    cards=[];ids=set()
    for idx,v in enumerate(variants):
        if not isinstance(v,dict):raise ValueError('Variant must be object')
        sid=str(v.get('id',f'V{idx+1}'));lab=str(v.get('label',sid));desc=str(v.get('description',''))
        if sid in ids:raise ValueError('Duplicate variant IDs')
        ids.add(sid)
        path=v.get('image');img=''
        if path:
            p=Path(path).expanduser().resolve(strict=True)
            if p.suffix.lower() not in VALID_IMAGE or p.stat().st_size>7*1024*1024:raise ValueError('Only bounded PNG/JPEG/WebP/GIF supported')
            src=f"data:{VALID_IMAGE[p.suffix.lower()]};base64,{base64.b64encode(p.read_bytes()).decode()}"
            img=f'<img src="{src}" alt="{html.escape(lab,quote=True)} visual variant" loading="lazy" />'
        else:img='<div class="placeholder">No image supplied — cannot judge visual quality</div>'
        cards.append(f'''<article class="variant" data-id="{html.escape(sid,quote=True)}"><div class="meta"><h2>{html.escape(lab)}</h2><p>{html.escape(desc)}</p></div>{img}<div class="controls"><label>Rating (1–5) <select data-rating="{html.escape(sid,quote=True)}"><option value="">Unrated</option>{''.join(f'<option value="{n}">{n}</option>' for n in range(1,6))}</select></label><label>Why / what to change <textarea data-note="{html.escape(sid,quote=True)}"></textarea></label></div></article>''')
    ids_json=json.dumps([str(v.get('id',f'V{i+1}')) for i,v in enumerate(variants)]).replace('</','<\\/')
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>
    :root{{--bg:#eeede8;--ink:#181817;--border:#aaa8a1;--accent:#9d4127;--focus:#0e59b8}}
    *{{box-sizing:border-box}}html{{font-family:system-ui,sans-serif}}body{{margin:0;background:var(--bg);color:var(--ink)}}
    header{{padding:2rem clamp(1rem,4vw,4rem);border-bottom:1px solid var(--border)}}h1{{font-size:clamp(1.8rem,3vw,3.4rem);letter-spacing:-.05em;margin:0}}.intro{{max-width:68ch;color:#454541}}
    main{{padding:1.25rem clamp(1rem,4vw,4rem);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:2rem;align-items:start}}.variant{{background:white;border:1px solid var(--border);padding:1.2rem}}.variant img{{width:100%;height:auto;display:block;border:1px solid var(--border)}}.meta h2{{font-size:1.2rem;margin:.2rem 0}}.meta p{{color:#555;min-height:2rem}}.controls{{display:grid;gap:1rem;padding-top:1.2rem}}label{{display:grid;gap:.4rem;font-weight:600}}select,textarea{{font:inherit;padding:.5rem;border:1px solid #777;background:white;color:#111}}textarea{{min-height:5rem;resize:vertical}}button{{font:inherit;padding:.8rem 1.2rem;border:1px solid #111;background:#151515;color:white;cursor:pointer}}button:hover{{background:#333}}:focus-visible{{outline:3px solid var(--focus);outline-offset:3px}}.placeholder{{padding:4rem 1rem;background:#ddd;color:#555;text-align:center}}footer{{border-top:1px solid var(--border);padding:1.5rem clamp(1rem,4vw,4rem);display:flex;gap:1rem;flex-wrap:wrap}}.selected{{outline:4px solid var(--accent)}}@media(prefers-reduced-motion:reduce){{*,*:before,*:after{{animation:none!important;transition:none!important;scroll-behavior:auto!important}}}}</style></head>
    <body><header><h1>{html.escape(title)}</h1><p class="intro">Compare actual artifacts, not self-awarded scores. Pick one direction only when you decide it; negatives remain context-specific.</p></header><main>{''.join(cards)}</main><footer><label>Chosen direction <select id="chosen"><option value="">No selection</option></select></label><button type="button" id="export">Export evidence JSON</button><p id="status" role="status" aria-live="polite"></p></footer>
    <script>const IDs={ids_json};const choice=document.getElementById('chosen');for(const id of IDs){{const o=document.createElement('option');o.value=id;o.textContent=id;choice.append(o)}}choice.addEventListener('change',()=>{{document.querySelectorAll('.variant').forEach(el=>el.classList.toggle('selected',el.dataset.id===choice.value))}});document.getElementById('export').addEventListener('click',()=>{{const feedback=IDs.map(id=>({{id,rating:document.querySelector('[data-rating="'+id+'"]')?.value||null,comment:document.querySelector('[data-note="'+id+'"]')?.value||''}}));const data={{schema_version:1,chosen:choice.value||null,feedback,approval:'not-implied-by-selection',source:'explicit-browser-comparison',recorded_at:new Date().toISOString()}};const blob=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='aco-taste-feedback.json';a.click();URL.revokeObjectURL(url);document.getElementById('status').textContent='Feedback exported locally. Import explicitly to project memory.'}});</script></body></html>'''

def write_board(packet,output):
    p=Path(output).expanduser().absolute()
    if p.exists():raise ValueError('Comparison output exists; refusing overwrite')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(board(packet),encoding='utf-8')
    return {'output':str(p),'variants':len(packet['variants']),'status':'comparison-ready','images_have_been_visually_judged':False,'feedback_recorded':False}
