"""Isolated contract tests: no claim of aesthetic evaluation or rendered QA."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = BASE / "skills/aco-taste/scripts"
sys.path.insert(0, str(SCRIPT_ROOT))
from aco_taste import deepening


class Variants(unittest.TestCase):
    def test_palette_swap_is_not_a_concept(self):
        p = {"variants": [
            {"id": "a", "structure": "centered hero", "imagery_role": "decoration", "palette": "red"},
            {"id": "b", "structure": "centered hero", "imagery_role": "decoration", "palette": "blue"}]}
        r = deepening.evaluate_variants(p)
        self.assertEqual(r["status"], "needs-concept-revision")
        self.assertEqual(r["pairwise"][0]["verdict"], "same-template-risk")
        self.assertFalse(r["aesthetic_quality_certified"])

    def test_distinct_morphologies(self):
        p = {"directions": [
            {"id": "index", "structure": "index grid", "imagery_role": "artifact documentation"},
            {"id": "archive", "structure": "annotated scroll", "imagery_role": "full bleed sequences"},
            {"id": "type", "structure": "big typographic index", "imagery_role": "small evidence crops"}]}
        self.assertEqual(deepening.evaluate_variants(p)["status"], "structurally-distinct-on-paper")

    def test_missing_structure_cannot_pass(self):
        p = {"variants": [{"id": "a", "imagery_role": "x"}, {"id": "b", "imagery_role": "y"}]}
        self.assertEqual(deepening.evaluate_variants(p)["pairwise"][0]["verdict"], "unverifiable-structure")

    def test_single_dimension_is_weak(self):
        p = {"variants": [{"structure": "grid", "imagery_role": "hero"},
                          {"structure": "stripe", "imagery_role": "hero"}]}
        self.assertEqual(deepening.evaluate_variants(p)["pairwise"][0]["verdict"], "weak-structural-separation")

    def test_reject_duplicate_ids(self):
        with self.assertRaises(ValueError):
            deepening.evaluate_variants({"variants": [{"id": "a"}, {"id": "a"}]})


class ScopedMemory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        d = self.root / ".aco-taste"
        d.mkdir()
        self.journal = d / "feedback.jsonl"
        self.journal.write_text("\n".join(json.dumps(r) for r in [
            {"id": "1", "scope": "current-project", "reason": "Loose typography improves legibility", "judgment": "prefer", "aspects": ["type"], "variant_id": "A", "time": "2026-10-30"},
            {"id": "2", "scope": "other-client", "reason": "Loose typography is forbidden", "judgment": "reject", "aspects": ["type"], "variant_id": "B", "time": "2026-10-31"},
            {"id": "3", "scope": "current-project", "reason": "Tighter typography helps archival table", "judgment": "depends", "aspects": ["type"], "variant_id": "C", "time": "2026-11-01"},
        ]), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_scoped_search_preserves_conflicts(self):
        r = deepening.query_feedback(self.root, "typography", aspect="type")
        self.assertEqual(r["total_matches"], 2)
        self.assertEqual({e["id"] for e in r["evidence"]}, {"1", "3"})
        self.assertFalse(r["model_trained"])

    def test_no_cross_scope_fallback(self):
        r = deepening.query_feedback(self.root, "forbidden")
        self.assertEqual(r["status"], "no-scoped-match")

    def test_missing_journal_is_read_only(self):
        self.journal.unlink()
        self.assertEqual(deepening.query_feedback(self.root, "spacing")["status"], "no-scoped-match")
        self.assertFalse(self.journal.exists())

    def test_corruption_is_not_ignored(self):
        self.journal.write_text("not-json", encoding="utf-8")
        with self.assertRaises(ValueError): deepening.query_feedback(self.root, "type")


class Cycle(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.before = self.root / "before.png"
        self.after = self.root / "after.png"
        self.before.write_bytes(b"before snapshot")
        self.after.write_bytes(b"different after snapshot")

    def tearDown(self):
        self.temp.cleanup()

    def receipt(self, path):
        return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "viewed_with": "image viewer", "review_scope": "desktop header"}

    def packet(self):
        return {"findings": [{"id": "F1", "severity": "major", "region_or_timecode": "top 400px",
                              "correction": "Reduce hero occlusion", "observed_result": "Text now clears the figure",
                              "before": self.receipt(self.before), "after": self.receipt(self.after)}]}

    def test_changed_artifact_and_observation(self):
        r = deepening.check_review_cycle(self.packet())
        self.assertEqual(r["status"], "receipt-supported")
        self.assertFalse(r["aesthetic_quality_certified"])

    def test_same_artifact_does_not_pass(self):
        p = self.packet()
        p["findings"][0]["after"] = p["findings"][0]["before"]
        self.assertEqual(deepening.check_review_cycle(p)["status"], "review-incomplete")

    def test_hash_mismatch_fails(self):
        p = self.packet()
        p["findings"][0]["after"]["sha256"] = "bad"
        self.assertEqual(deepening.check_review_cycle(p)["status"], "review-incomplete")

    def test_missing_observation_fails(self):
        p = self.packet()
        p["findings"][0]["observed_result"] = ""
        self.assertEqual(deepening.check_review_cycle(p)["status"], "review-incomplete")


class Motion(unittest.TestCase):
    def test_keyboard_shortcut_not_animated(self):
        r = deepening.motion_triage({"frequency": "occasional", "trigger": "keyboard", "purpose": "decoration"})
        self.assertEqual(r["decision"], "do-not-animate")

    def test_motion_without_purpose(self):
        self.assertEqual(deepening.motion_triage({"frequency": "rare"})["decision"], "do-not-animate")

    def test_reduced_motion_required(self):
        p = {"frequency": "occasional", "purpose": "spatial consistency", "duration_ms": 200}
        self.assertEqual(deepening.motion_triage(p)["decision"], "revise-before-implementation")

    def test_low_cost_motion_can_be_reviewed(self):
        p = {"frequency": "occasional", "purpose": "state indication", "duration_ms": 180,
             "reduced_motion": True, "properties": ["opacity", "transform"]}
        self.assertEqual(deepening.motion_triage(p)["decision"], "candidate-for-rendered-review")

    def test_layout_animation_flagged(self):
        p = {"frequency": "rare", "purpose": "state indication", "reduced_motion": True,
             "properties": ["height"]}
        self.assertTrue(deepening.motion_triage(p)["findings"])


class CLI(unittest.TestCase):
    def test_packet_routing(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "packet.json"
            p.write_text(json.dumps({"variants": [
                {"structure": "index", "imagery_role": "documentation"},
                {"structure": "full-bleed", "imagery_role": "narrative"}]}))
            command = [sys.executable, str(SCRIPT_ROOT / "deepen.py"), "variants", "--packet", str(p)]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "structurally-distinct-on-paper")


if __name__ == "__main__":
    unittest.main()
