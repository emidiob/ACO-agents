# ACO 1.0 — Operating System & Token Economy

ACO 1.0 treats context as a compiled runtime resource rather than accumulated conversation text.

## Kernel objects

The Concierge coordinates references to persistent `Program`, `Goal`, `Task`, `Context`, `Policy`, `Execution`, `Receipt`, and `Skill` objects. Workers receive a compact task capsule instead of the full conversation or repository.

## Code versus state

- `ACO_RUNTIME_ROOT` points to a versioned ACO source/runtime checkout.
- `ACO_HOME` points to private durable user state and never doubles as the runtime source path.
- `aco://current` is a logical alias resolved through `registry/bootstrap.json`; it is not a filesystem path.
- Updating ACO code must not overwrite Goals, feedback ledgers, private context, receipts, or skill candidates stored under `ACO_HOME`.

## Bootstrap contract

A global ChatGPT/custom-instruction bootstrap should be small. It tells the host to resolve `aco://current`, read `VERSION` plus `registry/bootstrap.json`, and load only the role, skill, policy, and context required for the task. It must never preload the full repository.

A local host resolves an explicit runtime root, `ACO_RUNTIME_ROOT`, an enclosing project, then the packaged runtime. A conversational host with authorized repository/project/file retrieval may instead resolve an explicitly attached/project release or the canonical repository `emidiob/ACO-agents`. In every case it verifies `VERSION` and `registry/bootstrap.json` before claiming ACO is loaded. `ACO_HOME` is never used as the code path.

## Context Compiler

Each model call receives a task capsule compiled from the current task/goal references, required policies, minimum relevant role/skill capsules, authorized context selected under a token budget, and a response contract.

Progressive loading uses L0 (task/goal/policies), L1 (directly relevant context/skills), and L2 (deep evidence loaded only after an explicit insufficiency/refinement signal). A snapshot/delta contract prevents unchanged context from being resent unnecessarily. Private cross-scope sources still require exact scope authorization.

## Token Budget Manager

Budget classes are targets, not permission boundaries: `MICRO`, `SMALL`, `STANDARD`, `DEEP`, `RESEARCH`. Safety/decisive context wins over token savings.

## Skill Engine

A technical skill is not a role and not merely a saved prompt. A skill contains a compact method, inputs, failure modes, output contract, source provenance, version, lifecycle status, and token estimate.

Lifecycle: `discovered → candidate / candidate_unverified → testing → validated → active → deprecated`. `candidate_unverified` is fail-closed and never auto-selected.

## Persistent technical-skill inbox

`skill-learn` remains pure: it distills repeated structured observations into a candidate but does not persist or activate it. `skill-candidate-store` is a separate dry-run-by-default operation. With `--apply`, a validated non-active candidate is appended idempotently to `ACO_HOME/skills/candidates.json`. The store is private state, not the active registry. Promotion still requires benchmark evidence, explicit approval and a versioned registry change.

This separation lets ACO accumulate reusable techniques across conversations without allowing one chat to silently rewrite production behavior.

## Release invariant

ACO 1.0 succeeds only if longer history does not imply larger default prompts. The release gate compares full-context baseline with compiled context and targets at least 70% median input-token reduction while preserving required evidence, privacy, and critical-task correctness.
