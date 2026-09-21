# Test report — ACO v0.6.2

Date: 2026-09-21. Status: **release gates passed**.

This report covers mechanical package behavior, deterministic routing and a structured same-model behavior simulation. It is not a certification of artistic, curatorial, strategic, legal, security, commercial or host-integration quality.

## Release gate

The release policy was fixed before final validation:

- zero critical failures;
- all automatic tests pass;
- deterministic routing score at least 90/100;
- structured behavioral simulation score at least 90/100.

## Captured results

| Check | Observed result |
|---|---|
| Full Python unittest suite | **465 tests passed** in the release candidate |
| Generator parity | **473 generated files verified** |
| Canonical / native roles | **363 / 363** |
| Entry skills / workflows / optional resources | **16 / 61 / 97** |
| Role stocktake | **Clean: 363 roles scanned, 0 flagged issues** |
| Final routing holdout | **98.57/100; 28 cases; 0 critical failures** |
| Routing office accuracy | **100%** |
| Routing top-1 role accuracy | **96.43%** |
| Routing top-3 recall | **100%** |
| Routing minimal-team / overstaff rate | **100% / 0%** |
| Behavioral simulation | **97.83/100; 24 cases; 0 critical failures** |
| Compact Memory default | Preserved |
| Proprietary LICENSE | Byte-identical to v0.6.1; SHA-256 `7c5825f8f5cd2bb1f488dd72b4be710481dc78443add8d0ea42d30a9e70c155d` |
| Migration from v0.6.1 | **Passed** in a temporary Git checkout; history plus unrelated tracked and untracked files were preserved; migrated target validated and all 465 tests passed |

## Holdout discipline

The deterministic router was frozen before `config/routing-final-holdout.json` was run. Its 28 prompts are excluded from `config/routing-examples.json`; validation and tests enforce that there is no exact prompt overlap. Earlier failed/development routing sets were used for tuning and are **not** represented as independent evidence.

The final holdout produced one non-critical top-1 miss while retaining the acceptable role in the selected team/top three. That failure is preserved in the benchmark output rather than hidden.

## Behavioral simulation limitation

`release/behavioral-simulation.json` contains 24 structured cases scored across routing/scope, evidence/state, minimality, domain quality and action safety. The same assistant that helped develop the candidate performed this structured review. Therefore **97.83/100 is same-model regression evidence, not an independent or blind model-quality benchmark**.

No live email, social publication, payment, booking, CRM write, legal filing, paid generation or destructive system action was executed. Open-ended artistic, curatorial, writing, brand and design quality still requires review of real work.

## New 0.6.2 checks

- All 363 roles have generated structured contracts.
- Final routing holdout is excluded from consumed routing examples.
- `route-benchmark` must meet the packaged score/critical-failure gate.
- `handoff-check` requires evidence for checked/reviewed completion states.
- `capability-resolve` keeps availability, authorization and verification separate.
- `role-overlap` and `role-stocktake` are read-only/advisory.
- `eval-score` scores recorded review data but never invokes a model.
- `validate` checks the routing/simulation gates locally and read-only.

## Reproduction

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py role-stocktake
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
python3 -m unittest discover -s tests -v
```

The final ZIP is additionally extracted into a clean directory and these local checks are repeated before release. A post-build migration smoke test is also rerun externally so this embedded report does not require a self-referential rebuild after packaging.
