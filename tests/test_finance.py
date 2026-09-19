import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ACOError
from aco.finance import budget_check
class FinanceTests(unittest.TestCase):
 def setUp(self):self.d={'currency':'EUR','lines':[{'id':'crew','quantity':'2','unit_cost':'500'}],'overhead':'100','contingency_percent':'10','quote_net':'1600'}
 def test_arithmetic(self):
  r=budget_check(self.d);self.assertEqual(r['total_cost'],'1210.00');self.assertEqual(r['estimated_contribution'],'390.00')
 def test_margin_and_markup_differ(self):
  r=budget_check(self.d);self.assertEqual(r['margin_percent'],'24.3750');self.assertNotEqual(r['margin_percent'],r['markup_percent'])
 def test_no_tax_inference(self):self.assertNotIn('quote_including_supplied_tax',budget_check(self.d))
 def test_explicit_tax(self):
  self.d['tax_percent']='10';self.assertEqual(budget_check(self.d)['quote_including_supplied_tax'],'1760.00')
 def test_target_margin(self):
  self.d['target_margin_percent']='50';self.assertEqual(budget_check(self.d)['price_for_target_margin'],'2420.00')
 def test_duplicate_line(self):
  self.d['lines']*=2
  with self.assertRaises(ACOError):budget_check(self.d)
 def test_no_mixed_currency(self):
  self.d['lines'][0]['currency']='USD'
  with self.assertRaises(ACOError):budget_check(self.d)
 def test_float_rejected(self):
  self.d['overhead']=1.5
  with self.assertRaises(ACOError):budget_check(self.d)
 def test_negative_cost_rejected(self):
  self.d['overhead']='-3'
  with self.assertRaises(ACOError):budget_check(self.d)
 def test_invalid_or_extreme_numbers(self):
  for value in ['NaN','Infinity','1e99999',True]:
   self.d['overhead']=value
   with self.assertRaises(ACOError):budget_check(self.d)
 def test_zero_revenue(self):
  self.d['quote_net']='0';r=budget_check(self.d);self.assertIsNone(r['margin_percent']);self.assertEqual(r['estimated_contribution'],'-1210.00')
 def test_loss_reported(self):
  self.d['quote_net']='100';self.assertEqual(budget_check(self.d)['estimated_contribution'],'-1110.00')
 def test_invalid_target(self):
  self.d['target_margin_percent']='100'
  with self.assertRaises(ACOError):budget_check(self.d)
