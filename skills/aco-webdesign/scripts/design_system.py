#!/usr/bin/env python3
"""Generate evidence-linked design proposals using ACO search and external data."""
import argparse
import json
from pathlib import Path
import re
from design_data import Catalog

DOMAINS=('products','ui-reasoning','styles','colors','typography','landing','charts','motion','ux-guidelines')

def generate(catalog, brief, stack=None, overrides=None):
    if not brief.strip():raise ValueError('A non-empty brief is required')
    selections={}
    product=catalog.search(brief,'products',1) if 'products' in catalog.files else None
    product_values=product['results'][0]['values'] if product and product['results'] else {}
    hints={'styles':product_values.get('Primary Style Recommendation',''),
           'landing':product_values.get('Landing Page Pattern',''),
           'colors':product_values.get('Product Type','')}
    for domain in DOMAINS:
        if domain in catalog.files:
            selections[domain]=catalog.search(brief+' '+hints.get(domain,''),domain,3)
    if stack:
        selections['stack']=catalog.search(brief,'stacks/'+stack,5)
    palette=selections.get('colors',{}).get('results',[])
    colors={}
    if palette:
        for key,value in palette[0]['values'].items():
            if re.fullmatch(r'#[0-9a-fA-F]{6}',value):
                colors[re.sub('[^a-z0-9]+','-',key.lower()).strip('-')]=value
    if overrides is not None and not isinstance(overrides,dict):raise ValueError('Color overrides must be an object')
    for key,value in (overrides or {}).items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*',key) or not re.fullmatch(r'#[0-9a-fA-F]{6}',value):
            raise ValueError('Color overrides must be semantic names and six-digit hex colors')
        colors[key]=value
    return {'schema':1,'status':'proposal','engine':'ACO independent search-based synthesis',
            'brief':brief,'stack':stack,'selections':selections,'color_tokens':colors,
            'user_overrides':overrides or {},'browser_verified':False,
            'limitations':['Ranked recommendations require design judgment.','Upstream conditional reasoning DSL is not executed.','Palette contrast and font licenses require project-specific verification.']}

def persist(result, output):
    output=Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink() or any(p.is_symlink() for p in output.parents):
        raise ValueError('Output must be a new directory without symlink ancestors')
    if not output.parent.is_dir():raise ValueError('Output parent must exist')
    output.mkdir()
    (output/'design-system.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    css=':root {\n'+''.join(f'  --{k}: {v};\n' for k,v in result['color_tokens'].items())+'}\n'
    (output/'tokens.css').write_text(css)
    return output

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('brief');p.add_argument('--data',type=Path,required=True);p.add_argument('--stack');p.add_argument('--overrides',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        overrides=json.loads(a.overrides.read_text()) if a.overrides else None
        result=generate(Catalog(a.data),a.brief,a.stack,overrides)
        if a.output: persist(result,a.output)
        print(json.dumps(result,indent=2,ensure_ascii=False))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
