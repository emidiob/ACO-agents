# ACO v0.4.3 — validation record

Checked 2026-09-19 with Python 3.13.5 on Linux.

**166 automated tests passed.** This is local implementation evidence, not certification of agent expertise or live application integrations.

## Executed checks

- 349 distinct canonical Markdown role definitions and 349 generated Codex TOMLs; original 246 role keys retained.
- 16 skill entry points and 24 workflow recipes; role paths, leads and dependency references resolve.
- Short-action/early-question contract present in every canonical and native role.
- Existing local memory, entity isolation, event, approval-reference, installer rollback and simulated Drive bridge tests retained.
- Early intake questions do not repeat supplied facts; no-work output is explicit.
- Action-planning tests distinguish missing/read-only/denied tools, exact sending account/target/action/payload approval, drafts, phone-vs-message capabilities and reconciliation of uncertain outcomes. The helper does not send, call or grant permissions.
- Budget checks use Decimal arithmetic, distinguish margin and markup, reject duplicate cost lines/mixed currency and do not invent tax rates.
- ComfyUI preflight tests inspect a synthetic API graph against a synthetic node-schema snapshot, including missing nodes/inputs, link bounds/types, cycles and literal validation. No real ComfyUI graph was executed.
- Generated parity, release hashes, relative documentation links and limited private-path/secret scans pass.

## Upgrade integration actually exercised

An extracted copy of the supplied v0.3.0 archive was initialized as a disposable Git repository. Its original 246 native agents were installed in a temporary home. The new migration ran in preview and apply modes, created a backup/work branch, preserved the Git commit and an untracked sentinel file, and left the separate private knowledge registry unchanged.

Updating the managed installation produced **349 native ACO profiles and 16 skills**, preserved an unrelated native profile, and retained the original private registry data/IDs. Intake, action-plan, budget-check and static ComfyUI preflight ran successfully from the **installed minimal runtime**, not just the source folder.

No remote push, email, WhatsApp, voice call, bank action, real rendering, publishing or Drive write was performed by this integration test.

## Not tested / important boundaries

No live Codex model session, ChatGPT project onboarding, macOS host run, authenticated messaging/calling integration, real Photoshop/Resolve/ComfyUI/EPUB production workflow or full professional-output quality benchmark is claimed. CI is configured for Linux/macOS and Python 3.11/3.13; those remote jobs are not passed until GitHub actually runs them.

Host capabilities and user/provider permission remain authoritative. Self-reported action-plan authorization/capability fields are checked for structure and binding only, not cryptographically authenticated. Native scope and folder names are not a security boundary for HR/client/financial data.

The optional Drive event bridge remains an immutable-event transport with simulated-provider tests; it is not a general synchronized filesystem or an always-on daemon. The connectors used by a real session must verify writes and receipts separately.

The basic secrets scan is not an exhaustive DLP audit of all user files, Git history, forks or remote releases.

## Reproduce

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

For live acceptance tests use [HOST-ACCEPTANCE-TESTS.md](HOST-ACCEPTANCE-TESTS.md) with synthetic data and explicit scoped authorization.

## Package

```bash
python3 scripts/build_release.py --output ../ACO-agents-v0.4.3-complete.zip
```

The release includes only fingerprinted public files, with hidden files and executable modes. SHA-256 detects transfer differences; it is not a developer digital signature.
