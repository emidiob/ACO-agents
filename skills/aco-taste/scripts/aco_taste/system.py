"""One scoped DESIGN.md source of truth; evidence-based and refusal-safe."""
from __future__ import annotations
from pathlib import Path
import re

SAFE_ROLES={'paper','surface','ink','muted','accent','focus','error','success','heading','body','caption','code','space-sm','space-md','space-lg','radius','max-width','grid'}

def compile_design_md(packet):
    if not isinstance(packet,dict):raise ValueError('Design packet must be object')
    name=str(packet.get('name','')).strip()
    if not name:raise ValueError('name required')
    evidence=packet.get('evidence',[])
    if not isinstance(evidence,list):raise ValueError('evidence must be list')
    confirmed=[];excluded=[];seen={}
    for entry in evidence:
        if not isinstance(entry,dict):raise ValueError('Each evidence item must be object')
        role=entry.get('role');value=entry.get('value');origin=entry.get('source');scope=entry.get('scope')
        if role not in SAFE_ROLES or not isinstance(value,str) or not value.strip() or not isinstance(origin,str) or not origin.strip() or not isinstance(scope,str) or not scope.strip():
            excluded.append({'entry':entry,'why':'missing value/source/scope or unknown role'});continue
        if entry.get('confidence') not in {'confirmed','observed-repeated'}:
            excluded.append({'role':role,'why':'not confirmed or repeated observed evidence'});continue
        if role in seen and seen[role]['value']!=value:
            excluded.append({'role':role,'why':'conflicting confirmed values; requires human choice'});seen.pop(role,None);continue
        seen[role]=entry
    confirmed=list(seen.values())
    constraints=packet.get('constraints',[])
    if not isinstance(constraints,list):raise ValueError('constraints must be list')
    lines=[f'# {name} — DESIGN.md','', '> Scope: '+str(packet.get('scope','selected product')),
           '> Evidence-based design source; never infer approval from source repetition.','', '## Core decisions','']
    for item in constraints:lines.append('- '+str(item).strip())
    lines+=['','## Verified tokens / choices','', '| Role | Value | Source | Scope |','|---|---|---|---|']
    def esc(s):return str(s).replace('|','\\|').replace('\n',' ')
    for item in confirmed:lines.append('| '+ ' | '.join(esc(item[x]) for x in ('role','value','source','scope'))+' |')
    lines+=['','## Omitted or unverified','']
    for item in excluded:lines.append('- '+esc(item.get('role',item.get('entry',{}).get('role','unknown')))+': '+esc(item['why']))
    if not excluded:lines.append('- None recorded.')
    lines+=['','## Integration constraints','','- Preserve existing approved brand assets and interaction states.','- Screen captures alone do not establish undocumented source token names.','- Changes to this document require scoped, reviewed source evidence.','']
    return {'document':'\n'.join(lines),'included':len(confirmed),'excluded':excluded,'status':'draft-from-evidence','user_approved':False}

def write_design_md(project, packet, *,apply=False):
    root=Path(project).expanduser().resolve(strict=True)
    if not root.is_dir():raise ValueError('Project folder required')
    target=root/'DESIGN.md'
    compiled=compile_design_md(packet)
    if target.exists():
        if target.is_symlink():raise ValueError('Refusing to write through symlink')
        if not packet.get('replace_approved_existing'):
            raise ValueError('Existing DESIGN.md; no automatic overwrite or parallel source of truth')
    if apply:
        target.write_text(compiled['document'],encoding='utf-8')
    return {**{k:v for k,v in compiled.items() if k!='document'},'path':str(target),'applied':apply,'document':compiled['document'] if not apply else None}
