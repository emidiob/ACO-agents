# ACO v0.5.1 — local test report

Run date: 2026-09-20. Complete package based on the latest 363-role v0.5.0 specialist-upgrade source.

## Executed checks

**365 unittest tests passed** in the final development-tree run. No skipped tests were counted as passed. Command:

```bash
python3 -m unittest discover -s tests -v
```

The original suite is retained, including explicit legacy-memory/Drive-bridge compatibility tests. Default behavior is separately tested through the CLI and CompactMemory tests; old legacy tests do not imply the legacy layout remains default. Provider tests use simulated providers.

Static validation confirms 363 canonical roles/native profiles, 16 skills, 38 workflows and 40 registry entries. Generated role/TOML/runtime/category-card parity, relative Markdown links, release fingerprints and basic secret/private-path checks passed. These are not a complete security audit.

## Compact memory and clutter
- Fresh empty root: exactly one index; adding a real owner adds exactly one canonical document.
- 100 speculative/submitted pipeline items: no increase beyond the index and owner document, no project registry entities.
- Rejection/loss/parking: row updates, no archive or project creation.
- Missing commitment or approval reference prevents entity activation. An active row still creates no file unless independent materialization is explicitly requested.
- Small active clients/activities/brands remain sections; independent/confidential child records can use one document with a reason.
- Same-name clients across organizations stay distinct; cross-owner and mismatched brand/client links are rejected.
- One local handoff per worktree; concurrent/open handoff overwrite is blocked. Closed known handoff can be reused. Blind/cross-scope exports are blocked.
- Proposed decisions do not become approved history; actual execution/verification requires evidence fields. These fields are assertions from the caller, not a professional or consent certification.
- Repeated events are idempotent, including across local sessions after recent-work compaction.
- Recent-work limit requests a reviewed summary rather than truncating history or creating a new file. Approved decision section preserved.
- Existing owner narrative can be explicitly adopted in place with hash/approval checks and original content retained. Existing unrecognized indices/managed markers and stale edits block adoption. Other files stay untouched.

## Cleanup tests
Read-only inventory and preview, scope segregation, exact-plan approval, stale source/target guards, symlink/traversal rejection, protected records, verified external backup/quarantine, restore without overwriting newer work, idempotent replay and explicit empty-folder removal were tested.

Folders containing unrelated or unexpected files are never pruned. Approved old folders can be removed only after becoming empty solely from the explicitly approved quarantined notes/child folders. No permanent file deletion or real Drive mutation occurs in these tools. Semantic completeness of a supplied merged text remains a human/agent review responsibility.

## Resource tests
All 40 IDs are unique, role references and method paths resolve, source/activation statuses are explicit, and no entry claims it was installed or execution-tested by ACO. Default shortlist is at most three and unresolved entries are excluded unless requested for inspection. Missing/stale capability evidence, denied actions, unclear private-data route, missing transfer/voice/spend/license/source permissions block readiness as applicable. Plans never execute.

Source-review distribution: 33 source-reviewed, 4 partially reviewed, 3 unresolved identities. Review means public source/README/selected method inspection, not runtime, safety or legal certification. Exact unresolved entries: Image 23.js, Shepherd, Open Higgsfield AI.

## Canonical remote update contract
Simulated providers test read → expected revision → update same ID → read-back, conflict handling, scope checks, idempotent retry and rejection when atomic revision guards are unavailable. There is no bundled Google adapter/authentication for this contract and no live authenticated Drive test.

## Integration smoke tests executed in temporary local directories
- Fresh installation: 16 skills and 363 prefixed native profiles.
- Resource search from the actual installed minimal runtime resolved Continuity.
- Default workspace-init from installed runtime created only one compact index.
- Repeat install completed without needing replacement of unrelated files.
- Actual public v0.4.3 and latest v0.5.0 ZIPs were imported into temporary Git fixtures. Migration preview/application preserved HEAD/history, an unrelated tracked file and a synthetic private untracked note, then validated as v0.5.1.
- Installation upgrade from v0.4.3 to v0.5.1 produced 363 profiles.
- ACO LICENSE bytes are identical to the v0.5.0 baseline.
- Self-contained HTML catalogue has 40 entries, no external scripts, and its JavaScript passes Node syntax checking. No rendered/browser UI acceptance test was performed for that catalogue.

## Explicitly not executed or not claimed
No GitHub push, live Drive cleanup/migration/write, external account setup, scheduler creation, email/WhatsApp/SMS/call send, private-repository upload to a hosted service, package/model/font/asset installation, third-party dependency security audit, ComfyUI/GPU render, paid AI generation, full upstream test suite, or aesthetic quality benchmark.

This report certifies observed local test outcomes only. The actual host, credentials, tool versions, provider permissions and any external resource must be checked again before real use. Old installed/chat instructions must be refreshed; a GitHub upload alone does not activate v0.5.1 everywhere.
