# Motion graphics and video

1. Establish target duration, format, audience, typography, real assets and output from the supplied context; ask only for facts that would materially change the result. Keep unconfirmed content labelled.
2. Inspect the existing project and installed Remotion versions. Read `remotion-best-practices`, then its create/markup/render references as relevant. All Remotion packages must be version compatible. Use official documentation for actual APIs; do not silently upgrade an existing project.
3. Storyboard time → visible composition → movement → readable landing → transition. Let meaning determine timing, not a fixed scene density. Tie typography reveals to reading time. Keep important content within the requested crop and safe areas.
4. Use deterministic frame-driven state: `useCurrentFrame()` and the composition fps, bounded interpolation, seeded variation, and explicit sequence durations. Browser CSS animations or wall-clock timers must not drive exported Remotion motion. Preload fonts/media and verify that seeks produce the same state.
5. Implement a representative scene and inspect beginning, movement, landing and boundary frames. Confirm final-frame duration, text overflow, alpha/background, asset loading and transitions. Extend after the proof works.
6. Preview in Studio when available. Render the requested local export with known composition ID, props, fps, dimensions and codec. For a preview request, show the working preview rather than declaring an MP4 exists. Do not enable cloud rendering by default.
7. Inspect the export itself, not only code: metadata, representative frames, transition playback and audio if present. Deliver source, export/preview and actual limitations. Keep screenshots/contact sheets alongside the requested project when useful.

A contact sheet cannot demonstrate pacing, smoothness or sync. A successful render cannot demonstrate taste. Review against the actual brief and references; avoid imposing scene counts, maximum hold times or one stock visual language on every film.
