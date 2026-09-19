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
from pathlib import Path
R = Path(__file__).resolve().parents[1]


def encoded(v):
    return json.dumps(v, ensure_ascii=False)


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
    out = {'catalog.json':(json.dumps(cat,indent=2,ensure_ascii=False)+'\n').encode(),
           'skills/aco-office-concierge/references/CATALOG.json':(json.dumps(cat,indent=2,ensure_ascii=False)+'\n').encode()}
    pattern = re.compile(r'(?<![\w])('+'|'.join(sorted(map(re.escape,roles),key=len,reverse=True))+r')(?![\w])')
    for key,d in roles.items():
        instructions = pattern.sub(lambda m:'aco_'+m.group(1),d['instructions'])
        out[d['codex_path']] = (f'name = {encoded(d["native_name"])}\n'
                               f'description = {encoded(d["description"])}\n'
                               f'developer_instructions = {encoded(instructions)}\n').encode()
    for p in (R/'assets/context-templates').glob('*.md'):
        out['skills/aco-context-setup/references/templates/'+p.name]=p.read_bytes()
    # A small runtime accompanies the native skill; not a duplicated canonical role collection.
    base='skills/aco-office-concierge/runtime/'
    out[base+'VERSION']=(R/'VERSION').read_bytes()
    out[base+'RUNTIME-ONLY']=b'Local knowledge/session/event commands only. Use the full source release for install, migrate and validate.\n'
    for name in ('aco_cli.py','aco/__init__.py','aco/common.py','aco/memory.py','aco/drive.py','aco/cli.py','aco/planning.py','aco/production.py','aco/finance.py'):
        out[base+'scripts/'+name]=(R/'scripts'/name).read_bytes()
    for p in (R/'assets/context-templates').glob('*.md'):
        out[base+'assets/context-templates/'+p.name]=p.read_bytes()
    out[base+'config/workflows.json']=(R/'skills/aco-office-concierge/references/WORKFLOWS.json').read_bytes()
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
           'Start with CHATGPT.md or AGENTS.md. Select an office below, then read its local ROLE-INDEX and only selected methods. Do not load the full catalogue by default.','']
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
