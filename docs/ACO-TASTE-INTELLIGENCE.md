# ACO Taste Intelligence · global automatic visual quality (ACO v1.0.7+)

This add-on is an **original ACO adaptation of the main capabilities** studied in Incline, Hallmark, Anthropic Skills (`frontend-design`, `canvas-design`), gstack (`design-shotgun`, `design-review`), Emil Kowalski Skills, UI Skills and Frontend Stack. It does **not copy proprietary code or claim exact parity** with seven independently evolving software projects. It preserves source references, license classification, deployment limitations and a feature coverage matrix.

**Most important:** ACO's Concierge and creative offices load Taste automatically for requests that create/edit/review visual artifacts: images, photography, video, motion, web, UI, graphics, presentations, PDFs and spatial work. `/aco-taste` is an optional explicit route, not a required incantation.

## Architecture

`ACO Concierge → existing ACO specialist + Taste direction → media production → Taste observed QA → corrections → verified output`

- Incline → taste collections, negative references, user feedback and scoped insights.
- Hallmark → 50 ACO-original visual directions, concept-first layout, bounded static slop warnings.
- Anthropic → intentional frontend and static-canvas composition.
- gstack → diverse variants and accessible browser compare board, skeptical QA.
- Emil → motion intent, easing, interruptibility, accessibility and performance audit.
- UI Skills → evidence-based `DESIGN.md` and component contract, protected project source.
- Frontend Stack → route by task and medium, lead + ≤2 supporting methods, precedence rules.

Seven methods cannot magically guarantee human-level taste. The key measurable upgrade is the **mandatory real output inspection**, with visibility into unrun checks and human-approved direction.

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

For an existing ACO 1.0.7 checkout, see `integration/aco_patch.py`; run a dry run first and then `--apply --backup-dir` on a clean checkout. After applying, run ACO's existing generator, manifest, validation, tests and release builder. Do not merge to `main` or tag a release until CI is green and the owner approves.
