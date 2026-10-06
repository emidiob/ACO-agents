"""ACO 0.9 adaptive feedback and shadow-learning primitives.

Pure, deterministic functions only. This module never captures hidden reasoning,
reads external accounts, changes production policy, or promotes a candidate by itself.
Feedback is scope-bound structured evidence. Adaptations are shadow-only until an
explicit, benchmarked promotion review succeeds outside this module.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, digest, read_json
from .goals import goal_graph_status, goal_graph_check


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _policy(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    data = read_json(root / 'config/adaptive-policy.json')
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported adaptive policy schema')
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Adaptive policy version mismatch')
    return data


def _canonical_hash(value: Any) -> str:
    payload = (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8')
    return digest(payload)


def _candidate_hash(candidate: dict[str, Any]) -> str:
    payload = deepcopy(candidate)
    payload.pop('candidate_sha256', None)
    return _canonical_hash(payload)


def _find_forbidden(value: Any, forbidden: set[str], path: str = '$') -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace('-', '_').replace(' ', '_')
            if normalized in forbidden:
                found.append(path + '.' + str(key))
            found.extend(_find_forbidden(child, forbidden, path + '.' + str(key)))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found.extend(_find_forbidden(child, forbidden, f'{path}[{i}]'))
    return found


def feedback_record_check(record: dict[str, Any], *, expected_scope: str | None = None,
                          root: Path | None = None) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ACOError('Feedback record must be an object')
    policy = _policy(root)
    errors: list[str] = []
    if record.get('schema_version') != 1:
        errors.append('feedback.schema_version must be 1')
    for field in ('feedback_id', 'scope_id', 'target_type', 'target_id', 'signal', 'source_ref'):
        if not _text(record.get(field)):
            errors.append(f'feedback.{field} is required')
    if expected_scope is not None and record.get('scope_id') != expected_scope:
        errors.append('feedback.scope_id must equal ledger scope')
    if record.get('target_type') not in set(policy.get('feedback', {}).get('target_types', [])):
        errors.append('unsupported feedback.target_type')
    if record.get('signal') not in set(policy.get('feedback', {}).get('signals', [])):
        errors.append('unsupported feedback.signal')
    weight = record.get('weight', 1)
    max_weight = int(policy.get('feedback', {}).get('maximum_weight', 5))
    if not isinstance(weight, int) or isinstance(weight, bool) or not 1 <= weight <= max_weight:
        errors.append(f'feedback.weight must be an integer 1..{max_weight}')

    forbidden = {str(x).lower().replace('-', '_').replace(' ', '_')
                 for x in policy.get('forbidden_reasoning_fields', [])}
    for location in _find_forbidden(record, forbidden):
        errors.append('hidden/private reasoning field is forbidden: ' + location)

    target_type = record.get('target_type')
    if target_type == 'output_preference':
        pref = record.get('preference')
        if not isinstance(pref, dict) or not _text(pref.get('key')) or not _text(pref.get('value')):
            errors.append('output_preference feedback requires preference.key and preference.value')
    if target_type == 'goal_ranking':
        ranking = record.get('ranking')
        directions = set(policy.get('ranking', {}).get('directions', []))
        if not isinstance(ranking, dict) or not _text(ranking.get('feature')) or ranking.get('direction') not in directions:
            errors.append('goal_ranking feedback requires ranking.feature and a supported ranking.direction')
    if str(record.get('signal', '')).startswith('outcome_') and not _text(record.get('evidence_ref')):
        errors.append('outcome feedback requires evidence_ref')

    return {
        'status': 'valid' if not errors else 'invalid',
        'aco_version': VERSION,
        'feedback_id': record.get('feedback_id'),
        'scope_id': record.get('scope_id'),
        'errors': errors,
        'policy': 'Feedback is structured evidence only. It cannot directly change routing, permissions, privacy boundaries or production scoring.'
    }


def feedback_ledger_check(ledger: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(ledger, dict):
        raise ACOError('Feedback ledger must be an object')
    errors: list[str] = []
    if ledger.get('schema_version') != 1:
        errors.append('ledger.schema_version must be 1')
    if not _text(ledger.get('ledger_id')):
        errors.append('ledger.ledger_id is required')
    if not _text(ledger.get('scope_id')):
        errors.append('ledger.scope_id is required')
    records = ledger.get('records')
    if not isinstance(records, list):
        errors.append('ledger.records must be a list')
        records = []

    seen: set[str] = set()
    previous_hash: str | None = None
    for pos, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f'records[{pos}] must be an object')
            continue
        check = feedback_record_check(record, expected_scope=ledger.get('scope_id'), root=root)
        errors.extend(f'records[{pos}]: {x}' for x in check['errors'])
        feedback_id = record.get('feedback_id')
        if feedback_id in seen:
            errors.append(f'duplicate feedback_id: {feedback_id}')
        if _text(feedback_id):
            seen.add(feedback_id)
        if record.get('previous_sha256') != previous_hash:
            errors.append(f'records[{pos}]: previous_sha256 does not match ledger chain')
        claimed = record.get('record_sha256')
        payload = deepcopy(record)
        payload.pop('record_sha256', None)
        actual = _canonical_hash(payload)
        if claimed != actual:
            errors.append(f'records[{pos}]: record_sha256 mismatch')
        previous_hash = actual

    computed_ledger_hash = _canonical_hash({'ledger_id': ledger.get('ledger_id'),
                                            'scope_id': ledger.get('scope_id'),
                                            'record_hashes': [r.get('record_sha256') for r in records if isinstance(r, dict)]})
    if ledger.get('ledger_sha256') is not None and ledger.get('ledger_sha256') != computed_ledger_hash:
        errors.append('ledger_sha256 mismatch')
    return {
        'status': 'valid' if not errors else 'invalid',
        'aco_version': VERSION,
        'ledger_id': ledger.get('ledger_id'),
        'scope_id': ledger.get('scope_id'),
        'records': len(records),
        'ledger_sha256': computed_ledger_hash,
        'errors': errors,
        'policy': 'The ledger is a scope-bound hash chain. Editing, deleting or reordering prior feedback invalidates the chain.'
    }


def feedback_append(ledger: dict[str, Any], record: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(ledger, dict):
        raise ACOError('Feedback ledger must be an object')
    base = deepcopy(ledger)
    if base.get('schema_version') != 1 or not _text(base.get('ledger_id')) or not _text(base.get('scope_id')):
        raise ACOError('Ledger requires schema_version=1, ledger_id and scope_id')
    if not isinstance(base.get('records'), list):
        raise ACOError('ledger.records must be a list')
    existing = feedback_ledger_check(base, root)
    if base['records'] and existing['status'] != 'valid':
        raise ACOError('Cannot append to an invalid feedback ledger: ' + '; '.join(existing['errors']))
    clean = deepcopy(record)
    clean.pop('record_sha256', None)
    clean['previous_sha256'] = base['records'][-1].get('record_sha256') if base['records'] else None
    check = feedback_record_check(clean, expected_scope=base['scope_id'], root=root)
    if check['status'] != 'valid':
        raise ACOError('Invalid feedback record: ' + '; '.join(check['errors']))
    if clean.get('feedback_id') in {r.get('feedback_id') for r in base['records'] if isinstance(r, dict)}:
        raise ACOError('Duplicate feedback_id')
    clean['record_sha256'] = _canonical_hash(clean)
    base['records'].append(clean)
    check2 = feedback_ledger_check(base, root)
    base['ledger_sha256'] = check2['ledger_sha256']
    return {
        'status': 'feedback_appended',
        'aco_version': VERSION,
        'ledger': base,
        'record_sha256': clean['record_sha256'],
        'ledger_sha256': base['ledger_sha256'],
        'policy': 'Append returns an updated ledger value only. Persistence is a separate scoped host responsibility.'
    }


def _validated_candidate(candidate: dict[str, Any], scope_id: str, policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(candidate, dict):
        return ['candidate must be an object']
    if candidate.get('schema_version') != 1:
        errors.append('candidate.schema_version must be 1')
    if candidate.get('state') != 'shadow_only':
        errors.append('candidate.state must be shadow_only')
    if candidate.get('scope_id') != scope_id:
        errors.append('candidate.scope_id must equal evaluation scope')
    if candidate.get('candidate_type') not in {'preference_rule', 'ranking_feature_delta'}:
        errors.append('unsupported candidate_type')
    if not _text(candidate.get('baseline_ref')) or not _text(candidate.get('rollback_ref')):
        errors.append('candidate requires baseline_ref and rollback_ref')
    claimed = candidate.get('candidate_sha256')
    if not _text(claimed) or claimed != _candidate_hash(candidate):
        errors.append('candidate_sha256 mismatch')
    if candidate.get('candidate_type') == 'ranking_feature_delta':
        delta = candidate.get('delta')
        bound = int(policy.get('ranking', {}).get('maximum_absolute_delta', 5))
        if not isinstance(delta, int) or isinstance(delta, bool) or delta == 0 or abs(delta) > bound:
            errors.append(f'ranking delta must be a non-zero integer within ±{bound}')
        if not _text(candidate.get('feature')):
            errors.append('ranking candidate requires feature')
    return errors


def adaptation_propose(payload: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get('ledger'), dict):
        raise ACOError('Adaptation proposal requires ledger')
    policy = _policy(root)
    ledger = payload['ledger']
    check = feedback_ledger_check(ledger, root)
    if check['status'] != 'valid':
        raise ACOError('Invalid feedback ledger: ' + '; '.join(check['errors']))
    minimum_support = int(policy.get('proposal', {}).get('minimum_support', 3))
    minimum_consensus = float(policy.get('proposal', {}).get('minimum_consensus', 0.67))
    baseline_ref = payload.get('baseline_ref', 'production-baseline')
    rollback_ref = payload.get('rollback_ref', 'rollback:production-baseline')
    if not _text(baseline_ref) or not _text(rollback_ref):
        raise ACOError('baseline_ref and rollback_ref must be non-empty strings')

    candidates: list[dict[str, Any]] = []
    records = ledger.get('records', [])

    # Scoped output preferences: repeated records/sources only. A large weight on one
    # record must never satisfy the minimum-evidence threshold by itself.
    preference_groups: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for r in records:
        if r.get('target_type') != 'output_preference':
            continue
        pref = r.get('preference', {})
        key, value = pref.get('key'), pref.get('value')
        target_id = r.get('target_id')
        if not (_text(key) and _text(value) and _text(target_id)):
            continue
        group = preference_groups.setdefault((target_id, key), {})
        bucket = group.setdefault(value, {'count': 0, 'ids': [], 'sources': set()})
        bucket['count'] += 1
        bucket['ids'].append(r.get('feedback_id'))
        if _text(r.get('source_ref')):
            bucket['sources'].add(r.get('source_ref'))
    minimum_sources = int(policy.get('proposal', {}).get('minimum_distinct_sources', 2))
    for target_id, key in sorted(preference_groups):
        values = preference_groups[(target_id, key)]
        total = sum(v['count'] for v in values.values())
        winner_value, winner = sorted(values.items(), key=lambda item: (-item[1]['count'], item[0]))[0]
        consensus = 0.0 if total == 0 else winner['count'] / total
        if (total >= minimum_support and winner['count'] >= minimum_support
                and len(winner['sources']) >= minimum_sources and consensus >= minimum_consensus):
            candidate = {
                'schema_version': 1, 'candidate_type': 'preference_rule', 'state': 'shadow_only',
                'scope_id': ledger['scope_id'], 'target_type': 'output_preference',
                'target_id': target_id, 'key': key, 'value': winner_value, 'support': winner['count'],
                'observations': total, 'distinct_sources': len(winner['sources']),
                'consensus': round(consensus, 4),
                'source_feedback_ids': sorted(x for x in winner['ids'] if _text(x)),
                'baseline_ref': baseline_ref, 'rollback_ref': rollback_ref,
            }
            candidate['candidate_sha256'] = _candidate_hash(candidate)
            candidates.append(candidate)

    # Goal ranking: each feedback record is one vote. Weight metadata cannot turn
    # a single observation into a learned ranking change. The resulting delta is bounded.
    ranking_groups: dict[tuple[str, str], dict[str, Any]] = {}
    for r in records:
        if r.get('target_type') != 'goal_ranking':
            continue
        ranking = r.get('ranking', {})
        feature, direction = ranking.get('feature'), ranking.get('direction')
        target_id = r.get('target_id')
        if not (_text(feature) and _text(target_id) and direction in {'prefer', 'avoid'}):
            continue
        bucket = ranking_groups.setdefault((target_id, feature), {'prefer': 0, 'avoid': 0, 'ids': [], 'sources': {'prefer': set(), 'avoid': set()}})
        bucket[direction] += 1
        bucket['ids'].append(r.get('feedback_id'))
        if _text(r.get('source_ref')):
            bucket['sources'][direction].add(r.get('source_ref'))
    max_delta = int(policy.get('ranking', {}).get('maximum_absolute_delta', 5))
    for target_id, feature in sorted(ranking_groups):
        bucket = ranking_groups[(target_id, feature)]
        total = bucket['prefer'] + bucket['avoid']
        direction = 'prefer' if bucket['prefer'] >= bucket['avoid'] else 'avoid'
        support = bucket[direction]
        consensus = 0.0 if total == 0 else support / total
        net = bucket['prefer'] - bucket['avoid']
        delta = max(-max_delta, min(max_delta, net))
        if (total >= minimum_support and support >= minimum_support
                and len(bucket['sources'][direction]) >= minimum_sources
                and consensus >= minimum_consensus and delta != 0):
            candidate = {
                'schema_version': 1, 'candidate_type': 'ranking_feature_delta', 'state': 'shadow_only',
                'scope_id': ledger['scope_id'], 'target_type': 'goal_ranking',
                'target_id': target_id, 'feature': feature, 'delta': delta, 'support': support,
                'observations': total, 'distinct_sources': len(bucket['sources'][direction]),
                'consensus': round(consensus, 4),
                'source_feedback_ids': sorted(x for x in bucket['ids'] if _text(x)),
                'baseline_ref': baseline_ref, 'rollback_ref': rollback_ref,
            }
            candidate['candidate_sha256'] = _candidate_hash(candidate)
            candidates.append(candidate)

    candidates.sort(key=lambda c: (c['candidate_type'], c.get('feature', ''), c.get('key', ''), c['candidate_sha256']))
    return {
        'status': 'proposals_ready' if candidates else 'no_supported_adaptations',
        'aco_version': VERSION,
        'scope_id': ledger.get('scope_id'),
        'candidate_count': len(candidates),
        'candidates': candidates,
        'policy': 'Candidates are shadow-only evidence summaries. They do not change production behavior or permissions.'
    }


def shadow_rank(payload: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get('graph'), dict):
        raise ACOError('Shadow ranking requires graph')
    policy = _policy(root)
    graph = payload['graph']
    check = goal_graph_check(graph, root)
    if check['status'] != 'valid':
        raise ACOError('Invalid goal graph: ' + '; '.join(check['errors']))
    candidates = payload.get('candidates', [])
    if not isinstance(candidates, list):
        raise ACOError('candidates must be a list')
    scope_id = graph.get('scope_id')
    for candidate in candidates:
        errors = _validated_candidate(candidate, scope_id, policy)
        if errors:
            raise ACOError('Invalid adaptive candidate: ' + '; '.join(errors))
    limit = payload.get('limit', 5)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 50:
        raise ACOError('limit must be an integer 1..50')
    base = goal_graph_status(graph, as_of=payload.get('as_of'), limit=50, root=root)
    nodes = {n['id']: n for n in graph.get('nodes', []) if isinstance(n, dict)}
    ranking_candidates = [c for c in candidates if c.get('candidate_type') == 'ranking_feature_delta']
    eligible_states = {'ready', 'in_progress', 'awaiting_approval', 'verification_required'}
    rows: list[dict[str, Any]] = []
    for row in base['task_states']:
        node = nodes.get(row['id'], {})
        features = node.get('adaptive_features', [])
        if features is None:
            features = []
        if not isinstance(features, list) or any(not _text(x) for x in features):
            raise ACOError(f'{row["id"]}: adaptive_features must be a string list')
        applied = [c for c in ranking_candidates
                   if c.get('feature') in features
                   and c.get('target_id') in {'next-best-action', graph.get('graph_id')}]
        delta = sum(int(c.get('delta', 0)) for c in applied)
        shadow = deepcopy(row)
        shadow['adaptive_features'] = list(features)
        shadow['adaptive_delta'] = delta
        shadow['shadow_score'] = row['score'] + delta
        shadow['candidate_sha256s'] = [c['candidate_sha256'] for c in applied]
        rows.append(shadow)
    eligible = [r for r in rows if r['computed_state'] in eligible_states]
    eligible.sort(key=lambda r: (-r['shadow_score'], r['id']))
    base_ids = base['next_task_ids'][:limit]
    shadow_ids = [r['id'] for r in eligible[:limit]]
    return {
        'status': 'shadow_comparison',
        'aco_version': VERSION,
        'graph_id': graph.get('graph_id'),
        'scope_id': scope_id,
        'base_next_task_ids': base_ids,
        'shadow_next_task_ids': shadow_ids,
        'ranking_changed': base_ids != shadow_ids,
        'shadow_tasks': eligible[:limit],
        'production_mutated': False,
        'candidate_count': len(candidates),
        'policy': 'Shadow ranking compares candidates against the deterministic production score. It never mutates the graph or activates a candidate.'
    }


def promotion_check(payload: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ACOError('Promotion review must be an object')
    policy = _policy(root)
    candidate = payload.get('candidate')
    benchmark = payload.get('benchmark')
    approval = payload.get('approval')
    if not isinstance(candidate, dict) or not isinstance(benchmark, dict) or not isinstance(approval, dict):
        raise ACOError('Promotion review requires candidate, benchmark and approval objects')
    scope_id = candidate.get('scope_id')
    blockers = _validated_candidate(candidate, scope_id, policy)
    expected_hash = candidate.get('candidate_sha256')
    if benchmark.get('candidate_sha256') != expected_hash:
        blockers.append('benchmark candidate_sha256 mismatch')
    if approval.get('candidate_sha256') != expected_hash:
        blockers.append('approval candidate_sha256 mismatch')
    if approval.get('approved') is not True or not _text(approval.get('approval_ref')):
        blockers.append('explicit approved approval_ref is required')
    gate = policy.get('promotion', {})
    cases = benchmark.get('cases')
    score = benchmark.get('score')
    critical = benchmark.get('critical_failures')
    if not isinstance(cases, int) or isinstance(cases, bool) or cases < int(gate.get('minimum_benchmark_cases', 20)):
        blockers.append('benchmark case count below promotion minimum')
    if not isinstance(score, (int, float)) or isinstance(score, bool) or float(score) < float(gate.get('minimum_score', 95.0)):
        blockers.append('benchmark score below promotion minimum')
    if critical != int(gate.get('maximum_critical_failures', 0)):
        blockers.append('benchmark critical failures exceed promotion maximum')
    if benchmark.get('historical_regressions_passed') is not True:
        blockers.append('historical regressions must pass')
    if benchmark.get('frozen_before_first_run') is not True:
        blockers.append('benchmark must be frozen before first run')
    if benchmark.get('scope_id') != scope_id:
        blockers.append('benchmark scope_id mismatch')
    return {
        'status': 'eligible_for_promotion' if not blockers else 'promotion_blocked',
        'aco_version': VERSION,
        'candidate_sha256': expected_hash,
        'scope_id': scope_id,
        'eligible': not blockers,
        'blockers': blockers,
        'rollback_ref': candidate.get('rollback_ref'),
        'execute': False,
        'policy': 'Eligibility is not activation. Promotion requires a separate deliberate versioned policy change and a new release validation.'
    }


def _get_path(value: dict[str, Any], dotted: str) -> Any:
    cursor: Any = value
    for part in dotted.split('.'):
        if isinstance(cursor, dict) and part in cursor:
            cursor = cursor[part]
        else:
            return None
    return cursor


def adaptive_benchmark(path: Path | None = None, root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    path = (path or root / 'config/adaptive-benchmark.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported adaptive benchmark schema')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Adaptive benchmark needs cases')
    rows: list[dict[str, Any]] = []
    critical_failures = 0
    for case in cases:
        op = case.get('operation')
        expected_error = bool(case.get('expected_error', False))
        try:
            if op == 'feedback_check':
                result = feedback_record_check(case.get('input', {}), root=root)
            elif op == 'ledger_check':
                result = feedback_ledger_check(case.get('input', {}), root=root)
            elif op == 'adaptation_propose':
                result = adaptation_propose(case.get('input', {}), root=root)
            elif op == 'shadow_rank':
                result = shadow_rank(case.get('input', {}), root=root)
            elif op == 'promotion_check':
                result = promotion_check(case.get('input', {}), root=root)
            else:
                raise ACOError('Unsupported adaptive benchmark operation: ' + str(op))
            passed = not expected_error
            for key, expected in case.get('expected', {}).items():
                if _get_path(result, key) != expected:
                    passed = False
            error = None
        except ACOError as exc:
            passed = expected_error
            result = None
            error = str(exc)
        critical = bool(case.get('critical', False))
        if critical and not passed:
            critical_failures += 1
        rows.append({'id': case.get('id'), 'operation': op, 'passed': passed,
                     'critical': critical, 'error': error})
    passed_count = sum(1 for r in rows if r['passed'])
    score = round(100.0 * passed_count / len(rows), 2)
    gate = data.get('gate', {})
    status = 'passed' if (critical_failures <= int(gate.get('maximum_critical_failures', 0))
                          and score >= float(gate.get('minimum_score', 100.0))) else 'failed'
    return {
        'status': status,
        'aco_version': VERSION,
        'cases': len(rows),
        'passed': passed_count,
        'score': score,
        'critical_failures': critical_failures,
        'rows': rows,
        'policy': 'This benchmark is deterministic and local. It does not prove external model learning quality or execute any provider action.'
    }
