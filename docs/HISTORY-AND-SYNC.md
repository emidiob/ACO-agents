# History and handoff — v0.5.1

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


# One local handoff, no permanent handoff archive by default

Use a separate work-project folder, not the public ACO checkout. Before writing, verify .agent-context/ is ignored and not already tracked.

```
<work-project>/.agent-context/HANDOFF.md
```

Include session/scope identifiers, ACO version, brief, minimum relevant source references/snapshots, decisions, actual files/tests, unresolved work and next action. Do not create SESSION.json, separate decisions/logs/changes or a directory per session. Detailed technical state stays in the single private local state store, not Drive.

One open session owns a worktree handoff. Concurrent sessions use separate worktrees, not a global current-client file. Never overwrite an unrecognized/active handoff. Closing a known session allows reuse of the same handoff path. Keep it until durable information has been verified in the existing canonical document; do not upload it as another permanent Drive file. Any removal of a user's existing handoff still needs appropriate authorization.

When switching client/organization, explicitly check scope. A new session does not erase previous chat knowledge; use a separate chat/runtime for confidentiality or truly blind evaluation.

Local tools do not infer completed work from unsaved actions and do not confirm Drive sync. Use the host's connected-tool canonical-document protocol for remote writes. The old event bridge is compatibility-only and disabled in compact mode.
