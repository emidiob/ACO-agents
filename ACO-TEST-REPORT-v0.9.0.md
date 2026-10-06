# ACO Agents v0.9.0 — Test & Release Report

## Release summary

ACO v0.9.0 adds **Adaptive ACO** above the validated v0.8.0 Goal Graph + Autonomy Engine. The new layer records explicit corrections, scoped preferences and observable outcomes as structured evidence, derives bounded **shadow-only** candidates from repeated evidence, compares adaptive ranking against the unchanged production Goal Graph, and checks whether a candidate is eligible for deliberate promotion.

The production execution, permission, privacy, routing, context and verification contracts remain unchanged. Adaptive ACO cannot grant permissions, broaden private scope, mark external work completed, or activate its own candidates.

- Version: **0.9.0**
- Canonical roles: **363**
- Native profiles: **363**
- Entry skills: **16**
- Workflows: **61**
- Optional resources: **99**
- Generated/derived files: **508**
- Memory default: **compact**

## Dogfooding the 0.8 system

The 0.9 development task was represented and run through the v0.8 Goal Graph itself as:

`Program → Goal → specification → feedback ledger → adaptation → shadow ranking → promotion contract → integration → fresh benchmark → release`

At the start, `goal-status` selected only the architecture/specification task and kept every dependent task blocked. After verified transitions, it selected integration, then the fresh benchmark, then release. Immediately before release work the graph reported **87.5% progress** with only `task-release` actionable.

The v0.8 Autonomy Engine was also used in `SIMULATE` mode to confirm that code inspection could proceed as an in-scope read while the dependent write action remained locked until its predecessor completed. No provider action was executed by the local engine.

## New v0.9.0 capabilities

### Scope-bound structured feedback

Feedback records are validated against a declared `scope_id`, target type, target ID, signal and source reference. Observable outcome feedback requires evidence. Hidden/private reasoning fields such as chain-of-thought, scratchpad and internal-monologue fields are rejected.

### Append-only evidence semantics

Feedback ledgers form a SHA-256 chain. Editing, deleting, reordering or moving a record across scope invalidates the ledger. `feedback-append` returns an updated ledger value but does not persist it.

### Minimum evidence before adaptation

A single correction cannot become a learned rule. Candidate proposals require repeated records, minimum consensus and multiple distinct evidence sources. Optional feedback weight cannot bypass the record/source threshold.

In v0.9, automatic candidates are intentionally limited to:

- scoped output preference key/value candidates;
- bounded Goal Graph `adaptive_feature` score deltas.

Routing, context and autonomy corrections may be recorded as evidence but do not auto-generate production policy changes.

### Shadow ranking

`shadow-rank` returns base and shadow next-task order together. It never mutates the graph. Ranking candidates apply only to the generic `next-best-action` target or the exact graph ID they were learned for. Same-scope graph feature names alone are not enough to apply an unrelated candidate.

### Promotion and rollback contract

`promotion-check` requires:

- the exact candidate SHA-256;
- a frozen-before-first-run benchmark;
- the configured minimum score/case count;
- zero allowed critical failures;
- historical regressions passing;
- exact explicit approval bound to the candidate hash;
- a rollback reference.

A passing check reports only **eligibility**. It does not activate or write a policy.

## Test suite

The full test suite passed in deterministic blocks to avoid the execution runner's monolithic timeout:

| Block | Tests | Result |
|---|---:|---|
| Compact / Drive / Execution / Expansion / Finance / Harness | 121 | PASS |
| Install / Migrate | 30 | PASS |
| Memory / Planning / Production / Routing / Resources / Specialist / Readiness / Tidy | 330 | PASS |
| v0.7.1 / v0.7.2 / v0.7.3 / v0.8.0 / v0.9.0 regressions | 81 | PASS |
| **Total** | **562** | **PASS** |

The initial monolithic run produced only expected release-integrity errors because the release manifest still fingerprinted v0.8.0. After a provisional v0.9.0 manifest was built, all install/migrate integrity tests passed.

## Deterministic release gates

| Gate | Result |
|---|---:|
| Execution benchmark | **100/100** |
| Delegation benchmark | **100/100** |
| Integration benchmark | **100/100** |
| Context benchmark | **100/100** |
| Context mean selection ratio | **47.07%** |
| Exact-scope privacy boundary | **100/100 — 28 cases** |
| Real-world routing/context/memory | **100/100 — 120 scenarios** |
| Real-world mean context selection ratio | **42.12%** |
| v0.7.2 routing regression | **96.39/100** |
| v0.7.3 development routing regression | **100/100** |
| v0.7.3 frozen fresh routing holdout | **98/100** |
| v0.8 autonomy benchmark | **100/100 — 29 cases** |
| v0.9 adaptive development benchmark | **100/100 — 32 cases** |
| v0.9 adaptive frozen fresh holdout | **100/100 — 27 cases** |
| Privacy/PII findings | **0** |

## Fresh adaptive holdout chronology

The final v0.9 adaptive holdout was written and frozen before its first execution.

- Holdout: `config/adaptive-v090-holdout.json`
- Cases: **27**
- Frozen SHA-256: `9d4604a52a766d24b73608f2647003b3423ca00556f41adc0e68cb9ebb0a60fe`
- First execution: **PASS**
- First-run score: **100.0**
- First-run critical failures: **0**

After the first run, semantic hashes were frozen for `scripts/aco/adaptive.py`, `scripts/aco/goals.py`, `config/adaptive-policy.json` and `config/goal-graph.json`. Release validation fails if any of those semantics change without a new holdout chronology.

## Privacy and package validation

The privacy scanner reported **0 findings**. The release validator also checks generated parity, canonical/native role coverage, relative links, release hashes, historical routing freezes, context boundary gates, behavior/delegation/integration/execution contracts, Goal Graph/Autonomy gates, the adaptive development benchmark, the frozen fresh adaptive holdout and the post-holdout semantic freeze.

## Limitations

- Adaptive ACO is deterministic evidence aggregation and shadow evaluation, not a trained machine-learning model.
- The benchmarks do not prove subjective professional, artistic or strategic quality.
- No live email, publishing, payment, deployment, deletion or other external provider action is executed by the local validator.
- Feedback persistence remains a separate authorized host responsibility.
- A candidate that is eligible for promotion is still not active; activation requires a deliberate versioned maintainer change followed by a new release validation.

## Release decision

**PASS — ACO Agents v0.9.0 is eligible for packaging.**
