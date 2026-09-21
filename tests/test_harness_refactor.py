import json
import tempfile
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))

from aco.harness import context_budget, role_stocktake, eval_lint, eval_show
from aco.common import ROOT


class HarnessRefactorTests(unittest.TestCase):
    def test_all_roles_use_compact_bootstrap(self):
        roles=list((ROOT/'skills').glob('*/references/agents/*.md'))
        self.assertEqual(len(roles),363)
        total=0
        for p in roles:
            text=p.read_text()
            total += len(text)
            self.assertIn('ACO ROLE BOOTSTRAP',text,p)
            self.assertNotIn('INTERACTION AND ACTION CONTRACT',text,p)
            self.assertNotIn('ACO OPERATING CONTRACT — applies to every role',text,p)
            self.assertNotIn('Compact storage and optional resources — v0.5.1',text,p)
        self.assertLess(total,1_900_000)

    def test_shared_protocols_exist(self):
        d=ROOT/'skills/aco-office-concierge/references/protocols'
        for name in ('OPERATING-CONTRACT.md','CONTEXT-RETRIEVAL.md','VERIFICATION.md','PLANNING-AND-APPROVAL.md','LEARNING-AND-SCOPE.md','ROLE-MAINTENANCE.md'):
            self.assertTrue((d/name).is_file(),name)

    def test_context_budget(self):
        r=context_budget(ROOT)
        self.assertEqual(r['roles']['count'],363)
        self.assertEqual(r['roles']['shared_bootstrap_copies'],363)
        self.assertGreater(r['roles']['package_duplicate_bootstrap_chars'],0)
        self.assertIn('not equal to active context',r['roles']['note'])

    def test_role_stocktake_never_mutates(self):
        before=(ROOT/'skills/aco-artist-office/references/agents/curator.md').read_bytes()
        r=role_stocktake(ROOT)
        after=(ROOT/'skills/aco-artist-office/references/agents/curator.md').read_bytes()
        self.assertEqual(before,after)
        self.assertEqual(r['roles_scanned'],363)
        self.assertIn(r['status'],('clean','review_required'))

    def test_eval_definitions(self):
        p=ROOT/'config/evals.json'
        r=eval_lint(p)
        self.assertEqual(r['cases'],18)
        artist=eval_show(p,'artist-office')
        self.assertGreaterEqual(len(artist['cases']),2)
        self.assertTrue(any(c['id']=='artist-rejected-application' for c in artist['cases']))

    def test_invalid_eval_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bad.json'
            p.write_text(json.dumps({'schema_version':1,'cases':[{'id':'X'}]}))
            with self.assertRaises(Exception): eval_lint(p)


if __name__=='__main__': unittest.main()
