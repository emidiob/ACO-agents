# Goal Graph & Autonomy Engine — 0.8.0

ACO 0.8 adds a coordination layer above routing and execution. It models **Program → Goal → Task → Dependency**, selects a bounded next task, then resolves any task actions through the existing capability, permission, receipt and verification contracts.

This does not turn 363 role definitions into 363 background processes. It gives the Concierge a deterministic way to continue multi-step work without confusing long-term intent, current outcomes, concrete tasks and external blockers.

## Minimal graph

```json
{
  "schema_version": 1,
  "graph_id": "practice-development",
  "scope_id": "artist-private",
  "nodes": [
    {
      "id": "program-practice",
      "kind": "program",
      "title": "Build a sustainable independent practice",
      "state": "active",
      "priority": 90,
      "effort": 3,
      "success_criteria": ["Sustained institutional opportunities and income"]
    },
    {
      "id": "goal-network",
      "kind": "goal",
      "parent_id": "program-practice",
      "title": "Strengthen curatorial relationships",
      "state": "active",
      "priority": 80,
      "effort": 3,
      "success_criteria": ["Qualified relationships move to concrete opportunities"]
    },
    {
      "id": "task-research",
      "kind": "task",
      "parent_id": "goal-network",
      "title": "Research current opportunities",
      "state": "active",
      "priority": 75,
      "effort": 2,
      "depends_on": [],
      "success_criteria": ["Qualified shortlist with source evidence"]
    }
  ]
}
```

Node states are intentionally explicit. `verified` requires evidence when applied through `goal-transition`; `done` is a separate closure state. Dependencies are satisfied only by verified/done states, not by a promise that something will happen.

## Next Best Action

`goal-status` checks graph structure, dependency cycles, parent relationships and scope consistency. Eligible tasks are ranked deterministically by:

1. continuation state (`in_progress`, approval/verification gates, then ready work);
2. declared priority;
3. deadline urgency when an explicit `--as-of` is supplied;
4. downstream-unblock value;
5. bounded effort penalty.

This score is a coordination heuristic, not a claim of business value. Explicit user intent and safety/approval policy still outrank it.

```bash
python3 scripts/aco_cli.py goal-check --input examples/goals/artist-program.json
python3 scripts/aco_cli.py goal-status --input examples/goals/artist-program.json --as-of 2026-10-06T00:00:00+00:00
```

## Task actions

A task may have no actions, in which case it represents professional/model work. Or it may define a small DAG of existing capability packets:

```json
{
  "id": "send_followup",
  "capability_id": "email.send",
  "operation": "send",
  "target": "recipient-fixture",
  "payload_ref": "approved-followup",
  "depends_on": ["prepare_followup"],
  "verification": {
    "success_states": ["sent", "delivered"],
    "require_evidence": true
  }
}
```

The engine never silently changes the existing permission model. `email.send`, deletion, publishing, applications, production deployment, purchases, signatures and sharing still require the approval level already defined by ACO.

## Simulation and host execution

```bash
python3 scripts/aco_cli.py autonomy-plan --input examples/goals/artist-program-simulation.json
python3 scripts/aco_cli.py autonomy-benchmark --input config/autonomy-benchmark.json
```

`SIMULATE` can return `simulation_ready` but no host actions. `HOST_EXECUTION` can return `host_action_required` packets only after capability and permission checks. The local CLI never calls a provider; the actual host executes, returns a receipt, and the engine then verifies or reconciles the result.

Important statuses include:

- `approval_required` — final packet lacks exact consequential approval;
- `host_action_required` — policy/capability checks pass and the host may perform the returned packet;
- `reconcile_required` — a prior exact action has uncertain/in-flight outcome;
- `manual_recovery` — retry is unsafe or exhausted;
- `verification_required` — a receipt exists but does not satisfy the task's verification rule;
- `task_verified` — all actions have sufficient evidence;
- `delegated_work_required` — the next task is professional/model work rather than a host capability action.

## Persistence

A Goal Graph is not automatically a new file or database. Keep it transient unless continuity materially benefits from persistence. If persisted, keep it inside an already-authorized scoped canonical record or approved local store and follow Compact/Hybrid Memory. Do not create a file per task or status event.

The complete fictional example is [`examples/goals/artist-program.json`](../examples/goals/artist-program.json). It contains no real recipient or private user data.
