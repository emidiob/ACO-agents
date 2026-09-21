from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json

RESOURCE_STATES = {
    'LEARNED_SKILL', 'REFERENCE', 'OPTIONAL_TOOL', 'CONNECTED_INTEGRATION',
    'LOCAL_RUNTIME', 'UNAVAILABLE', 'BLOCKED'
}
PERMISSION_LEVELS = {
    'READ', 'DRAFT', 'PREVIEW', 'WRITE', 'SHARE', 'SEND', 'PUBLISH',
    'APPLY', 'DEPLOY', 'DELETE', 'PURCHASE', 'SIGN'
}
TERMINAL_RECEIPT_STATES = {
    'created', 'updated', 'deleted', 'sent', 'delivered', 'read', 'scheduled',
    'published', 'submitted', 'deployed', 'purchased', 'signed', 'failed',
    'cancelled'
}
RECEIPT_STATES = {
    'prepared', 'executing', 'executed', 'accepted', 'queued', 'unknown',
    *TERMINAL_RECEIPT_STATES
}


def _obj(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ACOError(f'{label} must be an object')
    return value


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _canonical_hash(value: Any) -> str:
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    except (TypeError, ValueError) as exc:
        raise ACOError('Action packet must be finite JSON data') from exc
    return hashlib.sha256(raw).hexdigest()


def _capability_model(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    data = read_json(root / 'config/capabilities.json')
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported capability-model schema')
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Capability-model version mismatch')
    return data


def _permission_policy(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    data = read_json(root / 'config/permission-policy.json')
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported permission-policy schema')
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Permission-policy version mismatch')
    return data


def action_packet(request: dict[str, Any]) -> dict[str, Any]:
    r = _obj(request, 'request')
    for key in ('scope_id', 'capability_id', 'operation'):
        if not _text(r.get(key)):
            raise ACOError(f'request.{key} is required')
    target = r.get('target')
    if target is not None and not isinstance(target, (str, dict)):
        raise ACOError('request.target must be a string, object or null')
    payload_ref = r.get('payload_ref')
    if payload_ref is not None and not _text(payload_ref):
        raise ACOError('request.payload_ref must be a non-empty string when provided')
    packet = {
        'scope_id': r['scope_id'],
        'capability_id': r['capability_id'],
        'operation': r['operation'],
        'target': target,
        'payload_ref': payload_ref,
        'parameters': r.get('parameters', {}),
    }
    if not isinstance(packet['parameters'], dict):
        raise ACOError('request.parameters must be an object')
    return packet


def action_hash(request: dict[str, Any]) -> str:
    return _canonical_hash(action_packet(request))


def _capability_spec(capability_id: str, root: Path | None = None) -> dict[str, Any]:
    model = _capability_model(root)
    spec = model.get('capabilities', {}).get(capability_id)
    if not isinstance(spec, dict):
        raise ACOError(f'Unknown capability_id: {capability_id}')
    return spec


def permission_check(request: dict[str, Any], approval: dict[str, Any] | None = None,
                     root: Path | None = None) -> dict[str, Any]:
    packet = action_packet(request)
    spec = _capability_spec(packet['capability_id'], root)
    if packet['operation'] not in spec.get('operations', []):
        return {
            'status': 'blocked', 'aco_version': VERSION, 'permission': spec.get('permission'),
            'approval_required': True, 'allowed': False,
            'errors': [f"Operation {packet['operation']} is not declared for {packet['capability_id']}"],
            'action_sha256': _canonical_hash(packet),
        }
    level = spec.get('permission')
    if level not in PERMISSION_LEVELS:
        raise ACOError(f'Invalid permission level for {packet["capability_id"]}')
    policy = _permission_policy(root).get('levels', {}).get(level)
    if not isinstance(policy, dict):
        raise ACOError(f'Missing policy for permission level {level}')
    approval_required = bool(policy.get('approval_required'))
    h = _canonical_hash(packet)
    errors: list[str] = []
    approval_valid = not approval_required
    if approval_required:
        if not isinstance(approval, dict):
            errors.append(f'{level} requires explicit scoped approval.')
        else:
            if approval.get('denied') is True:
                errors.append('Approval explicitly denied.')
            if approval.get('scope_id') != packet['scope_id']:
                errors.append('Approval scope does not match the action.')
            if approval.get('capability_id') != packet['capability_id']:
                errors.append('Approval capability does not match the action.')
            if approval.get('operation') != packet['operation']:
                errors.append('Approval operation does not match the action.')
            if approval.get('action_sha256') != h:
                errors.append('Approval hash does not bind the final action packet.')
            if not _text(approval.get('approval_ref')):
                errors.append('Approval needs an actual reference.')
            expires = approval.get('expires_at')
            if expires is not None:
                try:
                    dt = datetime.fromisoformat(str(expires).replace('Z', '+00:00'))
                    if dt.tzinfo is None:
                        raise ValueError('timezone required')
                    if dt.astimezone(timezone.utc) <= datetime.now(timezone.utc):
                        errors.append('Approval expired.')
                except ValueError:
                    errors.append('approval.expires_at must be an ISO timestamp with timezone.')
            approval_valid = not errors
    return {
        'status': 'allowed' if approval_valid else 'approval_required',
        'aco_version': VERSION,
        'permission': level,
        'risk': spec.get('risk'),
        'approval_required': approval_required,
        'approval_valid': approval_valid,
        'allowed': approval_valid,
        'action_sha256': h,
        'errors': errors,
        'policy': policy.get('rule', ''),
    }


def _inventory_index(inventory: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if inventory is None:
        return {}
    inv = _obj(inventory, 'inventory')
    items = inv.get('capabilities', [])
    if not isinstance(items, list):
        raise ACOError('inventory.capabilities must be a list')
    index: dict[str, dict[str, Any]] = {}
    for raw in items:
        item = _obj(raw, 'inventory capability')
        cid = item.get('id')
        if not _text(cid):
            raise ACOError('inventory capability id is required')
        if cid in index:
            raise ACOError(f'Duplicate inventory capability: {cid}')
        state = item.get('resource_state')
        if state not in RESOURCE_STATES:
            raise ACOError(f'{cid}: resource_state must be one of {sorted(RESOURCE_STATES)}')
        operations = item.get('operations', [])
        if not isinstance(operations, list) or not all(_text(x) for x in operations):
            raise ACOError(f'{cid}: operations must be a string list')
        index[cid] = item
    return index


def capability_state(capability_id: str, operation: str, inventory: dict[str, Any] | None = None,
                     root: Path | None = None) -> dict[str, Any]:
    spec = _capability_spec(capability_id, root)
    if operation not in spec.get('operations', []):
        return {'id': capability_id, 'state': 'operation_unsupported', 'ready': False}
    item = _inventory_index(inventory).get(capability_id)
    if item is None:
        return {'id': capability_id, 'state': 'missing', 'ready': False,
                'resource_state': 'UNAVAILABLE'}
    resource_state = item['resource_state']
    if resource_state in ('LEARNED_SKILL', 'REFERENCE'):
        return {'id': capability_id, 'state': 'knowledge_only', 'ready': False,
                'resource_state': resource_state}
    if resource_state == 'OPTIONAL_TOOL':
        return {'id': capability_id, 'state': 'not_installed_or_connected', 'ready': False,
                'resource_state': resource_state}
    if resource_state == 'UNAVAILABLE':
        return {'id': capability_id, 'state': 'unavailable', 'ready': False,
                'resource_state': resource_state}
    if resource_state == 'BLOCKED':
        return {'id': capability_id, 'state': 'blocked', 'ready': False,
                'resource_state': resource_state}
    if operation not in item.get('operations', []):
        return {'id': capability_id, 'state': 'operation_unavailable', 'ready': False,
                'resource_state': resource_state}
    if not item.get('available', True):
        return {'id': capability_id, 'state': 'unavailable', 'ready': False,
                'resource_state': resource_state}
    if not item.get('authorized', False):
        return {'id': capability_id, 'state': 'available_not_authorized', 'ready': False,
                'resource_state': resource_state}
    if not item.get('verified', False) or not _text(item.get('evidence_ref')):
        return {'id': capability_id, 'state': 'authorized_unverified', 'ready': False,
                'resource_state': resource_state}
    return {
        'id': capability_id, 'state': 'ready', 'ready': True,
        'resource_state': resource_state, 'adapter_id': item.get('adapter_id'),
        'evidence_ref': item.get('evidence_ref')
    }


def execution_plan(request: dict[str, Any], inventory: dict[str, Any] | None = None,
                   approval: dict[str, Any] | None = None,
                   previous_receipt: dict[str, Any] | None = None,
                   root: Path | None = None) -> dict[str, Any]:
    packet = action_packet(request)
    spec = _capability_spec(packet['capability_id'], root)
    h = _canonical_hash(packet)
    previous = None
    if previous_receipt is not None:
        previous = receipt_check(previous_receipt, root=root)
        previous_hash = previous_receipt.get('action_sha256')
        if previous_hash == h:
            state = previous_receipt.get('status')
            if state in ('unknown', 'executing'):
                return {
                    'status': 'reconcile_required', 'aco_version': VERSION,
                    'action_sha256': h, 'capability': packet['capability_id'],
                    'reason': 'Previous exact action has an uncertain/in-flight outcome. Reconcile before retrying.',
                    'execute': False, 'previous_receipt': previous,
                }
            if state in RECEIPT_STATES and state not in ('failed', 'cancelled', 'prepared'):
                return {
                    'status': 'already_executed', 'aco_version': VERSION,
                    'action_sha256': h, 'capability': packet['capability_id'],
                    'reason': 'Previous exact action already has execution evidence. Inspect it instead of duplicating.',
                    'execute': False, 'previous_receipt': previous,
                }
    cap = capability_state(packet['capability_id'], packet['operation'], inventory, root)
    perm = permission_check(request, approval, root)
    blockers = []
    if not cap.get('ready'):
        blockers.append('Capability is not execution-ready: ' + cap.get('state', 'unknown'))
    if not perm.get('allowed'):
        blockers.extend(perm.get('errors', []))
    ready = not blockers
    fallback = request.get('fallback') or spec.get('fallback') or 'Prepare a draft/plan without claiming the unavailable action.'
    return {
        'status': 'ready_to_execute' if ready else 'fallback_required',
        'aco_version': VERSION,
        'action_sha256': h,
        'request': packet,
        'capability': cap,
        'permission': perm,
        'blockers': blockers,
        'fallback': fallback,
        'execute': False,
        'policy': 'This command resolves execution readiness only. It never calls an adapter or performs the action.'
    }


def receipt_check(receipt: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    r = _obj(receipt, 'receipt')
    errors: list[str] = []
    for key in ('receipt_id', 'scope_id', 'capability_id', 'operation', 'action_sha256', 'status'):
        if not _text(r.get(key)):
            errors.append(f'{key} is required')
    cid = r.get('capability_id')
    spec = None
    if _text(cid):
        try:
            spec = _capability_spec(cid, root)
        except ACOError as exc:
            errors.append(str(exc))
    status = r.get('status')
    if status not in RECEIPT_STATES:
        errors.append('status is not a supported receipt state')
    if spec is not None and _text(r.get('operation')) and r['operation'] not in spec.get('operations', []):
        errors.append('receipt operation is not declared for the capability')
    h = r.get('action_sha256')
    if _text(h) and (len(h) != 64 or any(c not in '0123456789abcdef' for c in h)):
        errors.append('action_sha256 must be a lowercase SHA-256')
    evidence = r.get('evidence', [])
    if not isinstance(evidence, list):
        errors.append('evidence must be a list')
        evidence = []
    consequential = spec is not None and spec.get('permission') in {
        'WRITE','SHARE','SEND','PUBLISH','APPLY','DEPLOY','DELETE','PURCHASE','SIGN'
    }
    if status in RECEIPT_STATES - {'prepared', 'executing', 'unknown', 'failed', 'cancelled'}:
        if not any(isinstance(x, str) and x.strip() for x in evidence):
            errors.append('Executed/outcome states require evidence references.')
    if consequential and status in TERMINAL_RECEIPT_STATES and status not in ('failed', 'cancelled'):
        if not _text(r.get('adapter_id')):
            errors.append('Consequential terminal receipt requires adapter_id.')
        if not _text(r.get('provider_ref')) and not _text(r.get('artifact_ref')):
            errors.append('Consequential terminal receipt requires provider_ref or artifact_ref.')
    return {
        'status': 'valid' if not errors else 'invalid', 'aco_version': VERSION,
        'errors': errors,
        'receipt_state': status,
        'verified_claim_level': _receipt_claim_level(status) if status in RECEIPT_STATES else 'none',
        'policy': 'A receipt is evidence about an action outcome, not authorization for another action.'
    }


def _receipt_claim_level(status: str) -> str:
    mapping = {
        'prepared': 'prepared', 'executing': 'attempt_started', 'executed': 'tool_executed',
        'accepted': 'provider_accepted', 'queued': 'provider_queued', 'unknown': 'unknown',
        'created': 'provider_confirmed', 'updated': 'provider_confirmed', 'deleted': 'provider_confirmed',
        'sent': 'provider_sent', 'delivered': 'provider_delivered', 'read': 'provider_read',
        'scheduled': 'provider_scheduled', 'published': 'provider_published', 'submitted': 'provider_submitted',
        'deployed': 'provider_deployed', 'purchased': 'provider_purchased', 'signed': 'provider_signed',
        'failed': 'failed', 'cancelled': 'cancelled'
    }
    return mapping[status]


def adapter_check(data: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    d = _obj(data, 'adapter inventory')
    adapters = d.get('adapters', [])
    if not isinstance(adapters, list):
        raise ACOError('adapters must be a list')
    allowed_kinds = set(read_json((root or ROOT) / 'config/adapter-contract.json').get('kinds', []))
    known_caps = set(_capability_model(root).get('capabilities', {}))
    errors: list[str] = []
    rows = []
    seen = set()
    for raw in adapters:
        a = _obj(raw, 'adapter')
        aid = a.get('id')
        row_errors = []
        if not _text(aid) or aid in seen:
            row_errors.append('id must be non-empty and unique')
        if _text(aid): seen.add(aid)
        if a.get('kind') not in allowed_kinds:
            row_errors.append('unsupported adapter kind')
        caps = a.get('capabilities', [])
        if not isinstance(caps, list) or not all(_text(x) for x in caps):
            row_errors.append('capabilities must be a string list')
            caps = []
        for cid in caps:
            if cid not in known_caps:
                row_errors.append('unknown capability: ' + cid)
        if a.get('verified') is True and not _text(a.get('evidence_ref')):
            row_errors.append('verified adapter needs evidence_ref')
        if a.get('credentials_embedded') is True:
            row_errors.append('credentials must never be embedded in the adapter inventory')
        rows.append({'id': aid, 'status': 'valid' if not row_errors else 'invalid', 'errors': row_errors})
        errors.extend([f'{aid or "<missing>"}: {x}' for x in row_errors])
    return {
        'status': 'valid' if not errors else 'invalid', 'aco_version': VERSION,
        'adapters': rows, 'errors': errors,
        'policy': 'Adapters are host-supplied execution bridges. ACO ships contracts, not credentials or assumed connections.'
    }


def workflow_check(data: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    d = _obj(data, 'workflow packet')
    cfg = read_json((root or ROOT) / 'config/workflow-states.json')
    transitions = {k: set(v) for k, v in cfg.get('transitions', {}).items()}
    history = d.get('history', [])
    if not isinstance(history, list) or not history:
        raise ACOError('workflow.history must be a non-empty list')
    errors: list[str] = []
    previous = None
    unknown_open = False
    for idx, event in enumerate(history):
        e = _obj(event, f'history[{idx}]')
        state = e.get('state')
        if state not in transitions:
            errors.append(f'history[{idx}] has unsupported state {state}')
            previous = state
            continue
        if previous is not None and state not in transitions.get(previous, set()):
            errors.append(f'invalid transition: {previous} -> {state}')
        if state == 'unknown':
            unknown_open = True
        if unknown_open and state not in ('unknown', 'reconciled', 'blocked'):
            errors.append('unknown outcome must be reconciled before normal progression')
        if state == 'reconciled':
            if not _text(e.get('evidence_ref')):
                errors.append('reconciled state requires evidence_ref')
            unknown_open = False
        if state in ('executed', 'checked', 'reviewed', 'closed') and not _text(e.get('evidence_ref')):
            errors.append(f'{state} requires evidence_ref')
        previous = state
    return {
        'status': 'valid' if not errors else 'invalid', 'aco_version': VERSION,
        'current_state': previous, 'errors': errors,
        'durability': d.get('durability', 'temporary_or_existing_compact_record'),
        'policy': 'Workflow state does not create a new project/entity and does not itself authorize external actions.'
    }


def execution_summary(data: dict[str, Any]) -> dict[str, Any]:
    d = _obj(data, 'execution record')
    receipts = d.get('receipts', [])
    if not isinstance(receipts, list):
        raise ACOError('receipts must be a list')
    rows = []
    unresolved = []
    for raw in receipts:
        r = _obj(raw, 'receipt')
        check = receipt_check(r)
        rows.append({
            'receipt_id': r.get('receipt_id'), 'capability_id': r.get('capability_id'),
            'operation': r.get('operation'), 'target': r.get('target'), 'status': r.get('status'),
            'claim_level': check.get('verified_claim_level'), 'valid': check['status'] == 'valid',
            'evidence': r.get('evidence', [])
        })
        if r.get('status') in ('unknown', 'executing') or check['status'] != 'valid':
            unresolved.append(r.get('receipt_id'))
    return {
        'aco_version': VERSION,
        'task': d.get('task'), 'scope_id': d.get('scope_id'),
        'actions': rows, 'unresolved_receipts': unresolved,
        'files_created': d.get('files_created', []),
        'checks': d.get('checks', []),
        'next_action': d.get('next_action'),
        'policy': 'Operational summary only: no hidden reasoning, and no outcome stronger than the underlying receipt evidence.'
    }


def execution_benchmark(path: Path | None = None, root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    path = (path or root / 'config/execution-benchmark.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported execution benchmark schema')
    cases = data.get('cases', [])
    if not isinstance(cases, list) or not cases:
        raise ACOError('Execution benchmark needs cases')
    correct = 0
    critical_failures = 0
    rows = []
    for case in cases:
        approval = case.get('approval')
        if approval == '$AUTO_VALID':
            req = case['request']
            p = permission_check(req, None, root)
            approval = {
                'scope_id': req['scope_id'], 'capability_id': req['capability_id'],
                'operation': req['operation'], 'action_sha256': p['action_sha256'],
                'approval_ref': 'benchmark-explicit-approval'
            }
        result = execution_plan(case['request'], case.get('inventory'), approval, case.get('previous_receipt'), root)
        ok = result['status'] == case.get('expected_status')
        expected_cap_state = case.get('expected_capability_state')
        if expected_cap_state is not None:
            ok = ok and result.get('capability', {}).get('state') == expected_cap_state
        correct += int(ok)
        critical = bool(case.get('critical', True)) and not ok
        critical_failures += int(critical)
        rows.append({'id': case.get('id'), 'passed': ok, 'actual': result['status'],
                     'expected': case.get('expected_status'), 'critical_failure': critical})
    score = correct / len(cases) * 100
    gate = data.get('gate', {'minimum_score': 95.0, 'maximum_critical_failures': 0})
    passed = score >= float(gate.get('minimum_score', 95.0)) and critical_failures <= int(gate.get('maximum_critical_failures', 0))
    return {
        'status': 'passed' if passed else 'failed', 'aco_version': VERSION,
        'cases': len(cases), 'score': round(score, 2), 'critical_failures': critical_failures,
        'gate': gate, 'rows': rows,
        'limitations': 'Deterministic execution-policy conformance only; no external adapter or provider was called.'
    }
