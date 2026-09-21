# Media implementation and reproducibility

## Programmatic motion
For an authorized Remotion project, read installed versions and the official documentation. Define composition dimensions/FPS/duration, input props and deterministic frame-based behaviour. Use seeded variability where required; avoid wall-clock timing or uncontrolled network changes during a render. Plan media loading, font readiness, captions, audio, transitions and handles. Preview representative frames and play the composition before rendering; a React build alone does not prove valid video. Check the engine's actual licence separately from the skills mirror.

## ComfyUI
Inventory application revision, Python/torch environment, GPU/VRAM, checkpoint architecture, encoders/VAE, model-file hashes and installed custom-node revisions. Read a current object_info snapshot. Distinguish API prompt JSON from UI workflow JSON. Resolve node choices and link types against that environment, run the existing comfy-preflight, then execute a minimal authorized test. Static success does not verify tensor shapes, model availability, VRAM use or visual quality. Never install arbitrary custom nodes or upload client images without approval. Save exact graph, assets, settings, output metadata and queue/error evidence.

## Colour and finishing
Determine actual source colour encoding and target display/delivery, not a guess from filename. Record transforms, working space, preview/display path and export tagging. Avoid applying transforms twice or silently changing exposure to conceal mismatches. Preserve the original and work non-destructively. Verify on available calibrated/appropriate viewing tools; an AI description cannot certify a grade.

## Output
Environment/asset manifest, runnable project or graph when actually built, test logs, previews/renders when actually produced, QC findings and a reproducible handoff. Fonts, paid plugins and model weights are never silently included in a public ACO package.

## Research provenance and limits

Comparison references: [S12](https://github.com/remotion-dev/skills), [S14](https://github.com/Comfy-Org/ComfyUI), [S11](https://github.com/vercel-labs/agent-skills).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
