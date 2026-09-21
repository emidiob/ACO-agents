> Current release is v0.5.1. Follow the new package migration prompt; Compact Memory affects future storage, not automatic deletion of existing private data.

# Repository migration is not knowledge migration

Keep .git, commit history and the remote. Apply the LICENSE supplied by the target release; never alter licensing silently or outside an explicit versioned release. Preserve all untracked private data and unrelated tracked files. No rm -rf, git clean, reset --hard or force push.

Use the supplied migration script from the newly extracted release OUTSIDE the existing repository. It checks a clean tracked worktree, verifies the release manifest, compares old files to known hashes, and lists additions/replacements/removals. --apply creates a backup branch and a work branch, changes only recognized ACO-owned paths, and stages an exact path list. Unknown or locally edited files block the operation; reconcile them before proceeding.

After applying, run validate and the full tests in the target repository. Review git diff --cached, privacy scan and deleted paths. Only then commit, fast-forward/merge the reviewed branch into main, and push without force under user authorization. A failed push is not a successful publication.

Drive data is not touched by this script. Private context migration is separately journaled through BOOTSTRAP.md. A source-code release and an installed copy are different: update the local managed install explicitly after pulling an approved version.
