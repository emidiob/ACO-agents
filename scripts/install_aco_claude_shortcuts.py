#!/usr/bin/env python3
"""Install ACO skills in Claude Code safely, dry-run by default.

The seven shortcuts refer to neighboring canonical office skill directories,
so copy *all* ACO skill folders from the complete checkout, not only shortcuts.
No provider credentials/network use; unrelated files are never overwritten.
"""
from __future__ import annotations
import argparse
import shutil
import sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--apply',action='store_true',help='Copy all managed ACO skills into Claude')
    ap.add_argument('--project',type=Path,help='Install inside this project instead of user home')
    a=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    source=root/'skills'
    target=(a.project.expanduser().resolve()/'.claude/skills') if a.project else Path.home()/'.claude/skills'
    if not source.is_dir():raise RuntimeError('Run from a complete ACO source checkout')
    if target.is_symlink():raise RuntimeError('Target directory is a symlink')
    pairs=[]
    for folder in sorted(source.iterdir()):
        if not folder.is_dir() or folder.is_symlink() or not (folder/'SKILL.md').is_file():continue
        for src in sorted(folder.rglob('*')):
            if src.is_symlink():raise RuntimeError('Source symlink refused: '+str(src))
            if not src.is_file():continue
            dest=target/src.relative_to(source)
            if any(p.is_symlink() for p in [dest,*dest.parents]):
                raise RuntimeError('Destination symlink refused: '+str(dest))
            if dest.exists() and (not dest.is_file() or dest.read_bytes()!=src.read_bytes()):
                raise RuntimeError('Unmanaged conflicting file, no write: '+str(dest))
            pairs.append((src,dest))
    print(('APPLY' if a.apply else 'DRY RUN'),len(pairs),'ACO source files; includes native /aco and /aco-genjutsu.')
    if a.apply:
        for src,dest in pairs:
            if not dest.exists():
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(src,dest)
        print('ACO Claude skills copied. Start a new Claude Code session to verify discovery.')
    else:print('No files written. Add --apply to copy.')

if __name__=='__main__':
    try:main()
    except Exception as e:print('ERROR:',e,file=sys.stderr);sys.exit(1)
