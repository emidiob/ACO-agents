"""Executable checks. These do not run language models or grade artistic judgment."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/aco-office-concierge/scripts/competence_library.py'
spec=importlib.util.spec_from_file_location('aco_cl_original',SCRIPT)
cl=importlib.util.module_from_spec(spec);spec.loader.exec_module(cl)
CASES=json.loads((ROOT/'tests/fixtures/competence-library/contracts.json').read_text())['cases']

class ContractTests(unittest.TestCase):
    pass

def positive(case):
    def run(self):
        result=cl.audit(case['kind'],copy.deepcopy(case['record']))
        self.assertEqual(result['status'],'checked',result)
        for k,v in case['expected'].items():self.assertEqual(result[k],v)
    return run

def negative(case,mutation):
    def run(self):
        record=copy.deepcopy(case['record']);p=record
        for key in mutation['path'][:-1]:p=p[key]
        p[mutation['path'][-1]]=copy.deepcopy(mutation['value'])
        try:result=cl.audit(case['kind'],record)
        except cl.LibraryError:return
        self.assertEqual(result['status'],'failed',result)
        self.assertTrue(result['errors'])
    return run

for case in CASES:
    setattr(ContractTests,'test_positive_'+case['id'].replace('-','_'),positive(case))
    for mutation in case['negative_mutations']:
        setattr(ContractTests,'test_reject_'+case['id'].replace('-','_')+'_'+mutation['name'],negative(case,mutation))

class LibraryTests(unittest.TestCase):
    def test_twenty_complete_modules(self):
        r=cl.validate();self.assertEqual(r['status'],'valid',r)
        self.assertEqual((r['competencies'],r['sources'],r['worked_examples']),(20,37,40))
    def test_curated_methods_available_for_ordinary_use(self):
        for row in cl.list_competencies():
            self.assertEqual(row['status'],'curated')
            self.assertTrue(row['auto_selectable'])
            self.assertEqual(cl.resolve(row['id'])['status'],'loaded_curated_method')
    def test_selected_loading_only(self):
        r=cl.resolve('administration')
        self.assertEqual(set(r['files']),{'METHOD.md','DECISIONS.md','OUTPUT.md'})
        self.assertNotIn('curatorial-practice',str(r['files']))
    def test_unknown_id(self):
        with self.assertRaises(cl.LibraryError):cl.resolve('../private')
    def test_office_filter(self):
        rows=cl.list_competencies(office='artist-office')
        self.assertTrue(rows)
        self.assertTrue(all('artist-office' in r['offices'] for r in rows))
    def test_invalid_office(self):
        with self.assertRaises(cl.LibraryError):cl.list_competencies(office='fake-office')
    def test_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            for rel in ('../secret','a/../b','/etc/passwd','C:/private','a\\b','a//b','./a'):
                with self.subTest(rel=rel):
                    with self.assertRaises(cl.LibraryError):cl.safe_path(Path(d),rel)
    def test_symlink_leaf(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'real').write_text('x');(p/'link').symlink_to(p/'real')
            with self.assertRaises(cl.LibraryError):cl.safe_path(p,'link')
    def test_symlink_parent(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'real').mkdir();(p/'link').symlink_to(p/'real',target_is_directory=True)
            with self.assertRaises(cl.LibraryError):cl.safe_path(p/'link','x')
    def test_json_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"x":1,"x":2}')
            with self.assertRaises(cl.LibraryError):cl.read_json(p)
    def test_json_nonfinite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{"x":NaN}')
            with self.assertRaises(cl.LibraryError):cl.read_json(p)
    def test_json_malformed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';p.write_text('{broken')
            with self.assertRaises(cl.LibraryError):cl.read_json(p)
    def test_amount_bool_float_rejected(self):
        for x in (True,False,0.1,float('inf')):
            with self.subTest(x=str(x)):
                with self.assertRaises(cl.LibraryError):cl.decimal(x)
    def test_zero_revenue_no_division_by_zero(self):
        b=copy.deepcopy(next(x for x in CASES if x['id']=='finance')['record']);b['revenue']='0'
        self.assertIsNone(cl.budget(b)['margin_percent'])
    def test_finance_cash_deficit_not_hidden(self):
        b=next(x for x in CASES if x['id']=='finance')['record'];r=cl.budget(b)
        self.assertEqual(r['cash'][0]['closing_cash'],'-500.00');self.assertTrue(r['cash'][0]['negative'])
    def test_delivery_change_is_plus_three(self):
        b=copy.deepcopy(next(x for x in CASES if x['id']=='delivery')['record'])
        b['tasks'][1]['duration']=5;b['tasks'][2]['duration']=5
        self.assertEqual(cl.schedule(b['tasks'])['duration'],'14')
    def test_parallel_tasks_not_naively_summed(self):
        r=cl.schedule([{'id':'A','duration':2,'depends_on':[]},{'id':'B','duration':5,'depends_on':[]},{'id':'C','duration':3,'depends_on':['A','B']}])
        self.assertEqual(r['duration'],'8')
    def test_duplicate_task_rejected(self):
        with self.assertRaises(cl.LibraryError):cl.schedule([{'id':'A','duration':1,'depends_on':[]},{'id':'A','duration':2,'depends_on':[]}])
    def test_portfolio_combinations(self):
        data=next(x for x in CASES if x['id']=='strategy')['record']
        self.assertEqual([r['ids'] for r in cl.portfolio(data)['feasible']],[['A'],['B'],['C'],['B','C']])
        self.assertIsNone(cl.portfolio(data)['recommendation'])
    def test_fractional_rate_no_silent_rounding(self):
        data={'fps':[30000,1001],'duration_frames':300,'expected_seconds':10,'tracks':[{'id':'v','continuous':True,'clips':[{'id':'x','start':0,'end':300}]}]}
        with self.assertRaises(cl.LibraryError):cl.timeline(data)
    def test_cli_unknown_audit_nonzero(self):
        p=subprocess.run([sys.executable,str(SCRIPT),'audit','--kind','fake','--input',str(ROOT/'registry/competences.json')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
    def test_cli_curated_no_experimental_gate(self):
        p=subprocess.run([sys.executable,str(SCRIPT),'show','--id','administration'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertTrue(json.loads(p.stdout)['auto_selectable'])
    def test_cli_selected_load(self):
        p=subprocess.run([sys.executable,str(SCRIPT),'show','--id','administration'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertTrue(json.loads(p.stdout)['auto_selectable'])
    def test_baseline_missing_is_not_faked(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(cl.LibraryError):cl.check_baseline(Path(d))
    def test_future_challenges_not_called_holdouts(self):
        for row in cl.load_registry()['competencies']:
            ev=cl.read_json(cl.DEFAULT_ROOT/row['directory']/'EVALS.json')
            self.assertFalse(ev['new_case_is_independent_holdout']);self.assertEqual(ev['new_case_status'],'not_run')

if __name__=='__main__':unittest.main()
