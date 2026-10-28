---
name: aco-webdesign
description: "Design, build and redesign websites and product interfaces with original ACO art direction, searchable design recipes, reusable tokens, functional states and browser verification."
---

# ACO Webdesign

Use `/aco-webdesign` in Claude Code, `$aco-webdesign` in Codex, or `aco webdesign <task>` through Concierge. This is a native, independently installable ACO skill. It contains its own methods; external agent skills are not runtime dependencies. Inspect the existing project before choosing libraries or changing its design system.

## Choose the needed work

| Request | Method |
|---|---|
| Direction, reference interpretation, new visual identity | [Direction](references/direction.md) |
| Tokens, typography, colors, components, consistency | [Design system](references/system.md) |
| Build a page, product UI, responsive prototype | [Implementation](references/build.md) |
| Redesign, simplify, strengthen, refine an existing interface | [Revision](references/redesign.md) |
| Audit, accessibility, interaction, performance, visual review | [Verification](references/review.md) |
| Select components, motion libraries or a stack | [Libraries](references/libraries.md) |

These are natural-language operations, not additional registered commands. For a scoped tweak, change and verify that tweak without forcing a full redesign. For a substantive build, establish the page's job, a brief-specific visual decision, realistic content and the key interaction; implement a representative slice, inspect it in the browser and finish the remaining requested scope. A reference collection or a moodboard is not a built website.

Use [the working kit](references/working-kit.md) for searchable original directions, collision-safe scaffolding, static HTML checks and standalone installation. The two examples demonstrate different compositions; they are not universal layouts. The agent should create new layouts and components for the brief rather than keep swapping their copy.

Distinguish marketing/editorial sites from task-oriented product UI. Preserve the supplied brand, framework, routes, business logic and working interactions during redesign. Prefer useful hierarchy over habitual card grids or decorative effects. Taste is a contextual judgment, not a ban list or a numeric score. Do not claim production quality from a successful build or a clean HTML report.

Follow [project contract](references/project-contract.md). In integrated ACO also apply COMPACT-MEMORY.md; keep project data outside this public library. Read [source review and scope](references/sources.md) when comparing capabilities or checking provenance. Runtime media/motion work may use ACO Image/Motion when present, but these sibling skills are optional. Claude/Codex VS Code extensions use the same folder; VS Code alone does not execute skills.
