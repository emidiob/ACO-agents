# CLI reference

Python 3.11+, macOS/Linux (WSL on Windows). All commands print JSON and exit nonzero on failure. Keep private knowledge outside Git. Use `--help` on each command.

## Installation
`doctor`; `validate`; `install [--offices none|all|<office...>] [--project PATH] [--apply] [--backup-modified]`; `install-status`; `install-recover`; `uninstall [--apply]`.

Global defaults are user's skills and Codex agents directories. `--home` is mainly for controlled tests; `--codex-home` overrides the agent destination. Honor the same options for update/uninstall/recover. Dry-run plans may create the private lock/state directory, but do not install skills or agents.

## Private workspace
```
python3 scripts/aco_cli.py workspace-init --knowledge /private/aco
python3 scripts/aco_cli.py entity-add --knowledge /private/aco --kind organization --key studio --name "Studio"
python3 scripts/aco_cli.py status --knowledge /private/aco
```

Use the returned organization ID with `--parent` to create an activity, client or project. `--links path/to/links.json` is supported for projects:
```
{"activity_ids": ["<existing-activity-id>"], "client_id": "<existing-client-id>"}
```
Values must be actual registered IDs. Keys are stable lowercase identifiers; names are display labels. Repeating an identical create is safe; changing data under an existing key requires review. `--authority drive` marks the local store as a snapshot/queue and blocks local canonical-context apply. It does not connect to Drive automatically.

## Session
```
python3 scripts/aco_cli.py session-start --knowledge /private/aco --entity <existing-project-id> --workspace /work/project --brief "Build the agreed homepage" --mode LIGHT
python3 scripts/aco_cli.py session-export --knowledge /private/aco --session <returned-session-id> --entities <allowed-entity-id>
python3 scripts/aco_cli.py checkpoint --knowledge /private/aco --session <returned-session-id> --event /private/event.json
python3 scripts/aco_cli.py session-close --knowledge /private/aco --session <returned-session-id>
```

Event example (place in a private directory, not the public repository):
```
{
  "id": "event-draft-one",
  "kind": "work",
  "status": "proposed",
  "summary": "Homepage wireframe drafted; not yet approved.",
  "artifacts": ["relative/path/to/wireframe.html"],
  "next_action": "Review the hierarchy before implementation."
}
```

For `executed` or `verified`, include actual evidence, e.g. an artifact hash or a test command with its observed exit status/output location. For an approved decision include `approval_ref` pointing to the user's actual message/record. A caller inventing evidence violates the workflow; the CLI validates required fields, not the truth of arbitrary strings.

## Context changes
`context-propose --entity ID --content FILE --base-sha256 HASH --rationale TEXT` creates a proposal. Get HASH from the current local Context.md; do not guess it. `context-apply --entity ID --proposal ID --approval-ref REF` checks the base again, preserves the old version and records a receipt. Stale proposals fail. No context replacement for Drive-authoritative stores.

## Repository migration
`migrate --target PATH` previews. `migrate --target PATH --apply` creates backup/work branches and stages exact managed file changes. It does not commit, push or modify Drive.

## Optional event bridge
`drive-bind --root-id ID --approval-ref REF` explicitly binds an accessible approved root and creates/reuses its ACO Session Events folder. `drive-sync [--session ID]` sends pending immutable event JSON and verifies read-back. A locally configured OAuth access token is required; see OPTIONAL-DRIVE-BRIDGE.md. No token is printed or stored.


## Intake, action planning, finance and production checks (0.4.0)

`intake --workflow KEY --facts JSON [--mode ACTION|DECISION|EXPLAIN]`: check an explicitly selected playbook's essential fields. Returns at most three early questions or brief_ready. It does not infer the correct playbook from arbitrary prose or execute work; the Concierge does that using the task.

`action-plan --request JSON [--capability JSON] [--authorization JSON] [--previous JSON]`: pure offline packet check. intent=draft always returns draft_only. execute requires declared connected/schema-verified exact action capability, matching account, verified target, action ID, scope/content and an approval reference bound to that action and payload fingerprint. Denial blocks; previous accepted/uncertain outcomes require reconciliation. These supplied fields do not prove real consent or authorization. The host must verify both and invoke its actual connector. This command never sends/calls/publishes.

`budget-check --input JSON`: one supplied currency, nonnegative integer/decimal-string quantity/rates, explicit overhead/contingency and optional net quote/target margin/supplied tax percentage. Computes cost and distinguishes margin from markup. No exchange rate or tax applicability inference; no payment.

`comfy-preflight --workflow API_JSON --object-info SNAPSHOT_JSON`: offline shape, registered node, required inputs, literal choices/basic bounds, links/types and cycle checks. UI JSON is rejected with guidance. Errors return process status 2. Dynamic node behavior, real model files, VRAM, rendering, licenses and visual quality are not validated. Synthetic examples exist only to test the checker.

The installed minimal runtime includes these helpers. Full installation, generation, validation and repository migration still require the complete release checkout.
