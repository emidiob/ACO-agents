"""ACO 1.0 token-budget selection primitives."""
from __future__ import annotations
import math
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json
from .scope import normalize_authorized_scope_ids, private_scope_decision

def _policy(root=None):
    root=(root or ROOT).expanduser().absolute();data=read_json(root/'config/token-policy.json')
    if data.get('schema_version')!=1:raise ACOError('Unsupported token-policy schema')
    if data.get('aco_version')!=VERSION and root==ROOT:raise ACOError('Token policy version mismatch')
    return data

def estimate_tokens(value,*,root=None):
    policy=_policy(root)
    if value is None:return 0
    if isinstance(value,bytes):chars=len(value.decode('utf-8',errors='replace'))
    elif isinstance(value,str):chars=len(value)
    else:
        import json;chars=len(json.dumps(value,ensure_ascii=False,separators=(',',':')))
    return 0 if chars==0 else max(1,math.ceil(chars/float(policy.get('chars_per_token_estimate',4.0))))

def _tokens(source,root=None):
    value=source.get('token_estimate')
    if isinstance(value,int) and not isinstance(value,bool) and value>=0:return value
    if isinstance(source.get('estimated_chars'),int) and source['estimated_chars']>=0:
        cpp=float(_policy(root).get('chars_per_token_estimate',4.0));return 0 if source['estimated_chars']==0 else max(1,math.ceil(source['estimated_chars']/cpp))
    if 'content' in source:return estimate_tokens(source.get('content'),root=root)
    raise ACOError(f'{source.get("id","source")}: token_estimate, estimated_chars or content is required')

def _bounded(value,default=0.0):
    try:return max(0.0,min(1.0,float(value)))
    except (TypeError,ValueError):return default

def _utility(source,policy):
    w=policy.get('utility_weights',{})
    value=_bounded(source.get('relevance'))*float(w.get('relevance',.38))+_bounded(source.get('authority',.5),.5)*float(w.get('authority',.18))+_bounded(source.get('recency',.5),.5)*float(w.get('recency',.10))+_bounded(source.get('dependency',0))*float(w.get('dependency',.24))+(1.0 if source.get('decisive') else 0.0)*float(w.get('decisive',.10))
    return round(value,6)

def _knapsack(rows,budget,max_sources):
    states={(0,0):(0.0,(),())}
    for idx,row in enumerate(rows):
        cost=int(row['tokens']);util=float(row['utility'])
        if cost>budget:continue
        for (used,count),(score,ids,indices) in list(states.items()):
            if count>=max_sources or used+cost>budget:continue
            key=(used+cost,count+1);cand_ids=tuple(sorted(ids+(str(row['id']),)));cand=(score+util,cand_ids,indices+(idx,));prev=states.get(key)
            if prev is None or cand[0]>prev[0]+1e-12 or (abs(cand[0]-prev[0])<=1e-12 and cand[1]<prev[1]):states[key]=cand
    best=max(states.items(),key=lambda kv:(kv[1][0],-kv[0][0],-kv[0][1],tuple(reversed(kv[1][1]))))[1]
    return [rows[i] for i in best[2]]

def token_plan(request,root=None):
    if not isinstance(request,dict):raise ACOError('Token plan request must be an object')
    policy=_policy(root);budget_class=str(request.get('budget_class','STANDARD')).upper();classes=policy.get('budget_classes',{})
    if budget_class not in classes:raise ACOError('Unknown budget_class: '+budget_class)
    spec=dict(classes[budget_class]);input_target=request.get('input_target',spec['input_target']);output_target=request.get('output_target',spec['output_target'])
    if not isinstance(input_target,int) or isinstance(input_target,bool) or input_target<100:raise ACOError('input_target must be an integer >=100')
    if not isinstance(output_target,int) or isinstance(output_target,bool) or output_target<1:raise ACOError('output_target must be a positive integer')
    base_tokens=request.get('base_tokens',0)
    if not isinstance(base_tokens,int) or isinstance(base_tokens,bool) or base_tokens<0:raise ACOError('base_tokens must be a non-negative integer')
    phase=request.get('phase','initial')
    if phase not in {'initial','refine'}:raise ACOError('phase must be initial or refine')
    max_level=int(policy.get('levels',{}).get('initial_max_load_level' if phase=='initial' else 'refine_max_load_level',1));max_sources=int(request.get('max_sources',spec.get('max_sources',12)))
    if max_sources<0:raise ACOError('max_sources must be >=0')
    sources=request.get('sources',[])
    if not isinstance(sources,list):raise ACOError('sources must be a list')
    authorized=normalize_authorized_scope_ids(request.get('authorized_private_scope_ids'));eligible=[];denied=[];required=[];authorized_candidate_tokens=0;authorized_candidate_sources=0;minimum_relevance=float(policy.get('minimum_relevance',.12))
    for raw in sources:
        if not isinstance(raw,dict) or not isinstance(raw.get('id'),str) or not raw['id'].strip():raise ACOError('Each source requires a non-empty id')
        row=dict(raw)
        if not bool(row.get('available',True)):denied.append({'id':row['id'],'reason':'unavailable'});continue
        private=bool(row.get('private',False));boundary=private_scope_decision(private=private,relation=row.get('scope_relation','task_local' if not private else 'unknown'),source_scope_id=row.get('scope_id'),authorized_private_scope_ids=authorized,legacy_cross_scope_authorized=bool(request.get('cross_scope_authorized',False)))
        if not boundary['allowed']:denied.append({'id':row['id'],'reason':boundary['reason']});continue
        row['tokens']=_tokens(row,root);authorized_candidate_tokens+=row['tokens'];authorized_candidate_sources+=1
        level=row.get('load_level',1)
        if not isinstance(level,int) or isinstance(level,bool) or level not in {0,1,2}:raise ACOError(f'{row["id"]}: load_level must be 0, 1 or 2')
        if level>max_level:denied.append({'id':row['id'],'reason':'deferred_to_refine'});continue
        relevance=_bounded(row.get('relevance'))
        if not row.get('required') and not row.get('decisive') and relevance<minimum_relevance:denied.append({'id':row['id'],'reason':'below_relevance_floor'});continue
        row['utility']=_utility(row,policy);row['load_level']=level;eligible.append(row)
        if row.get('required') or row.get('decisive'):required.append(row)
    required_ids={r['id'] for r in required};required_sorted=sorted(required,key=lambda r:(not bool(r.get('decisive')),-r['utility'],r['tokens'],r['id']));selected=list(required_sorted);used=base_tokens+sum(r['tokens'] for r in required_sorted);source_slots=max(0,max_sources-len(required_sorted));remaining_budget=max(0,input_target-used);optional=[r for r in eligible if r['id'] not in required_ids];optional.sort(key=lambda r:r['id']);selected+=_knapsack(optional,remaining_budget,source_slots) if source_slots else []
    selected_ids=[r['id'] for r in selected]
    for row in eligible:
        if row['id'] not in selected_ids:denied.append({'id':row['id'],'reason':'token_budget_optimized_out'})
    selected_source_tokens=sum(r['tokens'] for r in selected);selected_total=base_tokens+selected_source_tokens;baseline_total=base_tokens+authorized_candidate_tokens;reduction=0.0 if baseline_total==0 else max(0.0,1.0-selected_total/baseline_total);overflow=max(0,selected_total-input_target)
    missing_decisive=[d['id'] for d in denied if d['reason'] not in {'deferred_to_refine','token_budget_optimized_out','below_relevance_floor'} and any(s.get('id')==d['id'] and s.get('decisive') for s in sources)]
    status='needs_decisive_context' if missing_decisive else ('target_overflow' if overflow else 'planned')
    return {'status':status,'aco_version':VERSION,'budget_class':budget_class,'phase':phase,'input_target':input_target,'output_target':output_target,'base_tokens':base_tokens,'selected_source_ids':selected_ids,'denied_sources':denied,'missing_decisive_source_ids':sorted(set(missing_decisive)),'metrics':{'authorized_candidate_sources':authorized_candidate_sources,'eligible_sources':len(eligible),'selected_sources':len(selected),'baseline_input_tokens':baseline_total,'selected_input_tokens':selected_total,'selected_source_tokens':selected_source_tokens,'target_overflow_tokens':overflow,'input_reduction_ratio':round(reduction,4),'selected_utility':round(sum(r['utility'] for r in selected),4)},'selected':[{'id':r['id'],'tokens':r['tokens'],'utility':r['utility'],'load_level':r['load_level']} for r in selected],'authorization':{'authorized_private_scope_ids':sorted(authorized),'legacy_cross_scope_boolean_grants_access':False},'policy':'Maximize useful authorized context under a soft token target. Safety, decisive evidence and exact private-scope rules outrank token savings.'}
