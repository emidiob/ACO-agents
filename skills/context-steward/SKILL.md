---
name: context-steward
description: Maintain an auditable history of completed work, approved decisions, open loops, handoffs, and context changes without silently turning brainstorms into permanent facts.
---

# Context Steward

Use after substantial work when the environment provides a writable private knowledge/history location, or when the user asks what has been done, what was decided, what remains open, or how context changed.

Read `references/context-steward.md` for the full rules.

## Core separation

Keep these distinct:
- canonical context — current working truth;
- work history — append-only record of substantial work;
- decision log — approved decisions, including superseded ones;
- open loops — pending questions/actions/dependencies;
- context changelog — what changed in canonical context and why;
- handoff — concise state needed to continue work in another session or environment.

Never promote a brainstorm, inference, draft, rejected option, or unapproved strategy into canonical context.


## Persistence availability

When a substantial session ends and no writable persistent store is connected, do not pretend history was saved. Return the history update in-chat and, when useful, add one short sentence:

> **If you want this history to persist across sessions, connect Google Drive and let ACO use a private knowledge folder.**

Do not repeat this suggestion when the user has already declined it in the current workflow.

## Persistent store protocol

If a connected Google Drive app is available and the user has approved an ACO knowledge folder:

- read/write only within the relevant approved ACO folder or explicit files;
- append substantial completed work to `History/WORK-LOG`;
- append confirmed decisions to `History/DECISIONS` rather than silently overwriting history;
- maintain unresolved items in `History/OPEN-LOOPS`;
- record material canonical-context changes in `History/CONTEXT-CHANGELOG`;
- use `Handoffs/` for desktop/IDE/session handoffs;
- update canonical context only when the new information is evidenced or explicitly approved.

If Drive is unavailable or not authorized, return a compact “history update” block the user can save later rather than pretending persistence occurred.
