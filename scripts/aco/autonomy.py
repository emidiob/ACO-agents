"""ACO 0.8 autonomous decision/execution planner.

The engine selects the next graph task, resolves each host action against existing
capability/permission contracts, and reasons about receipts/recovery. It never
calls an external adapter itself. A host may execute returned host_action packets
only under its own real authorization and connector rules.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json
from .execution import action_hash, execution_plan, permission_check, receipt_check
from .goals import goal_graph_check, goal_graph_status

SUCCESS_DEFAULT = {
    'executed', 'accepted', 'queued', 'created', 'updated', 'deleted', 'sent',
    'delivered', 'read', 'scheduled', 'published', 'submitted', 'deployed',
    'purchased', 'signed'
}
UNCERTAIN_STATES = {'unknown', 'executing'}
FAIL_STATES = {'failed', 'cancelled'}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _policy(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    data = read_json(root / 'config/autonomy-policy.json')
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported autonomy policy schema')
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Autonomy policy version mismatch')
    return data


def _node(graph: dict[str, Any], node_id: str) -> dict[str, Any]:
    for node in graph.get('nodes', []):
        if node.get('id') == node_id:
            return node
    raise ACOError(f'Unknown task node: {node_id}')


def _action_request(scope_id: str, action: dict[str, Any]) -> dict[str, Any]:
    for key in ('id', 'capability_id', 'operation'):
        if not _text(action.get(key)):
            raise ACOError(f'action.{key} is required')
    target = action.get('target')
    if target is not None and not isinstance(target, (str, dict)):
        raise ACOError(f'{action["id"]}: target must be a string, object or null')
    parameters = action.get('parameters', {})
    if not isinstance(parameters, dict):
        raise ACOError(f'{action["id"]}: parameters must be an object')
    request = {
        'scope_id': scope_id,
        'capability_id': action['capability_id'],
        'operation': action['operation'],
        'target': target,
        'payload_ref': action.get('payload_ref'),
        'parameters': parameters,
    }
    return request


def _check_action_graph(task: dict[str, Any]) -> None:
    actions = task.get('actions', []) or []
    if not isinstance(actions, list):
        raise ACOError(f'{task["id"]}: actions must be a list')
    index: dict[str, dict[str, Any]] = {}
    for raw in actions:
        if not isinstance(raw, dict):
            raise ACOError(f'{task["id"]}: each action must be an object')
        aid = raw.get('id')
        if not _text(aid):
            raise ACOError(f'{task["id"]}: action.id is required')
        if aid in index:
            raise ACOError(f'{task["id"]}: duplicate action id {aid}')
        index[aid] = raw
        _action_request('scope-placeholder', raw)
        deps = raw.get('depends_on', [])
        if not isinstance(deps, list) or any(not _text(x) for x in deps):
            raise ACOError(f'{aid}: depends_on must be a string list')
    for aid, action in index.items():
        for dep in action.get('depends_on', []):
            if dep == aid:
                raise ACOError(f'{aid}: action cannot depend on itself')
            if dep not in index:
                raise ACOError(f'{aid}: unknown action dependency {dep}')
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(aid: str) -> None:
        if aid in visited:
            return
        if aid in visiting:
            raise ACOError(f'{task["id"]}: action dependency cycle includes {aid}')
        visiting.add(aid)
        for dep in index[aid].get('depends_on', []):
            visit(dep)
        visiting.remove(aid)
        visited.add(aid)
    for aid in index:
        visit(aid)


def _approval_for(action_sha: str, approvals: list[dict[str, Any]]) -> dict[str, Any] | None:
    exact = [a for a in approvals if isinstance(a, dict) and a.get('action_sha256') == action_sha]
    return exact[-1] if exact else None


def _receipts_for(action_sha: str, receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in receipts if isinstance(r, dict) and r.get('action_sha256') == action_sha]


def _verification(action: dict[str, Any], receipt: dict[str, Any]) -> tuple[bool, str]:
    spec = action.get('verification', {})
    if spec is None:
        spec = {}
    if not isinstance(spec, dict):
        raise ACOError(f'{action["id"]}: verification must be an object')
    states = spec.get('success_states', sorted(SUCCESS_DEFAULT))
    if not isinstance(states, list) or any(not _text(x) for x in states):
        raise ACOError(f'{action["id"]}: verification.success_states must be a string list')
    if receipt.get('status') not in set(states):
        return False, 'receipt_state_not_sufficient'
    if spec.get('require_evidence', True):
        evidence = receipt.get('evidence', [])
        if not isinstance(evidence, list) or not any(_text(x) for x in evidence):
            return False, 'verification_evidence_missing'
    return True, 'receipt_satisfies_verification'


def _retry_decision(action: dict[str, Any], matching_receipts: list[dict[str, Any]],
                    policy: dict[str, Any]) -> dict[str, Any]:
    retry = action.get('retry_policy', {}) or {}
    if not isinstance(retry, dict):
        raise ACOError(f'{action["id"]}: retry_policy must be an object')
    max_attempts = retry.get('max_attempts', policy.get('default_retry', {}).get('max_attempts', 1))
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or not 0 <= max_attempts <= 5:
        raise ACOError(f'{action["id"]}: retry max_attempts must be 0..5')
    retry_on = retry.get('retry_on', policy.get('default_retry', {}).get('retry_on', ['failed']))
    if not isinstance(retry_on, list) or any(not _text(x) for x in retry_on):
        raise ACOError(f'{action["id"]}: retry_on must be a string list')
    attempts = len(matching_receipts)
    last = matching_receipts[-1] if matching_receipts else None
    if not last or last.get('status') not in retry_on:
        return {'allowed': False, 'attempts': attempts, 'max_attempts': max_attempts, 'reason': 'state_not_retryable'}
    if attempts >= max_attempts + 1:  # first attempt + N retries
        return {'allowed': False, 'attempts': attempts, 'max_attempts': max_attempts, 'reason': 'retry_budget_exhausted'}
    requires_key = bool(retry.get('requires_idempotency_key', policy.get('default_retry', {}).get('requires_idempotency_key', True)))
    if requires_key and not _text(action.get('idempotency_key')):
        return {'allowed': False, 'attempts': attempts, 'max_attempts': max_attempts, 'reason': 'idempotency_key_required'}
    return {'allowed': True, 'attempts': attempts, 'max_attempts': max_attempts, 'reason': 'bounded_retry_allowed'}


def _action_row(scope_id: str, action: dict[str, Any], *, inventory: dict[str, Any] | None,
                approvals: list[dict[str, Any]], receipts: list[dict[str, Any]],
                completed_action_ids: set[str], mode: str, root: Path | None,
                policy: dict[str, Any]) -> dict[str, Any]:
    request = _action_request(scope_id, action)
    sha = action_hash(request)
    dependencies = action.get('depends_on', [])
    unmet = [d for d in dependencies if d not in completed_action_ids]
    base = {
        'id': action['id'], 'action_sha256': sha, 'capability_id': request['capability_id'],
        'operation': request['operation'], 'depends_on': dependencies,
    }
    if unmet:
        return {**base, 'status': 'blocked_by_action_dependency', 'completed': False,
                'blockers': unmet, 'decision_class': 'dependency_gate'}

    matches = _receipts_for(sha, receipts)
    if matches:
        last = matches[-1]
        checked = receipt_check(last, root=root)
        if checked['status'] != 'valid':
            return {**base, 'status': 'invalid_receipt', 'completed': False,
                    'receipt_id': last.get('receipt_id'), 'errors': checked['errors'],
                    'decision_class': 'verification_gate'}
        state = last.get('status')
        if state in UNCERTAIN_STATES:
            return {**base, 'status': 'reconcile_required', 'completed': False,
                    'receipt_id': last.get('receipt_id'),
                    'reason': 'Uncertain/in-flight outcome must be reconciled before any retry.',
                    'decision_class': 'reconciliation_gate'}
        if state in FAIL_STATES:
            retry = _retry_decision(action, matches, policy)
            if not retry['allowed']:
                return {**base, 'status': 'manual_recovery', 'completed': False,
                        'receipt_id': last.get('receipt_id'), 'recovery': retry,
                        'decision_class': 'recovery_gate'}
            approval = _approval_for(sha, approvals)
            plan = execution_plan(request, inventory, approval, None, root)
            if plan['status'] != 'ready_to_execute':
                return {**base, 'status': 'fallback_required' if plan['status'] == 'fallback_required' else plan['status'],
                        'completed': False, 'recovery': retry, 'execution': plan,
                        'decision_class': 'recovery_gate'}
            status = 'simulation_retry_ready' if mode == 'SIMULATE' else 'retry_host_action_required'
            return {**base, 'status': status, 'completed': False, 'recovery': retry,
                    'execution': plan, 'host_action': request if mode == 'HOST_EXECUTION' else None,
                    'decision_class': 'bounded_retry'}
        verified, reason = _verification(action, last)
        if verified:
            return {**base, 'status': 'verified', 'completed': True,
                    'receipt_id': last.get('receipt_id'), 'verification_reason': reason,
                    'decision_class': 'verified_evidence'}
        return {**base, 'status': 'verification_required', 'completed': False,
                'receipt_id': last.get('receipt_id'), 'verification_reason': reason,
                'decision_class': 'verification_gate'}

    # No prior outcome: resolve permission/capability and decide if the host may act.
    pre_permission = permission_check(request, None, root)
    approval = _approval_for(sha, approvals)
    plan = execution_plan(request, inventory, approval, None, root)
    decision_class = 'human_approval' if pre_permission.get('approval_required') else 'autonomous_in_scope'
    if plan['status'] != 'ready_to_execute':
        if plan.get('permission', {}).get('approval_required') and not plan.get('permission', {}).get('allowed'):
            status = 'approval_required'
        else:
            status = 'fallback_required'
        return {**base, 'status': status, 'completed': False, 'execution': plan,
                'decision_class': decision_class}
    if mode == 'SIMULATE':
        return {**base, 'status': 'simulation_ready', 'completed': False,
                'execution': plan, 'decision_class': decision_class,
                'would_request_host_action': request}
    return {**base, 'status': 'host_action_required', 'completed': False,
            'execution': plan, 'decision_class': decision_class,
            'host_action': request}


def autonomy_plan(packet: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise ACOError('Autonomy packet must be an object')
    graph = packet.get('graph')
    if not isinstance(graph, dict):
        raise ACOError('packet.graph is required')
    check = goal_graph_check(graph, root)
    if check['status'] != 'valid':
        raise ACOError('Invalid goal graph: ' + '; '.join(check['errors']))
    mode = packet.get('mode', 'SIMULATE')
    if mode not in {'SIMULATE', 'HOST_EXECUTION'}:
        raise ACOError('mode must be SIMULATE or HOST_EXECUTION')
    approvals = packet.get('approvals', [])
    receipts = packet.get('receipts', [])
    if not isinstance(approvals, list) or any(not isinstance(x, dict) for x in approvals):
        raise ACOError('approvals must be a list of objects')
    if not isinstance(receipts, list) or any(not isinstance(x, dict) for x in receipts):
        raise ACOError('receipts must be a list of objects')
    inventory = packet.get('inventory')
    if inventory is not None and not isinstance(inventory, dict):
        raise ACOError('inventory must be an object')
    max_tasks = packet.get('max_tasks', 1)
    if not isinstance(max_tasks, int) or isinstance(max_tasks, bool) or not 1 <= max_tasks <= 5:
        raise ACOError('max_tasks must be an integer 1..5')
    status = goal_graph_status(graph, as_of=packet.get('as_of'), limit=max_tasks, root=root)
    selected_ids = status['next_task_ids']
    if not selected_ids:
        return {
            'status': 'no_actionable_tasks', 'aco_version': VERSION, 'mode': mode,
            'graph_id': graph.get('graph_id'), 'scope_id': graph.get('scope_id'),
            'selected_task_ids': [], 'tasks': [], 'host_actions': [], 'host_action_count': 0,
            'execute': False,
            'policy': 'No task is currently actionable. The engine does not manufacture work or bypass dependencies.'
        }

    policy = _policy(root)
    task_rows: list[dict[str, Any]] = []
    host_actions: list[dict[str, Any]] = []
    all_action_statuses: list[str] = []
    for task_id in selected_ids:
        task = _node(graph, task_id)
        _check_action_graph(task)
        actions = task.get('actions', []) or []
        if not actions:
            task_rows.append({
                'task_id': task_id, 'status': 'delegated_work_required', 'actions': [],
                'role_hint': task.get('role_hint'), 'deliverable': task.get('deliverable'),
                'reason': 'This task is model/professional work, not a host capability action.'
            })
            all_action_statuses.append('delegated_work_required')
            continue
        completed_ids: set[str] = set()
        rows: list[dict[str, Any]] = []
        # Iterate in declared order; dependency rows only become eligible after verified evidence.
        for action in actions:
            row = _action_row(graph['scope_id'], action, inventory=inventory, approvals=approvals,
                              receipts=receipts, completed_action_ids=completed_ids, mode=mode,
                              root=root, policy=policy)
            rows.append(row)
            all_action_statuses.append(row['status'])
            if row.get('completed'):
                completed_ids.add(action['id'])
            if row.get('host_action'):
                host_actions.append({'task_id': task_id, 'action_id': action['id'], **row['host_action']})
        if rows and all(r.get('completed') for r in rows):
            task_status = 'task_verified'
        elif any(r['status'] == 'reconcile_required' for r in rows):
            task_status = 'reconcile_required'
        elif any(r['status'] == 'invalid_receipt' for r in rows):
            task_status = 'invalid_receipt'
        elif any(r['status'] == 'manual_recovery' for r in rows):
            task_status = 'manual_recovery'
        elif any(r['status'] == 'approval_required' for r in rows):
            task_status = 'approval_required'
        elif any(r['status'] in {'host_action_required', 'retry_host_action_required'} for r in rows):
            task_status = 'host_action_required'
        elif any(r['status'] in {'simulation_ready', 'simulation_retry_ready'} for r in rows):
            task_status = 'simulation_ready'
        elif any(r['status'] == 'fallback_required' for r in rows):
            task_status = 'fallback_required'
        else:
            task_status = 'blocked'
        task_rows.append({'task_id': task_id, 'status': task_status, 'actions': rows})

    precedence = [
        ('reconcile_required', {'reconcile_required'}),
        ('invalid_receipt', {'invalid_receipt'}),
        ('manual_recovery', {'manual_recovery'}),
        ('verification_required', {'verification_required'}),
        ('approval_required', {'approval_required'}),
        ('host_action_required', {'host_action_required', 'retry_host_action_required'}),
        ('fallback_required', {'fallback_required'}),
        ('delegated_work_required', {'delegated_work_required'}),
        ('simulation_ready', {'simulation_ready', 'simulation_retry_ready'}),
    ]
    overall = 'task_verified' if task_rows and all(t['status'] == 'task_verified' for t in task_rows) else 'blocked'
    if overall != 'task_verified':
        for label, states in precedence:
            if any(s in states for s in all_action_statuses):
                overall = label
                break

    return {
        'status': overall,
        'aco_version': VERSION,
        'mode': mode,
        'graph_id': graph.get('graph_id'),
        'scope_id': graph.get('scope_id'),
        'selected_task_ids': selected_ids,
        'goal_status': status,
        'tasks': task_rows,
        'host_actions': host_actions,
        'host_action_count': len(host_actions),
        'execute': False,
        'policy': 'ACO chooses and prepares bounded work, but this local engine never calls a provider. Exact approvals, real host capability and receipt verification remain mandatory.'
    }


def autonomy_benchmark(path: Path | None = None, root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    path = (path or root / 'config/autonomy-benchmark.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported autonomy benchmark schema')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Autonomy benchmark needs cases')
    rows: list[dict[str, Any]] = []
    correct = 0
    critical = 0
    for case in cases:
        ok = False
        actual: Any = None
        error: str | None = None
        try:
            kind = case.get('kind', 'autonomy')
            if kind == 'goal_status':
                result = goal_graph_status(case['graph'], as_of=case.get('as_of'), limit=case.get('limit', 5), root=root)
                actual = {'status': result['status'], 'next_task_ids': result['next_task_ids'],
                          'blocked_task_ids': result['blocked_task_ids']}
                ok = result['status'] == case.get('expected_status')
                if 'expected_next_task_ids' in case:
                    ok = ok and result['next_task_ids'] == case['expected_next_task_ids']
                if 'expected_blocked_task_ids' in case:
                    ok = ok and sorted(result['blocked_task_ids']) == sorted(case['expected_blocked_task_ids'])
            elif kind == 'graph_check':
                result = goal_graph_check(case['graph'], root)
                actual = {'status': result['status'], 'errors': result['errors']}
                ok = result['status'] == case.get('expected_status')
                contains = case.get('error_contains')
                if contains:
                    ok = ok and any(contains in x for x in result['errors'])
            else:
                result = autonomy_plan(case['packet'], root)
                actual = {'status': result['status'], 'selected_task_ids': result['selected_task_ids'],
                          'host_action_count': result['host_action_count'],
                          'action_statuses': [a['status'] for t in result['tasks'] for a in t.get('actions', [])]}
                ok = result['status'] == case.get('expected_status')
                if 'expected_host_action_count' in case:
                    ok = ok and result['host_action_count'] == case['expected_host_action_count']
                if 'expected_action_statuses' in case:
                    statuses = [a['status'] for t in result['tasks'] for a in t.get('actions', [])]
                    ok = ok and statuses == case['expected_action_statuses']
        except ACOError as exc:
            error = str(exc)
            actual = {'error': error}
            ok = case.get('expected_status') == 'error' and (
                not case.get('error_contains') or case['error_contains'] in error
            )
        is_critical = bool(case.get('critical', True)) and not ok
        correct += int(ok)
        critical += int(is_critical)
        rows.append({'id': case.get('id'), 'passed': ok, 'critical_failure': is_critical,
                     'expected': case.get('expected_status'), 'actual': actual, 'error': error})
    score = correct / len(cases) * 100
    gate = data.get('gate', {'minimum_score': 100.0, 'maximum_critical_failures': 0})
    passed = score >= float(gate.get('minimum_score', 100.0)) and critical <= int(gate.get('maximum_critical_failures', 0))
    return {
        'status': 'passed' if passed else 'failed', 'aco_version': VERSION,
        'cases': len(cases), 'score': round(score, 2), 'critical_failures': critical,
        'gate': gate, 'rows': rows,
        'limitations': 'Deterministic graph/policy conformance only. No provider or external adapter is called by this benchmark.'
    }
