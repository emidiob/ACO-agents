# Test report — ACO v0.6.1

Date: 2026-09-20. Status: **local release checks passed**. This report covers mechanical package behavior only; it is not a certification of artistic, strategic, legal, security, host-integration or third-party-tool quality.

## Release focus

v0.6.1 is an architecture/refinement release. It keeps the ACO office model and **363 canonical roles** while reducing duplicated role boilerplate, centralizing shared operating protocols, adding progressive context retrieval, explicit planning/approval and verification rules, scoped-learning guidance, maintenance audits and behavioral-evaluation definitions.

The canonical role corpus decreased from **3,097,029 characters** in the supplied v0.6.0 baseline to **1,631,183 characters** in v0.6.1, a reduction of about **47.3%**. This is a static package measurement, not provider token billing or active runtime telemetry; ACO normally loads selected roles rather than the full catalogue.

## Captured local results

| Check | Observed result |
|---|---|
| Full Python unittest suite | **454 tests passed** |
| Static package validation | Passed |
| Generator parity | **465 generated files verified** |
| Canonical / native roles | **363 / 363** |
| Entry skills / workflows / optional resources | **16 / 61 / 97** |
| Role maintenance stocktake | **Clean: 363 roles scanned, 0 flagged issues** |
| Behavioral eval definitions | **10 valid cases; 5 require human review** |
| Compact Memory default | Preserved |
| Migration from supplied v0.6.0 ZIP | Passed in a temporary Git repository; Git history plus unrelated tracked and untracked files were preserved; migrated target validated and its 454-test suite passed |
| Proprietary LICENSE | Byte-identical to v0.6.0 baseline; SHA-256 `7c5825f8f5cd2bb1f488dd72b4be710481dc78443add8d0ea42d30a9e70c155d` |
| Final extracted release | Re-validated and full 454-test suite passed from an independently extracted ZIP |

## Architecture checks added in 0.6.1

- Every canonical role uses the compact `ACO ROLE BOOTSTRAP`; the previous repeated long interaction/operating blocks are absent.
- Shared protocols exist for progressive context retrieval, planning versus approval, verification, scoped learning and role maintenance.
- `context-budget` reports static package/context estimates without presenting them as runtime telemetry.
- `role-stocktake` is read-only and never merges, retires or deletes roles automatically.
- `eval-lint` validates behavioral-eval definitions; it does not pretend to run a model benchmark.
- Compact Memory remains the only default durable continuity model. The release does not add a second memory vault or create one file per lesson/session.

## Behavioral evals

`config/evals.json` contains 10 cases spanning artist-development pipeline discipline, commercial lead boundaries, cross-client isolation, blind critique, web visual verification, AI-video capability claims, external-action outcomes, brand evidence, plan-versus-permission and minimal tool selection.

The release validates their structure and exposes them through `eval-show`. It **does not claim those 10 cases were executed as a model-quality benchmark**. Five explicitly require human review because package tests cannot establish artistic, curatorial, design or other open-ended quality.

## Reproduction

Run from the complete extracted release:

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py context-budget
python3 scripts/aco_cli.py role-stocktake
python3 scripts/aco_cli.py eval-lint
python3 -m unittest discover -s tests -v
```

The package manifest fingerprints distributed files. The ZIP checksum is supplied alongside the archive rather than embedded circularly inside it.

## Important limits

- No authenticated GitHub push or Google Drive mutation was performed by the release checks.
- No live email, WhatsApp, social publishing, CRM write, phone call, scheduler action or paid generation was performed.
- No external ECC runtime, hook system or Memory Vault is bundled or required. ECC was used as an architectural reference; ACO keeps its own identity, knowledge model and license.
- No automatic learning from raw conversations is enabled; durable learning remains scoped and reviewable under ACO's knowledge policy.
- Passing code/package tests does not prove that a design is visually successful, a film is well directed, a curatorial judgment is strong, or a business recommendation will perform.
- Optional third-party tools remain subject to availability, authorization, privacy and licensing checks at the time of use.
