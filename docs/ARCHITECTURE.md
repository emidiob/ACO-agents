# ACO 0.3 architecture

## Source and generated representations
Canonical role methods: skills/<office>/references/agents/*.md, one per key. Shared roles are canonical in aco-office-concierge. Offices refer to a catalogue with exact paths; no duplicate Markdown copies of shared role methods.
Generated artifacts: catalog.json, native prefixed TOMLs, ACO-INDEX.md, template mirrors and a minimal installed runtime. generate.py --check detects drift. The release manifest hashes all shipped files except itself. It detects accidental change, not a malicious publisher replacement.

## Runtime distinctions
ChatGPT reads instructions with connected tools. Codex can additionally use native skills/subagents and shell. The Python CLI is a local utility, not an agent orchestrator/model service. The optional Drive REST bridge transfers explicit immutable events; connected host tools handle canonical context and generalized Drive workflows.

## Ownership and scope
An organization owns its activities and client relationships. A brand belongs to an organization or client. A project has one owner and explicit activity/client/brand links. An artist/career scope is personal and separate. IDs are stable and labels mutable. The local engine rejects cross-owner project links and wrong brand/client combinations.

## Persistence model
Registry and entity journals are private. Local writes are atomic under an OS file lock. An interrupted entity registration is recovered from its journal on init. Each session is isolated by ID and has explicit context source hashes. Events are immutable by ID; repeated identical records are idempotent; conflicting reuse fails. Entity-local sequence numbers order local history but are not distributed clocks.

Context edits are proposed against a base hash, explicitly approved and checked again before replacement. Old content is retained and a receipt/event records the outcome. Drive-authoritative workspaces refuse local canonical apply; use the host's connected revision-controlled write instead.

Remote setup is single-writer because Drive names are not unique and search/create is not atomic. Native Docs should use requiredRevisionId. With raw files or limited tools, use immutable proposals and serialized reconciliation rather than falsely promising atomic compare-and-swap.

## Failure design
Partial work is a valid state: local_verified, pending, conflict, not_saved. Unconfirmed remote writes never get a verified receipt. Setup uses exact IDs after creation and resumes journals. Installation preflights all destinations, preserves unmanaged files, backs up changed owned content, and journals rollback. Migration creates backup/work branches and never force-pushes.

## Non-goals
No plugin directory submission, no model/LLM API key requirement, no central collection of user data, no always-on scheduler, no promise of hard multi-tenant isolation from prompts, no global current client, no hidden auto-submissions or production deployment.
