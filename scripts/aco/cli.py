from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from .common import ACOError, ROOT, VERSION, digest, private_root, read_json
from .memory import Memory  # Explicit legacy backend only.
from .compact import CompactMemory


def main() -> None:
    p = argparse.ArgumentParser(description='ACO: private records, safe installation and session handoffs. No background process.')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Check this environment without connecting to services')
    sub.add_parser('validate', help='Check library structure and release integrity')
    sub.add_parser('capability-audit', help='Locate known local commands; never execute them or inspect credentials')
    q = sub.add_parser('context-budget', help='Static ACO context/package-size audit; no runtime telemetry or writes')
    q.add_argument('--root', type=Path, help='ACO checkout or installed skills root; defaults to this release')
    q = sub.add_parser('role-stocktake', help='Read-only role quality/duplication scan; never merges or deletes')
    q.add_argument('--root', type=Path, help='ACO checkout or installed skills root; defaults to this release')
    q = sub.add_parser('eval-lint', help='Validate behavioral eval definitions; does not run a model')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('eval-show', help='Show behavioral eval cases for manual/model comparison')
    q.add_argument('--input', type=Path)
    q.add_argument('--office')
    q = sub.add_parser('eval-score', help='Score a recorded behavioral simulation/review; never invokes a model')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('route-suggest', help='Advisory office/role routing from local metadata; no actions or context writes')
    q.add_argument('--prompt', required=True)
    q.add_argument('--max-roles', type=int, default=3)
    q = sub.add_parser('route-benchmark', help='Run deterministic routing benchmark against packaged metadata')
    q.add_argument('--input', type=Path)
    q.add_argument('--root', type=Path)
    q.add_argument('--split', choices=['development','holdout'])
    q = sub.add_parser('role-contract', help='Show the generated structured contract for one canonical role')
    q.add_argument('--role', required=True)
    q.add_argument('--root', type=Path)
    q = sub.add_parser('role-overlap', help='Read-only lexical overlap review; never merges or retires roles')
    q.add_argument('--root', type=Path)
    q.add_argument('--threshold', type=float, default=0.62)
    q.add_argument('--limit', type=int, default=30)
    q = sub.add_parser('handoff-check', help='Validate a compact task handoff packet; no writes')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('capability-resolve', help='Resolve required capabilities against supplied availability/authorization evidence; no execution')
    q.add_argument('--request', type=Path, required=True)
    q.add_argument('--inventory', type=Path)
    q = sub.add_parser('execution-plan', help='Resolve capability + permission + retry state; never executes an adapter')
    q.add_argument('--request', type=Path, required=True)
    q.add_argument('--inventory', type=Path)
    q.add_argument('--approval', type=Path)
    q.add_argument('--previous', type=Path)
    q = sub.add_parser('permission-check', help='Check whether the exact action needs/has scoped approval; no execution')
    q.add_argument('--request', type=Path, required=True)
    q.add_argument('--approval', type=Path)
    q = sub.add_parser('receipt-check', help='Validate an execution receipt and its supported claim level')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('adapter-check', help='Validate caller-supplied host adapter metadata; reads no credentials')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('workflow-check', help='Validate execution/workflow state transitions; no persistence')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('execution-summary', help='Produce an operational summary from receipts; no hidden reasoning')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('execution-benchmark', help='Run deterministic v0.7 execution-policy conformance cases')
    q.add_argument('--input', type=Path)
    q.add_argument('--root', type=Path)
    q = sub.add_parser('delegation-resolve', help='Resolve whether delegated professional judgment should act, ask, or request approval')
    q.add_argument('--request', type=Path, required=True)
    q = sub.add_parser('delegation-benchmark', help='Run deterministic delegation-behavior conformance cases')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('memory-resolve', help='Route a memory need to durable, source, local-index or temporary storage without prompting for Drive')
    q.add_argument('--request', type=Path, required=True)
    q = sub.add_parser('context-plan', help='Plan minimum authorized context under NONE/BLIND/LIGHT/FULL/BLIND-FIRST; no retrieval or writes')
    q.add_argument('--request', type=Path, required=True)
    q = sub.add_parser('context-benchmark', help='Run deterministic context-scope and efficiency conformance cases')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('scope-boundary-benchmark', help='Run deterministic v0.7.3 exact private-scope boundary cases')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('real-world-benchmark', help='Run the packaged 120-scenario routing/context/memory regression benchmark')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('integration-resolve', help='Select a ready provider-neutral host adapter from caller-supplied current inventory; no execution')
    q.add_argument('--request', type=Path, required=True)
    q.add_argument('--inventory', type=Path)
    q = sub.add_parser('integration-benchmark', help='Run deterministic provider-neutral integration resolution conformance cases')
    q.add_argument('--input', type=Path)
    q = sub.add_parser('privacy-scan', help='Scan the release for likely personal/private data and credential leakage; read-only')
    q.add_argument('--root', type=Path)
    q = sub.add_parser('goal-check', help='Validate a Program → Goal → Task → Dependency graph; no writes')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('goal-status', help='Compute graph progress, blockers and deterministic next-best tasks; no writes')
    q.add_argument('--input', type=Path, required=True)
    q.add_argument('--as-of', help='ISO date/time used only for deterministic deadline ranking')
    q.add_argument('--limit', type=int, default=5)
    q = sub.add_parser('goal-transition', help='Apply one validated state transition in-memory and return the updated graph')
    q.add_argument('--graph', type=Path, required=True)
    q.add_argument('--event', type=Path, required=True)
    q = sub.add_parser('autonomy-plan', help='Choose next graph work and prepare bounded host actions; never calls providers')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('autonomy-benchmark', help='Run deterministic Goal Graph + Autonomy Engine conformance cases')
    q.add_argument('--input', type=Path)
    q.add_argument('--root', type=Path)
    q = sub.add_parser('feedback-check', help='Validate one structured adaptive feedback record; no persistence or learning')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('feedback-ledger-check', help='Validate a scope-bound append-only feedback ledger hash chain')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('feedback-append', help='Return a ledger with one validated feedback record appended; never persists it')
    q.add_argument('--ledger', type=Path, required=True)
    q.add_argument('--record', type=Path, required=True)
    q = sub.add_parser('adaptation-propose', help='Derive bounded shadow-only candidates from repeated scoped feedback')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('shadow-rank', help='Compare base Goal Graph ranking with shadow adaptive candidates; never mutates production state')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('promotion-check', help='Check exact-hash benchmark and approval evidence for candidate promotion eligibility; never activates it')
    q.add_argument('--input', type=Path, required=True)
    q = sub.add_parser('adaptive-benchmark', help='Run deterministic ACO 0.9 feedback/adaptation/promotion safety cases')
    q.add_argument('--input', type=Path)
    q.add_argument('--root', type=Path)
    q = sub.add_parser('bootstrap-resolve', help='Resolve aco://current without preloading the repository')
    q.add_argument('--root', type=Path)
    q.add_argument('--start', type=Path)
    q = sub.add_parser('bootstrap-check', help='Validate the ACO 1.0 bootstrap contract')
    q.add_argument('--root', type=Path)
    q = sub.add_parser('token-plan', help='Select maximum-value authorized context under a token target')
    q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('context-compile', help='Compile a minimal Task Capsule')
    q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-registry-check'); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-search'); q.add_argument('--query', default=''); q.add_argument('--tags', nargs='*'); q.add_argument('--limit', type=int, default=5); q.add_argument('--include-candidates', action='store_true'); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-resolve'); q.add_argument('--skill', required=True); q.add_argument('--allow-candidate', action='store_true'); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-candidate-check'); q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-learn'); q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-promotion-check'); q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('skill-candidate-store'); q.add_argument('--input', type=Path, required=True); q.add_argument('--state-root', type=Path); q.add_argument('--root', type=Path); q.add_argument('--apply', action='store_true')
    q = sub.add_parser('skill-candidate-store-status'); q.add_argument('--state-root', type=Path)
    q = sub.add_parser('skill-benchmark'); q.add_argument('--input', type=Path); q.add_argument('--root', type=Path)
    q = sub.add_parser('os-plan'); q.add_argument('--input', type=Path, required=True); q.add_argument('--root', type=Path)
    q = sub.add_parser('token-economy-benchmark'); q.add_argument('--input', type=Path); q.add_argument('--root', type=Path)
    q = sub.add_parser('os-benchmark'); q.add_argument('--input', type=Path); q.add_argument('--root', type=Path)
    for verb in ('practice-check', 'opportunity-check', 'brand-check', 'social-check'):
        q = sub.add_parser(verb, help='Offline studio readiness check, no writes or external actions')
        q.add_argument('--input', type=Path, required=True)
        if verb in ('opportunity-check', 'social-check'):
            q.add_argument('--as-of', help='ISO timestamp WITH timezone for reproducible checks')
    for verb in ('install', 'uninstall', 'install-status', 'install-recover'):
        q = sub.add_parser(verb)
        q.add_argument('--home', type=Path, help='Explicit home override, primarily for testing')
        q.add_argument('--project', type=Path, help='Install into this existing project instead of globally')
        q.add_argument('--codex-home', type=Path)
        if verb in ('install', 'uninstall'):
            q.add_argument('--apply', action='store_true', help='Execute; default is a dry run')
            q.add_argument('--backup-modified', action='store_true', help='Explicitly back up modified ACO-owned files before replacing/removing')
        if verb == 'install':
            q.add_argument('--offices', nargs='+', default=None, help='Native agent offices: artist-office agency-office ...; all or none. Skills always installed.')
    q = sub.add_parser('migrate', help='Replace only known ACO files in an existing clean Git checkout')
    q.add_argument('--target', type=Path, required=True)
    q.add_argument('--apply', action='store_true')
    q=sub.add_parser('intake', help='Offline early-question/brief check; does not execute the workflow')
    q.add_argument('--workflow', required=True)
    q.add_argument('--facts', type=Path, required=True)
    q.add_argument('--mode', choices=['ACTION','DECISION','EXPLAIN'], default='ACTION')
    q=sub.add_parser('action-plan', help='Check an external-action packet; never sends or calls')
    q.add_argument('--request', type=Path, required=True)
    q.add_argument('--capability', type=Path)
    q.add_argument('--authorization', type=Path)
    q.add_argument('--previous', type=Path)
    q=sub.add_parser('budget-check', help='Decimal project-estimate arithmetic; no payments or tax advice')
    q.add_argument('--input', type=Path, required=True)
    q=sub.add_parser('comfy-preflight', help='Offline API-prompt checks against a node-schema snapshot; never renders')
    q.add_argument('--workflow', type=Path, required=True)
    q.add_argument('--object-info', type=Path, required=True)
    for verb in ('web-contract-check', 'shot-plan-check', 'video-prompt-draft', 'evidence-check'):
        q=sub.add_parser(verb, help='Offline specialist contract/evidence check; never renders or submits')
        q.add_argument('--input', type=Path, required=True)
        if verb=='video-prompt-draft':
            q.add_argument('--capability', type=Path, required=True)
            q.add_argument('--as-of', help='Explicit ISO date for reproducible snapshot-freshness checks')
        if verb=='evidence-check': q.add_argument('--evidence-root', type=Path, required=True)
    q=sub.add_parser('resource-search',help='Find optional resources, not an installation command')
    q.add_argument('--query',default='');q.add_argument('--role');q.add_argument('--limit',type=int,default=3);q.add_argument('--include-unresolved',action='store_true')
    q=sub.add_parser('resource-plan',help='Offline readiness/permission plan; no external action')
    q.add_argument('--request',type=Path,required=True);q.add_argument('--inventory',type=Path);q.add_argument('--as-of')
    q=sub.add_parser('storage-plan',help='Decide chat, pipeline or eligible canonical document without writing')
    q.add_argument('--input',type=Path,required=True)
    q=sub.add_parser('tidy-inventory',help='Read-only private inventory; no deletion approvals inferred')
    q.add_argument('--root',type=Path,required=True)
    q=sub.add_parser('tidy-plan',help='Preview explicit reviewed consolidation')
    q.add_argument('--root',type=Path,required=True);q.add_argument('--spec',type=Path,required=True)
    q=sub.add_parser('tidy-apply',help='Apply a reviewed local plan with external backup, no permanent file deletion')
    q.add_argument('--root',type=Path,required=True);q.add_argument('--plan',type=Path,required=True);q.add_argument('--recovery-root',type=Path,required=True);q.add_argument('--approval-ref',required=True);q.add_argument('--approved-plan-id',required=True)
    q=sub.add_parser('tidy-restore',help='Restore verified sources from one cleanup batch')
    q.add_argument('--receipt',type=Path,required=True);q.add_argument('--approval-ref',required=True);q.add_argument('--rollback-target',action='store_true')
    commands = ('adopt-canonical','pipeline-upsert','pipeline-promote','compact-recent','workspace-init', 'entity-add', 'status', 'session-start', 'session-export',
                'checkpoint', 'session-close', 'context-propose', 'context-apply', 'drive-bind', 'drive-sync')
    for verb in commands:
        q = sub.add_parser(verb)
        q.add_argument('--knowledge', type=Path, default=private_root() / 'knowledge')
        q.add_argument('--legacy-memory',action='store_true',help='Explicitly opt into the old per-event/file layout. Never use for normal compact memory.')
        if verb=='adopt-canonical':
            q.add_argument('--canonical',required=True);q.add_argument('--kind',required=True,choices=['artist','career','organization']);q.add_argument('--key',required=True);q.add_argument('--name',required=True);q.add_argument('--base-sha256',required=True);q.add_argument('--approval-ref',required=True);q.add_argument('--authority',choices=['local','drive'],default='local')
        elif verb=='pipeline-upsert':
            q.add_argument('--entity',required=True);q.add_argument('--key',required=True);q.add_argument('--kind',required=True);q.add_argument('--title',required=True);q.add_argument('--state',default='exploring');q.add_argument('--summary',default='');q.add_argument('--next-action',default='');q.add_argument('--source',default='');q.add_argument('--base-sha256')
        elif verb=='pipeline-promote':
            q.add_argument('--entity',required=True);q.add_argument('--item',required=True);q.add_argument('--commitment',required=True,choices=['explicit_user','external_confirmed','existing_entity']);q.add_argument('--approval-ref',required=True);q.add_argument('--materialize',action='store_true');q.add_argument('--key');q.add_argument('--name');q.add_argument('--kind',default='project');q.add_argument('--reason',default='')
        elif verb=='compact-recent':
            q.add_argument('--entity',required=True);q.add_argument('--summary',required=True);q.add_argument('--base-sha256',required=True);q.add_argument('--approval-ref',required=True)
        if verb == 'workspace-init':
            q.add_argument('--authority', choices=['local', 'drive'], default='local')
        elif verb == 'entity-add':
            q.add_argument('--kind', required=True)
            q.add_argument('--key', required=True)
            q.add_argument('--name', required=True)
            q.add_argument('--parent')
            q.add_argument('--links', type=Path, help='JSON file with activity_ids/client_id/brand_id; projects only')
            q.add_argument('--commitment',choices=['explicit_user','external_confirmed','existing_entity']);q.add_argument('--approval-ref',default='');q.add_argument('--separate',action='store_true');q.add_argument('--reason',default='')
        elif verb == 'session-start':
            q.add_argument('--entity', required=True)
            q.add_argument('--workspace', type=Path, required=True)
            q.add_argument('--brief', required=True)
            q.add_argument('--mode', choices=['NONE', 'BLIND', 'LIGHT', 'FULL', 'BLIND-FIRST'], default='LIGHT')
            q.add_argument('--relationships', type=Path)
        elif verb == 'session-export':
            q.add_argument('--session', required=True)
            q.add_argument('--entities', nargs='+', required=True)
        elif verb == 'checkpoint':
            q.add_argument('--session', required=True)
            q.add_argument('--event', type=Path, required=True)
        elif verb == 'session-close':
            q.add_argument('--session', required=True)
        elif verb == 'context-propose':
            q.add_argument('--entity', required=True)
            q.add_argument('--content', type=Path, required=True)
            q.add_argument('--base-sha256', required=True)
            q.add_argument('--rationale', required=True)
        elif verb == 'context-apply':
            q.add_argument('--entity', required=True)
            q.add_argument('--proposal', required=True)
            q.add_argument('--approval-ref', required=True)
        elif verb == 'drive-bind':
            q.add_argument('--root-id', required=True)
            q.add_argument('--approval-ref', required=True)
        elif verb == 'drive-sync':
            q.add_argument('--session', help='Sync only this session; default all pending explicit events')
    a = p.parse_args()
    try:
        if a.command == 'doctor':
            result = {'aco_version': VERSION, 'python': platform.python_version(),
                      'platform': platform.system(), 'local_tools_supported': platform.system() in ('Linux', 'Darwin'),
                      'codex_executable_found': bool(shutil.which('codex')),
                      'git_executable_found': bool(shutil.which('git')),
                      'source_root': str(ROOT),
                      'drive_status': 'not_checked; configure connected tools separately',
                      'scope': 'environment checks only; not a host integration test'}
        elif a.command == 'capability-audit':
            from .readiness import capability_audit
            result = capability_audit()
        elif a.command in ('context-budget', 'role-stocktake', 'eval-lint', 'eval-show'):
            from .harness import context_budget, role_stocktake, eval_lint, eval_show
            if a.command == 'context-budget':
                result = context_budget(a.root)
            elif a.command == 'role-stocktake':
                result = role_stocktake(a.root)
            elif a.command == 'eval-lint':
                result = eval_lint(a.input)
            else:
                result = eval_show(a.input, a.office)
        elif a.command == 'eval-score':
            from .quality import score_simulation
            result = score_simulation(a.input)
        elif a.command in ('route-suggest','route-benchmark','role-contract','role-overlap'):
            from .routing import suggest_route, route_benchmark, role_contract, role_overlap
            if a.command == 'route-suggest':
                result = suggest_route(a.prompt, max_roles=a.max_roles)
            elif a.command == 'route-benchmark':
                result = route_benchmark(a.input, root=a.root, split=a.split)
            elif a.command == 'role-contract':
                result = role_contract(a.role, root=a.root)
            else:
                result = role_overlap(root=a.root, threshold=a.threshold, limit=a.limit)
        elif a.command == 'handoff-check':
            from .quality import handoff_check
            result = handoff_check(read_json(a.input))
        elif a.command == 'capability-resolve':
            from .quality import capability_resolve
            result = capability_resolve(read_json(a.request), read_json(a.inventory) if a.inventory else None)
        elif a.command in ('execution-plan','permission-check','receipt-check','adapter-check','workflow-check','execution-summary','execution-benchmark'):
            from .execution import execution_plan, permission_check, receipt_check, adapter_check, workflow_check, execution_summary, execution_benchmark
            if a.command == 'execution-plan':
                result = execution_plan(read_json(a.request), read_json(a.inventory) if a.inventory else None,
                                        read_json(a.approval) if a.approval else None,
                                        read_json(a.previous) if a.previous else None)
            elif a.command == 'permission-check':
                result = permission_check(read_json(a.request), read_json(a.approval) if a.approval else None)
            elif a.command == 'receipt-check':
                result = receipt_check(read_json(a.input))
            elif a.command == 'adapter-check':
                result = adapter_check(read_json(a.input))
            elif a.command == 'workflow-check':
                result = workflow_check(read_json(a.input))
            elif a.command == 'execution-summary':
                result = execution_summary(read_json(a.input))
            else:
                result = execution_benchmark(a.input, a.root)
        elif a.command == 'delegation-resolve':
            from .delegation import resolve_delegation
            result = resolve_delegation(read_json(a.request))
        elif a.command == 'delegation-benchmark':
            from .delegation import delegation_benchmark
            result = delegation_benchmark(a.input)
        elif a.command == 'memory-resolve':
            from .hybrid import memory_resolve
            result = memory_resolve(read_json(a.request))
        elif a.command == 'context-plan':
            from .context import context_plan
            result = context_plan(read_json(a.request))
        elif a.command in ('context-benchmark','scope-boundary-benchmark','real-world-benchmark'):
            from .efficiency import context_benchmark, scope_boundary_benchmark, real_world_benchmark
            if a.command == 'context-benchmark':
                result = context_benchmark(a.input)
            elif a.command == 'scope-boundary-benchmark':
                result = scope_boundary_benchmark(a.input)
            else:
                result = real_world_benchmark(a.input)
        elif a.command == 'integration-resolve':
            from .integrations import integration_resolve
            result = integration_resolve(read_json(a.request), read_json(a.inventory) if a.inventory else None)
        elif a.command == 'integration-benchmark':
            from .integrations import integration_benchmark
            result = integration_benchmark(a.input)
        elif a.command == 'privacy-scan':
            from .privacy import privacy_scan
            result = privacy_scan(a.root)
        elif a.command in ('goal-check','goal-status','goal-transition'):
            from .goals import goal_graph_check, goal_graph_status, goal_transition
            if a.command == 'goal-check':
                result = goal_graph_check(read_json(a.input))
            elif a.command == 'goal-status':
                result = goal_graph_status(read_json(a.input), as_of=a.as_of, limit=a.limit)
            else:
                result = goal_transition(read_json(a.graph), read_json(a.event))
        elif a.command in ('autonomy-plan','autonomy-benchmark'):
            from .autonomy import autonomy_plan, autonomy_benchmark
            if a.command == 'autonomy-plan':
                result = autonomy_plan(read_json(a.input))
            else:
                result = autonomy_benchmark(a.input, a.root)
        elif a.command in ('feedback-check','feedback-ledger-check','feedback-append','adaptation-propose','shadow-rank','promotion-check','adaptive-benchmark'):
            from .adaptive import feedback_record_check, feedback_ledger_check, feedback_append, adaptation_propose, shadow_rank, promotion_check, adaptive_benchmark
            if a.command == 'feedback-check':
                result = feedback_record_check(read_json(a.input))
            elif a.command == 'feedback-ledger-check':
                result = feedback_ledger_check(read_json(a.input))
            elif a.command == 'feedback-append':
                result = feedback_append(read_json(a.ledger), read_json(a.record))
            elif a.command == 'adaptation-propose':
                result = adaptation_propose(read_json(a.input))
            elif a.command == 'shadow-rank':
                result = shadow_rank(read_json(a.input))
            elif a.command == 'promotion-check':
                result = promotion_check(read_json(a.input))
            else:
                result = adaptive_benchmark(a.input, a.root)
        elif a.command in ('bootstrap-resolve','bootstrap-check'):
            from .bootstrap import resolve_runtime, bootstrap_check
            result = resolve_runtime(explicit_root=a.root, start=getattr(a,'start',None)) if a.command=='bootstrap-resolve' else bootstrap_check(a.root)
        elif a.command in ('token-plan','context-compile'):
            if a.command=='token-plan':
                from .token_budget import token_plan; result=token_plan(read_json(a.input),a.root)
            else:
                from .context_compiler import compile_context; result=compile_context(read_json(a.input),a.root)
        elif a.command in ('skill-registry-check','skill-search','skill-resolve','skill-candidate-check','skill-learn','skill-promotion-check','skill-candidate-store','skill-candidate-store-status','skill-benchmark'):
            from .skills import skill_registry_check, skill_search, skill_resolve, skill_candidate_check, skill_learn, skill_promotion_check, skill_candidate_store, skill_candidate_store_status, skill_benchmark
            if a.command=='skill-registry-check': result=skill_registry_check(a.root)
            elif a.command=='skill-search': result=skill_search(a.query,tags=a.tags,limit=a.limit,include_candidates=a.include_candidates,root=a.root)
            elif a.command=='skill-resolve': result=skill_resolve(a.skill,allow_candidate=a.allow_candidate,root=a.root)
            elif a.command=='skill-candidate-check': result=skill_candidate_check(read_json(a.input),a.root)
            elif a.command=='skill-learn': result=skill_learn(read_json(a.input),a.root)
            elif a.command=='skill-promotion-check': result=skill_promotion_check(read_json(a.input),a.root)
            elif a.command=='skill-candidate-store': result=skill_candidate_store(read_json(a.input),state_root=a.state_root,apply=a.apply,root=a.root)
            elif a.command=='skill-candidate-store-status': result=skill_candidate_store_status(state_root=a.state_root)
            else: result=skill_benchmark(a.input,a.root)
        elif a.command=='os-plan':
            from .kernel import os_plan; result=os_plan(read_json(a.input),a.root)
        elif a.command in ('token-economy-benchmark','os-benchmark'):
            from .os_benchmark import token_economy_benchmark, os_benchmark
            result=token_economy_benchmark(a.input,a.root) if a.command=='token-economy-benchmark' else os_benchmark(a.input,a.root)
        elif a.command in ('practice-check', 'opportunity-check', 'brand-check', 'social-check'):
            from .readiness import practice_check, opportunity_check, brand_check, social_check, _dt
            fn = {'practice-check': practice_check, 'opportunity-check': opportunity_check, 'brand-check': brand_check, 'social-check': social_check}[a.command]
            extra = {}
            if hasattr(a, 'as_of') and a.as_of:
                extra['as_of'] = _dt(a.as_of, 'as_of')
            result = fn(read_json(a.input), **extra)
        elif a.command == 'validate':
            if not (ROOT / 'catalog.json').exists():
                raise ACOError('Run validation from the complete ACO release checkout, not the installed minimal runtime.')
            from .validate import validate
            result = validate()
        elif a.command=='resource-search':
            from .resources import search_resources
            result=search_resources(a.query,a.role,a.limit,a.include_unresolved)
        elif a.command=='resource-plan':
            from .resources import resource_plan
            from datetime import date
            result=resource_plan(read_json(a.request),read_json(a.inventory) if a.inventory else None,date.fromisoformat(a.as_of) if a.as_of else None)
        elif a.command=='storage-plan':
            from .compact import storage_decision
            result=storage_decision(read_json(a.input))
        elif a.command.startswith('tidy-'):
            from .tidy import inventory,consolidation_plan,apply_plan,restore
            if a.command=='tidy-inventory':result=inventory(a.root)
            elif a.command=='tidy-plan':result=consolidation_plan(a.root,read_json(a.spec))
            elif a.command=='tidy-apply':
                plan=read_json(a.plan);plan=plan.get('plan',plan)
                result=apply_plan(a.root,plan,a.recovery_root,a.approval_ref,a.approved_plan_id)
            else:result=restore(a.receipt,a.approval_ref,a.rollback_target)
        elif a.command == 'intake':
            from .planning import intake
            result=intake(a.workflow,read_json(a.facts),mode=a.mode)
        elif a.command == 'action-plan':
            from .planning import plan_action
            result=plan_action(read_json(a.request),read_json(a.capability) if a.capability else None,
                               read_json(a.authorization) if a.authorization else None,
                               read_json(a.previous) if a.previous else None)
        elif a.command == 'budget-check':
            from .finance import budget_check
            result=budget_check(read_json(a.input))
        elif a.command == 'comfy-preflight':
            from .production import comfy_preflight
            result=comfy_preflight(read_json(a.workflow),read_json(a.object_info))
        elif a.command in ('web-contract-check', 'shot-plan-check', 'video-prompt-draft', 'evidence-check'):
            from .specialist import web_contract_check, shot_plan_check, video_prompt_draft, evidence_check
            if a.command=='web-contract-check': result=web_contract_check(read_json(a.input))
            elif a.command=='shot-plan-check': result=shot_plan_check(read_json(a.input))
            elif a.command=='video-prompt-draft':
                from datetime import date
                result=video_prompt_draft(read_json(a.input),read_json(a.capability),date.fromisoformat(a.as_of) if a.as_of else None)
            else: result=evidence_check(read_json(a.input),a.evidence_root)
        elif a.command.startswith('install') or a.command == 'uninstall':
            if not (ROOT / 'catalog.json').exists():
                raise ACOError('Run installation/update commands from the complete ACO release checkout, not the installed minimal runtime.')
            from .install import Installer
            home = a.codex_home
            if home is None and a.home is None and a.project is None and os.environ.get('CODEX_HOME'):
                home = Path(os.environ['CODEX_HOME'])
            i = Installer(a.home, a.project, home)
            if a.command == 'install':
                result = i.install(a.offices, a.apply, a.backup_modified)
            elif a.command == 'uninstall':
                result = i.uninstall(a.apply, a.backup_modified)
            elif a.command == 'install-recover':
                result = i.recover()
            else:
                result = i.status()
        elif a.command == 'migrate':
            if not (ROOT / 'catalog.json').exists():
                raise ACOError('Run migration from the complete ACO release checkout, not the installed minimal runtime.')
            from .migrate import migrate
            result = migrate(a.target, a.apply)
        else:
            m = Memory(a.knowledge) if a.legacy_memory else CompactMemory(a.knowledge)
            if a.legacy_memory and a.command in ('adopt-canonical','pipeline-upsert','pipeline-promote','compact-recent'):raise ACOError('This command requires compact memory; no implicit migration.')
            if a.command=='adopt-canonical':
                result=m.adopt(a.canonical,a.kind,a.key,a.name,a.base_sha256,a.approval_ref,a.authority)
            elif a.command == 'workspace-init':
                result = m.init(a.authority)
            elif a.command == 'entity-add':
                extra={} if a.legacy_memory else dict(commitment=a.commitment,approval_ref=a.approval_ref,separate=a.separate,reason=a.reason)
                result = m.add_entity(a.kind, a.key, a.name, a.parent, read_json(a.links) if a.links else None,**extra)
            elif a.command=='pipeline-upsert':
                result=m.pipeline_upsert(a.entity,a.key,a.kind,a.title,a.state,a.summary,a.next_action,a.source,a.base_sha256)
            elif a.command=='pipeline-promote':
                result=m.promote(a.entity,a.item,a.commitment,a.approval_ref,materialize=a.materialize,key=a.key,name=a.name,kind=a.kind,reason=a.reason)
            elif a.command=='compact-recent':
                result=m.compact_recent(a.entity,a.summary,a.base_sha256,a.approval_ref)
            elif a.command == 'status':
                result = m.status()
            elif a.command == 'session-start':
                result = m.start(a.entity, a.brief, a.workspace, a.mode, read_json(a.relationships) if a.relationships else None)
            elif a.command == 'session-export':
                result = m.export_context(a.session, a.entities)
            elif a.command == 'checkpoint':
                result = m.checkpoint(a.session, read_json(a.event))
            elif a.command == 'session-close':
                result = m.close(a.session)
            elif a.command == 'context-propose':
                result = m.propose_context(a.entity, a.content.read_text(), a.base_sha256, a.rationale)
            elif a.command == 'context-apply':
                result = m.apply_context(a.entity, a.proposal, a.approval_ref)
            elif a.command in ('drive-bind', 'drive-sync'):
                if not a.legacy_memory:raise ACOError('Compact mode updates canonical Drive documents through the host connected-tool protocol. The old per-event bridge is disabled by default. Do not create session/event folders. See docs/COMPACT-MEMORY.md.')
                from .drive import DriveBridge, DriveREST
                bridge = DriveBridge(m, DriveREST())
                result = bridge.bind(a.root_id, a.approval_ref) if a.command == 'drive-bind' else bridge.sync(a.session)
            else:
                raise ACOError('Unsupported command')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if a.command in ('comfy-preflight','web-contract-check','shot-plan-check','video-prompt-draft','evidence-check') and (result.get('errors') or result.get('missing')):
            sys.exit(2)
    except (ACOError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
