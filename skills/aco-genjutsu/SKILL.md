---
name: aco-genjutsu
description: "Analyze a supplied video and prepare reference-guided recreation, motion-transfer or selective-edit prompts. Creates visual reference files before drafting timed prompts; video rendering remains a separate action."
---

# ACO Genjutsu

Turn the user's source into an actionable recreation brief. Use the original ACO method in this folder; do not substitute a generic scene description for reference preparation. The name remains the existing ACO command alias.

## Choose the deliverable

Start with [reference delivery](references/reference-delivery.md) and the applicable case in [generation modes](references/generation-modes.md). Read [prompt notation](references/prompt-notation.md) only after preparing the references; it is an internal checklist, not a formula to return to the user.

- **Same scene:** retain identity, wardrobe, setting, objects and movement. Extract, inspect and deliver actual source-frame files as anchors, together with a contact sheet; replacement-character previews are unnecessary.
- **Changed scene:** identify the requested changes and which source properties must survive. Read [visual evidence](references/visual-evidence.md), then create and inspect the requested transformed reference stills through the available image tool before writing the final video prompt.
- **Existing render has a defect:** read [diagnosis](references/diagnosis.md); compare the actual render with its source before suggesting a targeted repair.
- **New video without a source:** use ACO Video when available; otherwise use the local generation modes and prompt notation for a new shot without invented reference bindings.

For camera wording or character/image briefs, use [visual language](references/visual-language.md). Read the closest [worked case](references/worked-cases.md) before drafting; examples are fictional and never replace inspecting the user's file.

## Evidence before a final prompt

Inspect source metadata, representative frames and the transition/contact moments. The local `scripts/inspect_video.py` helper creates metadata, a chronological overview, cut candidates, selected full-size frames, a reference strip and a draft reference map using existing ffmpeg/ffprobe. It samples images, not a complete playback or audio review. Read its help before execution. Inspect the extracted images, refine timestamps around uncertain events, and disclose uninspected audio. A scene detector may suggest cuts but cannot prove their absence.

When the user has already said “as it is,” carry that instruction forward. Ask only for a missing choice that changes the deliverable, such as the target model/interface. Continue reference analysis while that choice is pending. An unknown video provider must not block local extraction, visual inspection or delivery of references. Prepare those first; only the final provider bindings and settings remain unresolved.

Use only real reference files. Preserve their exact paths privately; use short filenames in the result. Record each reference's job and the moment it represents. Translate ACO notation into the chosen provider's verified syntax before calling a prompt ready to paste into that interface. Strong wording does not guarantee pixel, identity or timing fidelity.

## Complete motion transfer

For every source recreation or transformation, follow [motion reconstruction and transfer](references/motion-transfer.md) before drafting the final prompt. Inspect the entire temporal sequence, record meaningful subject/object/camera events in `motion-plan.json`, map each to the target and retain its concrete action in `shot-prompt.txt`. Anchors supplement this sequence; they do not replace it. Recheck coverage after shortening or translating the prompt. Uncertain or uninspected motion must remain unresolved, never filled with invented choreography.

## Response

Complete the local preparation and packet checks in [reference delivery](references/reference-delivery.md), including the source-specific `shot-prompt.txt`; a generic template is not a finished prompt. Lead with the actual reference images: show a contact sheet and link the individual full-resolution files in time order. State which images are extracted and which are generated/edited. Then give a compact file/time/purpose map, supported settings (or unresolved fields), one shot-specific English prompt, and relevant QC notes. Do not finish with prose-only placeholders when the files can be made.

A request to recreate/transform a supplied video through this skill includes preparing the reference stills needed for that requested result, unless the user explicitly asks for text only. Use the host image tool for requested image transformations and obey its actual permissions; do not ask for a redundant approval merely because a still must be produced. Preserve the user's chosen transformation. Video generation, external uploads and additional paid provider operations remain separate actions. If an essential reference or tool is missing, identify that specific blocker, deliver the source frames already available, and label unfinished previews accurately.

The preexisting technical candidate `video.seedance.reference-video-replica` remains experimental and may be inspected explicitly through `skill-resolve --skill video.seedance.reference-video-replica --allow-candidate`. This original prompt workflow does not promote that or any other model-specific registry entry.


## Project and host

Read [project contract](references/project-contract.md) before persistent writes. In a full ACO installation also follow its COMPACT-MEMORY.md protocol; standalone use does not require sibling skills. Keep private media outside the public library. Claude Code and Codex (including their VS Code extensions) use the same method; VS Code itself is not an agent host.

[Portable workflow](references/portable-workflow.md) explains local reference inventories, standalone installation and verification boundaries.
