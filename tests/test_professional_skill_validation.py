"""ACO 1.0.7 professional technical skill tests (structured synthetic scope)."""
import importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FULL=(ROOT/'scripts/aco/skills.py').is_file()
sys.path.insert(0,str(ROOT))
from scripts.professional_skill_validation import run,ValidationError
if FULL:
 from scripts.aco.skills import skill_resolve,skill_registry_check,skill_search,skill_promotion_check
else:
 skill_resolve=skill_registry_check=skill_search=skill_promotion_check=None

class ProfessionalSkillTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=json.loads((ROOT/'registry/professional-skills-additions.json').read_text())['skills']
 @unittest.skipUnless(FULL,"requires full integrated ACO checkout")
 def test_twenty_entries_are_registered_as_validated(self):
  reg=json.loads((ROOT/'registry/skills.json').read_text())['skills']
  lookup={x['skill_id']:x for x in reg}
  self.assertEqual(len(reg),64)
  for r in self.rows:
   self.assertEqual(lookup[r['skill_id']],r)
   self.assertEqual(r['status'],'validated')
 @unittest.skipUnless(FULL,"requires full integrated ACO checkout")
 def test_preserve_14_active_and_30_candidates(self):
  reg=json.loads((ROOT/'registry/skills.json').read_text())['skills']
  self.assertEqual(len([x for x in reg if x['status']=='active']),14)
  self.assertEqual(len([x for x in reg if x['status'] in {'candidate','candidate_unverified','testing'}]),30)
  self.assertEqual(len([x for x in reg if x['status']=='validated']),20)
  self.assertEqual(skill_registry_check(ROOT)['status'],'valid')
 @unittest.skipUnless(FULL,"requires full integrated ACO checkout")
 def test_selected_skills_resolve_without_experimental_flag(self):
  for r in self.rows:
   item=skill_resolve(r['skill_id'],root=ROOT)
   self.assertTrue(item['selectable'])
   self.assertEqual(item['body']['status'],'validated')
 def test_400_frozen_structured_cases(self):
  res=run(ROOT)
  self.assertEqual((res['status'],res['skills'],res['total_cases'],res['score'],res['critical_failures']),('passed',20,400,100.0,0))
  self.assertEqual({x['cases'] for x in res['per_skill'].values()},{20})
 @unittest.skipUnless(FULL,"requires full integrated ACO checkout")
 def test_original_candidate_promotion_requires_exact_approval(self):
  promotions=json.loads((ROOT/'config/professional-skill-promotions.json').read_text())['candidates']
  for x in promotions:
   packet={'candidate':x['candidate'],'benchmark':{'candidate_sha256':x['candidate_sha256'],'cases':20,'score':100,'critical_failures':0,'frozen_before_first_run':True},'approval':{'approved':False,'candidate_sha256':x['candidate_sha256'],'approval_ref':None}}
   check=skill_promotion_check(packet,root=ROOT)
   self.assertFalse(check['eligible']);self.assertIn('exact explicit approval required',check['errors'])
 def test_first_attempt_failure_is_preserved(self):
  receipt=json.loads((ROOT/'release/v107-professional-first-run.json').read_text())
  self.assertEqual(receipt['first_attempt']['status'],'failed')
  self.assertEqual(receipt['recovery']['rerun_status'],'passed')
  self.assertFalse(receipt['independent_human_review'])
 def test_publication_gate_needs_authorization(self):
  self.assertTrue(json.loads((ROOT/'config/professional-skill-promotions.json').read_text())['exact_hash_approval_required_before_publication'])

if __name__=='__main__':unittest.main()
