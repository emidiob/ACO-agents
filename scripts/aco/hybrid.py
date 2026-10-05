from __future__ import annotations
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json


def memory_resolve(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ACOError('Memory request must be an object')
    memory_class=request.get('memory_class')
    cfg=read_json(ROOT/'config/memory-classes.json')
    spec=cfg.get('classes',{}).get(memory_class)
    if not spec:
        raise ACOError('Unknown memory_class: '+str(memory_class))
    persistent=bool(request.get('persistent_store_available',False))
    code_index=bool(request.get('code_index_available',False))
    explicit_save=bool(request.get('explicit_persistence_request',False))
    material=bool(request.get('material_change',False))
    destinations=[]
    status='resolved'
    notice=None
    read_status=None

    # v0.7.2 read boundary: retrieval is mode-aware and entity/client scoped.
    # This extends the existing storage resolver without changing legacy write/default behavior.
    if request.get('operation') == 'read':
        from .context import mode_policy
        relation=str(request.get('scope_relation','same_entity'))
        private=bool(request.get('private', memory_class == 'durable_context'))
        cross_scope_authorized=bool(request.get('cross_scope_authorized',False))
        policy=mode_policy(request.get('mode','LIGHT'), phase=request.get('phase','initial'),
                           first_pass_complete=bool(request.get('first_pass_complete',False)))
        if private and relation in {'other_private_entity','unknown'} and not cross_scope_authorized:
            status='scope_blocked';read_status='scope_blocked';destinations=[]
        elif private and not policy.get('allow_private',False):
            status='continue_without_private_context';read_status='mode_blocked';destinations=[]
        else:
            read_status='allowed'
            primary=spec.get('primary')
            destinations=[primary] if isinstance(primary,str) and primary else []
        return {
            'status':status,'aco_version':VERSION,'memory_class':memory_class,'operation':'read',
            'destinations':destinations,'read_status':read_status,'effective_mode':policy.get('effective_mode'),
            'prompt_for_drive':False,'notice':notice,'spec':spec,
            'policy':'Read only the minimum authorized same-scope context. Cross-client/entity private context is blocked unless explicitly authorized; persistence availability never becomes a startup prompt.'
        }

    if memory_class=='durable_context':
        if persistent and material:
            destinations=['canonical_aco_document']
        elif material:
            destinations=['current_context_pending_persistence']
            status='continue_without_persistence'
            if explicit_save:
                notice='Requested durable persistence is unavailable; return the finished work and mark the save as pending/not performed.'
        else:
            destinations=['current_context']
    elif memory_class=='code_architecture':
        destinations=['repository_current_source']
        if code_index: destinations.append('local_code_intelligence')
        if persistent and material: destinations.append('canonical_aco_document_summary')
        elif material and explicit_save:
            notice='Durable architecture-summary persistence is unavailable; keep repository/source truth and mark only the summary update pending.'
    elif memory_class=='code_structure':
        destinations=['local_code_intelligence' if code_index else 'repository_search']
    elif memory_class=='research_corpus':
        destinations=['authorized_research_system_or_supplied_files']
    elif memory_class=='task_context':
        destinations=['current_chat_or_local_handoff']
    elif memory_class=='execution_receipt':
        destinations=['bounded_local_or_host_evidence']
        if persistent and material: destinations.append('canonical_outcome_reference')
    elif memory_class=='tool_state':
        destinations=['runtime_discovery']

    return {
        'status':status,'aco_version':VERSION,'memory_class':memory_class,
        'destinations':destinations,'prompt_for_drive':False,
        'notice':notice,'spec':spec,
        'policy':'Drive/persistent knowledge stores meaningful durable continuity only; code/source remains authoritative and technical indexes stay rebuildable/local.'
    }
