import json,sys,unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.resources import load_registry,resource_plan,search_resources
from aco.common import ROOT,ACOError
class ResourceTests(unittest.TestCase):
 def test_all_97_distinct(self):
  r=load_registry()['resources'];self.assertEqual(len(r),97);self.assertEqual(len({e['id'] for e in r}),97)
 def test_every_role_exists(self):
  roles=json.loads((ROOT/'catalog.json').read_text())['agents']
  for e in load_registry()['resources']:
   for r in e['roles']:self.assertIn(r,roles)
 def test_unresolved_exactly_three(self):self.assertEqual({e['id'] for e in load_registry()['resources'] if e['review_status']=='identity_unresolved'},{'image-23-js','shepherd','open-higgsfield'})
 def test_no_claim_installed_or_tested(self):
  for e in load_registry()['resources']:self.assertFalse(e['installed_by_aco']);self.assertFalse(e['execution_tested']);self.assertFalse(e['license']['aco_bundles_upstream'])
 def test_source_review_not_license_clearance(self):
  for e in load_registry()['resources']:self.assertEqual(e['license']['status'],'check_current_terms_before_reuse')
 def test_empty_query_no_install_list(self):self.assertEqual(search_resources()['resources'],[])
 def test_role_filter_relevance(self):self.assertIn('comfyui-continuity',{e['id'] for e in search_resources(role='comfyui_workflow_engineer')['resources']})
 def test_no_unresolved_default(self):self.assertEqual(search_resources('shepherd')['resources'],[])
 def test_unresolved_inspectable(self):self.assertEqual(search_resources('shepherd',include_unresolved=True)['resources'][0]['id'],'shepherd')
 def test_default_shortlist_three(self):self.assertLessEqual(len(search_resources('design motion reference')['resources']),3)
 def test_unknown_resource(self):
  with self.assertRaises(ACOError):resource_plan({'resource_id':'imagined'})
 def test_unresolved_blocks_activation(self):
  for r in ['image-23-js','shepherd','open-higgsfield']:self.assertEqual(resource_plan({'resource_id':r,'action':'install'})['status'],'needs_exact_source')
 def test_consult_public_plan_not_execution(self):
  r=resource_plan({'resource_id':'taste','purpose':'Design critique','action':'consult','data_scope':'public'});self.assertEqual(r['status'],'ready_for_host_review');self.assertFalse(r['executed'])
 def test_denied_no_alternate(self):self.assertEqual(resource_plan({'resource_id':'agent-reach','denied':True})['status'],'denied')
 def test_missing_inventory_blocks(self):self.assertEqual(resource_plan({'resource_id':'lenis','purpose':'Scroll treatment','action':'install','approval_ref':'u','license_review_ref':'l','data_scope':'none'})['status'],'blocked')
 def test_fresh_inventory_required(self):
  q={'resource_id':'lenis','purpose':'Scroll treatment','action':'install','approval_ref':'u','license_review_ref':'l','data_scope':'none'};inv={'checked_on':'2026-01-01','evidence_ref':'local help','capabilities':['local_package_review']};self.assertEqual(resource_plan(q,inv,date(2026,9,20))['status'],'blocked')
 def test_ready_install_still_not_executed(self):
  q={'resource_id':'lenis','purpose':'Scroll treatment','action':'install','approval_ref':'u','license_review_ref':'l','data_scope':'none'};inv={'checked_on':'2026-09-20','evidence_ref':'observed host','capabilities':['local_package_review']};r=resource_plan(q,inv,date(2026,9,20));self.assertEqual(r['status'],'ready_for_host_review');self.assertFalse(r['installed'])
 def test_private_hosted_needs_approval(self):self.assertEqual(resource_plan({'resource_id':'gitingest','purpose':'repo scan','data_scope':'private','external_transfer':True})['status'],'blocked')
 def test_explicit_private_transfer(self):self.assertEqual(resource_plan({'resource_id':'gitingest','purpose':'repo scan','data_scope':'private','external_transfer':True,'data_transfer_approval_ref':'u1'})['status'],'ready_for_host_review')
 def test_secrets_never_sent(self):self.assertEqual(resource_plan({'resource_id':'deepwiki','purpose':'scan','data_scope':'public','contains_secrets':True})['status'],'blocked')
 def test_no_data_class_inferred(self):self.assertEqual(resource_plan({'resource_id':'deepwiki','purpose':'scan'})['status'],'blocked')
 def test_no_cost_approval_from_license(self):
  q={'resource_id':'lenis','purpose':'prototype','action':'use','approval_ref':'u','license_review_ref':'l','paid':True,'data_scope':'none'};inv={'checked_on':'2026-09-20','evidence_ref':'observed','capabilities':['local_package_review']};self.assertTrue(any('cost' in s for s in resource_plan(q,inv,date(2026,9,20))['blockers']))
 def test_all_methods_exist(self):
  root=ROOT/'skills/aco-office-concierge/references/resources'
  for e in load_registry()['resources']:self.assertTrue((root/e['method']).exists())
 def test_all_skills_have_compact_gate(self):
  for p in (ROOT/'skills').glob('*/SKILL.md'):self.assertIn('COMPACT-MEMORY.md',p.read_text())
 def test_all_roles_have_compact_gate(self):
  for p in (ROOT/'skills').glob('*/references/agents/*.md'):self.assertIn('COMPACT-MEMORY.md',p.read_text())
 def test_scheduled_recipes_are_disabled(self):
  w=json.loads((ROOT/'skills/aco-office-concierge/references/WORKFLOWS.json').read_text())['workflows'];rs=[x for x in w.values() if 'schedule_enabled' in x];self.assertEqual(len(rs),8)
  for e in rs:self.assertFalse(e['schedule_enabled'])


 def test_v052_intake_present(self):
  ids={e['id'] for e in load_registry()['resources']}
  expected={'javascript-algorithms','thirty-seconds-code','public-apis','langflow','open-seo','i-have-adhd','no-ai-slop','open-notebook','uptime-kuma','excalidraw','vaultwarden','changedetection-io','localsend','gallery-dl','reactive-resume','searxng','cobalt','dify','crawl4ai','browser-use','maxun','openhands'}
  self.assertTrue(expected<=ids)
 def test_v052_skills_route_to_original_methods(self):
  byid={e['id']:e for e in load_registry()['resources']}
  self.assertTrue(byid['i-have-adhd']['method'].endswith('ACTION-FIRST-COMMUNICATION.md'))
  self.assertTrue(byid['no-ai-slop']['method'].endswith('HUMAN-WRITING-REVIEW.md'))
  self.assertTrue(byid['open-seo']['method'].endswith('SEO-OPERATIONS.md'))
 def test_external_resources_not_bundled(self):
  for rid in ['vaultwarden','dify','crawl4ai','browser-use','maxun','openhands','gallery-dl','cobalt']:
   e=next(x for x in load_registry()['resources'] if x['id']==rid)
   self.assertFalse(e['installed_by_aco']); self.assertFalse(e['license']['aco_bundles_upstream'])

class AdditionalResourceGuards(unittest.TestCase):
 def test_private_route_must_be_explicit(self):self.assertEqual(resource_plan({'resource_id':'deepwiki','purpose':'scan','data_scope':'private'})['status'],'blocked')
 def test_partial_source_execution_needs_verification(self):
  q={'resource_id':'shapes-gallery','purpose':'Use reviewed shape','action':'use','data_scope':'public','approval_ref':'u','license_review_ref':'l'}
  r=resource_plan(q,{'checked_on':'2026-09-20','evidence_ref':'host','capabilities':[]},date(2026,9,20));self.assertTrue(any('partially reviewed' in s for s in r['blockers']))
