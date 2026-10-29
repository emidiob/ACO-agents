#!/usr/bin/env python3
"""Original ACO competence loader and deterministic evidence checks.

Offline and side-effect free. It never invokes a model, promotes a skill, sends
messages or proves the truth of caller-supplied observations. Python >= 3.11.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

DEFAULT_ROOT = Path(__file__).resolve().parents[1] / 'references' / 'competencies'
VERSION = '0.3.0'
OFFICES = {'artist-office','organization-office','agency-office','product-office',
 'legal-office','recruitment-office','shared','finance-office','commercial-office',
 'people-office','delivery-office','administration-office','production-office','publishing-office'}
PARTS = ('METHOD.md','DECISIONS.md','OUTPUT.md','EXAMPLES.md','EVALS.json','SOURCES.json')
MAX_JSON_BYTES = 2_000_000

class LibraryError(ValueError):
    """Invalid, ambiguous or unsafe input; no side effects performed."""


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative,str) or not relative or '\\' in relative or '\x00' in relative:
        raise LibraryError('Invalid relative path')
    if relative.startswith('/') or re.match(r'^[A-Za-z]:',relative):
        raise LibraryError('Absolute path is not allowed')
    parts = relative.split('/')
    if any(part in ('','.', '..') for part in parts):
        raise LibraryError('Path traversal or empty segment')
    base = Path(root).absolute()
    # Reject symlinks in the root as well as in the requested path.
    for p in [base, *base.parents]:
        if p.is_symlink(): raise LibraryError('Symlink root is not allowed')
    p = base
    for part in parts:
        p = p / part
        if p.is_symlink(): raise LibraryError('Symlink reference is not allowed')
    if not p.resolve(strict=False).is_relative_to(base.resolve()):
        raise LibraryError('Path escapes library root')
    return p


def _duplicates(pairs):
    d = {}
    for k,v in pairs:
        if k in d: raise LibraryError('Duplicate JSON key: '+k)
        d[k] = v
    return d


def read_json(path: Path) -> Any:
    if path.is_symlink(): raise LibraryError('Symlink JSON input')
    if path.stat().st_size > MAX_JSON_BYTES: raise LibraryError('JSON input too large')
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_duplicates,
                          parse_constant=lambda x: (_ for _ in ()).throw(LibraryError('Non-finite JSON number')))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise LibraryError('Invalid UTF-8 JSON') from exc


def decimal(value: Any) -> Decimal:
    if isinstance(value,bool) or not isinstance(value,(str,int)):
        raise LibraryError('Amounts must be decimal strings or integers, not bool/float')
    try: d=Decimal(value)
    except InvalidOperation as exc: raise LibraryError('Invalid decimal amount') from exc
    if not d.is_finite(): raise LibraryError('Non-finite decimal')
    return d


def nonnegative(value: Any) -> Decimal:
    n=decimal(value)
    if n<0: raise LibraryError('Negative amount/duration')
    return n


def integer(v: Any, *, positive: bool=False) -> int:
    if isinstance(v,bool) or not isinstance(v,int) or v < (1 if positive else 0):
        raise LibraryError('Expected a non-negative integer' if not positive else 'Expected a positive integer')
    return v


def money(v: Decimal) -> str:
    return str(v.quantize(Decimal('.01')))


def load_registry(root: Path=DEFAULT_ROOT) -> dict:
    data=read_json(safe_path(root,'REGISTRY.json'))
    if not isinstance(data,dict) or data.get('schema_version')!=2:
        raise LibraryError('Unsupported registry schema')
    if not isinstance(data.get('competencies'),list): raise LibraryError('Missing competency index')
    return data


def list_competencies(root: Path=DEFAULT_ROOT, office: str|None=None) -> list[dict]:
    if office is not None and office not in OFFICES: raise LibraryError('Unknown office')
    return [dict(id=r['id'],title=r['title'],offices=r['offices'],status=r['status'],
                 auto_selectable=r['auto_selectable'],version=r['version'])
            for r in load_registry(root)['competencies'] if office is None or office in r['offices']]


def resolve(competence_id: str, *, experimental: bool=False, root: Path=DEFAULT_ROOT) -> dict:
    rows=[r for r in load_registry(root)['competencies'] if r['id']==competence_id]
    if len(rows)!=1: raise LibraryError('Unknown or duplicate competency')
    row=rows[0]
    if row.get('status')!='curated' or row.get('kind')!='professional_method' or row.get('auto_selectable') is not True:
        raise LibraryError('Method is not curated/available for ordinary office use')
    # Load only the selected method and decision/output contract, not all cases.
    files={name:safe_path(root,row['directory']+'/'+name).read_text(encoding='utf-8')
           for name in ('METHOD.md','DECISIONS.md','OUTPUT.md')}
    return {'status':'loaded_curated_method','id':competence_id,
            'auto_selectable':True,'files':files,
            'canonical_aco_references':row['existing_aco_paths'],
            'limits':'Loading a curated method is not professional validation, model training, provider execution or technical skill promotion.'}


def validate(root: Path=DEFAULT_ROOT) -> dict:
    errors=[]
    registry=load_registry(root)
    sources=read_json(safe_path(root,'SOURCES.json'))['sources']
    srcids={s['id'] for s in sources}
    if len(srcids)!=len(sources): errors.append('Duplicate source IDs')
    seen=set(); example_count=0
    if registry.get('baseline',{}).get('aco_version')!='1.0.6': errors.append('Unexpected ACO baseline')
    if registry.get('policy',{}).get('changes_technical_skill_registry') is not False:
        errors.append('Technical skill registry must be preserved')
    for s in sources:
        if not s.get('url','').startswith('https://'): errors.append('Non-HTTPS source: '+s['id'])
        if s.get('reuse',{}).get('content_bundled') is not False: errors.append('Upstream content bundled')
        if not s.get('review_scope') or not s.get('limits'): errors.append('Source scope/limits absent')
    for row in registry['competencies']:
        cid=row.get('id','')
        if not re.fullmatch(r'[a-z][a-z0-9-]{2,63}',cid): errors.append('Invalid competency ID')
        if cid in seen: errors.append('Duplicate competency: '+cid)
        seen.add(cid)
        if row.get('status')!='curated' or row.get('auto_selectable') is not True or row.get('kind')!='professional_method':
            errors.append('Invalid curated method status: '+cid)
        if not row.get('offices') or not set(row['offices'])<=OFFICES: errors.append('Unknown/empty offices: '+cid)
        if not row.get('source_ids') or not set(row['source_ids'])<=srcids: errors.append('Unknown/empty sources: '+cid)
        for rel in row.get('existing_aco_paths',[]):
            safe_path(root,rel) # safety only; existence checked against full checkout separately
        for name in PARTS:
            p=safe_path(root,row['directory']+'/'+name)
            if not p.is_file() or not p.read_bytes().strip(): errors.append('Missing/empty: '+cid+'/'+name)
        if errors and not safe_path(root,row['directory']+'/EVALS.json').exists(): continue
        ev=read_json(safe_path(root,row['directory']+'/EVALS.json'))
        if ev.get('independent_validation') is not False: errors.append('False independence claim: '+cid)
        if ev.get('qualitative_status')!='development_examples_not_independent_validation':
            errors.append('Unsupported quality claim: '+cid)
        examples=ev.get('worked_examples',[]); example_count+=len(examples)
        if len(examples)<2: errors.append('Insufficient worked examples: '+cid)
        for x in examples:
            if not all(isinstance(x.get(k),str) and x[k].strip() for k in ('brief','weak','application','commentary','limits')):
                errors.append('Incomplete worked example: '+cid)
        if not ev.get('new_case_brief') or ev.get('new_case_status')!='not_run':
            errors.append('Future evaluation scope misstated: '+cid)
    return {'status':'valid' if not errors else 'invalid','competencies':len(seen),
            'sources':len(sources),'worked_examples':example_count,'errors':errors,
            'scope':'File integrity, links and declared status only; not professional competence.'}


def check_baseline(checkout: Path, root: Path=DEFAULT_ROOT) -> dict:
    """Read-only check against a real complete checkout. Never makes placeholder files."""
    checkout=Path(checkout)
    version=safe_path(checkout,'VERSION')
    if not version.is_file() or version.read_text().strip()!='1.0.7':
        raise LibraryError('Target must be integrated ACO 1.0.7')
    required={p for r in load_registry(root)['competencies'] for p in r['existing_aco_paths']}
    missing=[p for p in sorted(required) if not safe_path(checkout,p).is_file()]
    policy=read_json(safe_path(checkout,'config/skill-policy.json'))
    p=policy.get('promotion',{})
    if (p.get('minimum_benchmark_cases',0)<20 or p.get('minimum_score',0)<95 or
        p.get('maximum_critical_failures')!=0 or not all(p.get(x) is True for x in
        ('requires_explicit_approval','requires_rollback_ref','requires_frozen_first_run'))):
        raise LibraryError('Existing promotion safeguards absent or weakened')
    return {'status':'compatible_integrated' if not missing else 'incompatible','missing':missing,
            'scope':'Version, named paths and policy only; not a full ACO regression run.'}


def timeline(data: dict) -> dict:
    fps=data['fps']
    if not isinstance(fps,list) or len(fps)!=2: raise LibraryError('fps must be [numerator, denominator]')
    rate=Fraction(integer(fps[0],positive=True),integer(fps[1],positive=True))
    frames=integer(data['duration_frames'],positive=True)
    tracks=data['tracks']
    if not isinstance(tracks,list) or not tracks: raise LibraryError('No timeline tracks')
    ids=set(); gaps=[]
    for track in tracks:
        cursor=0
        if not track.get('clips'): raise LibraryError('Empty track')
        for clip in track['clips']:
            cid=clip['id']
            if not isinstance(cid,str) or not cid or cid in ids: raise LibraryError('Duplicate/invalid clip ID')
            ids.add(cid)
            start=integer(clip['start']); end=integer(clip['end'])
            if not 0<=start<end<=frames: raise LibraryError('Clip outside timeline or empty interval')
            if start<cursor and not track.get('allow_overlap',False): raise LibraryError('Unapproved overlap')
            if start>cursor: gaps.append([track['id'],cursor,start])
            cursor=max(cursor,end)
        if cursor<frames: gaps.append([track['id'],cursor,frames])
        if track.get('continuous',False) and any(g[0]==track['id'] for g in gaps):
            raise LibraryError('Gap in a declared continuous track')
    expected=data.get('expected_seconds')
    seconds=Fraction(frames,1)/rate
    if expected is not None and seconds!=Fraction(str(expected)):
        raise LibraryError('Duration does not equal requested seconds at this frame rate')
    return {'status':'checked','duration_frames':frames,'duration_seconds':str(seconds),
            'clip_count':len(ids),'declared_gaps':gaps,'scope':'Timing arithmetic, not editorial quality.'}


def schedule(tasks: list[dict]) -> dict:
    if not isinstance(tasks,list) or not tasks or len(tasks)>500: raise LibraryError('Invalid task list')
    rows={}
    for t in tasks:
        tid=t['id']
        if not isinstance(tid,str) or not tid or tid in rows: raise LibraryError('Duplicate/invalid task ID')
        nonnegative(t['duration'])
        if not isinstance(t.get('depends_on'),list): raise LibraryError('Dependencies must be a list')
        if len(set(t['depends_on']))!=len(t['depends_on']): raise LibraryError('Duplicate dependency')
        rows[tid]=t
    for t in rows.values():
        if set(t['depends_on'])-rows.keys(): raise LibraryError('Unknown dependency')
    done={}; pending=dict(rows)
    while pending:
        ready=[k for k,t in pending.items() if all(d in done for d in t['depends_on'])]
        if not ready: raise LibraryError('Dependency cycle')
        for k in ready:
            t=pending.pop(k); start=max((done[d]['end'] for d in t['depends_on']),default=Decimal(0))
            done[k]={'start':start,'end':start+nonnegative(t['duration'])}
    total=max(t['end'] for t in done.values())
    return {'status':'checked','duration':str(total),'tasks':{k:{f:str(v) for f,v in t.items()} for k,t in done.items()},
            'scope':'Precedence-only earliest schedule; no resource leveling, calendar or approval inferred.'}


def budget(data: dict) -> dict:
    if not isinstance(data.get('currency'),str) or not re.fullmatch('[A-Z]{3}',data['currency']):
        raise LibraryError('Explicit three-letter currency required')
    revenue=nonnegative(data['revenue']); base=nonnegative(data['baseline_cost'])
    actual=nonnegative(data['actual']); committed=nonnegative(data['committed_remaining']); estimate=nonnegative(data['uncommitted_remaining'])
    total=actual+committed+estimate; margin=revenue-total
    balance=decimal(data['opening_cash']); periods=[]
    for p in data['cash_periods']:
        if p.get('currency',data['currency'])!=data['currency']: raise LibraryError('Mixed currencies require an explicit conversion model')
        balance+=nonnegative(p['receipts'])-nonnegative(p['payments'])
        periods.append({'id':p['id'],'closing_cash':money(balance),'negative':balance<0})
    return {'status':'checked','currency':data['currency'],'forecast_cost':money(total),
            'cost_variance':money(total-base),'margin':money(margin),
            'margin_percent':money(margin/revenue*100) if revenue else None,'cash':periods,
            'scope':'Arithmetic on supplied non-overlapping categories; not tax/accounting advice.'}


def portfolio(data: dict) -> dict:
    cap=nonnegative(data['budget']); projects=data['projects']
    if not isinstance(projects,list) or not 1<=len(projects)<=15: raise LibraryError('Use 1..15 projects')
    ids=[p['id'] for p in projects]
    if len(set(ids))!=len(ids): raise LibraryError('Duplicate project ID')
    feasible=[]
    for n in range(1,len(projects)+1):
        for subset in itertools.combinations(projects,n):
            cost=sum((nonnegative(p['cost']) for p in subset),Decimal(0))
            selected={p['id'] for p in subset}
            if cost>cap: continue
            if any(set(p.get('requires',[]))-selected for p in subset): continue
            if any(len(set(group)&selected)>1 for group in data.get('mutually_exclusive',[])): continue
            feasible.append({'ids':sorted(selected),'cost':money(cost)})
    return {'status':'checked','feasible':feasible,'recommendation':None,
            'scope':'Feasibility, not a preference ranking or proof of expected impact.'}


def _index(rows, key='id') -> dict:
    if not isinstance(rows,list): raise LibraryError('Expected a list')
    out={}
    for r in rows:
        v=r[key]
        if not isinstance(v,str) or not v or v in out: raise LibraryError('Duplicate/invalid ID')
        out[v]=r
    return out


def audit(kind: str, data: dict) -> dict:
    """Check explicit invariants in annotated records, NOT natural-language truth."""
    if not isinstance(data,dict): raise LibraryError('Record must be an object')
    if kind=='timeline': return timeline(data)
    if kind=='schedule': return schedule(data['tasks'])
    if kind=='budget': return budget(data)
    if kind=='portfolio': return portfolio(data)
    errors=[]
    def require(condition: bool, msg: str):
        if not condition: errors.append(msg)
    if kind=='administration':
        messages=_index(data['messages'])
        for a in data['activities']:
            proof=messages.get(a['commitment_ref'],{})
            require(proof.get('kind')=='commitment','availability/proposal is not a commitment')
            require(a.get('owner')==proof.get('owner'),'owner not supported by commitment')
            if a.get('deadline') is not None:
                dp=messages.get(a.get('deadline_ref'),{})
                require(dp.get('kind')=='confirmed_deadline' and dp.get('deadline')==a['deadline'] and dp.get('activity')==a['id'],'deadline not confirmed for this activity')
        require(data.get('sent') is False,'no send receipt supplied')
    elif kind=='motion-transfer':
        events=_index(data['source_events']); mapped=_index(data['target_events'],'source_id')
        require(set(mapped)==set(events),'missing or extraneous source event')
        allowed=set(data.get('authorized_omissions',[])); evidence=set(data['available_evidence'])
        duration=decimal(data['target_duration']); previous_start=Decimal(-1)
        for sid,t in mapped.items():
            if sid not in events: continue
            s=events[sid]
            if t.get('disposition')=='omitted':
                require(sid in allowed and bool(t.get('reason')),'unauthorized omission');continue
            require(t.get('certainty')=='observed','unresolved event cannot be marked transferred')
            require(bool(t.get('evidence')) and set(t.get('evidence',[]))<=evidence,'missing/unknown frame evidence')
            start,end=map(decimal,t['interval'])
            require(0<=start<end<=duration,'invalid target interval')
            if s.get('track')=='subject':
                require(start>=previous_start,'subject event order reversed');previous_start=start
            quote=t.get('prompt_excerpt','')
            require(bool(quote) and quote in data['prompt'],'event excerpt absent from prompt')
        require(data.get('generation_verified') is False,'a prompt/fixture cannot verify AI generation')
    elif kind=='claims':
        sources=_index(data['sources'])
        for c in data['claims']:
            refs=c.get('source_ids',[])
            require(bool(refs) and set(refs)<=sources.keys(),'claim source missing')
            groups={sources[s]['origin_group'] for s in refs if s in sources}
            require(c.get('independent_origins')==len(groups),'source independence overstated')
            if c.get('status')=='verified':
                require(c.get('source_status')=='observed' and c.get('material_qualifiers_preserved') is True,'unsupported certainty or lost qualifier')
        require(data.get('new_unverified_facts_added') is False,'revision adds unverified facts')
    elif kind=='research':
        obs=_index(data['observations'])
        for f in data['findings']:
            require(bool(f.get('evidence_refs')) and set(f.get('evidence_refs',[]))<=obs.keys(),'finding has unknown observations')
            require(bool(f.get('uncertainties')),'uncertainty omitted')
            require(f.get('population_prevalence_claim') is False,'sample generalized to population')
        require(data.get('conflicts_discarded') is False,'conflicting notes discarded')
    elif kind=='visual':
        require(data.get('inspection_mode') in {'rendered','source_only','provided_description'},'unknown inspection mode')
        for d in data['directions']:
            require(bool(d.get('preserved_identity')) and bool(d.get('task')),'identity or task absent')
            require(bool(d.get('correction')) and bool(d.get('reason')),'unmotivated correction')
        require(len({x['structure'] for x in data['directions']})==len(data['directions']),'one template imposed on all directions')
        require(not(data['inspection_mode']=='source_only' and data.get('visual_review_complete')),'source inspection claimed as rendered review')
    elif kind=='accessibility':
        names=[x.get('name') for x in data['controls']]
        require(all(isinstance(x,str) and x.strip() for x in names),'unnamed control')
        for e in data['errors']:
            require(e.get('field') in data['field_ids'] and bool(e.get('repair')) and bool(e.get('association')),'unlinked or unrepairable error')
        require(data.get('keyboard_complete') is True,'keyboard path not completed')
        require(data.get('global_conformance_claim') is False,'single fixture is not global conformance')
        require(not(data.get('screen_reader_pass') and not data.get('screen_reader_receipt')),'screen reader claim lacks receipt')
    elif kind=='ui-motion':
        require(len(data['variants'])==3,'three registers required')
        for v in data['variants']:
            require(v.get('final_state')==data['expected_final'],'final state differs across variants')
            require(v.get('reduced_final_state')==data['expected_final'],'reduced-motion loses state')
            require(v.get('interruptible') is True,'unhandled interrupted transition')
            require(v.get('reduced_transform')=='none','nonessential transform not removed')
    elif kind=='curating':
        works=set(data['available_work_ids']); shows=data['exhibitions']
        require(len(shows)==2,'two curatorial alternatives required')
        for s in shows:
            require(set(s['order'])<=works and len(s['order'])==len(set(s['order'])),'unknown or duplicate work')
            require(bool(s.get('thesis')) and bool(s.get('spatial_consequence')),'thesis or spatial consequence missing')
        require(shows[0]['order']!=shows[1]['order'],'no structural difference between alternatives')
        require(data.get('loans_confirmed') is False,'synthetic availability is not loan approval')
    elif kind=='criticism':
        evidence=set(data['visible_evidence_ids'])
        require(len(data['readings'])==2,'two readings required')
        for r in data['readings']:
            require(bool(r.get('evidence_ids')) and set(r.get('evidence_ids',[]))<=evidence,'interpretation lacks visible support')
            require(bool(r.get('counterevidence')),'reading cannot be challenged')
        require(data.get('artist_intent_asserted') is False,'artist intent invented')
        require(bool(data.get('experiment')),'no discriminating studio experiment')
    elif kind=='archive':
        src=_index(data['sources'])
        for f in data['fields']:
            require(bool(f.get('source_ids')) and set(f.get('source_ids',[]))<=src.keys(),'field provenance absent')
            require(not(f.get('conflict') and f.get('status')=='confirmed' and not f.get('resolution_ref')),'conflict silently resolved')
        require(data.get('ownership_inferred_from_location') is False,'location does not prove ownership')
        require(data.get('spectrum_compliance_claim') is False,'unlicensed/unverified standards claim')
    elif kind=='audience':
        require(data.get('participation') is None or data.get('attendance_evidence') is not None,'reach substituted for attendance')
        require(data.get('causal_claim') is False,'causal impact not established')
        require(data.get('sensitive_profiles_inferred') is False,'sensitive audience profiling')
        require(len({m['entry_point'] for m in data['messages']})>1,'audience messages do not differ')
        require(len({m['project_promise'] for m in data['messages']})==1,'project promise contradicts across audiences')
    elif kind=='copy':
        facts=set(data['verified_fact_ids'])
        for c in data['material_claims']:
            require(bool(c.get('fact_ids')) and set(c.get('fact_ids',[]))<=facts,'unsupported marketing claim')
        require(set(data['changed_units'])<=set(data['authorized_units']),'point edit expands scope')
        for x in data.get('declined_claims',[]): require(bool(x.get('missing_evidence')),'declined claim has no unlock evidence')
    elif kind=='legal':
        clauses=set(data['clause_ids'])
        for f in data['findings']:
            require(bool(f.get('clause_refs')) and set(f.get('clause_refs',[]))<=clauses,'legal finding lacks clause locator')
            require(not(f.get('legal_rule') and not f.get('primary_source')),'legal rule without primary source')
        for rule in data.get('notification_rules',[]):
            require(not(rule['role']=='processor' and rule.get('universal_deadline_hours')==72),'blanket processor 72-hour rule is incorrect')
        require(data.get('legal_validity_certified') is False,'legal validity not certified')
        require(data.get('signed_or_sent') is False,'no authorized signing or sending receipt')
    elif kind=='negotiation':
        require(len(data['packages'])==3,'three offers required')
        for p in data['packages']:
            require(all(p.get(k) is not None for k in ('price','scope','duration','rights')),'offer omits a material variable')
            require(not p.get('concession') or bool(p.get('counterpart')),'unconditional concession')
        require(data.get('alternative_fabricated') is False,'fabricated bargaining alternative')
        require(data.get('market_rate_claim') is False,'illustrative prices are not market rates')
    elif kind=='people':
        require(data.get('protected_traits_used') is False,'protected traits or proxies used')
        require(data.get('automated_hiring_decision') is False,'human hiring review required')
        for r in data['ratings']:
            require(not (r.get('score') is not None and not r.get('evidence_ids')),'missing evidence treated as a score')
        require(data.get('common_criteria') is True,'non-comparable candidate criteria')
    elif kind=='evaluation':
        require(not(data.get('same_author') and data.get('independent_validation')),'same-author cases called independent')
        require(not(data.get('mechanical_tests_only') and data.get('professional_validation')),'mechanical tests called professional validation')
        require(data.get('promoted') is False,'this package never promotes a competency')
        require(data.get('first_failures_preserved') is True,'first-run failures suppressed')
    else:
        raise LibraryError('Unknown audit kind: '+kind)
    return {'status':'checked' if not errors else 'failed','errors':errors,
            'scope':'Deterministic invariants on supplied annotations; not semantic truth or independent skill validation.'}


def main(argv: list[str]|None=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=DEFAULT_ROOT,help='Canonical competence directory')
    sub=p.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('list');q.add_argument('--office',choices=sorted(OFFICES))
    q=sub.add_parser('show');q.add_argument('--id',required=True);q.add_argument('--experimental',action='store_true')
    sub.add_parser('check')
    q=sub.add_parser('baseline-check');q.add_argument('--checkout',type=Path,required=True)
    q=sub.add_parser('audit');q.add_argument('--kind',required=True);q.add_argument('--input',type=Path,required=True)
    a=p.parse_args(argv)
    try:
        if a.cmd=='list': result={'competencies':list_competencies(a.root,a.office)}
        elif a.cmd=='show': result=resolve(a.id,experimental=a.experimental,root=a.root)
        elif a.cmd=='check': result=validate(a.root)
        elif a.cmd=='baseline-check': result=check_baseline(a.checkout,a.root)
        else: result=audit(a.kind,read_json(a.input))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result.get('status') in {'invalid','failed','incompatible'} else 0
    except (LibraryError, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status':'error','error':str(e)},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
