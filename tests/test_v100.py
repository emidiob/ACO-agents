import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.bootstrap import bootstrap_check,resolve_runtime
from aco.common import ACOError,ROOT,VERSION
from aco.context_compiler import compile_context
from aco.kernel import os_plan
from aco.skills import skill_benchmark,skill_candidate_store,skill_candidate_store_status,skill_registry_check,skill_resolve,skill_search
from aco.token_budget import token_plan

class Bootstrap100Tests(unittest.TestCase):
 def test_version(self):self.assertEqual(VERSION,'1.0.0')
 def test_bootstrap(self):
  r=bootstrap_check(ROOT);self.assertEqual(r['status'],'valid',r['errors']);self.assertEqual(r['bootstrap']['logical_root'],'aco://current');self.assertEqual(r['bootstrap']['host_resolution']['canonical_repository'],'emidiob/ACO-agents')
 def test_runtime_state_separate(self):
  with tempfile.TemporaryDirectory() as td:
   r=resolve_runtime(explicit_root=ROOT,env={'ACO_HOME':td});self.assertTrue(r['code_state_separated']);self.assertFalse(r['preload_repository'])
 def test_bad_runtime_fallback(self):
  with tempfile.TemporaryDirectory() as td:
   r=resolve_runtime(explicit_root=Path(td),env={'ACO_RUNTIME_ROOT':td});self.assertEqual(r['runtime_source'],'packaged_runtime');self.assertFalse(r['attempts'][0]['valid'])

class Context100Tests(unittest.TestCase):
 def sources(self):return [{'id':'req','token_estimate':150,'load_level':0,'relevance':1,'required':True,'private':False,'content_sha256':'a'},{'id':'work','token_estimate':300,'load_level':1,'relevance':.95,'private':False},{'id':'old','token_estimate':6000,'load_level':1,'relevance':.02,'private':False},{'id':'deep','token_estimate':2000,'load_level':2,'relevance':1,'private':False},{'id':'other','token_estimate':200,'load_level':1,'relevance':1,'private':True,'scope_relation':'other_private_entity','scope_id':'b'}]
 def test_small_context(self):
  r=token_plan({'budget_class':'STANDARD','base_tokens':200,'sources':self.sources()});self.assertIn('req',r['selected_source_ids']);self.assertIn('work',r['selected_source_ids']);self.assertNotIn('old',r['selected_source_ids']);self.assertNotIn('other',r['selected_source_ids']);self.assertGreater(r['metrics']['input_reduction_ratio'],.75)
 def test_exact_scope(self):self.assertIn('other',token_plan({'budget_class':'STANDARD','base_tokens':200,'sources':self.sources(),'authorized_private_scope_ids':['b']})['selected_source_ids'])
 def test_refine(self):self.assertIn('deep',token_plan({'budget_class':'DEEP','phase':'refine','sources':self.sources()})['selected_source_ids'])
 def test_delta(self):
  r=compile_context({'task':{'id':'t','text':'Continue'},'sources':self.sources(),'previous_snapshot':{'selected_source_ids':['req'],'content_hashes':{'req':'a'}}});self.assertIn('req',r['capsule']['reused_context_refs']);self.assertFalse(r['capsule']['response_contract']['show_internal_reasoning'])
 def test_needs_refine(self):self.assertEqual(compile_context({'task':{'id':'t','text':'Need more'},'sources':self.sources(),'missing_requirements':['deep']})['status'],'needs_refine')

class Skills100Tests(unittest.TestCase):
 def candidate(self):return {'schema_version':1,'skill_id':'video.test.reusable','scope_id':'scope-a','title':'Reusable','version':'0.1','status':'candidate','method':['separate camera and subject motion'],'failure_modes':[],'inputs':[],'output_contract':{},'evidence':[{'source_ref':'1','outcome':'success'},{'source_ref':'2','outcome':'success'},{'source_ref':'3','outcome':'success'}],'rollback_ref':'r'}
 def test_registry(self):
  r=skill_registry_check(ROOT);self.assertEqual((r['status'],r['skills'],r['active_skills'],r['candidate_skills']),('valid',15,14,1))
 def test_search(self):self.assertEqual(skill_search('React spring physics animation',root=ROOT)['results'][0]['skill_id'],'frontend_motion.react_spring')
 def test_mimic_closed(self):
  with self.assertRaises(ACOError):skill_resolve('software_analysis.mimic_littledavi',root=ROOT)
 def test_os_plan(self):
  r=os_plan({'task':{'id':'t','text':'Animate React spring'},'skill_query':'React spring physics','skill_limit':1,'sources':[{'id':'brief','token_estimate':100,'load_level':0,'relevance':1,'required':True,'private':False}]},root=ROOT);self.assertEqual(r['selected_skill_ids'],['frontend_motion.react_spring']);self.assertFalse(r['runtime']['preload_repository'])
 def test_store_dry(self):
  with tempfile.TemporaryDirectory() as td:
   r=skill_candidate_store(self.candidate(),state_root=Path(td),root=ROOT);self.assertEqual(r['status'],'planned');self.assertFalse((Path(td)/'skills/candidates.json').exists())
 def test_store_idempotent(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);self.assertEqual(skill_candidate_store(self.candidate(),state_root=root,apply=True,root=ROOT)['status'],'stored');self.assertEqual(skill_candidate_store(self.candidate(),state_root=root,apply=True,root=ROOT)['status'],'already_present');self.assertEqual(skill_candidate_store_status(state_root=root)['candidates'],1)
 def test_skill_benchmark(self):self.assertEqual(skill_benchmark(root=ROOT)['score'],100.0)

if __name__=='__main__':unittest.main()
