import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

class CreativePortabilityTests(unittest.TestCase):
    def test_packages_install_without_sibling_skills(self):
        exporter = module('exporter', ROOT/'scripts/package_motion_skill.py')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            for name in ('aco-capture', 'aco-image', 'aco-video', 'aco-genjutsu'):
                archive = base/(name+'.zip')
                exporter.package(archive, name)
                with zipfile.ZipFile(archive) as z:
                    z.extractall(base/'unpacked')
                skill = base/'unpacked'/name
                manifest = json.loads((skill/'package-manifest.json').read_text())
                for rel, digest in manifest['files'].items():
                    self.assertEqual(hashlib.sha256((skill/rel).read_bytes()).hexdigest(), digest)
                for host, folder in (('claude', '.claude'), ('codex', '.agents')):
                    run = subprocess.run([sys.executable, str(skill/'scripts/install_standalone.py'), '--host', host, '--project', str(base/'host'), '--apply'], capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertEqual((base/'host'/folder/'skills'/name/'SKILL.md').read_bytes(), (skill/'SKILL.md').read_bytes())

    def test_inventory_truthful_and_preserves_output(self):
        helper = module('inventory', ROOT/'scripts/creative_reference_inventory.py')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve();source = base/'reference.bin';source.write_bytes(b'actual source')
            output = base/'references.json'
            result = helper.inventory([source], output)
            row = result['references'][0]
            self.assertEqual(row['sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertFalse(row['visually_reviewed'])
            self.assertFalse(row['audio_listened'])
            self.assertIsNone(row['provider_binding'])
            before = output.read_bytes()
            with self.assertRaises(ValueError):helper.inventory([source], output)
            self.assertEqual(output.read_bytes(), before)
            with self.assertRaises(FileNotFoundError):helper.inventory([base/'missing'], base/'missing.json')
            self.assertFalse((base/'missing.json').exists())
            with self.assertRaises(ValueError):helper.inventory([source,source], base/'duplicate.json')
            self.assertFalse((base/'duplicate.json').exists())
