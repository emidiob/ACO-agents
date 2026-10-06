# Goal Graph & Autonomous Execution — ACO 0.8

Use this protocol only when work spans multiple dependent steps or a durable outcome. A one-step request should still be completed directly; do not create a Program/Goal ceremony for ordinary drafting, lookup or editing.

## 1. Four graph objects

- **Program** — a long-horizon direction that can contain several outcomes.
- **Goal** — a verifiable outcome inside one Program.
- **Task** — a bounded unit of work that can be selected and completed.
- **Dependency** — a blocker or prerequisite. It is not work merely because it exists.

The graph is scoped. Every node stays inside the graph's `scope_id`. A graph does not merge clients, organizations, projects or private contexts and never grants access to another scope.

## 2. Next Best Action

Use graph dependencies first, then continue work already in progress, then resolve approval/verification gates, then rank ready tasks by declared priority, deadline urgency, downstream-unblock value and bounded effort. The ranking is advisory: it cannot override the user's explicit current request, a safety rule, a private-scope boundary or a consequential approval gate.

Do not manufacture a task only to keep the graph busy. If every task is blocked, report the dependency that must change.

## 3. Two kinds of task

A task may be **professional/model work** with no host action packet, or it may contain a small action DAG using existing ACO capability IDs. Model work is delegated to the selected role/method. Host actions go through the Execution protocol.

For action DAGs, a downstream action is eligible only after its declared predecessor has sufficient receipt evidence. Merely planning or simulating the predecessor does not unlock the next action.

## 4. Autonomy is permission-aware

`SIMULATE` shows what would be eligible and never returns an executable host-action list. `HOST_EXECUTION` may return bounded action packets for the host, but the local ACO engine itself never invokes a provider.

Existing `permission-policy.json` remains authoritative:

- in-scope `READ`, `DRAFT`, `PREVIEW` and bounded non-destructive `WRITE` can be prepared without a new approval when their existing policy allows it;
- `SHARE`, `SEND`, `PUBLISH`, `APPLY`, `DEPLOY`, `DELETE`, `PURCHASE` and `SIGN` still require exact packet-bound approval;
- a Goal, Program, previous approval or general instruction is never blanket permission for a materially changed action.

## 5. Receipts before completion

The engine must never convert `ready_to_execute` into “done.” Completion is evidence-driven:

```text
selected → prepared → host action → receipt → verification → task verified → graph transition
```

An `unknown` or in-flight receipt requires reconciliation before retry. A failed action may be retried only under a bounded retry policy and, by default, with an idempotency key. Exhausted or unsafe retries become manual recovery/fallback.

Task-specific verification may require stronger provider states. For example, `accepted` need not satisfy a task that explicitly requires `sent` or `delivered`.

## 6. Graph state is not a second memory vault

Keep transient graphs in the task/session. Persist a material Program/Goal graph only inside an already-authorized existing scoped canonical record or other approved store. Do not create one file per goal, task, dependency, receipt or status transition. Pipeline ≠ project still applies.

## 7. Observable trace, not hidden reasoning

Expose the selected task IDs, blockers, permission class, action packet/hash, receipt state, verification result, retry/reconciliation decision and next observable step. Do not expose or require private chain-of-thought.

## 8. Local conformance tools

`goal-check`, `goal-status`, `goal-transition`, `autonomy-plan` and `autonomy-benchmark` are deterministic local tools. They do not connect accounts, persist a user's graph, or execute external providers.
