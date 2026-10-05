from __future__ import annotations
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json


def _adapter_state(adapter: dict[str, Any], capability: str, operation: str, remote_kinds: set[str]) -> tuple[bool,list[str]]:
    blockers=[]
    if capability not in adapter.get('capabilities',[]): blockers.append('capability_not_exposed')
    if not adapter.get('available',False): blockers.append('unavailable')
    if adapter.get('kind') in remote_kinds and not adapter.get('connected',False): blockers.append('not_connected')
    ops=adapter.get('authorized_operations',[])
    if operation not in ops: blockers.append('operation_not_authorized')
    if not adapter.get('verified',False): blockers.append('adapter_unverified')
    return not blockers,blockers


def integration_resolve(request: dict[str, Any], inventory: dict[str, Any] | None=None) -> dict[str, Any]:
    if not isinstance(request,dict): raise ACOError('Integration request must be an object')
    cap=request.get('capability_id'); op=request.get('operation')
    if not isinstance(cap,str) or not cap.strip() or not isinstance(op,str) or not op.strip():
        raise ACOError('capability_id and operation are required strings')
    inventory=inventory or {'adapters':[]}
    adapters=inventory.get('adapters',[])
    if not isinstance(adapters,list): raise ACOError('inventory.adapters must be a list')
    cfg=read_json(ROOT/'config/integration-adapters.json')
    kinds=cfg.get('kind_priority',[]); remote=set(cfg.get('remote_kinds',[]))
    preferred=request.get('preferred_adapter_id')
    allow_alt=bool(request.get('allow_alternate_provider', preferred is None))
    rows=[]
    for a in adapters:
        if not isinstance(a,dict) or not isinstance(a.get('id'),str):
            raise ACOError('Each adapter must be an object with id')
        ready,blockers=_adapter_state(a,cap,op,remote)
        rows.append({'id':a['id'],'kind':a.get('kind'),'ready':ready,'blockers':blockers,'priority':a.get('priority',999)})
    byid={r['id']:r for r in rows}
    selected=None
    if preferred:
        p=byid.get(preferred)
        if p and p['ready']: selected=p
        elif not allow_alt:
            return {'status':'fallback_required','aco_version':VERSION,'selected':None,'adapters':rows,
                    'fallback':request.get('fallback','Produce the result without claiming the unavailable external action.'),
                    'policy':'The explicitly selected provider is not ready; ACO does not silently switch providers.'}
    if selected is None:
        rank={k:i for i,k in enumerate(kinds)}
        ready=[r for r in rows if r['ready']]
        ready.sort(key=lambda r:(r.get('priority',999),rank.get(r.get('kind'),999),r['id']))
        selected=ready[0] if ready else None
    return {'status':'ready' if selected else 'fallback_required','aco_version':VERSION,'selected':selected,
            'adapters':rows,'fallback':None if selected else request.get('fallback','Produce the result without claiming the unavailable external action.'),
            'policy':'Resolution uses current caller-supplied adapter evidence and never executes the adapter.'}


def integration_benchmark(path=None):
    path=(path or ROOT/'config/integration-benchmark.json').expanduser().absolute()
    data=read_json(path)
    if data.get('schema_version')!=1: raise ACOError('Unsupported integration benchmark schema')
    cases=data.get('cases')
    if not isinstance(cases,list) or not cases: raise ACOError('Integration benchmark needs cases')
    rows=[]; passed=0; critical_failures=0
    for case in cases:
        got=integration_resolve(case.get('request',{}),case.get('inventory',{}))
        adapter=(got.get('selected') or {}).get('id')
        ok=got.get('status')==case.get('expect_status') and (case.get('expect_adapter') is None or adapter==case.get('expect_adapter'))
        passed+=int(ok); critical_failures+=int(bool(case.get('critical')) and not ok)
        rows.append({'id':case.get('id'),'passed':ok,'status':got.get('status'),'adapter':adapter,'critical':bool(case.get('critical'))})
    score=passed/len(cases)*100
    gate=data.get('gate',{'minimum_score':100,'maximum_critical_failures':0})
    ok=score>=float(gate.get('minimum_score',100)) and critical_failures<=int(gate.get('maximum_critical_failures',0))
    return {'status':'passed' if ok else 'failed','aco_version':VERSION,'cases':len(cases),'passed':passed,'score':round(score,2),'critical_failures':critical_failures,'gate':gate,'rows':rows}
