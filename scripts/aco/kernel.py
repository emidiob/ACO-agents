"""ACO 1.0 kernel planner."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .bootstrap import resolve_runtime
from .common import ACOError, VERSION
from .context_compiler import compile_context
from .skills import skill_resolve, skill_search

def os_plan(packet:dict[str,Any],root:Path|None=None)->dict[str,Any]:
    if not isinstance(packet,dict):raise ACOError('ACO OS packet must be an object')
    task=packet.get('task')
    if not isinstance(task,dict):raise ACOError('task is required')
    text=task.get('text',task.get('title'))
    if not isinstance(text,str) or not text.strip():raise ACOError('task.text or task.title required')
    requested_skill_ids=packet.get('skill_ids',[])
    if not isinstance(requested_skill_ids,list) or any(not isinstance(x,str) for x in requested_skill_ids):raise ACOError('skill_ids must be a string list')
    skill_limit=packet.get('skill_limit',3)
    if not isinstance(skill_limit,int) or isinstance(skill_limit,bool) or not 0<=skill_limit<=8:raise ACOError('skill_limit must be 0..8')
    chosen=[];seen=set()
    for sid in requested_skill_ids:
        row=skill_resolve(sid,root=root)['skill']
        if sid not in seen:chosen.append(row);seen.add(sid)
    if len(chosen)<skill_limit:
        result=skill_search(packet.get('skill_query',text),tags=packet.get('skill_tags'),limit=max(1,skill_limit*2) if skill_limit else 1,root=root)
        for row in result['results']:
            if row['skill_id'] not in seen:chosen.append(row);seen.add(row['skill_id'])
            if len(chosen)>=skill_limit:break
    skill_refs=[f"skill://{row['skill_id']}@{row['version']}" for row in chosen];skill_sources=[]
    for row in chosen:
        skill_sources.append({'id':f"skill-body:{row['skill_id']}",'kind':'skill','load_level':1,'token_estimate':row['token_estimate'],'relevance':min(1.0,.72+.03*float(row.get('score',0))),'authority':float(row.get('quality',.8)),'recency':.8,'dependency':.8,'required':row['skill_id'] in requested_skill_ids,'private':False,'ref':skill_refs[len(skill_sources)]})
    context_sources=packet.get('sources',[])
    if not isinstance(context_sources,list):raise ACOError('sources must be a list')
    compiled=compile_context({'task':task,'program_ref':packet.get('program_ref'),'goal_ref':packet.get('goal_ref'),'role_ref':packet.get('role_ref'),'policy_refs':packet.get('policy_refs',[]),'skill_refs':skill_refs,'sources':skill_sources+context_sources,'budget_class':packet.get('budget_class','STANDARD'),'phase':packet.get('phase','initial'),'bootstrap_tokens':packet.get('bootstrap_tokens',220),'max_sources':packet.get('max_sources',12),'authorized_private_scope_ids':packet.get('authorized_private_scope_ids',[]),'missing_requirements':packet.get('missing_requirements',[]),'previous_snapshot':packet.get('previous_snapshot'),'response_verbosity':packet.get('response_verbosity','concise')},root=root)
    selected_skill_ids=[row['skill_id'] for row in chosen if f"skill-body:{row['skill_id']}" in compiled['token_plan']['selected_source_ids']];runtime=resolve_runtime(explicit_root=root) if root is not None else resolve_runtime()
    return {'status':compiled['status'],'aco_version':VERSION,'runtime':{'status':runtime['status'],'logical_root':runtime.get('logical_root'),'runtime_source':runtime.get('runtime_source'),'preload_repository':False},'selected_skill_ids':selected_skill_ids,'task_capsule':compiled['capsule'],'snapshot':compiled['snapshot'],'token_metrics':compiled['token_plan']['metrics'],'progressive_loading':compiled['progressive_loading'],'policy':'Concierge compiles one bounded task capsule. Roles and skills are references until selected; the full repository/history is never a default prompt.'}
