# Drive-backed knowledge without a plugin

The canonical executable instruction for the host is `skills/aco-office-concierge/references/protocols/BOOTSTRAP.md`. ACO can direct available connected Drive tools to create, read and update within a user-approved root during an authorized session. It does not install or authenticate the Drive connection itself.

Use one root registry and index identified by provider ID, not by display name alone. Store context narrative in native Docs or supported Markdown; record its actual MIME type, ID and revision/hash. Keep immutable session/event documents and read-back receipts under the owning entity's history. Read only the task's scope.

If the connector supports native Docs revision control, read a fresh revision and write using requiredRevisionId. A rejected/stale revision becomes a conflict. Raw files without conditional writes must be serialized or kept as immutable proposals. There is no distributed lock or uniqueness guarantee from naming a folder.

### Bootstrap
After user authorization: inspect root and children, recognize existing version, journal planned objects, create/reuse missing base objects, verify each provider result, register returned IDs, then create only requested entity scopes and their base histories. Re-run should preserve user content and resume after errors. Unknown or duplicate records require review, not overwrite.

### Several users
Each user supplies their own authorized root. Nothing in the public repository points to a maintainer's private Drive. Teams needing actual access separation must configure provider permissions or separate roots/projects, not rely on a scope tag. Never share the root publicly to make an integration work.

### Existing data
Inventory files and ownership, preserve their IDs and content, move only clearly classified documents, and record old/new parents. Keep unknown legal/client records in a review/archive location until resolved. Do not delete old content because a new template exists. An empty duplicate index may be archived after verification; choose one canonical index and mark the other as legacy.

### Handoff
Drive remains the canonical source when configured as authority. Export a minimal per-session snapshot for IDE work; record where it came from. Local checkpoints form a pending outbox. A later steward pass reads and reconciles the changes through connected tools. The optional REST bridge can transfer immutable events, but does not replace this canonical-context reconciliation.
