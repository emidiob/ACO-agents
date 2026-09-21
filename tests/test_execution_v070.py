import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from aco.common import ROOT
from aco.execution import (
    action_hash, adapter_check, capability_state, execution_benchmark, execution_plan,
    execution_summary, permission_check, receipt_check, workflow_check,
)


def ready_inventory(cid, operation, state='CONNECTED_INTEGRATION'):
    return {'capabilities': [{
        'id': cid, 'resource_state': state, 'operations': [operation],
        'available': True, 'authorized': True, 'verified': True,
        'evidence_ref': 'test-capability-evidence', 'adapter_id': 'test-adapter'
    }]}


def approval_for(request):
    return {
        'scope_id': request['scope_id'], 'capability_id': request['capability_id'],
        'operation': request['operation'], 'action_sha256': action_hash(request),
        'approval_ref': 'test-explicit-approval'
    }


class ExecutionV070Tests(unittest.TestCase):
    def test_capability_model_has_formal_states(self):
        data = json.loads((ROOT / 'config/capabilities.json').read_text())
        self.assertEqual(data['aco_version'], '0.7.0')
        for state in ('LEARNED_SKILL','REFERENCE','OPTIONAL_TOOL','CONNECTED_INTEGRATION','LOCAL_RUNTIME','UNAVAILABLE','BLOCKED'):
            self.assertIn(state, data['states'])
        self.assertGreaterEqual(len(data['capabilities']), 30)

    def test_send_requires_packet_bound_approval(self):
        req = {'scope_id':'s','capability_id':'email.send','operation':'send','target':'a@example.com','payload_ref':'draft-1'}
        denied = permission_check(req)
        self.assertFalse(denied['allowed'])
        self.assertTrue(denied['approval_required'])
        allowed = permission_check(req, approval_for(req))
        self.assertTrue(allowed['allowed'])
        self.assertEqual(allowed['permission'], 'SEND')

    def test_write_does_not_add_repetitive_approval_gate(self):
        req = {'scope_id':'s','capability_id':'files.write','operation':'create','target':'out.txt','payload_ref':'artifact-1'}
        result = permission_check(req)
        self.assertTrue(result['allowed'])
        self.assertFalse(result['approval_required'])

    def test_execution_plan_never_executes(self):
        req = {'scope_id':'s','capability_id':'email.send','operation':'send','target':'a@example.com','payload_ref':'draft-1'}
        result = execution_plan(req, ready_inventory('email.send','send'), approval_for(req))
        self.assertEqual(result['status'], 'ready_to_execute')
        self.assertFalse(result['execute'])

    def test_optional_tool_is_not_capability(self):
        req = {'scope_id':'s','capability_id':'email.send','operation':'send','target':'a@example.com','payload_ref':'draft-1'}
        inv = {'capabilities':[{'id':'email.send','resource_state':'OPTIONAL_TOOL','operations':['send'],'available':True,'authorized':True,'verified':True,'evidence_ref':'x'}]}
        result = execution_plan(req, inv, approval_for(req))
        self.assertEqual(result['status'], 'fallback_required')
        self.assertEqual(result['capability']['state'], 'not_installed_or_connected')

    def test_learned_skill_does_not_claim_external_execution(self):
        result = capability_state('social.draft','draft',ready_inventory('social.draft','draft','LEARNED_SKILL'))
        self.assertFalse(result['ready'])
        self.assertEqual(result['state'], 'knowledge_only')

    def test_unknown_previous_action_blocks_retry(self):
        req = {'scope_id':'s','capability_id':'email.send','operation':'send','target':'a@example.com','payload_ref':'draft-1'}
        receipt = {'receipt_id':'r1','scope_id':'s','capability_id':'email.send','operation':'send','action_sha256':action_hash(req),'status':'unknown','evidence':[]}
        result = execution_plan(req, ready_inventory('email.send','send'), approval_for(req), receipt)
        self.assertEqual(result['status'], 'reconcile_required')

    def test_confirmed_previous_action_blocks_duplicate(self):
        req = {'scope_id':'s','capability_id':'email.send','operation':'send','target':'a@example.com','payload_ref':'draft-1'}
        receipt = {'receipt_id':'r1','scope_id':'s','capability_id':'email.send','operation':'send','action_sha256':action_hash(req),'status':'sent','adapter_id':'mail','provider_ref':'msg-1','evidence':['provider receipt']}
        result = execution_plan(req, ready_inventory('email.send','send'), approval_for(req), receipt)
        self.assertEqual(result['status'], 'already_executed')

    def test_receipt_does_not_allow_fictional_sent_state(self):
        receipt = {'receipt_id':'r1','scope_id':'s','capability_id':'email.send','operation':'send','action_sha256':'a'*64,'status':'sent','evidence':[]}
        result = receipt_check(receipt)
        self.assertEqual(result['status'], 'invalid')
        self.assertTrue(any('evidence' in x.lower() for x in result['errors']))

    def test_receipt_preserves_delivery_distinction(self):
        receipt = {'receipt_id':'r1','scope_id':'s','capability_id':'email.send','operation':'send','action_sha256':'a'*64,'status':'delivered','adapter_id':'mail','provider_ref':'delivery-1','evidence':['delivery receipt']}
        result = receipt_check(receipt)
        self.assertEqual(result['status'], 'valid')
        self.assertEqual(result['verified_claim_level'], 'provider_delivered')

    def test_adapter_inventory_rejects_embedded_credentials_claim(self):
        result = adapter_check({'adapters':[{'id':'x','kind':'api','capabilities':['email.send'],'verified':True,'evidence_ref':'schema','credentials_embedded':True}]})
        self.assertEqual(result['status'], 'invalid')

    def test_adapter_inventory_accepts_verified_metadata(self):
        result = adapter_check({'adapters':[{'id':'mail','kind':'connected_integration','capabilities':['email.read','email.send'],'verified':True,'evidence_ref':'host-schema','credentials_embedded':False}]})
        self.assertEqual(result['status'], 'valid')

    def test_workflow_unknown_requires_reconciliation(self):
        packet = {'history':[
            {'state':'proposed'}, {'state':'prepared'}, {'state':'approved'},
            {'state':'executing'}, {'state':'unknown'},
            {'state':'executed','evidence_ref':'provider'}
        ]}
        result = workflow_check(packet)
        self.assertEqual(result['status'], 'invalid')
        self.assertTrue(any('reconciled' in x for x in result['errors']))

    def test_workflow_reconciles_before_execution(self):
        packet = {'history':[
            {'state':'proposed'}, {'state':'prepared'}, {'state':'approved'},
            {'state':'executing'}, {'state':'unknown'},
            {'state':'reconciled','evidence_ref':'provider lookup'},
            {'state':'executed','evidence_ref':'provider receipt'},
            {'state':'checked','evidence_ref':'readback'},
            {'state':'closed','evidence_ref':'final verification'}
        ]}
        result = workflow_check(packet)
        self.assertEqual(result['status'], 'valid')
        self.assertEqual(result['current_state'], 'closed')

    def test_execution_summary_is_operational_not_reasoning(self):
        receipt = {'receipt_id':'r1','scope_id':'s','capability_id':'files.write','operation':'create','action_sha256':'a'*64,'status':'created','adapter_id':'local','artifact_ref':'/tmp/out','evidence':['sha256']}
        result = execution_summary({'task':'make file','scope_id':'s','receipts':[receipt],'checks':['hash verified'],'next_action':'review'})
        self.assertEqual(result['unresolved_receipts'], [])
        self.assertIn('no hidden reasoning', result['policy'])

    def test_execution_benchmark_passes(self):
        result = execution_benchmark(ROOT / 'config/execution-benchmark.json')
        self.assertEqual(result['status'], 'passed')
        self.assertGreaterEqual(result['cases'], 60)
        self.assertGreaterEqual(result['score'], 98)
        self.assertEqual(result['critical_failures'], 0)


if __name__ == '__main__':
    unittest.main()
