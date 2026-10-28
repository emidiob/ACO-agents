#!/usr/bin/env python3
"""Export ACO's original development-only Vite source editor bridge."""
import argparse
from pathlib import Path
import shutil
SOURCE=Path(__file__).resolve().parents[1]/'assets/framework-live'
def export(destination):
    destination=Path(destination).expanduser().absolute()
    if any(p.is_symlink() for p in (destination,*destination.parents)):raise ValueError('Symlink destination refused')
    if destination.exists():raise ValueError('Destination already exists')
    if destination.is_relative_to(SOURCE.parents[1]):raise ValueError('Export outside the skill directory')
    shutil.copytree(SOURCE,destination)
    return destination
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);a=p.parse_args()
    try:print(export(a.destination))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
