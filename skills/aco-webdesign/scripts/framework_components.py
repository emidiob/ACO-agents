#!/usr/bin/env python3
"""Export original ACO React or Vue components with framework-owned state."""
import argparse
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]/'assets'
NAMES=('Button','Toggle','Checkbox','TextField','Select','Tabs','Accordion','Dialog')
def export(destination,framework):
    if framework not in ('react','vue'):raise ValueError('Use react or vue')
    destination=Path(destination).expanduser().absolute()
    if destination.exists():raise ValueError('Destination already exists')
    if any(p.is_symlink() for p in (destination,*destination.parents)):raise ValueError('Symlink destination refused')
    if destination.is_relative_to(ROOT.parent):raise ValueError('Export outside the skill')
    destination.mkdir(parents=True)
    source=ROOT/'framework-components'/('react.jsx' if framework=='react' else 'vue.mjs')
    shutil.copy2(source,destination/('aco-components'+source.suffix));shutil.copy2(ROOT/'components/aco.css',destination/'aco.css')
    return destination
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);p.add_argument('--framework',required=True,choices=['react','vue']);a=p.parse_args()
    try:print(export(a.destination,a.framework))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
