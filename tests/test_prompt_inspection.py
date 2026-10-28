import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('aco_inspection', ROOT / 'skills/aco-genjutsu/scripts/inspect_video.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'optional local media tools unavailable')
class MediaInspectionTests(unittest.TestCase):
    def test_extracts_frames_without_mutating_source_and_rejects_bad_requests(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source.mkv'
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi', '-i',
                            'testsrc2=size=96x64:rate=10:duration=1', '-c:v', 'ffv1',
                            str(source)], check=True)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            result = helper.inspect(source, root / 'frames', [0, .4, .8])
            self.assertEqual(result['status'], 'extracted')
            self.assertEqual((result['width'], result['height']), (96, 64))
            self.assertFalse(result['audio_reviewed'])
            self.assertEqual(len(result['frames']), 3)
            for frame in result['frames']:
                self.assertTrue((root / 'frames' / frame['file']).read_bytes().startswith(b'\x89PNG'))
            saved = (root / 'frames/inspection.json').read_bytes()
            with self.assertRaises(ValueError):
                helper.inspect(source, root / 'frames', [0])
            self.assertEqual((root / 'frames/inspection.json').read_bytes(), saved)
            for invalid in [-1, 1, float('nan'), float('inf')]:
                with self.subTest(time=invalid), self.assertRaises(ValueError):
                    helper.inspect(source, root / 'invalid', [invalid])
                self.assertFalse((root / 'invalid').exists())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)

    def test_default_overview_endpoints_and_real_cut(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'cut.mkv'
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi', '-i',
                'color=black:size=96x64:rate=10:duration=1', '-f', 'lavfi', '-i',
                'color=white:size=96x64:rate=10:duration=1', '-filter_complex',
                '[0:v][1:v]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-c:v', 'ffv1', str(source)], check=True)
            result = helper.inspect(source, root / 'frames')
            self.assertEqual(result['frames'][0]['frame_number'], 0)
            self.assertEqual(result['frames'][-1]['frame_number'], 19)
            self.assertAlmostEqual(result['frames'][-1]['source_time_seconds'], 1.9)
            self.assertTrue(any(abs(t-1) < .05 for t in result['cut_candidates_seconds']))
            self.assertTrue((root / 'frames/references.jpg').stat().st_size)
            self.assertTrue((root / 'frames/overview/contact-sheet.jpg').stat().st_size)
            self.assertEqual(result['overview'][-1]['frame_number'], 19)
            bindings = json.loads((root / 'frames/reference-map.json').read_text())
            self.assertTrue(all(r['visually_reviewed'] is False for r in bindings['references']))

class ReferencePacketTests(unittest.TestCase):
    def test_incomplete_and_changed_packets_are_rejected(self):
        spec = importlib.util.spec_from_file_location('aco_pack', ROOT / 'skills/aco-genjutsu/scripts/check_reference_pack.py')
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'frame.png').write_bytes(b'fixture image bytes')
            ref = {'file': 'frame.png', 'source_time_seconds': 0, 'sha256': hashlib.sha256(b'fixture image bytes').hexdigest(),
                   'type': 'extracted_original', 'purpose': 'opening grip', 'visually_reviewed': False}
            data = {'intent': 'unchanged recreation', 'references': [ref]}
            def save():
                (root / 'reference-map.json').write_text(json.dumps(data))
            save()
            self.assertEqual(checker.check(root)['status'], 'incomplete')
            (root / 'shot-prompt.txt').write_text('Use frame.png at 0 s for the initial grip.')
            ref['visually_reviewed'] = True
            save()
            plan = {'source_duration_seconds': 1, 'target_duration_seconds': 1,
                    'reviewed_intervals': [[0, 1]], 'entities': {'hand': 'same hand', 'camera': 'same camera'},
                    'events': [{'id': track, 'actor': actor, 'track': track, 'source_interval': [0, 1],
                                'target_interval': [0, 1], 'observed': 'Holds still', 'target_action': 'Holds still',
                                'certainty': 'observed', 'evidence': ['frame.png'],
                                'prompt_excerpt': 'initial grip'} for track, actor in [('subject', 'hand'), ('camera', 'camera')]]}
            (root / 'motion-plan.json').write_text(json.dumps(plan))
            self.assertEqual(checker.check(root)['status'], 'reference_packet_consistent')
            (root / 'shot-prompt.txt').write_text('Use frame.png at 10 s for the initial grip.')
            self.assertEqual(checker.check(root)['status'], 'incomplete')
            (root / 'shot-prompt.txt').write_text('Use frame.png at 0 s for the initial grip.')
            (root / 'frame.png').write_bytes(b'changed')
            self.assertEqual(checker.check(root)['status'], 'incomplete')
            (root / 'frame.png').write_bytes(b'fixture image bytes')
            data['intent'] = 'requested transformation'
            save()
            self.assertEqual(checker.check(root)['status'], 'incomplete')
            ref['file'] = '../outside.png'
            save()
            self.assertEqual(checker.check(root)['status'], 'incomplete')
