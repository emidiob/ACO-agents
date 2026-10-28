#!/usr/bin/env python3
"""Create a dependency-free editable example in a new directory."""
import argparse
from pathlib import Path
import shutil

def scaffold(output, layout):
    if layout not in ('editorial', 'workspace'): raise ValueError('Unknown layout')
    output = Path(output).expanduser().absolute()
    if output.exists() or any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError('Destination exists or uses a symlink; no files changed')
    source = Path(__file__).resolve().parents[1]/'assets'/layout
    if any(p.is_symlink() for p in source.rglob('*')): raise ValueError('Symlink source refused')
    shutil.copytree(source, output)
    return output

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--layout', choices=['editorial', 'workspace'], required=True)
    p.add_argument('--output', type=Path, required=True);a = p.parse_args()
    try: print(scaffold(a.output, a.layout))
    except (OSError, ValueError) as e:p.exit(1, str(e)+'\n')
