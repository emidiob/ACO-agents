---
name: aco-webdesign
description: "Design, build and redesign websites and product interfaces with original ACO art direction, searchable design recipes, reusable tokens, functional states and browser verification."
---

# ACO Webdesign

Use `/aco-webdesign` in Claude Code, `$aco-webdesign` in Codex, or `aco webdesign <task>` through Concierge. This is a native, independently installable ACO skill. It contains its own methods; external agent skills are not runtime dependencies. Inspect the existing project before choosing libraries or changing its design system.

## Native operations

For a named operation such as `polish`, `harden`, `typeset`, `prototype` or `motion-review`, use [the operation index](references/operations.md) and read only its selected method. `python3 scripts/operations.py list` lists all operations; `python3 scripts/operations.py show harden` prints the selected method. These are agent workflows, not claims of automated engine parity.

Use [framework tools](references/framework-tools.md) for Vite-backed JSX/TSX/Vue source editing and stateful React/Vue components. Preserve the existing framework and dev server; use automatic static-text bindings or explicit source markers for live edits. The live panel also runs the rendered design review, typography inspection and frame measurements.

Use [interactive tools](references/interactive-tools.md) for source-backed static HTML editing, the 62-rule design review, 64 component recipes and 16 original effects. Run the selected tool and verify its output; do not substitute a written plan for a requested export or edit.

Use [project systems and prototype review](references/project-tools.md) for master/page token inheritance, functional variant comparison and generated stress content.

Use [native engines](references/native-engines.md) for external-data retrieval/search, design-system proposals and rendered DOM analysis.

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

Follow [project contract](references/project-contract.md). In integrated ACO also apply COMPACT-MEMORY.md; keep project data outside this public library. Read [dependencies and attribution](references/sources.md) when using external resources. Runtime media/motion work may use ACO Image/Motion when present, but these sibling skills are optional. Claude/Codex VS Code extensions use the same folder; VS Code alone does not execute skills.


<!-- ACO-V107-PROFESSIONAL-BRIDGE -->
## Professional method companion (ACO 1.0.7)

When the full ACO library is available, for task-specific critical procedure consult the validated professional skill `professional.visual_critique` (synthetic procedural checks only) and its original method at `skills/aco-office-concierge/references/competencies/visual-critique/METHOD.md` in that library. Existing provider-specific technical candidates remain gated. No new provider activation, professional certification or rendering authorization is implied.
<!-- END ACO-V107-PROFESSIONAL-BRIDGE -->
