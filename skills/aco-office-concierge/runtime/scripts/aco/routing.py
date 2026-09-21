from __future__ import annotations

import collections
import json
import math
import re
from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json

_STOP = set('''a an the and or to of for from in on at with without into my our your this that these those is are be been being i we you it as by about need want help please can could should would how what when where who me us make create prepare build find review check manage plan develop write draft update analyze analyse research improve design coordinate handle run use using new current actual some all before after do does did have has had get getting'''.split())


def _tokens(text: str) -> list[str]:
    text = text.lower().replace('&', ' and ')
    text = re.sub(r'[^a-z0-9à-ÿ]+', ' ', text)
    out: list[str] = []
    for word in text.split():
        if word in _STOP or len(word) < 2:
            continue
        if len(word) > 5 and word.endswith('ing'):
            word = word[:-3]
        elif len(word) > 4 and word.endswith('ies'):
            word = word[:-3] + 'y'
        elif len(word) > 4 and word.endswith('s') and not word.endswith('ss'):
            word = word[:-1]
        out.append(word)
    return out


def _phrase_in(text: str, phrase: str) -> bool:
    hay = ' ' + re.sub(r'[^a-z0-9à-ÿ]+', ' ', text.lower()).strip() + ' '
    needle = ' ' + re.sub(r'[^a-z0-9à-ÿ]+', ' ', phrase.lower()).strip() + ' '
    return bool(needle.strip()) and needle in hay

def _intent_clauses(text: str) -> list[set[str]]:
    """Extract short semantic signatures from a role purpose without external NLP.

    This is deliberately conservative: a clause only contributes when the request
    shares at least two meaningful terms, so one generic word cannot hijack routing.
    """
    chunks = re.split(r'[,;:.]|\band\b|\bfor\b', text.lower())
    out: list[set[str]] = []
    for chunk in chunks:
        toks = set(_tokens(chunk))
        if len(toks) >= 2:
            out.append(toks)
    return out


def _load_catalog(root: Path) -> dict[str, Any]:
    path = root / 'catalog.json'
    if not path.is_file():
        raise ACOError(f'Missing catalog.json under {root}')
    data = read_json(path)
    if data.get('aco_version') != VERSION and root == ROOT:
        raise ACOError('Catalogue version does not match ACO VERSION')
    return data


def _load_hints(root: Path) -> dict[str, Any]:
    path = root / 'config/routing-hints.json'
    if not path.is_file():
        raise ACOError(f'Missing routing hints: {path}')
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported routing-hints schema')
    return data


def _role_docs(catalog: dict[str, Any], hints: dict[str, Any], root: Path) -> tuple[dict[str, list[str]], dict[str, set[str]], collections.Counter[str]]:
    docs: dict[str, list[str]] = {}
    keydocs: dict[str, set[str]] = {}
    df: collections.Counter[str] = collections.Counter()
    role_hints = hints.get('role_hints', {})
    contracts = {}
    cpath = root / 'config/role-contracts.json'
    if cpath.is_file():
        try:
            contracts = read_json(cpath).get('roles', {})
        except Exception:
            contracts = {}
    for key, meta in catalog['agents'].items():
        phrases = ' '.join(role_hints.get(key, []))
        contract = contracts.get(key, {})
        structured = ' '.join(str(contract.get(field, '')) for field in ('purpose','inputs','method','outputs','verification','escalation'))
        doc = _tokens(key.replace('_', ' ') + ' ' + meta['description'] + ' ' + phrases + ' ' + structured)
        docs[key] = doc
        keydocs[key] = set(_tokens(key.replace('_', ' ')))
        for token in set(doc):
            df[token] += 1
    return docs, keydocs, df


def suggest_route(prompt: str, *, root: Path | None = None, max_roles: int = 3) -> dict[str, Any]:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ACOError('Prompt must be non-empty text')
    if max_roles < 1 or max_roles > 5:
        raise ACOError('max_roles must be between 1 and 5')
    root = (root or ROOT).expanduser().absolute()
    catalog = _load_catalog(root)
    hints = _load_hints(root)
    docs, keydocs, df = _role_docs(catalog, hints, root)
    contracts_path = root / 'config/role-contracts.json'
    contracts = read_json(contracts_path).get('roles', {}) if contracts_path.is_file() else {}
    examples_path = root / 'config/routing-examples.json'
    routing_examples = read_json(examples_path).get('examples', []) if examples_path.is_file() else []
    n_roles = len(catalog['agents'])
    role_hints = hints.get('role_hints', {})
    office_hints = hints.get('office_hints', {})
    synonyms = hints.get('synonyms', {})

    p0 = prompt.lower()
    base = _tokens(prompt)
    if any(phrase in p0 for phrase in ('not enough information', 'not enough info', 'have not said what', 'haven\'t said what', 'have not described the actual problem', 'not described the actual problem', 'have not described the actual request', 'have not explained whether', 'haven\'t explained whether', 'have not told you whether', 'haven\'t told you whether', 'have not given enough detail', 'haven\'t given enough detail', 'not given enough detail', 'have not explained the task', 'haven\'t explained the task', 'have not described what i need done', 'haven\'t described what i need done', 'do not know which office', 'don\'t know which office', 'whether it concerns')):
        return {
            'status': 'needs_clarification', 'aco_version': VERSION, 'prompt': prompt,
            'office': 'shared', 'selected_roles': ['office_concierge'], 'confidence': 'low',
            'ranked_candidates': [], 'office_candidates': [],
            'reason': 'The request explicitly states that routing information is missing.',
            'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
        }
    # Very low-information requests should not be over-routed from incidental words.
    if len(base) < 3:
        return {
            'status': 'needs_clarification', 'aco_version': VERSION, 'prompt': prompt,
            'office': 'shared', 'selected_roles': ['office_concierge'], 'confidence': 'low',
            'ranked_candidates': [], 'office_candidates': [],
            'reason': 'Insufficient task detail; use the Concierge and ask one decisive question.',
            'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
        }
    expanded = list(base)
    for token in base:
        expanded.extend(synonyms.get(token, []))
    q = collections.Counter(expanded)

    def idf(token: str) -> float:
        return math.log((n_roles + 1) / (df[token] + 1)) + 1.0

    # Example-based routing uses only curated, non-private development examples.
    # It is a deterministic nearest-neighbour hint, not model training or runtime memory.
    example_office_boost: dict[str, float] = collections.defaultdict(float)
    example_role_boost: dict[str, float] = collections.defaultdict(float)
    qset = set(expanded)
    q_weight = sum(idf(t) for t in qset) or 1.0
    neighbours: list[tuple[float, dict[str, Any]]] = []
    for ex in routing_examples:
        eset = set(_tokens(str(ex.get('prompt', ''))))
        if not eset:
            continue
        inter = qset & eset
        if len(inter) < 2:
            continue
        inter_w = sum(idf(t) for t in inter)
        # Coverage of the shorter semantic request is more useful than raw Jaccard
        # for concise paraphrases, but cap generic overlap.
        ex_w = sum(idf(t) for t in eset) or 1.0
        sim = inter_w / min(q_weight, ex_w)
        if sim >= 0.28:
            neighbours.append((sim, ex))
    neighbours.sort(key=lambda x: x[0], reverse=True)
    for sim, ex in neighbours[:4]:
        office_name = ex.get('office')
        if office_name in catalog['offices']:
            example_office_boost[office_name] += min(7.0, sim * 8.0)
        for role in ex.get('roles', [])[:2]:
            if role in catalog['agents']:
                example_role_boost[role] += min(8.0, sim * 9.0)

    office_boost: dict[str, float] = collections.defaultdict(float)
    office_reasons: dict[str, list[str]] = collections.defaultdict(list)
    profiles = hints.get('office_profiles', {})
    # Generic discovery hints are useful but weaker than explicit domain-boundary signals.
    for office, phrases in office_hints.items():
        for phrase in phrases:
            if _phrase_in(p0, phrase):
                office_boost[office] += 3.0 + min(3.0, len(phrase.split()) * 0.5)
                office_reasons[office].append(phrase)
    for office, profile in profiles.items():
        for phrase in profile.get('strong_signals', []):
            if _phrase_in(p0, phrase):
                office_boost[office] += 8.0 + min(5.0, len(phrase.split()) * 0.8)
                office_reasons[office].append('strong:' + phrase)
        for phrase in profile.get('negative_signals', []):
            if _phrase_in(p0, phrase):
                office_boost[office] -= 7.0 + min(4.0, len(phrase.split()) * 0.6)
                office_reasons[office].append('contrast:' + phrase)

    # A matched curated role example is also evidence for that role's office.
    # Cap this boost so office-level boundary signals can still override it.
    role_hint_office_boost: dict[str, float] = collections.defaultdict(float)
    for role, phrases in role_hints.items():
        meta = catalog['agents'].get(role)
        if not meta:
            continue
        matched = sum(1 for phrase in phrases if _phrase_in(p0, phrase))
        if matched:
            role_hint_office_boost[meta['office']] += min(10.0, 4.0 + 2.0 * matched)

    scored: list[dict[str, Any]] = []
    by_office: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for key, meta in catalog['agents'].items():
        dset = set(docs[key])
        lexical = 0.0
        reasons: list[str] = []
        for token, count in q.items():
            if token in dset:
                lexical += idf(token) * (2.6 if token in keydocs[key] else 1.0) * min(count, 2)
        phrase_boost = 0.0
        for phrase in role_hints.get(key, []):
            if _phrase_in(p0, phrase):
                phrase_boost += 12.0 + min(6.0, len(phrase.split()) * 0.8)
                reasons.append(f'phrase:{phrase}')
        purpose = str(contracts.get(key, {}).get('purpose') or meta.get('description', ''))
        qset = set(expanded)
        signature_boost = 0.0
        for clause in _intent_clauses(purpose):
            overlap = len(clause & qset)
            if overlap >= 2:
                signature_boost += min(7.0, 1.8 * overlap)
        signature_boost = min(12.0, signature_boost)
        if signature_boost:
            reasons.append(f'signature:{signature_boost:.1f}')
        exemplar_boost = example_role_boost.get(key, 0.0)
        if exemplar_boost:
            reasons.append(f'example:{exemplar_boost:.1f}')
        raw = lexical + phrase_boost + signature_boost + exemplar_boost
        if key.endswith('_orchestrator') and not any(x in p0 for x in ('route', 'across offices', 'multi-office', 'multi office', 'which office')):
            raw = max(0.0, raw - 6.0)
        if key == 'office_concierge' and not any(x in p0 for x in ('route', 'which office', 'which agent', 'not enough information', 'not enough info', 'have not said what', 'whether it concerns')):
            raw = max(0.0, raw - 10.0)
        item = {'role': key, 'office': meta['office'], 'raw_score': raw, 'description': meta['description'], 'reasons': reasons}
        by_office[meta['office']].append(item)

    # Two-stage routing: choose the office from explicit office evidence plus its strongest role signals,
    # then choose specialists inside that office. This prevents a role-title mention from hijacking the task.
    office_rank = []
    for office in catalog['offices']:
        role_scores = sorted((x['raw_score'] for x in by_office.get(office, [])), reverse=True)
        best = role_scores[0] if role_scores else 0.0
        second = role_scores[1] if len(role_scores) > 1 else 0.0
        role_evidence = role_hint_office_boost.get(office, 0.0)
        example_evidence = min(12.0, example_office_boost.get(office, 0.0))
        score = office_boost.get(office, 0.0) + role_evidence + example_evidence + 0.62 * best + 0.18 * second
        office_rank.append({'office': office, 'score': score, 'explicit_boost': office_boost.get(office, 0.0) + role_evidence + example_evidence})
    office_rank.sort(key=lambda x: (x['score'], x['office']), reverse=True)
    winning = office_rank[0] if office_rank else {'office': 'shared', 'score': 0.0, 'explicit_boost': 0.0}
    office = winning['office']
    # Short requests with no explicit domain signal are ambiguity, not routing evidence.
    if len(base) <= 4 and max((x.get('explicit_boost', 0.0) for x in office_rank), default=0.0) <= 0:
        return {
            'status': 'needs_clarification', 'aco_version': VERSION, 'prompt': prompt,
            'office': 'shared', 'selected_roles': ['office_concierge'], 'confidence': 'low',
            'ranked_candidates': [], 'office_candidates': [{**x, 'score': round(x['score'], 4)} for x in office_rank[:5]],
            'reason': 'Short request without a reliable domain anchor; ask one decisive question.',
            'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
        }
    # If the request carries almost no task signal, do not pretend precision.
    if winning['score'] < 4.0:
        return {
            'status': 'needs_clarification', 'aco_version': VERSION, 'prompt': prompt,
            'office': 'shared', 'selected_roles': ['office_concierge'], 'confidence': 'low',
            'ranked_candidates': [], 'office_candidates': office_rank[:5],
            'reason': 'Insufficient task signal; use the Concierge and ask one decisive question.',
            'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
        }

    allowed_roles = {x['role'] for x in by_office.get(office, [])}
    allowed_roles.update(catalog['offices'].get(office, {}).get('dependencies', []))
    if office != 'shared':
        allowed_roles.update(k for k, m in catalog['agents'].items() if m['office'] == 'shared')
    all_items = {x['role']: x for items in by_office.values() for x in items}
    for role in allowed_roles:
        item = dict(all_items[role])
        item['reasons'] = list(item['reasons'])
        item['score'] = round(item['raw_score'] + office_boost.get(office, 0.0) * 0.35, 4)
        if office_reasons.get(office):
            item['reasons'].append('office:' + ', '.join(office_reasons[office][:2]))
        if item['score'] > 0:
            scored.append({k: v for k, v in item.items() if k != 'raw_score'})
    scored.sort(key=lambda x: (x['score'], x['role']), reverse=True)
    if not scored:
        return {
            'status': 'needs_clarification', 'aco_version': VERSION, 'prompt': prompt,
            'office': 'shared', 'selected_roles': ['office_concierge'], 'confidence': 'low',
            'ranked_candidates': [], 'office_candidates': office_rank[:5],
            'reason': 'Office signal exists but no role is sufficiently specific; use the Concierge.',
            'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
        }

    top = scored[0]
    # Shared is the ambiguity-safe office. If no specific shared specialist has a strong signal, use the Concierge.
    if office == 'shared' and top['role'] != 'office_concierge' and top['score'] < 12.0:
        concierge = next((x for x in scored if x['role'] == 'office_concierge'), None)
        if concierge is not None:
            top = concierge
            scored = [concierge] + [x for x in scored if x['role'] != 'office_concierge']
    selected = [top]
    if max_roles > 1 and len(scored) > 1:
        second = scored[1]
        if second['score'] >= max(10.0, top['score'] * 0.90):
            selected.append(second)
    if max_roles > 2 and len(scored) > 2 and len(selected) == 2:
        third = scored[2]
        if third['score'] >= max(12.0, top['score'] * 0.94):
            selected.append(third)

    margin = top['score'] - (scored[1]['score'] if len(scored) > 1 else 0)
    confidence = 'high' if winning['score'] >= 14 and top['score'] >= 12 else 'medium' if winning['score'] >= 7 else 'low'
    return {
        'status': 'routed' if confidence != 'low' else 'routed_with_low_confidence',
        'aco_version': VERSION,
        'prompt': prompt,
        'office': office,
        'selected_roles': [x['role'] for x in selected],
        'confidence': confidence,
        'margin': round(margin, 4),
        'ranked_candidates': scored[:max(5, max_roles)],
        'office_candidates': [{**x, 'score': round(x['score'], 4)} for x in office_rank[:5]],
        'policy': 'Routing is advisory. It does not authorize tools/actions or broaden private scope.'
    }



def route_benchmark(path: Path | None = None, *, root: Path | None = None, split: str | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    path = (path or root / 'config/routing-benchmark.json').expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported routing benchmark schema')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Routing benchmark must contain cases')
    if split:
        cases = [c for c in cases if c.get('split') == split]
        if not cases:
            raise ACOError(f'No benchmark cases for split: {split}')

    rows = []
    office_ok = top1_ok = top3_ok = minimal_ok = 0
    critical_failures = 0
    for case in cases:
        result = suggest_route(case['prompt'], root=root, max_roles=3)
        ranked = result.get('ranked_candidates', [])
        selected_roles = result.get('selected_roles') or []
        top1 = ranked[0]['role'] if ranked else (selected_roles or [None])[0]
        top3 = [x['role'] for x in ranked[:3]]
        for role in selected_roles:
            if role not in top3:
                top3.append(role)
        top3 = top3[:3]
        expected_office = case['expected_office']
        acceptable = set(case['acceptable_roles'])
        office_pass = result.get('office') == expected_office
        top1_pass = top1 in acceptable
        top3_pass = bool(acceptable.intersection(top3))
        minimal_pass = len(result.get('selected_roles', [])) <= int(case.get('max_selected_roles', 2))
        office_ok += office_pass
        top1_ok += top1_pass
        top3_ok += top3_pass
        minimal_ok += minimal_pass
        critical = bool(case.get('critical')) and (not office_pass or not top3_pass)
        critical_failures += int(critical)
        rows.append({
            'id': case['id'], 'split': case.get('split'), 'expected_office': expected_office,
            'acceptable_roles': case['acceptable_roles'], 'actual_office': result.get('office'),
            'selected_roles': result.get('selected_roles', []), 'top3': top3,
            'office_pass': office_pass, 'top1_pass': top1_pass, 'top3_pass': top3_pass,
            'minimal_team_pass': minimal_pass, 'critical_failure': critical
        })
    n = len(rows)
    office_acc = office_ok / n
    top1_acc = top1_ok / n
    top3_recall = top3_ok / n
    minimal_rate = minimal_ok / n
    overstaff_rate = 1.0 - minimal_rate
    score = 100.0 * (0.30 * office_acc + 0.40 * top1_acc + 0.20 * top3_recall + 0.10 * minimal_rate)
    gate = data.get('gate', {})
    passed = (
        score >= float(gate.get('minimum_score', 90.0)) and
        office_acc >= float(gate.get('minimum_office_accuracy', 0.90)) and
        top1_acc >= float(gate.get('minimum_top1_role_accuracy', 0.85)) and
        top3_recall >= float(gate.get('minimum_top3_role_recall', 0.95)) and
        overstaff_rate <= float(gate.get('maximum_overstaff_rate', 0.05)) and
        critical_failures <= int(gate.get('maximum_critical_failures', 0))
    )
    return {
        'status': 'passed' if passed else 'failed', 'aco_version': VERSION, 'path': str(path), 'split': split or 'all',
        'cases': n, 'score': round(score, 2), 'office_accuracy': round(office_acc, 4),
        'top1_role_accuracy': round(top1_acc, 4), 'top3_role_recall': round(top3_recall, 4),
        'minimal_team_rate': round(minimal_rate, 4), 'overstaff_rate': round(overstaff_rate, 4),
        'critical_failures': critical_failures, 'gate': gate, 'failures': [r for r in rows if r['critical_failure'] or not r['top1_pass']]
    }



def role_contract(role: str, *, root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    path = root / 'config/role-contracts.json'
    if not path.is_file():
        raise ACOError(f'Missing generated role contracts: {path}')
    data = read_json(path)
    contract = data.get('roles', {}).get(role)
    if not contract:
        raise ACOError(f'Unknown role: {role}')
    return {'status': 'found', 'aco_version': VERSION, 'role': role, 'contract': contract}


def role_overlap(*, root: Path | None = None, threshold: float = 0.62, limit: int = 30) -> dict[str, Any]:
    if not 0 < threshold <= 1:
        raise ACOError('threshold must be >0 and <=1')
    root = (root or ROOT).expanduser().absolute()
    catalog = _load_catalog(root)
    docs = {}
    for key, meta in catalog['agents'].items():
        docs[key] = set(_tokens(key.replace('_', ' ') + ' ' + meta['description']))
    pairs = []
    keys = sorted(docs)
    for i, a in enumerate(keys):
        for b in keys[i+1:]:
            if catalog['agents'][a]['office'] != catalog['agents'][b]['office']:
                continue
            ua, ub = docs[a], docs[b]
            union = ua | ub
            if not union:
                continue
            sim = len(ua & ub) / len(union)
            if sim >= threshold:
                pairs.append({'a': a, 'b': b, 'office': catalog['agents'][a]['office'], 'jaccard': round(sim, 4)})
    pairs.sort(key=lambda x: x['jaccard'], reverse=True)
    return {
        'status': 'review_candidates' if pairs else 'clean', 'aco_version': VERSION, 'threshold': threshold,
        'pairs': pairs[:limit], 'pair_count': len(pairs),
        'policy': 'Similarity is a maintenance signal only. Never merge or retire roles automatically.'
    }
