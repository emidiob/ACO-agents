# History and verification protocol

History is not canonical context. Record work as immutable per-session events, then maintain readable projections. Never use a single shared global log as the only authoritative record.

## Required session fields
schema_version, id, aco_version, source revision when known, created_at, scope IDs, context_mode, goal/brief, context_sources with read date and revision/hash, status and capabilities available. Store private sources only in private memory. Pin context to this session; no global active client.

## Required event fields
id, session_id, scope, kind, status, summary, created_at and evidence. Optional: artifacts, exact tests and results, approval_ref, supersedes, loop_id, next_action. Accepted kind examples: work, proposal, decision, open_loop, context_change, verification, handoff, application, status.

Status semantics:
- proposed: an option/draft, not approved;
- approved: explicit user decision, reference required;
- executed: a real completed action, tool/artifact evidence required;
- verified: an actual check passed, check evidence required;
- rejected/superseded: preserve previous history;
- open/closed: open-loop lifecycle, stable loop_id required.

Do not infer decisions from silence, enthusiasm about a draft or an agent recommendation. Do not claim sent/submitted/deployed/paid from a draft. Write only a concise reasoning summary and results, never private chain-of-thought.

## Writes
Create one event file/document with its event ID in the name and payload. Check the target before retrying. If the same ID contains the same payload, reuse it. If content differs, conflict. Read back after writing and produce a receipt with provider file ID, event ID, payload checksum or verified exact content, scope and verified_at. Failed/unconfirmed writes stay pending in the private outbox.
Provider names alone are not idempotency; use stable IDs and content checks. If a write response is lost, search the exact event ID in the approved event location rather than creating a new random event.

WORK-LOG, DECISIONS, OPEN-LOOPS and CONTEXT-CHANGELOG are summaries derived from events. Only one writer refreshes a given shared summary at a time with revision checking; independent sessions can still add different event records. Canonical context updates require a proposal with base revision/hash and a user-approved change. Re-read before applying; stale proposals need reconciliation. Preserve a before-version and a receipt. An approval reference stored by an AI is provenance, not cryptographic proof of human approval.

## End-of-session status vocabulary
LOCAL VERIFIED — a local file exists and matches the record.
DRIVE VERIFIED — the remote write was read back successfully; provide reference.
PENDING — an update exists locally/in-chat but is not confirmed remotely.
CONFLICT — competing edits or ambiguous identity need reconciliation; originals preserved.
NOT SAVED — no writable store or write failed without a durable local queue.
Do not say “remembered forever”, “always synced” or “monitoring continuously”. Scheduled work requires a separate scheduler and permission.
