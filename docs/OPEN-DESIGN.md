# ACO Open Design — native design kit (ACO 1.0.9)

ACO Open Design is a **file-based, original** design kit inside ACO. It combines bounded creative briefs, a small original gallery, reusable design tokens, four HTML composition types, a project manifest, static evidence checks and optional browser export. It works alongside the existing `aco-webdesign` skill, which owns deeper visual direction, interaction design, framework code editing and actual rendered review.

No third-party Open Design Agent Kit code, examples, fonts, templates, branded systems or artwork are copied here. [Open Design Agent Kit](https://github.com/feimacode/open-design-agent-kit) was a capability reference; this is not a clone or an MCP server.

## Taste integration

Open Design complements [ACO Taste](../skills/aco-taste/SKILL.md). Load the [automatic visual gate](../skills/aco-office-concierge/references/protocols/VISUAL-TASTE-ROUTING.md) for direction and actual rendered review. Use the brief and chosen tokens as inputs; inspect HTML/SVG or exported pages and correct material issues before delivery. CLI structural and contrast checks remain separate evidence and never mark visual review complete.

## At a glance

| Capability | Present | Boundary |
|---|---|---|
| 7 original design-token systems | Yes | Not a set of third-party brand identities |
| Custom validated token overrides | Yes | Five supported token fields; simple JSON |
| 8 original remixable examples | Yes | Fictional sample content, not user projects |
| Landing, dashboard, slide deck and social HTML | Yes | Four distinct HTML layouts; not full app state logic |
| Local gallery HTML | Yes | Static previews, no background service |
| Project manifest and structural checks | Yes | Not a browser or assistive-technology audit |
| PDF/PNG export | Conditional | HTML requires browser; SVG requires Inkscape |
| Editable SVG composition | Yes | Original typographic vector layout; not HTML-to-SVG conversion |
| Figma/Canva/Drive handoff | Prepared packet | Requires separately connected, approved host action to upload |
| LLM-driven composition from natural-language prompts | Delegated to ACO/host | CLI itself is deterministic, uses JSON input |
| Visual quality certification | No | Requires rendered and human/specialist review |

## Commands

From the full ACO source checkout:

```sh
python3 scripts/aco_open_design.py systems
python3 scripts/aco_open_design.py examples
python3 scripts/aco_open_design.py remix research-studio --output /tmp/studio-brief.json
python3 scripts/aco_open_design.py plan --brief /tmp/studio-brief.json
python3 scripts/aco_open_design.py build --brief /tmp/studio-brief.json --output /tmp/studio.html
python3 scripts/aco_open_design.py check --brief /tmp/studio-brief.json --artifact /tmp/studio.html
python3 scripts/aco_open_design.py gallery --output /tmp/aco-gallery
python3 scripts/aco_open_design.py vector --brief /tmp/studio-brief.json --output /tmp/studio.svg
python3 scripts/aco_open_design.py handoff --artifact /tmp/studio.svg --target figma
python3 -m http.server 8768 --bind 127.0.0.1 --directory /tmp/aco-gallery
```

Open `http://127.0.0.1:8768` in your browser to inspect the gallery. The browser is not launched automatically. A generated HTML file has a neighboring `.manifest.json` containing the brief contract, token resolution and static checks. Existing output is protected; `build`, `remix` and `export` require explicit `--overwrite` to replace an artifact. A gallery target must be empty.

### Export with an installed browser

```sh
python3 scripts/aco_open_design.py export --source /tmp/studio.html --output /tmp/studio.pdf
python3 scripts/aco_open_design.py export --source /tmp/studio.html --output /tmp/studio.png --width 1440 --height 900
python3 scripts/aco_open_design.py export --source /tmp/studio.svg --output /tmp/studio.png
```

If the browser cannot be found, pass `--browser /path/to/chromium` for HTML export. SVG-to-PNG/PDF uses an existing Inkscape installation instead. The tool does not download, install or use a remote rendering service. HTML PDF uses the page's print CSS; slide decks have page breaks. HTML PNG is a viewport screenshot, not a multi-page image. Verify the exported file visually and check dimensions/page count for the intended destination.

SVG output is a separate original vector composition based on the same brief, not a pixel-identical conversion of the HTML. For decks, choose `--slide 0` for the cover or `--slide 1` and upward for individual slides. Excessive text causes an explicit error rather than silent truncation. A handoff packet for `figma`, `canva`, or `drive` contains a local artifact path, SHA-256 and the requested operation; it deliberately does **not** upload anything. ACO must resolve the actual connected capability and authorization before an external action.

## Brief format

```json
{
  "kind": "landing",
  "system": "editorial",
  "language": "en",
  "title": "A project title",
  "description": "A concise statement grounded in approved content.",
  "audience": "Institutions and cultural partners",
  "cta": {"label": "Discover", "href": "#features"},
  "sections": [{"heading": "Research", "body": "An introductory section."}]
}
```

`kind`: `landing`, `dashboard`, `deck`, `social`. Dashboards may specify up to eight `metrics` objects with `label`, `value` and optional `detail`; all figures are user-supplied and are not represented as live. For a custom system, pass `tokens` with `background`, `foreground`, `surface`, `accent` as six-digit hex colors, plus an approved `font` stack. The contrast report checks text against background/surface and warns when the ratios fall below 4.5:1. This is not a WCAG certification.

Use `--overrides /path/to/content.json` with `remix` to replace approved content and tokens. Links accept local fragment anchors, HTTPS or `mailto:`; arbitrary JavaScript URLs and raw HTML injection are rejected.

## ACO workflow

1. Concierge selects the smallest Agency/Product/Publishing specialist and scopes the client/project.
2. Load the relevant existing ACO competencies: visual-critique, UX, accessibility, editorial or copy.
3. Use `aco-webdesign` direction and existing approved project tokens/components when available; the seven presets are only fallbacks.
4. Select/remix one of the eight fictional examples or author a new brief; produce a representative HTML artifact.
5. Inspect it in a real browser and run the existing `aco-webdesign` audit/review as appropriate. Compare mobile/desktop/print, overflow, focus, long content and reduced motion.
6. Revise, export only through the installed/authorized tool, and hand off the verified files with known limitations.

## Testing and maintenance

```sh
python3 -m unittest discover -s tests -p 'test_open_design_v108.py' -v
python3 scripts/generate.py
python3 scripts/build_manifest.py
python3 scripts/aco_cli.py validate
python3 -m unittest discover -s tests -q
```

The build generator carries all Open Design sources and the gallery into `skills/aco-office-concierge/runtime/`. The new module is **not** an independent registered skill, and does not promote the existing experimental technical candidates. It inherits ACO's ordinary scope, permission, rights and verification policies.

## Provenance and rights

All bundled gallery text, design tokens, templates and code in this module are original additions. The separate third-party kit identifies MIT code and some Apache-2.0 content; none is bundled. Preserve ACO's existing license and check any future third-party asset source individually before copying it.
