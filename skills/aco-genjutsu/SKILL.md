---
name: aco-genjutsu
description: "Analyze a supplied video and prepare reference-guided recreation, motion-transfer or selective-edit prompts. Includes visual anchors, timed actions and render diagnosis; prompt preparation does not generate media."
---

# ACO Genjutsu

Turn the user's source into an actionable recreation brief. Use the original ACO method in this folder; do not substitute a generic scene description for reference preparation. The name remains the existing ACO command alias.

## Choose the deliverable

Read [prompt notation](references/prompt-notation.md), then the applicable case in [generation modes](references/generation-modes.md).

- **Same scene:** retain identity, wardrobe, setting, objects and movement. Use the original video and inspected source frames as anchors; replacement-character previews are unnecessary.
- **Changed scene:** identify the requested changes and which source properties must survive. Read [visual evidence](references/visual-evidence.md) before assigning references.
- **Existing render has a defect:** read [diagnosis](references/diagnosis.md); compare the actual render with its source before suggesting a targeted repair.
- **New video without a source:** route to `../aco-video/SKILL.md` and use the same notation without invented reference bindings.

For camera wording or character/image briefs, use [visual language](references/visual-language.md). Read the closest [worked case](references/worked-cases.md) before drafting; examples are fictional and never replace inspecting the user's file.

## Evidence before a final prompt

Inspect source metadata, representative frames and the transition/contact moments. The local `scripts/inspect_video.py` helper can extract selected frames and metadata using existing ffmpeg/ffprobe. It samples images, not a complete playback or audio review. Read its help before execution. Inspect the extracted images, refine timestamps around uncertain events, and disclose uninspected audio. A scene detector may suggest cuts but cannot prove their absence.

When the user has already said “as it is,” carry that instruction forward. Ask only for a missing choice that changes the deliverable, such as the target model/interface. Continue reference analysis while that choice is pending. If the provider is unknown, deliver a useful provider-neutral draft with unresolved controls clearly separated.

Use only real reference files. Preserve their exact paths privately; use short filenames in the result. Record each reference's job and the moment it represents. Translate ACO notation into the chosen provider's verified syntax before calling a prompt ready to paste into that interface. Strong wording does not guarantee pixel, identity or timing fidelity.

## Response

Give a brief source reading, a reference-to-purpose table, supported settings (or unresolved fields), one English prompt, and only the QC notes that matter to this shot. Explain in the user's language. Frame extraction is local analysis; generating replacement stills, uploading, rendering, editing video or spending credits requires the user's corresponding request.

The preexisting technical candidate `video.seedance.reference-video-replica` remains experimental and may be inspected explicitly through `skill-resolve --skill video.seedance.reference-video-replica --allow-candidate`. This original prompt workflow does not promote that or any other model-specific registry entry.

Before persistent writes, follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`. Keep media and private briefs outside the public ACO checkout.
