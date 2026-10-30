---
name: aco
description: "ACO Concierge entrypoint. Invoke as /aco in Claude Code or $aco in Codex. Route creative, studio and organizational tasks using the canonical ACO runtime."
---

# /aco — ACO Concierge

Use the canonical ACO 1.0.9 runtime (`aco://current`) in this checkout or a verified installed ACO skills root. This is a command **router**, not an independent model or process. Read `../aco-office-concierge/SKILL.md`, its relevant shared protocol, then only the selected office and specialist methods. Ask no unnecessary questions; follow authorization, source and verification rules.

## Argument dispatch

- `/aco` or `/aco <task>`: Concierge handles the request and selects the smallest relevant team.
- `/aco help`: show the short menu from `../aco-help/SKILL.md`.
- `/aco skills`: inspect registry with `skill-registry-check` / `skill-search`; report candidate status truthfully.
- `/aco webdesign <task>`: route via `../aco-webdesign/SKILL.md`.
- `/aco motion <task>`: route via `../aco-motion/SKILL.md`.
- `/aco image <task>`: route via `../aco-image/SKILL.md`.
- `/aco video <task>`: route via `../aco-video/SKILL.md`.
- `/aco capture <task>`: route via `../aco-capture/SKILL.md`.
- `/aco genjutsu <task>`: route via `../aco-genjutsu/SKILL.md`.

**Opt-in technical skills:** The 29 preexisting candidate entries (12 Seedance, 16 image, 1 Mimic) and the added Genjutsu prompt candidate may be **explicitly inspected and applied as experimental guidance** when the request selects them; use `skill-search --include-candidates` and `skill-resolve --allow-candidate`. This is not `active` promotion. The Mimic identity remains unverified; do not install unknown executables or claim it can run. Ordinary searches must stay fail-closed.

Invocation is host-specific: Claude Code Agent Skills can expose `/aco` when installed; Codex uses `$aco` when discovered; writing `/aco` in ChatGPT is a plain text request, not a registered native slash command.

Before any persistent write, follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`; keep private context outside the public library.

## Automatic visual-taste gate (ACO-TASTE-GLOBAL-108)

When this task produces, edits or reviews a visual artifact, load [the automatic cross-office Taste contract](../aco-office-concierge/references/protocols/VISUAL-TASTE-ROUTING.md) and [ACO Taste](../aco-taste/SKILL.md) **without requiring the user to invoke it**. Use the appropriate medium method and inspect real output. Nonvisual work stays direct; exact small changes preserve approved design.

## Open Design composition

For bounded visual briefs, original token presets, gallery remix, HTML/SVG composition or optional export, use the Open Design CLI in the Concierge runtime: `scripts/aco_open_design.py --help`. Combine it with ACO Taste direction and the automatic visual review gate; inspect actual rendered output before completion. Export availability and external handoff authorization are checked separately.
