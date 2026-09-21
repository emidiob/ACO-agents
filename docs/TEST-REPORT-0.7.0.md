# Test report — ACO v0.7.0

Date: 2026-09-21. Status: **release gates passed in the local release candidate**.

This report covers package mechanics, deterministic routing, deterministic execution-policy conformance and a structured same-model behavioral simulation. It is not a certification of artistic, curatorial, strategic, legal, security, commercial, provider or host-integration quality.

## Release gate

v0.7.0 requires:

- zero critical failures in deterministic gates;
- all automatic tests pass;
- routing regression score at least 90/100;
- execution-policy conformance at least 98/100;
- behavioral simulation score at least 90/100;
- generated-file parity and release integrity checks pass.

## Captured candidate results

| Check | Observed result |
|---|---|
| Full Python unittest suite | **481 tests passed** |
| Generator parity | **479 generated files verified** |
| Canonical / native roles | **363 / 363** |
| Entry skills / workflows / optional resources | **16 / 61 / 97** |
| Frozen routing regression | **98.57/100; 28 cases; 0 critical failures** |
| Routing office / top-1 / top-3 | **100% / 96.43% / 100%** |
| Routing overstaff rate | **0%** |
| Execution-policy benchmark | **100/100; 62 cases; 0 critical failures** |
| Structured behavioral simulation | **98.44/100; 36 cases; 0 critical failures** |
| Behavioral definitions | **18 cases** |
| Compact Memory default | Preserved |
| Canonical roles added | **0** |
| Mandatory third-party runtimes added | **0** |
| Migration from packaged v0.6.2 baseline | **Passed**; history plus unrelated tracked and untracked files preserved; migrated target validated and 481 tests passed |
| Final extracted v0.7.0 ZIP | **Passed after packaging**; independently extracted release re-ran validation and 481 tests |

## What v0.7.0 actually validates

The execution benchmark checks deterministic behavior for:

- learned/reference/optional/connected/local/unavailable/blocked capability distinctions;
- operation-level capability matching;
- availability, authorization and verification separation;
- exact action-packet-bound approval for SHARE/SEND/PUBLISH/APPLY/DEPLOY/DELETE/PURCHASE/SIGN;
- bounded non-destructive WRITE without repetitive approval ceremony;
- fallback behavior when execution is unavailable;
- prevention of blind retries after unknown outcomes;
- duplicate prevention when the exact action already has positive execution evidence.

`receipt-check` validates evidence requirements for outcome claims. `workflow-check` validates state transitions and forces reconciliation after an unknown result. `adapter-check` validates only caller-supplied adapter metadata and never reads credentials.

## What it does not validate

No live Gmail/WhatsApp/social/calendar/Drive/GitHub/CRM/payment/signature/provider adapter was called as part of the execution benchmark. No external account was connected, no purchase or paid generation was run, and no destructive remote action was performed.

`ready_to_execute` is therefore a **policy/capability readiness state**, not proof an action happened. Actual execution belongs to the host and requires real adapter/provider evidence.

The 36-case behavioral simulation remains same-model structured regression evidence, not an independent blind benchmark. Artistic, curatorial, brand, writing, design and film quality still require review of actual work.

## Routing continuity

The deterministic router is intentionally unchanged from v0.6.2. Its frozen 28-case final holdout remains excluded from routing examples and is rerun as a regression gate. v0.7.0 did not tune routing against that holdout.

## Reproduction

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
python3 -m unittest discover -s tests -v
```

The packaged v0.6.2 baseline was migrated in a temporary Git repository using the supplied migration command. The preview/apply path added 22 managed files, replaced 770 managed files, preserved the original Git history plus an unrelated tracked file and an unrelated untracked file, and the migrated target validated with all 481 tests passing.

The final v0.7.0 ZIP was then independently extracted and rerun through validation plus the full 481-test suite. This still does not constitute a live external-service integration test.
