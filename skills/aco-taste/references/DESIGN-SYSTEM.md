# Design-system evidence (ACO original; UI Skills studied)

A single confirmed `DESIGN.md` is the source of truth for each product. The document should distinguish **approved design intent** from **observed implementation**, and retain source, scope, recurrence and confidence. Do not promote duplicated CSS or design accidents into product standards.

- If source code is available, follow actual imports/components, variables, themes and tokens and the selected deployable product. Exclude stale migrations, unused UI libraries and unrelated sibling products.
- If only a public URL is supplied, computed browser styles may establish visible values but not internal token names, component ownership or intentions. If browser rendering is missing, generate a marked draft only, not fabricated tokens.
- Extract each role (paper, ink, accent, heading/body, spacing, radius, focus) and bind it to an observed or approved source. When two legitimate sources disagree, stop rather than overwrite one.
- Preserve component variants and states; a single screenshot proves neither loading/error/hover nor keyboard behavior.
- One component at a time in a variant canvas; compare with identical text, sample data and theme so effects are not mistaken for properties. Don't mutate original components for the demo.
- Audits must cite a binding contract and evidence; otherwise label a suggestion, not a proven defect.

`taste.py design-md --packet evidence.json --project PATH` previews the result and refuses to overwrite an existing `DESIGN.md` without an explicit packet instruction. `--apply` writes only the bounded document, not product code.
