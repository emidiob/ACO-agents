# ACO 1.1.0 — Deep Design Production (original integration)

This is an additive, standard-library-first extension to the existing ACO Open Design/Taste system. It does **not** install or bundle any code, styles, fonts, gallery content, licensed assets, images or models from the upstream references. ACO's own [LICENSE](../LICENSE) still applies.

## End-to-end flow

1. **Interpret** a concrete brief with approved text/claims, audience, project-specific factual anchor and optional observed reference treatments. Never invent visual observations from URL metadata.
2. **Explore** three structural strategies (`index-led`, `field-led`, `type-led`) under a shared token system rather than changing color palettes three times. These are real different HTML compositions, not three fully independent generative-design models.
3. **Adapt** observations using an original eight-lens checklist: hierarchy, whitespace, alignment, proximity, contrast, balance, repetition, unity. Safe bounded controls (`hero_scale`, `density`, `alignment`) can modify rendered output. Conflicting reference controls are held for human resolution, not silently averaged. Negative references constrain; they are not copied.
4. **Produce** a bounded matrix of locales (provided translations only) and media targets (landing, dashboard, deck, square/portrait/landscape social HTML). Preserve literal approved content; no invented metrics or slogans.
5. **QA** source escaping, file integrity, language, contrast ratios, anchors, responsive/reduced-motion/print CSS. Optionally run real Chromium screenshots and overflow/clipping smoke checks. Static and browser checks do not establish visual taste, user approval or WCAG certification.
6. **Review** screenshot evidence with the existing ACO Taste seven gates, prior Taste Deepening `cycle`, and actual humans when consequential. Make corrections in project-specific source, then regenerate and rerun. Local project feedback remains scoped and is explicitly consulted using the existing `deepen.py feedback` command.

## Commands

```bash
# From ACO source root
python3 scripts/aco_open_design.py deep-plan --packet examples/deep-design-campaign.json
python3 scripts/aco_open_design.py deep-study --packet examples/deep-design-campaign.json
python3 scripts/aco_open_design.py campaign --packet examples/deep-design-campaign.json --output /tmp/aco-deep-campaign
# Equivalent separate entry point, useful when using this patch in isolation:
python3 scripts/aco_open_design_deep.py build --packet examples/deep-design-campaign.json --output /tmp/aco-deep-campaign

# Optional; Playwright and Chromium must already be installed and authorized:
python3 scripts/aco_open_design_deep.py browser-check --bundle /tmp/aco-deep-campaign --output /tmp/aco-deep-qa --browser /path/to/chromium

# The existing project-local taste mechanism, if needed:
python3 skills/aco-taste/scripts/deepen.py feedback --project /path/to/project --query 'editorial type'
python3 skills/aco-taste/scripts/deepen.py cycle --packet /path/to/review-cycle.json
```

Never overwrite an existing campaign or browser QA directory; use a new path after revision. Local generated materials and taste memory stay OUTSIDE the public ACO library.

## Input schema

`examples/deep-design-campaign.json` is fictional and entirely user-approved only when used for a test. Real projects require their own approved content. At least one translated content block and one channel are required. Each referenced locale must exist in `content`; translations are never performed by the tool. `locked_identity=true` requires explicit approved color and font tokens.

Reference observations are **author-supplied evidence descriptions**, each with `lens`, `observation`, `effect`, and `adaptation`. Optional bounded `controls` can be `hero_scale: default|large`, `density: default|airy|compact`, `alignment: default|left|center`. An observation is not permission to copy an upstream layout or asset.

The emitted `manifest.json` includes direction rationale, the applied safe controls and conflicts, local file SHA-256 receipts, static checks and known limitations. The optional `browser-check` produces an independent screenshot folder and `report.json`, recording exact viewport and clipping/overflow results.

## Source and rights boundary

This original module adopts general design, accessibility and review techniques. It
bundles **no third-party source code, images, layouts, fonts, branding or templates**.
Use existing ACO source-provenance records and check the license of each future
external asset before adopting it. Reference URLs and reviewer-supplied observations
are not evidence that ACO retrieved or inspected their contents.

## Verification before release

Follow the repository's `AGENTS.md`. Generate, rebuild
the integrity manifest, validate, run publication checks, run the Python and
JavaScript suites, and inspect actual rendered output. Passing the static and
browser checks does not certify artistic quality, user acceptance or WCAG
conformance. The optional browser check runs only when authorized Playwright
and Chromium are already installed; it does not install dependencies.

## Explicitly not implemented

- LLM synthesis of unseen reference images, autonomous third-party design research, real image generation, video rendering or motion playback.
- Professional translations, live data, external assets, platform-specific native posts, true Figma editable-layer transfer or provider uploads.
- Global taste memory, silent machine learning, background monitoring, full accessibility compliance or production-quality signoff.
