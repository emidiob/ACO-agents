"""ACO Capture: structural, routing and candidate non-activation tests."""
import re
import unittest
from scripts.aco.common import ROOT
from scripts.aco.skills import skill_registry_check, skill_search

PLAYBOOK = ROOT / "skills/aco-office-concierge/references/playbooks/ACO-CAPTURE.md"


class ACOCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PLAYBOOK.read_text(encoding="utf-8")

    def test_four_layer_order(self):
        self.assertIn("Frame → Moment → Light → Matter", self.text)
        self.assertIn("four short paragraphs", self.text)
        self.assertIn("subject, action and setting", self.text)

    def test_seven_capture_modes(self):
        names = [
            "Close skate-camera", "Phone snapshot", "Intimate documentary",
            "Motion-blurred photo dump", "Low curbside", "Compact-camera flash",
            "Concealed observation",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertIn(name, self.text)
        self.assertEqual(len(re.findall(r"^### [1-7]\. ", self.text, re.M)), 7)

    def test_fisheye_preset(self):
        for term in ("Night Fisheye Flash", "12mm fisheye", "five visual invariants", "Hard direct on-camera flash"):
            self.assertIn(term.lower(), self.text.lower())

    def test_reference_and_scope_rules(self):
        for term in ("@image1", "9:16", "don't", "inspect actual renders"):
            self.assertIn(term.lower(), self.text.lower())

    def test_role_and_concierge_routing(self):
        for path in (
            "skills/aco-office-concierge/SKILL.md",
            "skills/aco-production-office/SKILL.md",
            "skills/aco-office-concierge/references/agents/art-director.md",
            "skills/aco-production-office/references/agents/visual-prompt-engineer.md",
        ):
            with self.subTest(path=path):
                self.assertIn("ACO-CAPTURE.md", (ROOT / path).read_text(encoding="utf-8"))

    def test_prior_candidates_not_activated(self):
        r = skill_registry_check(ROOT)
        self.assertEqual((r["status"], r["skills"], r["active_skills"], r["candidate_skills"]),
                         ("valid", 64, 34, 30))
        found = skill_search("nano banana", root=ROOT, limit=20)["results"]
        self.assertFalse(any(x["skill_id"].startswith("image.") for x in found))


if __name__ == "__main__":
    unittest.main()
