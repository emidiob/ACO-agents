"""Concept-driven direction generator, not category-to-template matching."""
from __future__ import annotations
from pathlib import Path
import hashlib, json, random

DATA=Path(__file__).resolve().parents[2]/'assets'/'directions.json'

def catalog():
    obj=json.loads(DATA.read_text(encoding='utf-8'))
    if len(obj['directions'])!=50 or len({x['id'] for x in obj['directions']})!=50:raise ValueError('Expected 50 distinct original visual materials')
    return obj['directions']

def _fact(brief):
    facts=brief.get('facts') or []
    facts=[str(f).strip() for f in facts if str(f).strip()]
    if facts:return facts[0], 'confirmed_in_brief'
    material=(brief.get('materials') or [])
    if material:return str(material[0]),'declared_material'
    return str(brief['subject']), 'subject_only_low_specificity'

def propose(brief, *,count=3,seed=0,previous=()):
    required=['subject','audience','action','surface']
    miss=[x for x in required if not isinstance(brief.get(x),str) or not brief[x].strip()]
    if miss:raise ValueError('Brief missing: '+', '.join(miss))
    if not 1<=count<=6:raise ValueError('count must be 1..6')
    if brief['surface'] not in {'marketing','product','component','editorial','poster','presentation','photo','image','video','motion','spatial','graphic'}:raise ValueError('Unrecognized surface')
    anchor,kind=_fact(brief)
    themes=[t for t in catalog() if t['id'] not in previous]
    rnd=random.Random(str(seed)+'|'+brief['subject']+'|'+brief.get('tone',''))
    rnd.shuffle(themes)
    pref=' '.join([brief.get('tone',''),brief['subject'],brief['surface'],anchor]).lower()
    def score(t):
        keywords=set(pref.split())
        relevance=len(keywords & set(t.get('keywords',[])))
        unsuitable=2 if brief['surface']=='product' and t['layout']=='narrative-drift' else 0
        return 2*relevance-unsuitable
    themes.sort(key=score,reverse=True)
    out=[];layouts=set();families=set();surfaces=set()
    for theme in themes:
        if len(out)>=count:break
        if theme['layout'] in layouts or theme['family'] in families:continue
        if theme['surface'] in surfaces and len(surfaces)<3:continue
        layouts.add(theme['layout']);families.add(theme['family']);surfaces.add(theme['surface'])
        out.append(_compose(brief,theme,anchor,kind))
    if len(out)<count:
        for theme in themes:
            if len(out)>=count:break
            if theme['id'] not in [x['id'] for x in out]:out.append(_compose(brief,theme,anchor,kind))
    return {'subject':brief['subject'],'surface':brief['surface'],'mode':'grounded_direction_exploration','anchor_confidence':kind,'directions':out, 'requires_human_choice':True,'unknowns':([] if kind!='subject_only_low_specificity' else ['Supply distinctive product/place/material facts before claiming a strong concept']), 'limitations':['A direction sheet does not prove aesthetic quality or authorize replacing existing brand identity','Images, fonts and assets must be verified independently']}

def _compose(brief,theme,anchor,kind):
    medium=brief['surface']
    structural={
      'photo':f"Compose the {anchor} using {theme['layout']} as a FRAME relationship, not as a CSS grid",
      'image':f"Build a static composition around {anchor} with {theme['layout']} scale relations",
      'video':f"Translate {theme['layout']} into shot staging and temporal rhythm around {anchor}; preserve continuity and motivated movement",
      'motion':f"Use {theme['layout']} as a timing/spatial-sequence metaphor, subject to interruption and reduced motion",
      'spatial':f"Treat {theme['layout']} as visitor path and object/light hierarchy, not a literal web template",
      'graphic':f"Use {theme['layout']} as typographic/image hierarchy within the physical format"
    }
    locked=brief.get('locked',{})
    palette=locked.get('palette',theme['palette']) if isinstance(locked,dict) else theme['palette']
    typography=locked.get('typography',theme['typography']) if isinstance(locked,dict) else theme['typography']
    return {'id':theme['id'],'direction':theme['title'],'concept_device':f"Use {anchor!r} as {theme['mechanism']}, not as decorative filler.", 'anchor_kind':kind, 'structure':structural.get(medium,theme['layout']), 'visual_material':theme['material'], 'palette':palette, 'typography':typography, 'imagery_role':theme['image_role'], 'motion_posture':theme['motion'], 'purpose':brief['action'],'audience':brief['audience'],'content_sequence':[x.get('role','content') if isinstance(x,dict) else str(x) for x in brief.get('sections',[])], 'difference_to_test':theme['tradeoff'], 'boundaries':['Do not invent claims, customers, photographs or usage evidence','Preserve locked tokens, existing routes and content','Interpret this material against this subject; do not clone a source layout']}
