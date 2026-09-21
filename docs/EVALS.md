# ACO evaluation gates — v0.7.0

Package tests establish mechanical behavior. They do **not** prove artistic quality, curatorial judgment, strategic value, legal correctness, security of third-party services or universal host reliability. ACO keeps separate gates for routing, behavior and execution-policy conformance.

## 1. Behavioral regression definitions

`config/evals.json` contains portable behavior cases covering Compact Memory, cross-client isolation, visual/evidence boundaries, plan-versus-permission and the v0.7 execution contract.

```bash
python3 scripts/aco_cli.py eval-lint
python3 scripts/aco_cli.py eval-show
```

These commands validate/display cases. They do not invoke a model.

## 2. Frozen routing regression

The deterministic router is unchanged from the v0.6.2 routing release. `config/routing-final-holdout.json` remains excluded from consumed routing examples and is rerun as a regression gate.

```bash
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
```

The v0.6.2 baseline was 98.57/100 with zero critical failures. v0.7.0 must not regress below the packaged gate. This benchmark measures the local router only, not every possible natural-language request.

## 3. Execution-policy conformance

`config/execution-benchmark.json` exercises capability state, permission, approval, fallback and retry/reconciliation logic across representative office actions.

```bash
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
```

It is deterministic and **does not call Gmail, Drive, GitHub, social platforms, payment providers, browsers or any other external service**. Its purpose is to catch policy regressions such as treating an optional tool as connected, bypassing approval, or retrying an unknown action.

Release threshold: at least 98/100 and zero critical failures.

## 4. Structured behavioral simulation

`release/behavioral-simulation.json` contains cross-office scenarios scored on routing/scope, evidence/state, minimality, domain quality and action safety. v0.7 adds execution-layer scenarios for receipts, approval binding, unknown outcomes, sharing, payments, signing and workflow state.

```bash
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
```

This is same-model structured regression evidence from development, not an independent blind judge. Open-ended artistic, curatorial, writing, visual and strategic quality still requires human review of real work.

## Release gate

v0.7.0 closes only if:

- all local automatic tests pass;
- routing regression is at least 90/100 with zero critical failures;
- execution-policy conformance is at least 98/100 with zero critical failures;
- behavioral simulation is at least 90/100 with zero critical failures;
- generated-file parity, release hashes, license integrity and migration checks pass.

## Future comparisons

1. Keep deterministic policy tests distinct from model-quality evaluation.
2. Freeze candidate behavior before running fresh final holdouts when routing or model-mediated logic changes.
3. Do not reinterpret `ready_to_execute` as an executed provider action.
4. Record unavailable live-host checks as unrun rather than faking evidence.
5. Preserve failed cases as regression evidence instead of rewriting the rubric to make a release pass.
