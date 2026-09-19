---
name: context-setup
description: Create, initialize, or refresh private ACO context for an Artist, Company, Client, Brand, Project, Campaign, Product, Technical stack, Career, Job Search, or Legal matter.
---

# Context Setup

Use when the user wants to create, populate, update, review, or restructure the private context that powers ACO.

Choose the smallest relevant template(s) from `references/`. Keep stable facts separate from current strategy, preferences, hypotheses, and open questions. Do not invent missing facts. Avoid secrets and unnecessary sensitive personal data.


## User-facing onboarding

If no persistent knowledge source is available, ACO may say:

> **ACO can work without memory. If you want continuity across chats and Codex sessions, connect Google Drive and choose a private folder for ACO. ACO will only use the folder you approve.**

If Google Drive is connected, offer two choices instead of assuming one:
1. use an existing user-selected knowledge folder; or
2. create a new folder named `ACO — Art & Commerce Office`.

Do not search or reorganize unrelated Drive content as part of setup.

## Recommended Google Drive layout

When the user wants persistent knowledge and a connected Google Drive app is available, initialize or use a user-approved folder:

```text
ACO — Art & Commerce Office/
  Contexts/
  History/
  Projects/
  Clients/
  Handoffs/
  Archive/
```

Use the templates in this skill to create the minimum necessary context files. Do not create or modify Drive content without the user's authorization and the permissions required by the connected app.

The public plugin ships templates only. Filled private context belongs in a user-controlled private store and should never be committed to the public ACO repository.
