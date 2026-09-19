# ACO — Art & Commerce Office

ACO is a modular, context-first agent framework for creative and professional work across ChatGPT and Codex.

## Offices

- `office-concierge` — front door and cross-office router
- `artist-office` — contemporary artist practice and studio operations
- `organization-office` — cultural/research organizations
- `agency-office` — brand, creative, design, production, marketing, social
- `product-office` — websites, apps, software, AI, QA, infrastructure
- `legal-office` — legal research, contracts, rights, risk, and legal operations
- `recruitment-office` — candidate-side job search and career operations
- `context-steward` — work history, decisions, open loops, context changes, handoffs
- `context-setup` — private context templates and knowledge-base initialization

## Core architecture

```text
AGENT / SKILL = stable expertise
PRIVATE CONTEXT = who or what the work is for
BRIEF = the current task
HISTORY = what happened, what was decided, what remains open
```

The public plugin is generic. It contains **no private artist, company, client, career, legal, or project knowledge**.

## Optional private knowledge with Google Drive

ACO v0.2.1 is distributed publicly as a **skills-only plugin**. Google Drive is not bundled or republished by ACO.

If a user separately connects the official Google Drive app, ACO can use a user-approved private knowledge folder for continuity:

### What ACO tells the user

When persistent context would help and no knowledge source is connected, the Concierge can explain:

> **Want ACO to remember your projects, decisions, history, and context across sessions? Connect Google Drive and choose or create a private ACO knowledge folder. Or continue without persistent memory.**

Connecting Drive is optional. ACO remains fully usable without it, and installation of ACO never grants Drive access automatically.

```text
ACO — Art & Commerce Office/
  Contexts/
  History/
  Projects/
  Clients/
  Handoffs/
  Archive/
```

ACO should use only the minimum relevant files. If Drive is unavailable, it can work statelessly or from context supplied directly in the conversation.

See [`docs/DRIVE-KNOWLEDGE.md`](docs/DRIVE-KNOWLEDGE.md).

## IDE handoff

For work that moves from ChatGPT/Codex Desktop into VS Code, use a project-local temporary context layer:

```text
.agent-context/
  CURRENT-BRIEF.md
  RELEVANT-CONTEXT.md
  DECISIONS.md
  OPEN-LOOPS.md
  WORK-LOG.md
  CHANGES.md
  HANDOFF.md
```

At the end of substantial IDE work, record what changed and what remains open. The Context Steward can later promote durable updates back to the private knowledge source.

## Public plugin format

- portable manifest: `plugin.json`
- OpenAI compatibility manifest: `.codex-plugin/plugin.json`
- skills: `skills/<skill>/SKILL.md`
- optional local/repository marketplace metadata: `.agents/plugins/marketplace.json`

The repository contains no `.app.json` and no MCP dependency for the public v0.2.0 submission.

## Codex custom subagents

For Codex users who also want the original true custom-agent TOMLs, the repository includes them under `extras/codex-custom-agents/` with an optional installer:

```bash
./extras/install-codex-custom-agents.sh
```

## Public submission

See [`docs/PUBLIC-SUBMISSION.md`](docs/PUBLIC-SUBMISSION.md) for listing copy, starter prompts, and review test cases.

## Privacy and terms

- [Privacy](PRIVACY.md)
- [Terms](TERMS.md)
- [MIT License](LICENSE)

## Example prompts

```text
Use the Concierge. I want to plan my artistic practice for the next year and build a realistic revenue strategy.
```

```text
Use the Agency Office. Create a brand identity process for this client: research, strategy, creative routes, design system, production.
```

```text
Use the Product Office. Audit this codebase and propose a prioritized implementation plan.
```

```text
Use the Recruitment Office. Find roles that materially improve my career and keep an application history so we don't duplicate applications.
```
