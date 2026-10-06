from __future__ import annotations
import json
import hashlib
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
    # Quality, Routing, Delegation, Hybrid Memory & Execution release checks. These are local/read-only.
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
    if holdout.get('aco_version')!='0.7.3':errors.append('Historical final routing holdout provenance/version mismatch')
    if not holdout.get('cases'):errors.append('Final routing holdout is empty')
    trained_prompts={x.get('prompt') for x in examples.get('examples',[]) if x.get('prompt')}
    holdout_prompts={x.get('prompt') for x in holdout.get('cases',[]) if x.get('prompt')}
    if trained_prompts & holdout_prompts:errors.append('Final routing holdout overlaps training examples')
    holdout3=read_json(ROOT/'config/routing-v072-holdout-3.json')
    if holdout3.get('schema_version')!=1:errors.append('v0.7.2 routing holdout schema mismatch')
    if holdout3.get('aco_version')!='0.7.3':errors.append('Historical v0.7.2 routing holdout provenance/version mismatch')
    if len(holdout3.get('cases',[]))<30:errors.append('v0.7.2 routing holdout is too small')
    holdout3_prompts={x.get('prompt') for x in holdout3.get('cases',[]) if x.get('prompt')}
    if trained_prompts & holdout3_prompts:errors.append('v0.7.2 routing holdout overlaps training examples')
    holdout4=read_json(ROOT/'config/routing-v073-holdout-4.json')
    holdout5=read_json(ROOT/'config/routing-v073-holdout-5.json')
    if holdout4.get('schema_version')!=1 or holdout4.get('aco_version')!='0.7.3':errors.append('Historical v0.7.3 development routing holdout contract mismatch')
    if holdout5.get('schema_version')!=1 or holdout5.get('aco_version')!='0.7.3':errors.append('Historical v0.7.3 final routing holdout contract mismatch')
    if len(holdout5.get('cases',[]))!=40:errors.append('v0.7.3 final routing holdout must contain 40 cases')
    holdout4_prompts={x.get('prompt') for x in holdout4.get('cases',[]) if x.get('prompt')}
    holdout5_prompts={x.get('prompt') for x in holdout5.get('cases',[]) if x.get('prompt')}
    if trained_prompts & holdout5_prompts:errors.append('v0.7.3 final routing holdout overlaps training examples')
    if (holdout_prompts|holdout3_prompts|holdout4_prompts) & holdout5_prompts:errors.append('v0.7.3 final routing holdout overlaps prior holdouts')

    def _sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    def _semantic_json_sha(path: Path) -> str:
        data=read_json(path)
        if isinstance(data,dict):data.pop('aco_version',None)
        payload=(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
        return hashlib.sha256(payload).hexdigest()
    fresh_freeze=read_json(ROOT/'release/v073-holdout-5-freeze.json')
    fresh_result=read_json(ROOT/'release/v073-holdout-5-result.json')
    dev_result=read_json(ROOT/'release/v073-holdout-4-result.json')
    semantic_freeze=read_json(ROOT/'release/v073-routing-semantic-freeze.json')
    if _sha(ROOT/'config/routing-v073-holdout-5.json')!=fresh_freeze.get('sha256'):errors.append('v0.7.3 final routing holdout hash differs from frozen pre-run hash')
    if fresh_result.get('disposition')!='final_fresh_release_gate' or fresh_result.get('first_execution',{}).get('status')!='passed' or fresh_result.get('first_execution',{}).get('critical_failures')!=0:
        errors.append('v0.7.3 final fresh holdout first-run evidence is invalid')
    if dev_result.get('disposition')!='development_regression_only' or dev_result.get('first_execution',{}).get('status')!='failed':
        errors.append('v0.7.3 development holdout chronology is invalid')
    if _sha(ROOT/'scripts/aco/routing.py')!=semantic_freeze.get('routing_py_sha256'):errors.append('Routing logic changed after final fresh holdout')
    for rel,key in [('config/routing-hints.json','routing_hints_semantic_sha256'),('config/routing-examples.json','routing_examples_semantic_sha256'),('config/role-contracts.json','role_contracts_semantic_sha256'),('catalog.json','catalog_semantic_sha256')]:
        if _semantic_json_sha(ROOT/rel)!=semantic_freeze.get(key):errors.append('Routing semantics changed after final fresh holdout: '+rel)
    simulation=read_json(ROOT/'release/behavioral-simulation.json')
    if simulation.get('schema_version')!=1:errors.append('Behavioral simulation schema mismatch')
    if simulation.get('aco_version')!=VERSION:errors.append('Behavioral simulation version mismatch')
    if not simulation.get('cases'):errors.append('Behavioral simulation is empty')
    from .routing import route_benchmark
    routing_gate=route_benchmark(ROOT/'config/routing-final-holdout.json')
    if routing_gate.get('status')!='passed' or routing_gate.get('critical_failures')!=0 or routing_gate.get('score',0)<90:
        errors.append('Final routing holdout gate failed')
    routing_gate_v072=route_benchmark(ROOT/'config/routing-v072-holdout-3.json')
    if routing_gate_v072.get('status')!='passed' or routing_gate_v072.get('critical_failures')!=0 or routing_gate_v072.get('score',0)<92:
        errors.append('v0.7.2 fresh routing holdout regression gate failed')
    routing_gate_v073_dev=route_benchmark(ROOT/'config/routing-v073-holdout-4.json')
    if routing_gate_v073_dev.get('status')!='passed' or routing_gate_v073_dev.get('critical_failures')!=0:
        errors.append('v0.7.3 development routing regression gate failed')
    routing_gate_v073=route_benchmark(ROOT/'config/routing-v073-holdout-5.json')
    if routing_gate_v073.get('status')!='passed' or routing_gate_v073.get('critical_failures')!=0 or routing_gate_v073.get('score',0)<98:
        errors.append('v0.7.3 final fresh routing holdout gate failed')
    context_cfg=read_json(ROOT/'config/context-engine.json')
    if context_cfg.get('schema_version')!=1 or context_cfg.get('aco_version')!=VERSION:
        errors.append('Context engine contract mismatch')
    from .efficiency import context_benchmark, real_world_benchmark, scope_boundary_benchmark
    context_gate=context_benchmark(ROOT/'config/context-benchmark.json')
    if context_gate.get('status')!='passed' or context_gate.get('critical_failures')!=0:
        errors.append('Context efficiency benchmark gate failed')
    scope_gate=scope_boundary_benchmark(ROOT/'config/scope-boundary-benchmark-v073.json')
    if scope_gate.get('status')!='passed' or scope_gate.get('critical_failures')!=0 or scope_gate.get('score')!=100.0 or scope_gate.get('drive_prompts')!=0:
        errors.append('v0.7.3 exact-scope boundary benchmark gate failed')
    real_world_gate=real_world_benchmark(ROOT/'config/real-world-benchmark-v073.json')
    if real_world_gate.get('status')!='passed' or real_world_gate.get('critical_failures')!=0 or real_world_gate.get('cases')!=120 or real_world_gate.get('drive_prompts')!=0:
        errors.append('v0.7.3 120-scenario real-world regression gate failed')
    from .quality import score_simulation
    simulation_gate=score_simulation(ROOT/'release/behavioral-simulation.json')
    if simulation_gate.get('status')!='passed' or simulation_gate.get('critical_failures')!=0 or simulation_gate.get('score',0)<90:
        errors.append('Behavioral simulation gate failed')
    # v0.7 execution contracts and deterministic conformance gate.
    for filename in ('capabilities.json','permission-policy.json','adapter-contract.json','workflow-states.json','execution-benchmark.json','memory-classes.json','integration-adapters.json','delegation-benchmark.json','integration-benchmark.json','privacy-policy.json','context-engine.json','context-benchmark.json','real-world-benchmark-v072.json','real-world-benchmark-v073.json','scope-boundary-benchmark-v073.json','goal-graph.json','autonomy-policy.json','autonomy-benchmark.json','adaptive-policy.json','adaptive-benchmark.json','adaptive-v090-holdout.json'):
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
    from .autonomy import autonomy_benchmark
    from .goals import goal_graph_check
    autonomy_gate=autonomy_benchmark(ROOT/'config/autonomy-benchmark.json')
    if autonomy_gate.get('status')!='passed' or autonomy_gate.get('critical_failures')!=0 or autonomy_gate.get('score')!=100.0 or autonomy_gate.get('cases')<25:
        errors.append('ACO 0.8 Goal Graph / Autonomy Engine benchmark gate failed')
    goal_example=goal_graph_check(read_json(ROOT/'examples/goals/artist-program.json'))
    if goal_example.get('status')!='valid':
        errors.append('Packaged Goal Graph example is invalid')
    from .adaptive import adaptive_benchmark
    adaptive_gate=adaptive_benchmark(ROOT/'config/adaptive-benchmark.json')
    if adaptive_gate.get('status')!='passed' or adaptive_gate.get('critical_failures')!=0 or adaptive_gate.get('score')!=100.0 or adaptive_gate.get('cases')<30:
        errors.append('ACO 0.9 adaptive safety benchmark gate failed')
    adaptive_holdout=read_json(ROOT/'config/adaptive-v090-holdout.json')
    adaptive_freeze=read_json(ROOT/'release/v090-adaptive-holdout-freeze.json')
    adaptive_result=read_json(ROOT/'release/v090-adaptive-holdout-result.json')
    adaptive_semantic=read_json(ROOT/'release/v090-adaptive-semantic-freeze.json')
    if adaptive_freeze.get('disposition')!='final_fresh_release_gate' or adaptive_freeze.get('frozen_before_first_execution') is not True:
        errors.append('ACO 0.9 adaptive fresh holdout freeze metadata invalid')
    if _sha(ROOT/'config/adaptive-v090-holdout.json')!=adaptive_freeze.get('sha256'):
        errors.append('ACO 0.9 adaptive fresh holdout hash differs from frozen pre-run hash')
    first_adaptive=adaptive_result.get('first_execution',{})
    if adaptive_result.get('disposition')!='final_fresh_release_gate' or adaptive_result.get('holdout_sha256')!=adaptive_freeze.get('sha256') or first_adaptive.get('status')!='passed' or first_adaptive.get('critical_failures')!=0 or first_adaptive.get('score')!=100.0 or first_adaptive.get('cases')<25:
        errors.append('ACO 0.9 adaptive fresh holdout first-run evidence invalid')
    dev_ids={x.get('id') for x in read_json(ROOT/'config/adaptive-benchmark.json').get('cases',[])}
    fresh_ids={x.get('id') for x in adaptive_holdout.get('cases',[])}
    if dev_ids & fresh_ids:
        errors.append('ACO 0.9 adaptive fresh holdout case IDs overlap development benchmark')
    if adaptive_semantic.get('disposition')!='post_fresh_holdout_semantic_freeze':
        errors.append('ACO 0.9 adaptive semantic freeze metadata invalid')
    for rel,expected in adaptive_semantic.get('files',{}).items():
        if _sha(ROOT/rel)!=expected:
            errors.append('Adaptive semantics changed after final fresh holdout: '+rel)
    adaptive_fresh_gate=adaptive_benchmark(ROOT/'config/adaptive-v090-holdout.json')
    if adaptive_fresh_gate.get('status')!='passed' or adaptive_fresh_gate.get('critical_failures')!=0 or adaptive_fresh_gate.get('score')!=100.0:
        errors.append('ACO 0.9 frozen fresh adaptive holdout regression gate failed')
    from .delegation import delegation_benchmark
    delegation_gate=delegation_benchmark(ROOT/'config/delegation-benchmark.json')
    if delegation_gate.get('status')!='passed' or delegation_gate.get('critical_failures')!=0 or delegation_gate.get('score',0)<100:
        errors.append('Delegation behavior benchmark gate failed')
    from .integrations import integration_benchmark
    integration_gate=integration_benchmark(ROOT/'config/integration-benchmark.json')
    if integration_gate.get('status')!='passed' or integration_gate.get('critical_failures')!=0 or integration_gate.get('score',0)<100:
        errors.append('Integration resolution benchmark gate failed')
    from .privacy import privacy_scan
    privacy_gate=privacy_scan(ROOT)
    if privacy_gate.get('status')!='passed':
        errors.append('Privacy/PII release gate failed: '+', '.join(sorted({x['type'] for x in privacy_gate.get('findings',[])})))
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
    for name in ('plugin.json','.codex-plugin','.agents/plugins','docs/PUBLIC-SUBMISSION.md','PRIVACY.md','TERMS.md','MCP-ROADMAP.md','docs/CODEX-MIGRATION-PROMPT.txt'):
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
            'delegation_score':delegation_gate.get('score'),'integration_score':integration_gate.get('score'),'privacy_findings':len(privacy_gate.get('findings',[])),'routing_v072_score':routing_gate_v072.get('score'),'routing_v073_development_score':routing_gate_v073_dev.get('score'),'routing_v073_fresh_score':routing_gate_v073.get('score'),'context_benchmark_score':context_gate.get('score'),'context_mean_selection_ratio':context_gate.get('mean_selection_ratio'),'scope_boundary_score':scope_gate.get('score'),'scope_boundary_cases':scope_gate.get('cases'),'real_world_benchmark_score':real_world_gate.get('score'),'real_world_context_selection_ratio':real_world_gate.get('mean_context_selection_ratio'),'checks':['TOML','role catalogue and dependencies','generated parity','no plugin artifacts','basic secret/private-path scan','release hashes','relative documentation links','resource identities/roles/methods','role contracts','routing holdout regression gate','v0.7.2 routing regression gate','v0.7.3 development routing regression gate','v0.7.3 frozen fresh routing holdout gate','routing semantic freeze gate','context efficiency gate','exact-scope privacy boundary gate','v0.7.3 120-scenario real-world regression gate','behavioral simulation gate','delegation benchmark gate','hybrid-memory contracts','integration adapter benchmark gate','privacy/PII release gate','capability/permission/adapter/workflow contracts','execution policy benchmark gate','Goal Graph contract','ACO 0.8 autonomy benchmark gate','ACO 0.9 adaptive shadow-learning benchmark gate','ACO 0.9 frozen fresh adaptive holdout gate','ACO 0.9 adaptive semantic freeze gate'],
            'execution_benchmark_score':execution_gate.get('score'),'autonomy_benchmark_score':autonomy_gate.get('score'),'autonomy_benchmark_cases':autonomy_gate.get('cases'),'adaptive_benchmark_score':adaptive_gate.get('score'),'adaptive_benchmark_cases':adaptive_gate.get('cases'),'adaptive_fresh_score':adaptive_fresh_gate.get('score'),'adaptive_fresh_cases':adaptive_fresh_gate.get('cases'),'limitations':'Static/local checks; no professional-quality certification and no live external adapter/provider action is executed by validation.'}
