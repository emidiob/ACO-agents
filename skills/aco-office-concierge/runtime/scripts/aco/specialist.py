"""Original offline design/video contract checks. No network, installs or rendering.
A passing result concerns the supplied structure/evidence, not artistic quality.
"""
from __future__ import annotations
import hashlib
import math
import re
import struct
from datetime import date
from fractions import Fraction
from pathlib import Path
from .common import ACOError


def obj(value, label='input'):
    if not isinstance(value, dict):
        raise ACOError(label + ' must be an object')
    return value


def text(value):
    return isinstance(value, str) and bool(value.strip())


def integer(value, minimum=1):
    return type(value) is int and value >= minimum


def finite(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def strings(value, nonempty=False):
    return isinstance(value, list) and (bool(value) or not nonempty) and all(text(x) for x in value)


def contrast_ratio(foreground: str, background: str) -> float:
    """WCAG relative luminance contrast for opaque sRGB #RGB/#RRGGBB only."""
    def luminance(value):
        if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?', value):
            raise ACOError('Only opaque sRGB #RGB or #RRGGBB colours are supported')
        raw=value[1:]
        if len(raw)==3: raw=''.join(c*2 for c in raw)
        channels=[int(raw[i:i+2],16)/255 for i in (0,2,4)]
        channels=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c,w in zip(channels,(0.2126,0.7152,0.0722)))
    a,b=sorted((luminance(foreground),luminance(background)))
    return (b+0.05)/(a+0.05)


def web_contract_check(packet: dict) -> dict:
    obj(packet);errors=[];missing=[];warnings=[];ratios=[]
    for k in ('project_id','audience','primary_task','visual_direction'):
        if not text(packet.get(k)):missing.append(k)
    if packet.get('schema_version')!=1 or type(packet.get('schema_version')) is not int: errors.append('schema_version must be integer 1')
    if not strings(packet.get('locked_decisions',[])): errors.append('locked_decisions must be a list of nonempty strings')
    widths=packet.get('viewport_widths')
    if not isinstance(widths,list) or not widths:missing.append('viewport_widths')
    elif any(not integer(w) or w>20000 for w in widths): errors.append('viewport_widths must be positive integer pixel widths <= 20000')
    elif len(set(widths))!=len(widths): errors.append('duplicate viewport widths')
    elif len(widths)==1: warnings.append('Only one width specified; responsive behaviour is not covered')
    pages=packet.get('pages');ids=set()
    if not isinstance(pages,list) or not pages:missing.append('pages')
    else:
        for i,p in enumerate(pages):
            if not isinstance(p,dict):errors.append(f'pages[{i}] must be an object');continue
            if not text(p.get('id')) or not text(p.get('purpose')):errors.append(f'pages[{i}] needs id and purpose')
            elif p['id'] in ids:errors.append('duplicate page id: '+p['id'])
            else:ids.add(p['id'])
            if not strings(p.get('states'),True):errors.append(f'pages[{i}] needs explicit states')
    checks=packet.get('acceptance');check_ids=set()
    if not isinstance(checks,list) or not checks:missing.append('acceptance')
    else:
        for i,c in enumerate(checks):
            if not isinstance(c,dict):errors.append(f'acceptance[{i}] must be an object');continue
            if not text(c.get('id')) or not text(c.get('requirement')):errors.append(f'acceptance[{i}] needs id and requirement');continue
            if c['id'] in check_ids:errors.append('duplicate acceptance id: '+c['id'])
            check_ids.add(c['id'])
            if c.get('method') not in {'browser','manual','static','unit','integration','performance'}:errors.append(f'acceptance[{i}] has unsupported method')
    pairs=packet.get('contrast_pairs',[])
    if not isinstance(pairs,list):errors.append('contrast_pairs must be a list');pairs=[]
    for i,pair in enumerate(pairs):
        if not isinstance(pair,dict):errors.append(f'contrast_pairs[{i}] must be an object');continue
        category=pair.get('category','normal_text')
        if category not in {'normal_text','large_text','non_text'}:errors.append(f'contrast_pairs[{i}] invalid category');continue
        try:r=contrast_ratio(pair.get('foreground'),pair.get('background'))
        except ACOError as e:errors.append(f'contrast_pairs[{i}]: {e}');continue
        threshold=4.5 if category=='normal_text' else 3.0
        ratios.append({'index':i,'ratio':round(r,6),'threshold':threshold,'passes_numerical_threshold':r>=threshold})
        if r<threshold:errors.append(f'contrast_pairs[{i}] below supplied category threshold')
    fonts=packet.get('fonts',[])
    if not isinstance(fonts,list):errors.append('fonts must be a list');fonts=[]
    for i,f in enumerate(fonts):
        if not isinstance(f,dict) or not text(f.get('family')):errors.append(f'fonts[{i}] needs family');continue
        if f.get('license_status')!='verified' or not text(f.get('source')):warnings.append(f'fonts[{i}] source/licence evidence unresolved')
    return {'status':'needs_input' if missing else 'issues_found' if errors else 'structure_checked',
            'missing':missing,'errors':errors,'warnings':warnings,'contrast':ratios,
            'expected_acceptance_ids':sorted(check_ids),'rendered':False,
            'limitations':'Contract completeness and opaque-colour arithmetic only. No browser execution, visual judgement, font-rights verification or WCAG certification.'}


def shot_plan_check(packet: dict) -> dict:
    obj(packet);errors=[];warnings=[];total=0
    if packet.get('schema_version')!=1 or type(packet.get('schema_version')) is not int:errors.append('schema_version must be integer 1')
    fps=packet.get('fps');target=packet.get('target_frames')
    if not integer(fps) or fps>240:errors.append('fps must be a positive integer <= 240')
    if not integer(target):errors.append('target_frames must be a positive integer')
    aspect=packet.get('aspect_ratio')
    if not isinstance(aspect,str) or not re.fullmatch(r'[1-9]\d{0,3}:[1-9]\d{0,3}',aspect):errors.append('aspect_ratio must be a positive W:H pair')
    assets=packet.get('assets',[]);asset_ids=set()
    if not isinstance(assets,list):errors.append('assets must be a list');assets=[]
    for i,a in enumerate(assets):
        if not isinstance(a,dict) or not text(a.get('id')):errors.append(f'assets[{i}] needs id');continue
        if a['id'] in asset_ids:errors.append('duplicate asset id: '+a['id'])
        asset_ids.add(a['id'])
        if a.get('rights_status') not in {'authorized','owned','cleared','example'}:warnings.append('asset rights unresolved: '+a['id'])
    shots=packet.get('shots');seen=set();prev=None;timeline=[]
    if not isinstance(shots,list) or not shots:errors.append('shots must be a nonempty list');shots=[]
    for i,s in enumerate(shots):
        label=f'shots[{i}]'
        if not isinstance(s,dict):errors.append(label+' must be an object');continue
        for k in ('id','scene_id','purpose','start_frame_description','subject_action','camera','end_frame_description'):
            if not text(s.get(k)):errors.append(label+' missing '+k)
        if text(s.get('id')):
            if s['id'] in seen:errors.append('duplicate shot id: '+s['id'])
            seen.add(s['id'])
        frames=s.get('frames');overlap=s.get('transition_in_frames',0)
        valid_frames=integer(frames)
        if not valid_frames:errors.append(label+'.frames must be a positive integer')
        if not integer(overlap,0):errors.append(label+'.transition_in_frames must be a nonnegative integer');overlap=0
        transition=s.get('transition_in','cut')
        if transition not in {'cut','dissolve'}:errors.append(label+' unsupported transition')
        if transition=='cut' and overlap:errors.append(label+' cut cannot have overlap')
        if transition=='dissolve' and not overlap:errors.append(label+' dissolve needs positive overlap')
        if i==0 and overlap:errors.append('First shot cannot overlap a predecessor')
        if valid_frames and overlap>=frames:errors.append(label+' overlap consumes whole shot')
        if prev and integer(prev.get('frames')) and overlap>=prev['frames']:errors.append(label+' overlap consumes whole previous shot')
        refs=s.get('reference_ids',[])
        if not strings(refs):errors.append(label+'.reference_ids must be strings');refs=[]
        for ref in refs:
            if ref not in asset_ids:errors.append(label+' unknown reference '+ref)
        if text(s.get('source_image_id')) and s['source_image_id'] not in refs:errors.append(label+' source_image_id must be one of reference_ids')
        for state in ('continuity_in','continuity_out'):
            if not isinstance(s.get(state),dict) or not s[state] or not all(text(k) and text(v) for k,v in s[state].items()):errors.append(label+'.'+state+' needs a flat nonempty string map')
        changes=s.get('intentional_changes',{})
        if not isinstance(changes,dict) or not all(text(k) and text(v) for k,v in changes.items()):errors.append(label+' intentional_changes needs reason strings');changes={}
        if prev and s.get('scene_id')==prev.get('scene_id'):
            before=prev.get('continuity_out');after=s.get('continuity_in')
            if isinstance(before,dict) and isinstance(after,dict):
                for key in before:
                    if before[key]!=after.get(key) and key not in changes:errors.append(label+' unaccounted continuity change: '+str(key))
        if valid_frames:
            start=total-overlap;total=start+frames
            timeline.append({'id':s.get('id'),'start_frame':start,'end_frame_exclusive':total})
        prev=s
    if integer(target) and total!=target:errors.append(f'Timeline is {total} frames; target is {target}')
    return {'status':'issues_found' if errors else 'structure_checked','errors':errors,'warnings':warnings,
            'timeline':timeline,'total_frames':total,'seconds':float(Fraction(total,fps)) if integer(fps) else None,
            'rendered':False,'limitations':'Integer-FPS planning only; overlaps are counted once. No visual continuity, actual asset rights, camera feasibility or rendered-media QC has been verified.'}


def video_prompt_draft(plan: dict, capability: dict, as_of: date|None=None) -> dict:
    obj(capability,'capability');check=shot_plan_check(plan);errors=list(check['errors']);warnings=list(check['warnings']);drafts=[]
    now=as_of or date.today()
    if not isinstance(now,date):raise ACOError('as_of must be a date')
    for k in ('provider','model','interface_scope','source_url','verified_on'):
        if not text(capability.get(k)):errors.append('capability missing '+k)
    try:
        verified=date.fromisoformat(capability.get('verified_on',''))
        age=(now-verified).days
        if age<0:errors.append('Capability snapshot is dated in the future')
        elif age>30:errors.append('Capability snapshot is older than 30 days; refresh before provider-specific drafting')
    except (ValueError,TypeError):errors.append('capability.verified_on must be an ISO date')
    if text(capability.get('source_url')) and not capability['source_url'].startswith('https://'):errors.append('capability.source_url must be an HTTPS source')
    modes=capability.get('modes');aspects=capability.get('aspect_ratios');durations=capability.get('durations_seconds')
    if not strings(modes,True):errors.append('capability.modes must be supplied');modes=[]
    if not strings(aspects,True):errors.append('capability.aspect_ratios must be supplied');aspects=[]
    if not isinstance(durations,list) or not durations or any(not finite(d) or d<=0 for d in durations):errors.append('capability.durations_seconds must be positive finite numbers');durations=[]
    if plan.get('aspect_ratio') not in aspects:errors.append('Requested aspect ratio is not in supplied capability')
    for k in ('supports_negative_prompt','supports_audio','supports_seed'):
        if type(capability.get(k)) is not bool:errors.append('capability missing explicit boolean '+k)
    max_chars=capability.get('max_prompt_characters')
    if max_chars is not None and not integer(max_chars):errors.append('max_prompt_characters must be null or a positive integer')
    if capability.get('example_fixture'):warnings.append('This capability is a fictional offline fixture, not a verified live provider contract')
    if errors:return {'status':'needs_correction','errors':errors,'warnings':warnings,'drafts':[], 'submitted':False,'api_payload':False}
    for s in plan['shots']:
        label=s['id'];mode=s.get('mode');duration=s.get('generation_seconds')
        if mode not in modes:errors.append(label+': unsupported or missing mode')
        if not finite(duration) or duration not in durations:errors.append(label+': unsupported generation duration')
        elif Fraction(str(duration))*plan['fps']<s['frames']:errors.append(label+': generation duration is shorter than the usable edit segment')
        if mode=='image_to_video' and not text(s.get('source_image_id')):errors.append(label+': image-to-video requires an actual source reference ID')
        negative=s.get('negative_prompt')
        if negative is not None and not text(negative):errors.append(label+': negative_prompt must be nonempty text or absent')
        elif negative and not capability['supports_negative_prompt']:errors.append(label+': negative prompting is unsupported; do not silently add a field')
        audio=s.get('audio_requested',False)
        if type(audio) is not bool:errors.append(label+': audio_requested must be boolean')
        elif audio and not capability['supports_audio']:errors.append(label+': generated audio unsupported; plan a separate authorized audio workflow')
        seed=s.get('seed')
        if seed is not None and (not integer(seed,0) or not capability['supports_seed']):errors.append(label+': seed unsupported or invalid')
        parts=[]
        if mode!='image_to_video':parts.append(s['start_frame_description'].strip())
        parts.extend([s['subject_action'].strip(),s['camera'].strip(),s['end_frame_description'].strip()])
        prompt=' '.join(parts)
        if max_chars is not None and len(prompt)>max_chars:errors.append(label+': prompt exceeds supplied character limit; no automatic truncation')
        drafts.append({'shot_id':label,'provider':capability['provider'],'model':capability['model'],
                       'interface_scope':capability['interface_scope'],'mode':mode,'prompt':prompt,
                       'generation_seconds':duration,'aspect_ratio':plan['aspect_ratio'],
                       'source_image_id':s.get('source_image_id'),'negative_prompt':negative,'seed':seed,
                       'audio_requested':audio,'capability_source':capability['source_url'],
                       'capability_verified_on':capability['verified_on']})
    return {'status':'needs_correction' if errors else 'draft_only','errors':errors,'warnings':warnings,'drafts':drafts,
            'submitted':False,'api_payload':False,
            'limitations':'Normalized draft metadata, NOT an API request. Current provider schema, actual reference files, permissions, costs, authorization and rendered quality still require verification. I2V text omits the static start description, retaining motion and end intent.'}


def evidence_check(packet: dict, evidence_root: Path) -> dict:
    obj(packet);root=Path(evidence_root).resolve();errors=[];checked=[]
    if not root.is_dir():raise ACOError('evidence_root must be an existing directory')
    required=packet.get('required_ids')
    if not strings(required,True) or len(set(required))!=len(required):raise ACOError('required_ids must be unique nonempty strings')
    revision=packet.get('expected_revision')
    if not text(revision):raise ACOError('expected_revision is required')
    claims=packet.get('claims')
    if not isinstance(claims,list):raise ACOError('claims must be a list')
    ids=set();passing=set()
    for i,c in enumerate(claims):
        label=f'claims[{i}]'
        if not isinstance(c,dict) or not text(c.get('id')):errors.append(label+' needs id');continue
        key=c['id']
        if key in ids:errors.append('duplicate claim: '+key)
        ids.add(key)
        if c.get('status') not in {'passed','failed','planned','not_run'}:errors.append(key+': invalid status');continue
        if c['status']!='passed':continue
        err_before=len(errors)
        if c.get('revision')!=revision:errors.append(key+': evidence revision mismatch')
        rel=c.get('path')
        if not text(rel):errors.append(key+': passed claim needs evidence path');continue
        p=Path(rel)
        if p.is_absolute() or '..' in p.parts:errors.append(key+': evidence path must stay relative to approved root');continue
        current=root
        for part in p.parts:
            current=current/part
            if current.is_symlink():errors.append(key+': symlink evidence is not accepted');break
        dest=(root/p).resolve()
        if not dest.is_relative_to(root):errors.append(key+': evidence outside root');continue
        if not dest.is_file() or dest.stat().st_size<=0:errors.append(key+': evidence file absent or empty');continue
        if dest.stat().st_size>16*1024*1024:errors.append(key+': evidence exceeds 16 MiB checker limit');continue
        if len(errors)!=err_before:continue
        data=dest.read_bytes();h=c.get('sha256')
        if not isinstance(h,str) or not re.fullmatch('[a-f0-9]{64}',h) or hashlib.sha256(data).hexdigest()!=h:errors.append(key+': evidence hash mismatch')
        kind=c.get('kind','report')
        if kind not in {'report','png_screenshot'}:errors.append(key+': unsupported evidence kind')
        if kind=='png_screenshot':
            if len(data)<33 or data[:8]!=b'\x89PNG\r\n\x1a\n' or data[12:16]!=b'IHDR':errors.append(key+': not a PNG header')
            else:
                width,height=struct.unpack('>II',data[16:24])
                if width<1 or height<1:errors.append(key+': invalid PNG dimensions')
                expected=c.get('viewport_width')
                if not integer(expected) or width!=expected:errors.append(key+': PNG width does not match declared capture width')
        if len(errors)==err_before:passing.add(key);checked.append(key)
    for k in required:
        if k not in passing:errors.append(k+': required evidence is not integrity-checked and reported passed')
    return {'status':'evidence_incomplete' if errors else 'integrity_checked','errors':errors,'checked_ids':checked,
            'tests_executed_by_checker':False,'limitations':'Checks required IDs, reported state, file boundary/hash, revision and limited PNG header metadata. Does not prove test execution, capture authenticity, visual quality, accessibility or truth of the report contents.'}
