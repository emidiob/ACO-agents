# Upgrade to ACO v0.7.0

0.7.0 is the Execution & Integration release. It adds no canonical roles and no mandatory external runtime.

## What changes

- formal capability states: learned skill, reference, optional tool, connected integration, local runtime, unavailable and blocked;
- a capability catalogue for common read/write/send/publish/apply/deploy/delete/purchase/sign operations;
- permission levels with exact action-packet-bound approval for consequential actions;
- host adapter contract without embedded credentials or assumed connections;
- execution receipt validation and provider-evidence claim levels;
- duplicate-action protection through unknown-outcome reconciliation;
- compact workflow-state validation without creating project/log files;
- operational execution summaries that expose observable actions/evidence, not hidden reasoning;
- deterministic execution-policy benchmark integrated into release validation.

## What does not change

- 363 canonical roles;
- 16 entry skills;
- 61 workflows;
- 97 optional resources;
- Compact Memory and Pipeline ≠ Project;
- the frozen v0.6.2 routing architecture and final routing holdout;
- no automatic third-party installation or account connection;
- no bundled credentials;
- proprietary ACO LICENSE.

## Important execution boundary

The included CLI **does not send, publish, purchase, sign, delete, deploy or connect services**. `execution-plan` resolves whether a host action is ready; the host's real authorized adapter performs it. Consequential outcomes need a receipt whose evidence supports the exact claim.

## Safe repository update

Use `docs/CODEX-MIGRATION-PROMPT.txt` from the new extracted package. Preview migration first; preserve `.git`, history, unrelated/private/untracked files and stop on unknown collisions. Never use `git clean`, `reset --hard`, blanket deletion or force push as an upgrade shortcut.

After migration run:

```bash
python3 scripts/generate.py --check
python3 scripts/aco_cli.py validate
python3 scripts/aco_cli.py route-benchmark --input config/routing-final-holdout.json
python3 scripts/aco_cli.py execution-benchmark --input config/execution-benchmark.json
python3 scripts/aco_cli.py eval-score --input release/behavioral-simulation.json
python3 -m unittest discover -s tests -v
```

Updating GitHub, updating locally installed skills and updating private knowledge remain separate operations.
