# ACO Agents v1.0.1 — Release Test Report

## Scope
Incremental Seedance technical skillpack integration based on the ACO 1.0.0 baseline. This release registers 12 independently worded, attributed Seedance methods as **candidate** technical skills; none are promoted to active status. Upstream reference: https://github.com/LearnPrompt/awesome-seedance.

## Gates
- Historical unit tests: **578/578 pass**, deterministically split into blocks 489 + 59 + 30 after monolithic runner timeout.
- New v1.0.1 tests: **17/17 pass**.
- Total: **595/595 passed**.
- `generate.py --check`: **553 generated files verified**.
- Full CLI validation: **validated**.
- Registry: **27 technical skills** (14 active, 13 candidates; 12 new Seedance candidates).
- Canonical agents: **363**; entry skills: **16**; workflows: **61**; optional resources: **99**.
- Privacy scan: **0 findings**.
- Frozen v1.0 historical benchmarks and prior algorithm semantics preserved; registry extension validated against the SHA-256 digest of the original 15 entries.
- Old routing holdouts, context, scope, execution, autonomy, adaptation and token-economy gates remain active.

## Limitations
- No Seedance provider was called and no live generation was verified. Candidate registry inclusion does **not** certify model output quality.
- No GitHub push, tag, merge, or deployment has been made.
- The bundle is a full distributable release, not an automatically deployed update to ChatGPT.

## Activation policy
Promoting any candidate requires real generation evidence, benchmark (>=20 cases, >=95%, 0 critical failures), explicit approval, and rollback reference. Do not treat structural validation as model testing.
