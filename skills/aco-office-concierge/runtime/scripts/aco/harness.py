from __future__ import annotations

import json
import re
import statistics
from pathlib import Path
from typing import Any

from .common import ACOError, ROOT, VERSION, read_json


def _role_files(root: Path) -> list[Path]:
    root = root.expanduser().absolute()
    candidates = list(root.glob('skills/*/references/agents/*.md'))
    if not candidates:
        candidates = list(root.glob('*/references/agents/*.md'))
    return sorted(p for p in candidates if p.is_file())


def _skill_files(root: Path) -> list[Path]:
    root = root.expanduser().absolute()
    candidates = list(root.glob('skills/*/SKILL.md'))
    if not candidates:
        candidates = list(root.glob('*/SKILL.md'))
    return sorted(p for p in candidates if p.is_file())


def _estimate_tokens(chars: int) -> int:
    # Deliberately rough: language/model tokenization differs. This is a budget signal, not billing telemetry.
    return max(0, round(chars / 4))


def context_budget(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    roles = _role_files(root)
    skills = _skill_files(root)
    if not roles and not skills:
        raise ACOError(f'No ACO skills/roles found under: {root}')

    role_rows = []
    for p in roles:
        text = p.read_text(encoding='utf-8')
        role_rows.append({
            'path': str(p.relative_to(root)),
            'chars': len(text),
            'estimated_tokens': _estimate_tokens(len(text)),
            'has_bootstrap': 'ACO ROLE BOOTSTRAP' in text,
        })
    role_sizes = [r['chars'] for r in role_rows]
    skill_rows = []
    for p in skills:
        text = p.read_text(encoding='utf-8')
        skill_rows.append({'path': str(p.relative_to(root)), 'chars': len(text), 'estimated_tokens': _estimate_tokens(len(text))})

    protocol_dirs = [root / 'skills/aco-office-concierge/references/protocols', root / 'aco-office-concierge/references/protocols']
    protocols = next((d for d in protocol_dirs if d.is_dir()), None)
    protocol_rows = []
    if protocols:
        for p in sorted(protocols.glob('*.md')):
            text = p.read_text(encoding='utf-8')
            protocol_rows.append({'path': str(p.relative_to(root)), 'chars': len(text), 'estimated_tokens': _estimate_tokens(len(text))})

    bootstrap = ''
    if roles:
        sample = roles[0].read_text(encoding='utf-8')
        m = re.search(r'ACO ROLE BOOTSTRAP\n.*?(?=\nROLE CONTEXT BOUNDARY|\n## |\Z)', sample, re.S)
        if m:
            bootstrap = m.group(0)
    duplicate_bootstrap_chars = len(bootstrap) * max(0, sum(r['has_bootstrap'] for r in role_rows) - 1)

    def percentile95(values: list[int]) -> int:
        if not values:
            return 0
        values = sorted(values)
        return values[int(0.95 * (len(values) - 1))]

    role_total = sum(role_sizes)
    return {
        'status': 'audited',
        'aco_version': VERSION,
        'root': str(root),
        'scope': 'static file-size/context-budget audit; estimates are not runtime telemetry or provider billing',
        'roles': {
            'count': len(role_rows),
            'total_chars': role_total,
            'estimated_tokens_if_all_loaded': _estimate_tokens(role_total),
            'median_chars': int(statistics.median(role_sizes)) if role_sizes else 0,
            'p95_chars': percentile95(role_sizes),
            'largest': sorted(role_rows, key=lambda x: x['chars'], reverse=True)[:10],
            'shared_bootstrap_copies': sum(r['has_bootstrap'] for r in role_rows),
            'package_duplicate_bootstrap_chars': duplicate_bootstrap_chars,
            'note': 'ACO normally loads selected roles, not all roles. Package duplication is not equal to active context overhead.'
        },
        'entry_skills': {
            'count': len(skill_rows),
            'total_chars': sum(x['chars'] for x in skill_rows),
            'estimated_tokens_if_all_loaded': _estimate_tokens(sum(x['chars'] for x in skill_rows)),
        },
        'shared_protocols': {
            'count': len(protocol_rows),
            'total_chars': sum(x['chars'] for x in protocol_rows),
            'largest': sorted(protocol_rows, key=lambda x: x['chars'], reverse=True)[:5],
        },
        'guidance': [
            'Load one office/role plus only the protocols/playbooks that materially change the task.',
            'Prefer shared protocols over copying long common contracts into every role.',
            'Audit again after adding agents, playbooks or large integration schemas.'
        ]
    }


def role_stocktake(root: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).expanduser().absolute()
    roles = _role_files(root)
    if not roles:
        raise ACOError(f'No canonical ACO roles found under: {root}')

    issues = []
    for p in roles:
        text = p.read_text(encoding='utf-8')
        rel = str(p.relative_to(root))
        found = []
        if 'ACO ROLE BOOTSTRAP' not in text:
            found.append('missing shared bootstrap')
        if 'INTERACTION AND ACTION CONTRACT' in text or 'ACO OPERATING CONTRACT — applies to every role' in text:
            found.append('legacy duplicated contract remains')
        if len(text) > 9000:
            found.append('heavy role file (>9000 chars); review for duplicated or non-role-specific material')
        if not re.search(r'\*\*Description:\*\* .+', text):
            found.append('missing description')
        if not re.search(r'\b(outputs?|deliverables?|acceptance|handoff|evidence)\b', text, re.IGNORECASE):
            found.append('no obvious deliverable/acceptance/evidence section; human review recommended')
        if found:
            issues.append({'path': rel, 'issues': found})

    return {
        'status': 'review_required' if issues else 'clean',
        'aco_version': VERSION,
        'roles_scanned': len(roles),
        'issues': issues,
        'verdicts': ['Keep', 'Improve', 'Update', 'Merge', 'Retire'],
        'policy': 'This command never edits, merges or deletes roles. Merge/Retire decisions require exact replacement/impact review and explicit maintainer action.'
    }


def _default_eval_path() -> Path:
    candidates = [ROOT / 'config/evals.json', ROOT / 'config' / 'evals.json']
    for p in candidates:
        if p.is_file():
            return p
    raise ACOError('No eval definition found. Pass --input explicitly in an installed runtime.')


def eval_lint(path: Path | None = None) -> dict[str, Any]:
    path = (path or _default_eval_path()).expanduser().absolute()
    data = read_json(path)
    if data.get('schema_version') != 1:
        raise ACOError('Unsupported eval schema_version')
    cases = data.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ACOError('Eval definition needs a non-empty cases list')
    ids = set()
    errors = []
    for i, case in enumerate(cases):
        cid = case.get('id')
        if not isinstance(cid, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,63}', cid):
            errors.append(f'case {i}: invalid id')
        elif cid in ids:
            errors.append(f'duplicate id: {cid}')
        ids.add(cid)
        for key in ('office', 'prompt'):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f'{cid or i}: missing {key}')
        for key in ('must', 'must_not'):
            if not isinstance(case.get(key), list) or not case[key] or not all(isinstance(x, str) and x.strip() for x in case[key]):
                errors.append(f'{cid or i}: {key} must be a non-empty string list')
        if not isinstance(case.get('human_review'), bool):
            errors.append(f'{cid or i}: human_review must be boolean')
    if errors:
        raise ACOError('Eval definition invalid:\n' + '\n'.join(errors))
    return {
        'status': 'valid',
        'aco_version': VERSION,
        'path': str(path),
        'cases': len(cases),
        'human_review_cases': sum(1 for c in cases if c['human_review']),
        'note': 'Schema validation only. It does not run models or prove agent quality.'
    }


def eval_show(path: Path | None = None, office: str | None = None) -> dict[str, Any]:
    path = (path or _default_eval_path()).expanduser().absolute()
    eval_lint(path)
    data = read_json(path)
    cases = data['cases']
    if office:
        cases = [c for c in cases if c['office'] == office]
    return {
        'status': 'ready_for_evaluation',
        'aco_version': VERSION,
        'office': office,
        'cases': cases,
        'instructions': [
            'Run the same case against the baseline and candidate ACO versions with equivalent tools/context.',
            'Check deterministic must/must_not conditions first.',
            'Use human review where marked; do not replace artistic/design judgment with package tests.',
            'Record model/host/tool versions and any unavailable checks before comparing results.'
        ]
    }
