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
    # Quality, Routing & Execution release checks (v0.7.0). These are local/read-only.
    contracts=read_json(ROOT/'config/role-contracts.json')
    if contracts.get('schema_version')!=1:errors.append('Role contracts schema mismatch')
    if contracts.get('aco_version')!=VERSION:errors.append('Role contracts version mismatch')
    if set(contracts.get('roles',{}))!=set(cat['agents']):errors.append('Role contracts do not cover canonical catalogue')
    hints=read_json(ROOT/'config/routing-hints.json')
    if hints.get('schema_version')!=1:errors.append('Routing hints schema mismatch')
    if hints.get('aco_version')!=VERSION:errors.append('Routing hints version mismatch')
    examples=read_json(ROOT/'config/routing-examples.json')
    if examples.get('schema_version')!=1:errors.append('Routing examples schema mismatch')
    if examples.get('aco_version')!=VERSION:errors.append('Routing examples version mismatch')
    if not examples.get('examples'):errors.append('Routing examples are empty')
    if 'routing-final-holdout.json' in set(examples.get('source_files',[])):errors.append('Final routing holdout listed as training source')
    holdout=read_json(ROOT/'config/routing-final-holdout.json')
    if holdout.get('schema_version')!=1:errors.append('Final routing holdout schema mismatch')
    if holdout.get('aco_version')!=VERSION:errors.append('Final routing holdout version mismatch')
    if not holdout.get('cases'):errors.append('Final routing holdout is empty')
    trained_prompts={x.get('prompt') for x in examples.get('examples',[]) if x.get('prompt')}
    holdout_prompts={x.get('prompt') for x in holdout.get('cases',[]) if x.get('prompt')}
    if trained_prompts & holdout_prompts:errors.append('Final routing holdout overlaps training examples')
    simulation=read_json(ROOT/'release/behavioral-simulation.json')
    if simulation.get('schema_version')!=1:errors.append('Behavioral simulation schema mismatch')
    if simulation.get('aco_version')!=VERSION:errors.append('Behavioral simulation version mismatch')
    if not simulation.get('cases'):errors.append('Behavioral simulation is empty')
    from .routing import route_benchmark
    routing_gate=route_benchmark(ROOT/'config/routing-final-holdout.json')
    if routing_gate.get('status')!='passed' or routing_gate.get('critical_failures')!=0 or routing_gate.get('score',0)<90:
        errors.append('Final routing holdout gate failed')
    from .quality import score_simulation
    simulation_gate=score_simulation(ROOT/'release/behavioral-simulation.json')
    if simulation_gate.get('status')!='passed' or simulation_gate.get('critical_failures')!=0 or simulation_gate.get('score',0)<90:
        errors.append('Behavioral simulation gate failed')
    # v0.7 execution contracts and deterministic conformance gate.
    for filename in ('capabilities.json','permission-policy.json','adapter-contract.json','workflow-states.json','execution-benchmark.json'):
        cfg=read_json(ROOT/'config'/filename)
        if cfg.get('schema_version')!=1:errors.append(filename+' schema mismatch')
        if cfg.get('aco_version')!=VERSION:errors.append(filename+' version mismatch')
    capability_cfg=read_json(ROOT/'config/capabilities.json')
    required_states={'LEARNED_SKILL','REFERENCE','OPTIONAL_TOOL','CONNECTED_INTEGRATION','LOCAL_RUNTIME','UNAVAILABLE','BLOCKED'}
    if not required_states.issubset(set(capability_cfg.get('states',[]))):errors.append('Capability resource states incomplete')
    from .execution import execution_benchmark
    execution_gate=execution_benchmark(ROOT/'config/execution-benchmark.json')
    if execution_gate.get('status')!='passed' or execution_gate.get('critical_failures')!=0 or execution_gate.get('score',0)<98:
        errors.append('Execution policy benchmark gate failed')
    from .resources import load_registry
    rr=load_registry();resource_ids=[x['id'] for x in rr['resources']]
    if len(resource_ids)!=len(set(resource_ids)):errors.append('Duplicate resource IDs')
    if rr.get('aco_version')!=VERSION:errors.append('Resource registry version mismatch')
    for entry in rr['resources']:
        for role in entry['roles']:
            if role not in cat['agents']:errors.append('Unknown resource role '+role)
        method=ROOT/'skills/aco-office-concierge/references/resources'/entry['method']
        if not method.exists():errors.append('Missing resource method '+entry['id'])
        if entry['review_status']=='identity_unresolved' and entry.get('activation')!='blocked_pending_exact_source':errors.append('Unresolved resource not gated '+entry['id'])
        if entry.get('installed_by_aco') or entry.get('execution_tested'):errors.append('Unverified installation/test claim in supplied-resource registry '+entry['id'])
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
            'native_agents':len(names),'skills':len(skills),'workflows':len(workflows),'optional_resources':len(resource_ids),'memory_default':'compact','text_files_scanned':scanned,'relative_links_checked':links_checked,
            'checks':['TOML','role catalogue and dependencies','generated parity','no plugin artifacts','basic secret/private-path scan','release hashes','relative documentation links','resource identities/roles/methods','role contracts','routing holdout gate','behavioral simulation gate','capability/permission/adapter/workflow contracts','execution policy benchmark gate'],
            'execution_benchmark_score':execution_gate.get('score'),'limitations':'Static/local checks; no professional-quality certification and no live external adapter/provider action is executed by validation.'}
