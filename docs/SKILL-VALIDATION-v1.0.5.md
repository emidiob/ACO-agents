# ACO 1.0.5 — Skill validation evidence

**Scope:** source and registry inspection, not video/image model performance tests. The original 14 active technical methods retain their recorded source-review/structural-test status. No inactive candidate is automatically promoted.

**Technical registry:** 44 total — 14 active, 30 candidate / unverified.

## What is verified and what is not

- Static check verifies each registered skill body exists and matches its ID, version and lifecycle status.
- The baseline active methods carry source provenance; historical ACO tests and current ACO suite should be run by the builder.
- No external provider outputs or real Genjutsu/Seedance/Nano Banana/Seedream experiments were inspected in this build.
- Candidates remain available only via an explicit experimental inspection route, not default selection.
- Promotion requires ≥20 frozen benchmark cases, ≥95% score, zero critical failures, exact approval and rollback reference, plus applicable actual output evidence.

## Inventory

| Skill | Current status | Method/source audit | Real output verified |
|---|---|---|---|
| `visual_research.archive_first` | active | static registry/body verified | No |
| `visual_research.letterform_archive` | active | static registry/body verified | No |
| `visual_research.met_open_access` | active | static registry/body verified | No |
| `visual_research.rijksmuseum_data` | active | static registry/body verified | No |
| `visual_research.nypl_public_domain` | active | static registry/body verified | No |
| `visual_research.archives_design` | active | static registry/body verified | No |
| `product_design.details_reference` | active | static registry/body verified | No |
| `product_design.refero_flow_research` | active | static registry/body verified | No |
| `product_design.design_spells_microinteractions` | active | static registry/body verified | No |
| `frontend_motion.library_selection` | active | static registry/body verified | No |
| `frontend_motion.gsap` | active | static registry/body verified | No |
| `frontend_motion.animejs` | active | static registry/body verified | No |
| `frontend_motion.motion_react` | active | static registry/body verified | No |
| `frontend_motion.react_spring` | active | static registry/body verified | No |
| `software_analysis.mimic_littledavi` | candidate_unverified | static registry/body verified | No |
| `video.seedance.action` | candidate | static registry/body verified | No |
| `video.seedance.audio` | candidate | static registry/body verified | No |
| `video.seedance.camera-motion` | candidate | static registry/body verified | No |
| `video.seedance.commercial` | candidate | static registry/body verified | No |
| `video.seedance.compact` | candidate | static registry/body verified | No |
| `video.seedance.fashion` | candidate | static registry/body verified | No |
| `video.seedance.found-footage` | candidate | static registry/body verified | No |
| `video.seedance.identity` | candidate | static registry/body verified | No |
| `video.seedance.performance` | candidate | static registry/body verified | No |
| `video.seedance.qa` | candidate | static registry/body verified | No |
| `video.seedance.storyboard` | candidate | static registry/body verified | No |
| `video.seedance.timeline` | candidate | static registry/body verified | No |
| `image.shared.reference-decomposition` | candidate | static registry/body verified | No |
| `image.shared.identity` | candidate | static registry/body verified | No |
| `image.shared.photo-realism` | candidate | static registry/body verified | No |
| `image.shared.optics` | candidate | static registry/body verified | No |
| `image.shared.fashion` | candidate | static registry/body verified | No |
| `image.shared.product` | candidate | static registry/body verified | No |
| `image.shared.composition` | candidate | static registry/body verified | No |
| `image.shared.textures` | candidate | static registry/body verified | No |
| `image.shared.editing` | candidate | static registry/body verified | No |
| `image.shared.multiref` | candidate | static registry/body verified | No |
| `image.shared.qa` | candidate | static registry/body verified | No |
| `image.shared.artifact-diagnosis` | candidate | static registry/body verified | No |
| `image.adapter.nano-banana-2` | candidate | static registry/body verified | No |
| `image.adapter.nano-banana-2-1` | candidate | static registry/body verified | No |
| `image.adapter.seedream-4-5` | candidate | static registry/body verified | No |
| `image.adapter.seedream-5` | candidate | static registry/body verified | No |
| `video.seedance.reference-video-replica` | candidate | static registry/body verified | No |

## New /aco-genjutsu scope

`video.seedance.reference-video-replica` is a prompt-only Genjutsu method adapted from JutsuHQ (MIT), not a runnable video-generation service. It remains a candidate with explicit access only.

## Reproduction

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py skill-registry-check
python3 scripts/aco_cli.py skill-benchmark
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

Use actual generated videos/images and a frozen output benchmark before changing candidate state.
