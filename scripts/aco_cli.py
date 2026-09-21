#!/usr/bin/env python3
"""Entry point; run `python3 scripts/aco_cli.py --help`."""
import sys
if sys.version_info < (3, 11):
    sys.exit('ACO needs Python 3.11 or newer. Install it, then run this command again.')
from aco.cli import main
if __name__ == '__main__':
    main()
