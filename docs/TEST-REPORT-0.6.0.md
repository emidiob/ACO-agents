# Test report — ACO v0.6.0

Date: 2026-09-20. Status: **local release checks passed**. This report is not a professional-quality, security, licensing or host-integration certification.

## Actual local results

| Check | Observed result |
|---|---|
| Full Python unittest suite | **448 tests passed**, 56.683 seconds in the captured source run |
| New studio-readiness/native-link tests | 80 tests included in that suite |
| Canonical and native role inventory | 363 / 363, preserved role keys from 0.5.2 |
| Entry skills / workflow recipes / optional resources | 16 / 61 / 97 |
| New task methods / roles receiving them | 19 / 114 |
| Generated catalogue, native TOMLs and installed runtime parity | Passed generator/validator checks |
| Native-profile method paths | All skill-qualified Markdown references checked against existing skill files; 363 profiles carry resolution instructions |
| Migration from supplied 0.4.3 ZIP | Passed in a temporary Git repository; history, unrelated tracked and untracked files preserved |
| Migration from supplied 0.5.2 ZIP | Passed in a temporary Git repository; history, unrelated tracked and untracked files preserved |
| Temporary full install | 363 profiles / 16 skills installed and files verified |
| New check from installed minimal runtime | `practice-check` returned ready-for-review with no execution |
| Installed resource search / capability audit | Candidate discovery and PATH-only result; no external connection or install |
| Repeated install preview | Zero changes |
| Proprietary LICENSE | Byte-identical to supplied 0.5.2 baseline |
| Known private-marker scan | No matches for checked markers; basic pattern scan only |
| Resource HTML | 97 cards; JavaScript syntax checked with Node; no external auto-loads in markup |

## Coverage highlights

The suite covers compact-memory promotion boundaries, retained pipeline items, scoped organizations/clients/projects, safe file operations and conflicts, simulated canonical synchronization, installer recovery, release migration, workflow/role validation, resource gates and the existing specialist checks.

The added cases exercise oversubscribed artistic plans, protected making time, unknown/failed eligibility, stale/future call evidence, explicit deadline timezone, assumption/approval/validation separation, lack of trademark-clearance evidence, publishing packet hashes, account/scope/platform mismatch, expired approval, stale capability snapshots, uncertain or accepted prior outcomes, media rights/hash binding and the distinction between an offline report and authorization. Malformed numbers and enum objects are rejected/flagged rather than silently accepted.

Synthetic fixtures use fictional evidence references deliberately. Their passage means input consistency was checked, not that those references authenticate an action or substantiate a fact.

## Reproduction

Run from the complete extracted release:

```bash
python3 scripts/aco_cli.py validate
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -v
python3 scripts/aco_cli.py practice-check --input examples/studio/practice.json
python3 scripts/aco_cli.py social-check --input examples/studio/social-draft.json
```

The package manifest fingerprints distributed files. The ZIP checksum is supplied alongside the archive rather than embedded circularly inside it. A later ZIP extraction/integrity result can be checked against that checksum; this source-run report does not claim an unrun browser or provider test.

## Not run / not established

- No authenticated GitHub push or live Drive/CRM/social/email/WhatsApp/phone writes.
- No real scheduler, private account connection or third-party deployment.
- No GPU ComfyUI render, paid generation, desktop-DCC operation or production FFmpeg/OTIO/OIIO processing.
- No human before/after benchmark demonstrating improved artworks, curatorial judgements, design, copy or business outcomes.
- No browser-rendered acceptance test of the catalogue or a user's website. HTML/JS checks were static.
- No real-run Gitleaks, Semgrep, Promptfoo, axe-core or Lighthouse result is claimed by the code tests or PATH audit.
- No exhaustive source-code/security/licence review of the external resource catalogue. Sources were selected by documented scope; inherited entries retain their provenance.
- No claim that a specific host loaded native subagents or that reading a role produces a separate agent process.

Use [human acceptance cards](EVALUATION-CARDS.md) and [host checks](HOST-ACCEPTANCE-TESTS.md) in the actual authorized environment. Failures or unavailable tools remain explicit, not converted into successes.
