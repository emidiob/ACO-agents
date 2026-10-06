"""ACO 1.0 technical Skill Registry and structured skill-learning gates."""
from __future__ import annotations
import hashlib,json,os,re
from collections import Counter
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, VERSION, no_symlinks, read_json, safe_path, write_json

def _policy(root=None):
    root=(root or ROOT).expanduser().absolute();data=read_json(root/'config/skill-policy.json')
    if data.get('schema_version')!=1:raise ACOError('Unsupported skill-policy schema')
    if data.get('aco_version')!=VERSION and root==ROOT:raise ACOError('Skill policy version mismatch')
    return data

def load_skill_registry(root=None):
    root=(root or ROOT).expanduser().absolute();data=read_json(root/'registry/skills.json')
    if data.get('schema_version')!=1:raise ACOError('Unsupported skill registry schema')
    if data.get('aco_version')!=VERSION and root==ROOT:raise ACOError('Skill registry version mismatch')
    if not isinstance(data.get('skills'),list):raise ACOError('Skill registry skills must be a list')
    return data

def _walk_forbidden(value,forbidden,path=''):
    if isinstance(value,dict):
        for k,v in value.items():
            if str(k).lower() in forbidden:return path+('.' if path else '')+str(k)
            found=_walk_forbidden(v,forbidden,path+('.' if path else '')+str(k))
            if found:return found
    elif isinstance(value,list):
        for i,v in enumerate(value):
            found=_walk_forbidden(v,forbidden,f'{path}[{i}]')
            if found:return found
    return None

def _canonical_hash(value):
    obj={k:v for k,v in value.items() if k not in {'candidate_sha256','promoted_at'}};raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();return hashlib.sha256(raw).hexdigest()

def _tokens(text):return {x for x in re.findall(r'[a-z0-9]{2,}',text.lower())}

def skill_registry_check(root=None):
    root=(root or ROOT).expanduser().absolute();registry=load_skill_registry(root);policy=_policy(root);lifecycle=set(policy.get('lifecycle',[]));seen=set();errors=[];active=0;candidates=0
    for row in registry['skills']:
        if not isinstance(row,dict):errors.append('skill index entry must be object');continue
        sid=row.get('skill_id')
        if not isinstance(sid,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{2,127}',sid):errors.append('invalid skill_id: '+str(sid));continue
        if sid in seen:errors.append('duplicate skill_id: '+sid)
        seen.add(sid)
        if row.get('status') not in lifecycle:errors.append(f'{sid}: invalid lifecycle status')
        body_path=row.get('body_path')
        if not isinstance(body_path,str):errors.append(f'{sid}: body_path required');continue
        try:path=safe_path(root,body_path)
        except ACOError as exc:errors.append(f'{sid}: {exc}');continue
        if not path.is_file():errors.append(f'{sid}: missing body {body_path}');continue
        body=read_json(path)
        if body.get('skill_id')!=sid or body.get('version')!=row.get('version'):errors.append(f'{sid}: registry/body identity mismatch')
        if row.get('status') in set(policy.get('active_states',[])):
            active+=1
            if body.get('source_status') not in {'verified_official','verified_primary','validated_internal'}:errors.append(f'{sid}: active skill requires verified source status')
        if row.get('status') in {'candidate','candidate_unverified','testing'}:candidates+=1
        te=row.get('token_estimate')
        if not isinstance(te,int) or isinstance(te,bool) or te<=0:errors.append(f'{sid}: token_estimate must be positive integer')
    return {'status':'valid' if not errors else 'invalid','aco_version':VERSION,'skills':len(registry['skills']),'active_skills':active,'candidate_skills':candidates,'errors':errors}

def skill_search(query='',*,tags=None,limit=5,include_candidates=False,root=None):
    if not isinstance(query,str):raise ACOError('query must be a string')
    if tags is not None and (not isinstance(tags,list) or any(not isinstance(x,str) for x in tags)):raise ACOError('tags must be a string list')
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1<=limit<=20:raise ACOError('limit must be 1..20')
    registry=load_skill_registry(root);policy=_policy(root);active_states=set(policy.get('active_states',[]));q=_tokens(query);wanted_tags={x.lower() for x in (tags or [])};rows=[]
    for row in registry['skills']:
        selectable=row.get('status') in active_states
        if not selectable and not include_candidates:continue
        hay_tags={str(x).lower() for x in row.get('tags',[])};title_tokens=_tokens(str(row.get('title','')));hay=_tokens(' '.join([str(row.get('skill_id','')),str(row.get('title','')),str(row.get('summary','')),' '.join(hay_tags)]));overlap=len(q&hay);title_overlap=len(q&title_tokens);tag_overlap=len(wanted_tags&hay_tags);exact_bonus=4 if query and query.lower() in str(row.get('title','')).lower() else 0;coverage=overlap/max(1,len(q)) if q else 1.0;score=overlap*3+title_overlap*2+tag_overlap*5+exact_bonus+(2 if selectable else 0)
        if q and len(q)>=2 and coverage<.5 and overlap<2 and tag_overlap==0:continue
        if (q or wanted_tags) and score<=0:continue
        rows.append({**row,'score':score,'selectable':selectable})
    rows.sort(key=lambda r:(-r['score'],not r['selectable'],-float(r.get('quality',0)),r['token_estimate'],r['skill_id']))
    return {'status':'ok','aco_version':VERSION,'query':query,'results':rows[:limit],'candidate_results_included':include_candidates,'policy':'Only validated/active skills are selectable by default. Candidate and unverified skills require explicit inspection.'}

def skill_resolve(skill_id,*,allow_candidate=False,root=None):
    if not isinstance(skill_id,str) or not skill_id.strip():raise ACOError('skill_id is required')
    root=(root or ROOT).expanduser().absolute();registry=load_skill_registry(root);policy=_policy(root);matches=[x for x in registry['skills'] if x.get('skill_id')==skill_id]
    if not matches:raise ACOError('Unknown skill: '+skill_id)
    row=matches[0];selectable=row.get('status') in set(policy.get('active_states',[]))
    if not selectable and not allow_candidate:raise ACOError(f'{skill_id} is {row.get("status")}; candidate/unverified skills cannot be auto-resolved')
    body=read_json(safe_path(root,row['body_path']))
    return {'status':'resolved','aco_version':VERSION,'selectable':selectable,'skill':row,'body':body,'policy':'Skill resolution loads one selected skill body, not the whole registry or pack.'}

def skill_candidate_check(candidate,root=None):
    if not isinstance(candidate,dict):raise ACOError('Skill candidate must be an object')
    policy=_policy(root);errors=[];forbidden={str(x).lower() for x in policy.get('forbidden_reasoning_fields',[])};found=_walk_forbidden(candidate,forbidden)
    if found:errors.append('forbidden reasoning field: '+found)
    if candidate.get('schema_version')!=1:errors.append('schema_version must be 1')
    sid=candidate.get('skill_id')
    if not isinstance(sid,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{2,127}',sid):errors.append('valid skill_id required')
    if not isinstance(candidate.get('scope_id'),str) or not candidate.get('scope_id','').strip():errors.append('scope_id required')
    if candidate.get('status') not in {'candidate','candidate_unverified','testing'}:errors.append('candidate status must be candidate, candidate_unverified or testing')
    method=candidate.get('method')
    if not isinstance(method,list) or not method or any(not isinstance(x,str) or not x.strip() for x in method):errors.append('method must be a non-empty string list')
    evidence=candidate.get('evidence',[])
    if not isinstance(evidence,list) or any(not isinstance(x,dict) for x in evidence):errors.append('evidence must be a list of objects')
    else:
        for i,ev in enumerate(evidence):
            if not isinstance(ev.get('source_ref'),str) or not ev.get('source_ref','').strip():errors.append(f'evidence[{i}].source_ref required')
            if ev.get('outcome') not in {'success','failure','mixed','source_verified'}:errors.append(f'evidence[{i}].outcome invalid')
    computed=_canonical_hash(candidate);supplied=candidate.get('candidate_sha256')
    if supplied is not None and supplied!=computed:errors.append('candidate_sha256 does not match candidate content')
    return {'status':'valid' if not errors else 'invalid','aco_version':VERSION,'candidate_sha256':computed,'errors':errors,'evidence_count':len(evidence) if isinstance(evidence,list) else 0,'distinct_sources':len({e.get('source_ref') for e in evidence if isinstance(e,dict) and e.get('source_ref')}) if isinstance(evidence,list) else 0}

def skill_learn(packet,root=None):
    if not isinstance(packet,dict):raise ACOError('Skill learning packet must be an object')
    policy=_policy(root);forbidden={str(x).lower() for x in policy.get('forbidden_reasoning_fields',[])};found=_walk_forbidden(packet,forbidden)
    if found:raise ACOError('Forbidden reasoning field: '+found)
    sid=packet.get('skill_id');scope=packet.get('scope_id')
    if not isinstance(sid,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{2,127}',sid):raise ACOError('valid skill_id required')
    if not isinstance(scope,str) or not scope.strip():raise ACOError('scope_id required')
    observations=packet.get('observations',[])
    if not isinstance(observations,list) or any(not isinstance(x,dict) for x in observations):raise ACOError('observations must be a list of objects')
    support=len(observations);distinct=len({x.get('source_ref') for x in observations if isinstance(x.get('source_ref'),str) and x['source_ref'].strip()});lp=policy.get('learning',{});min_support=int(lp.get('minimum_support',3));min_sources=int(lp.get('minimum_distinct_sources',2))
    if support<min_support or distinct<min_sources:return {'status':'insufficient_evidence','aco_version':VERSION,'candidate':None,'support':support,'distinct_sources':distinct,'required_support':min_support,'required_distinct_sources':min_sources}
    successes=[x for x in observations if x.get('outcome') in {'success','mixed'}];rule_counts=Counter();failure_counts=Counter()
    for obs in successes:
        rules=obs.get('rules',[])
        if not isinstance(rules,list) or any(not isinstance(x,str) for x in rules):raise ACOError('observation.rules must be a string list')
        rule_counts.update(set(x.strip() for x in rules if x.strip()))
    for obs in observations:
        fm=obs.get('failure_modes',[])
        if not isinstance(fm,list) or any(not isinstance(x,str) for x in fm):raise ACOError('observation.failure_modes must be a string list')
        failure_counts.update(set(x.strip() for x in fm if x.strip()))
    threshold=float(lp.get('minimum_rule_consensus',.67));denominator=max(1,len(successes));rules=sorted([r for r,count in rule_counts.items() if count/denominator>=threshold])
    if not rules:return {'status':'no_consensus','aco_version':VERSION,'candidate':None,'support':support,'distinct_sources':distinct}
    failures=sorted([r for r,count in failure_counts.items() if count/max(1,support)>=.34]);candidate={'schema_version':1,'skill_id':sid,'scope_id':scope,'title':packet.get('title',sid.replace('.',' ').title()),'version':packet.get('version','0.1.0'),'status':'candidate','method':rules,'failure_modes':failures,'inputs':packet.get('inputs',[]),'output_contract':packet.get('output_contract',{}),'evidence':[{'source_ref':x.get('source_ref'),'outcome':x.get('outcome')} for x in observations],'source_status':'structured_internal_evidence','rollback_ref':packet.get('rollback_ref')};candidate['candidate_sha256']=_canonical_hash(candidate);check=skill_candidate_check(candidate,root)
    if check['status']!='valid':raise ACOError('Generated candidate invalid: '+'; '.join(check['errors']))
    return {'status':'candidate_proposed','aco_version':VERSION,'candidate':candidate,'support':support,'distinct_sources':distinct,'execute':False,'policy':'Learning produces a candidate only. It does not update the active skill registry.'}

def _skill_state_root(state_root=None,env=None):
    env=dict(os.environ if env is None else env)
    if state_root is None:
        configured=env.get('ACO_HOME','').strip();state_root=Path(configured) if configured else Path.home()/'.local/share/aco'
    out=state_root.expanduser().absolute();no_symlinks(out);return out

def skill_candidate_store(candidate,*,state_root=None,apply=False,env=None,root=None):
    check=skill_candidate_check(candidate,root)
    if check['status']!='valid':raise ACOError('Skill candidate is invalid: '+'; '.join(check['errors']))
    if candidate.get('status') not in {'candidate','candidate_unverified','testing'}:raise ACOError('Only non-active skill candidates may enter the private inbox')
    state=_skill_state_root(state_root,env);store_path=state/'skills'/'candidates.json';record={'candidate_sha256':check['candidate_sha256'],'skill_id':candidate['skill_id'],'scope_id':candidate['scope_id'],'candidate':candidate,'source_release':VERSION}
    if not apply:return {'status':'planned','aco_version':VERSION,'applied':False,'state_root':str(state),'store_path':str(store_path),'candidate_sha256':check['candidate_sha256'],'skill_id':candidate['skill_id'],'active_registry_mutated':False,'policy':'Candidate persistence is private state, not activation. Apply only to an authorized ACO_HOME; promotion remains a later versioned release change.'}
    if store_path.exists():
        store=read_json(store_path)
        if store.get('schema_version')!=1 or store.get('store')!='aco-skill-candidates' or not isinstance(store.get('records'),list):raise ACOError('Invalid ACO skill candidate store')
    else:store={'schema_version':1,'store':'aco-skill-candidates','records':[]}
    hashes={x.get('candidate_sha256') for x in store['records'] if isinstance(x,dict)}
    if check['candidate_sha256'] in hashes:return {'status':'already_present','aco_version':VERSION,'applied':False,'state_root':str(state),'store_path':str(store_path),'candidate_sha256':check['candidate_sha256'],'skill_id':candidate['skill_id'],'records':len(store['records']),'active_registry_mutated':False}
    store['records'].append(record);write_json(store_path,store);return {'status':'stored','aco_version':VERSION,'applied':True,'state_root':str(state),'store_path':str(store_path),'candidate_sha256':check['candidate_sha256'],'skill_id':candidate['skill_id'],'records':len(store['records']),'active_registry_mutated':False,'policy':'Stored in private ACO state only. The active registry was not changed.'}

def skill_candidate_store_status(*,state_root=None,env=None):
    state=_skill_state_root(state_root,env);store_path=state/'skills'/'candidates.json'
    if not store_path.exists():return {'status':'empty','aco_version':VERSION,'state_root':str(state),'store_path':str(store_path),'candidates':0,'skill_ids':[],'scopes':[]}
    store=read_json(store_path)
    if store.get('schema_version')!=1 or store.get('store')!='aco-skill-candidates' or not isinstance(store.get('records'),list):raise ACOError('Invalid ACO skill candidate store')
    records=store['records'];return {'status':'ok','aco_version':VERSION,'state_root':str(state),'store_path':str(store_path),'candidates':len(records),'skill_ids':sorted({x.get('skill_id') for x in records if isinstance(x,dict) and x.get('skill_id')}),'scopes':sorted({x.get('scope_id') for x in records if isinstance(x,dict) and x.get('scope_id')}),'candidate_sha256s':[x.get('candidate_sha256') for x in records if isinstance(x,dict) and x.get('candidate_sha256')]}

def skill_promotion_check(packet,root=None):
    if not isinstance(packet,dict):raise ACOError('Skill promotion packet must be an object')
    policy=_policy(root);candidate=packet.get('candidate')
    if not isinstance(candidate,dict):raise ACOError('candidate is required')
    check=skill_candidate_check(candidate,root);errors=list(check['errors']);expected_hash=check['candidate_sha256'];benchmark=packet.get('benchmark',{});approval=packet.get('approval',{})
    if not isinstance(benchmark,dict) or not isinstance(approval,dict):raise ACOError('benchmark and approval must be objects')
    pp=policy.get('promotion',{})
    if benchmark.get('candidate_sha256')!=expected_hash:errors.append('benchmark candidate hash mismatch')
    if int(benchmark.get('cases',0))<int(pp.get('minimum_benchmark_cases',20)):errors.append('benchmark case count below minimum')
    if float(benchmark.get('score',0.0))<float(pp.get('minimum_score',95.0)):errors.append('benchmark score below minimum')
    if int(benchmark.get('critical_failures',999))>int(pp.get('maximum_critical_failures',0)):errors.append('benchmark has critical failures')
    if pp.get('requires_frozen_first_run',True) and benchmark.get('frozen_before_first_run') is not True:errors.append('benchmark must be frozen before first run')
    if pp.get('requires_explicit_approval',True) and (approval.get('approved') is not True or approval.get('candidate_sha256')!=expected_hash or not approval.get('approval_ref')):errors.append('exact explicit approval required')
    if pp.get('requires_rollback_ref',True) and not candidate.get('rollback_ref'):errors.append('rollback_ref required')
    return {'status':'eligible' if not errors else 'blocked','aco_version':VERSION,'eligible':not errors,'candidate_sha256':expected_hash,'errors':errors,'execute':False,'policy':'Promotion eligibility never mutates the registry. Activation requires a deliberate versioned release change.'}

def _get(value,path):
    cur=value
    for part in path.split('.'):
        if isinstance(cur,dict) and part in cur:cur=cur[part]
        elif isinstance(cur,list) and part.isdigit() and int(part)<len(cur):cur=cur[int(part)]
        else:return None
    return cur

def skill_benchmark(path=None,root=None):
    root=(root or ROOT).expanduser().absolute();path=(path or root/'config/skill-benchmark.json').expanduser().absolute();data=read_json(path)
    if data.get('schema_version')!=1:raise ACOError('Unsupported skill benchmark schema')
    rows=[];critical=0
    for case in data.get('cases',[]):
        op=case.get('operation');error=None
        try:
            if op=='search':result=skill_search(case.get('query',''),tags=case.get('tags'),limit=case.get('limit',5),include_candidates=case.get('include_candidates',False),root=root)
            elif op=='candidate_check':result=skill_candidate_check(case.get('input',{}),root)
            elif op=='learn':result=skill_learn(case.get('input',{}),root)
            elif op=='promotion_check':result=skill_promotion_check(case.get('input',{}),root)
            elif op=='registry_check':result=skill_registry_check(root)
            else:raise ACOError('Unsupported skill benchmark operation: '+str(op))
            passed=not bool(case.get('expected_error',False))
            for key,expected in case.get('expected',{}).items():
                if _get(result,key)!=expected:passed=False
        except (ACOError,ValueError,TypeError) as exc:passed=bool(case.get('expected_error',False));result=None;error=str(exc)
        crit=bool(case.get('critical')) and not passed;critical+=int(crit);rows.append({'id':case.get('id'),'operation':op,'passed':passed,'critical_failure':crit,'error':error})
    if not rows:raise ACOError('Skill benchmark needs cases')
    score=round(100*sum(1 for x in rows if x['passed'])/len(rows),2);gate=data.get('gate',{});status='passed' if score>=float(gate.get('minimum_score',100)) and critical<=int(gate.get('maximum_critical_failures',0)) else 'failed'
    return {'status':status,'aco_version':VERSION,'cases':len(rows),'score':score,'critical_failures':critical,'rows':rows,'failures':[x for x in rows if not x['passed']]}
