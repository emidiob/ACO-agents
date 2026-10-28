# Verify behavior and visual quality separately

Run the project's build/tests first. `scripts/audit_html.py` is an optional narrow check on rendered/static HTML for document structure, names, labels, IDs and placeholder links. It does not parse JSX, execute JavaScript, resolve CSS, evaluate contrast, measure performance or certify accessibility. Supply the built HTML or use browser tools for framework-rendered interfaces. Empty findings mean only that those checks found nothing.

Use an available browser to inspect at least a representative narrow and wide layout for substantive UI work. Record which viewport and route were actually inspected. Check page overflow, long copy, media, content order and the main action. Exercise keyboard navigation, focus visibility, dialogs/Escape/focus return and form feedback where relevant. Inspect loading/empty/error states if the interface has them. Check reduced motion using an actual preference/emulation when possible; a CSS rule alone is not runtime evidence.

Review hierarchy, typography, spacing, imagery and coherence visually. DOM assertions don't prove visual craft; screenshots don't prove interaction. Avoid absolute aesthetic scores. Report concrete observations and fix the meaningful failures, then recheck affected behavior. Do not claim mobile, screen-reader, performance or accessibility coverage that was not executed.

When available use appropriate browser profiling, axe or Lighthouse to supplement the task-specific review. Interpret measured findings and preserve the actual conditions. Distinguish code checked, rendered, visually inspected, interaction tested and untested. Finish with editable source, runnable preview and material limitations rather than a generic quality claim.
