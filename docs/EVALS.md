# ACO evaluation gates — v0.7.2

Package tests establish mechanical behavior. They do **not** prove artistic quality, curatorial judgment, strategic value, legal correctness, security of third-party services or universal host reliability. ACO keeps separate gates for routing, behavior, execution policy, delegation, adapter resolution and privacy hygiene.

## 1. Behavioral regression definitions

`config/evals.json` contains portable behavior cases covering Compact/Hybrid Memory, cross-client isolation, visual/evidence boundaries, delegation, no-Drive-nagging, provider evidence, plan-versus-permission and the execution contract.

```bash
python3 scripts/aco_cli.py eval-lint
python3 scripts/aco_cli.py eval-show
```

These commands validate/display cases. They do not invoke a model.

## 2. Frozen routing regression

The deterministic router remains the v0.6.2 routing baseline. `config/routing-final-holdout.json` stays excluded from consumed routing examples and is rerun as a regression gate.

```bash
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
```

The frozen baseline is 98.57/100 with zero critical failures. This benchmark measures the packaged local router only, not every possible natural-language request.

## 3. Execution-policy conformance

```bash
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
```

This deterministic benchmark checks capability state, permission, approval, fallback and retry/reconciliation logic. It does not call external services. Release threshold: at least 98/100 and zero critical failures.

## 4. Delegation conformance

```bash
python3 scripts/aco_cli.py delegation-benchmark
```

This gate checks the rule **resolve rather than defer**: reversible professional judgments inside a delegated role should be decided from sufficient evidence, while missing decisive facts, private-scope ambiguity, irreducible personal preference and consequential authorization still cause the appropriate user checkpoint.

Release threshold: 100/100 and zero critical failures.

## 5. Integration-resolution conformance

```bash
python3 scripts/aco_cli.py integration-benchmark
```

This gate checks provider-neutral adapter selection from current caller-supplied evidence: exact capability, availability, connection when remote, operation authorization, verification, provider boundary and fallback. It does not connect or execute any provider.

Release threshold: 100/100 and zero critical failures.

## 6. Privacy/PII release gate

```bash
python3 scripts/aco_cli.py privacy-scan
```

The public release must have zero unreviewed likely personal/private/credential findings. The scanner narrowly allows synthetic example domains, localhost fixtures, the public copyright holder in license files and the canonical public repository identifier. Findings are redacted in reports.

## 7. Structured behavioral simulation

`release/behavioral-simulation.json` contains cross-office scenarios scored on routing/scope, evidence/state, minimality, domain quality and action safety. v0.7.2 adds delegation, no-Drive-nagging, Hybrid Memory, provider-neutral adapter and privacy scenarios.

```bash
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
```

This remains same-model structured regression evidence from development, not an independent blind judge. Open-ended artistic, curatorial, writing, visual and strategic quality still requires human review of real work.

## Release gate

v0.7.2 closes only if:

- all local automatic tests pass;
- routing regression is at least 90/100 with zero critical failures;
- execution-policy conformance is at least 98/100 with zero critical failures;
- delegation conformance is 100/100 with zero critical failures;
- integration-resolution conformance is 100/100 with zero critical failures;
- behavioral simulation is at least 90/100 with zero critical failures;
- privacy scan reports zero unreviewed findings;
- generated-file parity, release hashes, license integrity and migration checks pass.

## Future comparisons

Keep deterministic policy tests distinct from model-quality evaluation. Freeze candidate behavior before fresh final holdouts when routing/model-mediated logic changes. Never reinterpret readiness as execution or an unavailable live-host test as passed evidence.
