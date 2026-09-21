# Specialist tools — actual checks and limits

All commands below run from the extracted ACO root using Python 3.11+. The four core helpers use the standard library, do not connect accounts and never render, submit, publish or spend. Results distinguish missing input, structural issues, draft metadata and integrity evidence.

## 1. Website contract

```bash
python3 scripts/aco_cli.py web-contract-check --input examples/specialist-upgrade/web-contract.example.json
```

Checks brief fields, route/state/acceptance IDs, viewports and optionally opaque sRGB contrast arithmetic. The example font declaration is fixture metadata, not a font licence audit. It is not a browser, design, WCAG or legal certification. `normal_text` uses 4.5:1; `large_text`/`non_text` use 3:1. Choose the category correctly and check actual compositing/context.

## 2. Frame timeline and continuity

```bash
python3 scripts/aco_cli.py shot-plan-check --input examples/specialist-upgrade/shot-plan.example.json
```

Validates stable shot/reference IDs, required shot purpose/action/camera, flat continuity states and reasoned exceptions. The 12-second example uses 24 FPS and counts a 24-frame dissolve only once. This helper deliberately supports integer FPS only; fractional broadcast rates need a different explicit timebase, not silent rounding. It cannot inspect visual identity or the correctness of a camera instruction.

## 3. Model-aware draft

```bash
python3 scripts/aco_cli.py video-prompt-draft --input examples/specialist-upgrade/shot-plan.example.json --capability examples/specialist-upgrade/capability.example.json --as-of 2026-09-20
```

This demonstrates a **fictional offline provider**. It is not a live Runway/Veo/Kling/Seedance request. For real work, copy `capability.TEMPLATE.json` into the private project and fill it only from the exact current provider/model/UI-or-API documentation or available tool schema. Do not publish client reference files or credentials.

The helper checks duration/aspect/mode, image reference, explicit audio/negative/seed support, character limits and a 30-day snapshot freshness policy. It composes normalized draft text/metadata, not an executable API payload. Generation duration must cover the usable edit segment. It never truncates a long prompt or silently inserts unsupported fields. Refresh stale snapshots; do not falsify their date.

## 4. Evidence integrity

```bash
python3 scripts/aco_cli.py evidence-check --input /absolute/private/project/evidence.json --evidence-root /absolute/private/project/evidence
```

Start from `evidence.TEMPLATE.json`; its entries are intentionally `not_run`. For a reported passed check, supply matching revision, relative file path and SHA-256. The checker rejects missing coverage, paths outside the root, symlinks, empty files, changed hashes and wrong revisions. PNG support checks only header/dimensions, not decoding, authenticity or visual quality. It cannot prove that an attached report is truthful.

## 5. Optional actual browser capture

```bash
python3 scripts/capture_web_evidence.py --url http://127.0.0.1:3000/ --out /absolute/private/project/evidence/run-001 --revision ACTUAL_BUILD_ID --widths 360 1440
```

Requires separately installed Playwright and Chromium. Supply an existing approved browser with `--executable /absolute/path/to/chromium` when needed. The script does not install either. Use a trusted authorized development server; it only supports the supplied loopback origin and blocks other HTTP(S) origins and non-GET/HEAD requests. This request guard is not a sandbox for hostile JavaScript. No login state, form submissions or client account credentials are injected.

It captures viewport PNGs, basic DOM overflow observations and a three-Tab focus probe into a **new** directory outside the ACO source library. Some blocked resources can affect fidelity. Perform complete functional, visual and accessibility acceptance separately. A policy block or missing dependency is a failed/not-run check, not permission to disable controls.

A synthetic page is included as `examples/specialist-upgrade/browser-fixture.html`; `?broken=1` introduces intentional overflow. The local browser attempt in the build environment was policy-blocked. The helper's guards have unit coverage; no successful capture smoke is claimed here.

## Reference and research
[Playwright screenshots](https://playwright.dev/python/docs/screenshots) · [Playwright network routing](https://playwright.dev/python/docs/network) · [WCAG contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Scripts are ACO-authored; references are not bundled vendor code.
