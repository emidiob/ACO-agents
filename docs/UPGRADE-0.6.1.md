# Upgrade to ACO v0.6.1

v0.6.1 is an architectural refinement of v0.6.0. It preserves the same 363 roles, 16 skills, 61 workflows, 97 optional resources, Compact Memory model and proprietary license.

## What changes

- Replaces the long duplicated role-wide operating/action contracts with a compact self-contained role bootstrap plus shared on-demand protocols.
- Adds progressive context retrieval, verification/evidence, planning/approval, scoped learning and role-maintenance protocols.
- Adds read-only `context-budget` and `role-stocktake` maintenance commands.
- Adds `eval-lint`, `eval-show` and 10 behavioral regression cases.
- Preserves all artist-development, curatorial, brand, web, social, production, publishing and office task methods from v0.6.0.
- Does not add a second memory store, background learning daemon, automatic hooks, ECC runtime, external software installation or new Drive scaffolding.

## Why

The canonical role Markdown in v0.6.0 contained about 3.10M characters, with the two shared operating/action contracts repeated in every role. v0.6.1 moves those details into shared protocols while retaining a short essential bootstrap in each role. Canonical role Markdown is about 1.66M characters after the refactor (~46% reduction).

This is a source/package duplication metric. ACO still expects hosts to load only selected roles and methods.

## Safe repository upgrade

Extract the new ZIP outside the existing checkout and follow the README’s “Updating GitHub and local installs” instructions from the new package. Preview first. Preserve `.git`, history, private/untracked/unrelated files and the supplied `LICENSE`. Do not use force push, `git clean`, hard reset or blanket deletion.

After repository validation, update a local ACO installation separately if desired. A GitHub push does not reload existing ChatGPT/Codex sessions or clean Drive.

## Private knowledge

No private-memory migration is needed. Compact schema 2 is unchanged. Existing pipeline rows, canonical document IDs and lazy folder rules remain valid.
