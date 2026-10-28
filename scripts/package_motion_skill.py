#!/usr/bin/env python3
"""Export the canonical native ACO Motion as an independent Agent Skill ZIP."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def package(output, skill="aco-motion"):
    if skill not in ("aco-motion", "aco-capture", "aco-image", "aco-video", "aco-genjutsu", "aco-webdesign"):
        raise ValueError("Unsupported portable skill")
    output=Path(output).expanduser().absolute()
    if any(p.is_symlink() for p in (output,*output.parents)):raise ValueError('Symlink output refused')
    if output.exists():raise ValueError('Output already exists')
    if output.is_relative_to(ROOT):raise ValueError('Place the package outside the library')
    source=ROOT/'skills'/skill;files={}
    for p in source.rglob('*'):
        if p.is_symlink():raise ValueError('Symlink source refused')
        if p.is_file() and '__pycache__' not in p.parts:
            rel=p.relative_to(source).as_posix();files[rel]=p.read_bytes()
            if p.suffix=='.md':
                for target in re.findall(r'\]\(([^\s)]+)\)',p.read_text()):
                    if '://' in target or target.startswith('#'):continue
                    resolved=(p.parent/target.split('#')[0]).resolve()
                    if not resolved.is_relative_to(source) or not resolved.is_file():raise ValueError('Nonportable reference: '+target)
    files['LICENSE']=(ROOT/'LICENSE').read_bytes()
    meta={'aco_version':(ROOT/'VERSION').read_text().strip(),'skill':skill,'standalone':True,
          'files':{n:hashlib.sha256(b).hexdigest() for n,b in sorted(files.items())}}
    files['package-manifest.json']=(json.dumps(meta,indent=2)+'\n').encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('xb') as stream:
        with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for n,b in sorted(files.items()):
                info=zipfile.ZipInfo(skill+'/'+n,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
    return {'zip':str(output),'files':len(files),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--skill',default='aco-motion')
    args=p.parse_args()
    try:print(json.dumps(package(args.output,args.skill),indent=2))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
