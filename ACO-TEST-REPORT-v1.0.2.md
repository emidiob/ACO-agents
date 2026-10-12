# ACO Agents v1.0.2 — Generative Image Candidate Skillpack

## Scope

Build on the v1.0.1 archive; preserve 363 roles, 16 original entry skills, all existing 12 Seedance candidates, and OS/token economy/security semantics. Add 12 independently structured reusable generative-image skill candidates and four model-specific adapters: Nano Banana 2, Nano Banana 2.1, Seedream 4.5 and Seedream 5 family.

All new skills are **candidate** and cannot be auto-resolved. Current model API availability, resolution and reference limits must be checked at execution time. Sources were read as supporting curation; they do not establish measured image-generation success.

## Evidence and limitations

- Sources: `imagineVid/Awesome-nano-banana-prompts-and-skills`, `imagineVid/Awesome-seedream-5-pro-prompts-and-skills`, `kingbootoshi/nano-banana-2-skill`.
- Source coverage: public GitHub descriptions and docs checked; no copied external media/assets, no third-party prompt corpus redistribution.
- New candidates: 16/16 structurally valid.
- Registry totals: 43 entries; 14 active; 29 candidate (13 inherited, 16 new).
- Fail-closed: each of the 16 candidate skills must reject normal resolution; explicit candidate inspection must be non-selectable.
- Historic Seedance candidate remains unchanged.

## Actual checks performed

- `python3 scripts/generate.py --check`: 569/569 generated file parity.
- `python3 scripts/aco_cli.py skill-registry-check`: valid.
- `python3 scripts/aco_cli.py validate`: validated; privacy findings 0; historic skill benchmark 28/28 at 100.0/100.
- Full unit suite executed in four deterministic groups (timeout avoided): 134 + 217 + 234 + 30 = **615/615 passed**.
- New image-specific tests: 20 passed, within the 615 total.
- Fresh image-output benchmark: **not run**. No live output was generated on Nano Banana or Seedream, so no claims about photographic realism, identity retention or multi-reference fidelity are certified. Promotion requires frozen first-run benchmark, >=20 cases, >=95 score, zero critical failures, explicit approval and rollback ref.

## Release handling

This release makes candidate methods available for explicit evaluation, not production auto-activation. No GitHub push, account access or provider operation is part of this artifact build.
