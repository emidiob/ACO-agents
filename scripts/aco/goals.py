"""ACO 0.8 goal graph primitives.

Pure, deterministic functions only. The graph models durable intent, not external
execution. Nothing in this module reads accounts, calls adapters, or persists a
user graph. Hosts may store the returned graph only under their normal scoped
memory/write rules.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _policy(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    data = read_json(root / 'config/goal-graph.json')
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported goal-graph policy schema')
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Goal-graph policy version mismatch')
    return data


def _parse_time(value: Any, label: str) -> datetime | None:
    if value is None:
        return None
    if not _text(value):
        raise ACOError(f'{label} must be an ISO date/time string')
    text = str(value).strip()
    try:
        if len(text) == 10:
            dt = datetime.fromisoformat(text + 'T23:59:59+00:00')
        else:
            dt = datetime.fromisoformat(text.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            raise ValueError('timezone required')
        return dt.astimezone(timezone.utc)
    except ValueError as exc:
        raise ACOError(f'{label} must be ISO-8601 with timezone, or YYYY-MM-DD') from exc


def _graph_index(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {n['id']: n for n in graph['nodes']}


def _detect_cycle(index: dict[str, dict[str, Any]], selector) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    trail: list[str] = []

    def visit(node_id: str) -> list[str] | None:
        if node_id in visited:
            return None
        if node_id in visiting:
            try:
                i = trail.index(node_id)
            except ValueError:
                i = 0
            return trail[i:] + [node_id]
        visiting.add(node_id)
        trail.append(node_id)
        for nxt in selector(index[node_id]):
            if nxt in index:
                cycle = visit(nxt)
                if cycle:
                    return cycle
        trail.pop()
        visiting.remove(node_id)
        visited.add(node_id)
        return None

    for node_id in index:
        cycle = visit(node_id)
        if cycle:
            return cycle
    return None


def goal_graph_check(graph: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    if not isinstance(graph, dict):
        raise ACOError('Goal graph must be an object')
    policy = _policy(root)
    errors: list[str] = []
    warnings: list[str] = []
    if graph.get('schema_version') != 1:
        errors.append('graph.schema_version must be 1')
    if not _text(graph.get('graph_id')):
        errors.append('graph.graph_id is required')
    if not _text(graph.get('scope_id')):
        errors.append('graph.scope_id is required')
    nodes = graph.get('nodes')
    if not isinstance(nodes, list) or not nodes:
        errors.append('graph.nodes must be a non-empty list')
        nodes = []

    kinds = set(policy.get('node_kinds', []))
    states = set(policy.get('states', []))
    parent_rules = {k: set(v) for k, v in policy.get('parent_kinds', {}).items()}
    seen: set[str] = set()
    index: dict[str, dict[str, Any]] = {}
    for pos, raw in enumerate(nodes):
        if not isinstance(raw, dict):
            errors.append(f'nodes[{pos}] must be an object')
            continue
        node_id = raw.get('id')
        if not _text(node_id):
            errors.append(f'nodes[{pos}].id is required')
            continue
        if node_id in seen:
            errors.append(f'duplicate node id: {node_id}')
            continue
        seen.add(node_id)
        index[node_id] = raw
        kind = raw.get('kind')
        state = raw.get('state')
        if kind not in kinds:
            errors.append(f'{node_id}: unsupported kind {kind}')
        if state not in states:
            errors.append(f'{node_id}: unsupported state {state}')
        if not _text(raw.get('title')):
            errors.append(f'{node_id}: title is required')
        if raw.get('scope_id') is not None and raw.get('scope_id') != graph.get('scope_id'):
            errors.append(f'{node_id}: node scope must equal graph scope')
        deps = raw.get('depends_on', [])
        if not isinstance(deps, list) or any(not _text(x) for x in deps):
            errors.append(f'{node_id}: depends_on must be a string list')
        if isinstance(deps, list) and len(deps) != len(set(deps)):
            errors.append(f'{node_id}: duplicate dependencies')
        priority = raw.get('priority', 50)
        if not isinstance(priority, int) or isinstance(priority, bool) or not 0 <= priority <= 100:
            errors.append(f'{node_id}: priority must be an integer 0..100')
        effort = raw.get('effort', 3)
        if not isinstance(effort, int) or isinstance(effort, bool) or not 1 <= effort <= 5:
            errors.append(f'{node_id}: effort must be an integer 1..5')
        criteria = raw.get('success_criteria', [])
        if not isinstance(criteria, list) or any(not _text(x) for x in criteria):
            errors.append(f'{node_id}: success_criteria must be a string list')
        if raw.get('due_at') is not None:
            try:
                _parse_time(raw.get('due_at'), f'{node_id}.due_at')
            except ACOError as exc:
                errors.append(str(exc))
        if kind != 'task' and raw.get('actions') not in (None, []):
            errors.append(f'{node_id}: only task nodes may declare actions')
        if kind == 'program' and raw.get('parent_id') is not None:
            errors.append(f'{node_id}: program nodes cannot have a parent')

    for node_id, node in index.items():
        parent_id = node.get('parent_id')
        if parent_id is not None:
            if not _text(parent_id) or parent_id not in index:
                errors.append(f'{node_id}: parent_id does not reference a graph node')
            else:
                allowed = parent_rules.get(node.get('kind'), set())
                if index[parent_id].get('kind') not in allowed:
                    errors.append(f'{node_id}: {node.get("kind")} cannot have parent kind {index[parent_id].get("kind")}')
        for dep in node.get('depends_on', []) if isinstance(node.get('depends_on', []), list) else []:
            if dep == node_id:
                errors.append(f'{node_id}: cannot depend on itself')
            elif dep not in index:
                errors.append(f'{node_id}: dependency {dep} is not in the graph')

    if index:
        parent_cycle = _detect_cycle(index, lambda n: [n['parent_id']] if n.get('parent_id') else [])
        if parent_cycle:
            errors.append('parent cycle: ' + ' -> '.join(parent_cycle))
        dependency_cycle = _detect_cycle(index, lambda n: n.get('depends_on', []))
        if dependency_cycle:
            errors.append('dependency cycle: ' + ' -> '.join(dependency_cycle))

    # Each graph should have at least one program root; multiple programs are allowed.
    roots = [n['id'] for n in index.values() if n.get('kind') == 'program']
    if not roots:
        errors.append('goal graph requires at least one program node')
    orphan_goals = [n['id'] for n in index.values() if n.get('kind') == 'goal' and not n.get('parent_id')]
    if orphan_goals:
        errors.append('goal nodes require a program parent: ' + ', '.join(orphan_goals))
    orphan_tasks = [n['id'] for n in index.values() if n.get('kind') == 'task' and not n.get('parent_id')]
    if orphan_tasks:
        errors.append('task nodes require a goal parent: ' + ', '.join(orphan_tasks))

    # Non-fatal hygiene signals.
    for node in index.values():
        if node.get('kind') in ('program', 'goal') and not node.get('success_criteria'):
            warnings.append(f'{node["id"]}: no success_criteria declared')

    return {
        'status': 'valid' if not errors else 'invalid',
        'aco_version': VERSION,
        'graph_id': graph.get('graph_id'),
        'scope_id': graph.get('scope_id'),
        'node_count': len(index),
        'programs': len([n for n in index.values() if n.get('kind') == 'program']),
        'goals': len([n for n in index.values() if n.get('kind') == 'goal']),
        'tasks': len([n for n in index.values() if n.get('kind') == 'task']),
        'dependencies': len([n for n in index.values() if n.get('kind') == 'dependency']),
        'errors': errors,
        'warnings': warnings,
        'policy': 'A graph models intent and dependencies only. It grants no new data access, permission, or external-action authority.'
    }


def _ancestor_chain(node_id: str, index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    cursor = index[node_id].get('parent_id')
    seen: set[str] = set()
    while cursor and cursor in index and cursor not in seen:
        seen.add(cursor)
        out.append(index[cursor])
        cursor = index[cursor].get('parent_id')
    return out


def _deadline_bonus(due_at: Any, as_of: datetime | None) -> int:
    if due_at is None or as_of is None:
        return 0
    due = _parse_time(due_at, 'due_at')
    assert due is not None
    seconds = (due - as_of).total_seconds()
    if seconds < 0:
        return 20
    days = seconds / 86400
    if days <= 3:
        return 15
    if days <= 7:
        return 10
    if days <= 30:
        return 5
    return 0


def goal_graph_status(graph: dict[str, Any], *, as_of: str | None = None,
                      limit: int = 5, root: Path | None = None) -> dict[str, Any]:
    if not isinstance(limit, int) or limit < 1 or limit > 50:
        raise ACOError('limit must be an integer 1..50')
    check = goal_graph_check(graph, root)
    if check['status'] != 'valid':
        raise ACOError('Invalid goal graph: ' + '; '.join(check['errors']))
    policy = _policy(root)
    satisfied = set(policy.get('satisfied_dependency_states', ['verified', 'done']))
    terminal = set(policy.get('terminal_states', ['done', 'cancelled']))
    as_of_dt = _parse_time(as_of, 'as_of') if as_of is not None else None
    index = _graph_index(graph)
    dependents: dict[str, int] = {k: 0 for k in index}
    for node in index.values():
        for dep in node.get('depends_on', []):
            if dep in dependents:
                dependents[dep] += 1

    task_rows: list[dict[str, Any]] = []
    for node in index.values():
        if node.get('kind') != 'task':
            continue
        node_id = node['id']
        unsatisfied = [dep for dep in node.get('depends_on', []) if index[dep].get('state') not in satisfied]
        blocked_ancestors = [a['id'] for a in _ancestor_chain(node_id, index)
                             if a.get('state') in {'blocked', 'cancelled', 'done'}]
        state = node.get('state')
        if state in terminal or state == 'verified':
            computed = 'terminal'
        elif blocked_ancestors:
            computed = 'blocked'
        elif unsatisfied:
            computed = 'blocked'
        elif state == 'proposed':
            computed = 'proposed'
        elif state == 'awaiting_approval':
            computed = 'awaiting_approval'
        elif state == 'in_progress':
            computed = 'in_progress'
        elif state == 'executed':
            computed = 'verification_required'
        else:
            computed = 'ready'

        state_bonus = {'in_progress': 30, 'awaiting_approval': 20, 'verification_required': 25,
                       'ready': 10}.get(computed, 0)
        priority = int(node.get('priority', 50))
        effort_penalty = (int(node.get('effort', 3)) - 1) * 2
        unblock_bonus = min(20, dependents.get(node_id, 0) * 5)
        urgency_bonus = _deadline_bonus(node.get('due_at'), as_of_dt)
        score = priority + state_bonus + urgency_bonus + unblock_bonus - effort_penalty
        blockers = []
        if unsatisfied:
            blockers.append({'type': 'dependency', 'node_ids': unsatisfied})
        if blocked_ancestors:
            blockers.append({'type': 'ancestor_state', 'node_ids': blocked_ancestors})
        task_rows.append({
            'id': node_id,
            'title': node.get('title'),
            'declared_state': state,
            'computed_state': computed,
            'priority': priority,
            'score': score,
            'score_factors': {
                'state_bonus': state_bonus,
                'deadline_bonus': urgency_bonus,
                'unblock_bonus': unblock_bonus,
                'effort_penalty': effort_penalty,
            },
            'blockers': blockers,
            'depends_on': list(node.get('depends_on', [])),
            'parent_id': node.get('parent_id'),
            'action_count': len(node.get('actions', []) or []),
        })

    eligible_states = {'ready', 'in_progress', 'awaiting_approval', 'verification_required'}
    eligible = [r for r in task_rows if r['computed_state'] in eligible_states]
    eligible.sort(key=lambda r: (-r['score'], r['id']))
    active_tasks = [r for r in task_rows if r['declared_state'] != 'cancelled']
    completed = [r for r in active_tasks if r['declared_state'] in {'verified', 'done'}]
    progress = 1.0 if not active_tasks else len(completed) / len(active_tasks)
    return {
        'status': 'actionable' if eligible else 'no_actionable_tasks',
        'aco_version': VERSION,
        'graph_id': graph.get('graph_id'),
        'scope_id': graph.get('scope_id'),
        'progress': round(progress, 4),
        'next_task_ids': [r['id'] for r in eligible[:limit]],
        'next_tasks': eligible[:limit],
        'blocked_task_ids': [r['id'] for r in task_rows if r['computed_state'] == 'blocked'],
        'task_states': task_rows,
        'policy': 'Next-best-action ranking is deterministic and advisory. It cannot broaden scope or bypass approval/verification gates.'
    }


def goal_transition(graph: dict[str, Any], event: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    check = goal_graph_check(graph, root)
    if check['status'] != 'valid':
        raise ACOError('Invalid goal graph: ' + '; '.join(check['errors']))
    if not isinstance(event, dict):
        raise ACOError('Transition event must be an object')
    node_id = event.get('node_id')
    to_state = event.get('to_state')
    if not _text(node_id) or not _text(to_state):
        raise ACOError('event.node_id and event.to_state are required')
    index = _graph_index(graph)
    if node_id not in index:
        raise ACOError(f'Unknown goal node: {node_id}')
    policy = _policy(root)
    transitions = {k: set(v) for k, v in policy.get('transitions', {}).items()}
    current = index[node_id].get('state')
    if to_state not in transitions.get(current, set()):
        raise ACOError(f'Invalid goal transition: {current} -> {to_state}')
    if to_state == 'verified' and not _text(event.get('evidence_ref')):
        raise ACOError('verified transition requires evidence_ref')
    if to_state == 'cancelled' and not _text(event.get('reason')):
        raise ACOError('cancelled transition requires reason')

    updated = deepcopy(graph)
    for node in updated['nodes']:
        if node['id'] == node_id:
            node['state'] = to_state
            node['last_transition'] = {
                'from_state': current,
                'to_state': to_state,
                'evidence_ref': event.get('evidence_ref'),
                'approval_ref': event.get('approval_ref'),
                'reason': event.get('reason'),
            }
            break
    return {
        'status': 'transition_applied',
        'aco_version': VERSION,
        'graph': updated,
        'node_id': node_id,
        'from_state': current,
        'to_state': to_state,
        'policy': 'This is an in-memory graph transformation. Persistence, external action and approval are separate host responsibilities.'
    }
