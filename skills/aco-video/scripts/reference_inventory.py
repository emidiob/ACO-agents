#!/usr/bin/env python3
"""Record real reference files without claiming visual inspection or provider upload."""
import argparse
import hashlib
import json
from pathlib import Path

def inventory(files, output):
    output = Path(output).expanduser().absolute()
    if output.exists() or any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError('Output exists or uses a symlink; choose a new file')
    entries = []
    seen = set()
    for value in files:
        path = Path(value).expanduser().resolve(strict=True)
        if not path.is_file():
            raise ValueError('Not a file: ' + str(path))
        if path in seen:
            raise ValueError('Duplicate reference: ' + str(path))
        seen.add(path)
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        entries.append({'file': str(path), 'sha256': digest.hexdigest(),
                        'bytes': path.stat().st_size, 'purpose': None,
                        'visually_reviewed': False, 'audio_listened': False,
                        'provider_binding': None})
    if not entries:
        raise ValueError('At least one reference is required')
    result = {'status': 'inventory_only', 'references': entries}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        inventory(args.files, args.output)
        print('Reference inventory saved; visual review and provider bindings remain unresolved.')
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')
