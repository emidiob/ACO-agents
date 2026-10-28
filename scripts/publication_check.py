#!/usr/bin/env python3
"""Reject internal working documents from public ACO distributions."""
import argparse
import fnmatch
import json
from pathlib import Path

PATTERNS=('research/*','ACO-TEST-REPORT-*','docs/TEST-REPORT-*','docs/SKILL-VALIDATION-*',
 'docs/PRODUCT-DECISIONS.md','docs/*-PARITY.md','docs/*-VERIFICATION.md',
 'docs/SPECIALIST-GAP-ANALYSIS.md','docs/RESOURCE-REVIEW-NOTES.md','docs/RESOURCE-SELECTION.json',
 'docs/SOURCE-REVIEW.md','*/research-snapshot.json','*/feature-parity.json','*/component-inventory.json',
 'release/test-summary.json','release/verification.json','release/skill-evidence-*.json')

def check(root):
    root=Path(root);findings=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if any(x in ('.git','__pycache__','.venv','node_modules') for x in rel.parts):continue
        if p.is_file() and any(fnmatch.fnmatchcase(rel.as_posix(),pattern) for pattern in PATTERNS):
            findings.append(rel.as_posix())
    return {'status':'passed' if not findings else 'failed','internal_documents':sorted(findings)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();result=check(a.root);print(json.dumps(result,indent=2));raise SystemExit(bool(result['internal_documents']))
