"""ACO 1.0 context compiler."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import ACOError, VERSION
from .token_budget import estimate_tokens, token_plan

def _ref(value,label,required=False):
    if value is None and not required:return None
    if not isinstance(value,str) or not value.strip():raise ACOError(label+' must be a non-empty reference string')
    return value.strip()

def _token_value(value,root):
    if value is None:return 0
    if isinstance(value,dict) and isinstance(value.get('token_estimate'),int):return max(0,value['token_estimate'])
    return estimate_tokens(value,root=root)

def compile_context(packet:dict[str,Any],root:Path|None=None)->dict[str,Any]:
    if not isinstance(packet,dict):raise ACOError('Context compiler packet must be an object')
    task=packet.get('task')
    if not isinstance(task,dict) or not isinstance(task.get('id'),str) or not task['id'].strip():raise ACOError('packet.task with id is required')
    task_text=task.get('text',task.get('title',''))
    if not isinstance(task_text,str) or not task_text.strip():raise ACOError('task.text or task.title is required')
    program_ref=_ref(packet.get('program_ref'),'program_ref');goal_ref=_ref(packet.get('goal_ref'),'goal_ref');role_ref=_ref(packet.get('role_ref'),'role_ref')
    policy_refs=packet.get('policy_refs',[]);skill_refs=packet.get('skill_refs',[])
    if not isinstance(policy_refs,list) or any(not isinstance(x,str) or not x.strip() for x in policy_refs):raise ACOError('policy_refs must be a string list')
    if not isinstance(skill_refs,list) or any(not isinstance(x,str) or not x.strip() for x in skill_refs):raise ACOError('skill_refs must be a string list')
    boot_tokens=int(packet.get('bootstrap_tokens',0))
    if boot_tokens<0:raise ACOError('bootstrap_tokens must be >=0')
    fixed_tokens=boot_tokens+_token_value(task_text,root)+_token_value({'program_ref':program_ref,'goal_ref':goal_ref,'role_ref':role_ref,'policy_refs':policy_refs,'skill_refs':skill_refs},root)
    sources=packet.get('sources',[])
    if not isinstance(sources,list):raise ACOError('sources must be a list')
    plan_request={'budget_class':packet.get('budget_class','STANDARD'),'base_tokens':fixed_tokens,'phase':packet.get('phase','initial'),'max_sources':packet.get('max_sources',12),'sources':sources,'authorized_private_scope_ids':packet.get('authorized_private_scope_ids',[]),'cross_scope_authorized':packet.get('cross_scope_authorized',False)}
    if packet.get('input_target') is not None:plan_request['input_target']=packet['input_target']
    if packet.get('output_target') is not None:plan_request['output_target']=packet['output_target']
    plan=token_plan(plan_request,root=root);selected=plan['selected_source_ids'];previous=packet.get('previous_snapshot') or {}
    if previous and not isinstance(previous,dict):raise ACOError('previous_snapshot must be an object')
    previous_ids=set(previous.get('selected_source_ids',[])) if isinstance(previous,dict) else set()
    if any(not isinstance(x,str) for x in previous_ids):raise ACOError('previous_snapshot.selected_source_ids must be strings')
    source_index={s.get('id'):s for s in sources if isinstance(s,dict) and isinstance(s.get('id'),str)};previous_hashes=previous.get('content_hashes',{}) if isinstance(previous,dict) else {}
    if previous_hashes and not isinstance(previous_hashes,dict):raise ACOError('previous_snapshot.content_hashes must be an object')
    reused=[];delta=[];content_hashes={}
    for sid in selected:
        row=source_index.get(sid,{});current_hash=row.get('content_sha256')
        if isinstance(current_hash,str) and current_hash:content_hashes[sid]=current_hash
        if sid in previous_ids and (not current_hash or previous_hashes.get(sid)==current_hash):reused.append(sid)
        else:delta.append(sid)
    missing_requirements=packet.get('missing_requirements',[])
    if not isinstance(missing_requirements,list) or any(not isinstance(x,str) for x in missing_requirements):raise ACOError('missing_requirements must be a string list')
    phase=packet.get('phase','initial');refine_recommended=bool(missing_requirements) and phase=='initial';verbosity=packet.get('response_verbosity','concise')
    if verbosity not in {'minimal','concise','standard','detailed'}:raise ACOError('response_verbosity must be minimal, concise, standard or detailed')
    capsule={'task':{'id':task['id'],'text':task_text},'program_ref':program_ref,'goal_ref':goal_ref,'role_ref':role_ref,'policy_refs':policy_refs,'skill_refs':skill_refs,'context_refs':selected,'delta_context_refs':delta,'reused_context_refs':reused,'response_contract':{'verbosity':verbosity,'output_token_target':plan['output_target'],'show_internal_reasoning':False,'evidence':'on_request_or_required'}}
    return {'status':'needs_refine' if refine_recommended else plan['status'],'aco_version':VERSION,'capsule':capsule,'token_plan':plan,'snapshot':{'selected_source_ids':selected,'content_hashes':content_hashes},'progressive_loading':{'phase':phase,'refine_recommended':refine_recommended,'missing_requirements':missing_requirements},'policy':'Compile minimal references first. Hydrate only selected authorized refs; unchanged context may be reused by the host instead of resent.'}
