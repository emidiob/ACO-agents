# Live editing, review and reusable components

Run commands from the installed `aco-webdesign` directory. Output belongs in the user's project, outside the skill. These Python tools require Python 3.10 or newer; exported pages use modern browser APIs and require no package installation or network service.

## Edit a local page

```bash
python3 scripts/live_editor.py --project /canonical/path/to/project
```

Open the printed loopback URL. Choose a page, select an element in the preview, edit its text or an allowed inline CSS property, then save. The HTML file changes immediately. Undo and redo preserve exact prior bytes during the current server session (up to 50 edits). A changed source hash blocks stale saves and history operations. Reload to select the current source. Writes are atomic and preserve file permissions.

The editor accepts static `.html`/`.htm` files and simple inline declarations. Text changes are limited to leaf elements so nested markup is not destroyed. Edit framework components, template expressions, shared stylesheets and complex markup in the project's source editor, then use the project's own preview/HMR. The live editor is not a React/Vue source mapper. It does not run a build command. Use it only with trusted local project code. Hidden paths and symlinks are excluded; the listener binds to `127.0.0.1` and mutations require the session token and same origin. Do not expose this development server publicly.

## Review measured design

Capture the schema 2 snapshot with `assets/browser-probe.js` through the host's authorized browser tools. Capture browser errors separately and add the returned error records as `scriptErrors`; omit that field if error capture is unavailable. Never substitute an empty error array for an unavailable log.

```bash
python3 scripts/audit_snapshot.py /project/evidence/page-dom.json
python3 scripts/audit_design.py /project/evidence/page-dom.json
python3 scripts/audit_design.py /project/evidence/page-dom.json --system /project/design-contract.json --ignore common-font
```

The first command applies 17 structural checks. The second applies 62 design-review predicates covering type, spacing, color, geometry, copy, media, movement and system consistency. `assets/design-rules.json` lists their IDs and meanings. An optional design contract supplies `fonts`, `colors` (opaque RGB or six-digit hex), `radii` (px), and `fontSizes` (px) arrays. Suppress an intentional element-level choice with `data-aco-ignore="rule-id another-rule"`. Unknown command-line rule IDs are rejected.

Findings are suggestions for contextual review, not proof of bad design or machine authorship. Automated checks do not replace keyboard, screen-reader, interaction or visual inspection. Contrast is computed only when opaque foreground/background colors can be resolved; gradients, images, blending and translucency need manual review. Line geometry covers leaf text; occlusion samples the center point of visible text boxes. The probe does not comprehensively traverse shadow roots or iframes. Missing logs, line/hit-test measurements or design-system contracts are reported as not evaluated. A clean result is not an accessibility certificate.

## Search and export components

```bash
python3 scripts/components.py list --query navigation
python3 scripts/components.py show tabs
python3 scripts/components.py export /project/new-components tabs dialog table
python3 scripts/components.py export /project/component-gallery --all
python3 scripts/effects.py list --query canvas
python3 scripts/effects.py export /project/effects-gallery --all
python3 scripts/effects.py export /project/hero-effect word-reveal --text "A specific idea" --duration 1800
```

The catalog contains 64 HTML component recipes with shared CSS and JavaScript, plus 16 original text, pointer and canvas effects. Exports refuse existing destinations. Each component record states its actual behavior. Form examples validate or update local state; they do not submit to a backend. Calendar/select use native controls. The chart is an SVG bar chart with a data table. Search controls filter local lists. Menu examples demonstrate action selection. These are adaptable HTML recipes, not framework packages or a complete data-grid/charting suite.

Effects provide pause/replay controls, stable accessible text, reduced-motion fallbacks and offscreen drawing suspension. Canvas sizes follow their containers with device pixel ratio capped at two. Ripple input accepts pointer clicks or Enter/Space. Change CSS tokens, text and duration in source. The examples do not include WebGL/3D effects.

Use a local static server to preview exports, or open their `index.html`. When composing multiple instances, namespace IDs and radio names and preserve the corresponding ARIA associations. Copy the needed markup and supporting CSS/JavaScript into the project, then adapt its data, navigation and lifecycle to the framework. Test at actual target widths, with keyboard and reduced motion, before delivery.
