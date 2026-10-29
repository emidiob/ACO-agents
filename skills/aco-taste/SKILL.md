---
name: aco-taste
description: "Automatic cross-office visual direction, contextual taste evidence, comparison and output review for image/photo/video/motion/graphics/web/UI/editorial/spatial work. Invoke automatically for any visual deliverable; /aco-taste is also available explicitly."
---

# ACO Taste Intelligence — automatic visual quality layer

**Critical:** ACO Concierge must invoke this layer for ANY requested visual creation, critique or modification, even when the user does not say `taste`. This is not a new office or a replacement for an existing specialist. For an exact small change, use the focused path rather than a complete rebrand. Read [the shared trigger contract](../aco-office-concierge/references/protocols/VISUAL-TASTE-ROUTING.md) before visual work.

Before any persistent write, follow `COMPACT-MEMORY.md` in the shared Concierge protocols.

## Task-owned path (selective loading)

Read [TASTE-PROTOCOL.md](references/TASTE-PROTOCOL.md) for the stage contract, then the **minimum relevant** modules:

- [Taste evidence and memory](references/TASTE-MEMORY.md): references, negative examples, explicit feedback, personal-library boundaries (Incline-inspired original ACO implementation).
- [Concepts and directions](references/DIRECTIONS.md): original ACO catalog of 50 visual materials, concept-first contrasting directions, purposeful anti-template critique (Hallmark-inspired).
- [Art direction](references/ART-DIRECTION.md): subject-grounded typographic and compositional design, and static-art composition (Anthropic skills-informed).
- [Variant exploration and visual QA](references/VARIANTS-AND-REVIEW.md): compare actual alternatives, browser screenshots, prioritized correction (gstack-informed).
- [Motion craft](references/MOTION-CRAFT.md): useful/restrained movement, interruption, easing, accessibility and performance (Emil Kowalski-informed).
- [Design-system evidence](references/DESIGN-SYSTEM.md): source-of-truth `DESIGN.md`, token provenance, component states and accessibility (UI Skills-informed).
- [Conflict resolution](references/ROUTING-AND-CONFLICTS.md): one lead, at most two supporting methods, explicit precedence, no incompatible packs stacked (Frontend Stack-informed).

Choose medium guidance: [Web + UI](references/MEDIUM-WEB-UI.md) · [Photography + image](references/MEDIUM-PHOTO-IMAGE.md) · [Video + motion](references/MEDIUM-VIDEO-MOTION.md) · [Graphics + documents + slides + spatial](references/MEDIUM-GRAPHICS.md).

## Run when appropriate

`python3 scripts/taste.py route --task "Make a magazine cover"`

`python3 scripts/taste.py directions --brief /path/to/brief.json`

`python3 scripts/taste.py compare --packet /path/to/variants.json --output /path/to/new-comparison.html`

`python3 scripts/taste.py gate --packet /path/to/evidence.json`

Source art and local visual evidence may require browser, image, FFmpeg, or actual rendering tools. ACO cannot claim images were inspected because it read metadata or code. External upstream implementations are **not bundled**; see `assets/sources.json`, attribution and feature coverage. No silent installation or media upload.

## Release acceptance

Before declaring visual work finished, apply the medium gate to **actual** screenshots, images, rendered pages, video timecodes or page exports. Give the user a specific before/after judgment, observed improvements, unresolved faults and named unrun checks. Human approval is not inferred from test success, silence or reference selection. Do not invoke fake independent agents; separate the reviewer pass or use a real reviewer only when available.
