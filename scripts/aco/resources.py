"""Optional resource discovery and side-effect-free readiness plans.

A registry is not a connection. Runtime inventories and user approvals must be
supplied from actual host evidence. This module never installs, sends, renders,
opens a page or changes a provider account.
"""
from __future__ import annotations
import re
from datetime import date
from .common import ACOError, ROOT, read_json


def load_registry():
    full=ROOT/'skills/aco-office-concierge/references/resources/REGISTRY.json'
    path=full if full.exists() else ROOT/'config/resources.json'
    obj=read_json(path)
    if obj.get('schema_version')!=1:raise ACOError('Unsupported resource registry')
    return obj


def search_resources(query='',role=None,limit=3,include_unresolved=False):
    if not isinstance(limit,int) or not 1<=limit<=100:raise ACOError('Limit must be 1–100')
    words=set(re.findall(r'[a-z0-9]+',query.lower()));rs=load_registry()['resources'];rank=[]
    if not words and not role:return {'status':'no_selection_needed','resources':[],'reason':'Supply a task or role; the registry is not an install list.'}
    for e in rs:
        if e['review_status']=='identity_unresolved' and not include_unresolved:continue
        text=' '.join([e['id'],e['name'],*e['aliases'],e['category'],e['type'],e['use_when']]).lower()
        tokens=set(re.findall(r'[a-z0-9]+',text))
        score=len(words&tokens)+(4 if role in e['roles'] else 0)
        if score:rank.append((score,e))
    rank.sort(key=lambda x:(-x[0],x[1]['id']))
    return {'status':'candidates_only','resources':[dict(e,match_score=s) for s,e in rank[:limit]],'selected_or_installed':False,'note':'Lexical/role matching is navigation, not a quality or safety ranking. Use no resource when none helps.'}


def resource_plan(request,inventory=None,as_of=None):
    if not isinstance(request,dict):raise ACOError('Request must be an object')
    allowed={'consult','use','install','deploy','identify'}
    rid=request.get('resource_id');action=request.get('action','consult')
    if action not in allowed:raise ACOError('Unsupported action')
    e=next((x for x in load_registry()['resources'] if x['id']==rid),None)
    if not e:raise ACOError('Unknown resource ID')
    out={'resource_id':rid,'action':action,'executed':False,'installed':False,'status':'plan_only','blockers':[],'warnings':[],'source':e['source_url']}
    if request.get('denied') is True:
        out.update(status='denied',blockers=['The action was denied; do not evade through another account, channel or tool.']);return out
    if e['review_status']=='identity_unresolved':
        out.update(status='needs_exact_source',blockers=['Ask for the exact repository/page. Do not guess a package or combine candidates.']);return out
    if e['review_status']=='partial_review':out['warnings'].append('Partial source review: retrieve and validate the original source before use.')
    if not str(request.get('purpose','')).strip():out['blockers'].append('Clarify the specific task benefit; do not select tools by default.')
    if request.get('data_scope') not in {'public','synthetic','private','none'}:out['blockers'].append('Declare data_scope: public, synthetic, private or none.')
    if request.get('data_scope')=='private' and not isinstance(request.get('external_transfer'),bool):
        out['blockers'].append('Explicitly identify whether private data leaves the authorized environment; do not infer a local route.')
    external=request.get('external_transfer') is True
    if request.get('data_scope')=='private' and external and not request.get('data_transfer_approval_ref'):
        out['blockers'].append('Explicit approval of the exact private-data transfer and destination is required.')
    if request.get('contains_secrets') is True:out['blockers'].append('Never send secrets as resource input.')
    if action in {'use','install','deploy'}:
        if e.get('license_gate')=='reference_only':
            out['blockers'].append('This resource is curated for consultation only. Do not execute, embed or adapt its protected contents; choose consult or obtain a separately reviewed permission and integration plan.')
        if e['review_status']=='partial_review' and not request.get('source_review_ref'):
            out['blockers'].append('This entry is only partially reviewed; verify the exact source/asset before execution.')
        if not request.get('approval_ref'):out['blockers'].append('Installation/execution needs an applicable user authorization reference.')
        if not request.get('license_review_ref'):out['blockers'].append('Record current source, asset/model and redistribution license review.')
        if request.get('paid') is True and not request.get('spend_approval_ref'):out['blockers'].append('Approve the specific cost/budget first.')
        inv=inventory if isinstance(inventory,dict) else {}
        try:
            checked=date.fromisoformat(inv.get('checked_on',''));today=as_of or date.today()
            if not 0<=(today-checked).days<=1:raise ValueError('stale')
            if not inv.get('evidence_ref'):raise ValueError('no evidence')
        except (ValueError,TypeError):out['blockers'].append('Inspect current host capabilities; registry presence or old inventory is not access.')
        caps=inv.get('capabilities',[])
        if not isinstance(caps,list):raise ACOError('Inventory capabilities must be a list')
        missing=[x for x in e['requirements'] if x not in caps]
        if missing:out['blockers'].append('Missing capabilities: '+', '.join(missing))
        if 'voice_consent' in e['requirements'] and not request.get('voice_consent_ref'):out['blockers'].append('Confirm the voice/likeness rights and consent for this use.')
    if action in {'install','deploy'}:out['warnings'].append('Review exact repository/ref, scripts, dependency/network effects, rollback and secrets handling. No blanket installs.')
    out['status']='blocked' if out['blockers'] else 'ready_for_host_review'
    out['fallback']='Work with existing tools or provide a copy-ready plan; do not pretend an external action happened.'
    out['note']='Caller-provided evidence references are not authentication or a sandbox. The host enforces real permissions and confirms actual results.'
    return out
