import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.tidy import inventory,consolidation_plan,apply_plan,restore
from aco.canonical_sync import plan_update,apply_update
from aco.common import ACOError,Conflict,digest
class TidyTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.b=Path(self.tmp.name);self.root=self.b/'knowledge';self.root.mkdir();self.src=self.root/'WORK-LOG.md';self.src.write_text('Approved decision and useful notes');self.spec={'scope_id':'private-owner-test','sources':[{'path':'WORK-LOG.md','sha256':digest(self.src.read_bytes()),'scope_id':'private-owner-test','reviewed_as_aco_note':True}],'target':'ACO.md','target_sha256':None,'merged_text':'# Canonical\nApproved decision and useful notes\n','quarantine_sources':True}
 def tearDown(self):self.tmp.cleanup()
 def plan(self):return consolidation_plan(self.root,self.spec)['plan']
 def apply(self,p=None):
  p=p or self.plan();return apply_plan(self.root,p,self.b/'recovery','user-test',p['plan_id'])
 def test_inventory_no_mutation(self):
  before=list(self.root.iterdir());r=inventory(self.root);self.assertFalse(r['modified']);self.assertEqual(before,list(self.root.iterdir()))
 def test_duplicate_not_delete_approval(self):
  (self.root/'another.md').write_bytes(self.src.read_bytes());r=inventory(self.root);self.assertEqual(len(r['byte_duplicate_groups']),1);self.assertEqual(len(list(self.root.iterdir())),2)
 def test_actual_deliverable_preserved(self):
  (self.root/'contract.txt').write_text('original');r=inventory(self.root);self.assertEqual(next(x for x in r['files'] if x['path']=='contract.txt')['classification'],'preserve_deliverable_or_restricted')
 def test_plan_only(self):
  p=self.plan();self.assertFalse((self.root/'ACO.md').exists());self.assertTrue(self.src.exists());self.assertEqual(p['scope_id'],'private-owner-test')
 def test_apply_quarantine_not_delete(self):
  r=self.apply();self.assertEqual(r['permanently_deleted_files'],0);self.assertFalse(self.src.exists());self.assertTrue((self.root/'ACO.md').exists());self.assertEqual(len(list(self.root.rglob('*'))),1);self.assertTrue(Path(r['backup']).exists())
 def test_keep_originals_by_default(self):
  self.spec.pop('quarantine_sources');self.apply();self.assertTrue(self.src.exists())
 def test_restore_sources_keeps_canonical(self):
  r=self.apply();restore(Path(r['receipt']),'approved restore');self.assertTrue(self.src.exists());self.assertTrue((self.root/'ACO.md').exists())
 def test_restore_will_not_overwrite_newer_source(self):
  r=self.apply();self.src.write_text('later edit')
  with self.assertRaises(Conflict):restore(Path(r['receipt']),'restore')
 def test_plan_hash_changed_refused(self):
  p=self.plan();p['merged_text']='changed'
  with self.assertRaises(Conflict):self.apply(p)
 def test_source_revision_changed_refused(self):
  p=self.plan();self.src.write_text('new')
  with self.assertRaises(Conflict):self.apply(p)
  self.assertFalse((self.root/'ACO.md').exists())
 def test_existing_target_revision_required(self):
  (self.root/'ACO.md').write_text('existing')
  with self.assertRaises(Conflict):self.plan()
 def test_target_changed_after_plan(self):
  p=self.plan();(self.root/'ACO.md').write_text('concurrent')
  with self.assertRaises(Conflict):self.apply(p)
 def test_cross_scope_rejected(self):
  self.spec['sources'][0]['scope_id']='other'
  with self.assertRaises(Conflict):self.plan()
 def test_review_classification_required(self):
  self.spec['sources'][0].pop('reviewed_as_aco_note')
  with self.assertRaises(Conflict):self.plan()
 def test_protected_record_rejected(self):
  self.spec['sources'][0]['protected']=True
  with self.assertRaises(Conflict):self.plan()
 def test_traversal_rejected(self):
  self.spec['target']='../ACO.md'
  with self.assertRaises(ACOError):self.plan()
 def test_symlink_source_rejected(self):
  link=self.root/'link.md';link.symlink_to(self.src);self.spec['sources'][0]['path']='link.md'
  with self.assertRaises(ACOError):self.plan()
 def test_recovery_not_in_knowledge(self):
  p=self.plan()
  with self.assertRaises(ACOError):apply_plan(self.root,p,self.root/'backup','u',p['plan_id'])
 def test_approval_bound_to_plan(self):
  p=self.plan()
  with self.assertRaises(Conflict):apply_plan(self.root,p,self.b/'recovery','u','wrong-plan')
 def test_empty_folders_exact(self):
  (self.root/'Empty').mkdir();self.spec['remove_empty_folders']=['Empty'];r=self.apply();self.assertEqual(r['empty_folders_removed'],1)
 def test_nonempty_folder_not_removed(self):
  self.spec['remove_empty_folders']=['.']
  with self.assertRaises((Conflict,ACOError)):self.plan()
 def test_folder_changed_after_plan(self):
  (self.root/'Empty').mkdir();self.spec['remove_empty_folders']=['Empty'];p=self.plan();(self.root/'Empty/new.txt').write_text('preserve')
  with self.assertRaises(Conflict):self.apply(p)
  self.assertTrue((self.root/'Empty/new.txt').exists())
 def test_apply_idempotent(self):
  p=self.plan();self.apply(p);self.assertEqual(self.apply(p)['status'],'already_applied')
 def test_existing_target_backup_restore(self):
  t=self.root/'ACO.md';t.write_text('Before');self.spec['target_sha256']=digest(t.read_bytes());r=self.apply();restore(Path(r['receipt']),'restore',True);self.assertEqual(t.read_text(),'Before')
 def test_rejected_folder_no_automatic_action(self):
  p=self.root/'Rejected';p.mkdir();(p/'idea.md').write_text('important idea');r=inventory(self.root);self.assertTrue((p/'idea.md').exists());self.assertEqual(next(x for x in r['files'] if x['path']=='Rejected/idea.md')['classification'],'unclassified_preserve')

class MockProvider:
 supports_revision_guard=True
 def __init__(self):self.doc={'document_id':'fixture-doc','scope_id':'test-owner','revision':'1','text':'Original'};self.writes=0;self.race=False
 def read_document(self,id):return copy.deepcopy(self.doc)
 def replace_document(self,id,text,expected_revision):
  if self.race:self.doc['revision']='2'
  if self.doc['revision']!=expected_revision:raise Conflict('Provider compare-and-swap refused')
  self.writes+=1;self.doc.update(text=text,revision='2')
class CanonicalSyncTests(unittest.TestCase):
 def setUp(self):self.p=MockProvider();self.plan=plan_update(self.p.read_document('fixture-doc'),'Revised','test-owner','user permission')
 def test_same_doc_verified(self):
  r=apply_update(self.plan,self.p);self.assertEqual(r['status'],'verified_remote');self.assertEqual(r['new_files'],0);self.assertEqual(self.p.writes,1)
 def test_idempotent_after_lost_response(self):apply_update(self.plan,self.p);self.assertEqual(apply_update(self.plan,self.p)['status'],'already_verified_remote');self.assertEqual(self.p.writes,1)
 def test_no_guard_refused(self):
  self.p.supports_revision_guard=False
  with self.assertRaises(Conflict):apply_update(self.plan,self.p)
 def test_new_revision_refused(self):
  self.p.doc['revision']='other'
  with self.assertRaises(Conflict):apply_update(self.plan,self.p)
 def test_mid_write_race_refused(self):
  self.p.race=True
  with self.assertRaises(Conflict):apply_update(self.plan,self.p)
  self.assertEqual(self.p.writes,0)
 def test_wrong_scope_refused(self):
  self.p.doc['scope_id']='another'
  with self.assertRaises(Conflict):apply_update(self.plan,self.p)
 def test_changed_plan_refused(self):
  self.plan['new_text']='surprise'
  with self.assertRaises(Conflict):apply_update(self.plan,self.p)
 def test_new_document_not_invented(self):
  s=self.p.read_document('fixture-doc');s.pop('document_id')
  with self.assertRaises(ACOError):plan_update(s,'new','test-owner','u')
 def test_empty_output_refused(self):
  with self.assertRaises(Conflict):plan_update(self.p.doc,'','test-owner','u')

class EmptyAfterMergeTests(unittest.TestCase):
 def test_approved_ancestors_removed_only_after_moving_sources(self):
  with tempfile.TemporaryDirectory() as t:
   b=Path(t);root=b/'knowledge';d=root/'History/Notes';d.mkdir(parents=True);p=d/'WORK-LOG.md';p.write_text('Reviewed notes')
   spec={'scope_id':'s','sources':[{'path':'History/Notes/WORK-LOG.md','sha256':digest(p.read_bytes()),'scope_id':'s','reviewed_as_aco_note':True}],'target':'ACO.md','target_sha256':None,'merged_text':'Reviewed notes','quarantine_sources':True,'remove_empty_folders':['History/Notes','History']}
   plan=consolidation_plan(root,spec)['plan'];r=apply_plan(root,plan,b/'recovery','u',plan['plan_id']);self.assertEqual(r['empty_folders_removed'],2);self.assertFalse((root/'History').exists());restore(Path(r['receipt']),'restore');self.assertEqual(p.read_text(),'Reviewed notes')
 def test_unapproved_sibling_blocks_folder_removal(self):
  with tempfile.TemporaryDirectory() as t:
   b=Path(t);root=b/'knowledge';d=root/'History';d.mkdir(parents=True);p=d/'WORK-LOG.md';p.write_text('notes');(d/'other.md').write_text('preserve')
   spec={'scope_id':'s','sources':[{'path':'History/WORK-LOG.md','sha256':digest(p.read_bytes()),'scope_id':'s','reviewed_as_aco_note':True}],'target':'ACO.md','target_sha256':None,'merged_text':'notes','quarantine_sources':True,'remove_empty_folders':['History']}
   with self.assertRaises(Conflict):consolidation_plan(root,spec)
