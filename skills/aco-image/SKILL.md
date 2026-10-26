---
name: aco-image
description: "Photographic and generative-image prompts using ACO methods, including Nano Banana and Seedream candidate adapters."
---

# /aco-image

Read the relevant ACO Artist/Production role, `../aco-office-concierge/references/playbooks/ACO-CAPTURE.md` if photographic, and only needed `image.shared.*` technical candidates. Apply 4 model-specific adapters (`image.adapter.nano-banana-2`, `image.adapter.nano-banana-2-1`, `image.adapter.seedream-4-5`, `image.adapter.seedream-5`) only if the user's model matches and its current UI is verified. The image skillpack is *candidate* in 1.0.4: opt-in method inspection is allowed via `--allow-candidate` but is not measured model output validation. Never claim a generated picture until one is inspected.

Before any persistent write, follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`; keep private context outside the public library.

## Original ACO prompt method

For character, object or scene briefs and video anchor images, read `../aco-genjutsu/references/visual-language.md` and `../aco-genjutsu/references/visual-evidence.md`. Separate visual design from pose, inspect reference conflicts, and generate images only when requested.
