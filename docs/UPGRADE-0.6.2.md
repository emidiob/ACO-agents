# Upgrade to ACO v0.6.2

0.6.2 is a Quality & Routing release. It adds no new canonical roles.

## What changes

- generated structured contracts for all 363 roles;
- advisory two-stage office/role routing with compact example evidence;
- a frozen 28-case final routing holdout excluded from the development examples;
- compact handoff validation and capability-state resolution;
- advisory role-overlap inspection;
- a scored 24-case behavioral simulation with explicit same-model limitations;
- release validation/tests for the new quality gates.

## What does not change

- 363 roles, 16 skills, 61 workflows and 97 optional resources;
- Compact Memory and Pipeline ≠ Project;
- no external software auto-install;
- no automatic Drive mutation;
- no plugin architecture;
- proprietary ACO LICENSE.

## Safe repository update

Use `docs/CODEX-MIGRATION-PROMPT.txt` from the **new extracted package**. Preview migration first, preserve `.git`, private/untracked/unrelated files, and never use `git clean`, `reset --hard`, blanket deletion or force push as a shortcut.

After migration run:

```bash
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
python3 scripts/generate.py --check
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
```

A GitHub update does not update an installed local ACO copy or private knowledge. Those are separate operations.
