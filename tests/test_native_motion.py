"""Native motion methods remain usable in an ACO-only installation."""
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.aco.common import ROOT

class NativeMotionTests(unittest.TestCase):
    def test_offline_method_links_resolve_without_external_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            # This fixture deliberately contains no third-party skill directories.
            shutil.copytree(ROOT/'skills/aco-motion', root/'aco-motion')
            for rel in ('aco-genjutsu/SKILL.md',
                        'aco-office-concierge/references/protocols/COMPACT-MEMORY.md'):
                dest = root/rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/'skills'/rel, dest)
            reached = set()
            queue = [root/'aco-motion/SKILL.md']
            while queue:
                path = queue.pop()
                if path in reached:
                    continue
                reached.add(path)
                for target in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
                    if '://' in target or target.startswith('#'):
                        continue
                    resolved = (path.parent/target.split('#')[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(root), target)
                    self.assertTrue(resolved.is_file(), target)
                    if resolved.is_relative_to(root/'aco-motion'):
                        queue.append(resolved)
            expected = set((root/'aco-motion/references').glob('*.md'))
            self.assertTrue(expected.issubset(reached), expected-reached)
            self.assertGreaterEqual(len(expected), 11)

    def test_each_dispatch_row_points_to_a_local_method(self):
        path = ROOT/'skills/aco-motion/SKILL.md'
        rows = [row for row in path.read_text().splitlines()
                if row.startswith('| `')]
        self.assertEqual(len(rows), 10)
        for row in rows:
            link = re.search(r'\]\((references/[^)]+)\)', row)
            self.assertIsNotNone(link, row)
            self.assertTrue((path.parent/link.group(1)).is_file())
