# ACO 1.0.7 — validated professional skillpacks

The 20 skill bodies here are **technical registry skills** (`professional.*`), not merely curated playbooks. Each is selectable through ACO's existing `skill-search` / `skill-resolve` and may be loaded by the OS context selector after this release is installed. **No new office or native slash command is created**; Concierge remains the entrypoint.

## What `validated` means in this release

The status is strictly scoped to **procedural conformance on synthetic structured records**: each skill has 20 frozen positive/negative checks, at least 95% must pass and no critical failure is allowed. These tests verify evidence/state boundaries and invariants, **not** whether an LLM will produce an excellent artwork, curatorial argument, design, contract judgment or usable product. No independent professional human review has occurred.

`source_status: validated_internal` refers to the original ACO procedure and local tests, **not** to licensing approval for all upstream content. External sites remain reference-only, and upstream code/assets are not bundled. Distinguish reviewed documentation, transferred methodological principles, and demonstrated execution.

## Previous ACO status kept intact

- 14 original technical entries remain `active`.
- 30 original technical candidates remain non-selectable.
- 20 new professional skillpacks are `validated` and selectable on the new version only.
- 363 role definitions, 14 office groups, workflows, private-state boundaries, original skill-policy thresholds and historical frozen releases are preserved.

## Frozen checks and user approval

- Frozen input set: `config/professional-skill-holdout.json` (400 synthetic cases).
- Immutable freeze: `release/v107-professional-skill-freeze.json`.
- Initial harness failure and later successful rerun: `release/v107-professional-first-run.json`.
- Candidacy/rollback hashes: `config/professional-skill-promotions.json`.
- Executable tests: `scripts/professional_skill_validation.py`.
- Before GitHub publication, interactive authorization must match the exact SHA-256 promotion manifest, and ACO's official `skill_promotion_check()` must declare all 20 candidates eligible.

The `validated` lifecycle label is **not a legal, accessibility, security, usability, creative or medical certification**. Human decisions, source checks and host approvals still apply.

## Skill catalogue

| ID | Task | Source body |
|---|---|---|
| `professional.visual_critique` | Critica visiva e web design | [`skillpacks/professional/visual-critique.json`](../skillpacks/professional/visual-critique.json) |
| `professional.ux_research` | UX, ricerca utenti e servizi | [`skillpacks/professional/ux-research.json`](../skillpacks/professional/ux-research.json) |
| `professional.accessibility` | Accessibilità contestuale | [`skillpacks/professional/accessibility.json`](../skillpacks/professional/accessibility.json) |
| `professional.interface_motion` | Motion design delle interfacce | [`skillpacks/professional/interface-motion.json`](../skillpacks/professional/interface-motion.json) |
| `professional.video_editing` | Video, montaggio e narrazione temporale | [`skillpacks/professional/video-editing.json`](../skillpacks/professional/video-editing.json) |
| `professional.genjutsu_motion` | Genjutsu: osservazione e trasferimento del movimento | [`skillpacks/professional/genjutsu-motion.json`](../skillpacks/professional/genjutsu-motion.json) |
| `professional.curatorial_practice` | Ricerca curatoriale e costruzione di mostre | [`skillpacks/professional/curatorial-practice.json`](../skillpacks/professional/curatorial-practice.json) |
| `professional.art_criticism` | Critica d’arte e sviluppo della pratica | [`skillpacks/professional/art-criticism.json`](../skillpacks/professional/art-criticism.json) |
| `professional.collections_records` | Archivi, opere e conservazione documentale | [`skillpacks/professional/collections-records.json`](../skillpacks/professional/collections-records.json) |
| `professional.cultural_marketing` | Marketing culturale e sviluppo del pubblico | [`skillpacks/professional/cultural-marketing.json`](../skillpacks/professional/cultural-marketing.json) |
| `professional.copy_positioning` | Copywriting, contenuti e posizionamento | [`skillpacks/professional/copy-positioning.json`](../skillpacks/professional/copy-positioning.json) |
| `professional.editorial_verification` | Giornalismo, editing e revisione documentale | [`skillpacks/professional/editorial-verification.json`](../skillpacks/professional/editorial-verification.json) |
| `professional.legal_review` | Contratti, diritti e preparazione legale | [`skillpacks/professional/legal-review.json`](../skillpacks/professional/legal-review.json) |
| `professional.administration` | Amministrazione, segreteria e continuità operativa | [`skillpacks/professional/administration.json`](../skillpacks/professional/administration.json) |
| `professional.project_delivery` | Project management e consegna | [`skillpacks/professional/project-delivery.json`](../skillpacks/professional/project-delivery.json) |
| `professional.negotiation` | Negoziazione, offerte e partnership | [`skillpacks/professional/negotiation.json`](../skillpacks/professional/negotiation.json) |
| `professional.studio_finance` | Finanza di studio e controllo economico | [`skillpacks/professional/studio-finance.json`](../skillpacks/professional/studio-finance.json) |
| `professional.people_recruitment` | HR, recruitment e sviluppo competenze | [`skillpacks/professional/people-recruitment.json`](../skillpacks/professional/people-recruitment.json) |
| `professional.strategy_evaluation` | Strategia e valutazione dei programmi | [`skillpacks/professional/strategy-evaluation.json`](../skillpacks/professional/strategy-evaluation.json) |
| `professional.skill_evaluation` | Apprendimento e verifica delle competenze ACO | [`skillpacks/professional/skill-evaluation.json`](../skillpacks/professional/skill-evaluation.json) |

## How to query

```bash
python3 scripts/aco_cli.py skill-search --query "curatorial exhibition artworks thesis"
python3 scripts/aco_cli.py skill-resolve --skill professional.curatorial_practice
python3 scripts/professional_skill_validation.py --summary
```

The skill resolver loads one selected body. Open its referenced `METHOD.md`, `DECISIONS.md` and `OUTPUT.md` only if further depth is necessary.
