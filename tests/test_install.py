import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError, Conflict, atomic_write, read_json, write_json, ROOT
from aco.install import Installer, agent_set

class InstallTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.home=Path(self.tmp.name)/'home';self.home.mkdir();self.i=Installer(self.home)
 def tearDown(self):self.tmp.cleanup()
 def test_dry_run_does_not_install(self):
  r=self.i.install(['none']);self.assertEqual(r['status'],'dry_run');self.assertFalse(self.i.skill_root.exists())
 def test_all_agents_and_nine_skills(self):
  r=self.i.install(['all'],True)
  self.assertEqual(r['status'],'installed_verified')
  self.assertEqual(len(list(self.i.agent_root.glob('*.toml'))),246)
  self.assertEqual(len(list(self.i.skill_root.glob('*/SKILL.md'))),9)
 def test_skills_only(self):
  self.i.install(['none'],True);self.assertFalse(self.i.agent_root.exists())
 def test_repeat_install_no_changes(self):
  self.i.install(['none'],True);self.assertEqual(self.i.install(['none'])['changes'],[])
 def test_unmanaged_collision_no_partial_install(self):
  p=self.i.skill_root/'aco-artist-office/SKILL.md';p.parent.mkdir(parents=True);p.write_text('personal instructions')
  with self.assertRaises(Conflict):self.i.install(['all'],True)
  self.assertEqual(p.read_text(),'personal instructions');self.assertFalse(self.i.agent_root.exists())
 def test_directory_collision_no_false_success(self):
  p=self.i.agent_root/'aco-art-director.toml';p.mkdir(parents=True)
  with self.assertRaises(Conflict):self.i.install(['all'],True)
  self.assertFalse(self.i.skill_root.exists())
 def test_existing_unprefixed_agent_preserved(self):
  p=self.i.agent_root/'art-director.toml';p.parent.mkdir(parents=True);p.write_text('user data')
  self.i.install(['all'],True);self.assertEqual(p.read_text(),'user data')
 def test_modified_owned_file_blocks(self):
  self.i.install(['none'],True);p=self.i.skill_root/'aco-artist-office/SKILL.md';p.write_text('local edit')
  with self.assertRaises(Conflict):self.i.install(['none'],True)
  self.assertEqual(p.read_text(),'local edit')
 def test_backup_modified_explicit(self):
  self.i.install(['none'],True);p=self.i.skill_root/'aco-artist-office/SKILL.md';p.write_text('local edit')
  self.i.install(['none'],True,True)
  backups=[p.read_bytes() for p in (self.i.state_root/'backups').rglob('*') if p.is_file()]
  self.assertIn(b'local edit',backups)
 def test_uninstall_only_managed(self):
  self.i.install(['none'],True);p=self.i.skill_root/'other-skill/SKILL.md';p.parent.mkdir();p.write_text('third party')
  self.i.uninstall(True);self.assertTrue(p.exists());self.assertEqual(self.i.status()['managed_files'],0)
 def test_uninstall_modified_refuses(self):
  self.i.install(['none'],True);p=self.i.skill_root/'aco-artist-office/SKILL.md';p.write_text('edited')
  with self.assertRaises(Conflict):self.i.uninstall(True)
  self.assertEqual(p.read_text(),'edited')
 def test_specific_office_dependencies(self):
  keys=agent_set(['agency-office']);self.assertIn('creative_director',keys);self.assertIn('office_concierge',keys)
  self.assertNotIn('mobile_engineer',keys)
 def test_unknown_office(self):
  with self.assertRaises(ACOError):self.i.install(['nonexistent'])
 def test_project_install_separate_paths(self):
  proj=self.home/'clientproject';proj.mkdir();i=Installer(self.home,proj);i.install(['artist-office'],True)
  self.assertTrue((proj/'.agents/skills/aco-artist-office/SKILL.md').exists())
  self.assertTrue((proj/'.codex/agents/aco-art-researcher.toml').exists())
 def test_symlink_refused(self):
  root=self.home/'.agents';root.mkdir();outside=self.home/'outside';outside.mkdir();(root/'skills').symlink_to(outside)
  with self.assertRaises(ACOError):Installer(self.home)
 def test_write_failure_rolls_back_and_raises(self):
  real=atomic_write;trigger={'used':False}
  def broken(path,data,mode=0o600):
   if path.name=='SKILL.md' and not trigger['used']:
    trigger['used']=True;raise OSError('simulated disk failure')
   return real(path,data,mode)
  with patch('aco.install.atomic_write',broken):
   with self.assertRaises(OSError):self.i.install(['none'],True)
  self.assertFalse(self.i.journal.exists());self.assertEqual(self.i.status()['managed_files'],0)
 def test_status_detects_missing_file(self):
  self.i.install(['none'],True);p=self.i.skill_root/'aco-artist-office/SKILL.md';p.unlink()
  self.assertIn(str(p),self.i.status()['modified_or_missing'])
 def test_recovery_no_transaction(self):
  self.assertEqual(self.i.recover()['status'],'nothing_to_recover')

 def test_unlisted_source_material_is_not_installed(self):
  marker=ROOT/'skills/aco-office-concierge/_synthetic-unlisted-test.txt'
  self.assertFalse(marker.exists())
  try:
   marker.write_text('not a released file')
   desired=self.i.desired(['none'])
   self.assertNotIn(str(self.i.skill_root/'aco-office-concierge/_synthetic-unlisted-test.txt'),desired)
  finally:
   marker.unlink(missing_ok=True)

 def test_update_without_offices_preserves_selection(self):
  self.i.install(['artist-office'],True)
  self.i.install(None,True)
  self.assertEqual(self.i.status()['offices'],['artist-office'])
  self.assertTrue((self.i.agent_root/'aco-art-researcher.toml').exists())
 def test_tampered_inventory_cannot_remove_outside_file(self):
  self.i.install(['none'],True)
  outside=self.home/'keep.txt';outside.write_text('preserve')
  state=read_json(self.i.state_file)
  import hashlib
  state['files'][str(outside)]={'sha256':hashlib.sha256(outside.read_bytes()).hexdigest(),'mode':0o644}
  write_json(self.i.state_file,state)
  with self.assertRaises(Conflict):self.i.uninstall(True)
  self.assertEqual(outside.read_text(),'preserve')

if __name__=='__main__':unittest.main()
