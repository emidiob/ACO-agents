"""Regression: the unified release ships both visual systems and keeps review honest."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class UnifiedVisualReleaseTest(unittest.TestCase):
    def test_taste_and_open_design_are_both_packaged(self):
        self.assertTrue((ROOT / "skills/aco-taste/SKILL.md").is_file())
        self.assertTrue((ROOT / "scripts/aco/open_design.py").is_file())
        self.assertTrue((ROOT / "skills/aco-office-concierge/runtime/scripts/aco/open_design.py").is_file())

    def test_both_entrypoints_keep_automatic_taste_gate(self):
        for skill in ("aco", "aco-office-concierge"):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text()
            self.assertIn("VISUAL-TASTE-ROUTING.md", text)
            self.assertIn("aco_open_design.py", text)

    def test_open_design_contract_requires_rendered_review(self):
        text = (ROOT / "docs/OPEN-DESIGN.md").read_text()
        self.assertIn("automatic visual gate", text)
        self.assertIn("never mark visual review complete", text)
