# Compact history and truthful status

Read COMPACT-MEMORY.md. Durable history is part of the existing scoped ACO.md, NOT per-session immutable files. Keep identity facts, proposals, approved decisions, work evidence and pending questions distinct inside that document.

During a session keep detailed transient notes in chat or one local .agent-context/HANDOFF.md. At a meaningful checkpoint write only what the next session needs: result, approved decision, changed status or unresolved dependency. Do not save every tool response or brainstorm. Use stable inline IDs for retry detection; different payloads with one ID are conflicts.

Status: proposed is not approved; approved needs actual authorization; executed needs an actual action/artifact; verified needs a real check. A draft email is not sent. A prepared prompt is not a render. Record sources and concise rationale, not hidden chain-of-thought.

Update the canonical file by its known provider ID and observed revision. Reread before write and verify afterward. If a response is lost, inspect the same ID before retrying. If another writer changed it, reconcile or leave a pending in-chat patch. Do not create another file to dodge a conflict.

Keep 10–20 meaningful recent-work entries, then request a reviewed concise summary inside the same document. Approved decisions, unresolved obligations, key sources and protected originals must survive. A periodic archive is exceptional and separately approved, never default. A declined opportunity just changes its pipeline row; it is not a new archive object.

LOCAL VERIFIED = local bytes exist and were checked, not Drive.
DRIVE VERIFIED = the actual remote canonical document was reread successfully.
PENDING = in-chat/local changes exist but no verified remote write.
CONFLICT = originals preserved; rebase or resolve ownership/sharing.
NOT SAVED = no durable authorized store.

Do not claim continuous monitoring, forever memory or scheduling from a skill. A real scheduler and scoped authorization are separate.
