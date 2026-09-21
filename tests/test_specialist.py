import copy, hashlib, json, struct, subprocess, sys, tempfile, unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from aco.common import ROOT, ACOError
from aco.specialist import contrast_ratio,web_contract_check,shot_plan_check,video_prompt_draft,evidence_check
E=ROOT/'examples/specialist-upgrade'
def sample(name):return json.loads((E/name).read_text())

class WebChecks(unittest.TestCase):
 def setUp(self):self.p=sample('web-contract.example.json')
 def test_valid_contract_not_rendered(self):
  r=web_contract_check(self.p);self.assertEqual(r['status'],'structure_checked');self.assertFalse(r['rendered'])
 def test_missing_question(self):
  self.p.pop('audience');self.assertIn('audience',web_contract_check(self.p)['missing'])
 def test_bool_width(self):
  self.p['viewport_widths']=[True];self.assertTrue(web_contract_check(self.p)['errors'])
 def test_duplicate_widths(self):
  self.p['viewport_widths']=[360,360];self.assertTrue(web_contract_check(self.p)['errors'])
 def test_bad_states(self):
  self.p['pages'][0]['states']='default';self.assertTrue(web_contract_check(self.p)['errors'])
 def test_duplicate_page_id(self):
  self.p['pages'].append(self.p['pages'][0]);self.assertTrue(web_contract_check(self.p)['errors'])
 def test_duplicate_acceptance(self):
  self.p['acceptance'].append(self.p['acceptance'][0]);self.assertTrue(web_contract_check(self.p)['errors'])
 def test_font_unverified_warns(self):
  self.p['fonts'][0]['license_status']='unknown';self.assertTrue(web_contract_check(self.p)['warnings'])
 def test_black_white_contrast(self):self.assertAlmostEqual(contrast_ratio('#000','#fff'),21)
 def test_same_colour(self):self.assertEqual(contrast_ratio('#123456','#123456'),1)
 def test_alpha_rejected(self):
  with self.assertRaises(ACOError):contrast_ratio('#00000000','#fff')
 def test_css_named_colour_rejected(self):
  with self.assertRaises(ACOError):contrast_ratio('red','#fff')
 def test_contrast_failure(self):
  self.p['contrast_pairs'][0]['foreground']='#aaa';self.assertTrue(web_contract_check(self.p)['errors'])
 def test_bad_acceptance_method(self):
  self.p['acceptance'][0]['method']='magic';self.assertTrue(web_contract_check(self.p)['errors'])
 def test_wrong_root_type(self):
  with self.assertRaises(ACOError):web_contract_check([])

class ShotChecks(unittest.TestCase):
 def setUp(self):self.p=sample('shot-plan.example.json')
 def test_exact_overlap_timeline(self):
  r=shot_plan_check(self.p);self.assertEqual(r['errors'],[]);self.assertEqual(r['total_frames'],288);self.assertEqual(r['seconds'],12);self.assertEqual(r['timeline'][-1]['start_frame'],168)
 def test_target_mismatch(self):
  self.p['target_frames']=300;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_duplicate_id(self):
  self.p['shots'][1]['id']=self.p['shots'][0]['id'];self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_unknown_reference(self):
  self.p['shots'][0]['reference_ids']=['missing'];self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_bool_frame(self):
  self.p['shots'][0]['frames']=True;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_fractional_fps_is_explicitly_unsupported(self):
  self.p['fps']=23.976;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_first_overlap(self):
  self.p['shots'][0]['transition_in_frames']=10;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_overlap_consumes_previous(self):
  self.p['shots'][2]['transition_in_frames']=100;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_dissolve_needs_overlap(self):
  self.p['shots'][2]['transition_in_frames']=0;self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_continuity_error(self):
  self.p['shots'][1]['continuity_in']['light']='hard';self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_intentional_change(self):
  s=self.p['shots'][1];s['continuity_in']['light']='hard';s['intentional_changes']={'light':'Intentional flash at the cut'};self.assertFalse(shot_plan_check(self.p)['errors'])
 def test_scene_change_not_forced_match(self):
  s=self.p['shots'][1];s['scene_id']='different';s['continuity_in']['light']='hard';self.assertFalse(shot_plan_check(self.p)['errors'])
 def test_nonstring_state(self):
  self.p['shots'][0]['continuity_in']['light']=[];self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_missing_purpose(self):
  self.p['shots'][0]['purpose']='';self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_source_must_be_linked(self):
  self.p['shots'][0]['source_image_id']='ref-03';self.assertTrue(shot_plan_check(self.p)['errors'])
 def test_bad_aspect(self):
  self.p['aspect_ratio']='0:9';self.assertTrue(shot_plan_check(self.p)['errors'])

class PromptChecks(unittest.TestCase):
 def setUp(self):self.p=sample('shot-plan.example.json');self.c=sample('capability.example.json');self.today=date(2026,9,20)
 def runcheck(self):return video_prompt_draft(self.p,self.c,self.today)
 def test_valid_never_submitted(self):
  r=self.runcheck();self.assertFalse(r['submitted']);self.assertFalse(r['api_payload']);self.assertEqual(r['status'],'draft_only');self.assertEqual(len(r['drafts']),3)
 def test_i2v_omits_redundant_start_frame(self):self.assertNotIn(self.p['shots'][0]['start_frame_description'],self.runcheck()['drafts'][0]['prompt'])
 def test_text_mode_keeps_start_frame(self):
  self.p['shots'][0]['mode']='text_to_video';self.assertIn(self.p['shots'][0]['start_frame_description'],self.runcheck()['drafts'][0]['prompt'])
 def test_negative_support_required(self):
  self.p['shots'][0]['negative_prompt']='flicker';self.assertTrue(self.runcheck()['errors'])
 def test_audio_support_required(self):
  self.p['shots'][0]['audio_requested']=True;self.assertTrue(self.runcheck()['errors'])
 def test_seed_support_required(self):
  self.p['shots'][0]['seed']=7;self.assertTrue(self.runcheck()['errors'])
 def test_duration_supported(self):
  self.p['shots'][0]['generation_seconds']=7;self.assertTrue(self.runcheck()['errors'])
 def test_generation_must_cover_edit(self):
  self.c['durations_seconds']=[3,5];self.p['shots'][0]['generation_seconds']=3;self.assertTrue(self.runcheck()['errors'])
 def test_unsupported_mode(self):
  self.p['shots'][0]['mode']='teleport';self.assertTrue(self.runcheck()['errors'])
 def test_stale(self):
  self.c['verified_on']='2025-01-01';self.assertTrue(self.runcheck()['errors'])
 def test_future(self):
  self.c['verified_on']='2027-01-01';self.assertTrue(self.runcheck()['errors'])
 def test_invalid_date(self):
  self.c['verified_on']='yesterday';self.assertTrue(self.runcheck()['errors'])
 def test_capability_does_not_assume_booleans(self):
  self.c['supports_seed']='false';self.assertTrue(self.runcheck()['errors'])
 def test_no_truncation(self):
  self.c['max_prompt_characters']=5;self.assertTrue(self.runcheck()['errors']);self.assertGreater(len(self.runcheck()['drafts'][0]['prompt']),5)
 def test_missing_image(self):
  self.p['shots'][0].pop('source_image_id');self.assertTrue(self.runcheck()['errors'])
 def test_nan_duration(self):
  self.c['durations_seconds']=[float('nan')];self.assertTrue(self.runcheck()['errors'])
 def test_empty_template_fails_closed(self):
  self.c=sample('capability.TEMPLATE.json');self.assertTrue(self.runcheck()['errors']);self.assertEqual(self.runcheck()['drafts'],[])

class EvidenceChecks(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.data=b'Example test report, not evidence of a real browser run';(self.root/'report.txt').write_bytes(self.data)
  self.p={'expected_revision':'test-build','required_ids':['flow'],'claims':[{'id':'flow','status':'passed','revision':'test-build','kind':'report','path':'report.txt','sha256':hashlib.sha256(self.data).hexdigest()}]}
 def tearDown(self):self.tmp.cleanup()
 def check(self):return evidence_check(self.p,self.root)
 def test_integrity_not_execution(self):
  r=self.check();self.assertEqual(r['status'],'integrity_checked');self.assertFalse(r['tests_executed_by_checker'])
 def test_absent_file(self):
  self.p['claims'][0]['path']='missing';self.assertTrue(self.check()['errors'])
 def test_hash_mismatch(self):
  (self.root/'report.txt').write_text('changed');self.assertTrue(self.check()['errors'])
 def test_old_build(self):
  self.p['claims'][0]['revision']='old';self.assertTrue(self.check()['errors'])
 def test_not_run_is_not_pass(self):
  self.p['claims'][0]['status']='not_run';self.assertTrue(self.check()['errors'])
 def test_unrelated_does_not_cover(self):
  self.p['required_ids'].append('keyboard');self.assertTrue(self.check()['errors'])
 def test_duplicate_claim(self):
  self.p['claims'].append(copy.deepcopy(self.p['claims'][0]));self.assertTrue(self.check()['errors'])
 def test_traversal(self):
  self.p['claims'][0]['path']='../report.txt';self.assertTrue(self.check()['errors'])
 def test_absolute(self):
  self.p['claims'][0]['path']=str(self.root/'report.txt');self.assertTrue(self.check()['errors'])
 def test_symlink(self):
  (self.root/'link.txt').symlink_to(self.root/'report.txt');self.p['claims'][0]['path']='link.txt';self.assertTrue(self.check()['errors'])
 def test_fake_png(self):
  self.p['claims'][0]['kind']='png_screenshot';self.p['claims'][0]['viewport_width']=360;self.assertTrue(self.check()['errors'])
 def test_png_header_only_limited_check(self):
  # This is deliberately only a header: passing checks are NOT PNG decoding or authenticity proof.
  data=b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+struct.pack('>II',360,640)+b'\x08\x02\x00\x00\x00'+b'\x00'*4
  (self.root/'header.png').write_bytes(data);c=self.p['claims'][0];c.update(path='header.png',kind='png_screenshot',viewport_width=360,sha256=hashlib.sha256(data).hexdigest());self.assertFalse(self.check()['errors'])
  c['viewport_width']=1440;self.assertTrue(self.check()['errors'])
 def test_required_ids_unique(self):
  self.p['required_ids']=['flow','flow']
  with self.assertRaises(ACOError):self.check()

class SpecialistCoverage(unittest.TestCase):
 def test_all_baseline_roles_preserved(self):
  b=json.loads((ROOT/'research/specialist-upgrade/baseline-roles.json').read_text());c=json.loads((ROOT/'catalog.json').read_text());self.assertTrue({r['key'] for r in b['roles']}<=set(c['agents']))
 def test_new_roles_distinct_and_count(self):
  d=json.loads((ROOT/'research/specialist-upgrade/decisions.json').read_text())['decisions'];new=[x['key'] for x in d if x['action']=='add_distinct_role'];self.assertEqual(len(new),14);self.assertEqual(len(set(new)),14)
 def test_every_baseline_role_compared_with_every_source(self):
  from compare_specialists import compare
  d=ROOT/'research/specialist-upgrade';r=compare(d/'sources.json',d/'baseline-roles.json',d/'decisions.json');self.assertEqual(len(r['pairs']),349*15);self.assertEqual(len({(p['role'],p['source_id']) for p in r['pairs']}),349*15)
 def test_every_playbook_exists(self):
  d=json.loads((ROOT/'research/specialist-upgrade/playbooks.json').read_text());self.assertEqual(len(d),12)
  for key in d:self.assertTrue((ROOT/'skills/aco-office-concierge/references/playbooks'/f'{key}.md').exists())
 def test_runtime_module_mirrors_source(self):
  self.assertEqual((ROOT/'scripts/aco/specialist.py').read_bytes(),(ROOT/'skills/aco-office-concierge/runtime/scripts/aco/specialist.py').read_bytes())
 def test_cli_usable(self):
  r=subprocess.run([sys.executable,str(ROOT/'scripts/aco_cli.py'),'shot-plan-check','--input',str(E/'shot-plan.example.json')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertFalse(json.loads(r.stdout)['rendered'])
 def test_cli_invalid_contract_fails(self):
  r=subprocess.run([sys.executable,str(ROOT/'scripts/aco_cli.py'),'video-prompt-draft','--input',str(E/'shot-plan.example.json'),'--capability',str(E/'capability.TEMPLATE.json'),'--as-of','2026-09-20'],capture_output=True,text=True);self.assertEqual(r.returncode,2,r.stderr)

class BrowserGuardTests(unittest.TestCase):
 def test_loopback_target(self):
  from capture_web_evidence import validate_target
  self.assertEqual(validate_target('http://127.0.0.1:3000/').hostname,'127.0.0.1')
 def test_external_target_rejected(self):
  from capture_web_evidence import validate_target
  with self.assertRaises(ValueError):validate_target('https://example.com/')
 def test_lookalike_rejected(self):
  from capture_web_evidence import validate_target
  with self.assertRaises(ValueError):validate_target('http://localhost.example.com/')
 def test_credentials_rejected(self):
  from capture_web_evidence import validate_target
  with self.assertRaises(ValueError):validate_target('http://user:pass@localhost/')
 def test_file_target_rejected(self):
  from capture_web_evidence import validate_target
  with self.assertRaises(ValueError):validate_target('file:///tmp/example.html')
 def test_existing_output_not_overwritten(self):
  from capture_web_evidence import capture
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):capture('http://localhost:3000/',Path(tmp),'revision')
 def test_output_inside_library_rejected(self):
  from capture_web_evidence import capture
  with self.assertRaises(ValueError):capture('http://localhost:3000/',ROOT/'should-not-exist','revision')
 def test_bad_width_rejected_before_launch(self):
  from capture_web_evidence import capture
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):capture('http://localhost:3000/',Path(tmp)/'new','revision',[True])
