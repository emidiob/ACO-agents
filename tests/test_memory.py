import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aco.common import ACOError, Conflict, digest, read_json, write_json, lock
from aco.memory import Memory

class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        self.m=Memory(self.base/'knowledge');self.m.init()
        self.workspace=self.base/'project';self.workspace.mkdir()
        self.org=self.m.add_entity('organization','studio','Studio')['entity']
    def tearDown(self):self.tmp.cleanup()
    def start(self, entity=None, mode='LIGHT'):
        return self.m.start((entity or self.org)['id'],'A bounded task',self.workspace,mode)['session']
    def event(self, **kw):
        e={'id':'event-test','kind':'work','status':'proposed','summary':'A draft'};e.update(kw);return e
    def test_repeat_init_preserves_context(self):
        p=self.m.root/self.org['path']/'Context.md';p.write_text('User text')
        self.m.init();self.assertEqual(p.read_text(),'User text')
    def test_repeat_entity_is_idempotent(self):
        result=self.m.add_entity('organization','studio','Studio')
        self.assertEqual(result['entity']['id'],self.org['id']);self.assertEqual(result['status'],'existing')
    def test_same_key_different_content_conflict(self):
        with self.assertRaises(Conflict):self.m.add_entity('organization','studio','Another name')
    def test_nonempty_foreign_root_refused(self):
        r=self.base/'foreign';r.mkdir();(r/'user.txt').write_text('preserve')
        with self.assertRaises(Conflict):Memory(r).init()
    def test_knowledge_in_git_refused(self):
        r=self.base/'gitrepo';r.mkdir();(r/'.git').mkdir()
        with self.assertRaises(ACOError):Memory(r/'knowledge').init()
    def test_authority_not_silently_switched(self):
        with self.assertRaises(Conflict):self.m.init('drive')
    def test_two_org_same_client_label_distinct(self):
        org2=self.m.add_entity('organization','other','Other')['entity']
        a=self.m.add_entity('client','north','North',self.org['id'])['entity']
        b=self.m.add_entity('client','north','North',org2['id'])['entity']
        self.assertNotEqual(a['id'],b['id'])
    def test_same_org_same_label_explicit_keys(self):
        a=self.m.add_entity('client','north-uk','North',self.org['id'])['entity']
        b=self.m.add_entity('client','north-fr','North',self.org['id'])['entity']
        self.assertNotEqual(a['id'],b['id'])
    def test_invalid_parent(self):
        with self.assertRaises(ACOError):self.m.add_entity('client','a','A')
    def test_unknown_parent(self):
        with self.assertRaises(ACOError):self.m.add_entity('project','p','P','unknown')
    def test_traversal_key(self):
        with self.assertRaises(ACOError):self.m.add_entity('organization','../escape','Bad')
    def test_activity_project_links(self):
        a=self.m.add_entity('activity','design','Design',self.org['id'])['entity']
        b=self.m.add_entity('activity','publishing','Publishing',self.org['id'])['entity']
        p=self.m.add_entity('project','book','Book',self.org['id'],{'activity_ids':[a['id'],b['id']]})['entity']
        s=self.start(p);self.assertEqual(len(s['scope']['activity_ids']),2)
    def test_cross_org_client_rejected(self):
        other=self.m.add_entity('organization','other','Other')['entity']
        c=self.m.add_entity('client','c','C',other['id'])['entity']
        with self.assertRaises(Conflict):self.m.add_entity('project','p','P',self.org['id'],{'client_id':c['id']})
    def test_wrong_brand_client_rejected(self):
        a=self.m.add_entity('client','a','A',self.org['id'])['entity']
        b=self.m.add_entity('client','b','B',self.org['id'])['entity']
        brand=self.m.add_entity('brand','brand','Brand',a['id'])['entity']
        with self.assertRaises(Conflict):self.m.add_entity('project','p','P',self.org['id'],{'client_id':b['id'],'brand_id':brand['id']})
    def test_project_scope_cannot_override_client(self):
        a=self.m.add_entity('client','a','A',self.org['id'])['entity']
        b=self.m.add_entity('client','b','B',self.org['id'])['entity']
        p=self.m.add_entity('project','p','P',self.org['id'],{'client_id':a['id']})['entity']
        with self.assertRaises(Conflict):self.m.start(p['id'],'Work',self.workspace,relationships={'client_id':b['id']})
    def test_session_ids_distinct_and_no_global_client(self):
        a,b=self.start(),self.start();self.assertNotEqual(a['id'],b['id'])
        self.assertTrue(Path(a['handoff_dir']).is_dir());self.assertTrue(Path(b['handoff_dir']).is_dir())
        self.assertFalse((self.workspace/'.agent-context/SESSION.json').exists())
    def test_gitignore_preserves_existing(self):
        p=self.workspace/'.gitignore';p.write_text('custom/\n')
        self.start();self.start();t=p.read_text()
        self.assertTrue(t.startswith('custom/'));self.assertEqual(t.count('.agent-context/'),1)
    def test_blind_does_not_export_context(self):
        for mode in ('BLIND','NONE','BLIND-FIRST'):
            s=self.start(mode=mode)
            with self.assertRaises(Conflict):self.m.export_context(s['id'],[self.org['id']])
    def test_scope_blocks_unrelated_same_org_client_context(self):
        c=self.m.add_entity('client','c','C',self.org['id'])['entity'];s=self.start()
        with self.assertRaises(Conflict):self.m.export_context(s['id'],[c['id']])
    def test_scoped_export_records_hash(self):
        s=self.start();r=self.m.export_context(s['id'],[self.org['id']])
        self.assertEqual(len(r['sources']),1);self.assertEqual(len(r['sources'][0]['sha256']),64)
    def test_duplicate_checkpoint_one_event(self):
        s=self.start();self.m.checkpoint(s['id'],self.event());self.m.checkpoint(s['id'],self.event())
        self.assertEqual(len(self.m.events(self.org)),1)
    def test_event_id_different_payload_conflict(self):
        s=self.start();self.m.checkpoint(s['id'],self.event())
        with self.assertRaises(Conflict):self.m.checkpoint(s['id'],self.event(summary='Changed'))
    def test_event_id_different_session_conflict(self):
        a,b=self.start(),self.start();self.m.checkpoint(a['id'],self.event())
        with self.assertRaises(Conflict):self.m.checkpoint(b['id'],self.event())
    def test_approved_decision_requires_approval(self):
        s=self.start()
        with self.assertRaises(ACOError):self.m.checkpoint(s['id'],self.event(kind='decision',status='approved'))
    def test_verified_requires_evidence(self):
        s=self.start()
        with self.assertRaises(ACOError):self.m.checkpoint(s['id'],self.event(status='verified'))
    def test_open_loop_requires_stable_id(self):
        s=self.start()
        with self.assertRaises(ACOError):self.m.checkpoint(s['id'],self.event(kind='open_loop',status='open'))
    def test_checkpoint_is_pending_not_drive_saved(self):
        s=self.start();r=self.m.checkpoint(s['id'],self.event())
        self.assertEqual(r['drive_status'],'pending');self.assertIn('event-test',self.m.status()['pending_drive_events'])
    def test_close_writes_handoff(self):
        s=self.start();self.m.checkpoint(s['id'],self.event(next_action='Review'))
        r=self.m.close(s['id']);self.assertTrue(Path(r['handoff']).is_file())
        self.assertEqual(self.m.close(s['id'])['status'],'closed')
    def test_closed_session_rejects_checkpoint(self):
        s=self.start();self.m.close(s['id'])
        with self.assertRaises(Conflict):self.m.checkpoint(s['id'],self.event())
    def test_context_proposal_not_applied(self):
        p=self.m.root/self.org['path']/'Context.md';old=p.read_bytes()
        self.m.propose_context(self.org['id'],'New',digest(old),'User requested revision')
        self.assertEqual(p.read_bytes(),old)
    def test_context_apply_verifies_and_audits(self):
        p=self.m.root/self.org['path']/'Context.md';old=p.read_bytes()
        proposal=self.m.propose_context(self.org['id'],'New',digest(old),'Approved revision')
        r=self.m.apply_context(self.org['id'],proposal['id'],'user-message-1')
        self.assertEqual(p.read_text(),'New');self.assertEqual(r['sha256'],digest(b'New'))
        self.assertEqual(self.m.events(self.org)[0]['kind'],'context_change')
        self.m.apply_context(self.org['id'],proposal['id'],'user-message-1')
        self.assertEqual(len(self.m.events(self.org)),1)
    def test_stale_context_proposal_rejected(self):
        p=self.m.root/self.org['path']/'Context.md';proposal=self.m.propose_context(self.org['id'],'New',digest(p.read_bytes()),'Reason')
        p.write_text('Concurrent change')
        with self.assertRaises(Conflict):self.m.apply_context(self.org['id'],proposal['id'],'user-message')
        self.assertEqual(p.read_text(),'Concurrent change')
    def test_drive_authority_blocks_local_context_apply(self):
        r=self.m.registry();r['authority']='drive';write_json(self.m.registry_path,r)
        p=self.m.root/self.org['path']/'Context.md';proposal=self.m.propose_context(self.org['id'],'New',digest(p.read_bytes()),'Reason')
        with self.assertRaises(Conflict):self.m.apply_context(self.org['id'],proposal['id'],'user-message')
    def test_entity_journal_recovers_interrupted_registry_save(self):
        r=self.m.registry();r['entities']={};write_json(self.m.registry_path,r)
        self.m.init();self.assertIn(self.org['id'],self.m.registry()['entities'])
    def test_symlink_destination_refused(self):
        outside=self.base/'outside';outside.mkdir()
        root=self.base/'link';root.symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ACOError):Memory(root)
    def test_lock_contention_fails_safely(self):
        with self.m._lock():
            with self.assertRaises(Conflict):self.m.add_entity('organization','other','Other')


class AdditionalMemoryTests(MemoryTests):
    # Test discovery for inherited methods is intentional: inherited tests run on the
    # same implementation, but do not inflate counts. Suppress inherited discovery
    # below and keep this class only for the additional cases.
    def test_git_tracked_handoff_refused(self):
        import subprocess
        subprocess.run(['git','init','-q',str(self.workspace)],check=True)
        p=self.workspace/'.agent-context';p.mkdir();(p/'old.md').write_text('not private fixture')
        subprocess.run(['git','-C',str(self.workspace),'add','.agent-context/old.md'],check=True)
        with self.assertRaises(Conflict):self.start()
        self.assertFalse((p/'sessions').exists())
    def test_symlink_context_export_refused(self):
        p=self.m.root/self.org['path']/'Context.md';p.unlink()
        outside=self.base/'external.txt';outside.write_text('Do not copy')
        p.symlink_to(outside)
        s=self.start()
        with self.assertRaises(ACOError):self.m.export_context(s['id'],[self.org['id']])
    def test_supersedes_must_exist(self):
        s=self.start()
        with self.assertRaises(Conflict):self.m.checkpoint(s['id'],self.event(supersedes='event-not-present'))
    def test_closed_loop_disappears_from_open_view_but_events_remain(self):
        s=self.start()
        self.m.checkpoint(s['id'],self.event(id='event-loop-open',kind='open_loop',status='open',loop_id='loop-a',summary='OPEN_SENTINEL'))
        self.m.checkpoint(s['id'],self.event(id='event-loop-close',kind='open_loop',status='closed',loop_id='loop-a',summary='CLOSED_SENTINEL',supersedes='event-loop-open'))
        text=(self.m.root/self.org['path']/'History/OPEN-LOOPS.md').read_text()
        self.assertNotIn('OPEN_SENTINEL',text);self.assertNotIn('CLOSED_SENTINEL',text)
        self.assertEqual(len(self.m.events(self.org)),2)
    def test_same_clock_events_stay_recorded_order(self):
        from unittest.mock import patch
        s=self.start()
        with patch('aco.memory.now',return_value='2026-01-01T00:00:00Z'):
            self.m.checkpoint(s['id'],self.event(id='event-z'))
            self.m.checkpoint(s['id'],self.event(id='event-a'))
        self.assertEqual([e['id'] for e in self.m.events(self.org)],['event-z','event-a'])
    def test_maintenance_session_can_close_without_workspace(self):
        p=self.m.root/self.org['path']/'Context.md'
        prop=self.m.propose_context(self.org['id'],'Changed',digest(p.read_bytes()),'User authorized change')
        self.m.apply_context(self.org['id'],prop['id'],'approval-explicit')
        e=self.m.events(self.org)[0]
        self.assertEqual(self.m.close(e['session_id'])['status'],'closed')

# Inherit fixtures only, not previously counted tests.
for _name in list(MemoryTests.__dict__):
    if _name.startswith('test_') and _name not in AdditionalMemoryTests.__dict__:
        setattr(AdditionalMemoryTests,_name,None)

if __name__=='__main__':unittest.main()
