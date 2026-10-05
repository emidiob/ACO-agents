from __future__ import annotations
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json
from .scope import normalize_authorized_scope_ids, private_scope_decision


def _config() -> dict[str, Any]:
    cfg = read_json(ROOT/'config/context-engine.json')
    if cfg.get('schema_version') != 1:
        raise ACOError('Unsupported context-engine schema')
    return cfg


def mode_policy(mode: str, *, phase: str = 'initial', first_pass_complete: bool = False) -> dict[str, Any]:
    cfg = _config()
    mode = str(mode or 'LIGHT').upper()
    if mode not in cfg['modes']:
        raise ACOError('Unknown context mode: '+mode)
    if phase not in {'initial','refine'}:
        raise ACOError('phase must be initial or refine')
    effective = mode
    if mode == 'BLIND-FIRST':
        effective = 'LIGHT' if phase == 'refine' and first_pass_complete else 'BLIND'
    spec = dict(cfg['modes'][effective])
    spec.update({'requested_mode': mode, 'effective_mode': effective, 'phase': phase,
                 'first_pass_complete': bool(first_pass_complete)})
    return spec


def _source_priority(source: dict[str, Any]) -> tuple[float, float, float, int, str]:
    decisive = 1.0 if source.get('decisive') else 0.0
    relevance = max(0.0, min(1.0, float(source.get('relevance', 0.0))))
    authority = max(0.0, min(1.0, float(source.get('authority', 0.0))))
    chars = max(0, int(source.get('estimated_chars', 0)))
    return (decisive, relevance, authority, -chars, str(source.get('id','')))


def context_plan(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ACOError('Context request must be an object')
    policy = mode_policy(request.get('mode','LIGHT'), phase=request.get('phase','initial'),
                         first_pass_complete=bool(request.get('first_pass_complete',False)))
    sources = request.get('sources', [])
    if not isinstance(sources, list):
        raise ACOError('sources must be a list')
    authorized_private_scope_ids = normalize_authorized_scope_ids(request.get('authorized_private_scope_ids'))
    legacy_cross_scope_authorized = bool(request.get('cross_scope_authorized', False))
    selected: list[dict[str, Any]] = []
    denied: list[dict[str, str]] = []
    eligible: list[dict[str, Any]] = []
    missing_decisive: list[str] = []
    candidate_chars = 0

    for raw in sources:
        if not isinstance(raw, dict) or not raw.get('id'):
            raise ACOError('Each context source needs an id')
        source = dict(raw)
        relation = source.get('scope_relation','unknown')
        chars = max(0, int(source.get('estimated_chars',0)))
        candidate_chars += chars
        if not bool(source.get('available', True)):
            denied.append({'id':source['id'],'reason':'unavailable'})
            if source.get('decisive'): missing_decisive.append(source['id'])
            continue
        private = bool(source.get('private', False))
        boundary = private_scope_decision(
            private=private,
            relation=relation,
            source_scope_id=source.get('scope_id'),
            authorized_private_scope_ids=authorized_private_scope_ids,
            legacy_cross_scope_authorized=legacy_cross_scope_authorized,
        )
        if not boundary['allowed']:
            denied.append({'id':source['id'],'reason':boundary['reason']})
            if source.get('decisive'): missing_decisive.append(source['id'])
            continue
        if private and not bool(policy.get('allow_private', False)):
            denied.append({'id':source['id'],'reason':'mode_blocks_private_context'})
            if source.get('decisive'): missing_decisive.append(source['id'])
            continue
        relevance=max(0.0,min(1.0,float(source.get('relevance',0.0))))
        if not source.get('decisive') and relevance < float(policy.get('minimum_relevance',0.0)):
            denied.append({'id':source['id'],'reason':'below_relevance_floor'})
            continue
        eligible.append(source)

    eligible.sort(key=_source_priority, reverse=True)
    max_sources = int(policy.get('max_sources',0))
    max_chars = int(policy.get('max_chars',0))
    selected_chars = 0
    for source in eligible:
        chars=max(0,int(source.get('estimated_chars',0)))
        if len(selected) >= max_sources:
            denied.append({'id':source['id'],'reason':'source_budget_exceeded'})
            if source.get('decisive'): missing_decisive.append(source['id'])
            continue
        if selected and selected_chars + chars > max_chars:
            denied.append({'id':source['id'],'reason':'character_budget_exceeded'})
            if source.get('decisive'): missing_decisive.append(source['id'])
            continue
        if not selected and chars > max_chars and max_chars > 0:
            # A single decisive source may be selected, but the over-budget fact remains explicit.
            if source.get('decisive'):
                selected.append(source); selected_chars += chars
                denied.append({'id':source['id'],'reason':'selected_decisive_source_over_budget'})
            else:
                denied.append({'id':source['id'],'reason':'character_budget_exceeded'})
            continue
        selected.append(source); selected_chars += chars

    persistent = bool(request.get('persistent_store_available',False))
    explicit_save = bool(request.get('explicit_persistence_request',False))
    material = bool(request.get('material_change',False))
    persistence_status = 'not_needed'
    notice = None
    if material:
        persistence_status = 'ready' if persistent else 'continue_without_persistence'
        if explicit_save and not persistent:
            notice = 'Requested durable persistence is unavailable; continue the task and mark only the save as pending/not performed.'

    ratio = (selected_chars / candidate_chars) if candidate_chars else 0.0
    status = 'needs_decisive_context' if missing_decisive else 'planned'
    return {
        'status': status, 'aco_version': VERSION, 'mode': policy['requested_mode'],
        'effective_mode': policy['effective_mode'], 'phase': policy['phase'],
        'selected_source_ids': [x['id'] for x in selected], 'denied_sources': denied,
        'missing_decisive_source_ids': sorted(set(missing_decisive)),
        'prompt_for_drive': False, 'persistence_status': persistence_status, 'notice': notice,
        'metrics': {
            'candidate_sources': len(sources), 'selected_sources': len(selected),
            'candidate_chars': candidate_chars, 'selected_chars': selected_chars,
            'selection_ratio': round(ratio, 4)
        },
        'authorization': {
            'authorized_private_scope_ids': sorted(authorized_private_scope_ids),
            'legacy_cross_scope_boolean_seen': legacy_cross_scope_authorized,
            'legacy_boolean_grants_access': False,
        },
        'policy': policy,
        'boundary': 'Private context remains entity/client scoped. Cross-scope private retrieval requires an exact authorized scope id; unknown private scope and wildcard/global authorization stay blocked.'
    }
