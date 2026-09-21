"""Offline consistency checks, not artistic/market judgements or provider execution tests."""
import copy
import json
import sys
import unittest
from datetime import datetime, timezone, date
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError, ROOT
from aco.readiness import (capability_audit, practice_check, opportunity_check,
                          brand_check, social_check, social_packet_hash)
from aco.resources import resource_plan
NOW=datetime(2026,9,20,12,0,tzinfo=timezone.utc)

def practice():
 return dict(scope_id='artist-fixture',current_question='How does scale change the encounter?',available_hours_per_week=10,other_commitments_hours=2,protected_making_research_hours=4,review_date='2026-12-20',priorities=[dict(id='p1',title='Two scale studies',next_action='Make two maquettes',learning_signal='Compare encounter at the same viewing distance',category='making',hours_per_week=5)])
def opportunity():
 return dict(scope_id='artist-fixture',title='Synthetic residency',practice_need='Workshop access',official_source='https://example.org/call',source_evidence_ref='fixture-only',checked_on='2026-09-20',deadline_kind='fixed',deadline_at='2026-10-01T17:00:00+02:00',cost_support_summary='Synthetic covered costs; not a real offer',eligibility=[dict(criterion='Synthetic eligibility criterion',result='pass',evidence_ref='fixture-only')])
def brand():
 return dict(scope_id='org-fixture',brand_id='brand-fixture',objective='Explain a service clearly',audience='A defined synthetic audience',proposition='A working hypothesis',decision_status='proposed',claims=[dict(id='c1',text='Hypothesis, not evidence',support='assumed',evidence_refs=[])],applications=['Website opening','Proposal cover'],names=[])
def social(action='publish'):
 p=dict(scope_id='org-fixture',brand_id='brand-fixture',account_id='account-fixture',platform='synthetic-platform',version='1',action=action,posts=[dict(id='post1',text='Synthetic test copy. Not for publication.',media=[],claims=[],privacy_review_ref='fixture-review',accessibility_review_ref='fixture-review',disclosure_review_ref='fixture-review')])
 if action=='schedule':p.update(schedule_at='2026-09-22T14:00:00+02:00',timezone='Europe/Rome')
 return dict(packet=p,approval=dict(scope_id=p['scope_id'],account_id=p['account_id'],approval_ref='synthetic-not-auth',packet_sha256=social_packet_hash(p)),capability=dict(scope_id=p['scope_id'],account_id=p['account_id'],platform=p['platform'],status='verified_available',operations=[action],checked_at='2026-09-20T11:00:00+00:00',evidence_ref='simulated-not-connected'))
def reapprove(d):d['approval']['packet_sha256']=social_packet_hash(d['packet']);return d

class CapabilityAuditTests(unittest.TestCase):
 def test_presence_does_not_run_programs(self):
  with patch('subprocess.run',side_effect=AssertionError('Must not execute')):
   r=capability_audit(which=lambda name:'/fake/'+name if name=='ffmpeg' else None)
  f=next(x for x in r['commands'] if x['command']=='ffmpeg')
  self.assertTrue(f['found']);self.assertFalse(f['runnable_verified']);self.assertFalse(r['credentials_read']);self.assertEqual(r['remote_integrations'],'not_checked')
 def test_none_installed_is_not_failure(self):
  r=capability_audit(which=lambda _:None);self.assertTrue(all(not c['found'] for c in r['commands']));self.assertFalse(r['executed'])

class PracticeTests(unittest.TestCase):
 def test_feasible_input_is_review_not_quality_score(self):
  r=practice_check(practice());self.assertEqual(r['status'],'ready_for_review');self.assertEqual(r['artistic_quality'],'not_scored');self.assertEqual(r['knowledge_files_created'],0)
 def test_four_priorities_block(self):
  d=practice();d['priorities']=[dict(d['priorities'][0],id=str(i)) for i in range(4)];self.assertEqual(practice_check(d)['status'],'needs_review')
 def test_no_priorities_block(self):
  d=practice();d['priorities']=[];self.assertTrue(practice_check(d)['blockers'])
 def test_duplicate_priority(self):
  d=practice();d['priorities']*=2;self.assertTrue(any('IDs' in x for x in practice_check(d)['blockers']))
 def test_unknown_capacity(self):
  d=practice();del d['available_hours_per_week'];self.assertTrue(practice_check(d)['blockers'])
 def test_other_commitments_count(self):
  d=practice();d['other_commitments_hours']=7;self.assertTrue(any('exceed' in x for x in practice_check(d)['blockers']))
 def test_protected_time(self):
  d=practice();d['protected_making_research_hours']=7;self.assertTrue(any('protected' in x for x in practice_check(d)['blockers']))
 def test_operations_only_warning(self):
  d=practice();d['protected_making_research_hours']=0;d['priorities'][0]['category']='operations';self.assertTrue(practice_check(d)['warnings'])
 def test_negative_rejected(self):
  d=practice();d['priorities'][0]['hours_per_week']=-1
  with self.assertRaises(ACOError):practice_check(d)
 def test_nan_rejected(self):
  d=practice();d['available_hours_per_week']=float('nan')
  with self.assertRaises(ACOError):practice_check(d)
 def test_boolean_number_rejected(self):
  d=practice();d['available_hours_per_week']=True
  with self.assertRaises(ACOError):practice_check(d)
 def test_category_object_does_not_crash(self):
  d=practice();d['priorities'][0]['category']={};self.assertTrue(practice_check(d)['blockers'])
 def test_no_mutation(self):
  d=practice();old=copy.deepcopy(d);practice_check(d);self.assertEqual(d,old)

class OpportunityTests(unittest.TestCase):
 def test_valid_stays_pipeline(self):
  r=opportunity_check(opportunity(),NOW);self.assertEqual(r['recommendation'],'consider_with_artist');self.assertFalse(r['creates_project']);self.assertFalse(r['submission_authorized'])
 def test_fail_cannot_submit_as_eligible(self):
  d=opportunity();d['eligibility'][0]['result']='fail';self.assertEqual(opportunity_check(d,NOW)['recommendation'],'do_not_submit_as_eligible')
 def test_unknown_not_pass(self):
  d=opportunity();d['eligibility'][0]['result']='unknown';self.assertEqual(opportunity_check(d,NOW)['recommendation'],'investigate')
 def test_empty_eligibility(self):
  d=opportunity();d['eligibility']=[];self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_missing_eligibility_evidence(self):
  d=opportunity();del d['eligibility'][0]['evidence_ref'];self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_bad_enum(self):
  d=opportunity();d['eligibility'][0]['result']={}
  with self.assertRaises(ACOError):opportunity_check(d,NOW)
 def test_expired(self):
  d=opportunity();d['deadline_at']='2026-09-01T00:00:00+00:00';self.assertEqual(opportunity_check(d,NOW)['recommendation'],'do_not_submit_as_eligible')
 def test_timezone_required(self):
  d=opportunity();d['deadline_at']='2026-10-01T12:00:00'
  with self.assertRaises(ACOError):opportunity_check(d,NOW)
 def test_rolling_needs_evidence(self):
  d=opportunity();d['deadline_kind']='rolling';del d['deadline_at'];self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_rolling_with_evidence(self):
  d=opportunity();d['deadline_kind']='rolling';d['rolling_evidence_ref']='fixture';self.assertEqual(opportunity_check(d,NOW)['status'],'ready_for_review')
 def test_unknown_deadline_kind(self):
  d=opportunity();d['deadline_kind']='assumed';self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_stale_call(self):
  d=opportunity();d['checked_on']='2026-08-01';self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_future_call_review(self):
  d=opportunity();d['checked_on']='2026-10-01';self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_url_credentials_refused(self):
  d=opportunity();d['official_source']='https://user:fake@example.org/';self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_malformed_url_handled(self):
  d=opportunity();d['official_source']='https://[broken';self.assertTrue(opportunity_check(d,NOW)['blockers'])
 def test_nonobject(self):
  with self.assertRaises(ACOError):opportunity_check([],NOW)

class BrandTests(unittest.TestCase):
 def test_assumption_stays_warning_not_fact(self):
  r=brand_check(brand());self.assertEqual(r['status'],'ready_for_review');self.assertTrue(r['warnings']);self.assertFalse(r['trademark_clearance_verified'])
 def test_approved_not_validated(self):
  d=brand();d.update(decision_status='approved',approval_ref='user');r=brand_check(d);self.assertTrue(any('Assumed' in w for w in r['warnings']))
 def test_approval_ref_required(self):
  d=brand();d['decision_status']='approved';self.assertTrue(brand_check(d)['blockers'])
 def test_validation_ref_required(self):
  d=brand();d['claims'][0]['support']='validated';self.assertTrue(brand_check(d)['blockers'])
 def test_researched_ref_required(self):
  d=brand();d['claims'][0]['support']='researched';self.assertTrue(brand_check(d)['blockers'])
 def test_duplicate_claims(self):
  d=brand();d['claims']*=2;self.assertTrue(brand_check(d)['blockers'])
 def test_clearance_not_from_search(self):
  d=brand();d['names']=[dict(name='Candidate',clearance='cleared')]
  with self.assertRaises(ACOError):brand_check(d)
 def test_professional_review_needs_ref(self):
  d=brand();d['names']=[dict(name='Candidate',clearance='professional_review_recorded')];self.assertTrue(brand_check(d)['blockers'])
 def test_enum_object(self):
  d=brand();d['claims'][0]['support']={}
  with self.assertRaises(ACOError):brand_check(d)
 def test_no_mutation(self):
  d=brand();old=copy.deepcopy(d);brand_check(d);self.assertEqual(d,old)

class SocialTests(unittest.TestCase):
 def test_review_is_not_authorization_or_execution(self):
  r=social_check(social(),NOW);self.assertEqual(r['status'],'ready_for_review');self.assertFalse(r['publication_authorized']);self.assertFalse(r['provider_called']);self.assertFalse(r['executed'])
 def test_draft_no_connection_needed(self):
  d=social('draft');d.pop('approval');d.pop('capability');r=social_check(d,NOW);self.assertEqual(r['status'],'ready_for_review');self.assertTrue(r['warnings'])
 def test_account_mismatch(self):
  d=social();d['approval']['account_id']='different';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_scope_mismatch(self):
  d=social();d['capability']['scope_id']='other';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_platform_mismatch(self):
  d=social();d['capability']['platform']='other';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_changed_copy_requires_reapproval(self):
  d=social();d['packet']['posts'][0]['text']='Changed';self.assertTrue(any('hash' in x for x in social_check(d,NOW)['blockers']))
 def test_media_hash_binding(self):
  d=social();d['packet']['posts'][0]['media']=[dict(uri='local/reviewed.png',sha256='a'*64,rights_status='confirmed',rights_ref='fixture')];reapprove(d);d['packet']['posts'][0]['media'][0]['sha256']='b'*64;self.assertTrue(social_check(d,NOW)['blockers'])
 def test_media_missing_hash(self):
  d=social();d['packet']['posts'][0]['media']=[dict(uri='https://example.org/a.png',rights_status='confirmed',rights_ref='r')];self.assertTrue(any('SHA-256' in x for x in social_check(reapprove(d),NOW)['blockers']))
 def test_rights_required(self):
  d=social();d['packet']['posts'][0]['media']=[dict(uri='local/a.png',sha256='a'*64,rights_status='unknown')];self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_claim_evidence_required(self):
  d=social();d['packet']['posts'][0]['claims']=[dict(text='Unsupported')];self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_privacy_review_required(self):
  d=social();del d['packet']['posts'][0]['privacy_review_ref'];self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_denied_no_route(self):
  d=social();d['approval']['denied']=True;self.assertTrue(any('denied' in x for x in social_check(d,NOW)['blockers']))
 def test_expired_approval(self):
  d=social();d['approval']['expires_at']='2026-09-19T12:00:00+00:00';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_missing_approval(self):
  d=social();d.pop('approval');self.assertTrue(social_check(d,NOW)['blockers'])
 def test_missing_connection(self):
  d=social();d.pop('capability');self.assertTrue(social_check(d,NOW)['blockers'])
 def test_stale_capabilities(self):
  d=social();d['capability']['checked_at']='2026-09-18T10:00:00+00:00';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_future_capabilities(self):
  d=social();d['capability']['checked_at']='2026-10-18T10:00:00+00:00';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_registry_not_capability(self):
  d=social();d['capability']['status']='listed_in_registry';self.assertTrue(social_check(d,NOW)['blockers'])
 def test_wrong_operation(self):
  d=social();d['capability']['operations']=['read'];self.assertTrue(social_check(d,NOW)['blockers'])
 def test_accepted_not_retried(self):
  d=social();d['previous_receipt']=dict(packet_sha256=d['approval']['packet_sha256'],state='accepted');self.assertTrue(any('already' in x for x in social_check(d,NOW)['blockers']))
 def test_timeout_reconcile(self):
  d=social();d['previous_receipt']=dict(packet_sha256=d['approval']['packet_sha256'],state='timeout');self.assertTrue(any('reconcile' in x for x in social_check(d,NOW)['blockers']))
 def test_schedule_valid(self):self.assertEqual(social_check(social('schedule'),NOW)['status'],'ready_for_review')
 def test_schedule_zone_mismatch(self):
  d=social('schedule');d['packet']['timezone']='America/New_York';self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_schedule_naive_rejected(self):
  d=social('schedule');d['packet']['schedule_at']='2026-09-22T14:00:00'
  with self.assertRaises(ACOError):social_check(reapprove(d),NOW)
 def test_schedule_past(self):
  d=social('schedule');d['packet']['schedule_at']='2026-09-19T14:00:00+02:00';self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_schedule_bad_zone(self):
  d=social('schedule');d['packet']['timezone']='not-a-zone';self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_action_malformed(self):
  d=social();d['packet']['action']={}
  with self.assertRaises(ACOError):social_check(d,NOW)
 def test_nan_packet(self):
  d=social();d['packet']['invalid']=float('nan')
  with self.assertRaises(ACOError):social_check(d,NOW)
 def test_duplicate_posts(self):
  d=social();d['packet']['posts']*=2;self.assertTrue(social_check(reapprove(d),NOW)['blockers'])
 def test_hash_order_independent(self):self.assertEqual(social_packet_hash({'a':1,'b':2}),social_packet_hash({'b':2,'a':1}))
 def test_no_mutation(self):
  d=social();old=copy.deepcopy(d);social_check(d,NOW);self.assertEqual(old,d)
 def test_evidence_is_caller_supplied_not_trusted(self):
  r=social_check(social(),NOW);self.assertIn('authenticity',r['limitation']);self.assertFalse(r['publication_authorized'])

class ConsolidationTests(unittest.TestCase):
 def test_targeted_original_methods(self):
  m=json.loads((ROOT/'docs/CURATED-METHODS.json').read_text());self.assertEqual(len(m['playbooks']),19)
  roles=set()
  for key,p in m['playbooks'].items():
   self.assertTrue((ROOT/f'skills/aco-office-concierge/references/playbooks/{key}.md').exists());roles.update(p['roles'])
  self.assertEqual(len(roles),114)
 def test_no_persona_inflation(self):
  c=json.loads((ROOT/'catalog.json').read_text());self.assertEqual(len(c['agents']),363);self.assertEqual(len(c['skills']),16)
 def test_reference_only_cannot_be_embedded_by_plan(self):
  q=dict(resource_id='spectrum',action='install',purpose='archive',data_scope='none',approval_ref='u',license_review_ref='not-a-licence')
  inv=dict(checked_on='2026-09-20',evidence_ref='fixture',capabilities=[])
  r=resource_plan(q,inv,date(2026,9,20));self.assertEqual(r['status'],'blocked');self.assertTrue(any('consultation only' in x for x in r['blockers']))
 def test_reference_consult_remains_possible(self):
  q=dict(resource_id='spectrum',action='consult',purpose='read authorized reference',data_scope='public');self.assertEqual(resource_plan(q)['status'],'ready_for_host_review')
 def test_no_automatic_persistence_in_new_recipes(self):
  w=json.loads((ROOT/'skills/aco-office-concierge/references/WORKFLOWS.json').read_text())['workflows']
  keys=['artist-development-review','peer-critique-session','residency-fit','social-editorial-cycle','brand-positioning']
  for k in keys:self.assertEqual(w[k]['storage'],'existing_canonical_section_by_default');self.assertNotIn('schedule_enabled',w[k])
class NativeMethodResolutionTests(unittest.TestCase):
 def test_all_native_links_use_existing_skill_paths(self):
  import re,tomllib
  cat=json.loads((ROOT/'catalog.json').read_text())
  seen=0
  for role in cat['agents'].values():
   text=tomllib.loads((ROOT/role['codex_path']).read_text())['developer_instructions']
   self.assertIn('NATIVE PROFILE REFERENCE RESOLUTION',text)
   self.assertIn('not to this TOML',text)
   for dest in re.findall(r'\]\(([^\s)]+)\)',text):
    if dest.startswith('aco-'):
     self.assertTrue((ROOT/'skills'/dest.split('#')[0]).exists(),dest);seen+=1
    self.assertFalse(dest.startswith('../../../aco-'),dest)
  self.assertGreater(seen,363)
 def test_artist_profile_points_to_shared_method(self):
  import tomllib
  text=tomllib.loads((ROOT/'extras/codex-custom-agents/artist-office/aco-practice-strategist.toml').read_text())['developer_instructions']
  self.assertIn('(aco-office-concierge/references/playbooks/ARTISTIC-DEVELOPMENT.md)',text)

if __name__=='__main__':unittest.main()
