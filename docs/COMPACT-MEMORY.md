# Compact Memory — fewer files, not less useful work

Version 0.5.1. Applies to artist practice, company/organization, client/commercial and product/project development, and every supporting office.

## What changes
ACO normally updates one existing ACO.md per independent owner/project. It no longer creates a permanent file per session, event, decision, lead, application, pitch, unaccepted artwork or handoff. Activities, clients and brands usually start as sections. A real requested proposal, code file, video, budget or application remains a deliverable and can still be saved.

An idea can stay in chat. Worth remembering? Add a pipeline row. Submitted, declined or abandoned? Update that row. Explicitly committed or evidenced real engagement? Mark active. Need independent work or confidential separation? Then a separate canonical document is eligible; activation does not force a folder.

## New local knowledge
From the full release folder (Python 3.11+):

```bash
python3 scripts/aco_cli.py workspace-init --knowledge "$HOME/ACO-private"
python3 scripts/aco_cli.py entity-add --knowledge "$HOME/ACO-private" --kind artist --key my-practice --name "My practice" --commitment existing_entity --approval-ref "My explicit setup request"
```

The first command creates only ACO-INDEX.md. The second adds one owner ACO.md. No empty Archive/History/Clients tree. The returned entity ID is used below; do not literally paste ARTIST_ID.

```bash
python3 scripts/aco_cli.py pipeline-upsert --knowledge "$HOME/ACO-private" --entity ARTIST_ID --key idea-one --kind idea --title "An idea to explore" --state exploring --summary "Not committed"
python3 scripts/aco_cli.py pipeline-upsert --knowledge "$HOME/ACO-private" --entity ARTIST_ID --key idea-one --kind idea --title "An idea to explore" --state rejected --summary "Not pursuing"
```

Both write the same row, with no new document/folder/entity. To reopen, update the state to exploring with the actual instruction; then promotion needs commitment and a source:

```bash
python3 scripts/aco_cli.py pipeline-promote --knowledge "$HOME/ACO-private" --entity ARTIST_ID --item PIPELINE_ID --commitment explicit_user --approval-ref "User decided to develop independently"
```

This only activates the row. To create an independent project document explicitly, additionally supply --materialize --key actual-project --name "Actual project" --reason "Independent committed body of work". Activities/clients/brands normally remain sections even when active. The local index contains logical IDs without demanding one file per ID.

## Default private files
Knowledge: one ACO-INDEX.md plus one ACO.md per independent owner/project. Local technical state: one state.json and lock outside the knowledge tree, a transient pending.json recovery journal and at most one rotating canonical recovery copy. Location defaults under ACO_HOME or ~/.local/share/aco/compact-state. It is private, never committed or synced to Drive automatically. Sessions are records inside that state file, not individual files.

A work-project uses one .agent-context/HANDOFF.md. Parallel sessions use separate worktrees. Do not export an entire company’s unrelated clients into a client session. The state registry supports multiple organizations, activities, clients, brands and projects with owner/relationship checks, but does not implement provider access control.

## Recent work and retention
Record only material durable facts. Keep approximately 10–20 recent work entries. At the limit the CLI requests a reviewed summary and preserves the pending item locally; it does not truncate old facts or create an archive. `compact-recent` requires the current full document SHA-256, approved summary and approval reference. Approved decisions and open loops are untouched. One rotating local backup is kept outside knowledge.

Pipeline rows can also be reviewed and summarized inside the same document through a guarded edit, preserving unresolved items and important rejected/reopening context. Do not invent a universal retention period for legal/financial records. An archive is exceptional and separately approved.

## Google Drive
This ZIP does NOT authenticate or modify Drive. The host must have actual read/write capabilities for the chosen account and root. Follow the [canonical Drive procedure](DRIVE-KNOWLEDGE.md): reuse provider IDs, reread current revision, update in place and verify the same document afterward. No per-session events, receipts or handoff documents on Drive.

A native Google Doc is fine instead of raw Markdown; do not create both. If the connector cannot safely guard competing edits, coordinate one writer or leave a pending in-chat patch. No bypass through another connector after denial. The `canonical_sync` Python contract has mock tests but no bundled Google adapter.

`--authority drive` labels a local staging mirror only. It cannot prove that mirror is current or sync it. Every local outcome explicitly says drive_verified=false. Fetch the current remote content before work; never upload a stale full mirror wholesale. The old drive-bind/drive-sync event bridge refuses default compact mode. Explicit legacy mode is compatibility only.

## Existing clutter is a separate operation
An upgrade changes future behavior, not your current Drive. Use [reviewed cleanup](CLEANUP.md). Preserve original deliverables, revisions, permissions and links. Consolidation must not merge independently shared or restricted HR/legal/finance records into broader-access context.

## Explicit in-place adoption of a reviewed existing local canonical document
After inspecting a legacy private snapshot, a known existing owner document may be adopted without creating a second owner folder. This is not automatic migration:

```bash
python3 scripts/aco_cli.py adopt-canonical --knowledge /absolute/private/snapshot --canonical Contexts/artist-context.md --kind artist --key my-practice --name "My practice" --base-sha256 ACTUAL_REVIEWED_FILE_HASH --approval-ref "Approval to adopt this exact owner document in place"
```

It preserves that narrative literally inside the managed Context section, keeps its current path, creates/updates one compact index and leaves other files untouched. It does not infer decisions, move old notes or delete a previous index alias. Existing ambiguous compact indices or managed markers cause a conflict. Review/consolidate other notes separately. For Drive use the host procedure with real document IDs and revisions; this local command does not modify Drive.
