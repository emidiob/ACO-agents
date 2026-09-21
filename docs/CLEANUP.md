# Reviewed cleanup — no blanket deletion

Two separate jobs: **stop new clutter** with Compact Memory, then **consolidate existing notes** only after inspecting them. A rejected proposal folder can still contain valuable original work; neither its name nor byte equality authorizes deletion.

## In ChatGPT with writable Drive tools
Ask: "Use ACO Compact Memory. Inspect only my approved ACO root. Show a consolidation plan; do not move, delete, share or rewrite anything yet."

ACO reads actual file IDs, content, versions and access boundaries; identifies candidate canonical records and old generated notes; and proposes exact retained/merged/moved items. After approval it updates the existing canonical ID where possible, rereads the result, repairs only approved references and verifies before moving old notes to a single reviewed archive/quarantine batch. Permanent trash/deletion is a separate explicit action. No new file per decision, cleanup check or session. If capabilities fail or are denied, leave the operation pending and do not use an alternate route to bypass it.

Never infer empty native Docs from a metadata size alone; fetch content. Never delete an original contract, invoice, application deliverable, proposal deck, source artwork, clip or project code to meet a file quota. Ambiguous owners, differing permissions and uncertain merges remain untouched.

## Local snapshot tools
These commands work on a specifically approved local private snapshot OUTSIDE Git. They do not operate the Drive API and do not guarantee coordination with a Drive sync client. Do not run them against a live concurrently synced shared folder; use an isolated export and separately review remote actions.

```bash
python3 scripts/aco_cli.py tidy-inventory --root /absolute/private/snapshot
python3 scripts/aco_cli.py tidy-plan --root /absolute/private/snapshot --spec /absolute/private/cleanup-spec.json
```

Inventory is read-only. Plan requires a reviewed merged text, exact source SHA-256 hashes, owner/access scope and current canonical target hash. The example in `examples/compact/cleanup-spec.TEMPLATE.json` is deliberately not ready to apply. Source classification and semantic completeness require human/agent review; these tools do not understand all private obligations.

Save the returned `plan` JSON in your PRIVATE local working area, not the public repository or as a new Drive memory record. Then approve its exact plan ID:

```bash
python3 scripts/aco_cli.py tidy-apply --root /absolute/private/snapshot --plan /absolute/private/reviewed-plan.json --recovery-root /absolute/private/recovery-outside-snapshot --approval-ref "Approval of the exact reviewed plan" --approved-plan-id EXACT_PLAN_ID
```

This creates one recovery batch outside knowledge: a verified before.zip, one receipt and (only when expressly requested) quarantined originals. It updates the canonical target, then moves only the approved note files. Only exact approved folders that are empty now or become empty solely from the approved quarantined notes and explicitly included child folders are removed. They are rechecked before every removal. Files are not permanently deleted. A stale source/target or changed directory stops the operation. A mid-operation failure can leave partial changes, but the backup and receipt remain for review; it is not a cloud transaction.

Restore source notes without overwriting later edits:

```bash
python3 scripts/aco_cli.py tidy-restore --receipt /absolute/private/recovery/PLAN_ID/receipt.json --approval-ref "Restore the approved batch"
```

`--rollback-target` can restore a previously existing canonical target only when it has not changed since the plan; a newly created canonical file is preserved rather than silently deleted. Recovery files stay until you explicitly decide retention. No automatic purge or recurrence.
