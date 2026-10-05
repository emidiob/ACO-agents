# Upgrading ACO safely

This is the evergreen repository-upgrade procedure. Release-specific copy/paste prompts belong next to a distributed ZIP, not inside `ACO-agents`.

1. Extract the new complete ACO release **outside** the existing Git checkout.
2. In the existing checkout inspect `git status`, current branch, origin and recent history. Resolve/preserve tracked edits before migration.
3. From the **new** source run a dry-run migration:
   ```bash
   python3 scripts/aco_cli.py migrate --target /ABSOLUTE/PATH/TO/EXISTING/ACO-agents
   ```
4. Review added/replaced/removed files, collisions and preserved unmanaged files. Never use `git clean`, `reset --hard`, blanket deletion or force push as an upgrade shortcut.
5. If the preview is safe, apply:
   ```bash
   python3 scripts/aco_cli.py migrate --target /ABSOLUTE/PATH/TO/EXISTING/ACO-agents --apply
   ```
   The migration creates backup/work branches and stages only recognized managed ACO files.
6. In the migrated target run the validation commands documented by the **new** release. At minimum:
   ```bash
   python3 scripts/generate.py --check
   python3 scripts/aco_cli.py validate
   python3 -m unittest discover -s tests -v
   ```
7. Inspect `git diff --cached`, the privacy/secret scan and the supplied `LICENSE`. Commit only after all gates pass.
8. `git fetch origin`, compare histories, and push normally only when a reviewed fast-forward/merge is safe. Never force-push over remote work.

Updating GitHub, updating locally installed ACO skills, and updating private knowledge are separate operations. A repository upgrade must not modify Drive/private context, connect accounts, install optional third-party tools, send messages, publish, purchase, sign or create schedules.
