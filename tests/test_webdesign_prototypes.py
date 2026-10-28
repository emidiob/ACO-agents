import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prototype_review',ROOT/'skills/aco-webdesign/scripts/prototype_review.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PrototypeTests(unittest.TestCase):
    def test_export_escapes_data_and_refuses_collision(self):
        config={'title':'<script>bad</script>','variants':[{'name':'</script><script>bad</script>','url':'/a'},{'name':'B','url':'http://127.0.0.1:1234/'}]}
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp).resolve()/'review';m.export(config,out);page=(out/'index.html').read_text();self.assertNotIn('<script>bad</script>',page);self.assertTrue((out/'review.js').exists());self.assertRaises(ValueError,m.export,config,out)
    def test_local_urls_only(self):
        for url in ['javascript:alert(1)','//example.org/','https://example.org/','http://localhost.evil/','/\\evil/','http://user:pass@localhost/']:
            self.assertRaises(ValueError,m.validate,{'variants':[{'name':'A','url':url},{'name':'B','url':'/b'}]})
    def test_stress_has_stable_unique_records_and_non_latin_cases(self):
        a=m.stress(42);self.assertEqual(a,m.stress(42));cases={x['id']:x for x in a['cases']};self.assertEqual(len({x['id'] for x in cases['large-list']['items']}),1000);self.assertEqual(cases['rtl']['dir'],'rtl');self.assertEqual(cases['empty']['items'],[])
