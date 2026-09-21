# ACO CLI — v0.6.2

Python 3.11+, macOS/Linux or Windows through WSL. Run `python3 scripts/aco_cli.py COMMAND --help`. Outputs are JSON. Keep private inputs outside the ACO source checkout. Source commands and installed minimal runtime are distinct; install/migrate/generate/validate need the full release.

## Install, update and repository migration
- `doctor`, `validate`, `install-status`, `install-recover`.
- `install [--offices all|none|OFFICE ...] [--project EXISTING_PATH] [--apply] [--backup-modified]`; default preview. All 16 skills, optional native profiles. No external resources installed.
- `uninstall [--apply]`: reviewed ACO-owned files only.
- `migrate --target EXISTING_REPO [--apply]`: preview; apply creates backup/work branches and stages only known ACO file changes. No commit, push or Drive changes.

## Compact memory — default
- `workspace-init --knowledge PATH [--authority local|drive]`: create/reuse one index, reject unknown nonempty legacy roots.
- `entity-add --knowledge PATH --kind KIND --key KEY --name NAME --commitment explicit_user|external_confirmed|existing_entity --approval-ref REF [--parent ID] [--links PRIVATE_JSON] [--separate --reason REASON]`.
- `pipeline-upsert --entity OWNER_ID --key KEY --kind idea|application|lead|... --title TITLE [--state STATE] [--summary TEXT] [--next-action TEXT] [--source REF] [--base-sha256 HASH]`: update one row, no new entity/file.
- `pipeline-promote --entity OWNER_ID --item ROW_ID --commitment ... --approval-ref ... [--materialize --key KEY --name NAME --kind project --reason REASON]`: activate inline by default.
- `session-start --entity ID --workspace EXISTING_PATH --brief TEXT [--mode LIGHT|FULL|NONE|BLIND|BLIND-FIRST] [--relationships PRIVATE_JSON]`: one ignored handoff per worktree.
- `session-export --session ID --entities ALLOWED_ID ...`: minimum explicit scope, blocked for blind sessions.
- `checkpoint --session ID --event PRIVATE_JSON`; `session-close --session ID`.
- `context-propose --entity ID --content PRIVATE_FILE --base-sha256 CURRENT_DOCUMENT_HASH --rationale TEXT`: private local proposal, no new knowledge file.
- `context-apply --entity ID --proposal ID --approval-ref REF`: guarded section update.
- `compact-recent --entity ID --summary TEXT --base-sha256 HASH --approval-ref REF`: reviewed summary, preserves decisions, one rotating local recovery copy.
- `status --knowledge PATH`: reports layout and actual local state, never fabricated Drive verification.

All memory commands accept --knowledge PATH. The local compact state is outside it. `--authority drive` marks a staging mirror, not a connection; refresh from actual remote content before use. No local result claims a remote write. `--legacy-memory` is deliberate schema-1 compatibility, never default or automatic fallback. `drive-bind`/`drive-sync` are blocked without that opt-in; use the compact host procedure instead.

Checkpoint JSON:
```
{"id":"stable-event-id","kind":"work","state":"executed","summary":"Verified artifact saved","evidence":["actual artifact/tool reference"]}
```
Proposed decisions remain local until actually approved. Executed/verified needs evidence; an approved decision needs approval_ref. `status` is accepted as an old alias for state; conflicting values fail. The tool checks structure and references, not whether invented evidence is true.

## Optional resource selection
`resource-search --query TEXT [--role ROLE_KEY] [--limit 3] [--include-unresolved]`.
`resource-plan --request PRIVATE_JSON [--inventory PRIVATE_JSON] [--as-of YYYY-MM-DD]`.
`storage-plan --input PRIVATE_JSON`.
No external actions occur in these commands. See [resource registry](RESOURCE-REGISTRY.md).

## Reviewed local cleanup
`tidy-inventory --root PATH`; `tidy-plan --root PATH --spec PRIVATE_JSON`; `tidy-apply --root PATH --plan PRIVATE_JSON --recovery-root EXTERNAL_PRIVATE_PATH --approved-plan-id ID --approval-ref REF`; `tidy-restore --receipt PRIVATE_PATH --approval-ref REF [--rollback-target]`.
Read [cleanup](CLEANUP.md) first. No permanent file deletion or Drive API calls. Plans require reviewed content/scope and exact source/target hashes. Inspect actual receipts after errors.

## Existing specialist helpers
`intake --workflow KEY --facts JSON [--mode ACTION|DECISION|EXPLAIN]`; `action-plan --request JSON [--capability JSON] [--authorization JSON] [--previous JSON]`; `budget-check --input JSON`; `comfy-preflight --workflow API_JSON --object-info SNAPSHOT_JSON`; `web-contract-check --input JSON`; `shot-plan-check --input JSON`; `video-prompt-draft --input JSON --capability JSON [--as-of DATE]`; `evidence-check --input JSON --evidence-root PATH`.
These inspect supplied contracts, arithmetic, prompts/graphs and evidence integrity, not actual renders, deployments, visual quality, professional certification or real recipient authorization. Invalid specialist contracts exit nonzero. Source/installed runtime includes the helpers; external apps remain separately configured.

`adopt-canonical --knowledge PATH --canonical EXISTING_RELATIVE_DOCUMENT --kind artist|career|organization --key KEY --name NAME --base-sha256 HASH --approval-ref REF [--authority local|drive]` is an explicit in-place adoption of a reviewed existing local owner narrative. It preserves other files, does not infer approvals from old text, and is not a cloud migration. See COMPACT-MEMORY.md.

## ACO readiness checks

`capability-audit` checks local command presence without executing anything. `practice-check`, `opportunity-check`, `brand-check` and `social-check` accept `--input FILE`; opportunity/social also accept an optional timezone-aware `--as-of` for repeatable tests. No network or persistent writes. See [input contracts and examples](STUDIO-CHECKS.md). A returned `ready_for_review` is not action authorization or a professional judgement.


## Architecture and behavior maintenance

- `context-budget [--root PATH]`: read-only static audit of canonical role/skill/protocol sizes. Token estimates are rough budgeting signals, not runtime telemetry or billing.
- `role-stocktake [--root PATH]`: read-only scan for legacy duplicated contracts, unusually heavy roles and missing deliverable/evidence cues. It never merges or deletes.
- `eval-lint [--input FILE]`: validates the behavioral-eval schema only; no model is run.
- `eval-show [--input FILE] [--office OFFICE]`: prints the selected eval cases and comparison instructions for baseline/candidate testing.

Use these during ACO development or regression review, not as mandatory ceremony for ordinary work. See [EVALS.md](EVALS.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Quality & routing — 0.6.2

- `route-suggest --prompt TEXT [--max-roles 1..3]`: proposes an office and compact role team. Advisory only; it never authorizes actions or expands context.
- `route-benchmark --input FILE [--split NAME]`: scores a deterministic routing case set. The packaged final holdout is `config/routing-final-holdout.json`.
- `role-contract --role ROLE`: returns the generated structured contract for one canonical role.
- `role-overlap [--threshold FLOAT] [--limit N]`: surfaces review candidates; read-only, never merges/retires roles.
- `handoff-check --input FILE`: validates a compact handoff packet. `checked`/`reviewed` states require evidence.
- `capability-resolve --request FILE --inventory FILE`: separates missing, unavailable, available-not-authorized, authorized-unverified and ready capabilities. It executes nothing.
- `eval-score --input FILE`: scores an already-reviewed structured simulation file. It does not run an LLM or turn self-review into an independent benchmark.

Release routing and simulation gates are also checked by `validate`. See [EVALS.md](EVALS.md).

## Execution & Integration — v0.7.0

These commands are local validators/planners. **None invokes an external provider.**

```bash
python3 scripts/aco_cli.py execution-plan --request request.json --inventory inventory.json --approval approval.json
python3 scripts/aco_cli.py permission-check --request request.json --approval approval.json
python3 scripts/aco_cli.py receipt-check --input receipt.json
python3 scripts/aco_cli.py adapter-check --input adapters.json
python3 scripts/aco_cli.py workflow-check --input workflow.json
python3 scripts/aco_cli.py execution-summary --input execution-record.json
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
```

`execution-plan` returns `ready_to_execute`, `fallback_required`, `reconcile_required` or `already_executed`; even `ready_to_execute` means only that policy/capability evidence is sufficient for the host to consider the action. The host still performs the actual action and must capture a receipt.
