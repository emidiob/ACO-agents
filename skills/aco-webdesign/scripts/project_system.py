#!/usr/bin/env python3
"""Resolve project tokens and page overrides without mutating the master."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

NAME = re.compile(r'[a-z][a-z0-9-]*\Z')
REFERENCE = re.compile(r'\{([a-z][a-z0-9.-]*)\}')

def merge(master, override):
    """Recursive object overlay; arrays replace, null removes an inherited key."""
    if not isinstance(master, dict) or not isinstance(override, dict):
        raise ValueError('Master and overrides must be objects')
    result = deepcopy(master)
    for key, value in override.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict):
            result[key] = merge(result.get(key, {}) if isinstance(result.get(key), dict) else {}, value)
        else:
            result[key] = deepcopy(value)
    return result

def flatten(tokens, prefix=''):
    if not isinstance(tokens, dict):
        raise ValueError('Tokens must be an object')
    result = {}
    for name, value in tokens.items():
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise ValueError('Token names must be lowercase words separated by hyphens')
        key = prefix + name
        if isinstance(value, dict):
            result.update(flatten(value, key + '.'))
        elif isinstance(value, str) and value.strip():
            result[key] = value
        else:
            raise ValueError('Token values must be nonempty strings or nested objects')
    return result

def resolve(document, page=None):
    if not isinstance(document, dict) or document.get('schema') != 1:
        raise ValueError('Expected a schema 1 project system')
    master = document.get('master', {})
    pages = document.get('pages', {})
    if not isinstance(pages, dict):
        raise ValueError('Pages must be an object')
    if page is not None and page not in pages:
        raise ValueError('Unknown page: ' + page)
    effective = merge(master, pages[page] if page is not None else {})
    tokens = flatten(effective.get('tokens', {}))
    names = [key.replace('.', '-') for key in tokens]
    if len(names) != len(set(names)):
        raise ValueError('Token paths collide as CSS custom properties')
    resolved = {}
    def visit(key, chain):
        if key not in tokens:
            raise ValueError('Missing token reference: ' + key)
        if key in chain:
            raise ValueError('Cyclic token reference: ' + ' -> '.join(chain + [key]))
        if key not in resolved:
            resolved[key] = REFERENCE.sub(lambda m: visit(m[1], chain + [key]), tokens[key])
            # Values only: declarations, URLs and stylesheet escape characters are refused.
            if re.search(r'[{};<>\\\x00-\x1f]|/\*|\*/|url\s*\(|@', resolved[key], re.I):
                raise ValueError('Unsafe CSS token value: ' + key)
        return resolved[key]
    for key in tokens:
        visit(key, [])
    css = ':root {\n' + ''.join(f'  --{key.replace(".", "-")}: {resolved[key]};\n' for key in sorted(tokens)) + '}\n'
    canonical = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return {'schema': 1, 'page': page, 'source_sha256': hashlib.sha256(canonical.encode()).hexdigest(),
            'effective': effective, 'resolved_tokens': resolved, 'css': css}

def from_proposal(proposal):
    colors = proposal.get('color_tokens', {})
    flatten({'color': colors})
    return {'schema': 1, 'brief': proposal.get('brief', ''), 'master': {'tokens': {'color': colors}}, 'pages': {}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('system', type=Path)
    parser.add_argument('--page')
    parser.add_argument('--format', choices=['json', 'css'], default='json')
    parser.add_argument('--from-proposal', action='store_true')
    args = parser.parse_args()
    try:
        document = json.loads(args.system.read_text(encoding='utf-8'))
        result = from_proposal(document) if args.from_proposal else resolve(document, args.page)
        if args.format == 'css':
            if args.from_proposal:
                result = resolve(result)
            print(result['css'], end='')
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, RecursionError) as error:
        parser.exit(2, str(error) + '\n')

if __name__ == '__main__':
    main()
