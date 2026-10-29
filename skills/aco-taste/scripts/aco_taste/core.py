"""ACO Taste Intelligence: explicit project-scoped design evidence, stdlib-only."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, tempfile, uuid

SCHEMA = 1

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')

def project_root(value: str) -> Path:
    p = Path(value).expanduser().resolve(strict=True)
    if not p.is_dir(): raise ValueError('Project must be an existing directory')
    return p

def store_root(project: Path) -> Path:
    return project / '.aco-taste'

def require_nonblank(text, field: str, max_len: int = 3000) -> str:
    if not isinstance(text,str) or not text.strip() or len(text)>max_len:
        raise ValueError(field+' requires nonempty text within '+str(max_len)+' characters')
    return text.strip()

def load(path: Path, default=None):
    if not path.exists(): return default
    if path.is_symlink():raise ValueError('Refusing symlink: '+str(path))
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e: raise ValueError('Invalid JSON; original preserved: '+str(path)) from e

def write(path: Path, data, *, overwrite=True):
    """Only explicit requested operations write; atomic without silently replacing corrupt history."""
    if path.exists() and (not overwrite or path.is_symlink()):raise ValueError('Existing or symlink path protected: '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.parent.is_symlink():raise ValueError('Symlink state parent blocked')
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'-',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def append_line(path:Path,item:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.is_symlink() or path.parent.is_symlink():raise ValueError('Symlink journal refused')
    with path.open('a',encoding='utf-8') as f:f.write(json.dumps(item,ensure_ascii=False,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())

def read_lines(path:Path):
    if not path.exists():return []
    if path.is_symlink():raise ValueError('Symlink journal refused')
    out=[]
    for idx,line in enumerate(path.read_text(encoding='utf-8').splitlines(),start=1):
        try:out.append(json.loads(line))
        except ValueError as e:raise ValueError(f'Journal corrupt at line {idx}; do not overwrite') from e
    return out

def digest(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def collections(project:Path):
    data=load(store_root(project)/'collections.json',{'schema_version':1,'collections':[]})
    if data.get('schema_version')!=SCHEMA or not isinstance(data.get('collections'),list):raise ValueError('Invalid collections schema; no edits allowed')
    return data

def new_collection(project:Path,name:str,description:str='',scope:str='project'):
    require_nonblank(name,'collection name',150)
    if scope not in {'project','personal'}:raise ValueError('Scope must be project or personal; personal sharing requires separate authorization')
    data=collections(project)
    item={'id':'col-'+uuid.uuid4().hex[:12],'name':name,'description':description,'scope':scope,'status':'exploring','created_at':now(),'references':[],'approved':False}
    data['collections'].append(item);write(store_root(project)/'collections.json',data)
    return item

def add_reference(project:Path,collection_id:str,*,url=None,file=None,note='',role='inspiration',negative=False,rights='unknown'):
    if bool(url)==bool(file): raise ValueError('Pass exactly one URL or local file')
    if role not in {'inspiration','direction','negative','constraint'}:raise ValueError('Unknown reference role')
    if rights not in {'unknown','permission','public-domain','cc0','cc-by','cc-by-sa','restricted'}:raise ValueError('Unknown rights state')
    data=collections(project)
    col=next((c for c in data['collections'] if c['id']==collection_id),None)
    if col is None:raise ValueError('Unknown collection')
    if url:
        if not re.match(r'^https?://[^\s/]+',url) or len(url)>2000:raise ValueError('HTTP(S) URL required')
        source={'url':url,'kind':'url','not_retrieved':True}
    else:
        p=Path(file).expanduser().resolve(strict=True)
        if not p.is_file() or p.stat().st_size>12*1024*1024:raise ValueError('Reference must be a file up to 12 MB')
        source={'file':str(p),'kind':'local_file','sha256':digest(p),'not_retrieved':False}
    entry={'id':'ref-'+uuid.uuid4().hex[:12],**source,'note':note,'role':role,'negative':negative,'rights':rights,'added_at':now(), 'approval':'not_assumed'}
    col['references'].append(entry);write(store_root(project)/'collections.json',data)
    return entry

def add_feedback(project:Path,variant_id:str,judgment:str,reason:str,*,scope='current-project',artifact=None,aspects=None):
    require_nonblank(variant_id,'variant',150);require_nonblank(reason,'reason',1200)
    if judgment not in {'prefer','reject','both','neither','depends','approve','revision'}:raise ValueError('Unknown judgment')
    e={'id':'ev-'+uuid.uuid4().hex[:12],'time':now(),'variant_id':variant_id,'judgment':judgment,'reason':reason,'scope':scope,'artifact':artifact,'aspects':aspects or [],'evidence_type':'explicit_user_feedback'}
    append_line(store_root(project)/'feedback.jsonl',e);return e

def insights(project:Path,*,scope='current-project'):
    records=[r for r in read_lines(store_root(project)/'feedback.jsonl') if r.get('scope')==scope]
    groups={}
    for ev in records:
        for aspect in ev.get('aspects') or ['overall']:
            key=str(aspect).strip().lower()
            if not key:continue
            groups.setdefault(key,[]).append(ev)
    result=[]
    for aspect,evs in groups.items():
        positive=[e for e in evs if e.get('judgment') in {'prefer','approve'}]
        negative=[e for e in evs if e.get('judgment') in {'reject','neither'}]
        qualified=[e for e in evs if e.get('judgment') in {'depends','both','revision'}]
        result.append({'aspect':aspect,'positive_events':[x['id'] for x in positive],'negative_events':[x['id'] for x in negative],'qualified_events':[x['id'] for x in qualified], 'inference':'ambiguous' if positive and negative else 'positive_evidence_only' if positive else 'negative_evidence_only' if negative else 'undetermined','confidence':'tentative' if len(evs)<3 else 'evidence-rich-but-contextual', 'scope':scope,'notes':'Compare original reasons; do not infer universal preferences from a relative choice.'})
    return {'scope':scope,'events_read':len(records),'insights':sorted(result,key=lambda x:x['aspect']),'automatic_global_taste_profile':False}

def status(project:Path):
    data=collections(project)
    ev=read_lines(store_root(project)/'feedback.jsonl')
    return {'project':str(project),'state':str(store_root(project)), 'collections':len(data['collections']),'references':sum(len(x['references']) for x in data['collections']),'feedback_events':len(ev),'scope_policy':'local project only; no automatic sharing or cross-project memory','model_trained':False}
