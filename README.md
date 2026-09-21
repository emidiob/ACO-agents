# ACO — Art & Commerce Office

**A working library for an artist, studio, agency or cultural business — with scoped private knowledge and evidence-aware execution.**

**ACO v0.7.0 · 363 roles · 16 entry skills · 61 workflows · 97 optional resources.**

Proprietary, source-available. Redistribution is restricted by [LICENSE](LICENSE). No third-party software, fonts, models or private knowledge are bundled.

**Start with [BEGINNER-GUIDE.md](BEGINNER-GUIDE.md).** For an existing checkout, use the [Codex upgrade prompt](docs/CODEX-MIGRATION-PROMPT.txt). For this release's decisions, see [What's changed](docs/UPGRADE-0.7.0.md).

## What ACO is — and is not

ACO is a set of task methods plus optional local Python tools. ChatGPT reads the relevant instructions through an available authorized repository/file tool. Codex can install the skills and optional native agent profiles.

It is **not a ChatGPT plugin, a model, an always-on team, a professional accreditation or an automatic connection to your accounts**. Saying a role's name does not launch an independent process. A host that supports native subagents may run them separately; otherwise role methods guide the current assistant.

The public library supplies expertise and procedures. Your private knowledge supplies the current practice, organizations, clients, decisions and constraints. These must stay separate.

## The operating model

```text
A natural request
  → resolve the actual practice / company / client / project
  → read only the relevant methods and authorized context
  → ask up to three decisive missing questions, early
  → do the work with real available tools
  → inspect the result and disclose unrun checks
  → update compact memory only when something material changed
```

No office-by-office performance or unnecessary planning ceremony. A simple request should receive a simple result. A commissioned essay, design system or codebase still needs a complete deliverable.

**Artistic authority remains with the artist.** Do not construct a practice around open calls or sales metrics. Do not mistake approved strategy for validated evidence.

## Which work can it handle?

| Office | Typical requests |
|---|---|
| Artist | Practice development, critical dialogue, curatorial research, portfolio, residencies, relationships, editions and sustainable income |
| Organization | Cultural programmes, organizational direction, partnerships, research, publishing and operations |
| Agency | Brand research, positioning, naming, voice, identity, web art direction, campaigns and social strategy |
| Product & Engineering | Websites, applications, prototypes, databases, integrations, AI features, debugging, security review and release work |
| Production & Post | Film direction, storyboard, video prompts, ComfyUI, photography, editing, grading, retouch, CG, sound and delivery |
| Publishing & Media | Books, catalogues, magazines, editorial production, research, rights, metadata, digital publications and newsletters |
| Finance | Budgets, margins, cash forecasts, billing, records and adviser preparation — not bank or tax authority |
| Commercial | Qualified leads, offers, tenders, relationships, pipeline and retention |
| People & HR | Staffing, sourcing, structured interviews, onboarding and restricted personnel processes; human employment decisions |
| Delivery | Plans, dependencies, capacity, change control and acceptance across projects |
| Administration | Inbox, appointments, minutes, documents, travel and authorized email/WhatsApp/call operations |
| Legal | Issue spotting, source-based research, draft clauses and questions for qualified counsel |
| Recruitment | Candidate-side job discovery, CV/portfolio, applications, interviews and offers |

The **Concierge** routes; **Context Setup** initializes the minimum knowledge structure; **Context Steward** records actual work and approved changes. Browse the [visual agent catalogue](docs/AGENT-CATALOG.md) or [exact role paths](docs/ALL-ROLES.md). Usually you do not need to pick individual agents.

## What makes 0.7.0 different?

0.7.0 is the **Execution & Integration** release. It keeps the 363 roles, 16 entry skills, 61 workflows, 97 optional resources, Compact Memory and the 0.6.2 router. The change is not more personas: ACO now has a formal boundary between knowing how to do work and being able to perform a real external action.

The execution layer distinguishes `LEARNED_SKILL`, `REFERENCE`, `OPTIONAL_TOOL`, `CONNECTED_INTEGRATION`, `LOCAL_RUNTIME`, `UNAVAILABLE` and `BLOCKED`. Consequential actions use explicit permission levels, an exact action-packet hash, host-supplied adapters and evidence-bearing receipts. ACO can therefore say **prepared**, **ready to execute**, **executed**, **sent**, **delivered**, **published** or **unknown** without collapsing those states.

The local commands are deliberately non-executing: `execution-plan` resolves readiness, `permission-check` binds approval to an exact action, `receipt-check` validates outcome claims, `adapter-check` validates host metadata, `workflow-check` checks state transitions, and `execution-summary` produces an operational log without exposing hidden reasoning. Actual provider calls still belong to the authorized host.

A deterministic execution-policy benchmark is now part of the release gate alongside the frozen routing regression and behavioral simulation. See the [architecture guide](docs/ARCHITECTURE.md), [execution protocol](skills/aco-office-concierge/references/protocols/EXECUTION.md), [evaluation guide](docs/EVALS.md) and [upgrade notes](docs/UPGRADE-0.7.0.md).

## Use in ChatGPT

1. Make the repository available through an authorized repository/file-reading tool, or attach the required instructions. Merely typing `Use ACO` does not load files.
2. In a private ChatGPT project, paste [these project instructions](docs/CHATGPT-PROJECT-INSTRUCTIONS.txt).
3. Optionally connect Drive separately and put the approved private root in the **private** instructions, never in this repository.
4. Ask for the work:

> Use ACO from `emidiob/ACO-agents`. Read `CHATGPT.md` first. Review my current artistic development from the work I provide. Start with the work, not opportunities. Ask only what is decisive.

Availability of repository tools, apps, writes and native subagents depends on the host/account. ACO must retrieve the files before claiming to use them. A missing connector does not prevent drafting from materials you provide.

Keep confidential client work in appropriately separated sessions/projects and access controls. Prompt scope rules are **not** security isolation. For a genuinely blind critique, start from a clean input/session rather than asking a model to forget what it already saw.

## Use locally in Codex or VS Code

Reading Markdown needs no local installation. Executing ACO's Python tools requires **Python 3.11+**. macOS/Linux are supported for local tooling; use an appropriately configured WSL environment on Windows. No dependency is downloaded automatically.

Keep the ACO library checkout separate from the work repository. Extract the package, open a terminal in `ACO-agents`, then:

```bash
python3 scripts/aco_cli.py doctor
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py install
```

The last command is an **installation preview**, not a completed install. To install the 16 skills:

```bash
python3 scripts/aco_cli.py install --apply
```

To include selected optional native profiles, or all of them:

```bash
python3 scripts/aco_cli.py install --offices artist-office agency-office production-office --apply
python3 scripts/aco_cli.py install --offices all --apply
```

On macOS, `Install ACO.command` provides a prompted version. Inspect scripts before running. Do not disable system security globally to bypass a warning.

Global skills use `~/.agents/skills/aco-*`; optional profiles use `~/.codex/agents/aco-*.toml` or the configured Codex home. Project-local installation is also supported:

```bash
python3 scripts/aco_cli.py install --project /absolute/path/to/work-project --offices product-office --apply
```

Start a new Codex session and verify host discovery. A validated file copy is not proof the host loaded it. The installer preserves unrelated profiles and does not replace your global AGENTS.md. Consult the [CLI guide](docs/CLI.md) for update, recovery and uninstall commands.

## Compact private knowledge

**Pipeline ≠ project. Tool bookmark ≠ knowledge file.**

A speculative idea can stay in chat. Worthwhile opportunities, applications, prospects and proposals are rows in an existing owner's `ACO.md`. A rejection changes status; it does not create an archive folder. Client, activity and brand details usually remain sections.

Dedicated records require actual commitment or import of an existing entity **and** meaningful independence, size or confidentiality. Existing documents are linked, not duplicated. Real requested deliverables — a contract, application, film, budget or software project — are still allowed.

A possible structure, created lazily:

```text
ACO/
  ACO-INDEX.md
  Personal/Artist/<actual-practice>/ACO.md
  Organizations/<actual-company>/ACO.md
  Projects/<independent-active-project>/ACO.md
```

Do not create placeholder companies, projects or empty folder trees. Multiple organizations can have identically named clients without sharing identity or private context; scopes have stable identifiers. Do not use a global “current client” shared across simultaneous tasks.

Each canonical record holds context, brief, confirmed decisions, open loops, selected recent work and references. A technical session database lives outside the knowledge tree. Worktree handoff uses one ignored `.agent-context/HANDOFF.md`, not a permanent Drive file per session.

A local mirror is not a Drive write. Connected workflows must update the actual canonical file, check its revision and read it back. Otherwise report **pending / not saved remotely**. See [Compact Memory](docs/COMPACT-MEMORY.md), [Drive](docs/DRIVE-KNOWLEDGE.md), and [History and sync](docs/HISTORY-AND-SYNC.md).

Existing clutter is a separate migration: inventory → reviewed consolidation → verification → explicitly approved quarantine. Never delete original artwork, contracts, source files or client documents as routine cleanup. See [cleanup and recovery](docs/CLEANUP.md).

## A small toolkit, chosen per task

The [resource catalogue](docs/RESOURCE-CATALOG.html) includes the user's earlier selections plus 35 curated additions. **None is installed or connected by this package.** Existing entries retain their review provenance; only the new selection was reviewed for this consolidation.

Default: use the current host and current software. For artistic research, Zotero/Tropy/Mirador can help when the task warrants them. For web QA, existing browser tools plus optional axe-core/Lighthouse can provide evidence. FFmpeg/OTIO/OIIO can support media delivery. Twenty, Plane, n8n and Omeka are scale-dependent options, not a mandatory office stack.

```bash
python3 scripts/aco_cli.py resource-search --query "curatorial research"
python3 scripts/aco_cli.py capability-audit
```

The second command **only checks a fixed allowlist of executables on PATH**; it runs none, reads no credentials and discovers no remote accounts. A registry entry, local executable, connected capability and verified result are four different facts.

Some learning sources are reference-only. In particular, Spectrum's commercial reuse terms require separate scrutiny; ACO does not reproduce the standard or claim conformance. Creative Capital written course access is currently limited according to the publisher page; do not promise access from a bookmark. See [source review and selection](docs/SOURCE-REVIEW.md).

## Practical readiness checks

These optional checks accept JSON and return issues. They do not create private files or act on accounts. You do not need to fill a JSON form for an ordinary conversation; a host can prepare one when a structured check adds value.

```bash
python3 scripts/aco_cli.py practice-check --input examples/studio/practice.json
python3 scripts/aco_cli.py opportunity-check --input examples/studio/opportunity.json --as-of 2026-09-20T12:00:00+00:00
python3 scripts/aco_cli.py brand-check --input examples/studio/brand.json
python3 scripts/aco_cli.py social-check --input examples/studio/social-draft.json
```

Opportunity examples are fictional fixtures, not real calls. The explicit `--as-of` is for repeatable tests only; real work uses today's date and fresh source evidence.

A social publication approval must match the exact scope, account, packet version, media hashes and timing. Even a consistent packet returns **host review required**, never an authorization token. Unknown prior sends are reconciled before retries. Without a verified tool, produce copy-ready text labeled **not sent** outside the message. See [Studio checks](docs/STUDIO-CHECKS.md).

## Execution readiness and receipts

For consequential host actions, ACO can prepare a machine-readable packet and check whether the actual capability, permission and previous-action state are sufficient. The CLI itself never performs the external action.

```bash
python3 scripts/aco_cli.py permission-check --request examples/execution/email-send-request.json
python3 scripts/aco_cli.py execution-plan --request examples/execution/email-send-request.json --inventory examples/execution/email-inventory.json
python3 scripts/aco_cli.py receipt-check --input examples/execution/email-sent-receipt.json
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
```

Use the returned action hash to bind explicit approval when the permission level requires it. After the real host adapter acts, record only the strongest outcome supported by its receipt. See [Execution](skills/aco-office-concierge/references/protocols/EXECUTION.md).

## What has and has not been verified

[The release test report](docs/TEST-REPORT-0.7.0.md) records the tests actually run, with explicit scope and limitations. Unit tests check local behavior, not taste, curatorial expertise, improved revenue or legal accuracy. Supplied evidence references are not proof of truth.

This package does not establish that your Mac, Codex session, Drive connector, phone account, ComfyUI GPU or paid generation service works. It installs no schedules and makes no calls. [Host acceptance tests](docs/HOST-ACCEPTANCE-TESTS.md) are for your actual environment; unrun rows stay unrun.

## Updating GitHub and local installs

Use [the migration prompt](docs/CODEX-MIGRATION-PROMPT.txt) from the **new** package. The script creates a backup/work branch, changes recognized ACO-managed files, and stops on collisions or unrecognized edits. Preserve `.git`, private and unrelated files; no blanket deletion, `git clean`, hard reset or force push.

Pushing GitHub does not update local skills or reload an existing chat. Re-run the local installer from the new package when authorized; start a new host session. Do not clean Drive as part of a repository update.

## Maintainer map

```text
README.md / BEGINNER-GUIDE.md  → human entry points
CHATGPT.md / AGENTS.md        → host entry points
skills/                      → canonical role instructions and protocols
extras/codex-custom-agents/   → generated native Codex profiles
catalog.json / ACO-INDEX.md   → generated lookup, not a giant startup prompt
scripts/                     → stdlib local tools, safe installer and migration
tests/                       → repeatable local checks
examples/                    → fictional plans and check inputs
docs/                        → task methods, beginner/upgrade guides and limitations
release/manifest.json        → packaged file hashes
```

After source changes, regenerate and validate; never hand-edit generated native profiles:

```bash
python3 scripts/generate.py
python3 scripts/build_manifest.py
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --output /absolute/path/outside/repo/ACO-release.zip
```

The [product decisions](docs/PRODUCT-DECISIONS.md), [source review](docs/SOURCE-REVIEW.md) and [known limits](docs/KNOWN-LIMITATIONS.md) are part of the release. Keep the proprietary license and third-party rights distinctions intact.
