"""ACO Deep Design: evidence-led variations and multichannel production.

Original stdlib-only implementation. Does not fetch sources, translate content,
render screenshots, certify design quality, access accounts or publish.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

LENSES = frozenset(('hierarchy','whitespace','alignment','proximity','contrast',
                    'balance','repetition','unity'))
COMPOSITIONS = ('index-led', 'field-led', 'type-led')
CHANNELS = {'landing': {'desktop','mobile'}, 'social': {'square','portrait','landscape'},
            'deck': {'slides'}, 'dashboard': {'desktop','mobile'}}
RATIOS = {'square':'1 / 1','portrait':'4 / 5','landscape':'16 / 9','slides':'16 / 9',
          'desktop':'auto','mobile':'auto'}
DEFAULT_TOKENS = {'background':'#f4f1ea','foreground':'#20201e',
                  'accent':'#973e29','surface':'#fffefa', 'font':'Georgia, serif'}
ALLOWED_FONTS = frozenset(('Georgia, serif','system-ui, sans-serif','Arial, sans-serif',
                           'Verdana, sans-serif','Times New Roman, serif'))
MAX_LANGUAGES = 8
CONTROLS = {'hero_scale': {'default','large'},
            'density': {'default','airy','compact'},
            'alignment': {'default','left','center'}}


def _text(value, label, limit=2500):
    if not isinstance(value, str) or not value.strip() or len(value)>limit:
        raise ValueError(f'{label}: requires a nonempty string up to {limit} characters')
    return value.strip()


def _safe_link(value):
    if not isinstance(value,str) or len(value)>2000 or re.search(r'[\x00-\x1f\x7f]', value):
        raise ValueError('Unsafe link')
    if re.fullmatch(r'#[A-Za-z0-9_-]+',value): return value
    u=urlsplit(value)
    if u.scheme=='https' and u.hostname and not u.username and not u.password and not value.startswith('https:////'):
        return value
    if u.scheme=='mailto' and u.path and '@' in u.path: return value
    raise ValueError('Links must be HTTPS, mailto or local #fragment')


def _tokens(raw):
    if raw is None: return dict(DEFAULT_TOKENS)
    if not isinstance(raw,dict) or set(raw)!=set(DEFAULT_TOKENS):
        raise ValueError('tokens must contain background, foreground, accent, surface, font')
    for field in ('background','foreground','accent','surface'):
        if not isinstance(raw[field],str) or not re.fullmatch('#[0-9A-Fa-f]{6}',raw[field]):
            raise ValueError('Invalid color token: '+field)
    if raw['font'] not in ALLOWED_FONTS:raise ValueError('Font stack not allowlisted')
    return dict(raw)


def _luminance(value):
    channels=(int(value[i:i+2],16)/255 for i in (1,3,5))
    rgb=[a/12.92 if a<=.04045 else ((a+.055)/1.055)**2.4 for a in channels]
    return sum(c*w for c,w in zip(rgb,(.2126,.7152,.0722)))


def contrast(a,b):
    hi,lo=sorted((_luminance(a),_luminance(b)),reverse=True)
    return round((hi+.05)/(lo+.05),2)


def _content(raw, locale):
    if not isinstance(raw,dict):raise ValueError('Missing content for '+locale)
    c={key:_text(raw.get(key),locale+'.'+key,800) for key in ('title','description')}
    sections=raw.get('sections',[])
    if not isinstance(sections,list) or not 1<=len(sections)<=10:raise ValueError('1–10 sections required for '+locale)
    c['sections']=[]
    for i,row in enumerate(sections):
        if not isinstance(row,dict):raise ValueError('Invalid section')
        c['sections'].append({'heading':_text(row.get('heading'),f'{locale}.section{i}.heading',160),
                              'body':_text(row.get('body'),f'{locale}.section{i}.body',2500)})
    cta=raw.get('cta')
    if cta is not None:
        if not isinstance(cta,dict):raise ValueError('Invalid CTA')
        c['cta']={'label':_text(cta.get('label'),'CTA label',100),'href':_safe_link(cta.get('href'))}
    else:c['cta']=None
    metrics=raw.get('metrics',[])
    if not isinstance(metrics,list) or len(metrics)>8:raise ValueError('Up to eight sourced metrics')
    c['metrics']=[]
    for m in metrics:
        if not isinstance(m,dict):raise ValueError('Invalid metric')
        c['metrics'].append({'label':_text(m.get('label'),'Metric label',120),
            'value':_text(m.get('value'),'Metric value',120),'detail':str(m.get('detail',''))[:240]})
    return c


def _controls(raw):
    if not isinstance(raw,dict) or set(raw)-set(CONTROLS):
        raise ValueError('Reference controls must use allowlisted design operations')
    for key,value in raw.items():
        if value not in CONTROLS[key]:raise ValueError('Invalid value for '+key)
    return dict(raw)


def _refs(raw):
    if not isinstance(raw,list) or len(raw)>20:raise ValueError('references must be a list of at most 20')
    out=[]; ids=set()
    for i,ref in enumerate(raw):
        if not isinstance(ref,dict):raise ValueError('Reference must be an object')
        rid=_text(ref.get('id'),'reference id',80)
        if not re.fullmatch('[A-Za-z0-9_-]+',rid) or rid in ids:raise ValueError('Duplicate/unsafe reference id')
        ids.add(rid)
        role=ref.get('role','inspiration')
        if role not in {'inspiration','constraint','negative','direction'}:raise ValueError('Invalid reference role')
        source=_text(ref.get('source'),'reference source',1000)
        obs=ref.get('observations',[])
        if not isinstance(obs,list) or len(obs)>12:raise ValueError('Too many observations')
        processed=[]
        for o in obs:
            if not isinstance(o,dict) or o.get('lens') not in LENSES:raise ValueError('Invalid eight-lens observation')
            processed.append({'lens':o['lens'],
                'observation':_text(o.get('observation'),'observed reference treatment',500),
                'effect':_text(o.get('effect'),'effect of treatment',500),
                'adaptation':_text(o.get('adaptation'),'original adaptation',500),
                'controls':_controls(o.get('controls',{}))})
        out.append({'id':rid,'source':source,'role':role,'rights':ref.get('rights','unknown'),
                    'observations':processed})
    return out


def validate_campaign(raw):
    if not isinstance(raw,dict):raise ValueError('Campaign packet must be JSON object')
    project=_text(raw.get('project'),'project',150)
    audience=_text(raw.get('audience'),'audience',400)
    anchor=_text(raw.get('anchor'),'unique factual anchor',500)
    purpose=_text(raw.get('purpose'),'purpose/action',500)
    identities=raw.get('locked_identity',False)
    if not isinstance(identities,bool):raise ValueError('locked_identity must be boolean')
    content=raw.get('content')
    if not isinstance(content,dict) or not 1<=len(content)<=MAX_LANGUAGES:
        raise ValueError('1–8 explicitly supplied locale translations required')
    localized={}
    for locale,block in content.items():
        if not re.fullmatch(r'[a-z]{2}(?:-[A-Z]{2})?',locale):raise ValueError('Invalid locale')
        localized[locale]=_content(block,locale)
    chans=raw.get('channels')
    if not isinstance(chans,list) or not 1<=len(chans)<=8:
        raise ValueError('1–8 output channels required')
    used=set(); checked=[]
    for ch in chans:
        if not isinstance(ch,dict):raise ValueError('Invalid channel')
        cid=_text(ch.get('id'),'channel id',48)
        if not re.fullmatch('[a-z0-9-]+',cid) or cid in used:raise ValueError('Duplicate or unsafe channel id')
        used.add(cid)
        kind,format_,locale=ch.get('kind'),ch.get('format'),ch.get('locale')
        if kind not in CHANNELS or format_ not in CHANNELS[kind]:raise ValueError('Unsupported kind/format')
        if locale not in localized:raise ValueError('Translations not supplied for '+str(locale))
        checked.append({'id':cid,'kind':kind,'format':format_,'locale':locale})
    if identities and 'tokens' not in raw:raise ValueError('Locked identity requires explicit approved tokens')
    tokens=_tokens(raw.get('tokens'))
    if identities and raw.get('explore_tokens'):
        raise ValueError('Cannot explore identity tokens when identity is locked')
    return {'schema':'aco-deep-design/1','project':project,'audience':audience,'anchor':anchor,
            'purpose':purpose,'locked_identity':identities,'tokens':tokens,
            'content':localized,'channels':checked,'references':_refs(raw.get('references',[])),
            'user_approval':False}


def study(packet):
    """Synthesize *supplied* observations, never claim to have seen URLs/images."""
    refs=packet['references']; observations=[(r,o) for r in refs for o in r['observations']]
    negative=[{'source':r['id'],'lens':o['lens'],'avoid':o['adaptation']} for r,o in observations if r['role']=='negative']
    positive=[{'source':r['id'],'lens':o['lens'],'evidence':o['observation'],
               'effect':o['effect'],'adaptation':o['adaptation'],'controls':o['controls']} for r,o in observations if r['role']!='negative']
    decisions={}; conflicts=[]
    for obj in positive:
        for key,value in obj['controls'].items():
            if key in decisions and decisions[key]['value']!=value:
                conflicts.append({'control':key,'first_source':decisions[key]['source'],
                                  'conflicting_source':obj['source'], 'status':'manual-resolution-required'})
                decisions[key]['conflicted']=True
            elif key not in decisions:
                decisions[key]={'value':value,'source':obj['source']}
    safe={k:v for k,v in decisions.items() if not v.get('conflicted')}
    return {'anchor':packet['anchor'],'observations_received':len(observations),
            'safe_design_controls':safe,'control_conflicts':conflicts,
            'adaptations':positive,'constraints_from_negatives':negative,
            'missing_evidence':([] if positive else ['No inspected positive reference observations were supplied']),
            'interpretation':'supplied-observations-only','reference_images_viewed':False,
            'permission_to_copy_assets':False,'source_licensing_unverified':True}


def directions(packet):
    """Three genuinely different HTML composition strategies, same approved claims."""
    purpose=packet['purpose']; anchor=packet['anchor']
    explanations={
      'index-led':('The work is navigated as a numbered register',
                   'small index → decisive heading → numbered evidence sections',
                   'makes dense or research-based information legible; can feel systematic'),
      'field-led':('The anchor becomes a spacious editorial field',
                   'full-width contextual statement → immersive typographic field → concise sections',
                   'supports cultural positioning; requires restraint with long headings'),
      'type-led':('Language itself carries the visual identity',
                  'overscale headline → direct action → stacked reading sequence',
                  'strong voice and legibility; long translations need responsive checks')}
    result=[]
    for idx,name in enumerate(COMPOSITIONS):
        mechanism,sequence,tradeoff=explanations[name]
        result.append({'id':name,'structure':sequence,'hierarchy':mechanism,
                       'imagery_role':'None by default; never invent a sourced photograph',
                       'interaction_model':'Readable text and standard links; no decorative UI animation',
                       'content_sequence':sequence.split(' → '),'palette':packet['tokens'],
                       'concept_device':f'Let the confirmed anchor “{anchor}” determine the composition, not a decorative preset',
                       'purpose':purpose,'tradeoff':tradeoff,'claimed_reference_inspection':False,
                       'needs_real_review':True,'reference_controls':study(packet)['safe_design_controls'],
                       'source':'original-aco-concept-mechanism'})
    return {'schema':'aco-deep-design/directions-v1','directions':result,
            'identities_preserved':packet['locked_identity'],
            'status':'structurally-distinct-in-generated-HTML-not-yet-visually-evaluated'}


def E(value):return html.escape(str(value),quote=True)

BASE_CSS="""
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.55 var(--font)}
.skip{position:absolute;left:-10000px;top:0;background:var(--surface);padding:1rem}.skip:focus{left:1rem;z-index:2}
a{color:inherit;text-underline-offset:.2em}a:focus-visible{outline:3px solid var(--accent);outline-offset:4px}
main{max-width:1540px;margin:auto;padding:clamp(1rem,3.6vw,4rem)}h1,h2,p{overflow-wrap:anywhere}h1{font-size:clamp(2.7rem,8.2vw,9.5rem);letter-spacing:-.055em;line-height:.98;margin:0}h2{font-size:clamp(1.5rem,3vw,3rem);letter-spacing:-.03em;line-height:1.1}p{max-width:66ch}
.eyebrow{font:700 .75rem/1.3 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.15em}header{padding:1rem clamp(1rem,3.6vw,4rem);border-bottom:1px solid currentColor;display:flex;justify-content:space-between;gap:2rem;flex-wrap:wrap}.cta{display:inline-block;padding:.7rem 1rem;border:2px solid currentColor;margin-top:1rem;font-weight:700;text-decoration:none}
.intro{font-size:clamp(1.15rem,2vw,1.8rem);max-width:55ch}.content{list-style:none;margin:0;padding:0}.content li{min-width:0}.content p{margin:0}.content h2{margin:.3rem 0 1rem}.index-label{font:.8rem system-ui,sans-serif;font-weight:700;letter-spacing:.1em}
.index-led .heading{display:grid;grid-template-columns:minmax(110px,1fr) minmax(0,3fr);gap:2rem;padding:clamp(2rem,5vw,5rem) 0 4rem}.index-led .content li{display:grid;grid-template-columns:minmax(110px,1fr) minmax(0,2fr) minmax(0,2fr);gap:2rem;border-top:1px solid currentColor;padding:1.5rem 0}.index-led h1{font-size:clamp(3rem,6.5vw,7rem)}
.field-led .heading{background:var(--surface);border-top:12px solid var(--accent);padding:clamp(2rem,7vw,8rem);min-height:60vh;display:flex;flex-direction:column;justify-content:space-between;gap:3rem}.field-led .intro{max-width:40ch;margin:1rem 0 0}.field-led .content li{padding:clamp(2rem,5vw,5rem) 0;border-bottom:1px solid currentColor;display:flex;align-items:flex-start;gap:clamp(1rem,7vw,8rem)}.field-led .content li:nth-child(even){flex-direction:row-reverse}.field-led .content li>*{flex:1}
.type-led .heading{padding:clamp(2rem,5vw,5rem) 0 3rem;display:flex;flex-direction:column;align-items:flex-start;gap:2rem}.type-led h1{max-width:11ch}.type-led .content li{border-top:4px solid var(--accent);padding:2rem 0;display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:clamp(1rem,4vw,5rem)}.type-led .content li:nth-child(odd) h2{font-style:italic}
.hint-hero-large h1{font-size:clamp(3.4rem,10.5vw,11rem)}.hint-density-airy .content li{padding-top:3.4rem;padding-bottom:3.4rem}.hint-density-compact .content li{padding-top:.8rem;padding-bottom:.8rem}.hint-align-center .heading{text-align:center}
.terminal{font:.75rem system-ui,sans-serif;padding:.8rem 0;border-top:1px solid currentColor;margin-top:4rem}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:.7rem}.metrics div{border:1px solid currentColor;padding:1rem;background:var(--surface)}.metrics strong{font-size:clamp(1.8rem,3vw,3rem);display:block;overflow-wrap:anywhere}.metrics p{font-size:.85rem}
.social{max-width:850px;margin:0 auto;padding:1.6rem}.social .sheet{aspect-ratio:var(--aspect);background:var(--surface);color:var(--fg);padding:clamp(1.2rem,5vw,3.5rem);display:flex;flex-direction:column;justify-content:space-between;min-width:0;min-height:0;overflow:hidden}.social h1{font-size:clamp(1.8rem,5.5vw,5.8rem);line-height:1;max-width:12ch}.social .sheet p{font-size:clamp(.85rem,1.8vw,1.35rem)}.social .sheet .eyebrow{font-size:clamp(.6rem,1vw,.8rem)}
.social.index-led .sheet{border:2px solid var(--fg)}.social.index-led .social-top{border-bottom:2px solid var(--accent);padding-bottom:1rem}.social.field-led .sheet{background:var(--accent);color:var(--bg);text-align:center;align-items:center;justify-content:space-around}.social.field-led .sheet h1{font-style:italic}.social.type-led .sheet{background:var(--bg);border-left:clamp(8px,3vw,28px) solid var(--accent)}.social.type-led .sheet h1{text-transform:uppercase;letter-spacing:-.08em}
.deck .slide{aspect-ratio:16/9;width:100%;min-height:0;padding:clamp(1.4rem,5vw,5rem);border:1px solid currentColor;margin-bottom:2rem;display:flex;flex-direction:column;justify-content:space-between;break-after:page}.deck .slide h1,.deck .slide h2{max-width:17ch}.deck.index-led .slide{background:var(--surface)}.deck.field-led .slide:first-child{background:var(--accent);color:var(--bg)}.deck.type-led .slide h1{font-size:clamp(3rem,8vw,8rem)}
@media(max-width:700px){.index-led .heading,.index-led .content li,.type-led .content li{display:block}.index-led .content li>*{margin-bottom:1rem}.field-led .content li,.field-led .content li:nth-child(even){display:block}.field-led .heading{min-height:40vh}.social{padding:.5rem}.social .sheet{padding:clamp(1rem,4vw,2rem)}.deck .slide{min-height:70svh;aspect-ratio:auto}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*,*:before,*:after{animation:none!important;transition:none!important}}
@media print{@page{size:A4 landscape;margin:0}body{print-color-adjust:exact;-webkit-print-color-adjust:exact}header,.skip,.terminal{display:none!important}.deck .slide{height:100vh;min-height:0;margin:0;break-after:page;border:0}.social{width:100%;margin:auto}.field-led .heading{min-height:0}}
"""


def _action(c):
    x=c.get('cta')
    return '' if not x else f'<a class="cta" href="{E(_safe_link(x["href"]))}">{E(x["label"])}</a>'


def _sections(c):
    return '<ol class="content" id="features">'+''.join(f'<li><span class="index-label">{i+1:02}</span><h2>{E(s["heading"])}</h2><p>{E(s["body"])}</p></li>' for i,s in enumerate(c['sections']))+'</ol>'


def _metrics(c):
    if not c.get('metrics'):return ''
    return '<section class="metrics" aria-label="Supplied project metrics">'+''.join(
        f'<div><span class="eyebrow">{E(m["label"])}</span><strong>{E(m["value"])}</strong><p>{E(m["detail"])}</p></div>'
        for m in c['metrics'])+'</section>'


def _main(packet,content,channel,direction):
    k=channel['kind'];fmt=channel['format'];label=E(packet['anchor']); title=E(content['title']);desc=E(content['description']);aud=E(packet['audience'])
    controls=study(packet)['safe_design_controls']
    hint=''.join(' hint-'+key.replace('_','-')+'-'+val['value'] for key,val in controls.items() if val['value']!='default')
    if k=='social':
        note=E(content['sections'][0]['body'])
        return (f'<main id="main" class="social {direction}{hint}"><article class="sheet" style="--aspect:{RATIOS[fmt]}">'
          f'<div class="social-top eyebrow">{aud} / {E(channel["locale"])}</div><h1>{title}</h1>'
          f'<p>{desc}</p><div class="eyebrow">{label} · {note}</div></article></main>')
    if k=='deck':
        first=f'<section class="slide"><div class="eyebrow">{aud}</div><div><h1>{title}</h1><p class="intro">{desc}</p></div><div>{label}</div></section>'
        slides=''.join(f'<section class="slide"><div class="eyebrow">{i+2:02} / {len(content["sections"])+1:02}</div><div><h2>{E(s["heading"])}</h2><p class="intro">{E(s["body"])}</p></div><div>{label}</div></section>' for i,s in enumerate(content['sections']))
        return f'<main id="main" class="deck {direction}{hint}">{first}{slides}</main>'
    header=f'<div class="heading"><div class="eyebrow">{label}</div><div><h1>{title}</h1><p class="intro">{desc}</p>{_action(content)}</div></div>'
    return f'<main id="main" class="{direction} {E(k)}{hint}">{header}{_metrics(content) if k=="dashboard" else ""}{_sections(content)}<footer class="terminal">{aud} · {E(packet["purpose"])}</footer></main>'


def render(packet,channel,direction):
    if direction not in COMPOSITIONS:raise ValueError('Unknown direction')
    if channel['id'] not in {c['id'] for c in packet['channels']}:raise ValueError('Unknown channel')
    tokens=packet['tokens']; c=packet['content'][channel['locale']]
    style=';'.join(f'--{name}:{E(tokens[field])}' for name,field in (('bg','background'),('fg','foreground'),('accent','accent'),('surface','surface'),('font','font')))
    contents=_main(packet,c,channel,direction)
    return (f'<!doctype html>\n<html lang="{E(channel["locale"])}"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(c["title"])}</title><meta name="description" content="{E(c["description"])}">'
            f'<style>:root{{{style}}}{BASE_CSS}</style></head><body>'
            '<a class="skip" href="#main">Skip to content</a>'
            f'<header><span class="eyebrow">{E(packet["project"])}</span><span class="eyebrow">{E(channel["kind"])} / {E(direction)}</span></header>'
            f'{contents}</body></html>')


def static_audit(packet,channel,direction,artifact):
    c=packet['content'][channel['locale']]
    required=[c['title'],c['description']]
    if channel['kind'] not in ('social',):
        required.extend(x['heading'] for x in c['sections'])
        required.extend(x['body'] for x in c['sections'])
    else: required.append(c['sections'][0]['body'])
    if channel['kind']=='dashboard':
        required.extend(m['label'] for m in c['metrics'])
        required.extend(m['value'] for m in c['metrics'])
    checks={'doctype':artifact.startswith('<!doctype html>'),
        'responsive':'@media(max-width:' in artifact,
        'reduced_motion':'@media(prefers-reduced-motion:' in artifact,
        'print':'@media print' in artifact,
        'focus':':focus-visible' in artifact,
        'skip':'href="#main"' in artifact,
        'no_script':'<script' not in artifact.lower(),
        'no_missing_content':all(E(t) in artifact for t in required),
        'composition':bool(re.search(r'class="[^"]*\b'+re.escape(direction)+r'\b',artifact)),
        'locale':f'<html lang="{E(channel["locale"])}"' in artifact}
    contrast_values={'body':contrast(packet['tokens']['foreground'],packet['tokens']['background']),
        'surface':contrast(packet['tokens']['foreground'],packet['tokens']['surface'])}
    if c.get('cta') and c['cta']['href'].startswith('#'):
        checks['fragment_target']='id="'+E(c['cta']['href'][1:])+'"' in artifact
    warnings=[]
    if channel['kind']=='social':
        if len(c['title'])>85:warnings.append('Social title may overflow: inspect at target dimensions')
        if len(c['description'])>240:warnings.append('Social description may overflow: inspect at target dimensions')
    return {'pass':all(checks.values()),'checks':checks,'contrast':contrast_values,
            'contrast_aa_candidate':all(x>=4.5 for x in contrast_values.values()),
            'rendered_visual_review':'not performed','human_approval':False,
            'warnings': warnings + (['Contrast below 4.5:1 in a text role'] if min(contrast_values.values())<4.5 else [])}


def _slug(s):return re.sub('[^a-z0-9-]+','-',s.lower()).strip('-')


def _hash(value):return hashlib.sha256(value.encode('utf-8')).hexdigest()


def build_campaign(raw,target):
    """Prevalidate every channel, stage atomically and refuse to overwrite any directory."""
    p=validate_campaign(raw)
    target=Path(target).expanduser().absolute()
    if target.exists() or target.is_symlink():raise FileExistsError('Output exists: refusing to replace it')
    if target.parent.is_symlink():raise ValueError('Symlink parent blocked')
    if not target.parent.is_dir():raise ValueError('Output parent must already exist')
    # All strings are escaped. Generated pages and manifest are project-local, never uploaded.
    generated={}; observations=[]
    for d in COMPOSITIONS:
        for ch in p['channels']:
            name=f'{d}/{ch["id"]}.html'
            page=render(p,ch,d); report=static_audit(p,ch,d,page)
            if not report['pass']:raise ValueError('Structural audit failed for '+name)
            generated[name]=page
            observations.append({'path':name,'sha256':_hash(page),'direction':d,
                'channel':ch['id'],'locale':ch['locale'],'kind':ch['kind'],
                'format':ch['format'],'audit':report})
    items=''.join(f'<li><a href="{E(item["path"])}">{E(item["direction"])} · {E(item["channel"])} · {E(item["locale"])}</a></li>' for item in observations)
    index='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ACO campaign comparison</title><style>body{font:1.2rem system-ui;max-width:900px;margin:3rem auto;padding:1rem}li{margin:1rem 0}a:focus-visible{outline:3px solid blue}</style><main><h1>Campaign comparison</h1><p>Three different compositions. Human choice is not implied.</p><ul>'+items+'</ul></main></html>'
    generated['index.html']=index
    manifest={'schema':'aco-deep-design/artifact-v1','project':p['project'],
        'creative_directions':directions(p)['directions'], 'reference_study':study(p),
        'artifacts':observations,'index':'index.html','source':'local-explicit-brief',
        'locales_supplied':list(p['content']),
        'limitations':['HTML prototypes; not screenshots or verified renders',
                       'No translation inferred; no external sources downloaded',
                       'No Figma, Canva, Drive, social publication or cloud upload',
                       'Each channel requires actual browser inspection and accessibility checks'],
        'user_approval':False,'visual_quality_certified':False}
    generated['manifest.json']=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
    with tempfile.TemporaryDirectory(prefix='.aco-deep-',dir=target.parent) as td:
        temp=Path(td)/'output';temp.mkdir()
        for name,data in generated.items():
            path=temp/name;path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(data,encoding='utf-8')
        if target.exists():raise FileExistsError('Output appeared during build')
        temp.rename(target)
    return {'output':str(target),'artifacts':len(observations),'directions':list(COMPOSITIONS),
            'channels':len(p['channels']),'index':str(target/'index.html'),
            'manifest':str(target/'manifest.json'),'visual_review':'not performed',
            'published':False,'full_aco_suite_run':False}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('plan','study','build'):
        cmd=sub.add_parser(name)
        cmd.add_argument('--packet',type=Path,required=True)
        if name=='build':cmd.add_argument('--output',type=Path,required=True)
    qa=sub.add_parser('browser-check',help='Optional Playwright screenshot and layout QA')
    qa.add_argument('--bundle',type=Path,required=True)
    qa.add_argument('--output',type=Path,required=True)
    qa.add_argument('--browser',type=Path)
    a=parser.parse_args(argv)
    if a.command=='browser-check':
        print(json.dumps(browser_check(a.bundle,a.output,browser_path=a.browser),ensure_ascii=False,indent=2))
        return 0
    packet=json.loads(a.packet.read_text(encoding='utf-8'))
    if a.command=='build': result=build_campaign(packet,a.output)
    else:
        contract=validate_campaign(packet)
        result={'directions':directions(contract),'references':study(contract),
                'channels':contract['channels'],'locked_identity':contract['locked_identity']} if a.command=='plan' else study(contract)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


# Optional real Chromium/Playwright smoke test. No silent browser installation.
def browser_check(bundle, output, *, browser_path=None):
    """Render every generated channel, check horizontal overflow and save screenshot receipts.

    Automated layout evidence is not human visual judgment or WCAG certification.
    """
    root=Path(bundle).expanduser().resolve(strict=True)
    if not root.is_dir():raise ValueError('Bundle directory required')
    manifest_file=root/'manifest.json'
    if manifest_file.is_symlink():raise ValueError('Symlink manifest refused')
    manifest=json.loads(manifest_file.read_text(encoding='utf-8'))
    if manifest.get('schema')!='aco-deep-design/artifact-v1':raise ValueError('Unexpected manifest schema')
    target=Path(output).expanduser().absolute()
    if target.exists() or target.is_symlink():raise FileExistsError('QA output exists; refusing overwrite')
    if not target.parent.is_dir() or target.parent.is_symlink():raise ValueError('QA output parent must exist and not be symlink')
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError('Playwright is optional and not installed; QA not performed') from exc
    results=[]
    # Verify all content receipts before touching the browser or creating output.
    pages=[]
    for row in manifest.get('artifacts',[]):
        rel=row.get('path','')
        candidate=(root/rel).resolve(strict=True)
        if root not in candidate.parents or candidate.is_symlink() or not candidate.is_file():
            raise ValueError('Unsafe artifact path in manifest')
        src=candidate.read_text(encoding='utf-8')
        if _hash(src)!=row.get('sha256') or '<script' in src.casefold():
            raise ValueError('Artifact differs from manifest or contains script: '+rel)
        pages.append((row,src))
    with tempfile.TemporaryDirectory(prefix='.aco-qa-',dir=target.parent) as td:
        tmp=Path(td)/'out';tmp.mkdir()
        with sync_playwright() as pl:
            kwargs={'headless':True,'args':['--no-sandbox']}
            if browser_path:kwargs['executable_path']=str(browser_path)
            browser=pl.chromium.launch(**kwargs)
            try:
                for row,src in pages:
                    formats=[('desktop',1440,900),('mobile',390,844)] if row['kind'] in ('landing','dashboard') else [('target',1200,1100)]
                    for label,width,height in formats:
                        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
                        try:
                            page.set_content(src,wait_until='load',timeout=12000)
                            render_ok=page.locator('main#main').count()==1 and page.locator('h1').count()==1
                            horizontal_overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth+1')
                            # Content outside a bounded social sheet is a concrete clipping risk.
                            clipped=False
                            if row['kind']=='social':
                                clipped=page.evaluate('''() => { const p=document.querySelector('.sheet');
                                  if(!p)return true;const b=p.getBoundingClientRect();
                                  return [...p.children].some(e=>{const r=e.getBoundingClientRect();
                                    return r.top < b.top-1 || r.bottom > b.bottom+1 || r.left < b.left-1 || r.right > b.right+1});}''')
                            name=row['path'].replace('/','__').removesuffix('.html')+'__'+label+'.png'
                            page.screenshot(path=str(tmp/name),full_page=True,animations='disabled')
                            results.append({'artifact':row['path'],'viewport':[width,height], 'view':label,
                                            'screenshot':name,'sha256':hashlib.sha256((tmp/name).read_bytes()).hexdigest(),
                                            'horizontal_overflow':bool(horizontal_overflow),
                                            'social_content_clipped':bool(clipped),
                                            'structure_present':bool(render_ok),
                                            'pass':bool(render_ok and not horizontal_overflow and not clipped)})
                        finally:page.close()
            finally:browser.close()
        report={'schema':'aco-deep-design/browser-qa-v1','bundle':str(root),
                'status':'automated-browser-smoke-passed' if all(x['pass'] for x in results) else 'browser-issues-observed',
                'checks':results,'screenshots':len(results),'human_visual_review':False,
                'note':'Chromium screenshots and layout checks do not establish artistic merit or complete accessibility.'}
        (tmp/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if target.exists():raise FileExistsError('QA destination appeared during checking')
        tmp.rename(target)
        return {'output':str(target),'screenshots':len(results),'status':report['status'],
                'human_visual_review':False}

if __name__=='__main__':raise SystemExit(main())
