"""Pure intake and external-action planning. No network, sending or auth granting.

Input assertions must be verified by the host against real tools and user consent.
A 'ready' result is NOT authorization and is NOT an execution receipt.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, read_json

WORKFLOW_PATH = ROOT / 'skills/aco-office-concierge/references/WORKFLOWS.json'

def workflows() -> dict:
    p = WORKFLOW_PATH if WORKFLOW_PATH.is_file() else ROOT / 'config/workflows.json'
    return read_json(p)['workflows']

def present(value: Any) -> bool:
    if value is None or value == '' or value == [] or value == {}:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().lower() not in {'unknown', 'tbd', 'unsure', '?'}
    return True

def intake(workflow: str, facts: dict, *, mode: str = 'ACTION') -> dict:
    if mode not in {'ACTION', 'DECISION', 'EXPLAIN'}:
        raise ACOError('Mode must be ACTION, DECISION or EXPLAIN.')
    if not isinstance(facts, dict):
        raise ACOError('Facts must be an object with known brief fields.')
    table = workflows()
    if workflow not in table:
        raise ACOError('Unknown workflow; choose: ' + ', '.join(sorted(table)))
    spec = table[workflow]
    missing = [f for f in spec['intake'] if f.get('essential') and not present(facts.get(f['key']))]
    return {'status': 'needs_clarification' if missing else 'brief_ready',
            'workflow': workflow, 'mode': mode, 'office': spec['office'], 'lead': spec['lead'],
            'questions': [{'key': f['key'], 'question': f['question']} for f in missing[:3]],
            'remaining_blockers': max(0, len(missing)-3),
            'potential_helpers': spec['team'], 'outputs': spec['outputs'], 'gates': spec['gates'],
            'executed': False,
            'note': 'Read supplied facts first. Use only needed helpers. This is intake validation, not task execution.'}

OPERATIONS = {'email': 'send_email', 'whatsapp': 'send_message', 'sms': 'send_message',
              'phone': 'place_call', 'calendar': 'create_event', 'publication': 'publish'}
FINGERPRINT_FIELDS = ('scope_id','channel','operation','account_id','target_id','body','subject',
                      'cc','bcc','attachments','scheduled_at','limits','ai_disclosure','language')

def action_fingerprint(request: dict) -> str:
    payload={k:request.get(k) for k in FINGERPRINT_FIELDS}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def plan_action(request: dict, capability: dict | None = None,
                authorization: dict | None = None, previous: dict | None = None) -> dict:
    for obj in (request, capability, authorization, previous):
        if obj is not None and not isinstance(obj, dict):
            raise ACOError('Request, capability, authorization and previous outcome must be objects.')
    if not isinstance(request,dict):raise ACOError('Request is required.')
    channel=request.get('channel')
    if channel not in OPERATIONS:raise ACOError('Unsupported channel: '+str(channel))
    for field in ('scope_id','account_id','target_id','body','subject','action_id'):
        if field in request and request[field] is not None and not isinstance(request[field],str):
            raise ACOError(field+': expected text')
    for field in ('cc','bcc','attachments'):
        if field in request and not isinstance(request[field],list):
            raise ACOError(field+': expected a list')
    operation=request.get('operation',OPERATIONS[channel])
    if operation!=OPERATIONS[channel]:
        raise ACOError('Channel/operation mismatch; text, voice, calendar and publication are distinct.')
    req=dict(request,operation=operation)
    fp=action_fingerprint(req)
    result={'status':'draft_only','channel':channel,'operation':operation,
            'action_id':req.get('action_id'),'content_sha256':fp,'executed':False,'host_action_eligible':False,
            'draft':{'target_id':req.get('target_id'),'subject':req.get('subject'),
                     'body':req.get('body',''),'attachments':req.get('attachments',[])},
            'note':'Planning only. Host must verify actual tools, scope and consent. This command never sends, calls, books or publishes.'}
    if request.get('intent','draft') not in {'draft','execute'}:
        raise ACOError('intent must be draft or execute.')
    if request.get('intent','draft')=='draft':return result
    if previous and previous.get('status') in {'accepted','queued','sent','delivered','read','connected','published','booked','unknown','timeout','attempted'}:
        result.update(status='reconcile_before_retry',reason='Previous attempt may already have taken effect. Check provider status; do not repeat blindly.')
        return result
    cap=capability or {}
    if 'operations' in cap and (not isinstance(cap['operations'],list) or any(not isinstance(x,str) for x in cap['operations'])):
        raise ACOError('capability.operations must be a list of semantic action names')
    if cap.get('denied') is True:
        result.update(status='blocked',reason='Provider/host denied this action. Do not bypass through another endpoint or account.')
        return result
    if not (cap.get('available') is True and cap.get('connected') is True and
            cap.get('schema_verified') is True and operation in cap.get('operations',[])):
        result.update(status='copy_ready_not_executed',reason='Exact action capability not verified. Return draft/script, not an execution claim.')
        return result
    missing=[k for k in ('action_id','scope_id','account_id','target_id','body') if not present(req.get(k))]
    if request.get('recipient_verified') is not True:missing.append('verified_recipient')
    if cap.get('account_id')!=req.get('account_id'):missing.append('matching_sending_account')
    if channel=='phone':
        missing.extend(k for k in ('ai_disclosure','language','limits') if not present(req.get(k)))
    if missing:
        result.update(status='needs_clarification',missing=missing,
                      reason='Resolve recipient, sending identity, scope/content or call limits before action.')
        return result
    auth=authorization or {}
    bound={'action_id':req['action_id'],'scope_id':req['scope_id'],'channel':channel,'operation':operation,
           'account_id':req['account_id'],'target_id':req['target_id'],'content_sha256':fp}
    if not present(auth.get('reference')) or any(auth.get(k)!=v for k,v in bound.items()):
        result.update(status='awaiting_authorization',reason='Explicit authorization must cover this exact action, identity, destination and payload.')
        return result
    result.update(status='ready_for_host_action',host_action_eligible=True,
                  authorization_ref=auth['reference'],reason='Packet checks passed. Host still verifies real permission and invokes the actual connector.')
    return result
