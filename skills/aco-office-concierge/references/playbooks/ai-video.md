# AI video prompting and provider adapters

## Separate four layers
1. Creative intent: the story/meaning.
2. Shot specification: the observable image, action, camera and timing.
3. Provider adapter: current model/interface capabilities and request syntax.
4. Render evidence: generated files, inspected results, cost and receipts.

A strong prompt cannot replace the last two layers.

## Intake and provider verification
Read supplied model/tool information first. Clarify generation mode, usable reference assets and target clip/deliverable only when missing. Verify the exact provider, model, UI or API surface, supported duration/aspect/resolution, input image/video rules, sound support, negative-prompt support and costs from current primary documentation/tool schema. Do not transfer parameters between providers or between a provider's UI and API. If this is unknown, deliver a provider-neutral shot and ask the essential question before preparing a runnable request.

## Shot prompting
1. Lock the visible start state and the intended end state. Separate appearance described by the input image from motion that the text needs to introduce.
2. Use concrete subject actions and a coherent camera instruction. Keep physical events within a plausible time budget. Avoid mutually exclusive static and moving-camera instructions.
3. Put model parameters in their actual fields, not in decorative prose. Reference images must exist and be authorized for the task.
4. For image-to-video, preserve the approved visual anchor and describe motion. For text-to-video, provide the essential visual scene as well as motion. For editing/extension, describe the boundary that must remain unchanged.
5. Negative prompting is provider-specific. Do not add a negative field to a model that does not expose it. Rewrite into desired positive behaviour only where it preserves the request; otherwise flag the unsupported control.
6. Treat temporal choreography and exact text/identity reproduction as uncertain until inspected. Split a difficult sequence into shots or use compositing when that better preserves the idea.
7. Run one small authorized test before a large batch. Track model version, reference IDs/hashes, exact prompt, seed when actually supported, settings, cost and result. Change one diagnostic variable at a time; do not promise identical results from a seed alone.
8. Stop after the agreed trial budget. A rejected/refused request is not permission to switch accounts/providers to bypass a restriction.

## Reference-video recreation — prompt-only method

For an explicit request to recreate a *source video* using original replacement characters or
objects, the optional `video.seedance.reference-video-replica` technical candidate can be
inspected **only on request**. It is **not active or auto-selected**; apply the ordinary
`ai_video_prompt_adapter` and this playbook for usable prompting without claiming provider
validation.

1. Inspect the actual authorized source video (or identify precisely what cannot be inspected).
   Record shot/cut boundaries, camera trajectory, framing, key poses, timing, actor/object
   positions, interaction and audio. Source timecodes require real visual evidence.
2. Specify what stays (motion, staging, camera, permitted sound, cut rhythm) versus what
   changes (character identity, wardrobe, props, setting). Do not assume the provider can
   preserve exact choreography. Respect source/reference rights and personal likeness consent.
3. If the verified provider uses them, bind `@Video1` to motion/camera/timing only and
   `@Image1`, `@Image2`, etc. to the corresponding new identities and objects. Map the
   actual upload order and reject unintentional source attributes; never invent assets.
4. For significant character swaps, plan inspected preview stills at key poses and
   occlusions before generation, when the user has authorized producing them. Reuse only
   reference images that actually exist.
5. Deliver **only** source observations/unknowns, a reference upload table, verified UI
   settings, one English copy-ready prompt and short QA/repair guidance. Split incompatible
   cuts into shots. Do not execute a render or claim a result from the prompt alone.

Provenance: independently adapted from [JutsuHQ's MIT-licensed Higgsfield Seedance prompt
skill](https://github.com/jutsuhq/higgsfield-seedance-prompt-skill), particularly its
motion-transfer reference. Model capabilities and UI tag syntax require current verification.
No upstream shell scripts, prompt corpus or generation service is bundled.

## Provider reading list (recheck before execution)
- [Runway Gen-4 video prompting](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide): positive, concise motion guidance for that documented model; not a universal latest-model contract.
- [Google video prompting](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide): subject/action/context/camera and model-dependent controls.
- [ComfyUI](https://github.com/Comfy-Org/ComfyUI): actual node and model environment determines graph capability.

## Output
Copy-ready prompt plus a small metadata table (provider/model or unresolved, mode, input refs, generation settings, uncertainty). The ACO prompt helper is an offline draft composer, not a provider client or a quality guarantee.

## Research provenance and limits

Comparison references: [S13](https://github.com/smixs/visual-skills), [S14](https://github.com/Comfy-Org/ComfyUI), [S12](https://github.com/remotion-dev/skills).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
