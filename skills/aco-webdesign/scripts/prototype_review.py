#!/usr/bin/env python3
"""Create a local comparison page for functional prototypes and content stress cases."""
import argparse
import html
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parents[1] / 'assets' / 'prototype-review'

def validate(config):
    if not isinstance(config, dict) or not isinstance(config.get('variants'), list):
        raise ValueError('Expected an object with a variants list')
    if not 2 <= len(config['variants']) <= 8:
        raise ValueError('Supply two to eight functional variants')
    names = set()
    for variant in config['variants']:
        if not isinstance(variant, dict) or set(variant) - {'name', 'url', 'rationale'}:
            raise ValueError('Variant fields: name, url, rationale')
        name, url = variant.get('name'), variant.get('url')
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError('Each variant needs a unique nonempty name')
        names.add(name)
        if not isinstance(url, str) or any(ord(c) < 32 for c in url) or '\\' in url:
            raise ValueError('Invalid prototype URL')
        parsed = urlsplit(url)
        local = parsed.scheme in ('http', 'https') and parsed.hostname in ('localhost', '127.0.0.1', '::1') and not parsed.username and not parsed.password
        relative = not parsed.scheme and not parsed.netloc and url.startswith('/') and not url.startswith('//')
        if not (local or relative):
            raise ValueError('Use local development URLs or absolute paths on the review server')
        if 'rationale' in variant and not isinstance(variant['rationale'], str):
            raise ValueError('Rationale must be text')
    return config

def export(config, output):
    validate(config)
    output = Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink() or any(p.is_symlink() for p in output.parents):
        raise ValueError('Output must be a new directory without symlink ancestors')
    if not output.parent.is_dir():
        raise ValueError('Output parent must exist')
    data = json.dumps(config, ensure_ascii=False).replace('<', '\\u003c').replace('&', '\\u0026')
    title = html.escape(str(config.get('title', 'ACO prototype review')))
    document = (ASSETS / 'index.html').read_text().replace('ACO_TITLE', title).replace('ACO_CONFIG', data)
    output.mkdir()
    (output / 'index.html').write_text(document, encoding='utf-8')
    shutil.copy2(ASSETS / 'review.js', output / 'review.js')
    shutil.copy2(ASSETS / 'review.css', output / 'review.css')
    return output

def stress(seed=0):
    # Stable synthetic examples; no user data or network access.
    return {'schema': 1, 'seed': seed, 'cases': [
        {'id': 'empty', 'title': '', 'description': '', 'items': []},
        {'id': 'long-copy', 'title': 'A project title that must remain readable when translated and expanded ' * 5, 'description': 'Detailed supporting information. ' * 80},
        {'id': 'unbroken', 'title': 'LongIdentifier' * 40, 'url': 'https://example.invalid/' + 'segment' * 80},
        {'id': 'unicode', 'title': '東京 — café — مرحباً — 👩🏽‍💻', 'description': 'e\u0301 / é; thin\u2009space; nonbreaking\u00a0space'},
        {'id': 'rtl', 'dir': 'rtl', 'lang': 'ar', 'title': 'مراجعة المشروع', 'description': 'تحتوي هذه الصفحة على معلومات متعددة اللغات 123 ABC'},
        {'id': 'large-list', 'items': [{'id': f'item-{seed}-{i}', 'title': f'Record {i + 1}', 'value': (i * 37 + seed) % 1000} for i in range(1000)]},
        {'id': 'zero-negative', 'values': [0, -1, -1234567.89, 0.000001, 9999999999]},
        {'id': 'states', 'states': ['loading', 'empty', 'error', 'offline', 'disabled', 'success'], 'error': 'The connection was interrupted. Your draft is preserved. Try again.'}
    ], 'usage': 'Bind the selected case to the actual component props or test route; no DOM is modified automatically.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    compare = commands.add_parser('compare'); compare.add_argument('config', type=Path); compare.add_argument('--output', required=True, type=Path)
    fixture = commands.add_parser('stress'); fixture.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    try:
        if args.command == 'stress':
            print(json.dumps(stress(args.seed), ensure_ascii=False, indent=2))
        else:
            print(export(json.loads(args.config.read_text(encoding='utf-8')), args.output))
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + '\n')

if __name__ == '__main__':
    main()
