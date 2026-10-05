import json
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aco.common import ROOT
from aco.delegation import resolve_delegation, delegation_benchmark
from aco.hybrid import memory_resolve
from aco.integrations import integration_resolve, integration_benchmark
from aco.privacy import privacy_scan


class Delegation071Tests(unittest.TestCase):
    def test_delegated_reversible_judgment_decides(self):
        r=resolve_delegation({'delegated':True,'within_role':True,'evidence_sufficient':True,'reversible':True})
        self.assertEqual(r['action'],'DECIDE_AND_ACT')

    def test_consequential_action_recommends_then_approval(self):
        r=resolve_delegation({'delegated':True,'within_role':True,'evidence_sufficient':True,'reversible':False,'consequential_authorization':True})
        self.assertEqual(r['action'],'RECOMMEND_AND_REQUEST_APPROVAL')

    def test_decisive_missing_fact_asks(self):
        r=resolve_delegation({'delegated':True,'within_role':True,'evidence_sufficient':False,'reversible':True,'missing_fact_decisive':True})
        self.assertEqual(r['action'],'ASK_DECISIVE_FACT')

    def test_scope_ambiguity_clarifies(self):
        r=resolve_delegation({'delegated':True,'within_role':True,'evidence_sufficient':False,'scope_ambiguous_material':True,'reversible':False})
        self.assertEqual(r['action'],'CLARIFY_SCOPE')

    def test_delegation_benchmark(self):
        r=delegation_benchmark()
        self.assertEqual(r['status'],'passed')
        self.assertEqual(r['score'],100.0)
        self.assertEqual(r['critical_failures'],0)


class HybridMemory071Tests(unittest.TestCase):
    def test_no_drive_prompt_when_store_missing(self):
        r=memory_resolve({'memory_class':'durable_context','persistent_store_available':False,'material_change':True})
        self.assertFalse(r['prompt_for_drive'])
        self.assertEqual(r['status'],'continue_without_persistence')
        self.assertIsNone(r['notice'])

    def test_explicit_save_reports_unavailable_without_prompt(self):
        r=memory_resolve({'memory_class':'durable_context','persistent_store_available':False,'material_change':True,'explicit_persistence_request':True})
        self.assertFalse(r['prompt_for_drive'])
        self.assertIn('unavailable',r['notice'].lower())

    def test_code_structure_never_routes_to_drive(self):
        r=memory_resolve({'memory_class':'code_structure','persistent_store_available':True,'code_index_available':True,'material_change':True})
        self.assertEqual(r['destinations'],['local_code_intelligence'])
        self.assertNotIn('canonical_aco_document',r['destinations'])

    def test_code_architecture_can_add_compact_summary(self):
        r=memory_resolve({'memory_class':'code_architecture','persistent_store_available':True,'code_index_available':True,'material_change':True})
        self.assertEqual(r['destinations'][0],'repository_current_source')
        self.assertIn('local_code_intelligence',r['destinations'])
        self.assertIn('canonical_aco_document_summary',r['destinations'])


class Integration071Tests(unittest.TestCase):
    def test_ready_adapter_selected(self):
        req={'capability_id':'email.send','operation':'send'}
        inv={'adapters':[{'id':'gmail','kind':'connected_integration','capabilities':['email.send'],'available':True,'connected':True,'authorized_operations':['send'],'verified':True}]}
        r=integration_resolve(req,inv)
        self.assertEqual(r['status'],'ready')
        self.assertEqual(r['selected']['id'],'gmail')

    def test_documented_but_not_connected_is_not_ready(self):
        req={'capability_id':'email.send','operation':'send'}
        inv={'adapters':[{'id':'gmail','kind':'connected_integration','capabilities':['email.send'],'available':True,'connected':False,'authorized_operations':['send'],'verified':True}]}
        self.assertEqual(integration_resolve(req,inv)['status'],'fallback_required')

    def test_explicit_blocked_provider_not_silently_switched(self):
        req={'capability_id':'email.send','operation':'send','preferred_adapter_id':'a'}
        inv={'adapters':[
            {'id':'a','kind':'connected_integration','capabilities':['email.send'],'available':True,'connected':False,'authorized_operations':['send'],'verified':True},
            {'id':'b','kind':'mcp','capabilities':['email.send'],'available':True,'connected':True,'authorized_operations':['send'],'verified':True}
        ]}
        r=integration_resolve(req,inv)
        self.assertEqual(r['status'],'fallback_required')
        self.assertIsNone(r['selected'])

    def test_local_runtime_does_not_need_connected_flag(self):
        req={'capability_id':'code.intelligence.query','operation':'query'}
        inv={'adapters':[{'id':'cbm','kind':'local_runtime','capabilities':['code.intelligence.query'],'available':True,'connected':False,'authorized_operations':['query'],'verified':True}]}
        self.assertEqual(integration_resolve(req,inv)['status'],'ready')

    def test_integration_benchmark(self):
        r=integration_benchmark()
        self.assertEqual(r['status'],'passed')
        self.assertEqual(r['score'],100.0)
        self.assertEqual(r['critical_failures'],0)


class Privacy071Tests(unittest.TestCase):
    def policy(self, root: Path):
        (root/'config').mkdir(parents=True,exist_ok=True)
        (root/'config/privacy-policy.json').write_text(json.dumps({
            'schema_version':1,'aco_version':'0.7.1',
            'canonical_public_repository':'example/repo',
            'owner_name_allowed_paths':['LICENSE'],
            'example_domains':['example.com','example.org','example.net','example.invalid'],
            'allowed_local_hosts':['127.0.0.1','localhost']
        }))
        (root/'LICENSE').write_text('Copyright © 2026 Public Owner. All rights reserved.')

    def test_example_fixtures_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.policy(root)
            (root/'fixture.md').write_text('recipient@example.invalid https://example.org')
            self.assertEqual(privacy_scan(root)['status'],'passed')

    def test_real_email_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.policy(root)
            (root/'private.md').write_text('Contact '+'real.person'+'@'+'private-domain.test')
            r=privacy_scan(root)
            self.assertEqual(r['status'],'failed')
            self.assertIn('email',{x['type'] for x in r['findings']})

    def test_home_path_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.policy(root)
            (root/'private.md').write_text('/Users/'+'alice'+'/Secret/file.txt')
            r=privacy_scan(root)
            self.assertIn('local_user_path',{x['type'] for x in r['findings']})

    def test_owner_only_allowed_in_license(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.policy(root)
            (root/'readme.md').write_text('Public Owner')
            r=privacy_scan(root)
            self.assertIn('public_owner_outside_allowed_path',{x['type'] for x in r['findings']})

    def test_current_release_has_no_version_specific_migration_prompt(self):
        self.assertFalse((ROOT/'docs/CODEX-MIGRATION-PROMPT.txt').exists())
        self.assertTrue((ROOT/'docs/UPGRADING.md').exists())

    def test_current_release_privacy_scan(self):
        r=privacy_scan(ROOT)
        self.assertEqual(r['status'],'passed',r['findings'])


class Content071Tests(unittest.TestCase):
    def test_no_old_drive_invitation_in_concierge(self):
        for rel in [
            'skills/aco-office-concierge/references/agents/office-concierge.md',
            'skills/aco-office-concierge/references/protocols/CONCIERGE.md']:
            text=(ROOT/rel).read_text()
            self.assertNotIn('You can also connect Google Drive separately',text)
            self.assertIn('Do not proactively invite the user to connect Drive',text)

    def test_delegation_protocol_linked(self):
        self.assertTrue((ROOT/'skills/aco-office-concierge/references/protocols/DELEGATION.md').is_file())
        self.assertIn('resolve it within the role', (ROOT/'skills/aco-office-concierge/references/agents/office-concierge.md').read_text())

    def test_code_memory_resources_present(self):
        d=json.loads((ROOT/'skills/aco-office-concierge/references/resources/REGISTRY.json').read_text())
        ids={x['id'] for x in d['resources']}
        self.assertIn('codebase-memory-yuga',ids)
        self.assertIn('codebase-memory-deusdata',ids)
        self.assertEqual(len(d['resources']),99)


if __name__=='__main__': unittest.main()
