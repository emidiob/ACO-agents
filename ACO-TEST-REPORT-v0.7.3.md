# ACO v0.7.3 — Test & Release Report

Release: **0.7.3**  
Focus: **Exact Context Boundaries, Routing Hardening & Fresh Holdout Evidence**

## Release summary

ACO v0.7.3 completes and hardens the context/routing work that remained unsafe or insufficiently demonstrated in v0.7.2. It does not expand the office/role surface. The canonical shape remains:

- 363 roles / 363 native agent profiles
- 16 skills
- 61 workflows
- 99 optional resources
- 499 generated/derived files
- Compact Memory remains the default

## What changed

### 1. Exact cross-scope private-context authorization

v0.7.2 accepted a request-wide boolean, `cross_scope_authorized`, as sufficient permission to read `other_private_entity` context. That was too broad: one boolean could authorize more foreign private sources than intended.

v0.7.3 centralizes the boundary in `scripts/aco/scope.py` and requires exact scope matching:

- foreign private sources declare a `scope_id`;
- the request grants only explicit `authorized_private_scope_ids`;
- authorization is exact, not wildcard-based;
- `*` is rejected;
- private sources with `scope_relation: unknown` remain blocked;
- a missing foreign `scope_id` is blocked;
- the legacy `cross_scope_authorized: true` field is observed for compatibility but **does not grant access**;
- Context Engine and Hybrid Memory use the same boundary decision.

### 2. Routing boundary hardening

General routing guards were added for three ambiguous boundaries without adding agents:

- cross-client/private-context isolation → `shared/context_steward`;
- independent/self-initiated brand foundation work → `shared/brand_strategist` rather than Agency;
- genuine client campaign strategy retains Agency / `campaign_strategist` preference.

The previously problematic artist-residency routing remains covered as an Artist Office regression.

### 3. Fresh-holdout discipline

Two v0.7.3 holdouts are intentionally retained with different roles:

- **Holdout #4** was frozen before execution and failed its first run at **94.75/100** with **2 critical failures**. Routing was changed afterward, so #4 is permanently classified as **development regression only**. It now scores 100/100, but that post-fix score is not treated as fresh evidence.
- **Holdout #5** was created only after those fixes, checked for exact prompt overlap, frozen, hashed, then executed. Its **first run passed at 98.0/100 with 0 critical failures**. Routing semantics were frozen immediately afterward and are now checked by release validation.

## Final benchmark results

| Gate | Result | Cases | Critical failures | Notes |
|---|---:|---:|---:|---|
| Historical final routing holdout | 98.57/100 | 28 | 0 | Office 100%; top-3 100% |
| v0.7.2 fresh routing holdout #3 | 96.39/100 | 36 | 0 | Preserved regression gate |
| v0.7.3 development holdout #4, current | 100/100 | 40 | 0 | First run was 94.75 with 2 critical; not fresh evidence |
| **v0.7.3 final fresh holdout #5** | **98.0/100** | **40** | **0** | Office 100%; top-1 95%; top-3 100%; minimal team 100% |
| Context efficiency | 100/100 | 30 | 0 | Mean selection ratio 47.07% |
| **Exact scope-boundary adversarial benchmark** | **100/100** | **28** | **0** | 0 Drive prompts |
| Real-world regression | 100/100 | 120 | 0 | Mean context selection ratio 42.12%; 0 Drive prompts |
| Execution policy | 100/100 | 62 | 0 | Passed |
| Delegation behavior | 100/100 | 14 | 0 | Passed |
| Integration resolution | 100/100 | 12 | 0 | Passed |
| Behavioral simulation | 98.67/100 | 42 | 0 | Passed |
| Privacy / PII scan | Passed | — | 0 findings | Passed |

## Unit/integration test suite

All test modules were executed. Because a single monolithic invocation exceeded the host runner's command-duration limit without producing a failure, the same complete suite was rerun in deterministic module groups:

- Group 1: 115 tests — passed
- Group 2: 115 tests — passed
- Group 3: 135 tests — passed
- Group 4: 116 tests — passed
- Group 5: 52 tests — passed

**Total: 533 / 533 tests passed.**

The targeted v0.7.2 + v0.7.3 regression suite also passed **29 / 29** after fixtures were migrated to explicit foreign `scope_id` values.

## Freshness and anti-contamination evidence

Final holdout #5:

- 40 cases
- exact overlap with routing training examples: 0
- exact overlap with prior routing holdouts at freeze time: 0
- frozen file SHA-256: `fd45fe713f055af62421ebe3328261fd616804ee6618fb4b66059f01b098959a`
- first-run score: 98.0/100
- first-run critical failures: 0

Post-holdout release validation also checks frozen hashes for:

- `scripts/aco/routing.py`
- normalized `config/routing-hints.json`
- normalized `config/routing-examples.json`
- normalized `config/role-contracts.json`
- normalized `catalog.json`

This prevents silent routing tuning after the final fresh result.

## Compatibility note

For intentional cross-scope private retrieval, callers should migrate from the old broad boolean to explicit scope IDs:

```json
{
  "authorized_private_scope_ids": ["client-b"],
  "sources": [
    {
      "id": "related-history",
      "private": true,
      "scope_relation": "other_private_entity",
      "scope_id": "client-b"
    }
  ]
}
```

`cross_scope_authorized: true` alone no longer grants access. This is an intentional privacy-hardening behavior change.

## Validation status

The v0.7.3 release validator passed with:

- generated parity verified;
- release hashes verified;
- relative documentation links verified;
- role contracts and catalogue coverage verified;
- historical routing gates preserved;
- development holdout chronology verified;
- final fresh holdout hash and first-run evidence verified;
- routing semantic freeze verified;
- exact-scope boundary benchmark verified;
- 120-scenario real-world regression verified;
- execution, delegation and integration gates verified;
- privacy / PII gate verified.

## Limitations

Validation is local/static and does not claim professional certification. It does not execute live external provider actions. Exact scope authorization is an application/runtime policy boundary; it is not a cryptographic isolation mechanism.
