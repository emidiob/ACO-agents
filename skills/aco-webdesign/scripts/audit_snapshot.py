#!/usr/bin/env python3
"""Analyze an ACO browser DOM snapshot; not a full accessibility or visual audit."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

RULES=('document-title','document-language','viewport-meta','zoom-disabled','page-overflow','main-landmark','page-heading','duplicate-id','image-alt','control-name','field-label','placeholder-link','positive-tabindex','small-target','small-text','text-overflow','motion-review')

def audit(snapshot):
    if snapshot.get('schema') not in (1,2) or not isinstance(snapshot.get('elements'),list):
        raise ValueError('Expected an ACO schema 1 or 2 browser probe snapshot')
    if not isinstance(snapshot.get('viewport',{}).get('width'),(int,float)):
        raise ValueError('Missing viewport width')
    findings=[]
    def add(code,message,element=None,severity='review'):
        findings.append({'code':code,'message':message,'element':element,'severity':severity})
    if not snapshot.get('title','').strip():add('document-title','Document title is empty',severity='error')
    if not snapshot.get('lang'):add('document-language','Document language is absent',severity='error')
    if not snapshot.get('viewportMeta'):add('viewport-meta','Viewport metadata is absent')
    if re.search(r'user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(?:\.0)?(?:\s*[,;]|$)',snapshot.get('viewportMeta','')):
        add('zoom-disabled','Viewport metadata may restrict zoom',severity='error')
    if snapshot.get('scrollWidth',0)>snapshot['viewport']['width']+1:add('page-overflow','Page exceeds the captured viewport width')
    rows=snapshot['elements']
    if not any(x['tag']=='main' or x.get('role')=='main' for x in rows):add('main-landmark','No visible main landmark captured')
    if not any(x['tag']=='h1' for x in rows):add('page-heading','No visible H1 captured')
    ids=Counter(x.get('id') for x in rows if x.get('id'))
    for ident,count in ids.items():
        if count>1:add('duplicate-id','Visible elements share an ID: '+ident,severity='error')
    for row in rows:
        loc={'index':row['index'],'tag':row['tag'],'id':row.get('id','')}
        tag=row['tag']; name=row.get('name','').strip()
        control=tag in ('button','select','textarea','input') or row.get('role') in ('button','link') or (tag=='a' and row.get('href') is not None)
        if tag=='img' and row.get('alt') is None:add('image-alt','Image has no alt attribute',loc,'error')
        if control and not name:add('control-name','Control has no name detected by the limited probe; verify its accessible name',loc)
        if tag in ('input','textarea','select') and row.get('type') not in ('hidden','submit','button','reset') and not name:add('field-label','Field has no detected label',loc)
        if tag=='a' and (row.get('href') or '').strip() in ('','#','javascript:void(0)'):add('placeholder-link','Link has no meaningful destination',loc)
        try:
            if int(row.get('tabindex') or 0)>0:add('positive-tabindex','Positive tabindex changes reading order',loc)
        except ValueError:add('positive-tabindex','Invalid tabindex value',loc)
        if control and not row.get('disabled') and min(row.get('width',0),row.get('height',0))<24:add('small-target','Target is below 24 CSS px in one dimension; review spacing and inline-text exceptions',loc)
        if row.get('text') and row.get('fontSize',16)<12:add('small-text','Text is below 12 CSS px; review readability in context',loc)
        if row.get('text') and row.get('scrollWidth',0)>row.get('clientWidth',0)+1 and row.get('overflowX') in ('hidden','clip'):add('text-overflow','Text may be clipped; verify access to full content',loc)
        if snapshot.get('reducedMotion') and row.get('animation') not in (None,'none','') and row.get('animationDuration') not in ('0s',None):add('motion-review','Animation remains active with reduced motion; assess whether it is essential',loc)
    return {'schema':1,'url':snapshot.get('url'),'viewport':snapshot['viewport'],'checks':list(RULES),
            'findings':findings,'input':'supplied_browser_snapshot','interaction_verified':False,
            'limitations':['Accessible-name heuristic is not the browser accessibility tree.','Hidden DOM, shadow roots and iframes are not fully captured.','No contrast, screen-reader, keyboard, performance or aesthetic certification.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('snapshot',type=Path);a=p.parse_args()
    try:
        result=audit(json.loads(a.snapshot.read_text()));print(json.dumps(result,indent=2));return 1 if result['findings'] else 0
    except (OSError,ValueError,KeyError,TypeError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':raise SystemExit(main())
