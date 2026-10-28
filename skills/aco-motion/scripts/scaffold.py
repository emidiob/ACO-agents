#!/usr/bin/env python3
"""Create an original ACO motion starter without downloading or running dependencies."""
import argparse
import json
import shutil
from pathlib import Path

def scaffold(output):
    output=Path(output).expanduser().absolute()
    if any(p.is_symlink() for p in (output,*output.parents)):
        raise ValueError('Symlink destinations are not supported')
    if output.exists(): raise ValueError('Output already exists; choose a new project directory')
    source=Path(__file__).resolve().parents[1]/'assets/starter'
    if any(p.is_symlink() for p in source.rglob('*')): raise ValueError('Source symlink refused')
    shutil.copytree(source, output)
    return {'status':'created','project':str(output),'dependencies_installed':False,
            'next':['npm ci','npm run preview','npm run render'],
            'ui':'ui.html','note':'Run commands in the project after checking available Node/browser/ffmpeg.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path)
    try: print(json.dumps(scaffold(p.parse_args().output),indent=2))
    except (OSError,ValueError) as e:p.exit(1,str(e)+'\n')
