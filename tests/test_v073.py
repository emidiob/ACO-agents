import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aco.common import ACOError, ROOT, VERSION
from aco.context import context_plan
from aco.efficiency import context_benchmark, real_world_benchmark, scope_boundary_benchmark
from aco.hybrid import memory_resolve
from aco.routing import route_benchmark


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _semantic_json_sha(path: Path) -> str:
    data=json.loads(path.read_text())
    if isinstance(data,dict):
        data.pop('aco_version',None)
    payload=(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
    return hashlib.sha256(payload).hexdigest()


class ExactScopeAuthorization073Tests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(VERSION,'0.8.0')

    def test_legacy_boolean_is_not_authorization(self):
        r=context_plan({'mode':'FULL','cross_scope_authorized':True,'sources':[
            {'id':'foreign','estimated_chars':1000,'relevance':1,'authority':1,'private':True,
             'scope_relation':'other_private_entity','scope_id':'client-b'}]})
        self.assertNotIn('foreign',r['selected_source_ids'])
        self.assertIn('exact_cross_scope_authorization_required',{x['reason'] for x in r['denied_sources']})
        self.assertFalse(r['authorization']['legacy_boolean_grants_access'])

    def test_exact_scope_id_authorizes_only_that_scope(self):
        r=context_plan({'mode':'FULL','authorized_private_scope_ids':['client-b'],'sources':[
            {'id':'b','estimated_chars':1000,'relevance':1,'authority':1,'private':True,'scope_relation':'other_private_entity','scope_id':'client-b'},
            {'id':'c','estimated_chars':1000,'relevance':1,'authority':1,'private':True,'scope_relation':'other_private_entity','scope_id':'client-c'}]})
        self.assertIn('b',r['selected_source_ids'])
        self.assertNotIn('c',r['selected_source_ids'])

    def test_unknown_private_scope_stays_blocked(self):
        r=context_plan({'mode':'FULL','authorized_private_scope_ids':['mystery'],'sources':[
            {'id':'x','estimated_chars':1000,'relevance':1,'authority':1,'private':True,'scope_relation':'unknown','scope_id':'mystery'}]})
        self.assertNotIn('x',r['selected_source_ids'])
        self.assertIn('unknown_private_scope_blocked',{x['reason'] for x in r['denied_sources']})

    def test_wildcard_authorization_rejected(self):
        with self.assertRaises(ACOError):
            context_plan({'mode':'FULL','authorized_private_scope_ids':['*'],'sources':[]})

    def test_memory_uses_same_exact_boundary(self):
        blocked=memory_resolve({'memory_class':'durable_context','operation':'read','private':True,
            'scope_relation':'other_private_entity','source_scope_id':'client-b','mode':'FULL','cross_scope_authorized':True})
        allowed=memory_resolve({'memory_class':'durable_context','operation':'read','private':True,
            'scope_relation':'other_private_entity','source_scope_id':'client-b','mode':'FULL','authorized_private_scope_ids':['client-b']})
        self.assertEqual(blocked['status'],'scope_blocked')
        self.assertEqual(allowed['read_status'],'allowed')
        self.assertEqual(allowed['scope_decision']['reason'],'cross_scope_exactly_authorized')

    def test_scope_boundary_benchmark(self):
        r=scope_boundary_benchmark()
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['score'],100.0)
        self.assertEqual(r['cases'],28)
        self.assertEqual(r['critical_failures'],0)
        self.assertEqual(r['drive_prompts'],0)


class RoutingFreshGate073Tests(unittest.TestCase):
    def test_development_holdout_is_regression_only(self):
        meta=json.loads((ROOT/'release/v073-holdout-4-result.json').read_text())
        self.assertEqual(meta['first_execution']['status'],'failed')
        self.assertEqual(meta['disposition'],'development_regression_only')
        r=route_benchmark(ROOT/'config/routing-v073-holdout-4.json')
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['critical_failures'],0)

    def test_final_fresh_holdout_5(self):
        result=json.loads((ROOT/'release/v073-holdout-5-result.json').read_text())
        self.assertEqual(result['first_execution']['status'],'passed')
        self.assertEqual(result['first_execution']['score'],98.0)
        self.assertEqual(result['first_execution']['critical_failures'],0)
        r=route_benchmark(ROOT/'config/routing-v073-holdout-5.json')
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['cases'],40)
        self.assertEqual(r['critical_failures'],0)
        self.assertGreaterEqual(r['score'],98.0)

    def test_final_holdout_hash_and_no_exact_overlap(self):
        freeze=json.loads((ROOT/'release/v073-holdout-5-freeze.json').read_text())
        hold=ROOT/'config/routing-v073-holdout-5.json'
        self.assertEqual(_sha(hold),freeze['sha256'])
        examples=json.loads((ROOT/'config/routing-examples.json').read_text())['examples']
        final=json.loads(hold.read_text())['cases']
        trained={x['prompt'] for x in examples}
        self.assertFalse(trained & {x['prompt'] for x in final})

    def test_routing_semantics_frozen_after_final_holdout(self):
        freeze=json.loads((ROOT/'release/v073-routing-semantic-freeze.json').read_text())
        self.assertEqual(_sha(ROOT/'scripts/aco/routing.py'),freeze['routing_py_sha256'])
        self.assertEqual(_semantic_json_sha(ROOT/'config/routing-hints.json'),freeze['routing_hints_semantic_sha256'])
        self.assertEqual(_semantic_json_sha(ROOT/'config/routing-examples.json'),freeze['routing_examples_semantic_sha256'])
        self.assertEqual(_semantic_json_sha(ROOT/'config/role-contracts.json'),freeze['role_contracts_semantic_sha256'])
        self.assertEqual(_semantic_json_sha(ROOT/'catalog.json'),freeze['catalog_semantic_sha256'])


class RegressionAndShape073Tests(unittest.TestCase):
    def test_context_benchmark(self):
        r=context_benchmark()
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['critical_failures'],0)

    def test_real_world_120(self):
        r=real_world_benchmark()
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['cases'],120)
        self.assertEqual(r['critical_failures'],0)
        self.assertEqual(r['drive_prompts'],0)

    def test_release_shape_unchanged(self):
        cat=json.loads((ROOT/'catalog.json').read_text())
        resources=json.loads((ROOT/'skills/aco-office-concierge/references/resources/REGISTRY.json').read_text())
        workflows=json.loads((ROOT/'skills/aco-office-concierge/references/WORKFLOWS.json').read_text())
        self.assertEqual(cat['role_count'],363)
        self.assertEqual(cat['skill_count'],16)
        self.assertEqual(len(resources['resources']),99)
        self.assertEqual(len(workflows['workflows']),61)


if __name__=='__main__': unittest.main()
