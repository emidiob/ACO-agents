"""Revision-guarded canonical-document update contract.

No Google credentials, service client, or background process is bundled. The
host must supply an authorized provider implementing atomic revision control.
Mock-provider tests do not prove a particular connector supports that control.
"""
from __future__ import annotations
from .common import ACOError, Conflict, digest, json_bytes


def plan_update(snapshot:dict,new_text:str,scope_id:str,approval_ref:str):
    if not isinstance(snapshot,dict) or not isinstance(new_text,str):raise ACOError('Snapshot object and UTF-8 text required')
    if not all(isinstance(snapshot.get(x),str) and snapshot[x] for x in ('document_id','revision','scope_id')):raise ACOError('Read an exact document ID, revision and access/owner scope first')
    if snapshot['scope_id']!=scope_id:raise Conflict('Canonical update crosses the authorized scope')
    if not isinstance(snapshot.get('text'),str) or not approval_ref.strip():raise Conflict('Current text and applicable update approval required')
    if not new_text.strip():raise Conflict('Empty replacement is not a compact-memory update')
    p={'schema_version':1,'document_id':snapshot['document_id'],'scope_id':scope_id,'expected_revision':snapshot['revision'],'before_sha256':digest(snapshot['text'].encode()),'after_sha256':digest(new_text.encode()),'new_text':new_text,'approval_ref':approval_ref}
    p['id']=digest(json_bytes(p))
    return p


def apply_update(plan:dict,provider):
    p=dict(plan);pid=p.pop('id',None)
    if digest(json_bytes(p))!=pid:raise Conflict('Update plan changed after review')
    if getattr(provider,'supports_revision_guard',False) is not True:raise Conflict('Provider cannot guard concurrent revisions. Return an in-chat patch and pending status; do not overwrite blindly.')
    current=provider.read_document(p['document_id'])
    if current.get('scope_id')!=p['scope_id'] or current.get('document_id')!=p['document_id']:raise Conflict('Provider returned another scope or document')
    actual=digest(current['text'].encode())
    if actual==p['after_sha256']:return {'status':'already_verified_remote','document_id':p['document_id'],'new_files':0}
    if current.get('revision')!=p['expected_revision'] or actual!=p['before_sha256']:raise Conflict('Remote document changed; reread and rebase')
    # Provider must enforce expected_revision atomically. It must never create a new doc on failure.
    provider.replace_document(p['document_id'],p['new_text'],expected_revision=p['expected_revision'])
    observed=provider.read_document(p['document_id'])
    if observed.get('document_id')!=p['document_id'] or observed.get('scope_id')!=p['scope_id'] or digest(observed['text'].encode())!=p['after_sha256']:raise Conflict('Write not verified; inspect the same document before retrying. Do not create a duplicate.')
    return {'status':'verified_remote','document_id':p['document_id'],'revision':observed['revision'],'sha256':p['after_sha256'],'new_files':0}
