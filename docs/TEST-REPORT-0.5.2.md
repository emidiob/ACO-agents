# ACO v0.5.2 — Test report

Date: 20 September 2026.

## Release shape
- Version: 0.5.2
- Canonical roles: 363
- Native Codex profiles: 363
- Entry-point skills: 16
- Workflows: 47
- Optional resource entries: 62
- Memory default: Compact Memory

## Executed local checks
- `python3 scripts/generate.py --check`: generated parity verified.
- `python3 scripts/aco_cli.py validate`: release structure, TOML, role dependencies, no plugin artifacts, basic secret/private-path scan, release hashes, relative links and resource role/method mappings validated.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: **368 tests passed**.
- v0.5.2-specific tests confirm all 22 newly supplied resources are present, learned skill concepts route to original ACO playbooks, and external software is not bundled/installed.
- Compact Memory and reviewed cleanup tests remain in the suite, including no automatic entity/file creation for ordinary pipeline items and reversible cleanup behavior.

## What was not tested
No third-party resource in the optional registry was installed or executed as part of this release test. No authenticated Google Drive cleanup, browser automation, scraping/crawling, monitoring deployment, media downloading, secret migration, external software-agent run, paid API call or GPU render was performed.

Repository/README review is not a complete security audit, legal clearance or perpetual license guarantee. Exact versions, deployment topology, data routes and current upstream terms must be checked at execution time.
