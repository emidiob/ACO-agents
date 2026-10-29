# Variant exploration and visual review (ACO original; gstack study)

**Variant board**: at least two truly distinct structures for exploratory work. Record identity, actual rendered screenshot/frame and tradeoff for each; use `taste.py compare --packet variants.json --output board.html` to create a standalone, accessible comparison board. The browser can export a local JSON file with ratings and comments. No choice means no approval; copied feedback is not stored until explicitly imported.

**Visual QA**: inspect actual screenshot or video frame/image. For web inspect desktop, mobile, readable large text, focus/error/empty states. For image inspect lighting, crop, material detail, anatomy/identity where relevant. For video compare source vs result event-by-event and review actual tail, not just first frame. For print inspect exported pages. A successful lint/compile doesn't demonstrate visual quality.

**Review findings**: for each issue provide evidence region/timecode, severity, relation to creative objective, minimal correction and verification. Distinguish broken usability from subjective taste. Rank the highest-impact three before tweaking colors and icons. Reinspect changed output.

**Comparison validity**: when evaluating alternatives, hold constant the brief, real content, viewport, data, asset permissions and task. A better screenshot can still have worse accessibility or broken interactions. An optional blind reviewer cannot be faked; label single-author assessment honestly.

**Provenance**: source snapshots and user responses remain in the project. No automatic shared database, provider API, browser authorization or code commits are granted by these methods.
