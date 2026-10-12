# ACO Agents v1.0.3 — Fix and documentation consolidation

## Scope

Consolidate the merged macOS system-alias and Git-relative-path fixes from 1.0.2 development, align release metadata and generated runtime/profiles, and refresh README, beginner setup, CLI, upgrade and validation guides. Historical upgrade notes and test reports retain their original evidence.

Preserve 363 roles, 16 entry skills, 61 workflows and 99 optional resources. The technical registry remains 43 entries: 14 active and 29 candidates. No change to the integration resolver, approval policies, proprietary license or candidate activation status.

## Verification

Checked on 2026-10-12 with Python 3.13.5 on macOS.

- `python3 scripts/generate.py --check`: 569 derived files verified.
- `python3 scripts/aco_cli.py validate`: validated as 1.0.3; 363 canonical/native roles, 16 entry skills, 61 workflows and 99 optional resources; 4,863 relative documentation links checked; zero privacy findings.
- `python3 -m unittest discover -s tests -v`: **622/622 passed**, 37.253 seconds.
- `bootstrap-resolve --root .`: resolved 1.0.3; the documented `skill-search --query frontend --root .` and `doctor` commands also completed.
- Installation preview exercised with an isolated temporary home; no host installation was applied. Installer/runtime behavior is additionally covered by the full suite.
- macOS fixture checks all three standard aliases and performs write/read plus nested malicious-link rejection under `/tmp`, avoiding a write requirement for `/var/tmp` in restricted hosts. The first sandboxed run failed only on that temporary-directory permission; the final complete run passed after the fixture was adjusted.

The existing GitHub workflow is configured for macOS/Ubuntu and Python 3.11/3.13. The results above are local release results; CI run status is separate.

## Limits

Local package tests do not establish live image/video quality, professional outcomes, host skill discovery or authenticated external-service access. Filesystem compatibility does not grant GitHub/app permissions. Private knowledge and installed skills are updated separately from the repository.
