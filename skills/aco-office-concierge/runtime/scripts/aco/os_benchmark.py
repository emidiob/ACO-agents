"""ACO 1.0 Operating System and token-economy deterministic benchmarks."""
from __future__ import annotations
import statistics
from pathlib import Path
from typing import Any
from .bootstrap import bootstrap_check
from .common import ACOError, ROOT, VERSION, read_json
from .context_compiler import compile_context
from .kernel import os_plan
from .skills import skill_candidate_check, skill_candidate_store, skill_learn, skill_promotion_check, skill_search

def _get(value:Any,dotted:str)->Any:
    cur=value
    for part in dotted.split('.'):
        if isinstance(cur,dict) and part in cur:cur=cur[part]
        elif isinstance(cur,list) and part.isdigit() and int(part)<len(cur):cur=cur[int(part)]
        else:return None
    return cur

def token_economy_benchmark(path=None,root=None):
    root=(root or ROOT).expanduser().absolute();path=(path or root/'config/token-economy-benchmark.json').expanduser().absolute();data=read_json(path)
    if data.get('schema_version')!=1:raise ACOError('Unsupported token-economy benchmark schema')
    rows=[];critical=0;reductions=[]
    for case in data.get('cases',[]):
        error=None
        try:
            result=compile_context(case['packet'],root=root);exp=case.get('expected',{});checks=[]
            if 'status' in exp:checks.append(result['status']==exp['status'])
            if 'required_selected' in exp:checks.append(set(exp['required_selected']).issubset(result['token_plan']['selected_source_ids']))
            if 'forbidden_selected' in exp:checks.append(set(exp['forbidden_selected']).isdisjoint(result['token_plan']['selected_source_ids']))
            if 'max_selected_tokens' in exp:checks.append(result['token_plan']['metrics']['selected_input_tokens']<=int(exp['max_selected_tokens']))
            if 'min_reduction' in exp:checks.append(result['token_plan']['metrics']['input_reduction_ratio']>=float(exp['min_reduction']))
            if 'refine_recommended' in exp:checks.append(result['progressive_loading']['refine_recommended'] is bool(exp['refine_recommended']))
            passed=all(checks) if checks else True;reduction=result['token_plan']['metrics']['input_reduction_ratio'];reductions.append(reduction)
        except (ACOError,ValueError,TypeError,KeyError) as exc:
            passed=bool(case.get('expected_error',False));result=None;error=str(exc);reduction=None
        crit=bool(case.get('critical')) and not passed;critical+=int(crit);rows.append({'id':case.get('id'),'passed':passed,'critical_failure':crit,'reduction':reduction,'error':error})
    if not rows:raise ACOError('Token economy benchmark needs cases')
    score=round(100*sum(1 for x in rows if x['passed'])/len(rows),2);median=round(float(statistics.median(reductions)),4) if reductions else 0.0;gate=data.get('gate',{});status='passed' if score>=float(gate.get('minimum_score',98)) and critical<=int(gate.get('maximum_critical_failures',0)) and median>=float(gate.get('minimum_median_input_reduction',.70)) else 'failed'
    return {'status':status,'aco_version':VERSION,'cases':len(rows),'score':score,'critical_failures':critical,'median_input_reduction':median,'gate':gate,'rows':rows,'failures':[x for x in rows if not x['passed']]}

def os_benchmark(path=None,root=None):
    root=(root or ROOT).expanduser().absolute();path=(path or root/'config/aco-os-benchmark.json').expanduser().absolute();data=read_json(path)
    if data.get('schema_version')!=1:raise ACOError('Unsupported ACO OS benchmark schema')
    rows=[];critical=0
    for case in data.get('cases',[]):
        op=case.get('operation');error=None
        try:
            if op=='bootstrap_check':result=bootstrap_check(root)
            elif op=='skill_search':result=skill_search(case.get('query',''),tags=case.get('tags'),limit=case.get('limit',5),include_candidates=case.get('include_candidates',False),root=root)
            elif op=='skill_candidate_check':result=skill_candidate_check(case.get('input',{}),root)
            elif op=='skill_learn':result=skill_learn(case.get('input',{}),root)
            elif op=='skill_promotion_check':result=skill_promotion_check(case.get('input',{}),root)
            elif op=='skill_candidate_store':result=skill_candidate_store(case.get('input',{}),state_root=root/'.benchmark-state',apply=False,root=root)
            elif op=='context_compile':result=compile_context(case.get('input',{}),root=root)
            elif op=='os_plan':result=os_plan(case.get('input',{}),root=root)
            else:raise ACOError('Unsupported OS benchmark operation: '+str(op))
            passed=not bool(case.get('expected_error',False))
            for key,expected in case.get('expected',{}).items():
                if _get(result,key)!=expected:passed=False
        except (ACOError,ValueError,TypeError,KeyError) as exc:passed=bool(case.get('expected_error',False));result=None;error=str(exc)
        crit=bool(case.get('critical')) and not passed;critical+=int(crit);rows.append({'id':case.get('id'),'operation':op,'passed':passed,'critical_failure':crit,'error':error})
    if not rows:raise ACOError('ACO OS benchmark needs cases')
    score=round(100*sum(1 for x in rows if x['passed'])/len(rows),2);gate=data.get('gate',{});status='passed' if score>=float(gate.get('minimum_score',100)) and critical<=int(gate.get('maximum_critical_failures',0)) else 'failed'
    return {'status':status,'aco_version':VERSION,'cases':len(rows),'score':score,'critical_failures':critical,'rows':rows,'failures':[x for x in rows if not x['passed']]}
