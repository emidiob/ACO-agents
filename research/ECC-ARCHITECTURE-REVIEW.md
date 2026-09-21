# ECC architecture review — ACO v0.6.1

Reviewed 2026-09-20 against `affaan-m/ECC` at commit `9ac593b55cba44c8b20152a5c7f28d300a67ec7e`.

ACO did **not** import ECC's agent/skill library or runtime. The review used ECC as an architectural reference for five general patterns: progressive context retrieval, context-budget auditing, skill stocktakes, evidence-driven verification/evals, and scoped continuous learning. ACO implements original, domain-neutral versions suited to Art & Commerce Office and preserves Compact Memory rather than adopting a second memory vault.

ECC is MIT-licensed. Its repository and license remain third-party material; no ECC source file is distributed in ACO. See the repository directly for current ECC behavior and terms.

## Decisions
- Keep ACO's office/role taxonomy and 363 roles.
- Reduce repeated role boilerplate substantially; keep a small safety/scope bootstrap in each independently loadable role.
- Add shared protocols loaded on demand instead of repeating long contracts.
- Add side-effect-free context-budget / role-stocktake utilities and behavioral-eval definitions.
- Do not auto-learn from raw transcripts, do not add background hooks as a requirement, and do not replace Compact Memory with ECC Memory Vault.
