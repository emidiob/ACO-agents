"""Automated evidence-contract tests; these do not pretend to certify aesthetic quality."""
from __future__ import annotations
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
SCRIPTS=BASE/'skills/aco-taste/scripts'
sys.path.insert(0,str(SCRIPTS))
from aco_taste import core,directions,routing,review,system,compare

class Route(unittest.TestCase):
    def test_surface_coverage(self):
        cases={'web':'Redesign website','ui':'Fix app screen UI','photo':'Make a portrait photograph','image':'Create a poster image','video':'Generate a video','motion':'Improve motion animation','document':'Design a magazine layout','spatial':'Design a 3D exhibition installation'}
        for medium,task in cases.items():
            with self.subTest(medium=medium):
                obj=routing.classify(task,declared_medium=medium)
                self.assertTrue(obj['automatic_taste']);self.assertEqual(obj['medium'],medium)
                self.assertTrue(obj['workflow'])
    def test_no_false_background_autonomy(self):self.assertFalse(routing.classify('What is an image format?')['automatic_taste'])
    def test_forced_medium(self):self.assertEqual(routing.classify('do it',declared_medium='video',force_visual=True)['medium'],'video')
    def test_review_no_mutation(self):self.assertIn('do-not-mutate-without-permission',routing.classify('Review UI screen',declared_medium='ui',operation='review')['workflow'])
    def test_small_change(self):self.assertEqual(routing.classify('Change only the text on the website',declared_medium='web')['mode'],'focused-edit')
    def test_bad_medium(self):
        with self.assertRaises(ValueError):routing.classify('make it',declared_medium='magic')
    def test_all_visual_requests_nonempty(self):
        for t in ('create image','make film','fotografa ritratto','impaginazione PDF','generate a dashboard','disegna poster','motion design','make 3d rendering'):
            with self.subTest(t=t):self.assertTrue(routing.classify(t)['automatic_taste'])

class OriginalDirections(unittest.TestCase):
    def setUp(self):self.brief=json.loads((BASE/'skills/aco-taste/examples/brief.json').read_text())
    def test_count(self):self.assertEqual(len(directions.catalog()),50)
    def test_unique(self):self.assertEqual(len({x['id'] for x in directions.catalog()}),50)
    def test_diverse(self):
        v=directions.propose(self.brief,seed=3)['directions'];self.assertEqual(len(v),3)
        self.assertEqual(len(set(x['structure'] for x in v)),3)
        self.assertEqual(len(set(x['visual_material'] for x in v)),3)
    def test_locked_color(self):
        v=directions.propose(self.brief)['directions'];self.assertTrue(all(x['palette']==self.brief['locked']['palette'] for x in v))
    def test_source_specificity(self):
        v=directions.propose(self.brief)['directions'];self.assertTrue(all('paper-origin label' in x['concept_device'] for x in v))
    def test_no_competitor_generalization(self):
        for v in directions.propose(self.brief)['directions']:self.assertIn('not as decorative filler',v['concept_device'])
    def test_unknown_facts_flagged(self):
        b={k:self.brief[k] for k in ('subject','audience','action','surface')};r=directions.propose(b);self.assertTrue(r['unknowns'])
    def test_all_media_supported(self):
        for surface in ('marketing','product','component','editorial','poster','presentation','photo','image','video','motion','spatial','graphic'):
            with self.subTest(surface=surface):
                b=dict(self.brief,surface=surface)
                self.assertEqual(len(directions.propose(b)['directions']),3)
    def test_video_not_css(self):
        b=dict(self.brief,surface='video');self.assertIn('shot staging',directions.propose(b)['directions'][0]['structure'])
    def test_preview(self):
        self.assertEqual(directions.propose(self.brief,seed=33),directions.propose(self.brief,seed=33))
    def test_missing_fails(self):
        with self.assertRaises(ValueError):directions.propose({'surface':'web'})

class SafeMemory(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_new_collection(self):
        item=core.new_collection(self.root,'Still life');self.assertFalse(item['approved']);self.assertEqual(core.status(self.root)['collections'],1)
    def test_reference_url_not_fetched(self):
        item=core.new_collection(self.root,'Visuals');r=core.add_reference(self.root,item['id'],url='https://example.org/study',note='Only typography',role='direction');self.assertTrue(r['not_retrieved']);self.assertEqual(r['approval'],'not_assumed')
    def test_reference_file_hashed(self):
        c=core.new_collection(self.root,'Photographs');p=self.root/'img.png';p.write_bytes(b'fake')
        r=core.add_reference(self.root,c['id'],file=str(p));self.assertEqual(r['sha256'],core.digest(p))
    def test_negative_ref(self):
        c=core.new_collection(self.root,'Bad UI');r=core.add_reference(self.root,c['id'],url='https://example.org/bad',negative=True,role='negative');self.assertTrue(r['negative'])
    def test_no_local_override_of_corrupt_state(self):
        p=core.store_root(self.root)/'collections.json';p.parent.mkdir();p.write_text('{garbage')
        with self.assertRaises(ValueError):core.new_collection(self.root,'Cannot erase');self.assertEqual(p.read_text(),'{garbage')
    def test_feedback_contextual(self):
        core.add_feedback(self.root,'A','prefer','Type scale is more legible',aspects=['typography'])
        core.add_feedback(self.root,'B','reject','Too dense',aspects=['typography'])
        r=core.insights(self.root);self.assertEqual(r['insights'][0]['inference'],'ambiguous');self.assertFalse(r['automatic_global_taste_profile'])
    def test_scope_isolation(self):
        core.add_feedback(self.root,'A','prefer','Good for museum',scope='museum');core.add_feedback(self.root,'B','reject','Bad for shop',scope='shop')
        self.assertEqual(core.insights(self.root,scope='museum')['events_read'],1)
    def test_bad_judgment(self):
        with self.assertRaises(ValueError):core.add_feedback(self.root,'A','perfect','Super')
    def test_bad_url(self):
        c=core.new_collection(self.root,'Visual')
        with self.assertRaises(ValueError):core.add_reference(self.root,c['id'],url='file:///etc/passwd')
    def test_same_url_file_rejected(self):
        c=core.new_collection(self.root,'Visual')
        with self.assertRaises(ValueError):core.add_reference(self.root,c['id'],url='https://example.org',file='/tmp/x')

class Review(unittest.TestCase):
    def test_every_medium_has_criterion(self):self.assertEqual(set(review.REQUIRED_BY_MEDIUM),set(routing.PROFILES))
    def test_missing_evidence(self):self.assertEqual(review.evidence_gate({'medium':'video','reviewed_by':'ACO','evidence':{}})['status'],'review-incomplete')
    def test_complete_not_certified(self):
        evidence={key:True for key in review.REQUIRED_BY_MEDIUM['photo']}
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'photograph.png';p.write_bytes(b'artifact')
            receipt={'path':str(p),'sha256':core.digest(p),'viewed_with':'actual image viewer','review_scope':'full image'}
            r=review.evidence_gate({'medium':'photo','evidence':evidence,'reviewed_by':'human','artifacts':[receipt],'observations':['Rim light verified on subject silhouette']})
            self.assertEqual(r['status'],'evidence-supported');self.assertFalse(r['aesthetic_quality_certified'])
    def test_checkboxes_without_artifact_do_not_pass(self):
        evidence={key:True for key in review.REQUIRED_BY_MEDIUM['web']}
        self.assertEqual(review.evidence_gate({'medium':'web','evidence':evidence,'reviewed_by':'agent','observations':['looks okay']})['status'],'review-incomplete')
    def test_mismatched_receipt_hash_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'image.png';p.write_bytes(b'a')
            o=review.evidence_gate({'medium':'image','artifacts':[{'path':str(p),'sha256':'bad','viewed_with':'viewer','review_scope':'full'}]})
            self.assertEqual(len(o['valid_artifact_receipts']),0);self.assertTrue(o['rejected_artifact_receipts'])
    def test_user_approval_not_inferred(self):
        with self.assertRaises(ValueError):review.evidence_gate({'medium':'image','evidence':{},'user_approved':True})
    def test_css_detection(self):
        r=review.audit_css('a:hover{transition:all 1s;animation:bounce 1s;}')
        self.assertIn('motion-all',[x['rule'] for x in r['findings']]);self.assertIn('reduced-motion',[x['rule'] for x in r['findings']]);self.assertFalse(r['render_verified'])
    def test_anti_slop_not_cert(self):
        a=review.audit_html('<main><h1>Our awesome product</h1>99.9%<p>Lorem ipsum</p></main>')
        self.assertIn('placeholder-text',[x['rule'] for x in a['findings']]);self.assertFalse(a['visually_verified'])
    def test_bad_medium(self):
        with self.assertRaises(ValueError):review.evidence_gate({'medium':'telepathy'})
    def test_preflight_metadata_not_visual(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'artifact.bin';p.write_bytes(b'abc');o=review.media_preflight(str(p));self.assertFalse(o['visually_inspected'])

class System(unittest.TestCase):
    def setUp(self):self.p=json.loads((BASE/'skills/aco-taste/examples/system-evidence.json').read_text())
    def test_confirmed_only(self):
        r=system.compile_design_md(self.p);self.assertEqual(r['included'],2);self.assertEqual(len(r['excluded']),1)
    def test_duplicate_conflict(self):
        p=dict(self.p,evidence=self.p['evidence'][:2]+[{'role':'paper','value':'#fff','source':'bad','scope':'site','confidence':'confirmed'}]);r=system.compile_design_md(p);self.assertTrue(any(x['why'].startswith('conflicting') for x in r['excluded']))
    def test_existing_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'DESIGN.md';p.write_text('locked')
            with self.assertRaises(ValueError):system.write_design_md(root,self.p,apply=True)
            self.assertEqual(p.read_text(),'locked')
    def test_preview_no_write(self):
        with tempfile.TemporaryDirectory() as d:
            r=system.write_design_md(d,self.p);self.assertFalse(Path(d,'DESIGN.md').exists());self.assertIn('DESIGN.md',r['document'])
    def test_explicit_apply(self):
        with tempfile.TemporaryDirectory() as d:
            system.write_design_md(d,self.p,apply=True);self.assertIn('Publishing Studio',Path(d,'DESIGN.md').read_text())

class Compare(unittest.TestCase):
    def setUp(self):self.p=json.loads((BASE/'skills/aco-taste/examples/variants.json').read_text())
    def test_board_accessible(self):
        doc=compare.board(self.p);self.assertIn('aria-live="polite"',doc);self.assertIn('prefers-reduced-motion',doc);self.assertIn('Export evidence JSON',doc)
    def test_duplicate_rejected(self):
        p=dict(self.p,variants=[{'id':'same'},{'id':'same'}])
        with self.assertRaises(ValueError):compare.board(p)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'board.html';p.write_text('keep')
            with self.assertRaises(ValueError):compare.write_board(self.p,p)
            self.assertEqual(p.read_text(),'keep')
    def test_img_data(self):
        with tempfile.TemporaryDirectory() as d:
            im=Path(d)/'a.png';im.write_bytes(b'synthetic');obj=dict(self.p,variants=[dict(x,image=str(im)) for x in self.p['variants'][:2]])
            self.assertIn('data:image/png;base64,',compare.board(obj))
    def test_no_approval(self):self.assertIn('approval:',compare.board(self.p))

class Integrity(unittest.TestCase):
    def test_skill_entry(self):self.assertIn('name: aco-taste',(BASE/'skills/aco-taste/SKILL.md').read_text())
    def test_canonical_global_contract(self):self.assertIn('Users do not have to type', (BASE/'skills/aco-office-concierge/references/protocols/VISUAL-TASTE-ROUTING.md').read_text())
    def test_seven_sources(self):
        data=json.loads((BASE/'skills/aco-taste/assets/sources.json').read_text());self.assertEqual(len(data['sources']),7)
    def test_upstream_incline_not_bundled(self):
        p=BASE/'vendor';self.assertEqual(len(list(p.rglob('*.mjs'))),0)
    def test_taste_cli(self):
        cp=subprocess.run([sys.executable,str(SCRIPTS/'taste.py'),'route','--task','make a cinematic video'],capture_output=True,text=True,timeout=10)
        self.assertEqual(cp.returncode,0,cp.stderr);self.assertEqual(json.loads(cp.stdout)['medium'],'video')

if __name__=='__main__':unittest.main()
