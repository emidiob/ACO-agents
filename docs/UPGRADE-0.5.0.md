> Historical/previous release material. For current storage, follow [v0.5.1 Compact Memory](COMPACT-MEMORY.md); do not initialize old event/session folder layouts.

# Upgrade to ACO v0.5.0

## What changes
363 roles (349 preserved + 14 distinct additions), 16 entry skills, 32 workflows, 12 specialist playbooks, offline design/video/evidence checks and optional passive browser capture. Existing private knowledge schema, licence and account boundaries are unchanged.

Read [the comparison](SPECIALIST-GAP-ANALYSIS.md) for all 15 source repositories and explicit research limits. The package is English-only, remains a skill library, and contains no private company/client data or third-party runtimes.

## Safe update
1. Extract the new ZIP outside your existing ACO checkout.
2. Ask Codex to follow [the migration prompt](CODEX-MIGRATION-PROMPT.txt) from the new release.
3. Review the plan; it must preserve .git, history, private/untracked/unrelated files and remote changes. No force push or broad deletion.
4. Rerun generation checks, validation and unit tests in the target.
5. Commit and push only the reviewed change under your authorization.
6. Update local installations separately with the existing installer and chosen offices. Start a new Codex session to load changed profiles.

No Drive migration is required for this upgrade. Never copy private context into the source repository. If an existing tracked ACO file differs from its known version, compare it rather than discarding it.

The optional browser and external-provider tests remain separate from a source migration. Do not install third-party dependencies, spend credits, connect accounts or bypass a policy block just to complete the update.
