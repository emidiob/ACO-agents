---
name: aco-genjutsu
description: "Prompt-only source-video recreation, camera/actor motion transfer and character substitution. Trigger: /aco-genjutsu or $aco-genjutsu; never generate a video automatically."
---

# /aco-genjutsu — video-reference replication prompts

Route through the ACO `production-office` specialist `ai_video_prompt_adapter`; read `../aco-office-concierge/references/playbooks/ai-video.md` and the technical body `../../skillpacks/seedance/reference-video-replica.json` (when in source checkout). In an installed ACO runtime, use the canonical skill registry `video.seedance.reference-video-replica` with explicit `--allow-candidate`; do not guess a relative file path in a client project.

1. Inspect the **actual** user-authorized source video before claiming cuts, motion beats or duration. If the video cannot be viewed, distinguish user description from inspected facts; do not fabricate timecodes.
2. Record what should remain: shot order, timing, camera, gesture, framing and allowed sound; and what must change: characters, wardrobe, props, setting. Preserve image/video rights and likeness consent.
3. Map real uploads to `@Video1`, `@Image1`, `@Image2`… with explicit retain/exclude attributes. Syntax, input count, duration, audio and resolution are **provider-specific**, and must be checked before giving clickable settings. Never pretend previews, crops or references already exist.
4. Provide **only** a short source analysis, ordered reference map, checked UI settings, one concise **English copy-ready prompt** and up to three QC/repair notes. No rendering, API calls, uploads or paid operations.
5. For motion transfer, separate motion source from target identity; check turns/occlusion, silhouette scale and costume leakage. If reference materials are insufficient, give a clearly labeled provisional prompt.

Reference adapted independently from JutsuHQ's MIT-licensed `higgsfield-seedance-prompt-skill`, particularly `references/motion-transfer.md`, with attribution in the registry. Candidate method is available for *explicit experimental use*, but no real model-render benchmark or provider acceptance is claimed.

Before any persistent write, follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`; keep private context outside the public library.
