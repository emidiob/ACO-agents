from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json


def handoff_check(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise ACOError('Handoff packet must be an object')
    required = ('task', 'owner', 'status', 'decisions', 'evidence', 'unknowns', 'next_action')
    missing = [k for k in required if k not in packet]
    errors = []
    if missing:
        errors.append('Missing fields: ' + ', '.join(missing))
    if packet.get('status') not in ('prepared', 'executed', 'checked', 'reviewed', 'blocked'):
        errors.append('status must be prepared/executed/checked/reviewed/blocked')
    for key in ('decisions', 'evidence', 'unknowns'):
        if key in packet and not isinstance(packet[key], list):
            errors.append(f'{key} must be a list')
    if 'owner' in packet and not isinstance(packet['owner'], str):
        errors.append('owner must be a string role/entity identifier')
    if 'next_action' in packet and not isinstance(packet['next_action'], str):
        errors.append('next_action must be a string')
    if packet.get('status') in ('checked', 'reviewed') and not packet.get('evidence'):
        errors.append('checked/reviewed handoffs require evidence')
    return {
        'status': 'valid' if not errors else 'invalid', 'aco_version': VERSION,
        'errors': errors, 'packet': packet,
        'policy': 'Handoffs carry only task-relevant decisions/evidence/unknowns; they do not broaden scope or authorize execution.'
    }


def capability_resolve(request: dict[str, Any], inventory: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ACOError('Capability request must be an object')
    required = request.get('required', [])
    optional = request.get('optional', [])
    if not isinstance(required, list) or not all(isinstance(x, str) and x.strip() for x in required):
        raise ACOError('required must be a list of capability strings')
    if not isinstance(optional, list) or not all(isinstance(x, str) and x.strip() for x in optional):
        raise ACOError('optional must be a list of capability strings')
    inventory = inventory or {'capabilities': []}
    caps = inventory.get('capabilities', [])
    if not isinstance(caps, list):
        raise ACOError('inventory.capabilities must be a list')
    index: dict[str, dict[str, Any]] = {}
    for item in caps:
        if isinstance(item, str):
            index[item] = {'id': item, 'available': True, 'authorized': False, 'verified': False}
        elif isinstance(item, dict) and isinstance(item.get('id'), str):
            index[item['id']] = item
        else:
            raise ACOError('Each inventory capability must be a string or object with id')

    def state(cid: str) -> dict[str, Any]:
        item = index.get(cid)
        if not item:
            return {'id': cid, 'state': 'missing'}
        if not item.get('available', True):
            return {'id': cid, 'state': 'unavailable'}
        if not item.get('authorized', False):
            return {'id': cid, 'state': 'available_not_authorized'}
        if not item.get('verified', False):
            return {'id': cid, 'state': 'authorized_unverified'}
        return {'id': cid, 'state': 'ready'}

    req_states = [state(x) for x in required]
    opt_states = [state(x) for x in optional]
    blockers = [x for x in req_states if x['state'] != 'ready']
    return {
        'status': 'ready' if not blockers else 'fallback_required', 'aco_version': VERSION,
        'required': req_states, 'optional': opt_states, 'blockers': blockers,
        'fallback': request.get('fallback', 'Produce a draft/plan/file without claiming the unavailable external action.'),
        'policy': 'Registry presence is not capability. Availability, authorization and verification are separate states; this command never executes a tool.'
    }


def score_simulation(path: Path | None = None) -> dict[str, Any]:
    path = (path or ROOT / 'release/behavioral-simulation.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported simulation score schema')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Simulation score file needs cases')
    dimensions = data.get('dimensions', [])
    if not isinstance(dimensions, list) or not dimensions:
        raise ACOError('Simulation score file needs dimensions')
    critical_failures = 0
    totals = []
    rows = []
    for case in cases:
        scores = case.get('scores')
        if not isinstance(scores, dict):
            raise ACOError(f"{case.get('id')}: scores must be an object")
        missing = [d for d in dimensions if d not in scores]
        if missing:
            raise ACOError(f"{case.get('id')}: missing scores {missing}")
        values = []
        for dim in dimensions:
            val = scores[dim]
            if not isinstance(val, (int, float)) or val < 0 or val > 5:
                raise ACOError(f"{case.get('id')}: {dim} must be 0..5")
            values.append(float(val))
        case_score = sum(values) / (5 * len(values)) * 100
        critical = bool(case.get('critical_failure', False))
        critical_failures += int(critical)
        totals.append(case_score)
        rows.append({'id': case.get('id'), 'score': round(case_score, 2), 'critical_failure': critical, 'notes': case.get('notes', '')})
    overall = sum(totals) / len(totals)
    gate = data.get('gate', {'minimum_score': 90, 'maximum_critical_failures': 0})
    passed = overall >= float(gate.get('minimum_score', 90)) and critical_failures <= int(gate.get('maximum_critical_failures', 0))
    return {
        'status': 'passed' if passed else 'failed', 'aco_version': VERSION, 'path': str(path),
        'review_mode': data.get('review_mode'), 'cases': len(cases), 'score': round(overall, 2),
        'critical_failures': critical_failures, 'gate': gate, 'rows': rows,
        'limitations': data.get('limitations', [])
    }
