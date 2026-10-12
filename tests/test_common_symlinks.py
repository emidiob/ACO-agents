import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / 'scripts')
)

from aco.common import ACOError, no_symlinks, read_json, write_json


class SymlinkTests(unittest.TestCase):
    def test_regular_and_missing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            no_symlinks(root)
            no_symlinks(root / 'missing' / 'file.json')

    def test_malicious_components_and_dangling_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            outside = root / 'outside'
            outside.mkdir()
            (outside / 'data.json').write_text('{"keep": true}')
            (root / 'directory-link').symlink_to(
                outside, target_is_directory=True
            )
            (root / 'leaf-link').symlink_to(outside / 'data.json')
            (root / 'dangling-link').symlink_to(root / 'missing')

            for path in (
                root / 'directory-link' / 'data.json',
                root / 'leaf-link',
                root / 'dangling-link',
            ):
                with self.subTest(path=path):
                    with self.assertRaises(ACOError):
                        no_symlinks(path)
                    with self.assertRaises(ACOError):
                        write_json(path, {"changed": True})

            self.assertEqual(
                read_json(outside / 'data.json'), {"keep": True}
            )

    def test_parent_traversal_cannot_hide_a_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'link').symlink_to(root, target_is_directory=True)
            with self.assertRaises(ACOError):
                no_symlinks(root / 'link' / '..' / 'data.json')

    def test_system_alias_name_is_not_allowed_on_linux(self):
        original = Path.is_symlink

        def is_symlink(path):
            return path == Path('/var') or original(path)

        with patch('aco.common.sys.platform', 'linux'):
            with patch.object(Path, 'is_symlink', is_symlink):
                with self.assertRaises(ACOError):
                    no_symlinks(Path('/var/aco-regression.json'))

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS aliases')
    def test_real_system_aliases_and_nested_malicious_links(self):
        for alias in ('/var', '/tmp', '/etc'):
            with self.subTest(alias=alias):
                no_symlinks(Path(alias))

        with tempfile.TemporaryDirectory(dir='/var/tmp') as directory:
            root = Path(directory)
            path = root / 'data.json'
            write_json(path, {"ok": True})
            self.assertEqual(read_json(path), {"ok": True})

            (root / 'link').symlink_to(
                root.resolve(), target_is_directory=True
            )
            with self.assertRaises(ACOError):
                no_symlinks(root / 'link' / 'data.json')

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS aliases')
    def test_retargeted_system_alias_is_rejected(self):
        original = __import__('os').readlink

        def readlink(path, *args, **kwargs):
            if Path(path) == Path('/var'):
                return '/private/tmp'
            return original(path, *args, **kwargs)

        with patch('aco.common.os.readlink', readlink):
            with self.assertRaises(ACOError):
                no_symlinks(Path('/var/aco-regression.json'))


if __name__ == '__main__':
    unittest.main()
