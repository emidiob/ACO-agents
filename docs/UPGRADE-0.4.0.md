> Historical/previous release material. For current storage, follow [v0.5.1 Compact Memory](COMPACT-MEMORY.md); do not initialize old event/session folder layouts.

# Upgrade to ACO 0.4.0

## From 0.3.0
Use the full release extracted outside the current checkout. Run the included migration script, not an overlay copy or a recursive deletion. The old release manifest is used to recognize managed files. Unrecognized edits/collisions stop the migration. Preserve the repository, work and private files. For v0.4.3, replace the current-release license only with the proprietary LICENSE supplied by this release; do not alter earlier Git history. The migration makes a backup branch and stages changes on a new branch; it does not push by itself.

The update adds Finance, Commercial, People, Delivery, Administration, Production and Publishing offices, extends Product with integration specialists, and applies early-question/short-action behavior to all roles. Existing six offices and all 246 old role keys remain. There are 349 roles and 16 skills.

Private registry `schema_version` remains **1**. Existing entity IDs, client/project relationships and history are not reset. New templates are optional project documents, not new entity kinds or permission grants. Do not migrate or recreate Drive as a side effect of this code update.

After a reviewed push, update local installations separately with `install` (preserves existing native selection), or deliberately choose new offices with `--offices`. Skills are all installed. ACO leaves unprefixed older third-party/unmanaged files untouched; review duplicate legacy installs separately.

## From the old plugin package
The same script recognizes included legacy baselines and removes only matched obsolete files. No plugin, app listing or marketplace is required. Do not use Git history rewriting, forced pushes or broad folder deletion.

## Checks
Run generator --check, validate and the unit suite. Inspect staged diff and confirm no client/media/personnel/financial/private Drive material is staged. Compare origin/main before pushing. If the connector is read-only, use the authorized local Codex/Git workflow; do not try alternate write APIs to circumvent a denial.

See [the repository update instructions](../README.md#updating-github-and-local-installs). [beginner step-by-step guide](../BEGINNER-GUIDE.md).
