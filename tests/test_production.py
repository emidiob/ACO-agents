import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError
from aco.production import comfy_preflight
class ComfyTests(unittest.TestCase):
 def setUp(self):
  self.g={'1':{'class_type':'ExampleSource','inputs':{'value':3}},'2':{'class_type':'ExampleOutput','inputs':{'value':['1',0]}}}
  self.i={'ExampleSource':{'input':{'required':{'value':['INT',{'min':0,'max':10}]}},'output':['INT']},'ExampleOutput':{'input':{'required':{'value':['INT',{'forceInput':True}]}},'output':[]}}
 def test_structural_pass_not_render(self):
  r=comfy_preflight(self.g,self.i);self.assertEqual(r['status'],'static_checks_passed');self.assertFalse(r['executed'])
 def test_missing_node(self):
  self.g['1']['class_type']='Unregistered';self.assertEqual(comfy_preflight(self.g,self.i)['status'],'static_issues')
 def test_ui_workflow_rejected(self):
  with self.assertRaises(ACOError):comfy_preflight({'nodes':[]},self.i)
 def test_missing_required_input(self):
  self.g['1']['inputs']={};self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_link_source_missing(self):
  self.g['2']['inputs']['value']=['9',0];self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_link_index_invalid(self):
  self.g['2']['inputs']['value']=['1',5];self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_negative_output_index(self):
  self.g['2']['inputs']['value']=['1',-1];self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_type_mismatch(self):
  self.i['ExampleSource']['output']=['IMAGE'];self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_literal_range(self):
  self.g['1']['inputs']['value']=40;self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_bool_not_integer(self):
  self.g['1']['inputs']['value']=True;self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_model_enum_missing(self):
  self.i['ExampleSource']['input']['required']['value']=[['registered-model']];self.g['1']['inputs']['value']='invented-model'
  self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_cycle_reported(self):
  self.g['1']['inputs']['value']=['1',0];self.assertIn('Dependency cycle',str(comfy_preflight(self.g,self.i)['errors']))
 def test_unknown_input_is_warning(self):
  self.g['1']['inputs']['dynamic']='x';self.assertTrue(comfy_preflight(self.g,self.i)['warnings'])
 def test_no_graph_mutation(self):
  before=copy.deepcopy(self.g);comfy_preflight(self.g,self.i);self.assertEqual(before,self.g)
 def test_no_schema_rejected(self):
  with self.assertRaises(ACOError):comfy_preflight(self.g,{})

 def test_malformed_schema(self):
  self.i['ExampleSource']['input']=None;self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
 def test_nonfinite_literal(self):
  self.g['1']['inputs']['value']=float('nan');self.assertTrue(comfy_preflight(self.g,self.i)['errors'])
