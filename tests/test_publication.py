from pathlib import Path
import tempfile
import unittest
from scripts.publication_check import check

class PublicationTests(unittest.TestCase):
    def test_internal_material_rejected_and_runtime_sources_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('README.md','LICENSE','tests/test_runtime.py','skills/example/references/research-method.md'):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('public source')
            self.assertEqual(check(root)['status'],'passed')
            for name in ('research/comparison.json','docs/TEST-REPORT-1.md','skills/example/references/feature-parity.json'):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('internal')
            self.assertEqual(len(check(root)['internal_documents']),3)
    def test_public_checkout(self):
        self.assertEqual(check(Path(__file__).resolve().parents[1])['status'],'passed')
