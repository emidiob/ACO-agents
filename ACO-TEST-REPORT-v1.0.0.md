# ACO Agents v1.0.0 — Release Test Report

## Release theme

**ACO Operating System & Token Economy.** ACO 1.0 moves Concierge from a primary router into a token-aware kernel coordinating persistent Programs, Goals, Tasks, Contexts, Policies, Executions, Receipts and technical Skills.

## Core additions

- `aco://current` logical runtime locator.
- `ACO_RUNTIME_ROOT` for versioned code/runtime; `ACO_HOME` for private durable state.
- Host-aware resolution through an explicitly attached/project ACO release or authorized canonical repository `emidiob/ACO-agents`; runtime identity must be verified through `VERSION` and `registry/bootstrap.json`.
- Minimal global bootstrap; repository/history/all roles/all skills are not preloaded.
- Context Compiler + Token Budget Manager with progressive loading, exact private-scope checks, soft token targets and snapshot/delta reuse.
- Technical Skill Registry with on-demand resolution and fail-closed candidate states.
- Structured Skill Learning that rejects hidden reasoning/scratchpad fields and requires repeated distinct evidence.
- Private skill candidate inbox at `ACO_HOME/skills/candidates.json`; storage is dry-run by default, idempotent with `--apply`, and never mutates the active registry.
- 15 initial technical skill records: 14 active verified seeds plus one unverified Mimic lead kept non-selectable.

## Token economy

Development benchmark:

- 32/32 cases passed
- 100/100 score
- 0 critical failures
- median input-token reduction: **92.33%** against the authorized full-candidate-context baseline

Final fresh holdout #4:

- 10/10 cases passed
- 100/100 score
- 0 critical failures
- median input-token reduction: **94.25%**

These figures are deterministic release-benchmark results, not a guarantee that every real conversation will achieve the same reduction.

## Skill / OS gates

- Technical skill benchmark: **28/28, 100/100, 0 critical failures**
- OS development benchmark: **31/31, 100/100, 0 critical failures**
- Final fresh OS holdout #4: **20/20, 100/100, 0 critical failures**
- Final fresh token holdout #4: **10/10, 100/100, 0 critical failures**

The final holdout #4 was frozen before its first execution.

### Recovery chronology

After the environment reset, a new recovery holdout #3 was frozen before execution. It produced one critical failure: a natural phrase for a small UI micro-interaction did not resolve Design Spells because the lexical coverage floor was too strict. The holdout was retained as development evidence, the resolver was generalized (two strong matching terms can satisfy a long natural query), development gates were rerun, and a distinct holdout #4 was frozen and passed on first execution.

## Historical regression suite

All historical suites remain green:

- Group 1: **228/228 PASS**
- Group 2: **320/320 PASS**
- Install + migrate: **30/30 PASS**
- Total: **578/578 PASS**

Preserved gates include routing, Context Engine, exact-scope privacy, Hybrid Memory, execution/approval/receipt handling, delegation/integration, Goal Graph/Autonomy, and Adaptive ACO shadow learning/promotion safety.

## Privacy and safety

- Release privacy scan: **0 findings**
- Cross-client private context still requires exact scope authorization.
- Legacy global cross-scope boolean does not grant private access.
- `candidate_unverified` skills cannot be automatically resolved.
- Skill candidates cannot activate themselves or rewrite production behavior.
- Hidden reasoning / chain-of-thought / scratchpad fields are rejected as learning material.
- ACO_HOME private state is not bundled in the release.
- No live external provider action is performed by release validation.

## Seed skills

Verified active seeds cover archive-first visual research, Letterform Archive, Met Open Access, Rijksmuseum data, NYPL public-domain research, archives.design, Details, Refero, Design Spells, frontend animation-library selection, GSAP, Anime.js, Motion for React, and React Spring.

The user-supplied LittleDavi/Mimic lead could not be verified to an exact primary repository, so it remains `candidate_unverified` and is excluded from default skill resolution.

## Release invariants

- 363 canonical roles
- 16 entry skills
- 61 workflows
- 99 optional resources
- Compact memory remains the default
- No GitHub push, merge, tag or external publication was performed during this build
