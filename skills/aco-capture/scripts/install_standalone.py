#!/usr/bin/env python3
"""Install/update this standalone skill. Preview by default; preserve modified/unowned files."""
import argparse
import hashlib
import json
import shutil
import tempfile
import time
from pathlib import Path

LEDGER='.aco-capture-owned.json'
def hashes(root):
    result={}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():raise ValueError('Symlink refused: '+str(p))
        if p.is_file() and '__pycache__' not in p.parts and p.name!=LEDGER:
            result[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result

def install(source, root, apply=False):
    source=Path(source).resolve();root=Path(root).expanduser().absolute();target=root/'aco-capture'
    if any(p.is_symlink() for p in (target,*target.parents)):raise ValueError('Symlink target refused')
    desired=hashes(source)
    if target.resolve()==source:return {'status':'already_at_target','target':str(target)}
    if target.exists():
        current=hashes(target)
        if current==desired:return {'status':'already_present','target':str(target)}
        ledger=target/LEDGER
        if not ledger.is_file() or json.loads(ledger.read_text()).get('files')!=current:
            raise ValueError('Unmanaged or locally modified skill; no files changed. Use the ACO installer for an integrated installation.')
    result={'status':'preview','target':str(target),'files':len(desired)}
    if not apply:return result
    root.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.aco-capture-stage-',dir=root));backup=None
    try:
        for rel in desired:
            dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,dest)
        (stage/LEDGER).write_text(json.dumps({'files':desired},indent=2)+'\n')
        if hashes(stage)!=desired:raise ValueError('Staging verification failed')
        if target.exists():
            backup=root/('.aco-capture-backup-'+str(time.time_ns()));target.rename(backup)
        try:stage.rename(target)
        except Exception:
            if backup is not None:backup.rename(target)
            raise
    finally:
        if stage.exists():shutil.rmtree(stage)
    result.update(status='installed',backup=str(backup) if backup else None)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--host',choices=['claude','codex'],required=True);p.add_argument('--project',type=Path);p.add_argument('--apply',action='store_true')
    a=p.parse_args();home=a.project or Path.home();root=home/('.claude/skills' if a.host=='claude' else '.agents/skills')
    try:print(json.dumps(install(Path(__file__).resolve().parents[1],root,a.apply),indent=2))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
