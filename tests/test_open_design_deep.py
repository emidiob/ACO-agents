"""Original design campaign contracts, distinct markup, content integrity and safe export.
No test here constitutes certification of aesthetics or browser accessibility.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from aco import open_design_deep as d


def sample():
    return {
      'project':'Independent Research Office',
      'audience':'Cultural institutions and collaborators',
      'purpose':'Present the research practice and invite contact',
      'anchor':'A live water archive reconstructed through visual marks',
      'locked_identity':False,
      'content':{
        'en':{'title':'The Archive Is a River',
          'description':'An experimental index of traces, water and machine vision.',
          'sections':[{'heading':'Index','body':'Research notes ordered by their source and date.'},
                      {'heading':'Methods','body':'Field observations are compared with machine-generated marks.'}],
          'cta':{'label':'Get in touch','href':'mailto:studio@example.org'}},
        'it':{'title':'L’archivio è un fiume',
          'description':'Un indice sperimentale di tracce, acqua e visione artificiale.',
          'sections':[{'heading':'Indice','body':'Note di ricerca ordinate per fonte e data.'},
                      {'heading':'Metodi','body':'Le osservazioni vengono confrontate con segni generati dalle macchine.'}]}
        },
      'channels':[{'id':'landing-en','kind':'landing','locale':'en','format':'desktop'},
                  {'id':'square-it','kind':'social','locale':'it','format':'square'},
                  {'id':'portrait-it','kind':'social','locale':'it','format':'portrait'},
                  {'id':'deck-en','kind':'deck','locale':'en','format':'slides'}],
      'references':[{'id':'gallery-a','source':'User-supplied reference notes','role':'inspiration',
        'observations':[{'lens':'hierarchy','observation':'Oversized project title over sparse indexing',
                         'effect':'Establishes a clear editorial point of entry',
                         'adaptation':'Use our own archive name as the structural headline'}]},
        {'id':'avoid-b','source':'User correction of crowded interface','role':'negative',
         'observations':[{'lens':'whitespace','observation':'Dense small labels',
                          'effect':'Slower reading on mobile',
                          'adaptation':'Avoid miniature condensed captions'}]}]
      }


class CampaignContracts(unittest.TestCase):
    def test_validation(self):
        x=d.validate_campaign(sample());self.assertEqual(x['project'],'Independent Research Office');self.assertEqual(len(x['channels']),4)
    def test_unique_anchor_required(self):
        x=sample();x['anchor']=''
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_missing_locale_fails(self):
        x=sample();x['channels'][0]['locale']='fr'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_missing_channel_fails(self):
        x=sample();x['channels']=[]
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_duplicate_channel_fails(self):
        x=sample();x['channels'][1]['id']='landing-en'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_traversal_channel_fails(self):
        x=sample();x['channels'][0]['id']='../evil'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_no_implicit_translation(self):
        x=sample();del x['content']['it']
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_locked_identity_requires_tokens(self):
        x=sample();x['locked_identity']=True
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_custom_tokens(self):
        x=sample();x['locked_identity']=True;x['tokens']=dict(d.DEFAULT_TOKENS)
        self.assertTrue(d.validate_campaign(x)['locked_identity'])
    def test_reject_css_value(self):
        x=sample();x['tokens']={**d.DEFAULT_TOKENS,'background':'url(x)'}
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_reject_injected_cta(self):
        x=sample();x['content']['en']['cta']['href']='javascript:alert(1)'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_reject_invalid_reference_lens(self):
        x=sample();x['references'][0]['observations'][0]['lens']='invented'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_reject_duplicate_reference_id(self):
        x=sample();x['references'][1]['id']='gallery-a'
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_reference_controls_render_into_output(self):
        x=sample();x['references'][0]['observations'][0]['controls']={'hero_scale':'large','density':'airy'}
        p=d.validate_campaign(x)
        self.assertEqual(d.study(p)['safe_design_controls']['hero_scale']['source'],'gallery-a')
        self.assertIn('hint-hero-scale-large',d.render(p,p['channels'][0],'index-led'))
        self.assertIn('hint-density-airy',d.render(p,p['channels'][0],'index-led'))
    def test_conflicting_reference_controls_not_applied(self):
        x=sample()
        x['references'][0]['observations'][0]['controls']={'alignment':'left'}
        x['references'].append({'id':'gallery-c','source':'another observed visual',
            'observations':[{'lens':'alignment','observation':'Strong central axis',
                             'effect':'Clear visual emphasis','adaptation':'Try centered hierarchy',
                             'controls':{'alignment':'center'}}]})
        p=d.validate_campaign(x)
        ref=d.study(p)
        self.assertEqual(len(ref['control_conflicts']),1)
        self.assertNotIn('alignment',ref['safe_design_controls'])
        self.assertNotIn('hint-align-center',d.render(p,p['channels'][0],'index-led').split('</style>')[1])
    def test_invalid_control_value_rejected(self):
        x=sample();x['references'][0]['observations'][0]['controls']={'alignment':'javascript:bad'}
        with self.assertRaises(ValueError):d.validate_campaign(x)
    def test_no_full_unlicensed_artefact_adoption(self):
        a=d.study(d.validate_campaign(sample()))
        self.assertFalse(a['permission_to_copy_assets']);self.assertFalse(a['reference_images_viewed'])
    def test_negative_refs_not_positive(self):
        a=d.study(d.validate_campaign(sample()))
        self.assertEqual(len(a['adaptations']),1);self.assertEqual(len(a['constraints_from_negatives']),1)


class RealArtifacts(unittest.TestCase):
    def setUp(self):self.packet=d.validate_campaign(sample())
    def test_three_structure_descriptions(self):
        xs=d.directions(self.packet)['directions']
        self.assertEqual(len({x['structure'] for x in xs}),3)
        self.assertEqual(len({x['hierarchy'] for x in xs}),3)
    def test_three_distinct_html_strategies(self):
        c=self.packet['channels'][0]
        renders=[d.render(self.packet,c,style) for style in d.COMPOSITIONS]
        self.assertEqual(len(set(renders)),3)
        self.assertIn('class="index-led landing"',renders[0])
        self.assertIn('class="field-led landing"',renders[1])
        self.assertIn('class="type-led landing"',renders[2])
        for style,markup in zip(d.COMPOSITIONS,renders):self.assertTrue(d.static_audit(self.packet,c,style,markup)['pass'])
    def test_localization_not_faked(self):
        c=self.packet['channels'][1]
        page=d.render(self.packet,c,'field-led')
        self.assertIn('lang="it"',page);self.assertIn('L’archivio',page);self.assertNotIn('The Archive Is a River',page)
    def test_content_escapes(self):
        p=sample();p['content']['en']['title']='B <script>alert(1)</script>'
        v=d.validate_campaign(p);markup=d.render(v,v['channels'][0],'index-led')
        self.assertIn('&lt;script&gt;',markup);self.assertNotIn('<script>',markup)
    def test_metric_supplied_only(self):
        p=sample();p['channels']=[{'id':'metrics','kind':'dashboard','locale':'en','format':'desktop'}]
        p['content']['en']['metrics']=[{'label':'Samples','value':'24','detail':'User-provided figure'}]
        v=d.validate_campaign(p);markup=d.render(v,v['channels'][0],'type-led')
        self.assertIn('>24</strong>',markup);self.assertNotIn('99.9%',markup)
    def test_social_portrait_geometry(self):
        c=self.packet['channels'][2];html=d.render(self.packet,c,'index-led')
        self.assertIn('--aspect:4 / 5',html)
    def test_in_page_fragment_must_exist(self):
        x=sample();x['content']['en']['cta']['href']='#missing'
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):d.build_campaign(x,Path(t)/'invalid')
            self.assertFalse((Path(t)/'invalid').exists())
    def test_features_anchor_is_valid(self):
        x=sample();x['content']['en']['cta']['href']='#features'
        p=d.validate_campaign(x)
        content=d.render(p,p['channels'][0],'index-led')
        self.assertTrue(d.static_audit(p,p['channels'][0],'index-led',content)['pass'])
    def test_output_fails_closed_if_exists(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'campaign';p.mkdir();(p/'keep').write_text('important')
            with self.assertRaises(FileExistsError):d.build_campaign(sample(),p)
            self.assertEqual((p/'keep').read_text(),'important')
    def test_campaign_files_and_receipts(self):
        with tempfile.TemporaryDirectory() as t:
            output=Path(t)/'edition'
            result=d.build_campaign(sample(),output)
            manifest=json.loads((output/'manifest.json').read_text())
            self.assertEqual(result['artifacts'],12)
            self.assertEqual(len(manifest['artifacts']),12)
            self.assertFalse(manifest['user_approval'])
            self.assertFalse(manifest['visual_quality_certified'])
            for row in manifest['artifacts']:
                src=(output/row['path']).read_text()
                self.assertEqual(row['sha256'],d._hash(src))
                self.assertTrue(row['audit']['pass'])
    def test_static_audit_not_a_visual_certificate(self):
        c=self.packet['channels'][0];report=d.static_audit(self.packet,c,'index-led',d.render(self.packet,c,'index-led'))
        self.assertEqual(report['rendered_visual_review'],'not performed')
        self.assertFalse(report['human_approval'])
    def test_cli_full_flow(self):
        with tempfile.TemporaryDirectory() as t:
            packet=Path(t)/'brief.json';packet.write_text(json.dumps(sample()))
            dest=Path(t)/'bundle'
            cli=ROOT/'scripts/aco_open_design_deep.py'
            plan=subprocess.run([sys.executable,str(cli),'plan','--packet',str(packet)],capture_output=True,text=True,timeout=10)
            self.assertEqual(plan.returncode,0,plan.stderr)
            created=subprocess.run([sys.executable,str(cli),'build','--packet',str(packet),'--output',str(dest)],capture_output=True,text=True,timeout=10)
            self.assertEqual(created.returncode,0,created.stderr)
            self.assertTrue((dest/'index.html').exists())

if __name__=='__main__':unittest.main()
