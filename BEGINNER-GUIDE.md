# ACO v0.4.3 — Beginner Guide (No Git Knowledge Required)

**What ACO is:** a library of instructions and tools for ChatGPT and Codex. **It is not a plugin and it is not an app you need to open every morning.** You describe the work; ACO selects the relevant roles and uses only the capabilities that are actually available.

**Three separate things:** updating GitHub publishes the library; installing ACO in Codex updates the local copies on your computer; connecting Drive gives ACO access to your private knowledge. None of these automatically does the other two.

## License in two lines

ACO v0.4.3 is **proprietary source-available software**. You may use it personally or internally, privately modify it, and use it to produce commercial work for your own clients. **You may not redistribute ACO, publish forks, resell it, sublicense it, or embed substantial parts of it in products distributed to third parties without written permission.** See `LICENSE`.

## 1. Already have the ACO repository? Update it like this

1. Download and extract the v0.4.3 ZIP into a **new folder outside your existing repository folder**. Do not manually copy only the visible files: the release also contains important hidden files.
2. Open your existing `emidiob/ACO-agents` repository in Codex. Attach the new ZIP or point Codex to the actual extracted release folder.
3. Paste the text below. You do not need to understand the Git commands; Codex should execute them and report exactly what happened.

```text
Update this repository using the ACO v0.4.3 release I supplied.
Read docs/CODEX-MIGRATION-PROMPT.txt FROM THE NEW RELEASE.
Use the controlled migration process: preview, backup, apply, test, and inspect the diff.
Preserve .git, repository history, private files, unrelated files, and local work.
Do not use git clean, reset --hard, broad deletion, or force push.
If all checks pass, I authorize the commit and a safe push to origin/main.
Report the version, commit SHA, test results, and the actual push result.
Do not modify Google Drive and do not install external plugins or services during this migration.
```

**How to check it worked:** after the push, reload the README on GitHub. It should show **0.4.3, 16 skills, and 349 roles**. Administration, Production, and Publishing should appear in the office list. The public repository must not contain your clients, phone numbers, filled private contexts, or Drive files.

If Codex reports modified files or conflicts, do not tell it to delete them. Ask it to compare the changes and preserve your work. A backup is not permission to destroy private data.

## 2. Want to use ACO in ChatGPT?

**You do not need to install anything on your Mac.** You need an authorized way for ChatGPT to read the repository and, only if you want persistent private memory, a separate Drive connection.

Create or use a private ChatGPT project and paste the contents of `docs/CHATGPT-PROJECT-INSTRUCTIONS.txt` into its project instructions. You can also start an ordinary chat with:

```text
Use ACO from the GitHub repository emidiob/ACO-agents.
Read CHATGPT.md and only the skills required for this request.
Ask me immediately for any essential missing information, then work with concise updates.
For now, do not use private data and do not send messages.
```

Then ask normally, for example:

> ACO, prepare the production of a 30-second film. First ask only the essential questions you need answered.

If ChatGPT cannot read the repository, it should say so. Attaching the required Markdown files is a fallback; it does not mean an unread repository has somehow been loaded. Connector availability depends on your environment and account.

## 3. Want to use ACO in Codex or the VS Code extension?

Use the complete updated ACO folder. On Mac, you can open `Install ACO.command`, or ask Codex:

```text
Read the ACO v0.4.3 README and run the environment doctor first.
Install the skills using the included installer.
Do not install every optional native agent profile unless it is useful; show me the proposed selection first.
Do not change my permissions, plugins, or private files.
Verify the installation and report the actual result.
```

If you want **all** optional native profiles, authorize that explicitly. The installer uses `--offices all`. If you only want selected offices, choose them, for example: `production-office publishing-office finance-office administration-office product-office`.

All 16 skills remain available through their instructions. Native Codex profiles are optional; they are not required to use the ACO methods.

**Local-script prerequisite:** Python 3.11 or newer. If it is missing, Codex should explain how to install it from an approved source. Do not disable operating-system security protections just to run ACO. If macOS blocks a downloaded script, inspect it and use the normal system approval flow rather than disabling security globally.

Restart or open a new Codex session if the new version does not appear. Use a **different working folder** for a client's website, film, software project, or publication. Do not put client work inside the ACO library repository.

**Verification:** `install-status` checks the local copied files. Asking Codex to “use ACO” also tests whether your host actually discovers the skill. A message saying “copy completed” does not by itself prove Codex loaded the integration.

## 4. Where should private memory live?

Use Google Drive or a private local folder outside Git. If you already have an ACO knowledge folder, **do not create a second one**.

```text
Use this private folder as my ACO knowledge root: [paste the link only here].
Check whether it is already initialized.
Reuse what exists and create only what is missing.
If migration is required, compare the documents and preserve the originals.
Do not share anything and do not search outside the authorized folder.
```

With authorized write capabilities, ACO can create or update the registry, folders, and records and then verify the result. With read-only access, it can work from the information but must leave updates **pending** rather than claiming they were saved.

The public ZIP does not contain your private knowledge and does not automatically configure accounts, permissions, or connectors.

## 5. Multiple companies, clients, and business activities

Speak naturally and identify the context whenever it changes:

> For Company A, publishing activity, Client X: prepare a catalogue with a print edition and EPUB edition.

> For Company B, prepare the cash-flow forecast. Do not use Company A's data.

> Back to my art practice: organize the next exhibition.

ACO should keep these contexts separate and ask if the client or organization is ambiguous. One project may involve multiple activities or deliverables without creating duplicate project records.

Sensitive HR files and restricted financial records require real access controls. Putting them in a different folder is useful organization, but a folder name alone is not a security boundary.

## 6. Email, WhatsApp, SMS, and phone calls

**“Write” or “draft” means prepare the message. “Send” requires the correct recipient, authorized content, and an actual connected sending capability.**

Examples:

> Draft a WhatsApp message for this contact. Do not send it.

> Send this approved version to the verified contact using my WhatsApp MCP, if that sending capability is actually available.

> Prepare a call to the supplier asking about availability. Do not commit me to any purchase.

If the integration is unavailable, ACO should immediately provide a copy-ready message or call script. For a phone call, it can prepare the opening, questions, decision boundaries, and voicemail version.

A tool that can read call history but cannot initiate calls **cannot place a call**. WhatsApp messaging and WhatsApp calling are different capabilities. A provider result such as **accepted** or **queued** is not proof that a message was delivered, read, or answered.

Do not paste passwords, API tokens, authentication codes, or private keys into prompts or the public repository. MCP and plugin connections must be authorized through the relevant environment or provider.

## 7. Production and publishing examples

> ACO, organize ingest, editing, conform, color, sound, and delivery for this film. Ask the essential questions first, then give me the operational plan.

> ACO, retouch these product images while preserving shape, branding, and labels. If you cannot operate the required software, write the production-ready brief for the retoucher.

> ACO, build this ComfyUI workflow against my actual version, installed nodes, and models. Do not install anything without authorization.

> ACO, take this manuscript from editing through layout, proofing, print/EPUB, metadata, rights, and distribution.

> ACO, structure a newsletter or podcast for this media company, including editorial workflow, revenue model, and source verification.

The roles are operating methods, not proof that software was executed or a human professional was hired. A colorist without footage and grading software has not graded the film. A ComfyUI specialist without a verified execution has produced a workflow or plan, not a tested render. A prepared publishing package is not the same as a published title.

## 8. Want shorter responses?

Say:

> ACTION mode. Give me only the result, essential questions, and blockers.

For explanations, ask for **EXPLAIN** mode.

ACO should still ask important questions early and must not hide errors, costs, uncertainty, or failed actions just to stay concise.

## 9. When you finish a work session

Ask:

> Record what we did, the decisions I approved, the files produced, and what remains open. Tell me whether it was actually saved to Drive or only locally.

No work continues after the chat closes unless a real authorized scheduled/automation system is configured. Writing “keep monitoring this” in a prompt does not create an always-on process by itself.

## The one rule to remember

**GitHub = public ACO instructions. Private Drive/local storage = your private knowledge. ChatGPT/Codex = the environment that performs the work.**

Publishing ACO to GitHub does not install it locally, connect private accounts, or send any message.
