# ACO Taste Intelligence · automatic visual direction and review (ACO v1.0.8+)

ACO Taste is an original visual direction and review layer. It does not bundle third-party implementations or guarantee a particular aesthetic result. Third-party references and rights information are recorded in `skills/aco-taste/assets/sources.json`.

**Most important:** ACO's Concierge and creative offices load Taste automatically for requests that create/edit/review visual artifacts: images, photography, video, motion, web, UI, graphics, presentations, PDFs and spatial work. `/aco-taste` is an optional explicit route, not a required incantation.

## Architecture

`ACO Concierge → existing ACO specialist + Taste direction → media production → Taste observed QA → corrections → verified output`

- Scoped reference collections, negative examples, user feedback and qualified insights.
- Fifty original visual directions and bounded static warnings.
- Composition guidance for web, graphics, photography, video and motion.
- Variant comparison, rendered output review and prioritized corrections.
- Motion, accessibility and performance checks where relevant.
- Evidence-based `DESIGN.md` and component contracts.
- One lead method with up to two supporting methods per phase.

These methods do not guarantee visual quality. The required completion gate is **inspection of the actual rendered output**, with any unrun checks made visible.

## Requirements

Python 3.11+ for the native CLI. Pillow and FFmpeg are optional for file metadata; browser/actual visuals must be rendered/inspected by the host. ACO Webdesign/Motion/Image/Video remain the execution engines where available. No network, vendor API keys, packages, persistent agents or cloud accounts are silently installed.

## Quick examples

```bash
python3 skills/aco-taste/scripts/taste.py route --task "Redesign my portfolio website"
python3 skills/aco-taste/scripts/taste.py route --task "Produce a short film" --medium video
python3 skills/aco-taste/scripts/taste.py directions --brief skills/aco-taste/examples/brief.json
python3 skills/aco-taste/scripts/taste.py audit-css --file my.css
python3 skills/aco-taste/scripts/taste.py media-preflight --file clip.mp4
python3 skills/aco-taste/scripts/taste.py compare --packet variants.json --output /tmp/variants.html
```

For an existing checkout, follow the [upgrade procedure](UPGRADING.md). After updating, run the generator, manifest builder, validation and tests listed in the root `AGENTS.md`.
