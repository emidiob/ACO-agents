from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from .common import ACOError, ROOT, VERSION, digest, private_root, read_json
from .memory import Memory


def main() -> None:
    p = argparse.ArgumentParser(description='ACO: private records, safe installation and session handoffs. No background process.')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Check this environment without connecting to services')
    sub.add_parser('validate', help='Check library structure and release integrity')
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
    commands = ('workspace-init', 'entity-add', 'status', 'session-start', 'session-export',
                'checkpoint', 'session-close', 'context-propose', 'context-apply', 'drive-bind', 'drive-sync')
    for verb in commands:
        q = sub.add_parser(verb)
        q.add_argument('--knowledge', type=Path, default=private_root() / 'knowledge')
        if verb == 'workspace-init':
            q.add_argument('--authority', choices=['local', 'drive'], default='local')
        elif verb == 'entity-add':
            q.add_argument('--kind', required=True)
            q.add_argument('--key', required=True)
            q.add_argument('--name', required=True)
            q.add_argument('--parent')
            q.add_argument('--links', type=Path, help='JSON file with activity_ids/client_id/brand_id; projects only')
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
        elif a.command == 'validate':
            if not (ROOT / 'catalog.json').exists():
                raise ACOError('Run validation from the complete ACO release checkout, not the installed minimal runtime.')
            from .validate import validate
            result = validate()
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
            m = Memory(a.knowledge)
            if a.command == 'workspace-init':
                result = m.init(a.authority)
            elif a.command == 'entity-add':
                result = m.add_entity(a.kind, a.key, a.name, a.parent, read_json(a.links) if a.links else None)
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
                from .drive import DriveBridge, DriveREST
                bridge = DriveBridge(m, DriveREST())
                result = bridge.bind(a.root_id, a.approval_ref) if a.command == 'drive-bind' else bridge.sync(a.session)
            else:
                raise ACOError('Unsupported command')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ACOError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
