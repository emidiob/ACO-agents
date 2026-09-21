# One local handoff, no permanent handoff archive by default

Use a separate work-project folder, not the public ACO checkout. Before writing, verify .agent-context/ is ignored and not already tracked.

```
<work-project>/.agent-context/HANDOFF.md
```

Include session/scope identifiers, ACO version, brief, minimum relevant source references/snapshots, decisions, actual files/tests, unresolved work and next action. Do not create SESSION.json, separate decisions/logs/changes or a directory per session. Detailed technical state stays in the single private local state store, not Drive.

One open session owns a worktree handoff. Concurrent sessions use separate worktrees, not a global current-client file. Never overwrite an unrecognized/active handoff. Closing a known session allows reuse of the same handoff path. Keep it until durable information has been verified in the existing canonical document; do not upload it as another permanent Drive file. Any removal of a user's existing handoff still needs appropriate authorization.

When switching client/organization, explicitly check scope. A new session does not erase previous chat knowledge; use a separate chat/runtime for confidentiality or truly blind evaluation.

Local tools do not infer completed work from unsaved actions and do not confirm Drive sync. Use the host's connected-tool canonical-document protocol for remote writes. The old event bridge is compatibility-only and disabled in compact mode.
