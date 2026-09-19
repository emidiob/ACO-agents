# ACO v0.3.0 — validation record

This document records executed checks, not a guarantee that every agent behaves correctly in every AI host. Release candidate checked on 2026-09-19.

**Executed result: 86 automated tests passed** under Python 3.13.5 on Linux, plus an end-to-end disposable Git migration of the actual v0.2.1 package, installation/read-back of the native skills, an initialized private store from the installed runtime, relative documentation link checks and Bash syntax checks. The migrated repository retained its Git history and an untracked sentinel file. No remote push or Google Drive write was performed by these tests.

## What is tested locally

- All 246 canonical roles have one Markdown source and matching generated native TOML.
- All nine skills have valid entry metadata; referenced role dependencies and generated files resolve.
- Release SHA-256 fingerprints, no active old plugin machinery, basic secret/private-path scanning.
- Repeatable private local initialization, stable entity keys and parent relationships, multi-organization isolation, project/client/brand consistency, session-specific scope.
- Immutable event IDs and payloads, approval/evidence requirements, context proposal stale-write rejection, closed loops, interruption recovery.
- Safe install/update/uninstall, collisions and local edits, backups, failed-copy rollback, inventory/read-back checks.
- Git migration with known-file fingerprints, backup branches, dirty-tree rejection, untracked/private/unrelated file preservation.
- Immutable Drive event bridge using a simulated provider: retry/lost response, duplicate detection, content and parent verification, read-back receipts and pending states.

## Integration boundaries

The automated suite runs in the supplied Linux container. macOS and Python 3.11/3.13 runs are configured in CI but are not claimed as completed until GitHub actually executes them. A beginner Mac launcher is shell-syntax checked, not tested on the user's Mac.

No live Codex model session, ChatGPT Project onboarding, authenticated Google OAuth upload, real Drive mutation or automatic multi-agent quality benchmark is certified by these unit tests. A native role file being valid TOML does not guarantee that a particular installed host version exposes the subagent capability.

The Drive event bridge is **not** a full bidirectional context sync service. It transfers immutable events after explicit configuration and execution. The connected-tool procedures handle mutable Drive knowledge; they must report actual available permissions and individual write results. No daemon or scheduler is bundled.

Evidence and approval fields are checked for structure/presence. The host and user must still verify that their contents are genuine. Scoping is organizational/application logic, not OS or Google Drive access control.

The basic secrets scan is deliberately limited; it is not an exhaustive DLP/security audit of all historical Git commits or user files.

## Reproduce

From the extracted release:

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
```

Checks do not need private knowledge, cloud tokens, paid model calls or a plugin.

For host testing, run `docs/HOST-ACCEPTANCE-TESTS.md` with synthetic data before using confidential clients. Keep the real report private and never claim a test passed merely because an expected-result paragraph exists.

## Build the public ZIP

```bash
python3 scripts/build_release.py --output ../ACO-agents-v0.3.0.zip
```

This includes only files listed in the validated public manifest plus the manifest itself. Hidden files and executable permissions are preserved. The accompanying SHA-256 file detects transfer differences; it is not a cryptographic developer signature. The same release inputs produce the same archive.
