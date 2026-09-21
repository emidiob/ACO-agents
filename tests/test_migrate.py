import hashlib,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError,Conflict,ROOT,read_json
from aco.migrate import migrate,git

class MigrationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.repo=Path(self.tmp.name)/'repo';self.repo.mkdir()
  git(self.repo,'init','-b','main');git(self.repo,'config','user.name','Test Fixture')
  git(self.repo,'config','user.email','fixture@example.invalid')
  # Known legacy content is reconstructed from a public baseline fixture below.
  old=ROOT/'tests/fixtures/legacy-plugin.txt';(self.repo/'plugin.json').write_bytes(old.read_bytes())
  (self.repo/'keep.txt').write_text('unrelated tracked file')
  git(self.repo,'add','.');git(self.repo,'commit','-m','fixture')
 def tearDown(self):self.tmp.cleanup()
 def test_dry_run_preserves_repo(self):
  before=git(self.repo,'rev-parse','HEAD');r=migrate(self.repo)
  self.assertEqual(r['status'],'dry_run');self.assertIn('plugin.json',r['remove'])
  self.assertEqual(git(self.repo,'rev-parse','HEAD'),before);self.assertTrue((self.repo/'plugin.json').exists())
 def test_apply_preserves_git_history_and_unrelated(self):
  before=git(self.repo,'rev-parse','HEAD');(self.repo/'private-notes.txt').write_text('untracked private')
  r=migrate(self.repo,True)
  self.assertTrue((self.repo/'.git').exists());self.assertEqual(git(self.repo,'rev-parse','HEAD'),before)
  self.assertEqual((self.repo/'private-notes.txt').read_text(),'untracked private')
  self.assertEqual((self.repo/'keep.txt').read_text(),'unrelated tracked file')
  self.assertFalse((self.repo/'plugin.json').exists());self.assertTrue((self.repo/'CHATGPT.md').exists())
  staged=git(self.repo,'diff','--cached','--name-only');self.assertNotIn('private-notes.txt',staged)
  self.assertEqual(r['status'],'staged_not_committed')
 def test_dirty_tracked_work_stops(self):
  (self.repo/'keep.txt').write_text('unfinished work')
  with self.assertRaises(Conflict):migrate(self.repo,True)
 def test_untracked_collision_stops(self):
  (self.repo/'CHATGPT.md').write_text('untracked custom guide')
  with self.assertRaises(Conflict):migrate(self.repo,True)
 def test_unknown_managed_version_stops(self):
  (self.repo/'plugin.json').write_text('custom plugin variant');git(self.repo,'add','.');git(self.repo,'commit','-m','changed')
  with self.assertRaises(Conflict):migrate(self.repo,True)
 def test_target_nested_folder_stops(self):
  d=self.repo/'nested';d.mkdir()
  with self.assertRaises(ACOError):migrate(d)

 def test_empty_managed_parent_removed(self):
  d=self.repo/'.codex-plugin';d.mkdir();p=d/'plugin.json';p.write_bytes((ROOT/'tests/fixtures/legacy-plugin.txt').read_bytes())
  # Reuse the already-verified owned-manifest mechanism for this synthetic old tree.
  meta=self.repo/'release';meta.mkdir()
  (meta/'manifest.json').write_text(json.dumps({'files':{'.codex-plugin/plugin.json':{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}}}))
  git(self.repo,'add','.');git(self.repo,'commit','-m','nested managed fixture')
  migrate(self.repo,True)
  self.assertFalse(d.exists())
 def test_untracked_in_obsolete_parent_is_not_deleted(self):
  d=self.repo/'.codex-plugin';d.mkdir();p=d/'plugin.json';p.write_bytes((ROOT/'tests/fixtures/legacy-plugin.txt').read_bytes())
  meta=self.repo/'release';meta.mkdir()
  (meta/'manifest.json').write_text(json.dumps({'files':{'.codex-plugin/plugin.json':{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}}}))
  git(self.repo,'add','.');git(self.repo,'commit','-m','nested managed fixture')
  (d/'user-notes.txt').write_text('preserve')
  migrate(self.repo,True)
  self.assertEqual((d/'user-notes.txt').read_text(),'preserve')
  self.assertFalse(p.exists())

 def test_mode_only_managed_change_is_migrated(self):
  # Identical bytes do not imply an identical executable installation.
  source=ROOT/'Install ACO.command';target=self.repo/source.name
  self.assertEqual(source.stat().st_mode & 0o777,0o755)
  target.write_bytes(source.read_bytes());target.chmod(0o644)
  meta=self.repo/'release';meta.mkdir()
  (meta/'manifest.json').write_text(json.dumps({'files':{source.name:{
   'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'mode':0o644}}}))
  git(self.repo,'add','.');git(self.repo,'commit','-m','mode-only managed fixture')
  preview=migrate(self.repo)
  self.assertIn(source.name,preview['replace'])
  result=migrate(self.repo,True)
  self.assertEqual(result['status'],'staged_not_committed')
  self.assertEqual(target.stat().st_mode & 0o777,0o755)
  self.assertEqual(target.read_bytes(),source.read_bytes())

if __name__=='__main__':unittest.main()
