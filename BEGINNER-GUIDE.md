# ACO 0.7.0 — Beginner Guide

**You do not need to know every agent, install 97 tools, or create a folder for every idea.**

## 1. Understand the three places

**GitHub** stores the generic ACO instructions and tools. **Your private knowledge** stores your work, company/client context and selected decisions. **ChatGPT or Codex** is the assistant that reads the relevant instructions and uses tools you actually have.

ACO is not a plugin to submit to a directory. Downloading it does not connect Drive, Gmail, WhatsApp or any account. It does not run when a conversation is closed unless a separate, real scheduler has been configured.

## 2. You have an older ACO repository: update it first

1. Download the complete 0.7.0 ZIP and extract it into a **new folder**. Do not drop it over your old checkout.
2. Open your existing `ACO-agents` checkout in Codex. Make the extracted new folder available to Codex too.
3. Paste this:

```text
Update this ACO repository using the new 0.7.0 package.
Read docs/CODEX-MIGRATION-PROMPT.txt FROM THE NEW PACKAGE.
Follow its safe preview, backup, migration, validation and tests.
Preserve .git, history, private, untracked and unrelated files.
If checks pass, commit and push normally only when safe.
No force push. Do not modify Drive or install external software.
Report the commit, tests and actual push result.
```

4. Codex should preview changes and stop on unrecognized edits. Give it the source/target paths when asked. Do not answer a collision by ordering it to delete everything.
5. A completed push updates GitHub only. Continue below if you also use locally installed skills.

No local checkout yet? Ask Codex to clone the repository you own/access, verify the remote, then use the new-package migration procedure. Do not initialize a second repository inside the extracted `ACO-agents` folder by mistake. The package folder should be the source, not a nested directory accidentally committed into the target.

## 3. Choose your interface

### Only ChatGPT

No Python or local installer is needed to read ACO instructions.

Create or use a **private ChatGPT project** and paste the text in `docs/CHATGPT-PROJECT-INSTRUCTIONS.txt` into its instructions. Replace the repository reference if you maintain an authorized different source. This is a normal ChatGPT project, not a paid organization workspace requirement invented by ACO.

The host must have a real way to retrieve the repository or the files you attach. If it cannot read them, attach `CHATGPT.md`, the relevant `SKILL.md` and the specific role/method files requested. Do not upload the ZIP and assume every host can unpack it. Do not let the assistant say “loaded” without actually reading.

Try:

> Use ACO. Help me choose the next practical step for my artistic work. Start by looking at the actual work I provide. Ask only what you need before advising.

### Codex / VS Code on your computer

Use Python 3.11 or newer for the local tools. `python3 --version` shows the version. Install Python from an official or organization-approved source if it is missing.

On macOS, open `Install ACO.command` from the extracted folder, inspect it, and answer the two questions. It installs the 16 skills. Native agent profiles are optional; you do not need every profile for every task. Follow normal macOS security guidance rather than disabling protections.

Or open a terminal in the extracted `ACO-agents` folder:

```bash
python3 scripts/aco_cli.py doctor
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py install --apply
```

Add native profiles only when useful:

```bash
python3 scripts/aco_cli.py install --offices artist-office agency-office product-office --apply
```

Start a new Codex session. Ask it which ACO skill it actually loaded. If discovery fails, explicitly ask it to read the installed `SKILL.md`. Installation verification checks files, not host behavior.

**Create websites and client deliverables in their own work repositories, not inside the public ACO source repository.**

## 4. Add private knowledge only when useful

You can use ACO without persistent memory. To use Drive, connect it separately through the host's available app controls. Authorize the specific private folder and place that reference only in your private instructions.

Say:

> Use this existing private ACO folder. Inspect its current index first. Reuse the canonical records. Do not create empty scaffolding or duplicate documents. Report whether reading and writing are actually available.

If no ACO folder exists:

> Initialize compact ACO knowledge in this approved location. Create only what is needed for my current practice. Ask before creating independent project documents.

If tools are read-only, ACO provides the proposed update in chat or local pending state. It must not say it saved to Drive. No password, token or API secret belongs in an `ACO.md` file.

## 5. Know when ACO should save something

**Stay in chat:** passing thoughts, rough alternatives, disposable copy variants.

**One row/section in the existing ACO record:** useful ideas, calls, leads, applications, proposals, rejections and small active clients/activities/brands.

**A dedicated project document only when justified:** actual commitment/existence plus independent work, substantial complexity or confidentiality. Even an accepted opportunity does not force a folder tree.

**Actual deliverables are allowed:** a requested proposal PDF, edited film, codebase or book is real work, not memory spam. Link it from the record rather than copying its contents into another knowledge file.

For existing clutter, ask for a read-only inventory and a consolidation proposal first. Repository upgrades never authorize private-drive cleanup. See `docs/CLEANUP.md`.

## 6. Use multiple companies or clients safely

Specify the owner when it is not obvious:

> Work for Company A, its publishing activity, Client X, the exhibition catalogue. Do not load Company B's material.

Activities and brands can remain sections inside Company A. A project can link to multiple activities without multiple copies. Two clients with the same display name need separate stable identities. A “current client” belongs to the task/session, not a global setting other chats can change.

Use separate account/project permissions for confidential work. Merely telling an agent “don't look” is not technical access control.

## 7. Useful requests to copy

**Artistic growth**
> Review these three works and the questions I am exploring. Separate observations from interpretation. Build at most three 90-day priorities around making and research, within my actual capacity. Do not find calls until we know what support the work needs.

**Curating**
> Help develop this exhibition question. Relate the proposed works, space, duration and audience. Mark availability, rights and budgets as unconfirmed unless there is evidence. Do not invent artist acceptance.

**Artist relationships**
> Research whether this curator's current programme genuinely relates to the work. Prepare one meaningful invitation, not a generic sales pitch. Do not send it yet.

**Brand and website**
> Use our approved Brand section. Check which claims are researched versus assumed. Propose two distinct directions, test them on real content, then implement the selected one. Review rendered pages rather than approving code alone.

**Social**
> Plan a realistic two-week content cycle for this artist profile. Use only the actual assets and channels we choose. Give final copy and media specifications. Keep it in draft unless I approve an exact publishing packet.

**Production**
> Plan this scene, then adapt shots to the model and interface actually available. Check continuity and edit needs first. Do not claim a prompt has been tested unless we ran it.

**Office**
> Read the relevant conversation with this verified client. Prepare a reply and next actions. Send only after the exact recipient/content approval and a working authorized tool; otherwise give copy-ready text marked not sent.

## 8. Understand execution states

ACO now distinguishes **knowing how** from **being able to do it in this host**. A listed tool is not automatically connected. For a real send, publication, application, deployment, deletion, purchase, signature or access change, ACO checks the actual capability and exact approval first. If the capability is missing, you should receive the finished draft/packet marked accurately as not executed.

After a real action, ACO should keep the provider/artifact receipt and say only what that evidence supports. A queued message is not delivered; an unknown timeout is not safe to retry blindly. The local `execution-*` commands only validate these states and never act on your accounts.

## 9. Tools: menu, not homework

You do not need to install the resource catalogue. ACO should choose the smallest useful addition after checking the actual task. An external tool must be reviewed and authorized separately. Tool availability can be checked without installation:

```bash
python3 scripts/aco_cli.py capability-audit
```

This only locates executables on PATH. It does not test them or check remote accounts. No new CRM or automation platform is needed for a small practice. Spectrum and other protected learning resources are references, not material ACO may freely repackage.

You can inspect ACO itself without changing anything:

```bash
python3 scripts/aco_cli.py context-budget
python3 scripts/aco_cli.py role-stocktake
python3 scripts/aco_cli.py eval-lint
```

These are maintenance checks, not required daily commands. They do not run external tools, edit roles or score your artwork/design.

## 10. End or resume work

At the end say:

> Summarize what changed, what I approved, what was actually verified and the next action. Update the existing canonical record only if useful and writable. Tell me the true save status. Do not create a new session document on Drive.

To resume:

> Continue this exact project. Read the canonical record and current handoff; separate pending ideas from approved work.

In a worktree ACO can maintain one ignored `.agent-context/HANDOFF.md`. It is not proof of a Drive update. A new host session must load the updated ACO instructions after an upgrade.

## 11. Common problems

| What you see | What to do |
|---|---|
| “I can't read the repo” | Confirm the repository/file tool and permissions; provide the necessary files, not imaginary access. |
| “Saved” but no Drive link/receipt | Ask for the actual write/read-back evidence; otherwise treat the update as pending. |
| A file for every rejected idea | Stop, reload `COMPACT-MEMORY.md`, and update an existing pipeline row instead. |
| Existing files would be overwritten | Stop and review the exact collision. Preserve the user's modified version. |
| A command is missing | Use an existing alternative or approve an exact installation plan; no blanket script from the internet. |
| A model/provider is unavailable | Verify current official docs and available tools; do not reuse stale capability claims. |
| Test suite passed, output still looks bad | Local tests do not judge taste. Inspect actual outputs and revise against the brief. |
| Chat keeps the old rules | Start a fresh session or explicitly reload the new version and relevant methods. |

Read the full [README](README.md), [CLI](docs/CLI.md), [Studio checks](docs/STUDIO-CHECKS.md) and [release test report](docs/TEST-REPORT-0.7.0.md) for details.
