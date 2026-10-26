# ACO Agents 1.0.5 — Genjutsu and Quick Commands

**Status of this local release candidate:** Prepared from the exact upstream ACO 1.0.4 release and independent JutsuHQ MIT source instructions. Verification is performed by the builder before producing a distributable ZIP; this report does not claim unobserved external provider testing or publication to GitHub.

## Contents

- Seven entrypoint skills: `/aco`, `/aco-genjutsu`, `/aco-video`, `/aco-image`, `/aco-capture`, `/aco-skills`, `/aco-help`.
- One prompt-only Genjutsu reference-video replica skill in the technical registry.
- Source-boundary checks, version-aware registry and safe installed-skill ownership.
- A per-skill evidence inventory: 14 existing active methods and 30 experimental candidates (44 total).
- All 363 original role methods remain the same, with runtime regenerated and release manifest rebuilt.

## Testing contract

Generator parity, ACO validate, full unittest suite, skill registry checks, candidate fail-closed tests, ZIP integrity and SHA-256 are mandatory builder checks. A locally built ZIP is not a public GitHub release until actually published. The 29 original candidates and new Genjutsu method have no substantiated model-output benchmark in this package and remain candidates.

See `docs/SKILL-VALIDATION-v1.0.5.md` and `release/skill-evidence-v1.0.5.json`.

## Verified release checks — 2026-10-26

Local macOS / Python 3.13.5 checks completed:

- Generator parity: 570 derived files verified.
- Full ACO validation: passed; 363 roles, 23 entry skills, 61 workflows, 99 optional resources.
- Full unittest discovery: 643 tests passed.
- Privacy release gate: zero findings.
- Technical registry: 44 methods, 14 active and 30 candidates; skill benchmark passed.
- Historical routing regression and semantic freeze checks passed. Only the seven known command names/count are excluded from historical catalogue comparison; all original routing fields remain hash-checked. Mutation tests reject altered roles, offices, unknown skills, missing original skills and incorrect counts.

Build-kit compatibility repairs include both installer ownership checks, compact-memory instructions on all shortcuts, current version/count assertions and current documentation metadata. Historical holdout files and their recorded hashes remain unchanged. No live provider rendering or external integration was tested.
