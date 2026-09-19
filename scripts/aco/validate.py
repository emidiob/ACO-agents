from __future__ import annotations
import json
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote
from pathlib import Path
from .common import ACOError, ROOT, VERSION, read_json
from .install import verify_release


def validate() -> dict:
    if not (ROOT/'catalog.json').exists():raise ACOError('Validate from the full ACO release checkout')
    cat=read_json(ROOT/'catalog.json')
    errors=[]
    names=set()
    for key,a in cat['agents'].items():
        for field in ('path','codex_path'):
            if not (ROOT/a[field]).is_file():errors.append('Missing '+a[field])
        data=tomllib.loads((ROOT/a['codex_path']).read_text())
        if data['name'] in names:errors.append('Duplicate native name '+data['name'])
        names.add(data['name'])
        if data['name']!='aco_'+key:errors.append('Invalid native name '+key)
        if not data.get('developer_instructions'):errors.append('Empty instructions '+key)
    skills=list((ROOT/'skills').glob('*/SKILL.md'))
    if len(skills)!=cat.get('skill_count'):errors.append('Skill count differs from catalogue')
    if sorted(p.parent.name for p in skills)!=cat.get('skills'):errors.append('Skill names differ from catalogue')
    if len(cat['agents'])!=cat.get('role_count'):errors.append('Role count differs from catalogue')
    for p in skills:
        text=p.read_text()
        if not text.startswith('---\n') or f'name: {p.parent.name}\n' not in text:
            errors.append('Invalid skill header '+str(p))
    for office,d in cat['offices'].items():
        for key in [d['lead'],*d['dependencies']]:
            if key not in cat['agents']:errors.append('Missing role dependency '+key)
    workflows=read_json(ROOT/'skills/aco-office-concierge/references/WORKFLOWS.json')['workflows']
    for key,w in workflows.items():
        if w['office'] not in cat['offices']:errors.append('Unknown workflow office '+key)
        for role in [w['lead'],*w['team']]:
            if role not in cat['agents']:errors.append('Unknown workflow role '+key+': '+role)
        if len({i['key'] for i in w['intake']})!=len(w['intake']):errors.append('Duplicate intake field '+key)
    # Check actual dangerous files, not intentional references in migration documentation.
    for name in ('plugin.json','.codex-plugin','.agents/plugins','docs/PUBLIC-SUBMISSION.md','PRIVACY.md','TERMS.md','MCP-ROADMAP.md'):
        if (ROOT/name).exists():errors.append('Obsolete plugin artifact '+name)
    private_components={'private-context','private-knowledge','.agent-context','credentials.json','token.json'}
    scanned=0
    secret_patterns=[re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
                     re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
                     re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{35,}\b'),
                     re.compile(r'\bAKIA[0-9A-Z]{16}\b')]
    for p in ROOT.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or '.git' in p.parts:continue
        rel=p.relative_to(ROOT)
        if p.is_symlink():errors.append('Symlink '+str(rel));continue
        if set(rel.parts)&private_components:errors.append('Private path '+str(rel))
        if p.suffix in {'.md','.json','.toml','.txt','.yaml','.yml','.py','.sh','.command'} or p.name in {'LICENSE','VERSION','.gitignore'}:
            text=p.read_text(encoding='utf-8');scanned+=1
            if any(pattern.search(text) for pattern in secret_patterns):errors.append('Potential secret pattern in '+str(rel))
            if re.search(r'https://(?:drive\.google\.com/(?:drive/folders|file/d)/|docs\.google\.com/(?:document|spreadsheets)/d/)[A-Za-z0-9_-]{20,}',text):
                errors.append('Real-looking private Drive ID in '+str(rel))
    links_checked=0
    for doc in ROOT.rglob('*.md'):
        if '.git' in doc.parts:continue
        text=re.sub(r'```.*?```','',doc.read_text(),flags=re.S)
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text):
            if '://' in target or target.startswith(('#','mailto:')):continue
            target=target.split('#')[0]
            if not target:continue
            links_checked+=1
            if not (doc.parent/unquote(target)).exists():errors.append('Broken relative link in '+str(doc.relative_to(ROOT))+': '+target)
    process=subprocess.run([sys.executable,str(ROOT/'scripts/generate.py'),'--check'],text=True,capture_output=True)
    if process.returncode:errors.append(process.stdout+process.stderr)
    verify_release()
    if errors:raise ACOError('Validation failed:\n'+'\n'.join(errors))
    return {'status':'validated','version':VERSION,'canonical_agents':len(cat['agents']),
            'native_agents':len(names),'skills':len(skills),'workflows':len(workflows),'text_files_scanned':scanned,'relative_links_checked':links_checked,
            'checks':['TOML','role catalogue and dependencies','generated parity','no plugin artifacts','basic secret/private-path scan','release hashes','relative documentation links'],
            'limitations':'Static/local checks; no professional-quality certification or live-host/Drive end-to-end test.'}
