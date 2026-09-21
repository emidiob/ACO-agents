# From identity to a real, reviewed website

Original ACO operational method · v0.6.0. Select for the relevant task; do not load every playbook.

## Define the actual site
Confirm purpose, audience, representative content, required interactions, stack/hosting constraints and what is already approved. Distinguish a portfolio, publication, service site, commerce site and software product. Do not default to a conversion landing page for an artwork or cultural archive.

## Visual contract
Extract current design rules only from authorized assets/site evidence and label them observed until approved. Capture hierarchy, type, spacing, grid, color roles, imagery, motion, content types and exceptions. Identify real assets vs placeholders. One concise contract in the existing project is enough. Do not invent a new visual system on every session or clone a reference site's proprietary expression.

## Build a representative slice
Implement one meaningful page and responsive state before reproducing all pages. Use real-length copy and representative media. Components should follow the approved identity. Radix or shadcn are optional foundations, not a required visual style. Use Storybook when component complexity justifies it; a tiny one-page site may not need another toolchain. Avoid installing a CMS until publishing roles, content model and maintenance requirements are clear.

## Review rendered evidence
Test the site in a real available browser: narrow/wide layout, keyboard flow, focus, navigation, long text, missing assets, loading/error states and reduced motion. Inspect imagery and typographic rhythm visually; DOM assertions do not prove good art direction. Screenshots do not prove interaction works. State the exact routes, viewport(s), browser and build when reporting results.

Use axe/Lighthouse as supporting checks, not an accessibility certificate or a universal aesthetic score. Verify production loading and performance against an agreed budget. Third-party animation libraries need cleanup/lifecycle handling, reduced-motion behavior and a demonstrable benefit. Website captures and analytics involving private accounts need authorization.

## Delivery
Give actual changed files, previews and checks, plus unresolved production items. Brand owner approves identity; product lead approves function; technical lead owns deployment readiness. Do not deploy to a public domain or spend on hosting without authorization. Retain a short handoff with references, not a screenshot report per tiny CSS change.

## References and use boundary
The linked sources inform scope and factual tool selection. Their courses, software, skill bundles and protected text are not included or relicensed by ACO. Recheck current terms before external reuse.

- [Radix primitives](https://github.com/radix-ui/primitives)
- [Storybook](https://github.com/storybookjs/storybook)
- [Lighthouse](https://github.com/GoogleChrome/lighthouse)
- [axe-core](https://github.com/dequelabs/axe-core)
- [W3C accessibility quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
