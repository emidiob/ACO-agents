# Hybrid Memory: durable knowledge, current source, rebuildable intelligence

ACO uses different stores for different kinds of truth. It does not copy everything into Drive and it does not make a code index the authority for business/project decisions.

## Memory classes

1. **Durable semantic context** — confirmed project, practice, organization, client and decision context. Keep compactly in the existing canonical ACO document when a persistent store is already available and the change is materially useful.
2. **Code architecture summary** — a small durable summary may live in the same canonical ACO document when architecture/constraints materially change. The current repository remains the source of truth.
3. **Code structure/intelligence** — symbols, ASTs, call graphs, dependency relationships and embeddings belong in a local/rebuildable index or an authorized code-intelligence service. Do not copy them into Drive.
4. **Research corpus** — use the appropriate research system (for example Zotero/Tropy or supplied files) when available; do not mirror a full corpus into Drive by default.
5. **Task context** — current chat/worktree handoff; temporary and local.
6. **Execution receipts** — bounded operational evidence. Persist only the reference/outcome needed for continuity; do not create a permanent file per action.
7. **Tool/runtime state** — local/ephemeral. Re-discover it; do not treat it as durable user knowledge.

## No Drive nagging

Do **not** interrupt work to invite the user to connect or use Drive merely because persistence could be useful. Start and complete the task with available context.

If an already-authorized persistent store is available and the task materially benefits from continuity, use the existing canonical record under Compact Memory. If it is unavailable, continue without persistence.

Mention the missing persistence capability only when:
- the user explicitly asked to save/update Drive or another durable store; or
- a material durable update remains pending and that status is necessary to report accurately at completion.

Never make Drive setup a prerequisite for a task that can be completed without it.

## Code workflow

For a code task:
1. read repository instructions and the closest relevant source;
2. use an available code-intelligence index only when it materially reduces retrieval cost;
3. verify important architecture claims against the current repository/commit;
4. make/test the change;
5. refresh or invalidate the local code index if needed;
6. update the existing durable architecture summary only if a materially important decision/constraint changed.

A stored architecture note should carry provenance when useful: repository, verified commit/revision and last-checked date. If HEAD has moved materially, verify before relying on the note.

## Storage rule

Drive/canonical knowledge stores **meaningful human continuity**. Git/source control stores **the actual code**. Local code intelligence stores **rebuildable technical structure**. ACO routes between them.
