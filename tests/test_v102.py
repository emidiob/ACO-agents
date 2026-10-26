"""Generative-image candidate skillpack regression / nonactivation."""
import unittest
from scripts.aco.common import ROOT, ACOError
from scripts.aco.skills import skill_registry_check,skill_search,skill_resolve

IDS = [
 'image.shared.reference-decomposition','image.shared.identity','image.shared.photo-realism',
 'image.shared.optics','image.shared.fashion','image.shared.product',
 'image.shared.composition','image.shared.textures','image.shared.editing',
 'image.shared.multiref','image.shared.qa','image.shared.artifact-diagnosis',
 'image.adapter.nano-banana-2','image.adapter.nano-banana-2-1',
 'image.adapter.seedream-4-5','image.adapter.seedream-5'
]
class ImageCandidateRegressions(unittest.TestCase):
 def test_registry_and_counts(self):
  r=skill_registry_check(ROOT)
  self.assertEqual((r['status'],r['skills'],r['active_skills'],r['candidate_skills']),('valid',44,14,30))
 def test_all_candidates_hidden_by_default(self):
  for query in ['nano banana','seedream','fashion editorial image']:
   result=skill_search(query,limit=20,root=ROOT)
   self.assertFalse(any(x['skill_id'].startswith('image.') for x in result['results']))
 def test_explicit_discovery(self):
  result=skill_search('nano banana',include_candidates=True,limit=20,root=ROOT)
  self.assertTrue(any(x['skill_id']=='image.adapter.nano-banana-2' for x in result['results']))
 def test_legacy_seedance_preserved(self):
  self.assertEqual(skill_resolve('video.seedance.identity',allow_candidate=True,root=ROOT)['skill']['status'],'candidate')
for id in IDS:
 def check(self,id=id):
  with self.assertRaises(ACOError):skill_resolve(id,root=ROOT)
  resolved=skill_resolve(id,allow_candidate=True,root=ROOT)
  self.assertFalse(resolved['selectable'])
  self.assertEqual(resolved['body']['status'],'candidate')
  self.assertTrue(resolved['body']['sources'])
  self.assertIn('no live',resolved['body']['verification'].lower()) if id.startswith('image.shared') else self.assertIn('live',resolved['body']['verification'].lower())
 setattr(ImageCandidateRegressions,'test_candidate_'+id.replace('.','_').replace('-','_'),check)
