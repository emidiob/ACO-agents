# Local runtime and host actions

Python 3.11+ local tools implement installation, scoped compact memory, checks and reviewed consolidation. No model/server, scheduler, credentials or live tool connections are included. ChatGPT can read Markdown without executing these tools.

Source: python3 scripts/aco_cli.py --help.
Installed skill: python3 <skills-root>/aco-office-concierge/runtime/scripts/aco_cli.py --help.

Default workspace-init/session/entity commands use CompactMemory. It creates only an index plus actual canonical ACO.md documents, with one private external state store and one worktree HANDOFF.md. Events and context proposals are not individual persistent files. Use --legacy-memory only when deliberately maintaining a pre-0.5.1 layout; never auto-fallback.

A local Drive-authority workspace is merely a staged mirror. Its writes always say local_verified and drive_verified=false. The host must reread the actual remote source before continuation and apply a verified guarded canonical update. The included canonical_sync contract needs a provider that atomically enforces revisions; no Google adapter is bundled for it. Local locks do not lock a Drive sync client or another machine.

resource-search selects optional candidates; resource-plan checks caller-supplied requirements, permissions and freshness. Neither installs nor executes tools. tidy tools operate only on local authorized snapshots, keep an external recovery batch and never permanently delete files. See the beginner guide and compact-memory manual for exact commands.


## v0.7 execution layer
`execution-plan`, `permission-check`, `receipt-check`, `adapter-check`, `workflow-check`, `execution-summary` and `execution-benchmark` are offline/read-only decision and validation tools. They do not send, publish, pay, sign, delete, deploy or connect a service. Actual adapter invocation belongs to the host and must return evidence suitable for the receipt contract.
