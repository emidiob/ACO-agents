# ACO — deterministic video composition

## Clock and coordinates

Use a composition's current frame and configured fps as the animation clock. Keep frame subscriptions in components that animate. Convert seconds to integer frame boundaries consistently; the last frame of an N-frame composition is N-1. Record whether a timing value is composition-global, sequence-local or source-media time. A trim changes source position, a sequence offset changes placement; applying both twice produces drift.

Use clamped interpolation for bounded movement and frame-evaluated springs for physical settling. A seek to frame k must produce the same state whether preceded by k-1 or a random frame. Avoid CSS keyframes, wall-clock timers and unseeded randomness in exported footage. Interactive web animation has a different clock; see [interactive](interactive.md).

## Structure and readable content

Separate scenes at genuine timing boundaries. Give independently editable clips their own nodes and names; retain the parent/child coordinate convention when extracting a component. Define transition overlap deliberately and account for it in total length. For a carried object match its screen location, dimensions and crop at the boundary before styling the transition.

Load and wait for real fonts before measuring text. Test longest copy, narrow crop and multilingual text; do not split joined scripts into disconnected glyphs. Animate words or blocks when character splitting would damage reading. Fit the hierarchy to video resolution rather than importing webpage type sizes unchanged.

## Assets and effects

Inspect media dimensions, duration, orientation, audio and alpha. Reference local public assets through the renderer's asset mechanism. Use media components supported by the installed Remotion release, not native video elements whose asynchronous clock can drift. Gate asynchronous font/image/media work with supported loading primitives and a bounded failure path.

Choose contain versus cover intentionally, including the focal point. Keep separate transform layers when motion and crop would compete. Apply an effect to the intended layer or group, not the entire composition by accident. Check that the installed version supports effects APIs before importing them; prefer built-in documented effects when they fit. Motion blur needs deterministic subframe sampling and a render proof, not a CSS blur substituted for temporal integration.

For 3D, drive camera, object pose and simulation from timeline time or reproducibly baked state. Match projected annotations to the same camera each frame. Await textures and models. Test random seeks and first/last frames. Use actual library APIs verified through [dependencies](dependencies.md); a plausible effect or component name is not evidence that it exists.
