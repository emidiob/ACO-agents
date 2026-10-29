#!/usr/bin/env python3
"""ACO 1.0.7: frozen procedural conformance for 20 professional Skill Registry entries.

This validator NEVER runs a language model or certifies independent professional
judgment. It does enforce 20 frozen synthetic checks per skill, a 95% threshold,
zero critical failures, SHA-256 case/body freezing, default resolution and exact
hash-bound approval before a release can mark each candidate promotion eligible.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from collections import Counter,defaultdict
from pathlib import Path

class ValidationError(ValueError):pass

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
 if not path.is_file() or path.is_symlink():raise ValidationError('Missing or symlinked file: '+str(path))
 return json.loads(path.read_text(encoding='utf-8'))

def run(root:Path,approval_ref:str|None=None)->dict:
 root=root.absolute()
 freeze=read(root/'release/v107-professional-skill-freeze.json')
 cases_path=root/'config/professional-skill-holdout.json';inputs=read(cases_path)
 if sha(cases_path)!=freeze['cases_sha256']:raise ValidationError('Frozen case hash changed')
 if not freeze.get('frozen_before_first_run') or freeze['case_count']!=400:raise ValidationError('Invalid first-run freeze metadata')
 additions=read(root/'registry/professional-skills-additions.json')['skills']
 if len(additions)!=20 or len({x['skill_id'] for x in additions})!=20:raise ValidationError('Expected twenty distinct skills')
 for row in additions:
  if row['status']!='validated':raise ValidationError('Professional skill is not marked validated')
  bodypath=root/row['body_path'];body=read(bodypath)
  if sha(bodypath)!=freeze['source_fingerprints'].get(row['skill_id']):raise ValidationError('Skill source changed after frozen benchmark: '+row['skill_id'])
  if body['skill_id']!=row['skill_id'] or body['status']!='validated' or body['source_status']!='validated_internal':raise ValidationError('Skill identity/status mismatch')
  if len(body.get('method',[]))<6 or not body.get('failure_modes') or not body.get('sources'):raise ValidationError('Incomplete skill body')
  if body['verification']['professional_quality_review']!='not independently assessed':raise ValidationError('False professional review claim')
 spec=importlib.util.spec_from_file_location('aco_competence_audit',root/'skills/aco-office-concierge/scripts/competence_library.py')
 module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
 known={r['skill_id'] for r in additions};counts=defaultdict(lambda:{'cases':0,'passes':0,'critical_failures':0,'failures':[]})
 case_ids=set()
 for case in inputs['cases']:
  cid=case['id'];sid=case['skill_id']
  if cid in case_ids or sid not in known:raise ValidationError('Duplicate case or unknown skill: '+cid)
  case_ids.add(cid);c=counts[sid];c['cases']+=1
  try:
   out=module.audit(case['kind'],case['record'])
   status=out['status'];error=None
  except (module.LibraryError,KeyError,TypeError,ValueError) as e:
   status='failed';error=str(e)
  passed=(case['expect']==status)
  if case['expect']=='failed' and status=='failed' and not error and not out.get('errors'):passed=False
  if passed:c['passes']+=1
  else:
   if case.get('critical'):c['critical_failures']+=1
   c['failures'].append({'id':cid,'expected':case['expect'],'actual':status,'error':error})
 if len(case_ids)!=400:raise ValidationError('Frozen set must contain 400 cases')
 for sid,c in counts.items():
  c['score']=round(c['passes']/c['cases']*100,2)
  if c['cases']<20 or c['score']<95.0 or c['critical_failures']!=0:raise ValidationError('Promotion benchmark failed: '+sid+': '+str(c))
 if set(counts)!=known:raise ValidationError('Skill without cases')
 release_gate='not_checked'
 if (root/'scripts/aco/skills.py').is_file():
  sys.path.insert(0,str(root/'scripts'))
  from aco.skills import skill_resolve,skill_registry_check,skill_promotion_check
  x=skill_registry_check(root)
  if (x['status'],x['skills'],x['active_skills'],x['candidate_skills'])!=('valid',64,34,30):raise ValidationError('Real ACO registry gate failed: '+str(x))
  for sid in known:
   if not skill_resolve(sid,root=root)['selectable']:raise ValidationError('Not selectable: '+sid)
  release_gate='baseline_and_skill_resolution_checked'
  if approval_ref:
   candidates=read(root/'config/professional-skill-promotions.json')['candidates']
   for record in candidates:
    sid=record['skill_id'];c=counts[sid]
    packet={'candidate':record['candidate'],'benchmark':{'candidate_sha256':record['candidate_sha256'],'cases':c['cases'],
      'score':c['score'],'critical_failures':c['critical_failures'],'frozen_before_first_run':True},
      'approval':{'approved':True,'candidate_sha256':record['candidate_sha256'],'approval_ref':approval_ref}}
    check=skill_promotion_check(packet,root=root)
    if check['status']!='eligible':raise ValidationError('Official promotion gate refused '+sid+': '+str(check['errors']))
   release_gate='official_promotion_check_passed_for_all_20'
 return {'status':'passed','aco_version':'1.0.7','skills':len(known),'total_cases':len(case_ids),'score':round(sum(x['passes'] for x in counts.values())/len(case_ids)*100,2),
   'critical_failures':sum(x['critical_failures'] for x in counts.values()),'per_skill':dict(sorted(counts.items())),
   'cases_sha256':freeze['cases_sha256'],'promotion_gate':release_gate,
   'scope':'Structured synthetic assertions only; not independent user testing, professional judgment validation, generative-output quality, or external provider verification.'}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--approval-ref')
 p.add_argument('--summary',action='store_true');a=p.parse_args()
 try:
  result=run(a.root,a.approval_ref)
  if a.summary:
   result=dict(result);result['per_skill']={k:{z:v[z] for z in ('cases','score','critical_failures')} for k,v in result['per_skill'].items()}
  print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except (ValidationError,KeyError,ValueError,OSError) as e:
  print(json.dumps({'status':'blocked','error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
