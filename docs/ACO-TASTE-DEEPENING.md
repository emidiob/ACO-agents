# ACO Taste Deepening

ACO 1.0.9 includes four local evidence checks for visual work. They use Python's standard library and do not require a model, network connection or new database. Passing a check does not certify visual quality; inspect the rendered result with the relevant ACO specialist.

## Commands

Run these from the ACO repository root:

```sh
python3 skills/aco-taste/scripts/deepen.py variants --packet /path/to/directions.json
python3 skills/aco-taste/scripts/deepen.py feedback --project /path/to/project --query 'typography density' --scope current-project
python3 skills/aco-taste/scripts/deepen.py cycle --packet /path/to/inspection.json
python3 skills/aco-taste/scripts/deepen.py motion --packet /path/to/motion.json
```

- `variants` flags directions that differ only in palette or lack declared structural differences. It compares the supplied descriptions, not rendered pages.
- `feedback` reads reasons from the project's existing `.aco-taste/feedback.jsonl` journal within the requested scope. It is read-only and does not infer a universal preference.
- `cycle` checks before and after artifact hashes, a named correction and a recorded observation. The observation is supplied by a reviewer; the command does not view images.
- `motion` flags animation without a purpose, missing reduced-motion treatment and potentially costly UI properties. Playback and interaction still need browser review.

The input packets are JSON objects. See `tests/test_taste_deepening.py` for small examples of each contract. Run the 19 focused tests with:

```sh
python3 -m unittest discover -s tests -p 'test_taste_deepening.py' -v
```

## Local integration ZIP

The optional patch ZIP contains these commands, documentation, tests and a dry-run installer for an existing ACO 1.0.9 checkout. Extract it outside the checkout, run `python3 apply_to_aco.py /path/to/ACO-checkout` to preview, then add `--apply` to install. Rebuild the release manifest and run validation after installation. The patch is not a standalone ACO release.
