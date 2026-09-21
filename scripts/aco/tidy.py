"""Read-only inventory and explicit, reversible consolidation of local knowledge.

No cloud deletion API and no automatic semantic compression. Content and scope
are reviewed by the user/agent before a plan is approved. A backup and receipt
are kept OUTSIDE the knowledge tree. Moving old files is an explicit option.
"""
from __future__ import annotations
import json
import os
import re
import shutil
import uuid
import zipfile
from pathlib import Path
from .common import ACOError, Conflict, ROOT, atomic_write, digest, json_bytes, lock, no_symlinks, read_json, safe_path, under_git, write_json

TEXT_EXT={'.md','.txt','.json'}
PROTECTED={'contract','invoice','receipt','certificate','release','license','legal','payroll','tax','master','deliverable','submission','application','proposal'}
GENERATED={'work-log.md','decisions.md','open-loops.md','context-changelog.md','handoff.md','current-handoff.md','current-brief.md','relevant-context.md','changes.md','context.md'}


def _root(root):
    root=Path(root).expanduser().absolute();no_symlinks(root)
    if not root.is_dir() or root==ROOT or root.is_relative_to(ROOT) or ROOT.is_relative_to(root) or under_git(root):raise ACOError('Select an existing authorized private knowledge root outside Git, not the ACO library.')
    return root


def inventory(root,limit=10000):
    root=_root(root);files=[];empty=[];duplicates={}
    for p in sorted(root.rglob('*')):
        no_symlinks(p)
        if len(files)>=limit:raise ACOError('Inventory limit reached; narrow the authorized scope instead of truncating silently.')
        rel=p.relative_to(root).as_posix()
        if p.is_dir():
            if not any(p.iterdir()):empty.append(rel)
            continue
        if not p.is_file():raise ACOError('Unsupported special file: '+rel)
        tokens=set(re.findall('[a-z]+',rel.lower()))
        generated=p.name.lower() in GENERATED or ('history' in tokens and p.suffix.lower() in TEXT_EXT)
        protected=bool(tokens&PROTECTED) or p.suffix.lower() not in TEXT_EXT
        # Primary media/records are metadata-only; do not read gigabytes just to
        # inventory generated notes. Large text needs a narrower manual review.
        h=digest(p.read_bytes()) if not protected and p.stat().st_size<=16*1024*1024 else None
        files.append({'path':rel,'bytes':p.stat().st_size,'sha256':h,'classification':'preserve_deliverable_or_restricted' if protected else 'review_aco_notes' if generated else 'unclassified_preserve'})
        if h is not None:duplicates.setdefault(h,[]).append(rel)
    return {'status':'inventory_only','root':str(root),'files':files,'byte_duplicate_groups':[v for v in duplicates.values() if len(v)>1],'empty_folders':empty,'modified':False,'rule':'Duplicate bytes and rejected status are NOT deletion approval. Preserve source documents and access boundaries.'}


def _check_empty_folders(root,folders,sources,quarantine,target):
    if not isinstance(folders,list) or len(set(folders))!=len(folders):raise ACOError('Empty-folder list must be unique')
    permitted=set(sources) if quarantine else set()
    approved=set(folders)
    for rel in folders:
        d=safe_path(root,rel)
        if d==root or not d.is_dir() or target.is_relative_to(d):raise Conflict('Invalid canonical/empty-folder target: '+str(rel))
        for child in d.rglob('*'):
            no_symlinks(child);c=child.relative_to(root).as_posix()
            if child.is_file() and c not in permitted:raise Conflict('Folder contains unapproved files: '+str(rel))
            if child.is_dir() and c not in approved:raise Conflict('Nested folder must be explicitly included or retained: '+str(c))
            if not child.is_dir() and not child.is_file():raise Conflict('Special file in folder: '+str(c))


def consolidation_plan(root,spec):
    root=_root(root)
    if not isinstance(spec,dict):raise ACOError('Consolidation spec must be an object')
    sources=spec.get('sources',[]);scope=spec.get('scope_id');target=spec.get('target');text=spec.get('merged_text')
    if not isinstance(scope,str) or not scope.strip() or not isinstance(sources,list) or not sources:raise ACOError('One explicit access/owner scope and at least one reviewed source are required')
    if not isinstance(target,str) or not isinstance(text,str) or not text.strip():raise ACOError('Provide a canonical target path and the reviewed merged text')
    if Path(target).name not in {'ACO.md','ACO-INDEX.md'}:raise ACOError('Canonical target must be ACO.md or ACO-INDEX.md')
    dest=safe_path(root,target);no_symlinks(dest)
    if dest.exists() and not dest.is_file():raise Conflict('Target is not a regular file')
    observed=digest(dest.read_bytes()) if dest.exists() else None
    if observed!=spec.get('target_sha256'):raise Conflict('Target revision is stale or missing from the spec')
    seen=set();checked=[]
    for s in sources:
        if not isinstance(s,dict) or s.get('scope_id')!=scope:raise Conflict('Cross-scope consolidation is forbidden; use separate documents for separately shared/restricted data')
        rel=s.get('path')
        if not isinstance(rel,str):raise ACOError('Source path must be relative text')
        if set(Path(rel).parts)&{'.git','.env','credentials.json','token.json'}:raise Conflict('Protected source path')
        p=safe_path(root,rel)
        if rel in seen:raise ACOError('Duplicate source path')
        seen.add(rel)
        if not p.is_file() or p.suffix.lower() not in TEXT_EXT:raise ACOError('Only explicitly reviewed text notes can be consolidated')
        if not s.get('reviewed_as_aco_note'):raise Conflict('Each source needs explicit classification as an ACO note, not an original deliverable')
        if s.get('protected') is True:raise Conflict('Protected records must be referenced, not consolidated/moved')
        if digest(p.read_bytes())!=s.get('sha256'):raise Conflict('Source changed: '+str(rel))
        try:p.read_text(encoding='utf-8')
        except UnicodeError as e:raise ACOError('Not valid UTF-8 text') from e
        checked.append({'path':rel,'sha256':s['sha256'],'scope_id':scope})
    empty=spec.get('remove_empty_folders',[])
    _check_empty_folders(root,empty,seen,spec.get('quarantine_sources') is True,dest)
    plan={'schema_version':1,'root':str(root),'scope_id':scope,'sources':checked,'target':target,'target_sha256':observed,'merged_text':text,'new_sha256':digest(text.encode()),'quarantine_sources':spec.get('quarantine_sources') is True,'remove_empty_folders':empty,'review_note':str(spec.get('review_note',''))}
    plan['plan_id']=digest(json_bytes(plan))
    return {'status':'preview','plan':plan,'modified':False,'notes':'Merge content must be reviewed for lost decisions, obligations, attribution, references and access boundaries. No semantic equivalence is certified.'}


def _verify_plan(root,p):
    if p.get('root')!=str(root):raise Conflict('Plan root mismatch')
    check=dict(p);pid=check.pop('plan_id',None)
    if digest(json_bytes(check))!=pid:raise Conflict('Plan was changed after review')
    for s in p['sources']:
        f=safe_path(root,s['path'])
        if not f.is_file() or digest(f.read_bytes())!=s['sha256']:raise Conflict('Source revision changed: '+s['path'])
    t=safe_path(root,p['target']);actual=digest(t.read_bytes()) if t.is_file() else None
    if actual!=p['target_sha256']:raise Conflict('Canonical target revision changed; replan')
    _check_empty_folders(root,p['remove_empty_folders'],[x['path'] for x in p['sources']],p['quarantine_sources'],t)


def apply_plan(root,plan,recovery_root,approval_ref,approved_plan_id):
    root=_root(root);recovery_root=Path(recovery_root).expanduser().absolute();no_symlinks(recovery_root)
    if recovery_root==root or recovery_root.is_relative_to(root) or root.is_relative_to(recovery_root) or recovery_root.is_relative_to(ROOT) or under_git(recovery_root):raise ACOError('Choose a distinct private recovery directory outside the knowledge root and Git')
    if not approval_ref.strip() or approved_plan_id!=plan.get('plan_id'):raise Conflict('Explicit approval of this exact plan ID is required')
    dest=recovery_root/approved_plan_id
    with lock(recovery_root/'lock'):
        if dest.exists():
            receipt=read_json(dest/'receipt.json')
            if receipt.get('status')=='applied':
                return {'status':'already_applied','receipt':str(dest/'receipt.json'),'drive_modified':False}
            raise Conflict('Interrupted operation has a backup/receipt; review or restore it before retrying, do not overwrite recovery data')
        _verify_plan(root,plan)
        dest.mkdir(parents=True,mode=0o700);paths={s['path'] for s in plan['sources']}
        if plan['target_sha256'] is not None:paths.add(plan['target'])
        backup=dest/'before.zip'
        with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for rel in sorted(paths):z.writestr(rel,safe_path(root,rel).read_bytes())
        os.chmod(backup,0o600)
        with zipfile.ZipFile(backup) as z:
            for rel in paths:
                if z.read(rel)!=safe_path(root,rel).read_bytes():raise Conflict('Backup verification failed')
        receipt={'status':'prepared','plan':plan,'approval_ref':approval_ref,'backup_sha256':digest(backup.read_bytes()),'moved':[],'removed_empty':[]}
        write_json(dest/'receipt.json',receipt)
        # Recheck after backup: fail closed if concurrent edits appeared.
        _verify_plan(root,plan)
        atomic_write(safe_path(root,plan['target']),plan['merged_text'].encode())
        receipt['status']='target_written';write_json(dest/'receipt.json',receipt)
        if plan['quarantine_sources']:
            for s in plan['sources']:
                if s['path']==plan['target']:continue
                src=safe_path(root,s['path'])
                if digest(src.read_bytes())!=s['sha256']:raise Conflict('A source changed during cleanup; it was preserved. Review receipt.')
                q=safe_path(dest/'files',s['path']);q.parent.mkdir(parents=True,exist_ok=True)
                shutil.move(str(src),str(q))
                if digest(q.read_bytes())!=s['sha256']:raise Conflict('Quarantine copy failed integrity verification')
                receipt['moved'].append(s['path']);write_json(dest/'receipt.json',receipt)
        for rel in sorted(plan['remove_empty_folders'],key=lambda x:len(Path(x).parts),reverse=True):
            p=safe_path(root,rel)
            if any(p.iterdir()):raise Conflict('Folder changed during cleanup; it was preserved')
            p.rmdir();receipt['removed_empty'].append(rel);write_json(dest/'receipt.json',receipt)
        receipt['status']='applied';write_json(dest/'receipt.json',receipt)
        return {'status':'applied_locally','canonical':plan['target'],'quarantined':len(receipt['moved']),'empty_folders_removed':len(receipt['removed_empty']),'backup':str(backup),'receipt':str(dest/'receipt.json'),'drive_modified':False,'permanently_deleted_files':0}


def restore(receipt_path,approval_ref,rollback_target=False):
    if not approval_ref.strip():raise Conflict('Explicit restoration approval required')
    receipt_path=Path(receipt_path).absolute();no_symlinks(receipt_path)
    rec=read_json(receipt_path);p=rec['plan'];root=_root(p['root']);backup=receipt_path.parent/'before.zip';no_symlinks(backup)
    if digest(backup.read_bytes())!=rec['backup_sha256']:raise Conflict('Backup changed')
    with lock(receipt_path.parent.parent/'lock'), zipfile.ZipFile(backup) as z:
        # Restore from verified before.zip even if interruption prevented recording a move.
        candidates=[s for s in p['sources'] if s['path']!=p['target']]
        for s in candidates:
            f=safe_path(root,s['path'])
            if f.exists() and (not f.is_file() or digest(f.read_bytes())!=s['sha256']):raise Conflict('Newer source would be overwritten; preserve it')
            if digest(z.read(s['path']))!=s['sha256']:raise Conflict('Backup source digest mismatch')
        t=safe_path(root,p['target'])
        if rollback_target:
            actual=digest(t.read_bytes()) if t.is_file() else None
            if actual not in {p['new_sha256'],p['target_sha256']}:raise Conflict('Newer canonical edit would be overwritten; preserve it')
        for s in candidates:
            f=safe_path(root,s['path'])
            if not f.exists():atomic_write(f,z.read(s['path']))
        if rollback_target:
            if p['target_sha256'] is not None:atomic_write(t,z.read(p['target']))
            # Leave a newly created canonical file in place rather than deleting it automatically.
        for rel in rec.get('removed_empty',[]):safe_path(root,rel).mkdir(parents=True,exist_ok=True)
        rec['restore_approval_ref']=approval_ref;rec['restored']=True;write_json(receipt_path,rec)
        return {'status':'restored_locally','drive_modified':False,'new_canonical_preserved':p['target_sha256'] is None,'recovery_kept':True}
