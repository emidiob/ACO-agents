# ACO v0.5.0 — Specialist gap analysis

## Executive finding

ACO v0.4.3 already had broad role coverage. The main gaps were depth, verification and boundaries: visual judgement versus implementation, Figma mapping, editorial content models, measurable experiments, scene-to-shot continuity, provider-specific video controls and frame-based production.

Implemented: **46 existing roles deepened**, **3 office routers updated**, **14 distinct roles added**, **12 on-demand playbooks** and executable specialist checks. **All 349 baseline roles are retained**, for **363 roles and 16 entry-point skills**. The workflow catalogue grows from 24 to 32.

## What was compared — and what was not

Every one of the 349 baseline role records was automatically compared with each of 15 external source inventories: **5,235 role/repository comparisons**, using **313 observed catalogue labels/topics**. The extraction of relevant catalogue items is curated and documented per source. Catalogue pages and README sections were inspected as recorded; not every source file, external dependency or claimed feature was tested. Some inventories intentionally retain only the relevant subset.

The matching script uses normalized token vectors with inverse-document-frequency weights. Similarity ranks related subjects; it cannot certify professional skill, creative quality or correctness. The proposed implementation changes are a separate reviewed decision layer. The remaining 300 baseline roles are **retained, not declared strong or comprehensively evaluated**. Art criticism, HR, legal accuracy and other domains outside this targeted pass need their own evidence-based evaluations.

Inputs: [source inventory](../research/specialist-upgrade/sources.json), [baseline records and hashes](../research/specialist-upgrade/baseline-roles.json), [implementation decisions](../research/specialist-upgrade/decisions.json). Outputs: [machine-readable comparison](../research/specialist-upgrade/comparison.json) and [filterable HTML](../research/specialist-upgrade/comparison.html).

Run `python3 scripts/compare_specialists.py` to reproduce the comparison from those supplied snapshots. It does not silently refresh online sources. Date and re-inspect sources before a later upgrade.

## The 15 repositories

| ID | Repository | Best use in ACO | Important limit |
|---|---|---|---|
| S01 | [anthropics/skills](https://github.com/anthropics/skills) | Progressive disclosure, design intent and browser-based verification. | Do not apply the repository-level licence to every skill, or copy provider-specific brand rules. Directory inventory read through GitHub contents as well as README. |
| S02 | [obra/superpowers](https://github.com/obra/superpowers) | Small reproducible steps, debugging evidence and verification before completion. | Do not import hooks, delete existing work to satisfy a testing ritual, or force every tiny task through the entire workflow. |
| S03 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | Repository-aware diagnostics, repeatable evaluations and scoped memory. | No blind installation of hooks, auto-approval settings or automatic learning from private client content. |
| S04 | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | Boundary checks and specialist gaps across design, engineering and agency work. | Role names and marketing claims do not demonstrate output quality. Most management roles already exist in ACO. |
| S05 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | Stack-aware routing and a design-to-implementation boundary. | Do not add a language agent without an actual stack need or assume model/frontmatter compatibility with Codex. |
| S06 | [github/awesome-copilot](https://github.com/github/awesome-copilot) | Runtime accessibility, explicit tool requirements and observable acceptance. | A Copilot agent profile is not a Codex configuration; a catalogue is not an audited installer. |
| S07 | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Measurable conversion hypotheses, instrumentation and research-backed copy. | Do not assume a newer skill has the old name, infer causality from dashboards or adopt intrusive outreach. |
| S08 | [anthropics/financial-services](https://github.com/anthropics/financial-services) | Project accounting evidence, reconciliation and close checklists. | Investment-banking workflows are not automatically relevant to a small creative practice; no automatic ledger posting or KYC decisions. |
| S09 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Separate durable product requirements from visual decisions; iterate in the browser. | Do not universalize bans on black, neutral fonts or cards; no downloaded binary or hooks are executed by ACO. |
| S10 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Structured visual alternatives, component states and resilient typography. | Category-to-style matches are starting hypotheses, not universal brand choices. No datasets or font files are copied. |
| S11 | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Performance triage, component composition and web checks. | No automatic hosting choice or deployment; React recommendations are stack/version dependent. |
| S12 | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Frame-based compositions, captions and deterministic motion deliverables. | This is code-driven video, not a universal generative-video prompt engine. Do not assume MIT or free commercial engine use. |
| S13 | [smixs/visual-skills](https://github.com/smixs/visual-skills) | Separates visual direction, shot logic and provider-oriented prompting. | Credit: Serge Shima (smixs). No prompt files copied. Provider limits must be checked against official current documentation. CC material cannot be relabelled as wholly ACO-restricted. |
| S14 | [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | Actual environment schemas and reproducibility constraints for ComfyUI. | No runtime, model weights or custom nodes are bundled. Static graph validity is not successful GPU execution. |
| S15 | [openai/plugins](https://github.com/openai/plugins) | Official design-system and product implementation workflows. | ACO remains a skill library, not a plugin. Do not import manifests, dependencies or account permissions. |

## Gaps and concrete changes

| Gap | Old state | Implemented change | Acceptance boundary |
|---|---|---|---|
| Visual design | Broad design roles; no common rigorous review loop | Visual critic, typography/layout specialist and design contract | Must inspect actual renders before visual signoff |
| Design-to-code | Design and engineering loosely handed off | Figma implementation role and revision/component mapping | Exact source node and rendered comparison required |
| Websites beyond a generic landing page | General frontend/product roles | CMS/content architecture and creative frontend with fallbacks | Content states, reflow, keyboard and budgets need evidence |
| Conversion claims | Marketing/analytics roles lacked shared experiment contract | Experiment designer and instrumentation engineer | No causal lift claims without a suitable experiment |
| Directing | Film director method was three broad steps | Scene purpose, beats, blocking, axis/eyeline and coverage playbook | A treatment is not a produced film |
| Shot continuity | No dedicated continuity/animatic role | Storyboards, continuity supervisor, animatic editor and timeline check | Structural agreement does not verify generated visuals |
| Video prompting | General visual prompt engineer | Model/interface adapter, source freshness, input/settings separation | No unsupported negative/audio/seed controls or fake requests |
| Generated-video acceptance | Generic delivery QC | Timecoded generative-video QC and remedy classification | Full playback and inspected frames required |
| Programmatic motion | General motion designers | Remotion engineering role with frame deterministic procedure | Engine licence and actual render remain separate |
| Engineering reliability | Broad test/review instructions | Evidence-led diagnosis, reproducible evaluation and receipts | Structural tests are not model-output benchmarks |
| Finance evidence | General controller/price roles | Reconciliation/close/variance procedures with source mapping | No accounting posting, tax certification or invented data |
| Source reuse | Risk of importing role packs and their defaults | Reference-only implementation and per-source licence cautions | No blanket licence clearance or third-party republishing |

## New roles

- **`visual_design_critic`** — Assess rendered design against a brief without imposing a default style.
- **`web_typography_layout_specialist`** — Develop and test typographic hierarchy and responsive layout systems.
- **`conversion_experiment_designer`** — Turn evidence-backed conversion hypotheses into interpretable experiments.
- **`figma_implementation_engineer`** — Reconcile authorized Figma designs with actual code components and runtime behaviour.
- **`creative_frontend_engineer`** — Build expressive interactive websites with accessible low-resource fallbacks.
- **`cms_content_architect`** — Design maintainable content models and editorial publishing workflows.
- **`analytics_instrumentation_engineer`** — Implement testable, privacy-aware product and marketing event instrumentation.
- **`skill_evaluation_engineer`** — Evaluate agent methods with reproducible tasks, evidence and controlled baselines.
- **`storyboard_artist`** — Translate scene beats into readable storyboard panels and shot-to-shot geography.
- **`script_continuity_supervisor`** — Maintain story, prop, wardrobe, action and spatial continuity across shots.
- **`animatic_editor`** — Test narrative pacing in a frame-accurate storyboard edit before full production.
- **`ai_video_prompt_adapter`** — Translate a shot specification into model- and interface-specific video prompting.
- **`generative_video_qc`** — Inspect generated clips for temporal, reference, continuity and delivery failures.
- **`remotion_video_engineer`** — Implement deterministic frame-based videos and graphics in authorized Remotion projects.

## Existing roles changed

| Role | Change | Method |
|---|---|---|
| `design_director` | deepen_existing | visual-direction |
| `digital_design_director` | deepen_existing | visual-direction |
| `brand_identity_designer` | deepen_existing | visual-direction |
| `art_director` | deepen_existing | visual-direction |
| `design_researcher` | deepen_existing | visual-direction |
| `product_designer` | deepen_existing | visual-direction |
| `design_system_designer` | deepen_existing | typography-responsive |
| `junior_designer` | deepen_existing | typography-responsive |
| `production_designer` | deepen_existing | typography-responsive |
| `frontend_prototyper` | deepen_existing | figma-implementation |
| `qa_engineer` | deepen_existing | web-acceptance |
| `accessibility_specialist` | deepen_existing | web-acceptance |
| `accessibility_tester` | deepen_existing | web-acceptance |
| `test_automation_engineer` | deepen_existing | web-acceptance |
| `frontend_engineer` | deepen_existing | web-engineering |
| `senior_frontend_engineer` | deepen_existing | web-engineering |
| `fullstack_engineer` | deepen_existing | web-engineering |
| `performance_engineer` | deepen_existing | web-engineering |
| `software_architect` | deepen_existing | web-engineering |
| `organic_discovery_strategist` | deepen_existing | growth-measurement |
| `seo_content_researcher` | deepen_existing | growth-measurement |
| `marketing_strategist` | deepen_existing | growth-measurement |
| `crm_lifecycle_strategist` | deepen_existing | growth-measurement |
| `marketing_analyst` | deepen_existing | growth-measurement |
| `bug_investigator` | deepen_existing | engineering-evaluation |
| `code_reviewer` | deepen_existing | engineering-evaluation |
| `dependency_researcher` | deepen_existing | engineering-evaluation |
| `llm_engineer` | deepen_existing | engineering-evaluation |
| `context_steward` | deepen_existing | engineering-evaluation |
| `film_director` | deepen_existing | film-direction |
| `cinematographer` | deepen_existing | film-direction |
| `junior_art_director` | deepen_existing | film-direction |
| `visual_prompt_engineer` | deepen_existing | ai-video |
| `generative_media_director` | deepen_existing | ai-video |
| `video_editor` | deepen_existing | continuity-qc |
| `media_delivery_qc` | deepen_existing | continuity-qc |
| `postproduction_supervisor` | deepen_existing | continuity-qc |
| `comfyui_workflow_engineer` | deepen_existing | remotion-comfy-colour |
| `comfyui_node_developer` | deepen_existing | remotion-comfy-colour |
| `color_pipeline_engineer` | deepen_existing | remotion-comfy-colour |
| `media_pipeline_engineer` | deepen_existing | remotion-comfy-colour |
| `motion_designer` | deepen_existing | remotion-comfy-colour |
| `financial_controller` | deepen_existing | finance-evidence |
| `bookkeeping_coordinator` | deepen_existing | finance-evidence |
| `pricing_margin_analyst` | deepen_existing | finance-evidence |
| `production_cost_controller` | deepen_existing | finance-evidence |
| `agency_orchestrator` | update_routing | focused routing |
| `product_software_orchestrator` | update_routing | focused routing |
| `production_orchestrator` | update_routing | focused routing |

## Not imported or automatically changed

No wholesale third-party prompt import, no extra agent runtime, no hooks/auto-approval profiles, no paid integrations, no global memory training, no default deployment provider. Existing account/permission, private knowledge, multi-company/client and communication safeguards remain. No role is deleted or merged based only on lexical similarity.

`openai/skills` was found to be deprecated in the inspected README; the selected official reference is `openai/plugins`. Its methods are studied without changing ACO back into a plugin. Browser-use, LangGraph, CrewAI and OpenHands are different runtime/integration decisions, not interchangeable prompt upgrades, and were not included in these 15 catalogue comparisons.

## Licence observations

ACO's supplied proprietary licence is preserved. No upstream code/prompt files or datasets are vendored by this upgrade. Research links and catalogue labels identify sources; they do not grant any new rights over those projects. **Serge Shima / smixs visual-skills** is credited as a research source. Its current LICENSE is CC BY 4.0 despite an older cached README claiming MIT. Anthropic document skills have separate terms. The inspected Remotion skills mirror has no top-level LICENSE; do not infer its terms from a different project. If future changes copy protected source expression/code, preserve the actual applicable licence/notice and obtain review before distribution.

## Evidence status

The baseline suite was actually run: 166 tests passed before editing. The updated suite and smoke results are recorded in [TEST-REPORT-0.5.0.md](TEST-REPORT-0.5.0.md). A live local-browser smoke was attempted but the environment returned ERR_BLOCKED_BY_ADMINISTRATOR; no policy bypass or successful browser capture is claimed. No Runway/Veo/Kling/Seedance/ComfyUI paid/GPU generation or paired model-output evaluation was run.

## How to tell whether the upgrade helps your work

Use the controlled [evaluation protocol](SPECIALIST-EVALUATION.md) on the same brief/assets/model/tool budget before and after. Look for fewer missing constraints, higher visual fidelity, correct critical flows, better continuity, fewer unsupported provider parameters and usable evidence. Do not count longer responses or more roles as improvements.
