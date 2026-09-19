# History, context and synchronization

Read the canonical HISTORY.md and HANDOFF.md protocols under the Concierge references.

Work record = immutable event with event/session/scope IDs and evidence. Canonical context = concise current information, updated only after approved reconciliation. Views such as Work Log and Open Loops are derived summaries, not the sole authoritative history.

Local CLI safeguards: fixed IDs prevent duplicate events; different data under an existing ID is a conflict; approved decisions need approval_ref; executed/verified states need evidence; open-loop events need loop_id. Evidence references are provided by the caller and are not independently cryptographically certified by the CLI.

`session-start` writes scope and ignores handoff paths before creating files. It refuses tracked private paths. `session-export` allows only the current entity, approved relationships and ancestors; BLIND/NONE stages reject exports. `checkpoint` records the event, creates an outbox item, and regenerates session views. `session-close` writes a recoverable handoff. It cannot infer unrecorded work when a user closes a window abruptly.

`context-propose` does not alter canonical context. `context-apply` requires the original base hash and explicit approval reference, preserves the previous version and emits a change receipt/event. With Drive authority, the CLI refuses local apply. Read/write the canonical source with connected tools and refresh the task snapshot afterwards.

The optional bridge journals a provider-generated file ID before uploading, retries the same ID, reads back payload bytes, and writes a local verified receipt only after a match. Duplicate remote names, different content, unavailable authorization and moved destinations fail without overwrite. This provides retry safety from one installation; it is not a distributed exactly-once transaction across independent devices. Concurrent same-event uploads must be detected/reconciled.

No scheduler, recurring task or continuous monitoring is installed. Never interpret a role description containing “monitor” as evidence that it is currently running. The user can configure a separate supported scheduler later, with bounded tasks and explicit permissions.
