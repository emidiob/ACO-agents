import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project_system', ROOT/'skills/aco-webdesign/scripts/project_system.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class ProjectSystemTests(unittest.TestCase):
    def system(self):
        return {'schema': 1, 'master': {'tokens': {'color': {'ink': '#112233', 'text': '{color.ink}'}, 'space': {'base': '4px', 'gap': 'calc({space.base} * 3)'}}, 'layout': {'columns': 3, 'order': ['a','b']}}, 'pages': {'article': {'tokens': {'color': {'ink': '#334455'}}, 'layout': {'columns': 1, 'order': ['b'], 'hidden': True}}}}
    def test_page_inheritance_references_arrays_and_no_mutation(self):
        doc = self.system(); result = m.resolve(doc, 'article')
        self.assertEqual(result['resolved_tokens']['color.text'], '#334455')
        self.assertEqual(result['resolved_tokens']['space.gap'], 'calc(4px * 3)')
        self.assertEqual(result['effective']['layout']['order'], ['b'])
        self.assertEqual(doc['master']['layout']['order'], ['a','b'])
        self.assertEqual(m.resolve(doc)['resolved_tokens']['color.text'], '#112233')
    def test_deleted_dependency_and_cycle_fail(self):
        doc = self.system();doc['pages']['article']['tokens']['color']['ink'] = None
        self.assertRaisesRegex(ValueError, 'Missing', m.resolve, doc, 'article')
        doc = self.system();doc['master']['tokens']['color']['ink'] = '{color.text}'
        self.assertRaisesRegex(ValueError, 'Cyclic', m.resolve, doc)
    def test_css_escape_and_colliding_names_fail(self):
        for value in ['red; } body {display:none}', 'url(https://example.test)', 'red/*x*/', '\\75rl(x)', '</style>']:
            doc = self.system();doc['master']['tokens']['color']['ink'] = value
            self.assertRaises(ValueError, m.resolve, doc)
        doc = self.system();doc['master']['tokens']['color-ink'] = 'red'
        self.assertRaisesRegex(ValueError, 'collide', m.resolve, doc)
    def test_unknown_page_and_proposal_conversion(self):
        self.assertRaisesRegex(ValueError, 'Unknown page', m.resolve, self.system(), 'absent')
        self.assertIn('--color-ink: #123456', m.resolve(m.from_proposal({'color_tokens': {'ink': '#123456'}}))['css'])
