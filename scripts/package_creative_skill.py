#!/usr/bin/env python3
"""Package a canonical creative skill with its portable resources."""
import argparse
import json
from pathlib import Path
from package_motion_skill import package

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skill', required=True, choices=['aco-capture', 'aco-image', 'aco-video', 'aco-genjutsu', 'aco-motion', 'aco-webdesign'])
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    try:
        print(json.dumps(package(a.output, a.skill), indent=2))
    except (OSError, ValueError) as error:
        p.exit(1, str(error) + '\n')
