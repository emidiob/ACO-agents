# Google Drive — compact canonical-document protocol

ACO remains a skill library, not a Google app or synchronization daemon. The user connects Drive separately in the host. Verify the actual tools and account in this session; do not assume that connected means writable.

Read [Compact Memory](COMPACT-MEMORY.md) before write and [cleanup](CLEANUP.md) before consolidation. Default: one canonical index and one ACO.md/native Doc for genuinely independent real owners/projects. Activities, brands, small clients and speculative items remain sections/rows. No file per session, decision, event, proposal, rejection or handoff. Actual requested deliverables stay legitimate files.

## Execution protocol for the host
1. Use the user-approved root and known canonical ID. Paginate discovery when necessary. If several plausible files exist, inspect and reconcile; do not choose merely by newest title or create another index.
2. Read current content, provider revision and access/owner boundary. Identify a minimal change, preserve unrelated sections, decisions, open obligations and source links. A local cached mirror is not current remote evidence.
3. For low-risk ordinary updates within explicit ongoing authority, do not ask repeatedly. Strategic identity changes, merges, moves, deletions, sharing and external communications need their applicable approval. A suggestion is not a committed project.
4. Use an actual provider revision guard where exposed. Native Google Docs may expose revision-controlled edits, but do not assume this is available for raw Markdown in every connector. If safe competing edits cannot be guarded, coordinate one writer or return a pending in-chat patch instead of blindly replacing the file.
5. Read back the same file ID and verify intended text. Report DRIVE VERIFIED only then. A lost response is reconciled against this ID, not retried as a new create.
6. Update the existing index only when a real independent canonical document/reference changed. Do not write a new Drive receipt document. Keep technical retry state in one local private record or the private session.

A first setup creates only missing necessary records, never a full set of placeholder folders. A discovered client/idea/lead is not permission to promote it. An actual small active project can remain an inline section.

## Offline tooling
`canonical_sync.py` defines a small provider-neutral read/guarded-update/read-back contract and is tested with a simulated provider. It has no bundled Google authentication or live connector adapter. A host can apply the same protocol with its authorized tools. Source CLI drive-bind/drive-sync defaults are blocked in compact mode; old event uploads require explicit legacy mode and are not recommended for this layout.

Folders, metadata and prompt scopes do not enforce confidentiality by themselves. Preserve provider permissions and separate restricted records. Never place private IDs or knowledge in public GitHub.
