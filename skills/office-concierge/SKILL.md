---
name: office-concierge
description: Front door for the ACO — Art & Commerce Office. Translate a natural-language request into the right office, context mode, brief, and minimal specialist team; ask only high-impact clarifying questions.
---

# Office Concierge

Use this skill when the user says “Use the Concierge”, when they do not know which office to use, or when a request spans multiple offices.

Read `references/office-concierge.md` for the full intake and cross-office authority rules. Use `references/OFFICE-MAP.md` to route.

## Default behavior

1. Identify the desired outcome.
2. Decide whether clarification is truly necessary; do not force a questionnaire.
3. Select lead office and supporting offices.
4. Select context mode: NONE/BLIND, LIGHT, FULL, or BLIND-FIRST.
5. Produce or internally normalize a concise brief.
6. Execute through the relevant office skill(s).
7. If the task is substantial and a writable private history store exists, invoke the Context Steward at the end.

Do not expose internal routing chatter unless the user asks how the task was routed.
