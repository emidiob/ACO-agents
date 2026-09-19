#!/usr/bin/env python3
"""Package only fingerprinted public release files, with executable modes preserved."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path
from aco.common import ACOError, ROOT, VERSION, no_symlinks
from aco.install import verify_release


def build(output: Path) -> dict:
    output=output.expanduser().absolute()
    no_symlinks(output)
    if output.is_relative_to(ROOT):
        raise ACOError('Place the distributable ZIP outside the source checkout.')
    if output.suffix.lower()!='.zip':
        raise ACOError('Output must be a ZIP path.')
    manifest=verify_release()
    files=dict(manifest['files'])
    files['release/manifest.json']={'mode':0o644}
    output.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(dir=output.parent,prefix='.aco-release-',suffix='.zip')
    os.close(fd)
    try:
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,meta in sorted(files.items()):
                info=zipfile.ZipInfo('ACO-agents/'+name,date_time=(2026,1,1,0,0,0))
                info.create_system=3
                info.external_attr=(0o100000 | meta.get('mode',0o644)) << 16
                info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,(ROOT/name).read_bytes())
        os.replace(temp,output)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    sha=hashlib.sha256(output.read_bytes()).hexdigest()
    checksum=output.with_suffix(output.suffix+'.sha256')
    no_symlinks(checksum)
    checksum.write_text(sha+'  '+output.name+'\n')
    return {'version':VERSION,'zip':str(output),'sha256':sha,'files':len(files),'bytes':output.stat().st_size}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    try:print(json.dumps(build(p.parse_args().output),indent=2))
    except (ACOError,OSError,ValueError) as e:p.exit(1,str(e)+'\n')
