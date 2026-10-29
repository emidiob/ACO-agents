"""Prompt-only reference-video recreation remains gated in ACO's technical registry."""
import unittest
from scripts.aco.common import ACOError, ROOT
from scripts.aco.skills import skill_registry_check, skill_resolve, skill_search

SKILL_ID = "video.seedance.reference-video-replica"

class ReferenceVideoReplicaCandidateTests(unittest.TestCase):
    def test_registry_counts(self):
        got = skill_registry_check(ROOT)
        self.assertEqual((got["status"], got["skills"], got["active_skills"], got["candidate_skills"]),
                         ("valid", 64, 34, 30))

    def test_not_automatically_selectable(self):
        self.assertFalse(any(row["skill_id"] == SKILL_ID for row in
                             skill_search("seedance reference video replica motion transfer", root=ROOT)["results"]))
        with self.assertRaises(ACOError):
            skill_resolve(SKILL_ID, root=ROOT)

    def test_explicit_inspection(self):
        rows = skill_search("reference video replica motion transfer", include_candidates=True,
                            root=ROOT)["results"]
        self.assertTrue(any(row["skill_id"] == SKILL_ID and not row["selectable"] for row in rows))
        item = skill_resolve(SKILL_ID, allow_candidate=True, root=ROOT)
        self.assertEqual(item["body"]["status"], "candidate")
        self.assertTrue(item["body"]["sources"])
        self.assertIn("only", item["body"]["method"][0])
        self.assertTrue(any("@Video1" in line for line in item["body"]["method"]))

if __name__ == "__main__":
    unittest.main()
