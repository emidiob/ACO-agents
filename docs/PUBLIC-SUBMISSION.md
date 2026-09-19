# Public Plugin Submission — ACO v0.2.1

ACO is prepared as a **skills-only** public plugin.

## Listing

**Name:** ACO — Art & Commerce Office

**Short description:** A modular office of specialist AI workflows.

**Long description:** ACO routes natural-language requests across specialist offices for artistic practice, cultural organizations, creative agencies, product/software, legal workflows, and recruitment. It can work statelessly or use a private knowledge layer such as a connected Google Drive, while keeping public agent logic separate from private context and history.

**Category:** Productivity

**Website:** https://github.com/emidiob/ACO-agents

**Support:** https://github.com/emidiob/ACO-agents/issues

**Privacy:** https://github.com/emidiob/ACO-agents/blob/main/PRIVACY.md

**Terms:** https://github.com/emidiob/ACO-agents/blob/main/TERMS.md

## Important Google Drive note

Do not submit ACO as a plugin that references/repackages the existing Google Drive integration. The public ACO submission remains skills-only. Persistent knowledge workflows use Google Drive only when the user has independently connected and authorized that app.

## Suggested starter prompts

1. `Use the Concierge. Help me decide which ACO office should handle my request.`
2. `Use the Artist Office. Build a 12-month practice plan while protecting time for making new work.`
3. `Use the Agency Office. Turn this client brief into strategy, creative territories, production, and channel execution.`
4. `Use the Product Office. Plan and implement a website from requirements through QA and release.`
5. `Use the Recruitment Office. Build a job-search strategy and avoid duplicate applications.`

## Positive test cases

### P1 — Artist practice planning
**Prompt:** `Use the Concierge. I want to plan my artistic practice for the next year.`
**Expected:** Routes to Artist Office, asks only material questions, protects artistic development from being reduced to revenue/career optimization, produces a practical plan.

### P2 — Cross-office website
**Prompt:** `Use the Concierge. I need a website for my creative studio.`
**Expected:** Routes Agency + Product; Agency owns strategy/brand/experience, Product owns architecture/implementation/QA; asks for existing context only when useful.

### P3 — Legal contract review
**Prompt:** `Use the Legal Office. Review this contractor agreement from my side.`
**Expected:** Identifies jurisdiction/doc-version assumptions, reviews clauses and risks, distinguishes legal information from professional legal advice, flags points needing counsel.

### P4 — Drive-backed continuity
**Prompt:** `Use the Concierge with my ACO knowledge on Google Drive and continue the project we worked on last week.`
**Expected:** If Drive is connected, starts from the user-approved ACO folder/history, loads minimum relevant files, summarizes prior decisions/open loops before continuing. If Drive is not connected, asks to connect/provide context rather than claiming access.

### P5 — Recruitment pipeline
**Prompt:** `Use the Recruitment Office. Find suitable roles and do not duplicate applications already in my history.`
**Expected:** Uses career/job-search context and application history when available, researches current opportunities, tracks duplicates and next actions.

## Negative test cases

### N1 — Unnecessary private search
**Prompt:** `Use the Concierge. Give me three naming ideas for a fictional coffee shop.`
**Expected:** Does not search private Drive/context; performs the simple task directly or routes minimally.

### N2 — False persistence
**Prompt:** `Remember this forever even though no writable knowledge store is connected.`
**Expected:** Does not claim persistence; explains the limitation and can provide a compact context/history update for the user to save.

### N3 — Blind critique
**Prompt:** `Critique this artwork without using anything you know about me or my previous work.`
**Expected:** Uses NONE/BLIND context mode and does not load Artist Context before the critique.


## Optional Drive onboarding copy

ACO may tell users: **“Want ACO to remember your projects, decisions, history, and context across sessions? Connect Google Drive and choose or create a private ACO knowledge folder. Or continue without persistent memory.”**

This is optional guidance only. ACO does not bundle Google Drive and cannot access Drive unless the user independently connects/authorizes the Google Drive app.
