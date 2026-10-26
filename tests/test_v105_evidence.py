"""ACO 1.0.5 technical registry evidence and candidate non-promotion regressions."""
import json
import unittest
from scripts.aco.common import ROOT, ACOError
from scripts.aco.skills import skill_registry_check, skill_resolve, skill_search

class Evidence105Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'registry/skills.json').read_text(encoding='utf-8'))
        cls.e=json.loads((ROOT/'release/skill-evidence-v1.0.5.json').read_text(encoding='utf-8'))
        cls.p=json.loads((ROOT/'config/skill-policy.json').read_text(encoding='utf-8'))

    def test_104_baseline_roles_and_new_entrypoints(self):
        self.assertEqual((ROOT/'VERSION').read_text().strip(),'1.0.5')
        for name in ('aco','aco-genjutsu','aco-video','aco-image','aco-capture','aco-skills','aco-help'):
            self.assertTrue((ROOT/'skills'/name/'SKILL.md').exists())

    def test_all_technical_registry_bodies(self):
        v=skill_registry_check(ROOT)
        self.assertEqual((v['status'],v['skills'],v['active_skills'],v['candidate_skills']),('valid',44,14,30))
        self.assertEqual(v['errors'],[])

    def test_previous_active_skills_kept(self):
        records=self.r['skills']; active=[s for s in records if s['status']=='active']
        self.assertEqual(len(active),14)
        self.assertTrue(all(s['skill_id'].startswith(('visual_research.','product_design.','frontend_motion.')) for s in active))
        self.assertFalse(any(s['skill_id'].startswith(('video.','image.')) for s in active))

    def test_no_candidate_mislabeled_or_auto_selected(self):
        exp=[s for s in self.r['skills'] if s['status'] in ('candidate','candidate_unverified','testing')]
        self.assertEqual(len(exp),30)
        for skill in exp:
            with self.subTest(skill=skill['skill_id']):
                with self.assertRaises(ACOError): skill_resolve(skill['skill_id'],root=ROOT)
                x=skill_resolve(skill['skill_id'],allow_candidate=True,root=ROOT)
                self.assertFalse(x['selectable'])
                self.assertEqual(x['body']['status'],skill['status'])

    def test_evidence_coverage_and_disclosure(self):
        ev=self.e
        self.assertEqual(ev['aco_version'],'1.0.5')
        self.assertEqual(ev['technical_total'],44)
        self.assertEqual(ev['existing_active_methods'],14)
        self.assertEqual(ev['candidates_unvalidated_for_default_use'],30)
        self.assertEqual(ev['provider_renders_tested_this_build'],0)
        self.assertEqual({s['skill_id'] for s in ev['skills']},{s['skill_id'] for s in self.r['skills']})
        for s in ev['skills']:
            self.assertFalse(s['real_provider_output_test_verified'])
            self.assertFalse(s['promotion_requested_or_performed'])

    def test_non_weakened_promotion_contract(self):
        q=self.p['promotion']
        self.assertGreaterEqual(q['minimum_benchmark_cases'],20)
        self.assertGreaterEqual(q['minimum_score'],95)
        self.assertEqual(q['maximum_critical_failures'],0)
        self.assertTrue(q['requires_explicit_approval'])
        self.assertTrue(q['requires_rollback_ref'])
        self.assertTrue(q['requires_frozen_first_run'])

    def test_genjutsu_is_prompt_only(self):
        a=skill_resolve('video.seedance.reference-video-replica',allow_candidate=True,root=ROOT)
        self.assertIn('only',a['body']['method'][0])
        self.assertIn('@Video1',str(a['body']['method']))
        self.assertFalse(a['selectable'])
        self.assertIn('/aco-genjutsu',(ROOT/'CHATGPT.md').read_text())

if __name__=='__main__':unittest.main()
