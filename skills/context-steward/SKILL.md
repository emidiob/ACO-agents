---
name: context-steward
description: Maintain an auditable history of completed work, approved decisions, open loops, and context changes without silently turning brainstorms into permanent facts.
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
- context changelog — what changed in canonical context and why.

Never promote a brainstorm, inference, draft, rejected option, or unapproved strategy into canonical context.
