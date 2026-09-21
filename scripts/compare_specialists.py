#!/usr/bin/env python3
"""Reproducible lexical catalogue comparison. Not an agent performance benchmark.
Uses the shipped, explicitly scoped source inventory. Does not call an LLM/network.
"""
from __future__ import annotations
import argparse, collections, hashlib, html, json, math, re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
STOP=set('a an and the for of to in on with as by from role roles agent agents office specialist specialists director manager engineer expert use generic tools current framework workflows workflow development developer analyst assistant coordinator lead senior junior method methods system systems'.split())
ALIASES={'ui':'interface visual design','ux':'experience usability','qa':'testing verification','qc':'quality verification','cro':'conversion experiment','seo':'search discoverability','cms':'content publishing','i2v':'image video','gl':'ledger reconciliation','tdd':'test regression','llm':'model evaluation','comfyui':'graph nodes generation','figma':'design interface components','typographic':'typography','color':'colour','test':'testing','tests':'testing'}

def tokens(value):
    words=re.findall(r'[a-z][a-z0-9]+',value.lower().replace('_',' ').replace('-',' '))
    expanded=[]
    for w in words:expanded.extend(ALIASES.get(w,w).split())
    return [w for w in expanded if w not in STOP]

def vector(words,idf):
    count=collections.Counter(words)
    v={k:(1+math.log(n))*idf.get(k,1) for k,n in count.items()}
    norm=math.sqrt(sum(x*x for x in v.values())) or 1
    return {k:x/norm for k,x in v.items()}

def similarity(a,b):return sum(v*b.get(k,0) for k,v in a.items())

def compare(source_path,baseline_path,decisions_path):
    sources=json.loads(source_path.read_text())['sources']
    base=json.loads(baseline_path.read_text())
    roles=base['roles'];decisions=json.loads(decisions_path.read_text())['decisions'];dm={x['key']:x for x in decisions}
    docs=[tokens(x['key']+' '+x['description']) for x in roles]
    docs += [tokens(i) for s in sources for i in s['observed_items']]
    freq=collections.Counter(k for t in docs for k in set(t));n=len(docs)
    idf={k:1+math.log((n+1)/(f+1)) for k,f in freq.items()}
    pair_rows=[];role_rows=[]
    for role in roles:
        rv=vector(tokens(role['key']+' '+role['description']),idf);rank=[]
        for source in sources:
            candidates=[]
            for item in source['observed_items']:
                iv=vector(tokens(item),idf);score=similarity(rv,iv)
                candidates.append({'item':item,'lexical_relatedness':round(score,6)})
            candidates.sort(key=lambda x:(-x['lexical_relatedness'],x['item']))
            best=candidates[:3]
            row={'role':role['key'],'office':role['office'],'source_id':source['id'],
                 'score_kind':'token_cosine_relatedness_not_proficiency','lexical_relatedness':best[0]['lexical_relatedness'] if best else 0,
                 'candidate_items':best,'inventory_coverage':source['coverage']}
            pair_rows.append(row);rank.append(row)
        rank.sort(key=lambda x:(-x['lexical_relatedness'],x['source_id']))
        d=dm.get(role['key'])
        role_rows.append({'role':role['key'],'office':role['office'],'description':role['description'],
                          'baseline_path':role['path'],'baseline_sha256':role['sha256'],
                          'decision':d['action'] if d else 'retained_not_domain_benchmarked',
                          'decision_basis':'curated implementation review' if d else 'no targeted change in this design/web/video-focused pass',
                          'playbook':d.get('playbook') if d else None,'source_ids_for_decision':d.get('sources',[]) if d else [],
                          'top_catalogue_matches':[{k:v for k,v in r.items() if k in ('source_id','lexical_relatedness','candidate_items')} for r in rank[:3]]})
    # Duplicate candidates are explicit review suggestions; no merge is automated.
    vectors={r['key']:vector(tokens(r['key']+' '+r['description']),idf) for r in roles};dups=[]
    for i,a in enumerate(roles):
        for b in roles[i+1:]:
            s=similarity(vectors[a['key']],vectors[b['key']])
            if s>=0.50:dups.append({'a':a['key'],'b':b['key'],'lexical_relatedness':round(s,6),'action':'review_boundaries_only_no_automatic_merge'})
    dups.sort(key=lambda x:(-x['lexical_relatedness'],x['a'],x['b']))
    counts=dict(collections.Counter(x['decision'] for x in role_rows))
    result={'schema_version':1,'baseline':base['version'],'target':'0.5.0','source_count':len(sources),'observed_source_items':sum(len(s['observed_items']) for s in sources),
            'baseline_roles':len(roles),'role_repository_comparisons':len(pair_rows),'decisions':counts,
            'new_roles':[d for d in decisions if d['action']=='add_distinct_role'],
            'limitations':['Source catalogue extraction is curated and explicitly scoped, not a recursive audit of every external file.',
                           'All baseline roles are compared with all selected source inventories; lexical relatedness is for discovery, not expertise scoring.',
                           'Targeted changes were reviewed; unchanged domains are not certified strong or complete.',
                           'No paired model-output or paid image/video generation benchmark was run.'],
            'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source_path,baseline_path,decisions_path)},
            'roles':role_rows,'duplicate_candidates':dups[:25],'pairs':pair_rows}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=R/'research/specialist-upgrade');a=p.parse_args()
    src=R/'research/specialist-upgrade';result=compare(src/'sources.json',src/'baseline-roles.json',src/'decisions.json')
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'comparison.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    rows=[]
    for r in result['roles']:
        matches='; '.join(x['source_id']+' '+x['candidate_items'][0]['item'] for x in r['top_catalogue_matches'] if x['lexical_relatedness']>0)
        rows.append(f'<tr><td>{html.escape(r["role"])}</td><td>{html.escape(r["office"])}</td><td>{html.escape(r["decision"])}</td><td>{html.escape(matches)}</td></tr>')
    sources=json.loads((src/'sources.json').read_text())['sources']
    source_rows=''.join(f'<li><b>{s["id"]}</b> — <a href="{html.escape(s["url"],quote=True)}">{html.escape(s["repository"])}</a><p>{html.escape(s["coverage"])}<br>{html.escape(s["license_observation"])}</p></li>' for s in sources)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ACO specialist comparison</title><style>body{font:16px/1.55 system-ui,sans-serif;max-width:1250px;margin:40px auto;padding:0 24px;color:#19232a;background:#f9faf8}h1{font-size:clamp(30px,5vw,55px);line-height:1.1}input{font:inherit;padding:12px;width:min(600px,90%);border:1px solid;border-radius:4px}table{border-collapse:collapse;width:100%;margin-top:24px}td,th{padding:10px;text-align:left;border-bottom:1px solid #ccd2d4;vertical-align:top}th{background:#edf1ed;position:sticky;top:0}td:first-child{font-family:monospace;overflow-wrap:anywhere}.scroll{overflow:auto}small,p{max-width:900px}a{color:#135c59}:focus-visible{outline:3px solid #a04500;outline-offset:3px}</style><h1>ACO<br>Specialist gap analysis</h1>'''
    page+=f'<p><b>{result["baseline_roles"]} ACO roles × {result["source_count"]} repositories = {result["role_repository_comparisons"]:,} catalogue comparisons.</b> {result["observed_source_items"]} observed catalogue entries/topics; {len(result["new_roles"])} distinct roles added.</p>'
    page+='<p>This is a traceable catalogue comparison, not a ranking of AI output quality. Source extraction is curated; matching is automatic. Unchanged roles are retained, not declared fully evaluated. No private knowledge or external tracking is included.</p><label for="q">Filter by role, office, decision or source</label><br><input id="q" type="search" placeholder="e.g. video, design, deepen_existing"><p id="count" aria-live="polite"></p><div class="scroll"><table><thead><tr><th>ACO role</th><th>Office</th><th>Reviewed decision</th><th>Lexical source candidates (not quality scores)</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><h2>Inspected sources</h2><ol>'+source_rows+'</ol><script>const q=document.getElementById("q"),rows=[...document.querySelectorAll("tbody tr")],count=document.getElementById("count");function update(){const s=q.value.toLowerCase();let n=0;for(const r of rows){r.hidden=!r.textContent.toLowerCase().includes(s);if(!r.hidden)n++}count.textContent=n+" of "+rows.length+" baseline roles shown"}q.addEventListener("input",update);update();</script></html>'
    (a.out/'comparison.html').write_text(page)
    print(json.dumps({k:v for k,v in result.items() if k not in ('roles','pairs','duplicate_candidates','new_roles','limitations','input_hashes')},indent=2))
if __name__=='__main__':main()
