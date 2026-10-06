"""ACO 1.0 runtime/bootstrap resolution."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, VERSION, no_symlinks, read_json

def _valid_runtime(path: Path) -> tuple[bool, str | None]:
    try:
        path=path.expanduser().absolute(); no_symlinks(path)
        version=path/'VERSION'; bootstrap=path/'registry/bootstrap.json'
        if not version.is_file() or not bootstrap.is_file(): return False,None
        value=version.read_text(encoding='utf-8').strip(); data=read_json(bootstrap)
        if data.get('schema_version')!=1 or data.get('aco_version')!=value:return False,value
        return True,value
    except (OSError,ACOError): return False,None

def _enclosing_runtime(start: Path|None)->Path|None:
    if start is None:return None
    start=start.expanduser().absolute(); cursor=start if start.is_dir() else start.parent
    for candidate in (cursor,*cursor.parents):
        valid,_=_valid_runtime(candidate)
        if valid:return candidate
    return None

def resolve_runtime(*,explicit_root:Path|None=None,start:Path|None=None,env:dict[str,str]|None=None)->dict[str,Any]:
    env=dict(os.environ if env is None else env); candidates=[]
    if explicit_root is not None:candidates.append(('explicit_root',explicit_root))
    runtime_env=env.get('ACO_RUNTIME_ROOT','').strip()
    if runtime_env:candidates.append(('ACO_RUNTIME_ROOT',Path(runtime_env)))
    enclosing=_enclosing_runtime(start)
    if enclosing is not None:candidates.append(('enclosing_project',enclosing))
    candidates.append(('packaged_runtime',ROOT));seen=set();attempts=[]
    for source,raw in candidates:
        path=raw.expanduser().absolute();key=str(path)
        if key in seen:continue
        seen.add(key);valid,version=_valid_runtime(path);attempts.append({'source':source,'path':key,'valid':valid,'version':version})
        if valid:
            bootstrap=read_json(path/'registry/bootstrap.json');state_root=Path(env.get('ACO_HOME',str(Path.home()/'.local/share/aco'))).expanduser().absolute()
            return {'status':'resolved','aco_version':version,'logical_root':'aco://current','runtime_root':key,'runtime_source':source,'state_root':str(state_root),'code_state_separated':path!=state_root,'bootstrap':bootstrap,'first_reads':['VERSION','registry/bootstrap.json'],'preload_repository':False,'host_resolution':bootstrap.get('host_resolution',{}),'attempts':attempts,'policy':'Resolve code/runtime separately from private state. Read the bootstrap and registries first; never preload the full repository.'}
    return {'status':'unresolved','aco_version':VERSION,'logical_root':'aco://current','attempts':attempts,'preload_repository':False,'host_resolution':{'policy':'Use an explicitly attached/project ACO release or an authorized canonical repository when the host supports repository/file retrieval; verify VERSION before use.'},'policy':'Do not invent an ACO runtime path. Continue only from the minimal bootstrap or ask the host to expose the configured runtime.'}

def bootstrap_check(root:Path|None=None)->dict[str,Any]:
    root=(root or ROOT).expanduser().absolute();valid,version=_valid_runtime(root);errors=[]
    if not valid:return {'status':'invalid','aco_version':VERSION,'root':str(root),'errors':['runtime must contain matching VERSION and registry/bootstrap.json']}
    data=read_json(root/'registry/bootstrap.json')
    if data.get('logical_root')!='aco://current':errors.append('logical_root must be aco://current')
    if data.get('runtime_env')!='ACO_RUNTIME_ROOT':errors.append('runtime_env must be ACO_RUNTIME_ROOT')
    if data.get('state_env')!='ACO_HOME':errors.append('state_env must be ACO_HOME')
    if data.get('preload_repository') is not False:errors.append('bootstrap must forbid repository preload')
    host=data.get('host_resolution',{})
    if not isinstance(host,dict) or host.get('canonical_repository')!='emidiob/ACO-agents' or host.get('requires_authorized_access') is not True:errors.append('host_resolution must name the authorized canonical repository fallback')
    target=data.get('bootstrap_token_target')
    if not isinstance(target,int) or isinstance(target,bool) or not 100<=target<=800:errors.append('bootstrap_token_target must be 100..800')
    return {'status':'valid' if not errors else 'invalid','aco_version':version,'root':str(root),'errors':errors,'bootstrap':data}
