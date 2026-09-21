# Legacy event bridge — not the compact-memory path

The code in `scripts/aco/drive.py` and its tests are retained for explicit compatibility with existing schema-1 event archives. Normal compact-memory use must NOT initialize or sync this layout.

The `drive-bind` and `drive-sync` commands reject default compact mode. Only deliberate `--legacy-memory` use opts into the old per-event transport. It requires separately obtained authorized credentials, uploads separate event files, and does not update canonical context. ACO does not obtain credentials or set up accounts. Do not paste tokens into chat or source control.

For normal use, read [the compact Drive protocol](DRIVE-KNOWLEDGE.md). Updating existing canonical files needs actual host tools and revision checking. No fallback to the legacy bridge to bypass a denied or unavailable compact write. Existing legacy data is preserved pending reviewed consolidation; compatibility tests are not live Drive tests.
