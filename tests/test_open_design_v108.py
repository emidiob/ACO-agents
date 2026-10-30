import unittest
import sys
from pathlib import Path
import json
import tempfile
import xml.etree.ElementTree as ET
import shutil
import importlib.util
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from aco.open_design import SYSTEMS, ROUTES, validate_brief, render, audit, build, make_gallery
from aco.open_design_gallery import list_examples, remix
from aco.open_design_systems import contrast_report, resolve_system
from aco.open_design_export import available_browser, export_artifact
from aco.open_design_vector import vector_svg
from aco.open_design_handoff import prepare_handoff


class OpenDesignTest(unittest.TestCase):
    def setUp(self):
        self.brief = {"kind": "landing", "title": "A <script> example", "description": "Research & design",
                      "audience": "Institutions", "sections": [{"heading": "About", "body": "A < B"}]}

    def test_each_type_routes(self):
        for kind in ROUTES:
            self.assertIn("accessibility", validate_brief({**self.brief, "kind": kind})["competencies"])

    def test_each_system_renders(self):
        for system in SYSTEMS:
            content = render(validate_brief({**self.brief, "system": system}))
            self.assertTrue(audit(validate_brief({**self.brief, "system": system}), content)["pass"])

    def test_escapes_untrusted_input(self):
        content = render(validate_brief(self.brief))
        self.assertNotIn("<script>", content)
        self.assertIn("&lt;script&gt;", content)

    def test_rejects_malformed_brief(self):
        with self.assertRaises(ValueError):
            validate_brief({"kind": "landing"})
        with self.assertRaises(ValueError):
            validate_brief({**self.brief, "sections": [{}]})

    def test_review_not_faked(self):
        c = validate_brief(self.brief)
        self.assertEqual(audit(c, render(c))["visual_review"], "not performed")

    def test_eight_original_gallery_examples(self):
        examples = list_examples()
        self.assertEqual(len(examples), 8)
        self.assertEqual(len({x["id"] for x in examples}), 8)
        for example in examples:
            c = validate_brief(remix(example["id"]))
            self.assertTrue(audit(c, render(c))["pass"])

    def test_layouts_are_distinct(self):
        html = {kind: render(validate_brief({**self.brief, "kind": kind})) for kind in ROUTES}
        self.assertIn('class="dashboard"', html["dashboard"])
        self.assertIn('class="deck"', html["deck"])
        self.assertIn('class="poster"', html["social"])
        self.assertIn('class="sections"', html["landing"])

    def test_custom_tokens_and_contrast(self):
        custom = dict(SYSTEMS["minimal"])
        c = validate_brief({**self.brief, "tokens": custom})
        self.assertEqual(c["tokens"], custom)
        self.assertGreaterEqual(contrast_report(c["tokens"])["ratios"]["body"], 4.5)
        with self.assertRaises(ValueError):
            validate_brief({**self.brief, "tokens": {**custom, "accent": "url(javascript:bad)"}})

    def test_dangerous_cta_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_brief({**self.brief, "cta": {"label": "Click", "href": "javascript:alert(1)"}})
        self.assertIn('href="https://example.org"', render(validate_brief({**self.brief, "cta": {"label": "Visit", "href": "https://example.org"}})))

    def test_build_creates_html_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "design.html"
            result = build(self.brief, target)
            self.assertTrue(target.is_file())
            self.assertTrue(Path(result["manifest"]).is_file())
            self.assertEqual(json.loads(Path(result["manifest"]).read_text())["schema"], "aco-open-design/artifact-v1")

    def test_gallery_writes_all_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            result = make_gallery(Path(directory))
            self.assertEqual(result["examples"], 8)
            self.assertEqual(len(list(Path(directory).glob("*.html"))), 9)

    def test_gallery_passes_existing_aco_webdesign_static_audit(self):
        checker = Path(__file__).resolve().parents[1] / "skills/aco-webdesign/scripts/audit_html.py"
        spec = importlib.util.spec_from_file_location("aco_webdesign_html_audit", checker)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            make_gallery(Path(directory))
            for example in list_examples():
                result = module.audit(Path(directory) / (example["id"] + ".html"))
                self.assertEqual(result["findings"], [], example["id"])

    def test_export_fail_closed_without_browser(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "page.html"
            source.write_text(render(validate_brief(self.brief)))
            with self.assertRaises(ValueError):
                export_artifact(source, Path(directory) / "invalid.jpg")
            if available_browser() is None:
                with self.assertRaises(RuntimeError):
                    export_artifact(source, Path(directory) / "image.png")

    def test_vector_export_is_parseable_and_escaped(self):
        svg = vector_svg(validate_brief(self.brief))
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertNotIn("<script>", svg)
        with self.assertRaises(ValueError):
            vector_svg(validate_brief(self.brief), width=200)

    def test_deck_slide_vector(self):
        c = validate_brief({**self.brief, "kind": "deck"})
        self.assertIn("A &lt;script&gt; example", vector_svg(c))
        with self.assertRaises(ValueError):
            vector_svg(c, slide_index=2)

    def test_handoff_never_calls_remote(self):
        with tempfile.TemporaryDirectory() as directory:
            svg = Path(directory) / "design.svg"
            svg.write_text(vector_svg(validate_brief(self.brief)))
            packet = prepare_handoff(svg, "figma")
            self.assertEqual(packet["status"], "pending_external_action")
            self.assertIsNone(packet["provider_receipt"])
            self.assertEqual(len(packet["sha256"]), 64)
            with self.assertRaises(ValueError):
                prepare_handoff(svg, "nonexistent")

    @unittest.skipUnless(shutil.which("inkscape"), "Inkscape unavailable")
    def test_svg_export_to_png_and_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "vector.svg"
            src.write_text(vector_svg(validate_brief(self.brief)))
            for ext in ("png", "pdf"):
                target = Path(directory) / ("vector." + ext)
                result = export_artifact(src, target)
                self.assertEqual(result["engine"], "inkscape")
                self.assertGreater(target.stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
