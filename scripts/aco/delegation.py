from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import ACOError, ROOT, VERSION, read_json


def resolve_delegation(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ACOError('Delegation request must be an object')
    delegated = bool(request.get('delegated', False))
    within = bool(request.get('within_role', False))
    evidence = bool(request.get('evidence_sufficient', False))
    reversible = bool(request.get('reversible', False))
    missing = bool(request.get('missing_fact_decisive', False))
    preference = bool(request.get('subjective_preference_only_user', False))
    approval = bool(request.get('consequential_authorization', False))
    scope = bool(request.get('scope_ambiguous_material', False))
    harm = bool(request.get('material_harm_if_wrong', False))

    if not delegated:
        action = 'SUPPORT_USER_DECISION'
    elif not within:
        action = 'ROUTE_OR_ESCALATE'
    elif scope:
        action = 'CLARIFY_SCOPE'
    elif approval:
        action = 'RECOMMEND_AND_REQUEST_APPROVAL'
    elif preference:
        action = 'RECOMMEND_AND_ASK_PREFERENCE'
    elif missing or harm or not evidence:
        action = 'ASK_DECISIVE_FACT'
    elif reversible:
        action = 'DECIDE_AND_ACT'
    else:
        # Evidence may be sufficient but an irreversible professional judgment
        # still warrants an explicit recommendation before commitment.
        action = 'RECOMMEND_AND_REQUEST_APPROVAL'
    return {
        'status': 'resolved', 'aco_version': VERSION, 'action': action,
        'policy': 'Resolve delegated professional judgment rather than returning it to the user. Ask only for decisive facts/preferences/scope or consequential authorization.'
    }


def delegation_benchmark(path: Path | None = None) -> dict[str, Any]:
    path = (path or ROOT/'config/delegation-benchmark.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported delegation benchmark schema')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Delegation benchmark needs cases')
    rows=[]; passed=0; critical_failures=0
    for case in cases:
        got=resolve_delegation(case.get('input',{}))['action']
        ok=got==case.get('expect')
        passed += int(ok)
        critical_failures += int(bool(case.get('critical')) and not ok)
        rows.append({'id':case.get('id'),'expected':case.get('expect'),'actual':got,'passed':ok,'critical':bool(case.get('critical'))})
    score=passed/len(cases)*100
    gate=data.get('gate',{'minimum_score':100,'maximum_critical_failures':0})
    ok=score>=float(gate.get('minimum_score',100)) and critical_failures<=int(gate.get('maximum_critical_failures',0))
    return {'status':'passed' if ok else 'failed','aco_version':VERSION,'cases':len(cases),'passed':passed,'score':round(score,2),'critical_failures':critical_failures,'gate':gate,'rows':rows}
