---
name: aco-image
description: "Photographic and generative-image prompts using ACO methods, including Nano Banana and Seedream candidate adapters."
---

# ACO Image

Create or edit images from the actual brief and references. Start with the requested output: new image, bounded edit, consistent series or video anchor. Read [visual language](references/visual-language.md) for design versus pose; for photographic treatment use [Capture](references/capture.md).

Inspect supplied images before assigning identity, pose, composition, material and illumination roles. State what each reference must not transfer when ambiguous. Preserve the original file and the user's requested changes. For a bounded edit identify the region/property that may change and what must survive; do not silently redesign the whole scene. For a series establish an approved design anchor and compare each result with it.

Use [image execution](references/image-workflow.md) to move from brief to actual output. If the user asks for an image, execute through an available image tool rather than ending with a prompt. If no tool is available, deliver the useful prompt and identify the execution blocker. Provider-specific syntax must come from the actual interface or official documentation.

In a full ACO runtime the Nano Banana and Seedream adapters are optional technical candidates. Inspect them only when relevant and explicitly allowed; they are not required dependencies and their registry status remains unchanged. Never equate a candidate method with measured model performance.

## Project and host

Read [project contract](references/project-contract.md) before persistent writes. In a full ACO installation also follow its COMPACT-MEMORY.md protocol; standalone use does not require sibling skills. Keep private media outside the public library. Claude Code and Codex (including their VS Code extensions) use the same method; VS Code itself is not an agent host.

[Portable workflow](references/portable-workflow.md) explains local reference inventories, standalone installation and verification boundaries.
