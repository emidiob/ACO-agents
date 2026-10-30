---
name: aco-office-concierge
description: "Front door: resolve the request, minimal team, scope and context; coordinate work and verified continuity."
---

# Aco Office Concierge

Use this skill only for the task it covers. This is a readable workflow, not a plugin, connection or guarantee of autonomous work.

The short native commands `/aco` and `/aco-genjutsu` are thin aliases into this Concierge and Production Office. See `../../docs/ACO-COMMANDS.md` in the source checkout for the complete command menu.

## Start
Read `references/protocols/CONCIERGE.md`; for substantial dependent work apply `references/protocols/GOAL-EXECUTION.md`, and apply `references/protocols/DELEGATION.md` before returning a delegated professional judgment to the user, and use the common permissions/context contract as needed. Start from the local `references/ROLE-INDEX.md` when present, or `../aco-office-concierge/references/ROLE-INDEX.md` for shared methods. Read only the selected role files. The full `../aco-office-concierge/references/CATALOG.json` is a machine lookup fallback; do not load it wholesale by default. For GitHub reads, paths are relative to repository root under `skills/`.

The lead role is `office_concierge` (native Codex name: `aco_office_concierge`). Read its full instructions using the catalogue; do not rely only on its title.

## Work and evidence
Resolve the current scope and available tools. Read relevant approved context or perform a blind first pass as requested. Use the smallest effective team; a role label does not start a real subprocess. Respect user approval for consequential actions. External factual claims require appropriate current sources.

Checkpoint substantial work using the context steward and the history protocol. Close with deliverable, unresolved risks and actual persistence status. Never pretend a local handoff updated Drive.

## Interaction default
When professional judgment is delegated, resolve it from sufficient evidence and act. Ask essential missing facts/preferences/scope/authorization early only when they materially change the work; otherwise do not turn the task into a questionnaire. Keep action updates brief and the requested deliverable complete. Follow `references/protocols/INTERACTION.md`. External messaging/calls/publishing use the same folder’s `COMMUNICATIONS.md`.


## Specialist work — v0.5.0

For realistic still-image prompting and photographic style comparisons, route to [ACO Capture](references/playbooks/ACO-CAPTURE.md) on demand, with one coherent camera style per image. This is a prompt-writing playbook, not a newly activated image-model adapter.
For design/web work, distinguish creative direction, design-to-code, browser acceptance and content/measurement. For AI video, distinguish direction/boards, provider prompting, graph implementation and rendered-clip QC. Read the relevant office ROLE-INDEX and selected methods only. Do not load the research comparison matrix during normal work. Avoid imposing source-repository aesthetic bans or downloading their tools.


## Shared context and resource defaults
[Compact Memory](references/protocols/COMPACT-MEMORY.md) replaces the former event/session file layout. Keep ideas, applications, leads, proposals and rejected items in chat or compact pipeline rows; active small items may remain sections. Do not create files merely for sessions, status changes, decisions or handoffs. Requested deliverables are not memory clutter. Existing files require reviewed consolidation, never automatic deletion.

Use the [resource index](references/resources/INDEX.md) only when a relevant capability or reference improves the task. Choose a few candidates, read their exact entries and linked original methods, and verify actual host access. Resources are optional, not installed dependencies. No guessed identities, unapproved asset purchases, private-code uploads or account changes.

## Studio release selection — v0.6.0
Start from the existing task scope, not a tour of all offices. For artist growth, route to practice work/critical development before open-call discovery. For brand/social, reuse the compact Brand section and distinguish assumptions, approved direction and validated evidence. Use the optional registry only when it adds a missing capability. A registry entry, a PATH executable, a connected action and an execution receipt are four different states.

The local `capability-audit` command checks PATH presence only. It does not inspect credentials or discover remote accounts. Use the host's actual connector schemas for connected services. Optional `practice-check`, `opportunity-check`, `brand-check` and `social-check` read a supplied JSON plan and produce blockers; none writes to Drive or sends anything. Simple requests must not be burdened with forms.


## Integration and Hybrid Memory — v0.7.1
Use [Hybrid Memory](references/protocols/HYBRID-MEMORY.md) to route durable semantic context, current repository source, rebuildable code intelligence, temporary task context, research corpora and receipts to the right store. Do not ask the user to connect Drive merely to begin or improve memory.

Use [Integration discovery](references/protocols/INTEGRATION-DISCOVERY.md) before a real external action when several host adapters may supply the same capability. `integration-resolve`, `memory-resolve` and `delegation-resolve` are local decision/validation tools only; they do not connect accounts or execute providers. Optional code-intelligence runtimes remain uninstalled until the current environment and authorization justify them.


## Goal Graph & execution — v0.8.0
Use a Program → Goal → Task → Dependency graph only when continuity and dependencies justify it. `goal-status` chooses a bounded next task; `autonomy-plan` resolves action DAGs through existing capability/permission/receipt contracts. Simulation is side-effect free. The local engine never executes a provider, and a task is not verified until receipts meet its evidence rule. Do not create a file per node or use a graph to cross private scopes.


<!-- ACO-COMPETENCE-LIBRARY-v1.0.7 -->
## Validated professional skillpacks — ACO 1.0.7

When the current task benefits from a professional method, select the applicable office
and read [the competence index](references/competencies/INDEX.md). Use only the
selected `METHOD.md`, `DECISIONS.md`, and `OUTPUT.md`; consult examples, sources and
evaluation evidence when material. Twenty original professional method packs
are also registered as technical ACO skill bodies with status `validated`. The 400
frozen synthetic checks test structured procedural consistency, not professional
judgment or output quality. Original experimental candidates stay gated.
For limits see `docs/PROFESSIONAL-SKILLS.md`.
Preserve author intent, source rights, project/client scope and external-action approval.
CLI: `python3 scripts/competence_library.py show --id visual-critique` in the full checkout.
<!-- END ACO-COMPETENCE-LIBRARY-v1.0.7 -->

## Automatically route visual tasks through Taste (ACO-TASTE-GLOBAL-108)

For any creation, modification, review or delivery of images, photography, film/video, motion, graphics, 3D, web/UI, editorial PDF or presentations, **MUST** load the shared [visual quality gate](references/protocols/VISUAL-TASTE-ROUTING.md) and [ACO Taste Intelligence](../aco-taste/SKILL.md) automatically. Do not require `/aco-taste`. Preserve scope for small edits and verify the real visual artifact.

## Open Design composition

For bounded visual briefs, original token presets, gallery remix, HTML/SVG composition or optional export, use the Open Design CLI in the Concierge runtime: `scripts/aco_open_design.py --help`. Combine it with ACO Taste direction and the automatic visual review gate; inspect actual rendered output before completion. Export availability and external handoff authorization are checked separately.
