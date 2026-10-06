# ACO Agents v0.8.0 — Test & Release Report

## Release objective

ACO v0.8.0 adds a durable **Goal Graph + Autonomy Engine** above the validated v0.7.3 routing/context/execution foundation. The release is designed to distinguish one-step work from durable dependent work and to represent the latter as:

`Program → Goal → Task → Dependency`

The autonomy layer can rank next-best actions, respect task/action dependencies, apply existing capability and permission contracts, require exact approvals for consequential actions, interpret execution receipts, reconcile unknown outcomes, and make bounded retry/fallback decisions. It does **not** call external providers by itself and it does not claim an action succeeded without sufficient evidence.

## Release shape

- Version: **0.8.0**
- Canonical agents: **363**
- Native agents: **363**
- Skills: **16**
- Workflows: **61**
- Optional resources: **99**
- Default memory mode: **compact**
- Generated derived files: **504**
- No canonical role inflation from v0.7.3

## New v0.8.0 capabilities

### Goal Graph

- Scoped graph model with Program, Goal, Task and Dependency nodes.
- Structural validation, parent-kind rules, dependency-reference validation and cycle rejection.
- Explicit task state transitions; `verified` requires evidence and `cancelled` requires a reason.
- Deterministic advisory Next Best Action ranking using priority, continuation, deadline urgency, downstream unblock value and effort.
- Cross-scope graph nodes are rejected.
- Simple one-step tasks remain direct and do not require graph creation.

### Autonomy Engine

- `SIMULATE` mode produces no host actions or side effects.
- `HOST_EXECUTION` may prepare bounded host-action packets but the local engine does not invoke providers itself.
- Existing capability/permission contracts are reused rather than bypassed.
- Consequential actions such as send/delete continue to require exact packet-bound approval.
- Action DAG successors remain blocked until predecessor evidence is verified.
- Unknown/in-flight execution receipts force reconciliation rather than blind retry.
- Failed actions are retryable only within the configured retry budget and, by default, with an idempotency key.
- Insufficient receipt evidence yields `verification_required` rather than false completion.
- Professional/model work without a host action remains explicit as delegated work.

## New deterministic autonomy benchmark

Command:

```text
python3 scripts/aco_cli.py autonomy-benchmark --input config/autonomy-benchmark.json
```

Result:

- Cases: **29/29 passed**
- Score: **100.0/100**
- Critical failures: **0**

Coverage includes graph readiness and dependencies, priority/continuation/deadline ranking, graph and action-DAG cycle rejection, cross-scope rejection, simulation safety, read/write capability behavior, exact approvals, verified/unknown/failed receipts, bounded retry, idempotency, reconciliation, missing-capability fallback, delete/send gates, strict verification and action dependency evidence.

## Full automated test suite

The full suite was executed in five deterministic groups to avoid a runner wall-clock limit on one monolithic invocation. Every discovered `tests/test_*.py` module was included exactly once.

| Group | Tests | Result |
|---|---:|---|
| compact + Drive + execution v0.7.0 + expansion | 102 | PASS |
| finance + harness + install + memory | 82 | PASS |
| migrate + planning + production + routing quality | 74 | PASS |
| resources + specialist + studio readiness + tidy/compact sync | 223 | PASS |
| v0.7.1 + v0.7.2 + v0.7.3 + v0.8.0 regressions | 69 | PASS |
| **Total** | **550** | **PASS** |

**Final unit/regression result: 550/550 passed.**

## Release validation gates

`python3 scripts/aco_cli.py validate` returned `status: validated` with:

- Delegation benchmark: **100.0/100**
- Integration benchmark: **100.0/100**
- Execution benchmark: **100.0/100**
- Autonomy benchmark: **100.0/100**, 29 cases
- v0.7.2 routing fresh holdout regression: **96.39/100**
- v0.7.3 development holdout regression: **100.0/100**
- v0.7.3 frozen fresh holdout: **98.0/100**
- Context benchmark: **100.0/100**
- Mean context selection ratio: **0.4707**
- Exact-scope privacy boundary benchmark: **100.0/100**, 28 cases
- Real-world routing/context/memory benchmark: **100.0/100**
- Real-world mean context selection ratio: **0.4212**
- Privacy findings: **0**
- Relative documentation links checked: **4825**

The frozen v0.7.3 final routing holdout remains historical evidence and is preserved byte-for-byte rather than rewritten to report v0.8.0.

## Privacy and approval properties

- Goal graph nodes cannot silently cross their graph scope.
- v0.7.3 exact private-scope authorization remains enforced.
- Wildcard/global cross-client authorization remains invalid.
- `SIMULATE` never emits host actions.
- Exact action approvals remain bound to the action packet.
- Unknown execution state is reconciled before retry.
- Completion requires sufficient receipt/evidence under the action verification policy.
- Final privacy scan: **0 findings**.

## Distribution integration

v0.8.0 is integrated into the generated/runtime distribution, not only the source tree:

- Runtime modules include `aco/goals.py` and `aco/autonomy.py`.
- Runtime configs include Goal Graph, autonomy policy and autonomy benchmark contracts.
- CLI commands added: `goal-check`, `goal-status`, `goal-transition`, `autonomy-plan`, `autonomy-benchmark`.
- Concierge/skill/architecture/CLI documentation describes when Goal Graph should and should not be used.
- A packaged artist-program example exercises durable goal/dependency behavior without external side effects.

## Known limitations

- Release validation and the autonomy benchmark are deterministic/static/local checks. They do not execute a live external adapter or provider action.
- The Next Best Action score is a deterministic heuristic, not a learned prediction of user utility.
- The local engine prepares host actions; actual provider execution belongs to the host/integration layer.
- ACO v0.8.0 does not introduce a background scheduler or asynchronous worker.
- Passing these gates does not certify professional/creative quality for every delegated task.

## Release decision

**PASS — ACO Agents v0.8.0 is eligible for packaging.**

The release adds the Goal Graph and Autonomy Engine while retaining all tested v0.7.3 routing, privacy, memory, integration and execution boundaries.
