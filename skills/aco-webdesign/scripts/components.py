#!/usr/bin/env python3
"""Search, inspect and export the original ACO HTML component catalog."""
import argparse
import json
from pathlib import Path
import shutil
from html import escape

ROOT=Path(__file__).resolve().parents[1]/'assets/components'

def catalog():return json.loads((ROOT/'catalog.json').read_text())
def export(destination,names):
    destination=Path(destination)
    if destination.exists():raise ValueError('Destination already exists')
    entries={e['id']:e for e in catalog()}
    if not names or set(names)-entries.keys():raise ValueError('Select known component IDs')
    blocks=[]
    for name in names:
        source=(ROOT/(name+'.html')).read_text()
        blocks.append('<section class="example" id="example-'+name+'"><h2>'+escape(entries[name]['name'])+'</h2>'+source+'</section>')
    destination.mkdir(parents=True)
    for name in ('aco.css','aco.js'):shutil.copy2(ROOT/name,destination/name)
    (destination/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ACO Components</title><link rel="stylesheet" href="aco.css"><script src="aco.js" defer></script><body><main><h1>ACO Components</h1><label>Find a component <input type="search" data-catalog-search></label><div class="catalog">'+''.join(blocks)+'</div></main></body></html>')
    (destination/'catalog.json').write_text(json.dumps([entries[n] for n in names],indent=2)+'\n')
    return destination

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    q=sub.add_parser('list');q.add_argument('--query',default='')
    q=sub.add_parser('show');q.add_argument('component')
    q=sub.add_parser('export');q.add_argument('destination',type=Path);q.add_argument('components',nargs='*');q.add_argument('--all',action='store_true')
    a=p.parse_args()
    try:
        if a.action=='list':print(json.dumps([e for e in catalog() if a.query.lower() in json.dumps(e).lower()],indent=2))
        elif a.action=='show':
            if a.component not in {e['id'] for e in catalog()}:raise ValueError('Unknown component')
            print((ROOT/(a.component+'.html')).read_text())
        else:print(export(a.destination,[e['id'] for e in catalog()] if a.all else a.components))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
