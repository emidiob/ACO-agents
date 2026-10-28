import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('motion_check', ROOT/'skills/aco-genjutsu/scripts/check_motion_plan.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class MotionTransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.prompt = 'The robot reaches forward. Its fingers close around the handle. It lifts the case. The camera holds still.'
        self.plan = {'source_duration_seconds': 3, 'target_duration_seconds': 3,
                     'reviewed_intervals': [[0, 3]], 'entities': {'person': 'robot', 'camera': 'fixed camera'}, 'events': []}
        for i, text in enumerate(self.prompt.split('. ')[:3]):
            self.plan['events'].append({'id': str(i), 'actor': 'person', 'track': 'subject',
                'source_interval': [i, i+1], 'target_interval': [i, i+1],
                'observed': ['Person reaches forward', 'Fingers grip handle', 'Case leaves support'][i],
                'target_action': text, 'prompt_excerpt': text, 'evidence': ['frame.png'], 'certainty': 'observed'})
        camera = copy.deepcopy(self.plan['events'][0])
        camera.update(id='camera', actor='camera', track='camera', source_interval=[0,3], target_interval=[0,3],
                      observed='Camera stationary', target_action='Camera stationary', prompt_excerpt='The camera holds still.')
        self.plan['events'].append(camera)

    def check(self):
        (self.folder/'motion-plan.json').write_text(json.dumps(self.plan))
        return checker.check_motion(self.folder, self.prompt, [{'file':'frame.png'}])

    def test_complete_parallel_tracks(self):
        self.assertEqual(self.check(), [])

    def test_shortened_prompt_loses_grip(self):
        self.prompt = self.prompt.replace('Its fingers close around the handle. ', '')
        self.assertTrue(any('excerpt' in e for e in self.check()))

    def test_static_camera_cannot_hide_missing_action_interval(self):
        del self.plan['events'][1]
        self.assertTrue(any('Subject/object' in e for e in self.check()))

    def test_unreviewed_tail_and_uncertainty(self):
        self.plan['reviewed_intervals'] = [[0,2]]
        self.plan['events'][1]['certainty'] = 'uncertain'
        errors = self.check()
        self.assertTrue(any('review' in e for e in errors))
        self.assertTrue(any('unresolved' in e for e in errors))

    def test_missing_evidence_and_target_mapping(self):
        self.plan['events'][1]['actor'] = 'unmapped'
        self.plan['events'][1]['evidence'] = ['invented.png']
        errors = self.check()
        self.assertTrue(any('unmapped' in e for e in errors))
        self.assertTrue(any('evidence' in e for e in errors))

    def test_duration_change_requires_target_retiming(self):
        self.plan['target_duration_seconds'] = 6
        self.assertTrue(any('target intervals' in e for e in self.check()))
        for event in self.plan['events']:
            event['target_interval'] = [x*2 for x in event['target_interval']]
        self.assertEqual(self.check(), [])

    def test_omission_requires_requested_change(self):
        self.plan['events'][1]['disposition'] = 'omitted'
        self.assertTrue(any('omission lacks' in e for e in self.check()))

    def test_source_duration_matches_inspection(self):
        (self.folder/'inspection.json').write_text(json.dumps({'duration_seconds': 4}))
        self.assertTrue(any('differs' in e for e in self.check()))
