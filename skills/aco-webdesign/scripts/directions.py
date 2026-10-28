#!/usr/bin/env python3
"""Search original ACO recipes with transparent keyword matches, not quality scores."""
import argparse
import json
from pathlib import Path
import re

def search(query):
    words = set(re.findall(r'[\w]+', query.lower()))
    recipes = json.loads((Path(__file__).resolve().parents[1]/'assets/directions.json').read_text())
    matches = []
    for recipe in recipes:
        matched = sorted(words & (set(recipe['tags']) | set(recipe['id'].split('-'))))
        if matched: matches.append(dict(recipe, matched_keywords=matched))
    matches.sort(key=lambda x: (-len(x['matched_keywords']), x['id']))
    return {'status': 'matched' if matches else 'no_keyword_match', 'query': query,
            'method': 'exact keyword matching; no aesthetic or outcome score', 'directions': matches}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--query', required=True)
    print(json.dumps(search(p.parse_args().query), indent=2))
