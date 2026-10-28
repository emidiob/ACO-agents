import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'skills/aco-webdesign/scripts'
def load(name):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/(name+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class WebdesignEngineTests(unittest.TestCase):
    def data(self, root):
        p=root/'colors.csv';p.write_text('Product Type,Primary,Background,Foreground\nClinic wellness,#006655,#FFFFFF,#111111\nSaaS analytics,#2233AA,#FFFFFF,#111111\n')
        (root/'aco-source.json').write_text(json.dumps({'repository':'test/fixture','revision':'fixture','files':[{'path':'colors.csv','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}))
        return p

    def test_rank_no_match_and_source_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();p=self.data(root);c=load('design_data').Catalog(root)
            result=c.search('clinic wellness','colors',1)
            self.assertEqual(result['results'][0]['values']['Primary'],'#006655')
            self.assertTrue(result['source']['manifest_verified'])
            self.assertEqual(c.search('xyzzy','colors')['results'],[])
            with self.assertRaises(ValueError):c.search('x','../colors')
            p.write_text(p.read_text()+'tampered')
            with self.assertRaises(ValueError):c.search('clinic','colors')

    def test_bad_csv_symlink_and_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();p=root/'bad.csv';p.write_text('name,name\na,b\n')
            c=load('design_data').Catalog(root)
            with self.assertRaises(ValueError):c.search('a','bad')
            with self.assertRaises(ValueError):c.search('a','bad',0)
            (root/'alias.csv').symlink_to(p)
            with self.assertRaises(ValueError):load('design_data').Catalog(root)

    def test_system_overrides_and_non_destructive_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();self.data(root);data=load('design_data')
            with patch.dict(sys.modules,{'design_data':data}):system=load('design_system')
            result=system.generate(data.Catalog(root),'clinic',overrides={'primary':'#AABBCC'})
            self.assertEqual(result['color_tokens']['primary'],'#AABBCC')
            self.assertFalse(result['browser_verified'])
            out=root/'proposal';system.persist(result,out)
            original=(out/'tokens.css').read_text()
            with self.assertRaises(ValueError):system.persist(result,out)
            self.assertEqual((out/'tokens.css').read_text(),original)
            with self.assertRaises(ValueError):system.generate(data.Catalog(root),'clinic',overrides={'x':'red; bad'})

    def test_snapshot_positive_and_negative_evidence(self):
        audit=load('audit_snapshot').audit
        base={'schema':1,'title':'App','lang':'en','viewport':{'width':390},'scrollWidth':390,'viewportMeta':'width=device-width','elements':[{'index':0,'tag':'main'},{'index':1,'tag':'h1'}]}
        self.assertEqual(audit(base)['findings'],[])
        base['scrollWidth']=800
        base['elements'].append({'index':2,'tag':'button','name':'','width':10,'height':10,'tabindex':'2'})
        codes={x['code'] for x in audit(base)['findings']}
        self.assertTrue({'page-overflow','small-target','control-name','positive-tabindex'}.issubset(codes))
        self.assertFalse(audit(base)['interaction_verified'])
        with self.assertRaises(ValueError):audit({})

    def test_fetch_preserves_existing_destinations(self):
        fetch=load('fetch_design_data').fetch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'user.txt').write_text('keep')
            with self.assertRaises(ValueError):fetch(root)
            self.assertEqual((root/'user.txt').read_text(),'keep')

if __name__=='__main__':unittest.main()
