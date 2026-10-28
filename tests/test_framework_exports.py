import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'skills/aco-webdesign/scripts'/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
class FrameworkExports(unittest.TestCase):
    def test_bridge_export_is_complete_and_collision_safe(self):
        module=load('framework_live')
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp).resolve()/'bridge';module.export(out);self.assertTrue((out/'aco-vite.mjs').is_file());self.assertTrue((out/'editor.html').is_file());self.assertTrue((out/'client.js').is_file());self.assertRaises(ValueError,module.export,out)
    def test_both_component_formats_and_invalid_framework(self):
        module=load('framework_components')
        with tempfile.TemporaryDirectory() as tmp:
            for framework,suffix in [('react','.jsx'),('vue','.mjs')]:
                out=Path(tmp).resolve()/framework;module.export(out,framework);self.assertTrue((out/('aco-components'+suffix)).is_file());self.assertTrue((out/'aco.css').is_file());self.assertRaises(ValueError,module.export,out,framework)
            self.assertRaises(ValueError,module.export,Path(tmp).resolve()/'invalid','missing')
