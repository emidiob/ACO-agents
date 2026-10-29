# ACO Competence Library 0.3.0 in ACO 1.0.7

Twenty original, office-indexed methods with decisions, worked examples, output contracts, provenance and evaluation briefs. The canonical index is in `skills/aco-office-concierge/references/competencies/REGISTRY.json`; `registry/competences.json` is only a pointer.

The associated [professional technical skillpacks](PROFESSIONAL-SKILLS.md) append 20 `validated` entries to the original 44-entry technical skill registry, yielding 64 entries total. The original 44 retain their states. The existing role catalogue, frozen routing algorithms, safety policy and original promotion thresholds remain intact. The release builder updates ACO VERSION and current version metadata to 1.0.7 without modifying historical frozen evidence. Every professional method is `curated`; its new registered technical counterpart is `validated` only for structured procedural consistency on a frozen synthetic test set. Neither requires experimental opt-in. The 30 pre-existing experimental technical candidates remain gated. The label does **not** imply independent professional validation or certification. This is a deliberate development boundary, not a license to invent missing evidence.

```sh
python3 scripts/competence_library.py check
python3 scripts/competence_library.py list --office administration-office
python3 scripts/competence_library.py show --id administration
python3 scripts/competence_library.py audit --kind administration --input /path/to/annotated-record.json
python3 scripts/competence_library.py baseline-check --checkout /path/to/ACO-agents
```

The executable is also inside the Concierge skill, so its loader and canonical data travel together. It does not require a new top-level native skill. The integration helper adds one bounded Concierge pointer, preserving original role methods and generated catalogue semantics. The 1.0.7 release builder rebuilds manifests and runs the full ACO suite in the real checkout before publishing.

## What the tests establish

Record audits check explicit supplied annotations: time arithmetic, DAG dependencies, budgets, evidence IDs, declared states and narrow safety invariants. They do not establish that a quoted source actually supports a natural-language conclusion. The example applications are authored development cases, not independently evaluated model runs. Browser and synthetic-video evidence is documented separately in the development delivery, not silently promoted into universal competence claims.

## What is not implemented

No new model weights, automatic training, new provider access, external installation, generalized video perception, legal certification, hiring decision, publication or asynchronous process. A frozen 400-case *synthetic* procedural benchmark passed locally; there is no independent professional/model-output holdout. The registered technical skillpack promotion still requires exact-hash user approval and the complete ACO 1.0.7 CI pipeline before GitHub release.

## Permissions and rights

Methods and fixtures are original ACO additions. External material is linked and scoped, not bundled. Preserve the repository's existing LICENSE. Access to a source is not permission to redistribute it, or to send private project data to its service.
