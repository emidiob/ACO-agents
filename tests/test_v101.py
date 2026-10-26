"""ACO v1.0.1 Seedance pack registration and fail-closed tests."""
import unittest
from scripts.aco.common import ROOT
from scripts.aco.skills import skill_registry_check, skill_resolve, skill_search
from scripts.aco.common import ACOError

class SeedanceCandidateGates(unittest.TestCase):
    def test_registry_totals(self):
        r=skill_registry_check(ROOT)
        self.assertEqual((r['status'],r['skills'],r['active_skills'],r['candidate_skills']),('valid',44,14,30))
    def test_candidates_excluded_by_default(self):
        rows=skill_search('seedance',limit=20,root=ROOT)['results']
        self.assertFalse(any(x['skill_id'].startswith('video.seedance.') for x in rows))
    def test_candidate_inspection_explicit(self):
        rows=skill_search('seedance',limit=20,include_candidates=True,root=ROOT)['results']
        self.assertGreaterEqual(len([x for x in rows if x['skill_id'].startswith('video.seedance.')]),10)
    def test_no_automatic_resolution(self):
        with self.assertRaises(ACOError):skill_resolve('video.seedance.identity',root=ROOT)
    def test_explicit_inspection_not_activation(self):
        row=skill_resolve('video.seedance.identity',allow_candidate=True,root=ROOT)
        self.assertFalse(row['selectable'])

for key in ['action','audio','camera-motion','commercial','compact','fashion','found-footage','identity','performance','qa','storyboard','timeline']:
    def check(self,key=key):
        result=skill_resolve('video.seedance.'+key,allow_candidate=True,root=ROOT)
        self.assertEqual(result['skill']['status'],'candidate')
        self.assertEqual(result['body']['status'],'candidate')
        self.assertTrue(result['body']['sources'])
    setattr(SeedanceCandidateGates,'test_candidate_'+key.replace('-','_'),check)
