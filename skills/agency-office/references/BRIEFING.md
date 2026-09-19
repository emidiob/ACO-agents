# Briefing the Agency Office

You should normally brief the **job**, not manually choose agents.

## Minimal form

```text
Use the Agency Office.
Task: ...
Objective: ...
Deliverables: ...
Constraints: ...
```

The orchestrator will load the minimum relevant context, use junior/maker agents for research and execution, specialists for domain decisions, and directors only where senior judgment is necessary.

## Context behavior

- **Company context** — the agency's capabilities, positioning, economics and internal constraints.
- **Client context** — relationship, stakeholders, scope and known client facts.
- **Brand context** — brand strategy, identity, voice and locked brand decisions.
- **Project context** — status, deliverables, budget, approvals and dependencies.
- **Campaign context** — proposition, audience, channels, assets and measurement.
- **BLIND-FIRST** — use for independent research, benchmarking, critique or alternative generation before exposing agents to current internal assumptions.

## Example: brand identity

```text
Use the Agency Office.
Load client and brand context.
Create a complete identity for a new hospitality brand.
Start with research and strategy, then positioning, verbal identity and visual identity.
Develop three genuinely distinct territories before converging.
Do not jump directly to logo design.
```

Expected routing can include junior brand/design/copy research first, then senior strategy, then design direction and maker execution.

## Example: campaign

```text
Use the Agency Office.
Load company, client, brand and campaign context.
Create an integrated campaign for [product].
Audience: ...
Market: ...
Budget: ...
Channels: film, OOH, social and digital.
First identify the strategic problem and cultural opportunity, then develop three campaign platforms.
```

## Example: film

```text
Use the Agency Office.
Load client, brand and project context.
Develop a 45-second advertising film within a €40k production budget.
Deliver a creative treatment, narrative, visual language, casting direction, location logic, cinematography, production approach and postproduction plan.
```

## Example: pitch

```text
Use the Agency Office.
Load our company context and the prospective client context.
Research the client and category first.
Identify the actual business and cultural problem behind the brief.
Develop the strategic proposition, creative opportunity, scope, team, process, timeline and commercial structure, then turn it into a concise pitch-deck structure.
```

## Useful control phrases

```text
Do a blind first pass before loading brand/company context.
Use junior/research agents for the first pass, then senior review.
Do not escalate to a director unless a material decision is required.
Show me three genuinely different routes before converging.
Separate verified facts from assumptions and recommendations.
```
