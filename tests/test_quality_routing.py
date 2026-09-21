import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from aco.common import ROOT
from aco.quality import capability_resolve, handoff_check, score_simulation
from aco.routing import role_contract, role_overlap, route_benchmark, suggest_route


class RoutingQualityTests(unittest.TestCase):
    def test_role_contracts_cover_catalog(self):
        contracts = json.loads((ROOT / 'config/role-contracts.json').read_text())
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        self.assertEqual(contracts['aco_version'], '0.7.0')
        self.assertEqual(set(contracts['roles']), set(catalog['agents']))
        self.assertEqual(len(contracts['roles']), 363)
        for key, contract in contracts['roles'].items():
            self.assertEqual(contract['office'], catalog['agents'][key]['office'])
            self.assertTrue(contract['purpose'])
            self.assertIn('use_when', contract)
            self.assertIn('verification', contract)

    def test_final_holdout_is_excluded_from_examples(self):
        examples = json.loads((ROOT / 'config/routing-examples.json').read_text())
        self.assertEqual(examples['aco_version'], '0.7.0')
        self.assertGreaterEqual(len(examples['examples']), 500)
        source_names = set(examples['source_files'])
        self.assertNotIn('routing-final-holdout.json', source_names)
        holdout_prompts = {c['prompt'] for c in json.loads((ROOT / 'config/routing-final-holdout.json').read_text())['cases']}
        trained_prompts = {x['prompt'] for x in examples['examples']}
        self.assertFalse(holdout_prompts & trained_prompts)

    def test_final_routing_gate_passes(self):
        result = route_benchmark(ROOT / 'config/routing-final-holdout.json')
        self.assertEqual(result['status'], 'passed')
        self.assertGreaterEqual(result['score'], 90.0)
        self.assertGreaterEqual(result['office_accuracy'], 0.90)
        self.assertGreaterEqual(result['top1_role_accuracy'], 0.85)
        self.assertGreaterEqual(result['top3_role_recall'], 0.95)
        self.assertLessEqual(result['overstaff_rate'], 0.05)
        self.assertEqual(result['critical_failures'], 0)

    def test_ambiguous_request_uses_concierge(self):
        result = suggest_route('There is not enough information to know which office should handle this.')
        self.assertEqual(result['status'], 'needs_clarification')
        self.assertEqual(result['office'], 'shared')
        self.assertEqual(result['selected_roles'], ['office_concierge'])

    def test_role_contract_lookup(self):
        result = role_contract('curator')
        self.assertEqual(result['status'], 'found')
        self.assertEqual(result['contract']['office'], 'artist-office')
        self.assertIn('curator', result['contract']['purpose'].lower())

    def test_overlap_scan_is_advisory_and_read_only(self):
        before = (ROOT / 'config/role-contracts.json').read_bytes()
        result = role_overlap(threshold=0.50, limit=10)
        after = (ROOT / 'config/role-contracts.json').read_bytes()
        self.assertEqual(before, after)
        self.assertIn(result['status'], ('clean', 'review_candidates'))
        self.assertIn('Never merge or retire roles automatically', result['policy'])

    def test_handoff_requires_evidence_when_checked(self):
        packet = {
            'task': 'Synthetic task', 'owner': 'project_manager', 'status': 'checked',
            'decisions': [], 'evidence': [], 'unknowns': [], 'next_action': 'Review'
        }
        result = handoff_check(packet)
        self.assertEqual(result['status'], 'invalid')
        self.assertTrue(any('require evidence' in e for e in result['errors']))

    def test_handoff_valid_compact_packet(self):
        packet = {
            'task': 'Synthetic task', 'owner': 'project_manager', 'status': 'prepared',
            'decisions': ['Use approved scope'], 'evidence': [],
            'unknowns': ['Final delivery date'], 'next_action': 'Resolve date'
        }
        result = handoff_check(packet)
        self.assertEqual(result['status'], 'valid')

    def test_capability_states_are_separate(self):
        request = {'required': ['send_email'], 'optional': ['render_video'], 'fallback': 'Return drafts only.'}
        inventory = {'capabilities': [
            {'id': 'send_email', 'available': True, 'authorized': False, 'verified': True},
            {'id': 'render_video', 'available': True, 'authorized': True, 'verified': False}
        ]}
        result = capability_resolve(request, inventory)
        self.assertEqual(result['status'], 'fallback_required')
        self.assertEqual(result['required'][0]['state'], 'available_not_authorized')
        self.assertEqual(result['optional'][0]['state'], 'authorized_unverified')

    def test_behavioral_simulation_gate_passes(self):
        result = score_simulation(ROOT / 'release/behavioral-simulation.json')
        self.assertEqual(result['status'], 'passed')
        self.assertGreaterEqual(result['score'], 90.0)
        self.assertEqual(result['critical_failures'], 0)
        self.assertIn('same-model', result['review_mode'])

    def test_bad_simulation_score_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad.json'
            p.write_text(json.dumps({
                'schema_version': 1,
                'dimensions': ['x'],
                'cases': [{'id': 'bad', 'scores': {'x': 6}}]
            }))
            with self.assertRaises(Exception):
                score_simulation(p)


if __name__ == '__main__':
    unittest.main()
