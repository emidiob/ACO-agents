import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from aco.adaptive import (
    adaptation_propose,
    adaptive_benchmark,
    feedback_append,
    feedback_ledger_check,
    feedback_record_check,
    promotion_check,
    shadow_rank,
)
from aco.common import ACOError, VERSION


def _ledger(scope='scope-a'):
    return {'schema_version': 1, 'ledger_id': 'ledger', 'scope_id': scope, 'records': []}


def _pref(i, value='concise', scope='scope-a'):
    return {'schema_version': 1, 'feedback_id': f'p{i}-{value}', 'scope_id': scope,
            'target_type': 'output_preference', 'target_id': 'style', 'signal': 'preferred',
            'source_ref': f'correction:{i}', 'preference': {'key': 'response_length', 'value': value}}


def _rank(i, direction='prefer', scope='scope-a', weight=1):
    out = {'schema_version': 1, 'feedback_id': f'r{i}-{direction}', 'scope_id': scope,
           'target_type': 'goal_ranking', 'target_id': 'next-best-action',
           'signal': 'outcome_success' if direction == 'prefer' else 'corrected',
           'source_ref': f'run:{i}', 'weight': weight,
           'ranking': {'feature': 'low_context_cost', 'direction': direction}}
    if direction == 'prefer':
        out['evidence_ref'] = f'receipt:{i}'
    return out


def _append(records):
    ledger = _ledger()
    for record in records:
        ledger = feedback_append(ledger, record)['ledger']
    return ledger


def _graph():
    return {'schema_version': 1, 'graph_id': 'g', 'scope_id': 'scope-a', 'nodes': [
        {'id': 'p', 'kind': 'program', 'title': 'Program', 'state': 'active', 'priority': 50, 'effort': 3, 'success_criteria': ['done']},
        {'id': 'g1', 'kind': 'goal', 'title': 'Goal', 'state': 'active', 'parent_id': 'p', 'priority': 50, 'effort': 3, 'success_criteria': ['done']},
        {'id': 'a', 'kind': 'task', 'title': 'Adaptive', 'state': 'active', 'parent_id': 'g1', 'priority': 50, 'effort': 1, 'depends_on': [], 'success_criteria': ['done'], 'adaptive_features': ['low_context_cost']},
        {'id': 'b', 'kind': 'task', 'title': 'Base', 'state': 'active', 'parent_id': 'g1', 'priority': 52, 'effort': 1, 'depends_on': [], 'success_criteria': ['done']},
    ]}


class Adaptive090Tests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(VERSION, '1.0.0')

    def test_hidden_reasoning_rejected(self):
        r = _pref(1); r['hidden_reasoning'] = 'never store this'
        self.assertEqual(feedback_record_check(r)['status'], 'invalid')

    def test_feedback_hash_chain_detects_tamper(self):
        ledger = _append([_pref(1), _pref(2), _pref(3)])
        self.assertEqual(feedback_ledger_check(ledger)['status'], 'valid')
        ledger['records'][0]['preference']['value'] = 'changed'
        self.assertEqual(feedback_ledger_check(ledger)['status'], 'invalid')

    def test_cross_scope_ledger_rejected(self):
        ledger = _append([_pref(1), _pref(2), _pref(3)])
        ledger['records'][1]['scope_id'] = 'other'
        self.assertEqual(feedback_ledger_check(ledger)['status'], 'invalid')

    def test_single_feedback_does_not_become_policy(self):
        r = adaptation_propose({'ledger': _append([_pref(1)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})
        self.assertEqual(r['candidate_count'], 0)

    def test_repeated_preference_proposes_shadow_candidate(self):
        r = adaptation_propose({'ledger': _append([_pref(1), _pref(2), _pref(3)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})
        self.assertEqual(r['candidate_count'], 1)
        self.assertEqual(r['candidates'][0]['state'], 'shadow_only')
        self.assertEqual(r['candidates'][0]['candidate_type'], 'preference_rule')

    def test_ranking_delta_is_bounded(self):
        ledger = _append([_rank(i) for i in range(1, 8)])
        r = adaptation_propose({'ledger': ledger, 'baseline_ref': 'base', 'rollback_ref': 'rollback'})
        self.assertEqual(r['candidates'][0]['delta'], 5)

    def test_shadow_ranking_does_not_mutate_graph(self):
        graph = _graph(); before = copy.deepcopy(graph)
        candidate = adaptation_propose({'ledger': _append([_rank(1), _rank(2), _rank(3)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})['candidates'][0]
        r = shadow_rank({'graph': graph, 'candidates': [candidate], 'limit': 2})
        self.assertTrue(r['ranking_changed'])
        self.assertFalse(r['production_mutated'])
        self.assertEqual(graph, before)

    def test_candidate_for_other_graph_does_not_apply(self):
        candidate = adaptation_propose({'ledger': _append([_rank(1), _rank(2), _rank(3)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})['candidates'][0]
        # Rebuild a valid candidate for a graph-specific target that does not match this graph.
        candidate['target_id'] = 'another-graph'
        from aco.adaptive import _candidate_hash
        candidate['candidate_sha256'] = _candidate_hash(candidate)
        r = shadow_rank({'graph': _graph(), 'candidates': [candidate], 'limit': 2})
        self.assertFalse(r['ranking_changed'])
        self.assertEqual([x['adaptive_delta'] for x in r['shadow_tasks']], [0, 0])

    def test_cross_scope_candidate_fails_closed(self):
        candidate = adaptation_propose({'ledger': _append([_rank(1), _rank(2), _rank(3)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})['candidates'][0]
        candidate['scope_id'] = 'other'
        with self.assertRaises(ACOError):
            shadow_rank({'graph': _graph(), 'candidates': [candidate]})

    def test_promotion_requires_exact_approval_and_benchmark(self):
        candidate = adaptation_propose({'ledger': _append([_rank(1), _rank(2), _rank(3)]), 'baseline_ref': 'base', 'rollback_ref': 'rollback'})['candidates'][0]
        bench = {'candidate_sha256': candidate['candidate_sha256'], 'scope_id': 'scope-a', 'cases': 30,
                 'score': 100.0, 'critical_failures': 0, 'historical_regressions_passed': True,
                 'frozen_before_first_run': True}
        blocked = promotion_check({'candidate': candidate, 'benchmark': bench,
                                   'approval': {'approved': False, 'candidate_sha256': candidate['candidate_sha256'], 'approval_ref': 'no'}})
        self.assertFalse(blocked['eligible'])
        allowed = promotion_check({'candidate': candidate, 'benchmark': bench,
                                   'approval': {'approved': True, 'candidate_sha256': candidate['candidate_sha256'], 'approval_ref': 'maintainer'}})
        self.assertTrue(allowed['eligible'])
        self.assertFalse(allowed['execute'])

    def test_packaged_benchmark(self):
        r = adaptive_benchmark()
        self.assertEqual(r['status'], 'passed', [x for x in r['rows'] if not x['passed']])
        self.assertEqual(r['cases'], 32)
        self.assertEqual(r['score'], 100.0)
        self.assertEqual(r['critical_failures'], 0)


if __name__ == '__main__':
    unittest.main()
