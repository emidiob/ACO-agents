import json,re,sys,tomllib,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ROOT,read_json
from aco.install import agent_set

class ExpansionTests(unittest.TestCase):
 def setUp(self):self.c=read_json(ROOT/'catalog.json')
 def test_expected_release_coverage(self):
  self.assertEqual(len(self.c['agents']),363);self.assertEqual(self.c['skill_count'],16)
  self.assertEqual(self.c['offices']['product-office']['count'],58)
 def test_new_offices_have_leads(self):
  for o in ['finance-office','commercial-office','people-office','delivery-office','production-office','publishing-office','administration-office']:
   lead=self.c['offices'][o]['lead'];self.assertEqual(self.c['agents'][lead]['office'],o)
 def test_requested_roles_exist(self):
  for role in ['colorist','video_editor','photo_retouch_artist','line_producer','visual_prompt_engineer','comfyui_workflow_engineer','comfyui_node_developer','communications_operator','cashflow_treasury_analyst','people_operations_manager','copy_editor','typesetter','newsroom_editor']:
   self.assertIn(role,self.c['agents'])
 def test_producers_reused_not_copied(self):
  self.assertEqual(self.c['agents']['film_producer']['office'],'agency-office')
  self.assertIn('film_producer',self.c['offices']['production-office']['dependencies'])
 def test_project_managers_reused(self):
  self.assertIn('project_manager',agent_set(['delivery-office']))
  self.assertEqual(self.c['agents']['project_manager']['office'],'agency-office')
 def test_finance_native_dependency_selected(self):
  self.assertIn('pricing_margin_analyst',agent_set(['commercial-office']))
 def test_publication_dependencies_selected(self):
  self.assertIn('royalty_revenue_accountant',agent_set(['publishing-office']))
 def test_all_roles_have_compact_role_bootstrap(self):
  for k,a in self.c['agents'].items():
   self.assertIn('ACO ROLE BOOTSTRAP',(ROOT/a['path']).read_text(),k)
 def test_all_native_profiles_include_compact_role_bootstrap(self):
  for k,a in self.c['agents'].items():
   self.assertIn('ACO ROLE BOOTSTRAP',tomllib.loads((ROOT/a['codex_path']).read_text())['developer_instructions'],k)
 def test_unique_canonical_roles(self):
  keys=[]
  for p in (ROOT/'skills').glob('*/references/agents/*.md'):
   keys.append(re.search(r'\*\*Agent key:\*\* `([^`]+)`',p.read_text()).group(1))
  self.assertEqual(len(keys),len(set(keys)));self.assertEqual(set(keys),set(self.c['agents']))
 def test_workflow_references(self):
  w=read_json(ROOT/'skills/aco-office-concierge/references/WORKFLOWS.json')['workflows']
  self.assertEqual(len(w),61)
  for spec in w.values():
   for role in [spec['lead'],*spec['team']]:self.assertIn(role,self.c['agents'])
 def test_old_knowledge_kinds_preserved(self):
  from aco.memory import KINDS
  self.assertEqual(KINDS,{'organization','artist','career','activity','client','brand','project','matter'})
 def test_runtime_helpers_present(self):
  for name in ['planning.py','finance.py','production.py','harness.py']:
   self.assertTrue((ROOT/'skills/aco-office-concierge/runtime/scripts/aco'/name).exists())
