# ACO v0.5.0 — Verification report

Verification date: 2026-09-20.

## Scope

This report distinguishes executable local checks from creative or professional output evaluation. Passing a syntax, schema, fixture or integrity test does not certify the quality of 363 specialists, the legality of an output, an accessible website, a rendered film, or a working remote integration.

## Actual local results

| Check | Result | Scope and limit |
|---|---|---|
| Unmodified v0.4.3 baseline suite | 166 tests passed | Baseline run before editing |
| v0.5.0 full unit/regression suite | 243 tests passed | Includes the baseline, 68 specialist-check tests, 8 passive-capture guard tests and 1 executable-mode migration regression |
| Static release validation | Passed | 363 canonical roles, 363 generated native TOMLs, 16 skill entry points, 32 workflows, references, parity and release hashes |
| Catalogue comparison | Reproduced locally | 349 baseline roles × 15 curated repository inventories = 5,235 pairs; 313 observed catalogue labels/topics. Lexical matching is triage, not a model-output score |
| v0.4.3 → v0.5.0 migration smoke | Passed in a temporary Git repository | Preserved previous HEAD via a backup branch, unrelated tracked file, private untracked marker and executable launcher permissions; no remote push |
| Validation and tests after migration | Passed | Run inside the migrated temporary checkout |
| Isolated full local install | Passed | Installed 363 native profiles and 16 skills into a temporary home, not the user's computer |
| Installed-runtime specialist command | Passed | The installed CLI checked the example shot plan, including its dissolve, at 288 frames / 24 fps |
| Repeat installation | Passed | No changes required on a second identical installation |
| Proprietary license file | Preserved | Byte-for-byte unchanged from the supplied v0.4.3 LICENSE. External reference projects retain their own terms |

All figures above are local measured counts, not claims that external services or paid models ran. Generated artefacts and templates are included in the release integrity manifest.

## Important blocked or unperformed checks

- **Browser capture was attempted but blocked.** Chromium navigation to the synthetic loopback fixture returned `ERR_BLOCKED_BY_ADMINISTRATOR`. No alternative route was attempted to evade that policy. There is no successful browser screenshot, visual comparison or runtime accessibility result from this session. The optional Playwright runner is supplied for later authorized testing; its eight guard tests are not an end-to-end browser test.
- No actual Figma-to-browser fidelity test was run.
- No Runway, Veo, Kling, Seedance or other paid video generation was submitted. No GPU/ComfyUI render was run. Capability examples are explicitly fictional, and creative prompt examples are untested drafts.
- No Remotion engine install/render was performed. The engine's installation and license conditions are separate from these ACO methods.
- No paired before/after model-output benchmark was performed. The evaluation protocol in `SPECIALIST-EVALUATION.md` is a plan for that work, not a result.
- No user Mac, real Codex host loading, remote GitHub push, authenticated Drive write, email, WhatsApp, phone or other consequential external action was tested or performed.
- Public-source review covers the recorded catalogue pages/README sections and selected methods, not all upstream implementation files or every role in each repository. The source inventory deliberately does not present stale or unverified star counts as current.

## Helper-specific boundaries

`web-contract-check` checks structured requirements and limited opaque sRGB hex contrast calculations; it does not render a page or certify WCAG conformance. `shot-plan-check` checks timing and declared continuity, not the visual truth of clips. `video-prompt-draft` uses a supplied capability snapshot and does not contact or emulate a provider SDK. `evidence-check` checks required records, bounded file paths, hashes and limited PNG metadata; it cannot prove that the recorded test actually ran or that an image is authentic.

The passive browser helper requires a separately available Playwright installation and browser. Its origin/method restrictions reduce accidental scope expansion but are not a security sandbox for hostile JavaScript. Run only against trusted, authorized development content.

## Reproduce locally

From the extracted ACO source folder, using Python 3.11 or newer:

```bash
python3 scripts/compare_specialists.py
python3 scripts/generate.py
python3 scripts/build_manifest.py
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests
```

Keep this source folder separate from client work. Do not run unknown upstream installers or hooks merely to perform the comparison. See `SPECIALIST-TOOLS.md` for concrete sample commands and `CODEX-MIGRATION-PROMPT.txt` for the safe repository update process.
