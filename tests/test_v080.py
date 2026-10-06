import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from aco.autonomy import autonomy_benchmark, autonomy_plan
from aco.common import ACOError, ROOT, VERSION
from aco.execution import action_hash
from aco.goals import goal_graph_check, goal_graph_status, goal_transition


def _graph(task):
    return {
        'schema_version': 1, 'graph_id': 'test-graph', 'scope_id': 'scope-a',
        'nodes': [
            {'id':'p','kind':'program','title':'Program','state':'active','priority':50,'effort':3,'success_criteria':['Outcome']},
            {'id':'g','kind':'goal','title':'Goal','state':'active','parent_id':'p','priority':50,'effort':3,'success_criteria':['Outcome']},
            task,
        ]
    }


def _task(**updates):
    task = {'id':'t','kind':'task','title':'Task','state':'active','parent_id':'g','priority':50,'effort':2,'depends_on':[],'success_criteria':['Verified']}
    task.update(updates)
    return task


def _inventory(cid, operation):
    return {'capabilities':[{'id':cid,'resource_state':'CONNECTED_INTEGRATION','operations':[operation],
        'available':True,'authorized':True,'verified':True,'evidence_ref':'test-evidence','adapter_id':'test-adapter'}]}


class GoalGraph080Tests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(VERSION, '1.0.0')

    def test_valid_graph(self):
        r = goal_graph_check(_graph(_task()))
        self.assertEqual(r['status'], 'valid', r['errors'])
        self.assertEqual(r['programs'], 1)
        self.assertEqual(r['goals'], 1)
        self.assertEqual(r['tasks'], 1)

    def test_cross_scope_node_rejected(self):
        g = _graph(_task(scope_id='other-scope'))
        r = goal_graph_check(g)
        self.assertEqual(r['status'], 'invalid')
        self.assertTrue(any('node scope must equal graph scope' in x for x in r['errors']))

    def test_dependency_blocks_then_unblocks(self):
        g = _graph(_task(depends_on=['d']))
        g['nodes'].append({'id':'d','kind':'dependency','title':'External reply','state':'active','parent_id':'t',
                           'priority':50,'effort':1,'success_criteria':['Reply received']})
        r = goal_graph_status(g)
        self.assertEqual(r['next_task_ids'], [])
        self.assertEqual(r['blocked_task_ids'], ['t'])
        g['nodes'][-1]['state'] = 'done'
        r = goal_graph_status(g)
        self.assertEqual(r['next_task_ids'], ['t'])

    def test_in_progress_work_gets_continuation_bonus(self):
        g = _graph(_task(id='new', priority=65))
        g['nodes'].append(_task(id='cont', state='in_progress', priority=45))
        r = goal_graph_status(g, limit=2)
        self.assertEqual(r['next_task_ids'], ['cont', 'new'])

    def test_verified_transition_requires_evidence(self):
        g = _graph(_task(state='executed'))
        with self.assertRaises(ACOError):
            goal_transition(g, {'node_id':'t','to_state':'verified'})
        r = goal_transition(g, {'node_id':'t','to_state':'verified','evidence_ref':'receipt:test'})
        self.assertEqual(r['graph']['nodes'][-1]['state'], 'verified')

    def test_invalid_transition_rejected(self):
        g = _graph(_task(state='active'))
        with self.assertRaises(ACOError):
            goal_transition(g, {'node_id':'t','to_state':'done'})


class Autonomy080Tests(unittest.TestCase):
    def _action(self, cid='web.research', op='search', aid='a'):
        return {'id':aid,'capability_id':cid,'operation':op,'target':'fixture','payload_ref':'fixture-payload','parameters':{}}

    def test_simulation_never_returns_host_action(self):
        a = self._action()
        g = _graph(_task(actions=[a]))
        r = autonomy_plan({'graph':g,'mode':'SIMULATE','inventory':_inventory('web.research','search')})
        self.assertEqual(r['status'], 'simulation_ready')
        self.assertEqual(r['host_action_count'], 0)
        self.assertEqual(r['tasks'][0]['actions'][0]['status'], 'simulation_ready')

    def test_read_can_be_prepared_without_approval(self):
        a = self._action()
        g = _graph(_task(actions=[a]))
        r = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':_inventory('web.research','search')})
        self.assertEqual(r['status'], 'host_action_required')
        self.assertEqual(r['host_action_count'], 1)
        self.assertEqual(r['tasks'][0]['actions'][0]['decision_class'], 'autonomous_in_scope')

    def test_send_requires_exact_approval(self):
        a = self._action('email.send','send')
        g = _graph(_task(actions=[a]))
        inv = _inventory('email.send','send')
        blocked = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':inv})
        self.assertEqual(blocked['status'], 'approval_required')
        request = {'scope_id':'scope-a','capability_id':'email.send','operation':'send','target':'fixture','payload_ref':'fixture-payload','parameters':{}}
        approval = {'scope_id':'scope-a','capability_id':'email.send','operation':'send',
                    'action_sha256':action_hash(request),'approval_ref':'explicit-test-approval'}
        allowed = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':inv,'approvals':[approval]})
        self.assertEqual(allowed['status'], 'host_action_required')
        self.assertEqual(allowed['host_action_count'], 1)

    def test_unknown_receipt_requires_reconciliation(self):
        a = self._action()
        g = _graph(_task(actions=[a]))
        request = {'scope_id':'scope-a','capability_id':'web.research','operation':'search','target':'fixture','payload_ref':'fixture-payload','parameters':{}}
        receipt = {'receipt_id':'r','scope_id':'scope-a','capability_id':'web.research','operation':'search',
                   'action_sha256':action_hash(request),'status':'unknown','evidence':[]}
        r = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':_inventory('web.research','search'),'receipts':[receipt]})
        self.assertEqual(r['status'], 'reconcile_required')
        self.assertEqual(r['host_action_count'], 0)

    def test_verified_receipt_closes_task_at_engine_level(self):
        a = self._action()
        g = _graph(_task(actions=[a]))
        request = {'scope_id':'scope-a','capability_id':'web.research','operation':'search','target':'fixture','payload_ref':'fixture-payload','parameters':{}}
        receipt = {'receipt_id':'r','scope_id':'scope-a','capability_id':'web.research','operation':'search',
                   'action_sha256':action_hash(request),'status':'executed','evidence':['provider:test']}
        r = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':_inventory('web.research','search'),'receipts':[receipt]})
        self.assertEqual(r['status'], 'task_verified')
        self.assertEqual(r['tasks'][0]['actions'][0]['status'], 'verified')

    def test_failed_retry_needs_idempotency(self):
        a = self._action()
        a['retry_policy'] = {'max_attempts':1,'retry_on':['failed'],'requires_idempotency_key':True}
        g = _graph(_task(actions=[a]))
        request = {'scope_id':'scope-a','capability_id':'web.research','operation':'search','target':'fixture','payload_ref':'fixture-payload','parameters':{}}
        receipt = {'receipt_id':'r','scope_id':'scope-a','capability_id':'web.research','operation':'search',
                   'action_sha256':action_hash(request),'status':'failed','evidence':[]}
        r = autonomy_plan({'graph':g,'mode':'HOST_EXECUTION','inventory':_inventory('web.research','search'),'receipts':[receipt]})
        self.assertEqual(r['status'], 'manual_recovery')
        self.assertEqual(r['tasks'][0]['actions'][0]['recovery']['reason'], 'idempotency_key_required')

    def test_action_dependency_needs_verified_predecessor(self):
        a1 = self._action(aid='a1')
        a2 = self._action('files.write','create','a2')
        a2['depends_on'] = ['a1']
        g = _graph(_task(actions=[a1,a2]))
        inv = {'capabilities': _inventory('web.research','search')['capabilities'] + _inventory('files.write','create')['capabilities']}
        r = autonomy_plan({'graph':g,'mode':'SIMULATE','inventory':inv})
        self.assertEqual([x['status'] for x in r['tasks'][0]['actions']], ['simulation_ready','blocked_by_action_dependency'])

    def test_action_cycle_rejected(self):
        a1 = self._action(aid='a1'); a1['depends_on']=['a2']
        a2 = self._action('files.write','create','a2'); a2['depends_on']=['a1']
        g = _graph(_task(actions=[a1,a2]))
        with self.assertRaises(ACOError):
            autonomy_plan({'graph':g,'mode':'SIMULATE'})

    def test_packaged_benchmark(self):
        r = autonomy_benchmark()
        self.assertEqual(r['status'], 'passed', [x for x in r['rows'] if not x['passed']])
        self.assertEqual(r['cases'], 29)
        self.assertEqual(r['score'], 100.0)
        self.assertEqual(r['critical_failures'], 0)

    def test_packaged_artist_example(self):
        graph = json.loads((ROOT/'examples/goals/artist-program.json').read_text())
        r = goal_graph_status(graph, as_of='2026-10-06T00:00:00+00:00')
        self.assertEqual(r['status'], 'actionable')
        self.assertEqual(r['next_task_ids'][0], 'task-opportunity-scan')
        self.assertIn('task-followup', r['blocked_task_ids'])


if __name__ == '__main__':
    unittest.main()
