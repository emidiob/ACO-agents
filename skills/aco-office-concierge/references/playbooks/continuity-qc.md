# Continuity, timing and generated-video QC

## Planning records
Use stable shot IDs and scene IDs. Track reference IDs, intended start/end states, wardrobe/props, location/light, action progression, gaze, screen direction and camera axis where relevant. Explicit continuity deviations need a reason; do not turn every intentional discontinuity into an error.

## Timeline checks
Use integer frame durations and a stated FPS for planning. Count dissolves/overlaps once, include pauses and audio tails, and preserve source handles. Distinguish source generation duration from the usable edit segment; a five-second generated clip may contribute fewer seconds to the final cut.

## Visual inspection
1. Inspect reference, opening, action-critical, transition and closing frames, plus full playback at delivery speed. A small contact sheet can miss temporal failures.
2. Compare identity, prop geometry, hands/limbs, spatial relation, lighting, texture and text against approved references; record the timecode of every issue.
3. Check motion for unwanted morphs, inconsistent speed, camera drift, flicker, loop seams and physically incoherent transitions. Do not mistake compression or interpolation artefacts for creative choices without review.
4. Review edit comprehension and continuity across shots, not only the attractiveness of each isolated clip. Sound and subtitles need their own checks.
5. Classify by remedy: regenerate, shorten/select alternate take, stabilize/retime with approval, composite/paint, or intentional accepted exception. Preserve originals and sidecar provenance.
6. Verify delivery frame rate, resolution, aspect, colour tags, audio, captions and master/derivative naming in actual files. A visually pleasing preview is not a delivery QC report.

## Acceptance
State which frames/segments were inspected and which checks were not run. Structural shot-plan validation does not prove visual continuity in rendered footage. A rendering receipt does not prove that the result passed visual review.

## Research provenance and limits

Comparison references: [S13](https://github.com/smixs/visual-skills), [S12](https://github.com/remotion-dev/skills), [S14](https://github.com/Comfy-Org/ComfyUI).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
