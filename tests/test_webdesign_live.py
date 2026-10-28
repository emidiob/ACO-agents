import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import threading
import unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError

SCRIPTS=Path(__file__).resolve().parents[1]/'skills/aco-webdesign/scripts'
sys.path.insert(0,str(SCRIPTS))
from live_editor import Project,server
from components import catalog,export,ROOT
from audit_design import audit
from design_rules import RULES,contrast

class LiveEditorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.file=self.root/'index.html';self.file.write_text('<!doctype html><html><body><h1>Hello</h1><p style="color: red">World</p><div><b>Nested</b></div></body></html>');self.project=Project(self.root)
    def tearDown(self):self.tmp.cleanup()
    def edit(self,**kw):
        data={'file':'index.html','hash':hashlib.sha256(self.file.read_bytes()).hexdigest(),'node':0,'kind':'text','value':'Changed'};data.update(kw);return self.project.apply(data)
    def test_source_roundtrip_and_markup_escape(self):
        original=self.file.read_bytes();self.edit(value='<script>x</script>');self.assertIn('&lt;script&gt;',self.file.read_text());changed=self.file.read_bytes();self.project.history('undo');self.assertEqual(self.file.read_bytes(),original);self.project.history('redo');self.assertEqual(self.file.read_bytes(),changed)
    def test_conflict_does_not_overwrite(self):
        digest=hashlib.sha256(self.file.read_bytes()).hexdigest();self.file.write_text('external');self.assertRaises(ValueError,self.edit,hash=digest);self.assertEqual(self.file.read_text(),'external')
    def test_history_conflict(self):
        self.edit();self.file.write_text('external');self.assertRaises(ValueError,self.project.history,'undo');self.assertEqual(self.file.read_text(),'external')
    def test_nested_text_refused(self):self.assertRaises(ValueError,self.edit,node=2)
    def test_style_preserves_other_properties(self):
        self.edit(node=1,kind='style',property='font-size',value='24px');self.assertIn('color: red; font-size: 24px',self.file.read_text())
    def test_bad_styles_and_paths(self):
        for value in ['red; display:none','url(http://example.com)','expression(x)']:
            with self.subTest(value=value):self.assertRaises(ValueError,self.edit,kind='style',property='color',value=value)
        for value in ['../index.html','/etc/passwd','.secret']:
            with self.subTest(path=value):self.assertRaises(ValueError,self.project.path,value)
        (self.root/'link.html').symlink_to(self.file);self.assertRaises(ValueError,self.project.read,'link.html')
    def test_preview_does_not_modify_source(self):
        before=self.file.read_bytes();self.assertIn('data-aco-node="0"',self.project.preview('index.html'));self.assertEqual(self.file.read_bytes(),before)
    def test_http_auth_and_source_save(self):
        httpd=server(self.project);thread=threading.Thread(target=httpd.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{httpd.server_port}'
        try:
            with urlopen(base+'/__aco/') as response:html=response.read().decode()
            token=re.search(r'acoToken="([\w-]{30,})"',html).group(1)
            data=json.dumps({'file':'index.html','hash':hashlib.sha256(self.file.read_bytes()).hexdigest(),'node':0,'kind':'text','value':'HTTP saved'}).encode()
            with self.assertRaises(HTTPError) as error:urlopen(Request(base+'/__aco/edit',data=data))
            self.assertEqual(error.exception.code,403)
            with urlopen(Request(base+'/__aco/edit',data=data,headers={'Origin':base,'X-ACO-Token':token})) as response:self.assertTrue(json.load(response)['saved'])
            self.assertIn('HTTP saved',self.file.read_text())
            with self.assertRaises(HTTPError):urlopen(Request(base+'/__aco/',headers={'Host':'evil.example'}))
        finally:httpd.shutdown();httpd.server_close();thread.join()

class ComponentTests(unittest.TestCase):
    def test_catalog_has_concrete_sources(self):
        entries=catalog();self.assertEqual(len(entries),64);self.assertEqual(len(set(e['id'] for e in entries)),len(entries))
        for entry in entries:
            with self.subTest(component=entry['id']):
                html=(ROOT/(entry['id']+'.html')).read_text();self.assertTrue(html.strip());self.assertTrue(entry['behavior']);self.assertNotIn('<script src="http',html)
    def test_export_collision_and_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'gallery';export(dest,['tabs','dialog']);html=(dest/'index.html').read_text();self.assertIn('data-tabs',html);self.assertIn('<dialog',html);self.assertNotIn('data-carousel',html);self.assertTrue((dest/'aco.js').is_file());self.assertRaises(ValueError,export,dest,['tabs']);self.assertRaises(ValueError,export,Path(tmp)/'bad',['../../x'])

class DesignTests(unittest.TestCase):
    def test_registry(self):self.assertEqual(len(RULES),62);self.assertEqual(len({r[0] for r in RULES}),62)
    def test_contrast_known_pairs(self):
        self.assertAlmostEqual(contrast('#000000','#ffffff'),21);self.assertAlmostEqual(contrast('rgb(255, 255, 255)','#ffffff'),1);self.assertIsNone(contrast('rgba(0, 0, 0, 0.5)','#ffffff'))
    def test_unknown_measurements_are_not_passes(self):
        result=audit({'schema':2,'elements':[],'viewport':{'width':1200,'height':800}});ids={r['id'] for r in result['not_evaluated']};self.assertTrue({'covered-text','orphan-word','runtime-error','system-font'}<=ids)
    def test_ignore_and_findings(self):
        snap={'schema':2,'elements':[{'index':0,'tag':'p','text':'Example','fontSize':10,'color':'#aaaaaa','effectiveBackground':'#ffffff'}],'viewport':{'width':1200,'height':800}}
        result=audit(snap);self.assertIn('text-contrast',{f['rule'] for f in result['findings']});self.assertNotIn('text-contrast',{f['rule'] for f in audit(snap,ignore=['text-contrast'])['findings']});self.assertRaises(ValueError,audit,snap,ignore=['missing'])

class EffectExports(unittest.TestCase):
    def test_effect_catalog_and_safe_export(self):
        from effects import export as export_effect,ROOT as EFFECTS
        entries=json.loads((EFFECTS/'catalog.json').read_text());self.assertEqual(len(entries),16)
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'effects';export_effect(dest,[e['id'] for e in entries],'<script>alert(1)</script>',1800)
            html=(dest/'index.html').read_text();self.assertNotIn('<script>alert',html);self.assertIn('&lt;script&gt;',html);self.assertEqual(html.count('data-effect='),16)
            self.assertRaises(ValueError,export_effect,dest,['word-reveal'])
            self.assertRaises(ValueError,export_effect,Path(tmp)/'invalid',['word-reveal'],duration=0)
