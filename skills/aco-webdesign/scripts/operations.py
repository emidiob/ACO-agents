#!/usr/bin/env python3
"""Discover original ACO methods without implying runtime capability."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def operations():
    return json.loads((ROOT / 'assets/operations.json').read_text())

def show(name):
    entry = next((x for x in operations() if x['name'] == name), None)
    if entry is None:
        raise ValueError('Unknown operation: ' + name)
    path = ROOT / entry['reference']
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise ValueError('Operation reference escapes the skill')
    return path.read_text()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    selected = sub.add_parser('show')
    selected.add_argument('name', choices=[x['name'] for x in operations()])
    args = p.parse_args()
    print(json.dumps({'kind':'agent_methods','operations':operations()},indent=2) if args.command == 'list' else show(args.name))

if __name__ == '__main__':
    main()
