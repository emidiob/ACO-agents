#!/usr/bin/env python3
"""Check local reference files and prompt bindings, not model output quality or provider acceptance."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path


def check(folder):
    folder = Path(folder).resolve(strict=True)
    data = json.loads((folder / 'reference-map.json').read_text())
    errors = []
    if data.get('intent') not in ('unchanged recreation', 'requested transformation'):
        errors.append('Select the actual recreation intent')
    refs = data.get('references', [])
    if not refs:
        errors.append('No references listed')
    prompt_path = folder / 'shot-prompt.txt'
    prompt = prompt_path.read_text() if prompt_path.is_file() else ''
    if not prompt.strip():
        errors.append('Missing shot-prompt.txt')
    previous = -1
    names = set()
    for ref in refs:
        name = ref.get('file', '')
        path = folder / name
        if not name or path.is_symlink() or not path.resolve().is_relative_to(folder) or not path.is_file():
            errors.append(f'Invalid or missing reference: {name}')
            continue
        if name in names:
            errors.append(f'Duplicate reference: {name}')
        names.add(name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != ref.get('sha256'):
            errors.append(f'Reference changed after mapping: {name}')
        time = ref.get('source_time_seconds')
        if not isinstance(time, (int, float)) or not math.isfinite(time) or time < previous or time < 0:
            errors.append(f'Invalid or unordered timestamp: {name}')
        else:
            previous = time
            if not any(name in line and re.search(r'(?<![\d.])' + re.escape(f'{time:g} s') + r'(?!\w)', line) for line in prompt.splitlines()):
                errors.append(f'Missing prompt timestamp for {name}: {time:g} s')
        if not ref.get('purpose', '').strip() or ref.get('visually_reviewed') is not True:
            errors.append(f'Purpose or recorded visual review missing: {name}')
        if name not in prompt:
            errors.append(f'Missing prompt file binding: {name}')
        if ref.get('type') not in ('extracted_original', 'generated', 'edited'):
            errors.append(f'Unknown reference type: {name}')
        if data.get('intent') == 'requested transformation' and ref.get('type') in ('generated', 'edited'):
            for field in ('source_frame', 'image_prompt_file'):
                asset = folder / ref.get(field, '')
                if asset.is_symlink() or not asset.resolve().is_relative_to(folder) or not asset.is_file():
                    errors.append(f'Missing {field} for {name}')
    if data.get('intent') == 'requested transformation' and not any(r.get('type') in ('generated', 'edited') for r in refs):
        errors.append('Transformation has no generated/edited references')
    return {'status': 'incomplete' if errors else 'reference_packet_consistent', 'errors': errors,
            'limitations': 'Checks file integrity and declared review/bindings only; does not verify visual quality, provider settings or generated video.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    try:
        result = check(args.folder)
        print(json.dumps(result, indent=2))
        raise SystemExit(bool(result['errors']))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Packet check failed: {error}\n')
