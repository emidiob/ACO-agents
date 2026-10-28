"""Exercise actual standalone packaging, install/update ownership, scaffold and exports."""
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.aco.common import ROOT

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

skill=ROOT/'skills/aco-motion'
scaffold=module('motion_scaffold',skill/'scripts/scaffold.py')
installer=module('motion_installer',skill/'scripts/install_standalone.py')
checker=module('motion_checker',skill/'scripts/check_export.py')
packager=module('motion_packager',ROOT/'scripts/package_motion_skill.py')

class MotionKitTests(unittest.TestCase):
    def test_scaffold_preserves_existing_project(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d).resolve()/'project';scaffold.scaffold(p)
            self.assertTrue((p/'src/index.jsx').is_file())
            self.assertTrue((p/'package-lock.json').is_file())
            (p/'ui.html').write_text('user edits')
            with self.assertRaises(ValueError):scaffold.scaffold(p)
            self.assertEqual((p/'ui.html').read_text(),'user edits')

    def test_standalone_package_hosts_update_and_edit_protection(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d).resolve();archive=d/'motion.zip';packager.package(archive)
            with zipfile.ZipFile(archive) as z:
                self.assertIsNone(z.testzip());z.extractall(d/'extracted')
            source=d/'extracted/aco-motion'
            self.assertTrue((source/'LICENSE').is_file())
            for host in ('.claude/skills','.agents/skills'):
                root=d/'project'/host
                self.assertEqual(installer.install(source,root)['status'],'preview')
                self.assertFalse(root.exists())
                self.assertEqual(installer.install(source,root,True)['status'],'installed')
                self.assertEqual(installer.hashes(source),installer.hashes(root/'aco-motion'))
                with self.assertRaises(ValueError):
                    # A locally changed owned file must not be overwritten.
                    (root/'aco-motion/SKILL.md').write_text('my local edit')
                    installer.install(source,root,True)
                shutil.copyfile(source/'SKILL.md',root/'aco-motion/SKILL.md')
            (source/'references/project-contract.md').write_text('updated project contract')
            result=installer.install(source,d/'project/.agents/skills',True)
            self.assertEqual(result['status'],'installed')
            self.assertTrue(Path(result['backup']).is_dir())
            with self.assertRaises(ValueError):packager.package(archive)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'needs ffmpeg/ffprobe')
    def test_real_export_acceptance_and_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'test.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=160x90:r=30','-t','1','-pix_fmt','yuv420p',str(path)],check=True)
            self.assertEqual(checker.check(path,160,90,30,1,'absent')['errors'],[])
            self.assertIn('dimensions',checker.check(path,1280,720,30,1)['errors'])
            self.assertIn('missing_audio',checker.check(path,160,90,30,1,'required')['errors'])
            self.assertIn('duration',checker.check(path,160,90,30,3)['errors'])
