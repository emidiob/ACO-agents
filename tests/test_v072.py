import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aco.common import ROOT, VERSION
from aco.context import context_plan, mode_policy
from aco.efficiency import context_benchmark, real_world_benchmark
from aco.hybrid import memory_resolve
from aco.routing import route_benchmark, suggest_route


class ContextEngine072Tests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(VERSION, '0.8.0')

    def test_full_does_not_cross_client_boundary(self):
        r=context_plan({'mode':'FULL','sources':[
            {'id':'current','estimated_chars':3000,'relevance':.9,'authority':.9,'private':True,'scope_relation':'same_entity'},
            {'id':'foreign','estimated_chars':3000,'relevance':1,'authority':1,'private':True,'scope_relation':'other_private_entity','scope_id':'client-foreign'}]})
        self.assertIn('current',r['selected_source_ids'])
        self.assertNotIn('foreign',r['selected_source_ids'])
        self.assertIn('cross_scope_private_blocked',{x['reason'] for x in r['denied_sources']})
        self.assertFalse(r['prompt_for_drive'])

    def test_blind_first_only_opens_after_first_pass(self):
        self.assertEqual(mode_policy('BLIND-FIRST',phase='initial',first_pass_complete=False)['effective_mode'],'BLIND')
        self.assertEqual(mode_policy('BLIND-FIRST',phase='refine',first_pass_complete=True)['effective_mode'],'LIGHT')

    def test_full_stays_selective(self):
        r=context_plan({'mode':'FULL','sources':[
            {'id':'brief','estimated_chars':2000,'relevance':.95,'authority':.9,'private':False,'scope_relation':'task_local'},
            {'id':'archive','estimated_chars':12000,'relevance':.2,'authority':.6,'private':True,'scope_relation':'same_entity'}]})
        self.assertEqual(r['selected_source_ids'],['brief'])
        self.assertIn('below_relevance_floor',{x['reason'] for x in r['denied_sources']})

    def test_explicit_cross_scope_can_be_used(self):
        r=context_plan({'mode':'FULL','authorized_private_scope_ids':['client-related'],'sources':[
            {'id':'related','estimated_chars':3000,'relevance':.95,'authority':.9,'private':True,'scope_relation':'other_private_entity','scope_id':'client-related'}]})
        self.assertEqual(r['selected_source_ids'],['related'])

    def test_unavailable_persistence_never_prompts(self):
        r=context_plan({'mode':'LIGHT','material_change':True,'explicit_persistence_request':True,'persistent_store_available':False,'sources':[]})
        self.assertFalse(r['prompt_for_drive'])
        self.assertEqual(r['persistence_status'],'continue_without_persistence')
        self.assertIn('pending',r['notice'])

    def test_context_benchmark(self):
        r=context_benchmark()
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['critical_failures'],0)
        self.assertLessEqual(r['mean_selection_ratio'],.55)


class HybridMemoryRead072Tests(unittest.TestCase):
    def test_cross_client_read_blocked_even_full(self):
        r=memory_resolve({'memory_class':'durable_context','operation':'read','private':True,'scope_relation':'other_private_entity','mode':'FULL'})
        self.assertEqual(r['status'],'scope_blocked')
        self.assertEqual(r['read_status'],'scope_blocked')
        self.assertFalse(r['prompt_for_drive'])

    def test_blind_read_continues_without_private(self):
        r=memory_resolve({'memory_class':'durable_context','operation':'read','private':True,'scope_relation':'same_entity','mode':'BLIND'})
        self.assertEqual(r['read_status'],'mode_blocked')
        self.assertEqual(r['destinations'],[])


class RoutingAndBenchmark072Tests(unittest.TestCase):
    def test_cross_client_request_routes_context_steward(self):
        r=suggest_route("There is similar private history for another client, but keep this client's context isolated and use only the minimum necessary context.")
        self.assertEqual(r['office'],'shared')
        self.assertEqual(r['selected_roles'][0],'context_steward')

    def test_artist_residency_regression(self):
        r=suggest_route('I need to apply to an artist residency for my practice; check the open call, deadline and work samples.')
        self.assertEqual(r['office'],'artist-office')
        self.assertIn(r['selected_roles'][0],{'art_opportunities_scout','grants_applications_manager'})

    def test_independent_brand_strategy_regression(self):
        r=suggest_route('For an independent cultural project, define positioning and brand architecture before visual identity work; this is not a client account.')
        self.assertEqual(r['office'],'shared')
        self.assertEqual(r['selected_roles'][0],'brand_strategist')

    def test_fresh_holdout_3(self):
        r=route_benchmark(ROOT/'config/routing-v072-holdout-3.json')
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['critical_failures'],0)
        self.assertEqual(r['cases'],36)

    def test_real_world_120(self):
        r=real_world_benchmark()
        self.assertEqual(r['status'],'passed',r['failures'])
        self.assertEqual(r['cases'],120)
        self.assertEqual(r['critical_failures'],0)
        self.assertEqual(r['drive_prompts'],0)
        self.assertLessEqual(r['mean_context_selection_ratio'],.55)

    def test_holdout_not_in_routing_examples(self):
        examples=json.loads((ROOT/'config/routing-examples.json').read_text())
        hold=json.loads((ROOT/'config/routing-v072-holdout-3.json').read_text())
        trained={x['prompt'] for x in examples['examples']}
        fresh={x['prompt'] for x in hold['cases']}
        self.assertFalse(trained & fresh)


if __name__=='__main__': unittest.main()
