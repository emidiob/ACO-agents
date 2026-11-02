# ACO 1.1.0 — Deep Design Production

**Canonical target:** `emidiob/ACO-agents`, branch `main`, runtime `aco://current`.

## Delivered native capability

- Three distinct structural HTML composition families (`index-led`, `field-led`, `type-led`) with a factual brief anchor and scoped art-direction rationale. This is **not** generative aesthetic intelligence or automatic design ranking.
- A bounded eight-lens observation checklist (hierarchy, whitespace, alignment, proximity, contrast, balance, repetition, unity) that can adapt rendering through explicit `hero_scale`, `density`, and `alignment` controls while surfacing conflicts.
- Multiple production targets: landing, dashboard, deck, and social square/portrait/landscape, with supplied language-specific copy, HTML and local SHA-256 receipts.
- Reuse of the existing ACO Taste Deepening methods for project-scoped feedback and before/after QA. User preferences are never generalized across projects automatically.
- Native Open Design routing: `deep-plan`, `deep-study`, `campaign`, and an independent CLI browser smoke check when Chromium/Playwright is already available.
- Portable Concierge runtime receives the new helper and example through `scripts/generate.py`; release manifests are rebuilt after all source changes.

## Verification boundary

Review the actual content, screenshots and functionality. HTML/code checks do not certify artistic merit, accessibility compliance, legal rights or human preference. No external kit code, assets, fonts, brand examples or designs are bundled. No third-party providers, browsers, model downloads, accounts, private data or background agents are installed. Existing experimental technical candidates remain experimental. Current native entry skill count remains unchanged.

## Release gates

On the **actual existing 1.0.9 main working copy**, with a clean tree and verified upstream state:

```bash
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 scripts/build_manifest.py
python3 scripts/publication_check.py
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -v
node --test tests/test_framework_live.mjs
```

Review `git diff --check`, `git diff --stat`, `git diff`, and run `python3 scripts/aco_cli.py install` in preview mode only if the installed skills need updating. A clean build and passing test suite are prerequisites for the first 1.1.0 main commit. The release kit never performs `git push --force` or silently modifies remote accounts.
