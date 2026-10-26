"""Command aliases may extend discovery without masking historical routing changes."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.aco.common import ROOT
from scripts.aco.validate import _routing_catalog_sha

class RoutingFreezeTests(unittest.TestCase):
    def test_only_known_alias_metadata_is_excluded(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        expected = json.loads((ROOT / 'release/v073-routing-semantic-freeze.json').read_text())['catalog_semantic_sha256']
        self.assertEqual(_routing_catalog_sha(ROOT / 'catalog.json'), expected)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'catalog.json'
            for mutation in ('role', 'office', 'unknown_skill', 'wrong_count', 'removed_skill'):
                data = copy.deepcopy(catalog)
                if mutation == 'role':
                    data['agents'][next(iter(data['agents']))]['description'] = 'changed routing'
                elif mutation == 'office':
                    data['offices'][next(iter(data['offices']))]['lead'] = 'changed_lead'
                elif mutation == 'unknown_skill':
                    data['skills'].append('aco-unknown'); data['skill_count'] += 1
                elif mutation == 'wrong_count':
                    data['skill_count'] += 1
                else:
                    data['skills'].remove('aco-office-concierge'); data['skill_count'] -= 1
                path.write_text(json.dumps(data))
                with self.subTest(mutation=mutation):
                    self.assertNotEqual(_routing_catalog_sha(path), expected)
