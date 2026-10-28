# ACO Motion kit — verification scope

Reviewed 2026-10-28. Integrated and standalone builds share the canonical `skills/aco-motion` source. This record is implementation evidence, not a creative-quality certification.

| Check | Result | Limit |
|---|---|---|
| Original Typography composition | Actual H.264 render, 1280×720, 30 fps, 240 frames / 8 s, no audio; sampled frames inspected | No audio/mix validation; not a general design benchmark |
| Remotion Studio | Three compositions loaded; preview playback advanced | Source-panel visual editing of individual layers not tested |
| UI prototype | Desktop browser load, Video/Web filters, keyboard opening, Escape and focus return observed | Mobile and OS reduced-motion execution not tested; implementation includes both paths |
| Reference graphics | Two interpolation implementations rendered 91 frames each; decoded-frame SSIM minimum 0.999968, mean 0.99999933 | Same known anchor table; not blind inference or live-action recreation; not pixel-identical |
| Standalone packaging/install | Archive integrity, both host folder conventions, dry run, ownership checks, update backup and local-edit refusal tested | Does not prove a fresh Claude/Codex/VS Code extension discovery session |
| Scaffold/export checks | Existing project preserved; actual ffmpeg fixture accepted; wrong dimensions, missing required audio and duration rejected | Metadata acceptance does not inspect visual quality |

Reproduce with the original starter and tools described in `skills/aco-motion/references/working-kit.md`. Use a new task directory; do not put generated renders or private inputs in the public library. Preserve the engine and project dependency licenses. Additional production cases should extend this evidence with observed results rather than promoting untested capabilities.
