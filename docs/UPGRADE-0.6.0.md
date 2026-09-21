# Upgrade to ACO v0.6.0

This complete release consolidates the supplied 0.5.2 package. It does not require installing intervening ZIPs. The remote repository version checked during preparation was 0.4.3; it was not updated by this packaging operation.

## Decisions

- Preserve all 363 roles and 16 skills. No new persona count race.
- Give 114 roles targeted references to 19 new original methods, not all methods in every startup prompt.
- Add 14 workflow recipes, taking the total from 47 to 61.
- Preserve the earlier 62 resources and add 35 curated entries, taking the total to 97. Existing review provenance is retained; no full re-audit of every inherited entry is claimed.
- Add side-effect-free practice, opportunity, brand and social-packet checks plus PATH capability discovery.
- Preserve compact schema 2 and the proprietary LICENSE byte-for-byte. No automatic private knowledge migration is required.
- Fix generated native-profile reference resolution: canonical relative links are rewritten under a selected skills root instead of being incorrectly relative to the TOML directory.
- Fix the macOS installer’s stale native-profile count and explicit Python-version check.

## Safe upgrade

Extract the new package separately. Follow [the repository update instructions](../README.md#updating-github-and-local-installs). The migration tool must preview changes, preserve .git/history and unrelated/private/untracked files, and stop on unknown edits. Do not erase the old checkout blindly. The release includes baseline hashes from 0.5.2 and earlier supported releases.

After the Git update, update local skills from the new source only when authorized. Reinstall the same optional offices you actually use. Start a new host session or reload the versioned instructions. Pushing GitHub is not local installation.

## Private knowledge

No additional Drive folders or structured event files are needed. The new Artist Development and Brand/Social content belongs in existing scoped ACO.md sections. Do not instantiate all fields from an example; ask only what matters for the current work. Cleanup remains separate and reviewed.

## What to review

Read [product decisions](PRODUCT-DECISIONS.md), [method map](METHODS.md), [source review](SOURCE-REVIEW.md), [local check contracts](STUDIO-CHECKS.md) and [test evidence](TEST-REPORT-0.6.0.md).
