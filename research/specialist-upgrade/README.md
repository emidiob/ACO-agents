# Research inventory, not an upstream bundle

`sources.json` documents 15 inspected source catalogues, selected observations, snapshot limitations and licence cautions. `baseline-roles.json` preserves metadata/hashes for the 349 original ACO roles. `decisions.json` records targeted changes separately from automatic lexical matches. `comparison.json` contains every role/repository pair; `comparison.html` is a searchable local view.

Run `python3 scripts/compare_specialists.py` from the release root to reproduce the comparison. Source labels were extracted from the inspected catalogues and normalized; this is not an exhaustive ingestion of all external prompt bodies. No raw third-party prompt files, code, datasets, fonts or weights are bundled.

ACO's licence governs ACO material, not the external repositories linked here. Their original rights and notices remain their own. Credit to Serge Shima / smixs for visual-skills as a comparison source, alongside all other named maintainers. No endorsement is implied. A future adaptation of protected content requires its own licence/notice review; rewriting a file superficially does not erase those obligations.
