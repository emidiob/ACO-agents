"""ACO quick commands: installation, routing and fail-closed technical statuses."""
import tempfile
import unittest
from pathlib import Path
from scripts.aco.common import ROOT
from scripts.aco.skills import skill_registry_check, skill_resolve, skill_search
from scripts.aco.install import Installer

COMMANDS = ['aco','aco-genjutsu','aco-video','aco-image','aco-capture','aco-skills','aco-help']

class ACOCommandKitTests(unittest.TestCase):
    def test_entry_points(self):
        for name in COMMANDS:
            with self.subTest(name=name):
                file = ROOT / 'skills' / name / 'SKILL.md'
                self.assertTrue(file.is_file())
                self.assertIn('name: ' + name, file.read_text())

    def test_registry_and_experimental_method(self):
        r = skill_registry_check(ROOT)
        self.assertEqual((r['skills'], r['active_skills'], r['candidate_skills']),(44,14,30))
        self.assertFalse(any(x['skill_id']=='video.seedance.reference-video-replica'
                             for x in skill_search('reference video replica motion transfer',root=ROOT)['results']))
        resolved=skill_resolve('video.seedance.reference-video-replica',allow_candidate=True,root=ROOT)
        self.assertFalse(resolved['selectable'])

    def test_managed_aco_name_installs_and_uninstalls(self):
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            installer=Installer(home)
            self.assertEqual(installer.install(['none'],True)['status'],'installed_verified')
            self.assertTrue((home/'.agents/skills/aco/SKILL.md').exists())
            self.assertTrue((home/'.agents/skills/aco-genjutsu/SKILL.md').exists())
            self.assertEqual(installer.status()['modified_or_missing'],[])
            self.assertEqual(installer.uninstall(True)['status'],'uninstalled_verified')

    def test_documented_commands_in_entrypoints(self):
        for doc in ('AGENTS.md','CHATGPT.md','docs/CHATGPT-PROJECT-INSTRUCTIONS.txt'):
            with self.subTest(doc=doc):
                body=(ROOT / doc).read_text(encoding='utf-8')
                self.assertIn('/aco-genjutsu',body)
                self.assertIn('/aco',body)
