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
