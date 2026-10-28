#!/usr/bin/env python3
"""Fetch an explicitly selected, pinned external dataset; never fetch/execute tools."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

def fetch(output):
    output=Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink() or any(p.is_symlink() for p in output.parents):
        raise ValueError('Output must be new, without symlink ancestors')
    if not output.parent.is_dir():raise ValueError('Output parent must already exist')
    source=json.loads((ROOT/'assets/external-data-source.json').read_text())
    prefix=f"https://raw.githubusercontent.com/{source['repository']}/{source['revision']}/"
    staging=Path(tempfile.mkdtemp(prefix='.aco-data-',dir=output.parent))
    try:
        def download(entry):
            rel=PurePosixPath(entry['path'])
            if rel.is_absolute() or '..' in rel.parts or not entry['url'].startswith(prefix):
                raise ValueError('Invalid pinned source entry')
            if rel.suffix not in ('.csv','.json') and str(rel)!='LICENSE':
                raise ValueError('Only data and LICENSE may be fetched')
            request=urllib.request.Request(entry['url'],headers={'User-Agent':'ACO-data-fetch'})
            with urllib.request.urlopen(request,timeout=45) as response:
                raw=response.read(16*1024*1024+1)
            if len(raw)>16*1024*1024 or hashlib.sha256(raw).hexdigest()!=entry['sha256']:
                raise ValueError('Size or integrity failure: '+str(rel))
            dest=staging/str(rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,source['files']))
        (staging/'aco-source.json').write_text(json.dumps(source,indent=2)+'\n')
        # mkdir reserves the destination and prevents overwriting a concurrent creation.
        output.mkdir()
        for item in staging.iterdir():shutil.move(str(item),str(output/item.name))
        return {'output':str(output),'files':len(source['files']),'revision':source['revision']}
    finally:shutil.rmtree(staging)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(fetch(a.output),indent=2))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
