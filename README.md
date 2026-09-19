# ACO — Art & Commerce Office

A modular, context-first agent framework for art, creative practice, commerce, professional work, and technical production across ChatGPT and Codex.

## What it includes

- `office-concierge` — front door and cross-office router
- `artist-office` — contemporary artist practice and studio operations
- `organization-office` — cultural/research organizations
- `agency-office` — brand, creative, design, production, marketing, social
- `product-office` — websites, apps, software, AI, QA, infrastructure
- `legal-office` — first-pass legal workflows and legal research
- `recruitment-office` — candidate-side job search and career operations
- `context-steward` — work history, decisions, open loops, context changes
- `context-setup` — private context templates

The plugin itself is generic. It does **not** include the creator's private artist/company/career/legal context.

## Architecture

```text
PLUGIN / SKILLS = reusable expertise + routing
PRIVATE CONTEXT = who/what the system is working for
BRIEF = the current task
HISTORY = what happened, what was decided, what remains open
```

Recommended deployment:

```text
GitHub = public plugin / skills / generic agents
Google Drive = private knowledge + history
Project .agent-context/ = temporary VS Code handoff
```

## ChatGPT / Codex plugin format

The root `plugin.json` is the portable Agent Plugins manifest. `.codex-plugin/plugin.json` is included as a compatibility fallback. The package is skills-only in v0.1.0; no MCP server is bundled yet.

## Private knowledge

Filled context should live outside this public plugin. The recommended source of truth is a private Google Drive folder such as `ACO — Art & Commerce Office/`, with separate `Contexts`, `History`, `Projects`, `Clients` and `Handoffs` folders. See [`docs/DRIVE-KNOWLEDGE.md`](docs/DRIVE-KNOWLEDGE.md).

The public GitHub repository contains only generic expertise, routing logic and empty templates. Never commit filled private context.

A private MCP server remains an optional future layer when direct structured read/write tools are needed beyond the connected Drive workflow.

Possible future MCP tools:

- `get_context(scope)`
- `get_work_history(scope)`
- `get_decisions(scope)`
- `get_open_loops(scope)`
- `append_work_log(entry)`
- `record_decision(entry)`
- `update_open_loop(entry)`
- `propose_context_update(change)`

This keeps public expertise separate from private memory.

## Codex custom subagents

The plugin skills work as workflow instructions in ChatGPT and Codex. For Codex users who also want the original true custom-agent TOMLs, they are bundled under `extras/codex-custom-agents/` with an optional installer:

```bash
./extras/install-codex-custom-agents.sh
```

## Test prompts

```text
Use the Concierge. I want to plan my artistic practice for the next year and build a realistic revenue strategy.
```

```text
Use the Agency Office. Create a brand identity process for this client; research first, then strategy, then creative routes, then design system.
```

```text
Use the Product Office. Audit this codebase, identify the biggest architecture and UX risks, and propose a prioritized implementation plan.
```

```text
Use the Recruitment Office. Find roles that materially improve my career and keep an application history so we don't duplicate applications.
```
