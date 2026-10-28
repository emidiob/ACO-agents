# Project systems and prototype review

Run these tools from the installed skill directory. Keep project configuration, previews and review reports in the actual project, outside the ACO distribution.

## Master tokens and page overrides

`design_system.py` exports a `project-system.json` alongside its proposal. A manually authored system can use the same schema:

```json
{
  "schema": 1,
  "master": {
    "tokens": {
      "color": {"ink": "#182331", "text": "{color.ink}"},
      "space": {"unit": "4px", "section": "calc({space.unit} * 12)"}
    },
    "layout": {"columns": 3}
  },
  "pages": {
    "article": {"tokens": {"space": {"section": "32px"}}, "layout": {"columns": 1}}
  }
}
```

```bash
python3 scripts/project_system.py /project/project-system.json
python3 scripts/project_system.py /project/project-system.json --page article --format css
```

The resolver leaves the master untouched. Objects merge recursively, lists replace and `null` removes a key. Token references resolve against the effective page, so a page override also changes aliases pointing to that token. Cycles, missing references, invalid names and CSS-property collisions are errors. Token paths become custom properties (`space.section` → `--space-section`). Values are CSS values, not declarations; URLs, stylesheet delimiters and escape sequences are refused. Validate the exported values in the target browser before adopting them. Fonts remain project dependencies, not downloaded assets.

Results include the effective configuration, resolved token values, CSS and a source SHA-256. Save the chosen output using the project's usual file workflow. To convert an earlier color-only proposal, use `--from-proposal`; this prints a schema 1 document without modifying the source file.

## Compare working alternatives

Supply two to eight local prototype URLs or absolute paths on the server hosting the comparison:

```json
{
  "title": "Task flow alternatives",
  "variants": [
    {"name": "Inline editor", "url": "/prototype/inline", "rationale": "Edit without leaving the list."},
    {"name": "Detail panel", "url": "/prototype/panel", "rationale": "Keep more context beside each record."}
  ]
}
```

```bash
python3 scripts/prototype_review.py compare /project/variants.json --output /project/public/review
```

The destination must be new. Serve it through the project's existing local server. The page switches between mounted iframes without reloading them, offers side-by-side display, and sets 390/768/1440 px or fluid preview widths. Fixed widths intentionally scroll within the frame container when space is narrower. Record task observations and export the session JSON before closing: notes are in memory, not permanently stored. Browser frame restrictions, CSP, authentication and third-party cookie rules still apply. Review only trusted local application routes. Remote sites are not accepted by this exporter.

This tool compares already working alternatives; it does not manufacture design decisions or claim that screenshot similarity proves equivalent behavior. Test the key task in each variant and record the reason for the chosen design.

## Stress content

```bash
python3 scripts/prototype_review.py stress --seed 42
```

The JSON contains empty content, long copy, unbroken identifiers, multilingual/RTL text, 1,000 stable records, zero/negative/extreme values and loading/error/offline state labels. Bind selected fixtures to real component inputs or test routes. Verify overflow, wrapping, focus, announcements and recovery in the browser. No live page or application store is modified by generating the fixtures.
