from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json
from .context import context_plan
from .hybrid import memory_resolve
from .routing import suggest_route


def _context_case(case: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    result=context_plan(case['request'])
    exp=case.get('expect',{})
    checks=[]
    if 'status' in exp: checks.append(result['status']==exp['status'])
    if 'effective_mode' in exp: checks.append(result['effective_mode']==exp['effective_mode'])
    if 'selected_exact' in exp: checks.append(result['selected_source_ids']==exp['selected_exact'])
    if 'selected_contains' in exp: checks.append(set(exp['selected_contains']).issubset(result['selected_source_ids']))
    if 'denied_reason' in exp: checks.append(exp['denied_reason'] in {x['reason'] for x in result['denied_sources']})
    if 'max_selection_ratio' in exp: checks.append(result['metrics']['selection_ratio']<=float(exp['max_selection_ratio']))
    if exp.get('no_drive_prompt',True): checks.append(result['prompt_for_drive'] is False)
    return (all(checks) if checks else True), result


def context_benchmark(path: Path | None=None) -> dict[str, Any]:
    path=(path or ROOT/'config/context-benchmark.json').expanduser().absolute()
    data=read_json(path)
    if data.get('schema_version')!=1: raise ACOError('Unsupported context benchmark schema')
    rows=[];passed=0;critical=0;ratios=[]
    for case in data.get('cases',[]):
        ok,result=_context_case(case);passed+=int(ok);ratios.append(result['metrics']['selection_ratio'])
        crit=bool(case.get('critical')) and not ok;critical+=int(crit)
        rows.append({'id':case['id'],'passed':ok,'critical_failure':crit,'result':result})
    if not rows: raise ACOError('Context benchmark must contain cases')
    score=100.0*passed/len(rows);mean=sum(ratios)/len(ratios)
    gate=data.get('gate',{})
    status='passed' if (score>=float(gate.get('minimum_score',95)) and critical<=int(gate.get('maximum_critical_failures',0)) and mean<=float(gate.get('maximum_mean_selection_ratio',0.55))) else 'failed'
    return {'status':status,'aco_version':VERSION,'path':str(path),'cases':len(rows),'score':round(score,2),'critical_failures':critical,'mean_selection_ratio':round(mean,4),'gate':gate,'failures':[x for x in rows if not x['passed']]}


def _route_case(case: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    r=suggest_route(case['prompt'],max_roles=3)
    ranked=[x['role'] for x in r.get('ranked_candidates',[])[:3]]
    selected=r.get('selected_roles',[])
    top3=list(dict.fromkeys(ranked+selected))[:3]
    acceptable=set(case['acceptable_roles'])
    ok=r.get('office')==case['expected_office'] and bool(acceptable.intersection(top3)) and len(selected)<=int(case.get('max_selected_roles',2))
    return ok, {'office':r.get('office'),'selected_roles':selected,'top3':top3}


def _memory_case(case: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    r=memory_resolve(case['request']);exp=case.get('expect',{});checks=[]
    if 'status' in exp:checks.append(r['status']==exp['status'])
    if 'destination_contains' in exp:checks.append(exp['destination_contains'] in r.get('destinations',[]))
    if 'destination_excludes' in exp:checks.append(exp['destination_excludes'] not in r.get('destinations',[]))
    if 'read_status' in exp:checks.append(r.get('read_status')==exp['read_status'])
    if exp.get('no_drive_prompt',True):checks.append(r['prompt_for_drive'] is False)
    return (all(checks) if checks else True), r


def real_world_benchmark(path: Path | None=None) -> dict[str, Any]:
    path=(path or ROOT/'config/real-world-benchmark-v072.json').expanduser().absolute()
    data=read_json(path)
    if data.get('schema_version')!=1: raise ACOError('Unsupported real-world benchmark schema')
    cases=data.get('cases',[])
    if len(cases)!=120: raise ACOError('Real-world benchmark must contain exactly 120 scenarios')
    rows=[];passed=0;critical=0;context_ratios=[];drive_prompts=0
    for case in cases:
        kind=case.get('kind')
        if kind=='route':ok,result=_route_case(case)
        elif kind=='context':
            ok,result=_context_case(case);context_ratios.append(result['metrics']['selection_ratio']);drive_prompts+=int(result['prompt_for_drive'])
        elif kind=='memory':
            ok,result=_memory_case(case);drive_prompts+=int(result.get('prompt_for_drive',False))
        else:raise ACOError('Unknown real-world benchmark kind: '+str(kind))
        passed+=int(ok);crit=bool(case.get('critical')) and not ok;critical+=int(crit)
        rows.append({'id':case['id'],'kind':kind,'passed':ok,'critical_failure':crit,'result':result})
    score=100.0*passed/len(rows);mean=sum(context_ratios)/len(context_ratios) if context_ratios else 0.0
    gate=data.get('gate',{})
    status='passed' if (score>=float(gate.get('minimum_score',96)) and critical<=int(gate.get('maximum_critical_failures',0)) and drive_prompts<=int(gate.get('maximum_drive_prompts',0)) and mean<=float(gate.get('maximum_mean_context_selection_ratio',0.55))) else 'failed'
    return {'status':status,'aco_version':VERSION,'path':str(path),'cases':len(rows),'score':round(score,2),'critical_failures':critical,'context_cases':len(context_ratios),'mean_context_selection_ratio':round(mean,4),'drive_prompts':drive_prompts,'gate':gate,'failures':[x for x in rows if not x['passed']]}
