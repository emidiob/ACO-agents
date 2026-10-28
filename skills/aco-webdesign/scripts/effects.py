#!/usr/bin/env python3
"""Export configurable original ACO text, interaction and canvas effects."""
import argparse
from html import escape
import json
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]/'assets/effects'

def export(dest,ids,text='Ideas in motion',duration=2400):
    entries={e['id']:e for e in json.loads((ROOT/'catalog.json').read_text())}
    if not ids or set(ids)-entries.keys():raise ValueError('Select known effect IDs')
    if not 200<=duration<=30000:raise ValueError('Duration must be 200–30000 ms')
    dest=Path(dest)
    if dest.exists():raise ValueError('Destination already exists')
    blocks=[]
    for id in ids:
        entry=entries[id];content=('<canvas aria-label="'+escape(entry['description'],quote=True)+'" role="img"></canvas>' if entry['category']=='canvas' else '<span class="effect-text">'+escape(text)+'</span>')
        blocks.append('<article><h2>'+escape(entry['name'])+'</h2><p>'+escape(entry['description'])+'</p><div class="stage" tabindex="0" data-effect="'+id+'" data-duration="'+str(duration)+'">'+content+'</div><button data-replay>Replay</button><button data-pause aria-pressed="false">Pause</button></article>')
    dest.mkdir(parents=True)
    for name in ('effects.css','effects.js'):shutil.copy2(ROOT/name,dest/name)
    (dest/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ACO Effects</title><link rel="stylesheet" href="effects.css"><script src="effects.js" defer></script><body><main><h1>ACO Effects</h1><p>Original effects with pause, replay and reduced-motion support.</p><div class="gallery">'+''.join(blocks)+'</div></main></body></html>')
    (dest/'catalog.json').write_text(json.dumps([entries[id] for id in ids],indent=2)+'\n')
    return dest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True);q=sub.add_parser('list');q.add_argument('--query',default='');q=sub.add_parser('export');q.add_argument('destination',type=Path);q.add_argument('effects',nargs='*');q.add_argument('--all',action='store_true');q.add_argument('--text',default='Ideas in motion');q.add_argument('--duration',type=int,default=2400);a=p.parse_args()
    try:
        entries=json.loads((ROOT/'catalog.json').read_text())
        if a.action=='list':print(json.dumps([e for e in entries if a.query.lower() in json.dumps(e).lower()],indent=2))
        else:print(export(a.destination,[e['id'] for e in entries] if a.all else a.effects,a.text,a.duration))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
