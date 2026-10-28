#!/usr/bin/env python3
"""Report explicit parity gaps; fail closed while coverage is incomplete."""
import json
from pathlib import Path
from collections import Counter

def report():
    data=json.loads((Path(__file__).resolve().parents[1]/'references/feature-parity.json').read_text())
    counts=Counter(x['status'] for x in data['features'])
    complete=bool(data.get('inventory_complete')) and bool(data['features']) and all(x.get('parity_verified') is True for x in data['features'])
    return {'full_parity':complete,'inventory_complete':data.get('inventory_complete',False),'counts':dict(counts),
            'outstanding':[x for x in data['features'] if not x.get('parity_verified')],
            'scope':data['scope']}
if __name__=='__main__':
    result=report();print(json.dumps(result,indent=2));raise SystemExit(0 if result['full_parity'] else 1)
