# Compact setup — repeatable and lazy

Read COMPACT-MEMORY.md before any write. The former per-session/event folder tree is legacy and must not be initialized by default.

1. Check actual account, read/create/update capabilities and user-approved root. If unavailable, work in chat and say NOT SAVED; do not create another root or claim access.
2. Read the root's direct children and known index IDs; paginate fully when needed. Search is not proof of absence. Existing uncertain/duplicate indices need reconciliation, not a fresh hierarchy.
3. New empty root: create only one ACO-INDEX document. Do not create Personal/Organizations/Archive or placeholders before needed. Existing root: reuse verified canonical IDs; preserve its content.
4. Read the real owner scope. Create a single owner ACO.md only for an authorized existing/committed practice, career or organization that needs continuity. No example companies or clients.
5. Add speculative items as rows in that owner document only when worth remembering. Actual small activities/clients/brands can remain sections with stable logical IDs; IDs do not mandate folders.
6. Separate active project/client documents only for real independence, complexity or confidentiality. Record links rather than copying the same project under multiple business activities.
7. After each create/update, read back the exact ID and verify content. Hold incomplete setup state in the existing index/private local state; never create a journal file per operation on Drive.
8. Resume by saved IDs and exact parent/metadata lookup. A lost response requires read/reconciliation, not another random-name create.

Drive folder names are not unique; a search-then-create is not a distributed lock. Use one setup writer. For ordinary canonical updates use provider revision guards; otherwise coordinate a single writer, reread immediately and never claim race-proof writes. When safe concurrent writing cannot be guaranteed, return an in-chat pending patch instead of overwriting or creating a proposal document.

Local CLI: workspace-init uses CompactMemory schema 2 by default. A nonempty old layout is deliberately refused pending a reviewed migration. --legacy-memory is explicit compatibility only and is never the automatic fallback. No local command reports a Drive write from a local mirror.
