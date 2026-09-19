"""Fake-provider contract tests. These are NOT live Google Drive tests."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError,Conflict,json_bytes,read_json
from aco.memory import Memory
from aco.drive import DriveBridge

class FakeDrive:
 def __init__(self):
  self.files={'root':{'id':'root','name':'ACO','mimeType':'application/vnd.google-apps.folder','parents':[]}}
  self.bytes={};self.n=0;self.fail_upload=False;self.lose_response=False;self.read_corrupt=False
 def generate_id(self):self.n+=1;return 'f'+str(self.n)
 def metadata(self,id):
  if id not in self.files:raise ACOError('not found')
  return copy.deepcopy(self.files[id])
 def list_named(self,parent,name):return [copy.deepcopy(f) for f in self.files.values() if parent in f.get('parents',[]) and f['name']==name]
 def create_folder(self,parent,name):
  id=self.generate_id();f={'id':id,'name':name,'mimeType':'application/vnd.google-apps.folder','parents':[parent]};self.files[id]=f;return f
 def read(self,id):
  if id not in self.bytes:raise ACOError('not readable')
  return b'corrupt' if self.read_corrupt else self.bytes[id]
 def upload(self,parent,id,name,data):
  if self.fail_upload:raise ACOError('permission denied')
  if id in self.files:raise ACOError('already exists')
  self.files[id]={'id':id,'name':name,'mimeType':'application/json','parents':[parent]};self.bytes[id]=data
  if self.lose_response:raise ACOError('response lost')
  return self.files[id]

class DriveTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();b=Path(self.tmp.name);self.m=Memory(b/'knowledge');self.m.init()
  o=self.m.add_entity('organization','studio','Studio')['entity'];p=b/'project';p.mkdir()
  self.session=self.m.start(o['id'],'Test',p)['session']['id']
  self.m.checkpoint(self.session,{'id':'event-one','kind':'work','status':'proposed','summary':'Draft'})
  self.d=FakeDrive();self.bridge=DriveBridge(self.m,self.d)
 def tearDown(self):self.tmp.cleanup()
 def bind(self):return self.bridge.bind('root','user approved root')
 def test_bind_requires_approval(self):
  with self.assertRaises(ACOError):self.bridge.bind('root','')
 def test_repeated_bind_single_folder(self):
  a=self.bind();b=self.bind();self.assertEqual(a,b);self.assertEqual(len(self.d.files),2)
 def test_bind_different_root_conflict(self):
  self.bind();self.d.files['other']={'id':'other','mimeType':'application/vnd.google-apps.folder','name':'Other','parents':[]}
  with self.assertRaises(Conflict):self.bridge.bind('other','approved')
 def test_duplicate_folder_conflict(self):
  self.d.create_folder('root','ACO Session Events');self.d.create_folder('root','ACO Session Events')
  with self.assertRaises(Conflict):self.bind()
 def test_sync_readback_receipt(self):
  self.bind();r=self.bridge.sync();self.assertEqual(r['events'][0]['status'],'drive_verified')
  self.assertEqual(self.m.status()['pending_drive_events'],[])
 def test_repeated_sync_no_duplicate(self):
  self.bind();self.bridge.sync();n=len(self.d.files);r=self.bridge.sync()
  self.assertEqual(len(self.d.files),n);self.assertEqual(r['events'][0]['status'],'already_synced_verified')
 def test_denied_write_stays_pending(self):
  self.bind();self.d.fail_upload=True
  with self.assertRaises(ACOError):self.bridge.sync()
  self.assertEqual(self.m.status()['pending_drive_events'],['event-one'])
 def test_retry_uses_same_preallocated_id(self):
  self.bind();self.d.fail_upload=True
  with self.assertRaises(ACOError):self.bridge.sync()
  mapping=read_json(self.m.system/'Sync/event-one.json')
  self.d.fail_upload=False;r=self.bridge.sync();self.assertEqual(r['events'][0]['file_id'],mapping['file_id'])
 def test_lost_write_response_verified_not_duplicated(self):
  self.bind();self.d.lose_response=True;r=self.bridge.sync();self.assertEqual(r['events'][0]['status'],'drive_verified')
  self.assertEqual(len(self.d.bytes),1)
 def test_corrupt_readback_no_receipt(self):
  self.bind();self.d.read_corrupt=True
  with self.assertRaises(Conflict):self.bridge.sync()
  self.assertEqual(self.m.status()['pending_drive_events'],['event-one'])
 def test_remote_event_changed_after_sync(self):
  self.bind();r=self.bridge.sync();fid=r['events'][0]['file_id'];self.d.bytes[fid]=b'changed'
  with self.assertRaises(Conflict):self.bridge.sync()
 def test_destination_moved_outside_root(self):
  cfg=self.bind();self.d.files[cfg['events_folder_id']]['parents']=[]
  with self.assertRaises(Conflict):self.bridge.sync()
 def test_duplicate_remote_event_conflict(self):
  cfg=self.bind()
  for _ in range(2):self.d.upload(cfg['events_folder_id'],self.d.generate_id(),'event-one.json',b'x')
  with self.assertRaises(Conflict):self.bridge.sync()
 def test_session_filter(self):
  self.bind();r=self.bridge.sync('session-'+'0'*32);self.assertEqual(r['events'],[])
 def test_existing_different_event_no_overwrite(self):
  cfg=self.bind();fid=self.d.generate_id();self.d.upload(cfg['events_folder_id'],fid,'event-one.json',b'different')
  with self.assertRaises(Conflict):self.bridge.sync()
  self.assertEqual(self.d.bytes[fid],b'different')

if __name__=='__main__':unittest.main()
