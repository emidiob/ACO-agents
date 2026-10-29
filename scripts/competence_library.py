#!/usr/bin/env python3
"""Source-checkout entry point; canonical executable ships inside the Concierge."""
import runpy
from pathlib import Path
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1]/'skills/aco-office-concierge/scripts/competence_library.py'), run_name='__main__')
