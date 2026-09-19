# Context Architecture

The agents in this repository are intentionally **generic**. Their expertise is stable; the identity of the artist, organization, client or project is supplied separately as mutable context.

## Three layers

1. **Agent** — stable role, expertise, methods, standards and decision rules.
2. **Context** — mutable information about the artist, organization, client or project.
3. **Brief** — the current task, deliverable, constraints and deadline.

## Context modes

- **NONE / BLIND** — do not load persistent context. Use for independent research, critique, benchmarking and alternative generation.
- **LIGHT** — load only mission/identity/current direction needed to orient the task.
- **FULL** — load the relevant context file(s) for continuity, operations, relationship management, production, sales or strategy.
- **BLIND-FIRST** — complete an independent first pass, then load context and perform a second contextualized pass.

## Rules

- Do not infer an artist or organization from prior work unless it is supplied in the current task or context.
- Treat context as versioned and revisable, especially strategy and positioning.
- Separate facts, decisions, hypotheses, preferences and open questions.
- Load the minimum context required.
- Never fabricate missing clients, projects, achievements, finances, relationships or credentials.
- For current claims, use live research when available and distinguish evidence from interpretation.

## Recommended project setup

Copy only the private context files you need into `contexts/private/` in your working project. The folder is git-ignored by default. Templates remain public.


Additional context templates now include `product-context` and `technical-context` for software/web/product work.

## History and canonical context

History is not canonical context. The framework keeps an append-only work log, decision log, open-loops list and context changelog under `contexts/private/history/` when used. `context_steward` may maintain those records automatically after substantial work, but provisional ideas must not be promoted into canonical context without clear evidence or user approval.

## Legal and career contexts
- `legal-context` stores recurring legal/entity/jurisdiction assumptions; matter-specific facts belong in `legal-matter-context`.
- `career-context` stores verified, relatively stable career facts and goals; `job-search-context` stores the active search thesis and changing pipeline assumptions.
- Application and legal-matter histories should remain auditable and append-only where practical; canonical context should stay concise.
