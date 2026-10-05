from __future__ import annotations

from typing import Any, Iterable

from .common import ACOError

ALLOWED_RELATIONS = {
    'same_entity', 'explicit_relationship', 'ancestor', 'public_general',
    'repository_current_source', 'task_local', 'other_private_entity', 'unknown'
}


def normalize_authorized_scope_ids(value: Any) -> set[str]:
    """Return the exact private scope IDs explicitly authorized for this request.

    Wildcards and scalar booleans are intentionally rejected: cross-scope private
    retrieval must be bounded to named scopes rather than opened globally.
    """
    if value is None:
        return set()
    if not isinstance(value, (list, tuple, set)):
        raise ACOError('authorized_private_scope_ids must be a list of exact scope ids')
    out: set[str] = set()
    for raw in value:
        if not isinstance(raw, str) or not raw.strip():
            raise ACOError('authorized_private_scope_ids entries must be nonempty strings')
        scope_id = raw.strip()
        if scope_id == '*' or '*' in scope_id:
            raise ACOError('Wildcard private-scope authorization is not allowed')
        out.add(scope_id)
    return out


def private_scope_decision(*, private: bool, relation: str,
                           source_scope_id: str | None = None,
                           authorized_private_scope_ids: Iterable[str] | None = None,
                           legacy_cross_scope_authorized: bool = False) -> dict[str, Any]:
    """Decide whether scope alone permits a source before context-mode checks.

    `cross_scope_authorized=True` from v0.7.2 is retained only as a detectable
    legacy signal. It is no longer sufficient by itself because it can authorize
    an unbounded set of foreign private sources. Exact scope IDs are required.
    """
    relation = str(relation or 'unknown')
    if relation not in ALLOWED_RELATIONS:
        raise ACOError('Unknown scope_relation: ' + relation)
    if not private:
        return {'allowed': True, 'reason': 'non_private', 'authorization': 'not_required'}

    if relation == 'unknown':
        return {
            'allowed': False,
            'reason': 'unknown_private_scope_blocked',
            'authorization': 'scope_identity_or_relationship_required'
        }

    if relation != 'other_private_entity':
        return {'allowed': True, 'reason': 'same_or_bound_scope', 'authorization': 'not_required'}

    exact = set(authorized_private_scope_ids or [])
    sid = str(source_scope_id).strip() if source_scope_id is not None else ''
    if not sid:
        return {
            'allowed': False,
            'reason': 'cross_scope_identity_missing',
            'authorization': 'exact_scope_required'
        }
    if sid in exact:
        return {'allowed': True, 'reason': 'cross_scope_exactly_authorized', 'authorization': 'exact_scope'}
    return {
        'allowed': False,
        'reason': 'exact_cross_scope_authorization_required' if legacy_cross_scope_authorized else 'cross_scope_private_blocked',
        'authorization': 'legacy_boolean_insufficient' if legacy_cross_scope_authorized else 'not_authorized'
    }
