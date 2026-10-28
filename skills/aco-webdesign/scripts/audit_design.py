#!/usr/bin/env python3
"""Review measured DOM snapshots using ACO's design rules."""
import argparse
import json
from pathlib import Path
from design_rules import RULES


def audit(snapshot,system=None,ignore=()):
    if snapshot.get('schema')!=2:raise ValueError('Design review requires a schema 2 DOM snapshot')
    system=system or {};rows=snapshot['elements'];byid={e['index']:e for e in rows}
    body=[e['fontSize'] for e in rows if e['tag']=='p' and e.get('fontSize')]
    body_size=sorted(body)[len(body)//2] if body else 16
    spaces=[e['marginBottom'] for e in rows if e.get('tag')=='section' and e.get('marginBottom',0)>0]
    findings=[];unknown=[];skipped=set(ignore)
    ids={r[0] for r in RULES}
    if skipped-ids:raise ValueError('Unknown ignored rule: '+', '.join(sorted(skipped-ids)))
    for rule_id,message,category,predicate in RULES:
        if rule_id in skipped:continue
        if category=='system' and not system:
            unknown.append({'id':rule_id,'reason':'No design system supplied'});continue
        if rule_id=='runtime-error' and 'scriptErrors' not in snapshot:
            unknown.append({'id':rule_id,'reason':'No browser error log supplied'});continue
        if rule_id in ('orphan-word','uneven-title') and not snapshot.get('lineMeasurement'):
            unknown.append({'id':rule_id,'reason':'Text line geometry unavailable'});continue
        if rule_id=='covered-text' and not snapshot.get('occlusionMeasurement'):
            unknown.append({'id':rule_id,'reason':'Hit-test measurements unavailable'});continue
        for e in rows:
            if rule_id in e.get('ignoreRules',[]):continue
            parent=byid.get(e.get('parent'),{});previous=byid.get(e.get('previous'),{})
            siblings=[x.get('text','') for x in rows if x.get('parent')==e.get('parent')]
            try:matched=predicate(e,parent,previous,snapshot,system,body_size,spaces,snapshot['viewport']['width'],snapshot['viewport']['height'],siblings)
            except (TypeError,ValueError,KeyError,ZeroDivisionError) as exc:
                raise ValueError(f'Invalid measurement for {rule_id}: {exc}') from exc
            if matched:findings.append({'rule':rule_id,'category':category,'severity':'review','message':message,'element':{'index':e['index'],'tag':e['tag'],'id':e.get('id','')},'evidence':{k:e.get(k) for k in ('text','fontSize','color','background','width','height')}})
    return {'rules':len(RULES),'findings':findings,'not_evaluated':unknown,'ignored':sorted(skipped),'viewport':snapshot['viewport'],'visual_judgment_required':True}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('snapshot',type=Path);p.add_argument('--system',type=Path);p.add_argument('--ignore',action='append',default=[]);a=p.parse_args()
    try:
        result=audit(json.loads(a.snapshot.read_text()),json.loads(a.system.read_text()) if a.system else None,a.ignore);print(json.dumps(result,indent=2));raise SystemExit(1 if result['findings'] else 0)
    except (ValueError,OSError,KeyError) as e:p.exit(2,str(e)+'\n')
