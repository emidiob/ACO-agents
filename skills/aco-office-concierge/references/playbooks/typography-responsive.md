# Typography, tokens and responsive text

## Inputs
Approved brand rules, actual font sources and licences, languages, content samples, page hierarchy and target devices. Ask about missing fonts or intended text hierarchy before substituting a visual identity.

## Method
1. Inventory font families, weights actually available, variable axes, fallbacks and loading. Test fallback metrics and layout shifts; do not request a weight whose file does not exist.
2. Define semantic roles (display, title, body, caption, label) and tokens for size, weight, line-height, tracking and maximum measure. Use optical judgement; a mathematical scale is a proposal, not proof of legibility.
3. Establish a spacing/grid system appropriate to content density. Make page margins, gutters, nested indentation and repeated alignment explicit. Avoid pixel-only fixes that collapse at nearby widths.
4. Test long names, dates, translated labels, URLs, prices, unbroken identifiers and empty content. Essential text must not depend on hover to reveal clipping. Truncation requires a meaningful accessible alternative.
5. Review 320/360-class narrow layouts when in scope, representative intermediate widths and desktop. Check 200% zoom and enlarged text separately from merely shrinking the viewport. Document actual tested dimensions.
6. Define breakpoints where content needs them. Use fluid values only when they preserve an intelligible hierarchy. Verify overflow, image aspect ratios and control wrapping in the browser.
7. Check contrast in the actual composited interface. The offline ACO contrast helper supports opaque sRGB hex colours only; it does not resolve gradients, opacity, images, font rendering or full accessibility compliance.

## Output
Token table, CSS/design-system proposal, before/after evidence, long-content test cases and a short list of unresolved brand decisions. Reuse approved tokens; do not publish an invented universal font-pair catalogue.

## Research provenance and limits

Comparison references: [S09](https://github.com/pbakaus/impeccable), [S10](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [S11](https://github.com/vercel-labs/agent-skills).
This is an ACO-authored operating procedure, not a bundled upstream skill. No external installer, runtime, prompt collection, palette/font dataset or model weights are included. Read the source inventory for inspection scope and licence cautions. Source popularity is not a quality benchmark.
