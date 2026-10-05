# Test report — ACO v0.7.2

Date: 2026-10-05. Status: **release gates passed locally**.

ACO v0.7.2 hardens context efficiency and private-scope isolation without adding roles.

## Release focus

- Context Engine for `NONE`, `BLIND`, `LIGHT`, `FULL` and `BLIND-FIRST`.
- Same-entity/client private-context boundary; another-client and unknown private scope stay blocked unless explicitly authorized.
- Relevance, source-count and character budgets make progressive retrieval measurable.
- Hybrid Memory read resolution respects context mode and scope while preserving the no-proactive-Drive policy.
- Routing hardening for artist residencies, independent brand strategy and cross-client context-boundary requests.
- Third fresh routing holdout frozen before its first run; no router changes were made after seeing that holdout result.
- 120-scenario deterministic routing/context/memory regression suite.

## Exact local release checks

| Check | Result |
|---|---:|
| Version | **0.7.2** |
| Canonical / native roles | **363 / 363** |
| Entry skills | **16** |
| Workflows | **61** |
| Optional resources | **99** |
| Generated files verified | **494** |
| Full Python unittest suite | **519 / 519 passed** |
| Existing final routing holdout | **98.57 / 100**, 28 cases, 0 critical failures |
| v0.7.2 fresh routing holdout 3 | **96.39 / 100**, 36 cases, 0 critical failures |
| Context benchmark | **100 / 100**, 30 cases, 0 critical failures |
| Context benchmark mean selection ratio | **47.07%** |
| 120-scenario real-world regression benchmark | **100 / 100**, 0 critical failures |
| Real-world mean context selection ratio | **42.12%** |
| Proactive Drive prompts in 120-scenario benchmark | **0** |
| Execution-policy benchmark | **100 / 100**, 62 cases |
| Delegation benchmark | **100 / 100**, 14 cases |
| Integration benchmark | **100 / 100**, 12 cases |
| Behavioral simulation | **98.67 / 100**, 42 cases, 0 critical failures |
| Privacy/PII scan | **Passed, 0 findings** |
| Compact Memory default | **Preserved** |

## Benchmark limitations

The context and 120-scenario suites are deterministic package-authored regression tests. They do not constitute independent human evaluation, live-provider testing, professional certification, or proof of universal routing/context quality. The behavioral simulation retains its same-model-review limitation. The fresh routing holdout is isolated from routing examples; it was frozen before first execution in this development pass.

## Remote state

No GitHub branch, commit or push is claimed by this local release report. The connected repository was observed with only `main`; a branch named `aco.agents` was not present when checked. No Google Drive/private-knowledge mutation was performed.
