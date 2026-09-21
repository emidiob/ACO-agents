# Compact memory — default in v0.5.1

## The gate before every persistent write
Use existing canonical knowledge before creating a file. A suggestion is not a project, a contacted prospect is not a client, an application is not an artwork, and a possible activity is not a business unit.

1. Is this just useful in this conversation? Leave it in chat.
2. Is it worth remembering but speculative? Update one pipeline row in the relevant existing ACO document. Do not register an entity or create a folder.
3. Has the user explicitly committed, has evidenced external acceptance activated the work, or is this an import of an existing real entity? It may be active. Keep small activities, clients, brands and projects as sections by default.
4. Does an active item need materially independent work, substantial context or a separate access boundary? Reuse its existing canonical document; otherwise create one ACO.md after that scope is clear.
5. Is the user asking for an actual deliverable, such as a proposal PDF, application, code, budget or treatment? Produce it when requested. Deliverables are not memory clutter and do not require an invented project hierarchy. Never suppress work the user asked for just to keep file count low.

All four working domains—artist practice, organizations/companies, agency/commercial clients, and product/project development—use this gate. Finance, HR, recruitment, publishing and other supporting offices inherit it. Entity activation and folder creation are separate decisions.

## Smallest durable layout
Create only the index initially. Add an owner document when that real owner is known and needs continuity. Example, NOT a scaffold to create wholesale:

```
ACO/
  ACO-INDEX.md
  Personal/Artist/<actual-owner>/ACO.md
  Organizations/<actual-organization>/ACO.md
  Projects/<committed-independent-project>/ACO.md
```

The root name is user-selected. Native Google Docs are also supported by the connected-tool procedure: one canonical provider ID per document, not both a Doc and an MD copy. IDs/paths belong only in private context. Activities, leads, clients and brands normally are named sections in their owner document. Separate confidential client, HR, legal or financial material into genuinely restricted locations when needed; fewer files must not broaden access.

Each ACO.md contains identity/context, current brief, compact pipeline, decisions, open loops, recent material work, next actions and references. Existing contracts, decks, proposals, footage, source code, scans and paid assets stay in their source location; retain a link and only the necessary summary.

## Lifecycle
Pipeline states: exploring, considering, draft, proposed, submitted, waiting, parked, rejected, lost, abandoned, active, completed. Submission, refusal and abandonment update a row. No folder, archive record or new registry object is created just for the status change.

Promotion requires a traceable explicit_user, external_confirmed or existing_entity reference. An agent recommendation or a positive response to brainstorming is not approval. A rejected/lost/abandoned item must be explicitly reopened before activation. An independent artistic commitment counts without institutional selection. External acceptance must identify the scope actually accepted; it is not authority to reorganize unrelated records.

## History without proliferation
Do not create a persistent file for a session, event, decision, task, candidate, rejected application or handoff. Add only material durable changes to the selected ACO.md. Use stable inline IDs for meaningful decisions/loops and preserve superseded decisions. Proposed decisions remain proposed.

Keep roughly 10–20 significant recent-work entries. When it grows, review a concise replacement summary; do not silently truncate or create a new quarterly archive by default. A separate archive is exceptional, justified by retention/volume and approved. Never compact away contractual obligations, financial records, unresolved actions, approved decisions or evidence links.

Technical state, locks, retries and receipts must stay in a bounded private local state store, outside Drive/knowledge/Git. The local compact backend uses one state JSON, one OS lock, a transient recovery journal and at most one rotating canonical recovery copy—not a file per session. It is not an always-on sync service.

## Existing clutter
Updating ACO does not authorize deletion. Read the selected root and canonical index, compare sources, detect duplicates, identify access boundaries, propose a precise consolidation, and get approval before moves/removals. Preserve originals and provider IDs until merged content and references are verified. Prefer reusing the existing canonical file ID. Ambiguous ownership, conflicting text, hidden content, revisions or sharing differences block automatic consolidation.

Local cleanup tools only act on an approved local snapshot and keep an external recovery batch. They cannot clean Google Drive. Connected Drive cleanup must use the actual authorized actions, a before-inventory and verifiable post-read. An unsupported/denied action is not a reason to try a workaround.
