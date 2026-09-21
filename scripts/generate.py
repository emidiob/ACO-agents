#!/usr/bin/env python3
"""Generate Codex TOMLs, catalogue, template mirrors and minimal installed runtime.
Canonical role methods live only under skills/*/references/agents/*.md.
"""
from __future__ import annotations
import argparse
import os
import json
import re
import sys
from urllib.parse import unquote
from pathlib import Path
R = Path(__file__).resolve().parents[1]


def encoded(v):
    return json.dumps(v, ensure_ascii=False)


def native_references(instructions, canonical_path, version):
    """Resolve source-relative Markdown links to portable paths under a skills root.

    A TOML lives outside the canonical role directory. Copying ../ references
    unchanged silently points at the wrong files in ~/.codex/agents.
    """
    role_dir = (R / canonical_path).parent
    def replace_link(match):
        target = match.group(2)
        if '://' in target or target.startswith(('#', 'mailto:')):
            return match.group(0)
        part, sep, fragment = target.partition('#')
        resolved = (role_dir / unquote(part)).resolve()
        if resolved.is_relative_to(R / 'skills'):
            if not resolved.exists():
                raise ValueError('Missing canonical method link: ' + canonical_path + ': ' + target)
            portable = resolved.relative_to(R / 'skills').as_posix()
            return '[' + match.group(1) + '](' + portable + (sep + fragment if sep else '') + ')'
        return match.group(0)
    converted = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', replace_link, instructions)
    header = (
        'NATIVE PROFILE REFERENCE RESOLUTION\n'
        'ACO version: ' + version + '. Canonical source: ' + canonical_path + '.\n'
        'Links beginning aco- in this profile are relative to the SELECTED skills root, '
        'not to this TOML or the current work directory. Locate the matching project '
        '.agents/skills or user ~/.agents/skills installation; in the source checkout '
        'use its skills/ directory. Resolve those links under that root and verify '
        'the actual file/version before reading. Do not silently mix installations. '
        'If the source is unavailable, report it rather than inventing a loaded method.\n\n'
    )
    return header + converted


def md_section(text, prefix):
    m = re.search(r'^## ' + re.escape(prefix) + r'.*?\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''


def outputs():
    roles = {}
    for p in sorted((R/'skills').glob('*/references/agents/*.md')):
        t = p.read_text()
        key = re.search(r'\*\*Agent key:\*\* `([^`]+)`', t).group(1)
        office = re.search(r'\*\*Office:\*\* `([^`]+)`', t).group(1)
        description = re.search(r'\*\*Description:\*\* (.*)', t).group(1)
        if key in roles:
            raise ValueError('Duplicate canonical agent key: ' + key)
        roles[key] = {'office': office, 'description': description,
                      'path': p.relative_to(R).as_posix(),
                      'skill_path': p.relative_to(R/'skills').as_posix(),
                      'native_name': 'aco_' + key,
                      'codex_path': f'extras/codex-custom-agents/{office}/aco-{key.replace("_","-")}.toml',
                      'instructions': t.split('## Instructions\n',1)[1].strip()}
    office_spec=json.loads((R/'config/offices.json').read_text())['offices']
    leads={k:v['lead'] for k,v in office_spec.items()}
    dependencies={k:v.get('dependencies',[]) for k,v in office_spec.items()}
    skill_names=sorted(p.parent.name for p in (R/'skills').glob('*/SKILL.md'))
    for dep in sum(dependencies.values(), []):
        if dep not in roles:raise ValueError('Missing dependency: '+dep)
    cat = {'schema_version':1, 'aco_version':(R/'VERSION').read_text().strip(),
           'skill_count':len(skill_names), 'role_count':len(roles), 'skills':skill_names,
           'offices':{o:{'lead':l,'dependencies':dependencies.get(o,[]),
                         'count':sum(a['office']==o for a in roles.values())} for o,l in leads.items()},
           'agents':{k:{f:v for f,v in d.items() if f!='instructions'} for k,d in roles.items()}}
    routing_hints=json.loads((R/'config/routing-hints.json').read_text())
    if routing_hints.get('aco_version') != cat['aco_version']:
        raise ValueError('Routing-hints version mismatch')
    role_contracts={'schema_version':1,'aco_version':cat['aco_version'],'roles':{}}
    for key,d in roles.items():
        source=(R/d['path']).read_text()
        hints=routing_hints.get('role_hints',{}).get(key,[])
        role_contracts['roles'][key]={
            'office':d['office'],
            'purpose':d['description'],
            'use_when':hints or [d['description']],
            'avoid_when':['The task is outside this role boundary or another specialist has a materially more specific mandate.'],
            'inputs':md_section(source,'Intake'),
            'method':md_section(source,'Method'),
            'outputs':md_section(source,'Deliverables'),
            'verification':md_section(source,'Acceptance and evidence'),
            'escalation':md_section(source,'Escalation'),
            'source_path':d['path']
        }
    out = {'catalog.json':(json.dumps(cat,indent=2,ensure_ascii=False)+'\n').encode(),
           'skills/aco-office-concierge/references/CATALOG.json':(json.dumps(cat,indent=2,ensure_ascii=False)+'\n').encode(),
           'config/role-contracts.json':(json.dumps(role_contracts,indent=2,ensure_ascii=False)+'\n').encode()}
    pattern = re.compile(r'(?<![\w])('+'|'.join(sorted(map(re.escape,roles),key=len,reverse=True))+r')(?![\w])')
    for key,d in roles.items():
        instructions = pattern.sub(lambda m:'aco_'+m.group(1),d['instructions'])
        instructions = native_references(instructions, d['path'], cat['aco_version'])
        out[d['codex_path']] = (f'name = {encoded(d["native_name"])}\n'
                               f'description = {encoded(d["description"])}\n'
                               f'developer_instructions = {encoded(instructions)}\n').encode()
    for p in (R/'assets/context-templates').glob('*.md'):
        out['skills/aco-context-setup/references/templates/'+p.name]=p.read_bytes()
    # A small runtime accompanies the native skill; not a duplicated canonical role collection.
    base='skills/aco-office-concierge/runtime/'
    out[base+'VERSION']=(R/'VERSION').read_bytes()
    out[base+'RUNTIME-ONLY']=b'Local compact knowledge, optional resource selection and checks only. Use the full source release for install, migrate and validate. Legacy event storage is explicit opt-in.\n'
    for name in ('aco_cli.py','aco/__init__.py','aco/common.py','aco/memory.py','aco/drive.py','aco/cli.py','aco/planning.py','aco/production.py','aco/finance.py','aco/specialist.py','aco/compact.py','aco/resources.py','aco/tidy.py','aco/canonical_sync.py','aco/readiness.py','aco/harness.py','aco/routing.py','aco/quality.py','aco/execution.py'):
        out[base+'scripts/'+name]=(R/'scripts'/name).read_bytes()
    for p in (R/'assets/context-templates').glob('*.md'):
        out[base+'assets/context-templates/'+p.name]=p.read_bytes()
    out[base+'config/workflows.json']=(R/'skills/aco-office-concierge/references/WORKFLOWS.json').read_bytes()
    resources_path=R/'skills/aco-office-concierge/references/resources/REGISTRY.json'
    resources=json.loads(resources_path.read_text())
    out[base+'config/resources.json']=resources_path.read_bytes()
    out[base+'config/evals.json']=(R/'config/evals.json').read_bytes()
    out[base+'config/routing-hints.json']=(R/'config/routing-hints.json').read_bytes()
    out[base+'config/routing-benchmark.json']=(R/'config/routing-benchmark.json').read_bytes()
    out[base+'config/routing-examples.json']=(R/'config/routing-examples.json').read_bytes()
    out[base+'config/routing-final-holdout.json']=(R/'config/routing-final-holdout.json').read_bytes()
    out[base+'config/role-contracts.json']=out['config/role-contracts.json']
    for name in ('capabilities.json','permission-policy.json','adapter-contract.json','workflow-states.json','execution-benchmark.json'):
        out[base+'config/'+name]=(R/'config'/name).read_bytes()
    # One canonical JSON; generated compact browsing cards avoid loading all entries.
    rbase='skills/aco-office-concierge/references/resources/'
    overview=['# Optional ACO resources','',f'Version {cat["aco_version"]}; {len(resources["resources"])} deduplicated resources. NOT installed, connected or blanket-approved.','',
              'Use only relevant entries. Read the selected category card and original ACO method before use. Source review is not execution, security audit or license clearance. No upstream code/assets/models/fonts are bundled. Three ambiguous names stay gated.','',
              '| Resource | Type | Review | Category card |','|---|---|---|---|']
    cats=sorted({e['category'] for e in resources['resources']})
    for e in resources['resources']:
        overview.append(f'| {e["name"]} | {e["type"]} | {e["review_status"]} | [{e["category"]}](CATEGORY-{e["category"]}.md#{e["id"]}) |')
    for c in cats:
        lines=['# '+c.title()+' resources','', 'Optional catalogue, not an installation list. Consult current source and actual host capabilities.','']
        for e in resources['resources']:
            if e['category']!=c:continue
            lines += ['## '+e['id'],'', '**'+e['name']+'** · '+e['type']+' · '+e['review_status']+' · reviewed '+e['review_date'],'',
                      'Source: '+(e['source_url'] or 'Unresolved; exact link required.')+'',
                      '', '**Use:** '+e['use_when'],'', '**Avoid:** '+e['avoid_when'],'', '**Checks:** '+e['notes'], '',
                      'Roles: '+', '.join('`'+x+'`' for x in e['roles'])+'.', '',
                      'Required capabilities when executing: '+(', '.join(e['requirements']) or 'none declared; inspect the actual task/tool')+'.', '',
                      '[Original ACO method]('+e['method']+'). External upstream content is not bundled. No execution tests performed.','']
            if e.get('candidates'):lines+=['Unconfirmed candidates: '+', '.join(e['candidates'])+'. Obtain the exact intended source; do not auto-select.','']
        out[rbase+'CATEGORY-'+c+'.md']='\n'.join(lines).encode()
    overview += ['', '[Complete policy](../../../../docs/RESOURCE-REGISTRY.md) in the source release. In an installed skill, use the linked methods and protocols instead of expecting full documentation locally.']
    # Avoid linking outside installed skills while preserving full-source relative-link validation.
    overview[-1]='Read the relevant original method and `../protocols/COMPACT-MEMORY.md` before storing references; one bookmark must not create a Drive file.'
    out[rbase+'INDEX.md']='\n'.join(overview).encode()

    # Human index is generated, too: every role has a concrete canonical link.
    lines=['# ACO catalogue','',f'Version {cat["aco_version"]}. {len(roles)} generic role definitions; not {len(roles)} autonomous running processes.','',
           'Start with [CHATGPT.md](CHATGPT.md) or [AGENTS.md](AGENTS.md). Read only relevant skills and role methods.','']
    for office,meta in cat['offices'].items():
        lines += ['## '+office, '',f'Lead: `{meta["lead"]}`. Native agents use the `aco_` prefix.','']
        for k,d in roles.items():
            if d['office']==office:
                lines += [f'- [`{k}`]({d["path"]}) — {d["description"]}']
        if meta['dependencies']:lines += ['', 'Reused dependencies: '+', '.join('`'+x+'`' for x in meta['dependencies'])]
        lines += ['']
    # The full catalogue is available for inspection, but is not the startup payload.
    out['docs/ALL-ROLES.md']='\n'.join(lines).replace('](skills/','](../skills/').replace('](CHATGPT.md)','](../CHATGPT.md)').replace('](AGENTS.md)','](../AGENTS.md)').encode()
    short=['# ACO — routing index','',f'Version {cat["aco_version"]}; {len(roles)} role definitions and {len(skill_names)} skills. These are not permanently running agents.','',
           'Use skills/aco-office-concierge/references/protocols/CONTEXT-RETRIEVAL.md for progressive context, EXECUTION.md before consequential external actions, VERIFICATION.md before completion claims, and COMPACT-MEMORY.md before persistent writes. Optional resource selection starts at skills/aco-office-concierge/references/resources/INDEX.md. Select an office below, then read its local ROLE-INDEX and only selected methods. Do not load the full catalogue by default.','']
    for office,meta in cat['offices'].items():
        skill='aco-office-concierge' if office=='shared' else 'aco-'+office
        dest=f'skills/{skill}/references/ROLE-INDEX.md'
        office_lines=['# '+office+' — role index','',f'Lead: `{meta["lead"]}`. Read only selected role instructions; native names use `aco_`.','']
        keys=[k for k,d in roles.items() if d['office']==office]+meta['dependencies']
        for k in keys:
            d=roles[k]
            relative=os.path.relpath(d['path'],str(Path(dest).parent))
            office_lines += [f'- [`{k}`]({relative}) — {d["description"]}']
        if office!='shared':
            office_lines += ['', 'Shared methods: [shared role index](../../aco-office-concierge/references/ROLE-INDEX.md).']
        out[dest]='\n'.join(office_lines).encode()
        short += [f'- **{office}** ({meta["count"]}): [start](skills/{skill}/SKILL.md) · [roles]({dest})']
    short += ['', '- **Context setup**: [start](skills/aco-context-setup/SKILL.md).',
              '- **Context steward**: [start](skills/aco-context-steward/SKILL.md).','',
              'Optional: [visual agent catalogue](docs/AGENT-CATALOG.md) · [all roles with descriptions](docs/ALL-ROLES.md); `catalog.json` is the machine-readable path/dependency registry, not the default conversational context.']
    out['ACO-INDEX.md']='\n'.join(short).encode()
    # Generated visual catalogue: no manually maintained duplicate list.
    icons={'artist-office':'🎨','organization-office':'🏛️','agency-office':'🎯','product-office':'💻','legal-office':'⚖️','recruitment-office':'💼','shared':'🧭','finance-office':'💰','commercial-office':'📈','people-office':'👥','delivery-office':'📋','administration-office':'🗂️','production-office':'🎬','publishing-office':'📚'}
    visual=['# ACO — visual agent catalogue','',f'Version {cat["aco_version"]} · {len(roles)} canonical roles · {len(skill_names)} entry-point skills.','', 'Roles are reusable methods, not constantly running employees. Usually brief the Concierge rather than choosing a large team.','']
    for office,meta in cat['offices'].items():
        visual += [f'## {icons.get(office,"🧩")} {office} — {meta["count"]}','']
        for key,d in roles.items():
            if d['office']==office:
                icon='🧪' if any(s in key for s in ('test','qc','review','critic','evaluation')) else '✍️' if any(s in key for s in ('writer','editor')) else icons.get(office,'🧩')
                title=key.replace('_',' ').title()
                visual += [f'- {icon} **{title}** — [`{key}`](../{d["path"]})']
        visual += ['']
    out['docs/AGENT-CATALOG.md']='\n'.join(visual).encode()

    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    generated=outputs();bad=[]
    for name,content in generated.items():
        p=R/name
        if args.check:
            if not p.is_file() or p.read_bytes()!=content:bad.append(name)
        else:
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
    if bad:
        print('Generated files out of date:\n'+'\n'.join(bad));sys.exit(1)
    print(f'{"Verified" if args.check else "Generated"} {len(generated)} derived files')
if __name__=='__main__':main()
