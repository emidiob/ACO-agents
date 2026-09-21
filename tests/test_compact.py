import copy,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError,Conflict,ROOT,digest,read_json
from aco.compact import CompactMemory,storage_decision,_part

class CompactTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.b=Path(self.tmp.name);self.m=CompactMemory(self.b/'knowledge',self.b/'state');self.m.init();self.org=self.add('organization','studio','Studio');self.w=self.b/'work';self.w.mkdir()
 def tearDown(self):self.tmp.cleanup()
 def add(self,kind,key,name,parent=None,**kw):return self.m.add_entity(kind,key,name,parent,commitment='existing_entity',approval_ref='user-test-approval',**kw)['entity']
 def files(self):return sorted(str(p.relative_to(self.m.root)) for p in self.m.root.rglob('*') if p.is_file())
 def doc(self,e=None):return (self.m.root/(e or self.org)['document']).read_text()
 def start(self,e=None,mode='LIGHT'):return self.m.start((e or self.org)['id'],'Test brief',self.w,mode)['session']
 def ev(self,key='e1',**kw):return dict(id=key,kind='work',state='executed',summary='Completed a test artifact',evidence=['synthetic-fixture'],**kw)
 def pipe(self,key='idea',kind='idea',**kw):return self.m.pipeline_upsert(self.org['id'],key,kind,'An unaccepted possibility',**kw)
 def test_new_owner_only_two_files(self):self.assertEqual(len(self.files()),2);self.assertFalse((self.m.root/'00-System').exists())
 def test_empty_init_only_index(self):
  m=CompactMemory(self.b/'empty',self.b/'state');m.init();self.assertEqual([x.name for x in m.root.iterdir()],['ACO-INDEX.md'])
 def test_repeat_init_preserves(self):
  before={p:(self.m.root/p).read_bytes() for p in self.files()};self.m.init();self.assertEqual(before,{p:(self.m.root/p).read_bytes() for p in self.files()})
 def test_pipeline_100_items_no_file_growth(self):
  before=self.files()
  for i in range(100):self.pipe('item-'+str(i),'application',status='submitted')
  self.assertEqual(before,self.files());self.assertEqual(len(self.m.registry()['entities']),1)
 def test_rejections_update_only_one_row(self):
  p=self.pipe();self.pipe(status='rejected');self.assertEqual(self.doc().count('| '+p['pipeline_id']+' |'),1);self.assertEqual(len(self.files()),2)
 def test_all_speculative_states_no_entities(self):
  for i,st in enumerate(['exploring','proposed','submitted','waiting','rejected','lost','parked','abandoned']):self.pipe('x'+str(i),'proposal',status=st)
  self.assertEqual(len(self.m.registry()['entities']),1)
 def test_no_commitment_rejected(self):
  with self.assertRaises(Conflict):self.m.add_entity('client','lead','Lead',self.org['id'])
 def test_no_reference_rejected(self):
  with self.assertRaises(Conflict):self.m.add_entity('client','lead','Lead',self.org['id'],commitment='explicit_user')
 def test_active_cannot_be_inferred(self):
  with self.assertRaises(Conflict):self.pipe(status='active')
 def test_activate_inline_no_folder(self):
  p=self.pipe();r=self.m.promote(self.org['id'],p['pipeline_id'],'explicit_user','approval');self.assertEqual(r['status'],'activated_inline');self.assertEqual(len(self.files()),2)
 def test_rejected_must_reopen(self):
  p=self.pipe(status='rejected')
  with self.assertRaises(Conflict):self.m.promote(self.org['id'],p['pipeline_id'],'explicit_user','approval')
 def test_materialize_needs_reason(self):
  p=self.pipe()
  with self.assertRaises(ACOError):self.m.promote(self.org['id'],p['pipeline_id'],'explicit_user','approval',materialize=True,key='p',name='P')
  self.assertNotIn('| active |',self.doc())
 def test_materialize_one_canonical(self):
  p=self.pipe();self.m.promote(self.org['id'],p['pipeline_id'],'explicit_user','approval',materialize=True,key='p',name='P',reason='Independent accepted work');self.assertEqual(len(self.files()),3)
 def test_small_active_client_is_section(self):
  e=self.add('client','c','Client',self.org['id']);self.assertEqual(e['storage'],'section');self.assertEqual(len(self.files()),2)
 def test_separate_client_boundary(self):
  e=self.add('client','c','Client',self.org['id'],separate=True,reason='Distinct sharing boundary');self.assertEqual(e['storage'],'document');self.assertEqual(len(self.files()),3)
 def test_duplicate_key_no_newfile(self):
  a=self.add('client','c','Client',self.org['id']);b=self.add('client','c','Client',self.org['id']);self.assertEqual(a['id'],b['id']);self.assertEqual(len(self.files()),2)
 def test_same_key_changed_name_conflict(self):
  self.add('client','c','Client',self.org['id'])
  with self.assertRaises(Conflict):self.add('client','c','Another',self.org['id'])
 def test_multi_company_same_client_distinct(self):
  other=self.add('organization','other','Other');a=self.add('client','c','Same',self.org['id']);b=self.add('client','c','Same',other['id']);self.assertNotEqual(a['id'],b['id'])
 def test_cross_owner_link_refused(self):
  other=self.add('organization','other','Other');c=self.add('client','c','C',other['id'])
  with self.assertRaises(Conflict):self.add('project','p','P',self.org['id'],links={'client_id':c['id']})
 def test_multi_activity_project_one_doc(self):
  a=self.add('activity','design','Design',self.org['id']);b=self.add('activity','print','Print',self.org['id']);p=self.add('project','p','P',self.org['id'],links={'activity_ids':[a['id'],b['id']]},separate=True,reason='Real project');self.assertEqual(len(self.files()),3);self.assertEqual(len(p['links']['activity_ids']),2)
 def test_wrong_brand_client(self):
  a=self.add('client','a','A',self.org['id']);b=self.add('client','b','B',self.org['id']);brand=self.add('brand','b','Brand',a['id'])
  with self.assertRaises(Conflict):self.add('project','p','P',self.org['id'],links={'client_id':b['id'],'brand_id':brand['id']})
 def test_one_handoff_no_knowledge_session_files(self):
  before=self.files();s=self.start();self.m.checkpoint(s['id'],self.ev());self.m.close(s['id']);self.assertEqual(self.files(),before);self.assertEqual([p.name for p in (self.w/'.agent-context').iterdir()],['HANDOFF.md'])
 def test_same_worktree_two_sessions_blocked(self):
  self.start()
  with self.assertRaises(Conflict):self.start()
 def test_closed_handoff_reused(self):
  s=self.start();self.m.close(s['id']);t=self.start();self.assertNotEqual(s['id'],t['id']);self.assertEqual(len(list((self.w/'.agent-context').iterdir())),1)
 def test_foreign_handoff_preserved(self):
  (self.w/'.agent-context').mkdir();p=self.w/'.agent-context/HANDOFF.md';p.write_text('user notes')
  with self.assertRaises(Conflict):self.start()
  self.assertEqual(p.read_text(),'user notes')
 def test_blind_no_export(self):
  s=self.start(mode='BLIND')
  with self.assertRaises(Conflict):self.m.export_context(s['id'],[self.org['id']])
 def test_no_cross_scope_export(self):
  c=self.add('client','c','C',self.org['id']);s=self.start(c)
  with self.assertRaises(Conflict):self.m.export_context(s['id'],[self.org['id']])
 def test_inline_export_only_section(self):
  c=self.add('client','c','C',self.org['id']);other=self.add('client','other','Secret other client',self.org['id']);s=self.start(c);self.m.export_context(s['id'],[c['id']]);self.assertNotIn('Secret other client',Path(s['handoff_path']).read_text())
 def test_same_event_no_duplicate(self):
  s=self.start();e=self.ev();self.m.checkpoint(s['id'],e);self.assertEqual(self.m.checkpoint(s['id'],e)['status'],'already_recorded');self.assertEqual(self.doc().count('- [e1]'),1)
 def test_changed_event_id_conflict(self):
  s=self.start();self.m.checkpoint(s['id'],self.ev());e=self.ev();e['summary']='different'
  with self.assertRaises(Conflict):self.m.checkpoint(s['id'],e)
 def test_proposed_decision_not_durable(self):
  s=self.start();before=self.doc();e=self.ev();e.update(kind='decision',state='proposed');self.assertEqual(self.m.checkpoint(s['id'],e)['status'],'local_handoff_only');self.assertEqual(self.doc(),before)
 def test_approved_decision_needs_authority(self):
  s=self.start();e=self.ev();e.update(kind='decision',state='approved')
  with self.assertRaises(Conflict):self.m.checkpoint(s['id'],e)
 def test_legacy_status_not_promoted_to_execution(self):
  s=self.start();e={'id':'old','kind':'decision','status':'proposed','summary':'just possible'};self.m.checkpoint(s['id'],e);self.assertNotIn('just possible',self.doc())
 def test_missing_state_refused(self):
  s=self.start();e={'id':'old','kind':'work','summary':'possible'}
  with self.assertRaises(ACOError):self.m.checkpoint(s['id'],e)
 def test_execution_needs_evidence(self):
  s=self.start();e=self.ev();e.pop('evidence')
  with self.assertRaises(Conflict):self.m.checkpoint(s['id'],e)
 def test_cap_does_not_truncate_or_archive(self):
  s=self.start()
  for i in range(20):self.m.checkpoint(s['id'],self.ev('item'+str(i)))
  before=self.doc();r=self.m.checkpoint(s['id'],self.ev('item21'));self.assertEqual(r['status'],'compaction_review_required');self.assertEqual(before,self.doc());self.assertEqual(len(self.files()),2)
 def test_compaction_preserves_decisions(self):
  s=self.start();e=self.ev();e.update(kind='decision',state='approved',approval_ref='user actual');self.m.checkpoint(s['id'],e);decision=_part(self.doc(),'decisions');self.m.compact_recent(self.org['id'],'Reviewed summary',digest(self.doc().encode()),'approval');self.assertEqual(_part(self.doc(),'decisions'),decision);self.assertEqual(len(self.files()),2)
 def test_stale_summary_refused(self):
  with self.assertRaises(Conflict):self.m.compact_recent(self.org['id'],'summary','old','approval')
 def test_proposal_no_file_and_stale_check(self):
  before=self.files();p=self.m.propose_context(self.org['id'],'New context',digest(self.doc().encode()),'Reason')['proposal'];self.assertEqual(before,self.files());self.pipe()
  with self.assertRaises(Conflict):self.m.apply_context(self.org['id'],p,'approval')
 def test_apply_context_preserves_pipeline(self):
  self.pipe();before=_part(self.doc(),'pipeline');p=self.m.propose_context(self.org['id'],'New context',digest(self.doc().encode()),'Reason')['proposal'];self.m.apply_context(self.org['id'],p,'approval');self.assertEqual(_part(self.doc(),'pipeline'),before)
 def test_recover_from_index_same_entities(self):
  m=CompactMemory(self.m.root,self.b/'other-state');m.init();self.assertEqual(set(m.registry()['entities']),set(self.m.registry()['entities']))
 def test_legacy_nonempty_refused(self):
  k=self.b/'old';k.mkdir();(k/'WORK-LOG.md').write_text('preserve')
  with self.assertRaises(Conflict):CompactMemory(k,self.b/'state').init()
 def test_state_inside_knowledge_refused(self):
  with self.assertRaises(ACOError):CompactMemory(self.m.root,self.m.root/'internal-state')
 def test_symlink_refused(self):
  link=self.b/'link';link.symlink_to(self.m.root)
  with self.assertRaises(ACOError):CompactMemory(link,self.b/'state')
 def test_stale_pipeline_refused(self):
  with self.assertRaises(Conflict):self.pipe(expected_sha256='bad')
 def test_runtime_cli_defaults_to_compact(self):
  env=dict(os.environ,ACO_HOME=str(self.b/'home'));root=self.b/'cli-root';r=subprocess.run([sys.executable,str(ROOT/'scripts/aco_cli.py'),'workspace-init','--knowledge',str(root)],env=env,text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['layout'],'compact');self.assertEqual([p.name for p in root.iterdir()],['ACO-INDEX.md'])
 def test_cli_drive_default_does_not_use_old_bridge(self):
  env=dict(os.environ,ACO_HOME=str(self.b/'home'));r=subprocess.run([sys.executable,str(ROOT/'scripts/aco_cli.py'),'drive-sync','--knowledge',str(self.m.root)],env=env,text=True,capture_output=True);self.assertNotEqual(r.returncode,0);self.assertIn('old per-event bridge is disabled',r.stderr)
 def test_all_work_domains_same_policy(self):
  for kind in ['idea','activity','lead','application','proposal','experiment','product','client']:
   with self.subTest(kind=kind):self.assertFalse(storage_decision({'kind':kind,'remember':True})['create_project'])
 def test_real_deliverable_allowed(self):self.assertEqual(storage_decision({'kind':'application','artifact_requested':True,'artifact_type':'application'})['action'],'deliverable_allowed')
 def test_restriction_overrides_file_reduction(self):self.assertEqual(storage_decision({'kind':'client','restricted':True})['action'],'restricted_boundary_review')
 def test_active_does_not_force_document(self):self.assertEqual(storage_decision({'kind':'project','commitment':'explicit_user','approval_ref':'user','independent':False})['action'],'inline_existing_document')

class AdoptionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.b=Path(self.tmp.name);self.root=self.b/'old';self.root.mkdir();self.p=self.root/'artist-context.md';self.original='# Original\n\nImportant approved material and speculative ideas.\n';self.p.write_text(self.original);(self.root/'old-log.md').write_text('preserve');self.m=CompactMemory(self.root,self.b/'local')
 def tearDown(self):self.tmp.cleanup()
 def adopt(self):return self.m.adopt('artist-context.md','artist','practice','Practice',digest(self.p.read_bytes()),'user review')
 def test_adopt_reuses_path(self):
  r=self.adopt();self.assertEqual(r['entity']['document'],'artist-context.md');self.assertIn(self.original.rstrip(),self.p.read_text());self.assertTrue((self.root/'old-log.md').exists());self.assertEqual(len(list(self.root.iterdir())),3)
 def test_double_adopt_refused(self):
  self.adopt()
  with self.assertRaises(Conflict):self.adopt()
 def test_stale_adoption(self):
  with self.assertRaises(Conflict):self.m.adopt('artist-context.md','artist','practice','Practice','stale','user review')
 def test_no_approval_no_changes(self):
  with self.assertRaises(Conflict):self.m.adopt('artist-context.md','artist','practice','Practice',digest(self.p.read_bytes()),'')
  self.assertEqual(self.p.read_text(),self.original)
 def test_adopt_does_not_infer_decisions(self):
  self.adopt();self.assertEqual(_part(self.p.read_text(),'decisions'),'');self.assertEqual(len(self.m.registry()['entities']),1)
 def test_unknown_index_preserved(self):
  idx=self.root/'ACO-INDEX.md';idx.write_text('Unknown old index')
  with self.assertRaises(Conflict):self.adopt()
  self.assertEqual(idx.read_text(),'Unknown old index')

class CompactedRetryTests(unittest.TestCase):
 def test_receipt_survives_summary_and_new_session(self):
  with tempfile.TemporaryDirectory() as t:
   b=Path(t);m=CompactMemory(b/'knowledge',b/'state');m.init();e=m.add_entity('artist','art','Art',commitment='existing_entity',approval_ref='u')['entity'];work=b/'work';work.mkdir();s=m.start(e['id'],'Work',work)['session'];entry={'id':'event-1','kind':'work','state':'executed','summary':'Completed','evidence':['fixture']};m.checkpoint(s['id'],entry);m.close(s['id']);doc=m.root/e['document'];m.compact_recent(e['id'],'Summary',digest(doc.read_bytes()),'u');s=m.start(e['id'],'More',work)['session'];before=doc.read_text();self.assertEqual(m.checkpoint(s['id'],entry)['status'],'already_recorded');self.assertEqual(doc.read_text(),before)
