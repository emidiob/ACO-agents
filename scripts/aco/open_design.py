"""ACO Open Design — native design brief, gallery, rendering and export CLI.

The creative brief and human review remain authoritative. This code supplies
deterministic templates and does not claim model generation or live visual QA.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from .open_design_export import export_artifact
from .open_design_handoff import prepare_handoff, TARGETS
from .open_design_gallery import list_examples, remix
from .open_design_render import render as render_html, safe_href
from .open_design_systems import SYSTEMS, contrast_report, resolve_system
from .open_design_vector import vector_svg

ROUTES = {
    "landing": ("visual-critique", "ux-research", "accessibility"),
    "dashboard": ("visual-critique", "ux-research", "accessibility"),
    "deck": ("visual-critique", "editorial-verification", "accessibility"),
    "social": ("visual-critique", "copy-positioning", "accessibility"),
}


def validate_brief(brief: dict) -> dict:
    if not isinstance(brief, dict):
        raise ValueError("Brief must be a JSON object")
    kind = brief.get("kind")
    system = brief.get("system", "editorial")
    if kind not in ROUTES or not isinstance(system, str):
        raise ValueError("Unsupported kind or design system")
    for key in ("title", "description", "audience"):
        if not isinstance(brief.get(key), str) or not brief[key].strip() or len(brief[key]) > 800:
            raise ValueError("Missing, invalid or oversized field: " + key)
    sections = brief.get("sections", [])
    if not isinstance(sections, list) or len(sections) > 12:
        raise ValueError("sections must be an array of at most 12 items")
    for s in sections:
        if not isinstance(s, dict) or not all(isinstance(s.get(k), str) and len(s[k]) <= 2500 for k in ("heading", "body")):
            raise ValueError("Each section needs bounded heading and body strings")
    metrics = brief.get("metrics", [])
    if not isinstance(metrics, list) or len(metrics) > 8:
        raise ValueError("metrics must be an array of at most 8 items")
    for m in metrics:
        if not isinstance(m, dict) or not all(isinstance(m.get(k), str) and len(m[k]) <= 300 for k in ("label", "value")) or not isinstance(m.get("detail", ""), str):
            raise ValueError("Each metric needs label, value and optional detail")
    language = brief.get("language", "en")
    if not isinstance(language, str) or not re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?", language):
        raise ValueError("Invalid BCP47 language code")
    cta = brief.get("cta")
    if cta is not None:
        if not isinstance(cta, dict) or not isinstance(cta.get("label"), str) or not isinstance(cta.get("href"), str) or len(cta["label"]) > 120:
            raise ValueError("Invalid CTA")
        safe_href(cta["href"])
    tokens = resolve_system(system, brief.get("tokens"))
    return {"kind": kind, "system": system, "title": brief["title"], "description": brief["description"],
            "audience": brief["audience"], "sections": sections, "metrics": metrics,
            "cta": cta, "language": language, "tokens": tokens,
            "competencies": list(ROUTES[kind]), "schema": "aco-open-design/1.0.8"}


def render(contract: dict) -> str:
    return render_html(contract)


class _Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.main_ids = 0
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        data = dict(attrs)
        if tag == "main" and data.get("id") == "main":
            self.main_ids += 1
        if tag == "a":
            self.links.append(data.get("href"))


def audit(contract: dict, artifact: str) -> dict:
    parsed = _Structure()
    parsed.feed(artifact)
    expected = [contract["title"], contract["description"]]
    expected.extend(s["heading"] for s in contract["sections"])
    expected.extend(s["body"] for s in contract["sections"])
    if contract["kind"] == "dashboard":
        expected.extend(m["label"] for m in contract["metrics"])
        expected.extend(m["value"] for m in contract["metrics"])
    if contract["kind"] == "social":
        expected = expected[:2] + ([contract["sections"][0]["body"]] if contract["sections"] else [])
    checks = {"doctype": artifact.startswith("<!doctype html>"),
              "viewport": 'name="viewport"' in artifact,
              "main_landmark": parsed.main_ids == 1,
              "skip_link": "#main" in parsed.links,
              "reduced_motion": "prefers-reduced-motion" in artifact,
              "escaped_script": "<script" not in artifact.lower(),
              "title": bool(re.search(r"<title>[^<]+</title>", artifact)),
              "responsive_css": "@media(max-width:" in artifact,
              "print_css": "@media print" in artifact,
              "brief_content": all(html.escape(value, quote=True) in artifact for value in expected)}
    ratios = contrast_report(contract["tokens"])
    return {"pass": all(checks.values()), "checks": checks, "contrast": ratios,
            "visual_review": "not performed", "assistive_technology_test": "not performed",
            "competencies": contract["competencies"]}


def build(brief: dict, target: Path, *, overwrite: bool = False) -> dict:
    contract = validate_brief(brief)
    artifact = render(contract)
    report = audit(contract, artifact)
    if not report["pass"]:
        raise ValueError("Structural audit failed")
    target = target.resolve()
    if target.suffix.lower() != ".html":
        raise ValueError("Build output must be an .html file")
    manifest = target.with_suffix(".manifest.json")
    if not overwrite and (target.exists() or manifest.exists()):
        raise FileExistsError("Artifact or manifest already exists; explicit overwrite required")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(artifact, encoding="utf-8")
    manifest.write_text(json.dumps({"schema": "aco-open-design/artifact-v1", "source": "local-brief", "contract": contract,
                                    "checks": report, "artifact": target.name}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**report, "artifact": str(target), "manifest": str(manifest)}


def make_gallery(target: Path) -> dict:
    target = target.resolve()
    if target.exists() and any(target.iterdir()):
        raise FileExistsError("Gallery target must be empty")
    target.mkdir(parents=True, exist_ok=True)
    examples = list_examples()
    links = []
    for example in examples:
        name = example["id"]
        item_path = target / (name + ".html")
        build(remix(name), item_path)
        links.append(f'<li><a class="card" href="{name}.html"><div class="thumb"><iframe title="Preview of {name}" sandbox="" loading="lazy" tabindex="-1" src="{name}.html"></iframe></div><div class="cardinfo"><strong>{name.replace("-", " ").title()}</strong><span>{example["kind"]}</span></div></a></li>')
    index = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
             '<title>ACO Design Gallery</title><style>body{font:1.1rem system-ui;background:#eeeae3;color:#17171a;max-width:1200px;margin:2rem auto;padding:1.5rem;line-height:1.6}h1{font-size:clamp(2rem,5vw,4rem);letter-spacing:-.05em}ul{padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:1.2rem}.card{display:block;background:#fff;color:inherit;text-decoration:none;border:1px solid #b9b5ad}.card:focus-visible{outline:4px solid #1b59ad}.cardinfo{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1rem;font-size:.9rem}.cardinfo span{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em}.thumb{height:205px;overflow:hidden;position:relative;pointer-events:none}.thumb iframe{border:0;width:1200px;height:800px;transform:scale(.28);transform-origin:top left;pointer-events:none}</style>'
             '<main><h1>ACO Open Design — original examples</h1><p>Eight standalone HTML compositions. All text is illustrative.</p><ul>'
             + "".join(links) + '</ul></main></html>')
    (target / "index.html").write_text(index, encoding="utf-8")
    return {"gallery": str(target / "index.html"), "examples": len(examples)}


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="ACO Open Design — native, file-based design kit")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("systems", help="List original design-token systems")
    p_list = sub.add_parser("examples", help="List original gallery examples")
    p_list.add_argument("--kind", choices=ROUTES)
    p_remix = sub.add_parser("remix", help="Create an editable brief from a gallery example")
    p_remix.add_argument("id")
    p_remix.add_argument("--output", required=True, type=Path)
    p_remix.add_argument("--overrides", type=Path, help="Optional JSON patch of permitted content fields")
    p_remix.add_argument("--overwrite", action="store_true")
    p_plan = sub.add_parser("plan", help="Print structured plan without writing")
    p_plan.add_argument("--brief", required=True, type=Path)
    p_build = sub.add_parser("build", help="Produce HTML and JSON manifest")
    p_build.add_argument("--brief", required=True, type=Path)
    p_build.add_argument("--output", required=True, type=Path)
    p_build.add_argument("--overwrite", action="store_true")
    p_gallery = sub.add_parser("gallery", help="Generate a browseable local HTML example gallery")
    p_gallery.add_argument("--output", required=True, type=Path)
    p_check = sub.add_parser("check", help="Recheck a generated artifact against its brief")
    p_check.add_argument("--brief", required=True, type=Path)
    p_check.add_argument("--artifact", required=True, type=Path)
    p_export = sub.add_parser("export", help="PDF/PNG export from HTML (browser) or SVG (Inkscape)")
    p_export.add_argument("--source", "--html", required=True, dest="source", type=Path)
    p_export.add_argument("--output", required=True, type=Path)
    p_export.add_argument("--browser", help="Explicit Chrome/Chromium/Edge executable path")
    p_export.add_argument("--width", type=int, default=1440)
    p_export.add_argument("--height", type=int, default=900)
    p_export.add_argument("--overwrite", action="store_true")
    p_vector = sub.add_parser("vector", help="Create an original editable SVG composition")
    p_vector.add_argument("--brief", required=True, type=Path)
    p_vector.add_argument("--output", required=True, type=Path)
    p_vector.add_argument("--width", type=int, default=1080)
    p_vector.add_argument("--height", type=int, default=1080)
    p_vector.add_argument("--slide", type=int, default=0, help="Deck slide index: 0 is cover")
    p_vector.add_argument("--overwrite", action="store_true")
    p_handoff = sub.add_parser("handoff", help="Prepare a provider-specific pending-action packet")
    p_handoff.add_argument("--artifact", required=True, type=Path)
    p_handoff.add_argument("--target", required=True, choices=TARGETS)
    parser.add_argument("--brief", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.command == "systems":
        result = {"systems": SYSTEMS}
    elif args.command == "examples":
        result = {"examples": [{"id": e["id"], "kind": e["kind"], "system": e["system"], "title": e["title"]} for e in list_examples(args.kind)]}
    elif args.command == "remix":
        result = remix(args.id, _load(args.overrides) if args.overrides else None)
        if args.output.exists() and not args.overwrite:
            raise FileExistsError("Brief already exists; explicit overwrite required")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = {"brief": str(args.output)}
    elif args.command == "plan" or (args.command is None and args.brief and not args.output):
        result = validate_brief(_load(args.brief))
    elif args.command == "build" or (args.command is None and args.brief and args.output):
        result = build(_load(args.brief), args.output, overwrite=getattr(args,"overwrite",False))
    elif args.command == "gallery":
        result = make_gallery(args.output)
    elif args.command == "check":
        result = audit(validate_brief(_load(args.brief)), args.artifact.read_text(encoding="utf-8"))
        if not result["pass"]:
            print(json.dumps(result, indent=2))
            raise SystemExit(1)
    elif args.command == "export":
        if args.output.exists() and not args.overwrite:
            raise FileExistsError("Export already exists; explicit overwrite required")
        result = export_artifact(args.source, args.output, browser=args.browser, width=args.width, height=args.height, overwrite=args.overwrite)
    elif args.command == "vector":
        if args.output.suffix.lower() != ".svg":
            raise ValueError("Vector output requires an .svg filename")
        if args.output.exists() and not args.overwrite:
            raise FileExistsError("SVG already exists; explicit overwrite required")
        svg = vector_svg(validate_brief(_load(args.brief)), width=args.width, height=args.height, slide_index=args.slide)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
        result = {"vector": str(args.output.resolve()), "editable_svg": True, "visual_review": "not performed"}
    elif args.command == "handoff":
        result = prepare_handoff(args.artifact, args.target)
    else:
        parser.print_help()
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
