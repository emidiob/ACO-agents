#!/usr/bin/env python3
"""ACO's independent BM25 search over explicitly supplied external CSV datasets.

Never executes snippets or downloads data. Scores are relevance, not quality/confidence.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import re

STOP = {'a','an','the','and','or','for','of','to','in','with','is','on','by'}
def tokens(text):
    return [x for x in re.findall(r'[^\W_]+', text.casefold(), re.UNICODE) if x not in STOP]

class Catalog:
    def __init__(self, root):
        self.root = Path(root).resolve(strict=True)
        self.files = {}
        self.source = None
        manifest = self.root / 'aco-source.json'
        if manifest.exists():
            self.source = json.loads(manifest.read_text())
        for path in sorted(self.root.rglob('*.csv')):
            if path.is_symlink() or not path.resolve().is_relative_to(self.root):
                raise ValueError('Dataset symlink is not allowed: ' + str(path))
            domain = path.relative_to(self.root).with_suffix('').as_posix()
            self.files[domain] = path
        if not self.files:
            raise ValueError('No CSV datasets found')

    def rows(self, domain):
        if domain not in self.files:
            raise ValueError('Unknown domain: ' + domain)
        path = self.files[domain]
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        verified = False
        if self.source:
            entry = next((x for x in self.source.get('files',[]) if x['path'] == path.relative_to(self.root).as_posix()), None)
            if entry:
                if entry['sha256'] != digest:
                    raise ValueError('Dataset checksum mismatch: ' + domain)
                verified = True
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ValueError('Invalid CSV header: ' + domain)
            rows = list(reader)
        if any(None in r or any(v is None for v in r.values()) for r in rows):
            raise ValueError('Malformed CSV row: ' + domain)
        return rows, {'domain':domain,'sha256':digest,'manifest_verified':verified,
                      'repository':(self.source or {}).get('repository'),
                      'revision':(self.source or {}).get('revision')}

    def search(self, query, domain, limit=5):
        if limit < 1 or limit > 100:
            raise ValueError('limit must be between 1 and 100')
        rows, source = self.rows(domain)
        q = set(tokens(query))
        docs = [Counter(tokens(' '.join(r.values()))) for r in rows]
        lengths = [sum(d.values()) for d in docs]
        average = sum(lengths)/len(docs) if docs else 1
        average = average or 1
        df = {term:sum(term in doc for doc in docs) for term in q}
        matches=[]
        for index, (row, doc, size) in enumerate(zip(rows,docs,lengths)):
            score=0
            for term in q:
                freq=doc[term]
                if freq:
                    idf=math.log(1+(len(docs)-df[term]+0.5)/(df[term]+0.5))
                    score += idf*(freq*2.2)/(freq+1.2*(0.25+0.75*size/average))
            if score:
                matches.append({'row':index+2,'score':round(score,6),'matched_terms':sorted(q & doc.keys()),'values':row})
        matches.sort(key=lambda r:(-r['score'],r['row']))
        return {'query':query,'status':'matched' if matches else 'no_match','algorithm':'ACO BM25 k1=1.2 b=0.75',
                'source':source,'results':matches[:limit],'total_matches':len(matches)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',required=True,type=Path)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('domains')
    s=sub.add_parser('search');s.add_argument('query');s.add_argument('--domain',required=True);s.add_argument('--limit',type=int,default=5)
    args=p.parse_args()
    try:
        c=Catalog(args.data)
        out={'domains':sorted(c.files)} if args.command=='domains' else c.search(args.query,args.domain,args.limit)
        print(json.dumps(out,indent=2,ensure_ascii=False))
    except (OSError,ValueError,csv.Error) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
