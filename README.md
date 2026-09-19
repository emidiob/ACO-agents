# ACO — Art & Commerce Office

**A generic skill library for creative and professional work, with private context and auditable work history.**

Version **0.3.0** · 9 entry-point skills · 246 role definitions · MIT license.

ACO is **not a ChatGPT plugin** and is not submitted to an app directory. ChatGPT can read its Markdown instructions through an available authorized repository/file tool. Codex can also install the skills and optional native agent profiles locally. The library does not include a model, an always-on agent service, account credentials or anyone's private knowledge.

**New here?** Read [Start here — English](docs/START-HERE.md) or [Inizia qui — Italiano](START-HERE-IT.md).

## Contents of this manual

[1. What it does](#1-what-you-can-use-aco-for) · [2. How it works](#2-how-it-works) · [3. ChatGPT setup](#3-use-in-chatgpt-no-local-installation-required) · [4. Codex setup](#4-use-in-codex-or-vs-code) · [5. Private knowledge](#5-private-knowledge-and-first-setup) · [6. Multiple businesses and clients](#6-multiple-organizations-activities-clients-and-brands) · [7. Everyday use](#7-everyday-use) · [8. History](#8-history-and-handoffs) · [9. Local tools](#9-executable-local-tools) · [10. Updates](#10-update-uninstall-and-recover) · [11. Old repository migration](#11-replace-the-old-plugin-repository-safely) · [12. Limits](#12-what-is-and-is-not-automatic) · [13. Troubleshooting](#13-troubleshooting) · [14. Files](#14-repository-layout) · [15. Testing](#15-testing-and-contributing).

## 1. What you can use ACO for

| Office | Typical work | Deliverables |
|---|---|---|
| Artist | Research, critique, practice planning, curating, grants, exhibitions, editions, sales and commissions | Practice plan, research dossier, critical text, application, technical rider, revenue options |
| Organization | Cultural/research programmes, publishing, partnerships, funding, operations and commercial structure | Programme, editorial plan, partnership brief, operating model, production plan |
| Agency | Brand strategy, identity, copy, creative direction, film/photo production, marketing, social and client delivery | Strategy, creative territories, campaign, treatment, quotation, production plan |
| Product | Websites, apps, UX, frontend/backend, AI features, testing and release preparation | Requirements, prototype, code, test evidence, bug diagnosis, documentation |
| Legal | First-pass legal research, contracts, rights and matter organization | Clause review, draft language, rights matrix, questions for qualified counsel |
| Recruitment | Candidate-side job search, CV/portfolio, applications, interviews and offer preparation | Verified shortlist, tailored materials, interview preparation, application history |

The Concierge routes natural-language requests. Context Setup initializes/extends private records. Context Steward records work, decisions, open loops and handoffs. You rarely need to name a specialist.

A role definition is a method, not proof of expert credentials. Legal work needs jurisdiction-appropriate professional review; financial, technical and other consequential outputs need independent verification. Recruitment is **candidate-side**, not an automated employer hiring/ranking system.

## 2. How it works

```
Your request
    → Concierge
    → task scope + relevant skill/role instructions
    → minimum relevant authorized context
    → work through tools actually available
    → result + evidence + private history/checkpoint
```

**Expertise is public and generic. Context is private and changeable.** A company changing direction updates its context, not 33 agents. A different user can use the same library with their own files and permissions.

There are 246 role definitions, not 246 constantly running agents. Only a few are selected for a task. Native Codex subagents may run independently when supported and enabled; ordinary ChatGPT role-based analysis does not become a parallel agent system merely by naming roles. “Junior” describes scope, not a lower price or a different configured model.

The user retains authority. On an artwork, technical or marketing convenience must not silently redefine artistic intent.

## 3. Use in ChatGPT — no local installation required

1. Have access to the ACO repository through an available GitHub/file-reading tool. Connecting GitHub and having access to a repository are separate from write permissions. Product/account availability varies.
2. For continuity, optionally connect Google Drive separately. ACO does not grant that access.
3. Use a ChatGPT project with the [copy-paste project instructions](docs/CHATGPT-PROJECT-INSTRUCTIONS.txt), or provide the bootstrap in an ordinary chat.
4. Add the link to your approved private ACO root **in your private project instructions**, not the public GitHub repository.
5. Start with a request such as:

> Use ACO from `emidiob/ACO-agents`. Read `CHATGPT.md` first. Help me plan the next three months of my artistic practice.

`Use ACO` is an instruction you configure, not a built-in ChatGPT slash command. ChatGPT must actually retrieve the relevant files before saying it is using them. If the repository is unavailable or not indexed, fetch known file paths or attach the required Markdown files; do not pretend it was loaded.

In a shared ChatGPT project, check member access before adding private client context. Use separate private projects where confidentiality requires it. Prompt-level scope rules are not access controls.

## 4. Use in Codex or VS Code

### Mac: easiest path

Download/extract the release to a normal folder. Open **Install ACO.command**. It checks the Python environment and asks whether to install the nine skills and, optionally, all native agents. The terminal may require macOS approval to run a downloaded script. Do not disable system security globally; inspect the script and follow your organization's policy.

**Prerequisite:** Python 3.11 or newer. Run `python3 --version`. If missing, install a current Python from [python.org](https://www.python.org/downloads/) or your approved package manager. Native local tools support macOS/Linux; use WSL on Windows. No Python is required merely to read the skills in ChatGPT.

### Terminal: reproducible path

In the extracted ACO folder:

```bash
python3 scripts/aco_cli.py doctor
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py install
```

The last command is a **dry run**. To install:

```bash
python3 scripts/aco_cli.py install --apply
```

This installs nine skills, **without** all 246 optional native agents. For selected native agents:

```bash
python3 scripts/aco_cli.py install --offices artist-office agency-office product-office --apply
```

For every profile:

```bash
python3 scripts/aco_cli.py install --offices all --apply
```

For a project-local installation:

```bash
python3 scripts/aco_cli.py install --project /absolute/path/to/work-project --offices product-office --apply
```

The project must already exist. Global skills go under `~/.agents/skills/aco-*`; optional native agents under `~/.codex/agents/aco-*.toml` (or the configured Codex home). Project installs use `.agents/skills/` and `.codex/agents/`. ACO never overwrites your global AGENTS.md or disables approval/sandbox settings. Native agent names are prefixed `aco_` to avoid collisions with generic existing agents.

Restart/start a new Codex session and ask it to use ACO. If automatic discovery is unavailable in your host/version, explicitly read the relevant SKILL.md and methods. A valid TOML parse does not prove your particular host loaded it: verify the selected skill/profile in that host.

**Keep the library checkout separate from work repositories.** Build a client's website in that client's project, not in the public ACO repository.

## 5. Private knowledge and first setup

Drive is optional. With connected Drive read/write tools, tell ACO:

> Set up my private ACO knowledge in this folder. Create the missing control files, verify the result, and do not overwrite existing content.

After authorization, the skill directs the host to create/reuse the base structure, register actual IDs and verify each step. The user should not create every folder manually.

```
ACO — Art & Commerce Office/
  KNOWLEDGE-INDEX
  00-System/
    REGISTRY
    Setup-Journal/
    Sync-Receipts/
  Personal/
  Organizations/
  Archive/
```

The index/registry may be native Google Docs or raw Markdown/JSON according to the connected tools. Store the actual file type and ID. Native Docs support revision-controlled updates where exposed; raw files without conditional writes require single-writer coordination or immutable proposals. Do not mix several registry formats as separate competing sources of truth.

Only create artist/career/company/client/project contexts when needed. Each active scope gets Context, History and Handoffs; history includes immutable Events/Sessions and readable Work Log, Decisions, Open Loops and Context Changelog views. Re-running setup preserves data and resumes recorded steps rather than duplicating everything.

Drive folder names are not unique and search-then-create is not atomic. Serialize initial setup and registry restructuring. Ordinary work uses separate session/event IDs. See [Drive workflow](docs/DRIVE-KNOWLEDGE.md).

## 6. Multiple organizations, activities, clients and brands

```
Organizations/
  organization-A/
    Context
    Activities/Design ... Publishing ... Research
    Clients/client-X ... client-Y
    Brands/brand-X
    Projects/project-1 ... project-2
    History/
  organization-B/
    ...
```

An **organization** is your business or organization. An **activity** is a business line within it. A **client** is a relationship belonging to that organization. A **brand** belongs to the organization or a client. A **project** has one canonical folder and may reference multiple activities, one client and one brand. Names are labels; IDs resolve identity.

> For my second company, add a publishing activity and a new client called North. Create a book project involving publishing and design.

ACO resolves the organization first. Another company's client with the same name is not reused automatically. When ambiguous, it asks one necessary question. A single project spanning two activities is linked, not duplicated. Cross-organization collaboration needs explicit data-sharing boundaries and is not silently allowed by the local tools.

Each chat/task has its own locked scope. There is **no global current client** shared by concurrent sessions. If a task changes organization/client, create a new session. For genuine confidentiality, also use appropriate provider permissions and separate chats/projects as needed.

## 7. Everyday use

You brief the job, not an org chart:

> Use ACO. Plan my practice for the next 12 months. Protect research/making time and build realistic revenue options.

> Use ACO. For company A, design activity, client X, prepare a proposal for a brand identity and website. Do not contact the client yet.

> Use ACO. Continue project Y from its last verified handoff. First tell me what is completed, uncertain and still open.

> Use ACO. Find active jobs that match my approved career context; check the application history before suggesting a duplicate.

> Use ACO. Review this contract from my side. Identify jurisdiction assumptions and issues for qualified legal review.

> Use ACO. Critique this work without fetching my personal context. If this chat already contains it, explain that a clean session is needed for a genuinely blind assessment.

Context modes: **NONE/BLIND** (no private fetch), **LIGHT** (minimum basics), **FULL** (all relevant authorized context, not everything), **BLIND-FIRST** (independent first stage, then a separately contextualized stage).

## 8. History and handoffs

Substantial work is recorded at milestones and closing, not inferred from memory later. An event distinguishes **proposed**, **approved**, **executed** and **verified**. An approved decision needs its user-approval reference. A successful build/test/send/save needs actual evidence.

```
work-project/.agent-context/sessions/<session-id>/
  SESSION.json
  CURRENT-BRIEF.md
  RELEVANT-CONTEXT.md
  WORK-LOG.md
  DECISIONS.md
  OPEN-LOOPS.md
  CHANGES.md
  HANDOFF.md
```

The local tools refuse to start a private handoff when these paths are already tracked by Git. Ignore rules alone do not unpublish previously tracked files. Keep the packet minimal; never export entire inboxes or unrelated client context.

A local save is **LOCAL VERIFIED**, not **DRIVE VERIFIED**. A remote write needs a read-back and receipt. Unconfirmed writes stay **PENDING**. Conflicts preserve originals. Canonical context changes require a proposal against the version/hash originally read and an approved change; no silent last-writer-wins.

See [History and synchronization](docs/HISTORY-AND-SYNC.md). These rules improve auditability but are not cryptographic proof that a human approved a decision.

## 9. Executable local tools

The CLI can initialize private local knowledge, create scoped entities, start/checkpoint/close sessions, export approved context, handle context-change proposals and manage installation. It does not run an AI model or watch your computer continuously.

```bash
python3 scripts/aco_cli.py workspace-init
python3 scripts/aco_cli.py entity-add --kind organization --key studio-one --name "Studio One"
python3 scripts/aco_cli.py status
```

Default private location: `~/.local/share/aco/knowledge`. Override with `--knowledge /private/path` (outside Git). In normal assisted use, Codex can run these commands and retain the returned IDs so you need not copy them manually.

Use `--help` on each command, or read [CLI reference](docs/CLI.md). There is also an installed minimal runtime under `aco-office-concierge/runtime/` for knowledge/session/event commands; use the full source checkout for install/update/migration/validation.

**Optional advanced Drive event bridge:** an explicitly configured local OAuth access token can transfer immutable session events with retry IDs and read-back receipts. It does not synchronize all Drive files or apply canonical context changes. It is not required for the connected-tool ChatGPT workflow. Its provider contract is tested with a fake provider; live Google authorization and your host must be tested separately. See [optional bridge](docs/OPTIONAL-DRIVE-BRIDGE.md).

## 10. Update, uninstall and recover

Pull/download a reviewed ACO version, then rerun `install`. With no `--offices` argument it preserves your existing selection (skills-only on first install). Supply `--offices` to deliberately change the selection; `--offices none` explicitly removes managed native roles while retaining skills. It replaces only unchanged ACO-managed files. Local edits block updates unless you explicitly choose `--backup-modified`, which backs them up before replacing them. Unmanaged files are never overwritten. Existing unprefixed agents from an older ACO installation are left untouched; inspect them separately before removing duplicates.

```bash
python3 scripts/aco_cli.py install-status
python3 scripts/aco_cli.py install --offices all --apply
python3 scripts/aco_cli.py uninstall                 # preview
python3 scripts/aco_cli.py uninstall --apply         # only ACO-managed files
python3 scripts/aco_cli.py install-recover           # interrupted transaction
```

Use the same `--project`, `--home` or `--codex-home` options as the original installation. Backups and installation inventory live under the user's private ACO installation-state directory. Knowledge is not removed by uninstalling. A process interrupted mid-write leaves a journal; recover it before another install. Do not delete state/backups to suppress a conflict.

GitHub changes do not automatically update installed local copies. Restart the host after updating. ChatGPT should read the chosen repository revision for each task instead of combining instructions from different releases.

## 11. Replace the old plugin repository safely

**Do not delete the GitHub repository or `.git/`.** The migration removes known obsolete plugin files and imports the new release on a work branch, preserving history, unrelated tracked files and untracked private files.

Extract this release outside the old repository. From the new release:

```bash
python3 scripts/aco_cli.py migrate --target /absolute/path/to/old/ACO-agents
python3 scripts/aco_cli.py migrate --target /absolute/path/to/old/ACO-agents --apply
```

The second command creates a backup branch and a migration branch, then stages the exact changes. It **does not commit or push**. Review the diff, run all tests/validation and only then commit/push under your authorization. Unknown edits, dirty tracked work or untracked collisions stop migration.

Use the [Codex migration prompt](docs/CODEX-MIGRATION-PROMPT.txt). Drive migration is separate and journaled; this script never touches Drive. No force push, `git clean`, recursive deletion of the checkout or changed license.

## 12. What is and is not automatic

| Mechanism | What it actually does |
|---|---|
| Readable skills | Tell an available host model how to route, research, create/check records and work; they are not a service |
| Connected Drive workflow | Can perform scoped setup/reads/writes during the run when the host exposes authorized tools; otherwise returns a pending packet |
| Local CLI | Executes deterministic local file operations with checks, IDs, locks and journals |
| Optional REST bridge | Sends explicit immutable events after local OAuth configuration; no continuous sync or canonical-context overwrite |
| Native Codex agents | Optional prefixed role profiles; actual delegation depends on host support/tools |
| Always-on monitoring | **Not installed.** Requires a separately configured scheduler/runtime and explicit authorization |

The user still authorizes accounts, selects the initial root, supplies unknowable facts and approves consequential actions. Sending mail/applications, spending, publishing, sharing permissions, production deployment and legal commitments are not silently authorized by using ACO.

## 13. Troubleshooting

| Problem | Safe response |
|---|---|
| “ACO wasn't loaded” | Fetch CHATGPT.md and the required skill/method explicitly; check repository access |
| GitHub search returns nothing | Fetch concrete paths at a known revision; indexing may be incomplete |
| Drive is read-only | Work from read context; label new records pending/not saved |
| Two matching folders/clients | Resolve IDs using the registry; do not create a third |
| Installation collision | Preserve the existing file; inspect the plan rather than force-overwriting it |
| Local ACO file modified | Preserve it or use explicit backup-modified after review |
| Installation interrupted | Run install-recover with the same destination options |
| A client context appears in another job | Stop, check scope and start a clean appropriately isolated session |
| Context changed during work | Re-read, reconcile the proposal and preserve the old version |
| “Saved” but no remote receipt | Treat it as pending until a remote read-back confirms it |
| Wrong Python version | Use Python 3.11+; `doctor` reports the actual interpreter |
| Native profiles not visible | Verify host version, installation path and discovery; restart a session |

## 14. Repository layout

```
CHATGPT.md / AGENTS.md       entry points
ACO-INDEX.md / catalog.json exact role routing and dependencies
skills/                     9 skills, canonical role methods and protocols
assets/context-templates/   blank generic templates
extras/codex-custom-agents/ generated prefixed native profiles
scripts/                    installer, migration, local records, optional bridge, validation
tests/                      automated local and fake-provider tests
docs/                       setup, workflows, migration, limitations and sources
release/                    versioned manifest and legacy-file fingerprints
```

Canonical agent methods exist once in Markdown. `scripts/generate.py` generates TOMLs, catalogues, template mirrors and the installed minimal runtime. Do not edit generated files directly.

## 15. Testing and contributing

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

After intentional source changes:

```bash
python3 scripts/generate.py
python3 scripts/build_manifest.py
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

The manifest detects accidental changes; it is not a signed proof of publisher identity. The basic secret scan is not a guarantee that no sensitive information exists. Review staged diffs and provider permissions before publication.

See [validation report and limits](docs/VALIDATION.md), [security model](SECURITY.md), [architecture](docs/ARCHITECTURE.md) and [dated official documentation](docs/SOURCES.md).

ACO is distributed under the existing **MIT License**, which permits reuse and redistribution under its terms. No private knowledge is distributed here. The number of roles is not a professional-quality certification or a guarantee that every host/integration has been tested.
