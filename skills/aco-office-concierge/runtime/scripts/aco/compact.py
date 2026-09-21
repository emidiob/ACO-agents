"""Compact knowledge: canonical Markdown, lazy entities, pipeline rows, no per-event files.

State/locks/recovery journal are local and OUTSIDE the knowledge tree. This is
not a Drive mount/sync daemon. The connected-tool protocol updates the same
canonical documents by ID; the old immutable-event bridge is opt-in legacy.
"""
from __future__ import annotations
import copy
import json
import re
import subprocess
import uuid
from pathlib import Path
from .common import (ACOError, Conflict, ROOT, VERSION, atomic_write, digest, json_bytes,
                     key_ok, lock, no_symlinks, now, private_root, read_json, safe_path, under_git, write_json)
from .memory import KINDS, OWNER_KINDS, ALLOWED_PARENTS, MODES, EVENT_KINDS, STATES

PIPE_KINDS = {'idea','opportunity','application','lead','prospect','proposal','experiment','collaboration','activity','product','project','client','brand'}
PIPE_STATES = {'exploring','considering','draft','proposed','submitted','waiting','parked','rejected','lost','abandoned','active','completed'}
COMMITMENTS = {'explicit_user','external_confirmed','existing_entity'}
INDEX_START = '<!-- ACO compact index start -->'
INDEX_END = '<!-- ACO compact index end -->'
MAX_WORK = 20

def _one_line(s: str) -> str:
    return str(s).replace('\r',' ').replace('\n',' ').replace('|','&#124;').replace('<','&lt;').replace('>','&gt;')

def _section(name: str, body: str) -> str:
    return f'<!-- ACO {name} start -->\n{body.rstrip()}\n<!-- ACO {name} end -->'

def _part(text: str, name: str) -> str:
    pat = re.compile(r'<!-- ACO '+re.escape(name)+r' start -->\n(.*?)\n<!-- ACO '+re.escape(name)+r' end -->', re.S)
    matches = list(pat.finditer(text))
    if len(matches)!=1:
        raise Conflict(f'Canonical document needs exactly one managed {name} section; preserve and reconcile manual edits.')
    return matches[0].group(1)

def _replace(text: str, name: str, body: str) -> str:
    old = _part(text,name)
    return text.replace(_section(name,old), _section(name,body), 1)

def storage_decision(item: dict) -> dict:
    """Planning policy only. Activation permits, but never mandates, a new document."""
    if not isinstance(item,dict): raise ACOError('Storage request must be an object')
    kind=item.get('kind','idea'); status=item.get('status','exploring')
    explicit=item.get('commitment') in COMMITMENTS and bool(str(item.get('approval_ref','')).strip())
    independent=item.get('independent') is True
    requested=item.get('artifact_requested') is True
    if requested and item.get('artifact_type') in {'proposal','application','treatment','contract','budget','deliverable'}:
        return {'action':'deliverable_allowed','create_project':False,'reason':'A requested real deliverable may be saved without creating project scaffolding.'}
    if item.get('restricted') is True:
        return {'action':'restricted_boundary_review','create_project':False,'reason':'Do not consolidate HR, legal, finance or separately shared client material into a broader-access document.'}
    if status in {'rejected','lost','abandoned','parked'}:
        return {'action':'inline_status_update','create_project':False,'reason':'Rejection/abandonment changes a row, not the folder structure.'}
    if kind in PIPE_KINDS and not explicit:
        return {'action':'inline_pipeline' if item.get('remember') else 'chat_only','create_project':False,'reason':'Pipeline is not a project; an agent suggestion is not user commitment.'}
    if explicit and independent:
        return {'action':'eligible_canonical_document','create_project':kind in {'project','product'},'reason':'Evidence of activation plus a genuinely independent body of work; reuse an existing document first.'}
    return {'action':'inline_existing_document','create_project':False,'reason':'Activities, clients, brands and small active items normally remain sections.'}

class CompactMemory:
    def __init__(self, root: Path, state_root: Path | None=None):
        self.root=Path(root).expanduser().absolute(); no_symlinks(self.root)
        if self.root==ROOT or self.root.is_relative_to(ROOT) or ROOT.is_relative_to(self.root): raise ACOError('Knowledge must remain outside the public ACO library.')
        base=(Path(state_root).expanduser().absolute() if state_root else private_root()/'compact-state')
        no_symlinks(base)
        self.system=base/digest(str(self.root).encode())[:24]
        if self.system.is_relative_to(self.root) or self.system==self.root: raise ACOError('Local compact state must not be inside the knowledge/Drive tree.')
        if self.system.is_relative_to(ROOT): raise ACOError('Local state must not be in the public library.')
        self.registry_path=self.system/'state.json'; self.journal=self.system/'pending.json'
        self.index=self.root/'ACO-INDEX.md'

    def _lock(self): return lock(self.system/'lock')

    def _recover(self):
        if not self.journal.exists():return
        j=read_json(self.journal)
        if j.get('root')!=str(self.root):raise Conflict('Recovery journal belongs to a different root')
        # Preflight every write before applying any. Edited files halt recovery.
        for w in j['writes']:
            p=safe_path(self.root,w['path']); actual=digest(p.read_bytes()) if p.is_file() else None
            if actual not in {w['before'],digest(w['text'].encode())}:raise Conflict('Recovery conflicts with a newer edit: '+w['path'])
        for w in j['writes']:
            p=safe_path(self.root,w['path']); data=w['text'].encode()
            if not p.is_file() or p.read_bytes()!=data:atomic_write(p,data)
        write_json(self.registry_path,j['state']); self.journal.unlink()

    def _commit(self,r:dict,writes:dict[str,tuple[str|None,str]]):
        for rel,(base,text) in writes.items():
            p=safe_path(self.root,rel)
            if p.exists() and not p.is_file():raise Conflict('Expected a file: '+rel)
            actual=digest(p.read_bytes()) if p.is_file() else None
            if actual!=base:raise Conflict('Canonical document changed; reread before writing: '+rel)
            if not isinstance(text,str):raise ACOError('Canonical output must be UTF-8 text')
        j={'root':str(self.root),'state':r,'writes':[{'path':k,'before':v[0],'text':v[1]} for k,v in writes.items()]}
        write_json(self.journal,j); self._recover()

    def registry(self):
        r=read_json(self.registry_path)
        if r.get('schema_version')!=2 or r.get('layout')!='compact':raise Conflict('Not a compact registry; no implicit migration.')
        return r

    def _render_index(self,r):
        # Only identity/path information travels in the index. Session payloads stay local.
        public={k:r[k] for k in ('schema_version','layout','namespace','authority','entities')}
        body=['# ACO — compact knowledge index','','Private knowledge. Update existing canonical files; pipeline items do not create folders.','']
        for e in r['entities'].values():
            if e['storage']=='document':body.append(f'- [{_one_line(e["name"])}]({e["document"]}) — `{e["id"]}`')
        body+=['',INDEX_START,'```json',json.dumps(public,indent=2,ensure_ascii=False),'```',INDEX_END,'']
        return '\n'.join(body)

    def init(self,authority='local'):
        if authority not in {'local','drive'}:raise ACOError('Authority must be local or drive')
        if under_git(self.root):raise ACOError('Keep private knowledge outside Git.')
        with self._lock():
            self._recover()
            if self.registry_path.exists():
                r=self.registry()
                if r['authority']!=authority:raise Conflict('Changing authority needs a reviewed migration')
                if not self.index.exists():raise Conflict('Missing canonical index; do not silently recreate it')
            elif self.index.is_file():
                text=self.index.read_text(); match=re.search(re.escape(INDEX_START)+r'\n```json\n(.*?)\n```\n'+re.escape(INDEX_END),text,re.S)
                if not match:raise Conflict('Existing index is not compact; use the reviewed consolidation process')
                try:r=json.loads(match.group(1))
                except ValueError as e:raise Conflict('Invalid compact index') from e
                if r.get('schema_version')!=2 or r.get('layout')!='compact' or not isinstance(r.get('entities'),dict) or r.get('authority')!=authority:raise Conflict('Index schema/authority mismatch')
                r.update(aco_version=VERSION,sessions={},proposals={})
                for e in r['entities'].values():
                    p=safe_path(self.root,e['document'])
                    if not p.is_file():raise Conflict('Index points to a missing canonical document')
                write_json(self.registry_path,r)
            else:
                if self.root.exists() and any(self.root.iterdir()):raise Conflict('Nonempty legacy/unrecognized knowledge. Preview consolidation; do not create a second hierarchy.')
                r={'schema_version':2,'layout':'compact','aco_version':VERSION,'namespace':str(uuid.uuid4()),'authority':authority,'entities':{},'sessions':{},'proposals':{}}
                self._commit(r,{'ACO-INDEX.md':(None,self._render_index(r))})
            return {'status':'ready','layout':'compact','entities':len(r['entities']),'root':str(self.root),'local_state':str(self.system),'persistence':'local_verified','drive_verified':False}

    def adopt(self,relative,kind,key,name,expected_sha256,approval_ref,authority='local'):
        """Explicitly adopt a reviewed existing owner document in place; preserve bytes
        as its context. No move/delete or inferred extraction of decisions occurs.
        """
        if kind not in OWNER_KINDS or not name.strip() or not approval_ref.strip():raise Conflict('Adoption requires a real owner kind/name and explicit approval')
        if authority not in {'local','drive'}:raise ACOError('Invalid authority')
        key_ok(key)
        if under_git(self.root):raise ACOError('Knowledge must remain outside Git')
        path=safe_path(self.root,relative)
        if path==self.index or path.suffix.lower() not in {'.md','.txt'} or not path.is_file():raise Conflict('Select an existing canonical UTF-8 narrative document, not the index')
        original=path.read_text(encoding='utf-8')
        if digest(path.read_bytes())!=expected_sha256:raise Conflict('Adoption source changed since review')
        if '<!-- ACO compact entity:' in original:raise Conflict('Already managed document; recover/use its existing index instead of adopting twice')
        if self.index.exists() and not self.registry_path.exists():self.init(authority)
        with self._lock():
            self._recover()
            if self.registry_path.exists():
                r=self.registry()
                if r['authority']!=authority:raise Conflict('Authority mismatch')
                if any(e['document']==relative for e in r['entities'].values()):raise Conflict('Document already registered')
            else:
                if self.index.exists():raise Conflict('Unrecognized index must be reconciled before adoption')
                r={'schema_version':2,'layout':'compact','aco_version':VERSION,'namespace':str(uuid.uuid4()),'authority':authority,'entities':{},'sessions':{},'proposals':{}}
            eid=kind+'-'+uuid.uuid5(uuid.UUID(r['namespace']),f'{kind}/root/{key}').hex
            if eid in r['entities']:raise Conflict('Owner key already registered; reuse its document')
            e={'id':eid,'kind':kind,'key':key,'name':name.strip(),'parent_id':None,'owner_id':eid,'document':relative,'storage':'document','links':{},'activation':{'kind':'existing_entity','reference':approval_ref},'reason':'Reviewed in-place canonical adoption'}
            new=self._new_doc(e)
            # Preserve original narrative literally inside context; do not infer approvals.
            if '<!-- ACO ' in original:raise Conflict('Existing managed markers need explicit reconciliation before adoption')
            new=_replace(new,'context',original)
            if digest(path.read_bytes())!=expected_sha256:raise Conflict('Adoption source changed during review')
            atomic_write(self.system/'previous-canonical.md',original.encode())
            r['entities'][eid]=e
            base=digest(self.index.read_bytes()) if self.index.exists() else None
            self._commit(r,{relative:(expected_sha256,new),'ACO-INDEX.md':(base,self._render_index(r))})
            return {'status':'adopted_in_place','entity':e,'new_knowledge_files':1 if base is None else 0,'other_files_preserved':True,'persistence':'local_verified','drive_verified':False,'note':'Original narrative retained in Context. No decisions or projects inferred. Reconcile/archive old index aliases only through a separate reviewed plan.'}

    def entity(self,eid,r=None):
        r=r or self.registry()
        if eid not in r['entities']:raise ACOError('Unknown entity ID; choose an existing owner before remembering a pipeline item')
        return r['entities'][eid]

    def _document(self,e):
        p=safe_path(self.root,e['document']); no_symlinks(p)
        if not p.is_file():raise Conflict('Canonical document missing: '+e['document'])
        return p.read_text(encoding='utf-8')

    def _new_doc(self,e):
        sections=[('context','Context'),('brief','Current brief'),('pipeline','Development / commercial pipeline'),('decisions','Decisions'),('open','Open loops'),('recent','Recent work'),('next','Next actions'),('references','Important references')]
        parts=[f'# {_one_line(e["name"])}',f'<!-- ACO compact entity: {e["id"]} -->','',f'Kind: {e["kind"]}. No facts inferred beyond the approved identity.','']
        for s,title in sections:
            contents='| ID | Kind | State | Title | Summary | Next | Source |\n|---|---|---|---|---|---|---|' if s=='pipeline' else ''
            parts.extend(['## '+title,'',_section(s,contents),''])
        return '\n'.join(parts)

    def add_entity(self,kind,key,name,parent_id=None,links=None,*,commitment=None,approval_ref='',separate=False,reason=''):
        if kind not in KINDS or not isinstance(name,str) or not name.strip():raise ACOError('Supported kind and name required')
        key_ok(key); links=links or {}
        if commitment not in COMMITMENTS or not approval_ref.strip():raise Conflict('Entity activation needs explicit_user, external_confirmed or existing_entity plus an approval/source reference. Otherwise use pipeline-upsert.')
        if set(links)-{'activity_ids','client_id','brand_id'}:raise ACOError('Unknown relationship')
        if links and kind!='project':raise ACOError('Only projects accept client/activity/brand links')
        if separate and kind not in OWNER_KINDS and not reason.strip():raise Conflict('Separate child documents need an independence or access-boundary reason')
        with self._lock():
            self._recover();r=self.registry();parent=self.entity(parent_id,r) if parent_id else None
            if (parent['kind'] if parent else None) not in ALLOWED_PARENTS[kind]:raise Conflict('Invalid parent kind')
            eid=kind+'-'+uuid.uuid5(uuid.UUID(r['namespace']),f'{kind}/{parent_id or "root"}/{key}').hex
            if eid in r['entities']:
                old=r['entities'][eid]
                if old['name']!=name.strip() or old['links']!=links:raise Conflict('Stable key already has different metadata')
                return {'status':'existing','entity':old,'persistence':'local_verified'}
            owner=eid if kind in OWNER_KINDS else parent['owner_id']
            is_doc=kind in OWNER_KINDS or separate
            group='Organizations' if kind=='organization' else 'Personal/Artist' if kind=='artist' else 'Personal/Career' if kind=='career' else 'Projects' if kind=='project' else 'Entities'
            rel=f'{group}/{key}--{eid[-8:]}/ACO.md' if is_doc else parent['document']
            e={'id':eid,'kind':kind,'key':key,'name':name.strip(),'parent_id':parent_id,'owner_id':owner,'document':rel,'storage':'document' if is_doc else 'section','links':links,'activation':{'kind':commitment,'reference':approval_ref},'reason':reason}
            rr=copy.deepcopy(r);rr['entities'][eid]=e; self.validate_scope({'entity_id':eid,**links},rr)
            if is_doc:doc=self._new_doc(e);base=None
            else:
                doc=self._document(parent);base=digest(doc.encode());doc+='\n## '+_one_line(name.strip())+'\n\n'+_section('entity-'+eid,'Active '+kind+'. Source: '+_one_line(approval_ref))+'\n'
            index_base=digest(self.index.read_bytes());self._commit(rr,{rel:(base,doc),'ACO-INDEX.md':(index_base,self._render_index(rr))})
            return {'status':'created','entity':e,'persistence':'local_verified','files_created':1 if is_doc else 0,'drive_verified':False}

    def validate_scope(self,scope,r=None):
        r=r or self.registry()
        if set(scope)-{'entity_id','activity_ids','client_id','brand_id'}:raise ACOError('Unsupported scope fields')
        e=self.entity(scope.get('entity_id'),r);s=copy.deepcopy(scope)
        for k,v in e.get('links',{}).items():
            if k in s and s[k]!=v:raise Conflict('Session cannot change project relationships')
            s[k]=v
        act=s.get('activity_ids',[])
        if not isinstance(act,list) or len(set(act))!=len(act):raise Conflict('Activity IDs must be unique')
        for k,ids,kind in [('activities',act,'activity'),('client',[s['client_id']] if s.get('client_id') else [],'client'),('brand',[s['brand_id']] if s.get('brand_id') else [],'brand')]:
            for eid in ids:
                linked=self.entity(eid,r)
                if linked['owner_id']!=e['owner_id'] or linked['kind']!=kind:raise Conflict('Cross-organization or wrong-kind relationship')
        if s.get('brand_id'):
            brand=self.entity(s['brand_id'],r)
            if brand.get('parent_id') and self.entity(brand['parent_id'],r)['kind']=='client' and brand['parent_id']!=s.get('client_id'):raise Conflict('Brand does not belong to the selected client')
        return {**s,'owner_id':e['owner_id']}

    def pipeline_upsert(self,eid,key,kind,title,status='exploring',summary='',next_action='',source='',expected_sha256=None):
        key_ok(key)
        if kind not in PIPE_KINDS or status not in PIPE_STATES:raise ACOError('Unknown pipeline kind/state')
        if status=='active':raise Conflict('Use pipeline-promote with actual commitment; do not infer activation')
        if not title.strip():raise ACOError('A title is required')
        with self._lock():
            self._recover();r=self.registry();e=self.entity(eid,r)
            if e['storage']!='document':raise Conflict('Use the parent canonical document for its inline pipeline')
            doc=self._document(e);base=digest(doc.encode())
            if expected_sha256 and expected_sha256!=base:raise Conflict('Stale canonical document')
            pid='pipe-'+uuid.uuid5(uuid.UUID(r['namespace']),eid+'/'+key).hex
            body=_part(doc,'pipeline');lines=body.splitlines()
            hits=[i for i,line in enumerate(lines) if line.startswith('| '+pid+' |')]
            if len(hits)>1:raise Conflict('Duplicate pipeline ID; reconcile first')
            row='| '+' | '.join(_one_line(x) for x in [pid,kind,status,title,summary,next_action,source])+' |'
            if hits:lines[hits[0]]=row
            else:lines.append(row)
            new=_replace(doc,'pipeline','\n'.join(lines))
            if new==doc:return {'status':'unchanged','pipeline_id':pid,'files_created':0}
            self._commit(r,{e['document']:(base,new)})
            return {'status':'updated','pipeline_id':pid,'entity_count':len(r['entities']),'files_created':0,'persistence':'local_verified','drive_verified':False}

    def promote(self,eid,pid,commitment,approval_ref,*,materialize=False,key=None,name=None,kind='project',reason=''):
        if commitment not in COMMITMENTS or not approval_ref.strip():raise Conflict('Promotion needs actual commitment and a reference')
        # Precheck materialization before altering the active row. Both writes remain
        # resumable/idempotent; no folder is created merely for activation.
        if materialize:
            if kind not in KINDS or kind in OWNER_KINDS or not key or not name or not reason.strip():raise ACOError('Materialization needs supported child kind, key, name and reason')
            key_ok(key)
            parent=self.entity(eid)
            if parent['kind'] not in ALLOWED_PARENTS[kind]:raise Conflict('Materialization parent is invalid')
        with self._lock():
            self._recover();r=self.registry();e=self.entity(eid,r);doc=self._document(e);base=digest(doc.encode())
            lines=_part(doc,'pipeline').splitlines();hits=[i for i,line in enumerate(lines) if line.startswith('| '+pid+' |')]
            if len(hits)!=1:raise Conflict('Unknown or duplicate pipeline item')
            cells=[x.strip() for x in lines[hits[0]].strip('|').split('|')]
            if len(cells)!=7:raise Conflict('Pipeline row has been manually changed; reconcile')
            if cells[2] in {'rejected','lost','abandoned'}:raise Conflict('Reopen the pipeline item explicitly before activating it')
            if materialize and (not key or not name or not reason.strip()):raise ACOError('Materialization needs key, name and independent-work/access reason')
            cells[2]='active';cells[6]=_one_line(approval_ref)
            lines[hits[0]]='| '+' | '.join(cells)+' |'
            self._commit(r,{e['document']:(base,_replace(doc,'pipeline','\n'.join(lines)))})
        if materialize:
            result=self.add_entity(kind,key,name,eid,commitment=commitment,approval_ref=approval_ref,separate=True,reason=reason)
            return {'status':'promoted','pipeline_id':pid,**result}
        return {'status':'activated_inline','pipeline_id':pid,'files_created':0,'persistence':'local_verified','drive_verified':False}

    def _session(self,sid,r):
        if sid not in r['sessions']:raise ACOError('Unknown local session. Continue from the canonical ACO.md in a new session.')
        return r['sessions'][sid]

    def _write_handoff(self,s):
        p=Path(s['handoff_path']);no_symlinks(p)
        if p.exists() and f'<!-- ACO handoff: {s["id"]} -->' not in p.read_text():raise Conflict('A different handoff occupies this workspace; use a separate worktree')
        text=f'# ACO handoff\n<!-- ACO handoff: {s["id"]} -->\n\nScope: {s["scope"]["entity_id"]}\nMode: {s["context_mode"]}\nStatus: {s["status"]}\n\n## Brief\n{s["brief"]}\n\n## Relevant context\n{s.get("context","Not exported.")}\n\n## Recent checkpoint\n{s.get("latest_summary", "None.")}\n\nPersistence: local only; never a Drive receipt.\n'
        atomic_write(p,text.encode())

    def start(self,eid,brief,workspace,mode='LIGHT',relationships=None):
        workspace=Path(workspace).expanduser().absolute();no_symlinks(workspace)
        if mode not in MODES or not brief.strip():raise ACOError('Valid mode and nonempty brief required')
        if not workspace.is_dir() or workspace==ROOT or workspace.is_relative_to(ROOT) or workspace==self.root or workspace.is_relative_to(self.root):raise ACOError('Use an existing separate work-project directory, not the library or knowledge tree')
        with self._lock():
            self._recover();r=self.registry();scope=self.validate_scope({'entity_id':eid,**(relationships or {})},r)
            if any(s['workspace']==str(workspace) and s['status']=='open' for s in r['sessions'].values()):raise Conflict('One active handoff per worktree; close or use another worktree')
            handoff=workspace/'.agent-context/HANDOFF.md';no_symlinks(handoff)
            if handoff.exists():
                txt=handoff.read_text();m=re.search(r'<!-- ACO handoff: ([^ ]+) -->',txt)
                if not m or m[1] not in r['sessions'] or r['sessions'][m[1]]['status']!='closed':raise Conflict('Unrecognized/open handoff; preserve it and choose a different worktree')
            try:
                g=subprocess.run(['git','-C',str(workspace),'rev-parse','--show-toplevel'],capture_output=True,text=True)
            except FileNotFoundError:g=None
            if g and g.returncode==0:
                top=Path(g.stdout.strip());prefix=workspace.relative_to(top).as_posix();prefix='' if prefix=='.' else prefix+'/'
                tracked=subprocess.run(['git','-C',str(top),'ls-files','-z','--',prefix+'.agent-context'],capture_output=True)
                if tracked.returncode or tracked.stdout:raise Conflict('Private handoff is tracked by Git; review/untrack first')
            ignore=workspace/'.gitignore';no_symlinks(ignore);txt=ignore.read_text() if ignore.exists() else ''
            if '.agent-context/' not in txt.splitlines():atomic_write(ignore,(txt.rstrip()+'\n\n# Private ACO handoff\n.agent-context/\n').encode(),0o644)
            sid='session-'+uuid.uuid4().hex
            s={'id':sid,'aco_version':VERSION,'scope':scope,'context_mode':mode,'brief':brief,'workspace':str(workspace),'handoff_path':str(handoff),'status':'open','created_at':now(),'events':{}}
            r['sessions'][sid]=s;write_json(self.registry_path,r)
            # Reuse one handoff file only after known previous session closed.
            if handoff.exists():atomic_write(handoff,f'<!-- ACO handoff: {sid} -->\n'.encode())
            self._write_handoff(s)
            return {'status':'started','session':s,'knowledge_files_created':0,'persistence':'local_verified'}

    def export_context(self,sid,eids):
        with self._lock():
            self._recover();r=self.registry();s=self._session(sid,r)
            if s['status']!='open' or s['context_mode'] in {'NONE','BLIND','BLIND-FIRST'}:raise Conflict('Closed/blind session cannot export context')
            scope=s['scope'];e=self.entity(scope['entity_id'],r)
            allowed={scope['entity_id'],*scope.get('activity_ids',[])}|{scope[k] for k in ('client_id','brand_id') if scope.get(k)}
            # Do not export the whole organization just because it owns the client.
            if set(eids)-allowed:raise Conflict('Context export crosses the explicit session scope')
            chunks=[]
            for x in dict.fromkeys(eids):
                ent=self.entity(x,r);d=self._document(ent)
                chunks.append(d if ent['storage']=='document' else _part(d,'entity-'+x))
            s['context']='\n\n'.join(chunks);write_json(self.registry_path,r);self._write_handoff(s)
            return {'status':'exported','entity_ids':list(dict.fromkeys(eids)),'knowledge_files_created':0,'persistence':'local_verified'}

    def checkpoint(self,sid,entry):
        if not isinstance(entry,dict):raise ACOError('Event must be an object')
        entry=copy.deepcopy(entry);ev_id=entry.get('id')
        if not isinstance(ev_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',ev_id):raise ACOError('Provide a stable event id for safe retries')
        kind=entry.get('kind');state=entry.get('state',entry.get('status'));summary=entry.get('summary','')
        if entry.get('state') and entry.get('status') and entry['state']!=entry['status']:raise Conflict('Conflicting state/status fields')
        if kind not in EVENT_KINDS or state not in STATES or not isinstance(summary,str) or not summary.strip():raise ACOError('Event needs valid kind, state and summary')
        if state in {'executed','verified'} and not (entry.get('evidence') or entry.get('artifacts')):raise Conflict('Executed/verified work needs actual artifact or action evidence')
        if kind=='decision' and state in {'approved','executed','verified'} and not entry.get('approval_ref'):raise Conflict('Approved decisions need actual user approval')
        if state=='verified' and not entry.get('evidence'):raise Conflict('Verified results require evidence references')
        with self._lock():
            self._recover();r=self.registry();s=self._session(sid,r)
            if s['status']!='open':raise Conflict('Session closed')
            fingerprint=digest(json_bytes(entry))
            receipt_key=s['scope']['entity_id']+'/'+ev_id
            receipt_map=r.setdefault('event_receipts',{})
            if receipt_key in receipt_map:
                if receipt_map[receipt_key]!=fingerprint:raise Conflict('Cross-session event ID reused with different content')
                return {'status':'already_recorded','id':ev_id,'files_created':0}
            if ev_id in s['events']:
                if s['events'][ev_id]!=fingerprint:raise Conflict('Event id reused with different data')
                return {'status':'already_recorded','id':ev_id,'files_created':0}
            if entry.get('material') is False or kind in {'proposal','handoff'} or (kind=='decision' and state=='proposed'):
                s['events'][ev_id]=fingerprint;s['latest_summary']=summary;write_json(self.registry_path,r);self._write_handoff(s)
                return {'status':'local_handoff_only','files_created':0,'drive_verified':False}
            e=self.entity(s['scope']['entity_id'],r);doc=self._document(e);base=digest(doc.encode())
            section='decisions' if kind=='decision' else 'open' if kind=='open_loop' else 'recent'
            row=f'- [{ev_id}] {now()[:10]} · {state} · {_one_line(summary)}'
            row+=' <!-- payload:'+fingerprint+' -->'
            if entry.get('approval_ref'):row+=' · approval: '+_one_line(entry['approval_ref'])
            if e['storage']=='section':
                section='entity-'+e['id']
            body=_part(doc,section)
            # Cross-session idempotency in the canonical document as well as local receipts.
            oldrows=[x for x in body.splitlines() if x.startswith(f'- [{ev_id}] ')]
            if oldrows:
                if not any(('<!-- payload:'+fingerprint+' -->') in x for x in oldrows):raise Conflict('Canonical event id has different content')
                return {'status':'already_in_canonical','id':ev_id,'files_created':0}
            if section=='recent' and len([x for x in body.splitlines() if x.startswith('- [')])>=MAX_WORK:
                # No automatic deletion or archive explosion. Ask for one meaningful summary replacement.
                s['latest_summary']=summary;write_json(self.registry_path,r);self._write_handoff(s)
                return {'status':'compaction_review_required','files_created':0,'pending_summary':summary,'reason':'Recent work reached 20 material entries. Review a consolidation; no old entry was deleted.'}
            new=_replace(doc,section,(body.rstrip()+'\n'+row).strip())
            s['events'][ev_id]=fingerprint;s['latest_summary']=summary;receipt_map[receipt_key]=fingerprint
            self._commit(r,{e['document']:(base,new)});self._write_handoff(s)
            return {'status':'recorded','id':ev_id,'files_created':0,'persistence':'local_verified','drive_verified':False}

    def close(self,sid):
        with self._lock():
            self._recover();r=self.registry();s=self._session(sid,r);s['status']='closed';s['closed_at']=now();write_json(self.registry_path,r);self._write_handoff(s)
            return {'status':'closed','files_created':0,'persistence':'local_verified','drive_verified':False,'next':'Update the same canonical Drive document through a verified connected write; do not upload handoffs/events.'}

    def propose_context(self,eid,content,base_sha256,rationale):
        if not rationale.strip():raise ACOError('Explain the proposed context change')
        with self._lock():
            self._recover();r=self.registry();e=self.entity(eid,r);doc=self._document(e)
            if digest(doc.encode())!=base_sha256:raise Conflict('Stale canonical context')
            pid='proposal-'+digest((eid+base_sha256+content+rationale).encode())[:32]
            r['proposals'][pid]={'entity_id':eid,'content':content,'base_sha256':base_sha256,'rationale':rationale}
            write_json(self.registry_path,r)
            return {'status':'proposed_locally','proposal':pid,'files_created':0}

    def apply_context(self,eid,pid,approval_ref):
        if not approval_ref.strip():raise Conflict('Approval reference required')
        with self._lock():
            self._recover();r=self.registry();e=self.entity(eid,r);proposal=r['proposals'].get(pid)
            if not proposal or proposal['entity_id']!=eid:raise Conflict('Wrong proposal scope')
            doc=self._document(e);base=digest(doc.encode())
            if base!=proposal['base_sha256']:raise Conflict('Canonical changed after proposal; rebase explicitly')
            section='context' if e['storage']=='document' else 'entity-'+eid
            new=_replace(doc,section,proposal['content']);r['proposals'].pop(pid)
            self._commit(r,{e['document']:(base,new)})
            return {'status':'applied','persistence':'local_verified','drive_verified':False,'sha256':digest(new.encode())}

    def compact_recent(self,eid,summary,base_sha256,approval_ref):
        if not summary.strip() or not approval_ref.strip():raise Conflict('Reviewed summary and approval reference required')
        with self._lock():
            self._recover();r=self.registry();e=self.entity(eid,r);doc=self._document(e);base=digest(doc.encode())
            if base!=base_sha256:raise Conflict('Stale summary; reread recent work')
            if e['storage']!='document':raise Conflict('Compact only the selected canonical document')
            # One rotating LOCAL recovery copy, not a file per session on Drive.
            atomic_write(self.system/'previous-canonical.md',doc.encode())
            new=_replace(doc,'recent',f'- Consolidated {now()[:10]} · {_one_line(summary)} · approval: {_one_line(approval_ref)}')
            self._commit(r,{e['document']:(base,new)})
            return {'status':'compacted','files_created_in_knowledge':0,'persistence':'local_verified','decisions_preserved':True}

    def status(self):
        with self._lock():
            self._recover();r=self.registry()
            return {'version':VERSION,'layout':'compact','authority':r['authority'],'entities':len(r['entities']),'canonical_documents':len({e['document'] for e in r['entities'].values()}),'pipeline_is_not_entity':True,'open_sessions':sum(s['status']=='open' for s in r['sessions'].values()),'drive_verified':False}
