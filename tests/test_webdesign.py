import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from scripts.package_motion_skill import package

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/aco-webdesign'
def module(name):
    spec=importlib.util.spec_from_file_location(name,SKILL/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class WebdesignTests(unittest.TestCase):
    def test_search_has_real_matches_and_no_invented_confidence(self):
        search=module('directions').search
        self.assertEqual(search('editorial archive')['directions'][0]['id'],'editorial-fieldnotes')
        self.assertEqual(search('operations tasks')['directions'][0]['id'],'working-console')
        self.assertEqual(search('unlistedword')['status'],'no_keyword_match')
        self.assertEqual(search('unlistedword')['directions'],[])

    def test_audit_reports_real_line_and_control_failures(self):
        audit=module('audit_html').audit
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.html';p.write_text('<html>\n<img src="x">\n<button></button>\n<input placeholder="Email">\n<a href="#">Go</a></html>')
            result=audit(p);codes={x['code'] for x in result['findings']}
            self.assertTrue({'image-alt','control-name','field-label','placeholder-link'}.issubset(codes))
            self.assertEqual(next(x['line'] for x in result['findings'] if x['code']=='image-alt'),2)
            self.assertFalse(result['browser_verified'])
            with self.assertRaises(ValueError):audit(p.with_suffix('.tsx'))

    def test_labels_and_duplicate_ids(self):
        audit=module('audit_html').audit
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'labels.html';p.write_text('<label>Search<input></label><span id="name">Filter</span><input aria-labelledby="name"><button><img src="x" alt="Close"></button><i id="name"></i>')
            codes={x['code'] for x in audit(p)['findings']}
            self.assertIn('duplicate-id',codes)
            self.assertNotIn('control-name',codes)
            # The duplicate ID makes aria-labelledby ambiguous and must remain reviewable.

    def test_examples_and_scaffold_preserve_user_files(self):
        scaffold=module('scaffold').scaffold;audit=module('audit_html').audit
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp).resolve()
            for layout in ('editorial','workspace'):
                target=scaffold(base/layout,layout)
                self.assertEqual(audit(target/'index.html')['findings'],[])
                (target/'index.html').write_text('user edit')
                with self.assertRaises(ValueError):scaffold(target,layout)
                self.assertEqual((target/'index.html').read_text(),'user edit')
            (base/'alias').symlink_to(base/'editorial',target_is_directory=True)
            with self.assertRaises(ValueError):scaffold(base/'alias/new','editorial')

    def test_standalone_archive_and_both_hosts(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp).resolve();archive=base/'webdesign.zip';package(archive,'aco-webdesign')
            with zipfile.ZipFile(archive) as z:z.extractall(base/'unpacked')
            skill=base/'unpacked/aco-webdesign'
            for host,folder in [('claude','.claude'),('codex','.agents')]:
                run=subprocess.run([sys.executable,str(skill/'scripts/install_standalone.py'),'--host',host,'--project',str(base/'host'),'--apply'],capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)
                self.assertEqual((base/'host'/folder/'skills/aco-webdesign/SKILL.md').read_bytes(),(skill/'SKILL.md').read_bytes())
