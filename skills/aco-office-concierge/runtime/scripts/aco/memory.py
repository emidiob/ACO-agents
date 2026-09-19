"""Local, private, crash-recoverable ACO records and session handoffs.

This is a filesystem backend, not a background agent. Drive operations use the
separate connected-tool protocol or the explicitly configured event bridge.
"""
from __future__ import annotations
import copy
import json
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any
from .common import (ACOError, Conflict, ROOT, VERSION, atomic_write, digest,
                     ensure_file, json_bytes, key_ok, lock, no_symlinks, now,
                     read_json, safe_path, uid, under_git, write_json)

KINDS = {'organization', 'artist', 'career', 'activity', 'client', 'brand', 'project', 'matter'}
OWNER_KINDS = {'organization', 'artist', 'career'}
ALLOWED_PARENTS = {
    'organization': {None}, 'artist': {None}, 'career': {None},
    'activity': {'organization'}, 'client': {'organization'},
    'brand': {'organization', 'client'}, 'project': OWNER_KINDS,
    'matter': OWNER_KINDS | {'client', 'project'},
}
GROUPS = {'organization': 'Organizations', 'artist': 'Personal/Artists',
          'career': 'Personal/Careers', 'activity': 'Activities', 'client': 'Clients',
          'brand': 'Brands', 'project': 'Projects', 'matter': 'Matters'}
TEMPLATES = {'organization': 'COMPANY', 'artist': 'ARTIST', 'career': 'CAREER',
             'activity': 'ACTIVITY', 'client': 'CLIENT', 'brand': 'BRAND',
             'project': 'PROJECT', 'matter': 'LEGAL-MATTER'}
MODES = {'NONE', 'BLIND', 'LIGHT', 'FULL', 'BLIND-FIRST'}
EVENT_KINDS = {'work', 'proposal', 'decision', 'open_loop', 'context_change',
               'verification', 'handoff', 'application', 'status'}
STATES = {'proposed', 'approved', 'executed', 'verified', 'rejected', 'superseded', 'open', 'closed'}

class Memory:
    def __init__(self, root: Path):
        self.root = Path(root).expanduser().absolute()
        no_symlinks(self.root)
        if self.root == ROOT or self.root.is_relative_to(ROOT):
            raise ACOError('Private knowledge must not be inside the public ACO library.')
        self.system = self.root / '00-System'
        self.registry_path = self.system / 'REGISTRY.json'

    def _lock(self):
        return lock(self.root / '.aco.lock')

    def init(self, authority: str = 'local') -> dict:
        if authority not in {'local', 'drive'}:
            raise ACOError('Authority must be local or drive.')
        if under_git(self.root):
            raise ACOError('Choose a private knowledge folder outside a Git checkout. Handoffs are separate.')
        marker = self.root / '.aco-knowledge.json'
        if self.root.exists() and not marker.exists():
            visible = [p for p in self.root.iterdir() if p.name != '.aco.lock']
            if visible:
                raise Conflict('Nonempty unrecognized knowledge folder. Use the documented legacy migration; do not reset it.')
        with self._lock():
            ensure_file(marker, json_bytes({'schema_version': 1, 'kind': 'aco-private-knowledge'}))
            if self.registry_path.exists():
                registry = self.registry()
                if registry['authority'] != authority:
                    raise Conflict('Authority cannot be switched silently. Use a reviewed migration.')
            else:
                registry = {'schema_version': 1, 'aco_version': VERSION,
                            'namespace': str(uuid.uuid4()), 'authority': authority,
                            'created_at': now(), 'entities': {}}
                write_json(self.registry_path, registry)
            for folder in ('00-System/Entities', '00-System/Outbox', '00-System/Receipts',
                           '00-System/Sync', 'Personal', 'Organizations', 'Archive'):
                safe_path(self.root, folder).mkdir(parents=True, exist_ok=True)
            ensure_file(self.root / 'KNOWLEDGE-INDEX.md', (
                '# ACO — Art & Commerce Office\n\n'
                'Private knowledge. Canonical machine index: `00-System/REGISTRY.json`.\n'
                'Every entity has its own context and history; no global current client.\n'
                'Names are labels. Entity IDs, session IDs and explicit file references resolve identity.\n'
                'Do not publish this directory.\n').encode())
            # Entities are journaled before registry updates; replay after an interrupted write.
            for p in sorted((self.system / 'Entities').glob('*.json')):
                entity = read_json(p)
                old = registry['entities'].get(entity['id'])
                if old is not None and old != entity:
                    raise Conflict(f'Entity journal mismatch: {entity["id"]}')
                registry['entities'][entity['id']] = entity
            write_json(self.registry_path, registry)
            return {'status': 'ready', 'authority': authority, 'root': str(self.root),
                    'entities': len(registry['entities']), 'persistence': 'local_verified'}

    def registry(self) -> dict:
        r = read_json(self.registry_path)
        if r.get('schema_version') != 1 or not isinstance(r.get('entities'), dict):
            raise ACOError('Unsupported or damaged registry. Preserve it and restore/reconcile; do not overwrite.')
        return r

    def entity(self, entity_id: str, registry: dict | None = None) -> dict:
        r = registry or self.registry()
        if entity_id not in r['entities']:
            raise ACOError(f'Unknown entity ID: {entity_id}')
        return r['entities'][entity_id]

    def _owner(self, entity: dict, registry: dict) -> str:
        visited = set()
        while entity['kind'] not in OWNER_KINDS:
            if entity['id'] in visited:
                raise Conflict('Cyclic entity parents')
            visited.add(entity['id'])
            entity = self.entity(entity['parent_id'], registry)
        return entity['id']

    def add_entity(self, kind: str, key: str, name: str, parent_id: str | None = None,
                   links: dict | None = None) -> dict:
        if kind not in KINDS or not name.strip():
            raise ACOError('A supported entity kind and nonempty name are required.')
        key_ok(key)
        links = links or {}
        if set(links) - {'activity_ids', 'client_id', 'brand_id'}:
            raise ACOError('Unknown relationship field')
        if links and kind != 'project':
            raise ACOError('Activity/client/brand links belong to projects.')
        with self._lock():
            r = self.registry()
            parent = self.entity(parent_id, r) if parent_id else None
            if (parent['kind'] if parent else None) not in ALLOWED_PARENTS[kind]:
                raise ACOError(f'Invalid parent for {kind}')
            identity = f'{kind}/{parent_id or "root"}/{key}'
            eid = kind + '-' + uuid.uuid5(uuid.UUID(r['namespace']), identity).hex
            if eid in r['entities']:
                old = r['entities'][eid]
                if old['name'] != name.strip() or old.get('links', {}) != links:
                    raise Conflict('This stable key already exists with different data. Reuse its ID or explicitly revise it.')
                return {'status': 'existing', 'entity': old, 'persistence': 'local_verified'}
            base = Path(parent['path']) / GROUPS[kind] if parent else Path(GROUPS[kind])
            relative = (base / (key + '--' + eid[-8:])).as_posix()
            ent = {'id': eid, 'kind': kind, 'key': key, 'name': name.strip(),
                   'parent_id': parent_id, 'path': relative, 'links': links,
                   'created_at': now()}
            temp = copy.deepcopy(r)
            temp['entities'][eid] = ent
            owner = self._owner(ent, temp)
            ent['owner_id'] = owner
            self.validate_scope({'entity_id': eid, **links}, temp)
            folder = safe_path(self.root, relative)
            for d in ('History/Events', 'History/Sessions', 'History/Proposals', 'History/ContextVersions', 'Handoffs'):
                (folder / d).mkdir(parents=True, exist_ok=True)
            for fn, title in [('WORK-LOG.md', 'Work log'), ('DECISIONS.md', 'Decisions'),
                              ('OPEN-LOOPS.md', 'Open loops'), ('CONTEXT-CHANGELOG.md', 'Context changelog')]:
                ensure_file(folder / 'History' / fn, (
                    f'# {title}\n\nEvents are canonical in `Events/`. This file is a generated view.\n').encode())
            template = ROOT / 'assets/context-templates' / f'{TEMPLATES[kind]}-CONTEXT.template.md'
            body = template.read_text(encoding='utf-8') if template.exists() else '# Context\n\n## Facts\n\n## Open questions\n'
            ensure_file(folder / 'Context.md', (
                f'<!-- ACO entity: {eid}; no assumed facts beyond user-supplied identity. -->\n'
                f'Name: {name.strip()}\n\n' + body).encode())
            # A fixed journal entry allows recovery if the process stops before registry save.
            write_json(self.system / 'Entities' / f'{eid}.json', ent)
            r['entities'][eid] = ent
            write_json(self.registry_path, r)
            return {'status': 'created', 'entity': ent, 'persistence': 'local_verified'}

    def validate_scope(self, scope: dict, registry: dict | None = None) -> dict:
        r = registry or self.registry()
        if set(scope) - {'entity_id', 'activity_ids', 'client_id', 'brand_id'}:
            raise ACOError('Unsupported scope fields')
        ent = self.entity(scope.get('entity_id', ''), r)
        owner_id = self._owner(ent, r)
        expected = {'client_id': 'client', 'brand_id': 'brand'}
        result = copy.deepcopy(scope)
        # Project-linked relationships are locked to the canonical project record.
        for k, v in ent.get('links', {}).items():
            if k in result and result[k] != v:
                raise Conflict(f'Session {k} conflicts with the project relationship')
            result[k] = v
        ids = result.get('activity_ids', [])
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            raise ACOError('activity_ids must be a list of IDs')
        for ref in ids:
            obj = self.entity(ref, r)
            if obj['kind'] != 'activity' or self._owner(obj, r) != owner_id:
                raise Conflict('An activity belongs to another organization or is not an activity')
        for field, kind in expected.items():
            if result.get(field):
                obj = self.entity(result[field], r)
                if obj['kind'] != kind or self._owner(obj, r) != owner_id:
                    raise Conflict(f'{field} belongs to another owner or has the wrong type')
        if result.get('brand_id'):
            brand = self.entity(result['brand_id'], r)
            bp = self.entity(brand['parent_id'], r)
            if bp['kind'] == 'client':
                if result.get('client_id') not in (None, bp['id']):
                    raise Conflict('Brand and client do not match')
                result['client_id'] = bp['id']
        if ent['kind'] == 'client' and result.get('client_id') not in (None, ent['id']):
            raise Conflict('Client scope cannot switch to another client')
        return {'entity_id': ent['id'], 'owner_id': owner_id,
                **{k: v for k, v in result.items() if k != 'entity_id'}}

    def _session_path(self, session_id: str) -> Path:
        if not re.fullmatch(r'session-[0-9a-f]{32}', session_id):
            raise ACOError('Invalid session ID')
        r = self.registry()
        found = []
        for ent in r['entities'].values():
            p = safe_path(self.root, ent['path']) / 'History/Sessions' / (session_id + '.json')
            if p.exists():
                found.append(p)
        if len(found) != 1:
            raise ACOError(f'Session not found unambiguously: {session_id}')
        return found[0]

    def start(self, entity_id: str, brief: str, workspace: Path, mode: str = 'LIGHT',
              relationships: dict | None = None) -> dict:
        if mode not in MODES or not brief.strip():
            raise ACOError('Valid context mode and nonempty brief required')
        workspace = workspace.expanduser().absolute()
        no_symlinks(workspace)
        if not workspace.is_dir():
            raise ACOError('Workspace must be an existing project directory')
        if workspace == ROOT or workspace.is_relative_to(ROOT):
            raise ACOError('Use a separate work-project folder, not the public ACO source repository.')
        with self._lock():
            r = self.registry()
            scope = self.validate_scope({'entity_id': entity_id, **(relationships or {})}, r)
            ent = self.entity(entity_id, r)
            # Ignore rules never untrack existing files. Fail before writing any private packet.
            gp = subprocess.run(['git', '-C', str(workspace), 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True) if __import__('shutil').which('git') else None
            if gp is not None and gp.returncode == 0:
                top = Path(gp.stdout.strip())
                relative = workspace.relative_to(top).as_posix()
                prefix = '' if relative == '.' else relative + '/'
                check = subprocess.run(['git', '-C', str(top), 'ls-files', '-z', '--',
                                        prefix + '.agent-context', prefix + '.aco-binding.json'], capture_output=True)
                if check.returncode or check.stdout:
                    raise Conflict('Private ACO paths are already tracked by Git. Remove them from tracking after review before writing a handoff.')
            # Ignore handoffs before creating them. Preserve an existing .gitignore verbatim.
            ignore = workspace / '.gitignore'
            no_symlinks(ignore)
            text = ignore.read_text() if ignore.exists() else ''
            rules = ['.agent-context/', '.aco-binding.json', '.aco-install/']
            missing = [rule for rule in rules if rule not in text.splitlines()]
            if missing:
                atomic_write(ignore, (text.rstrip() + '\n\n# ACO private session files\n' + '\n'.join(missing) + '\n').encode(), 0o644)
            sid = uid('session')
            local = safe_path(workspace, f'.agent-context/sessions/{sid}')
            local.mkdir(parents=True, exist_ok=True)
            record = {'schema_version': 1, 'id': sid, 'aco_version': VERSION,
                      'created_at': now(), 'scope': scope, 'context_mode': mode,
                      'brief': brief, 'workspace': str(workspace),
                      'handoff_dir': str(local), 'status': 'open', 'context_sources': []}
            write_json(safe_path(self.root, ent['path']) / 'History/Sessions' / f'{sid}.json', record)
            write_json(local / 'SESSION.json', record)
            atomic_write(local / 'CURRENT-BRIEF.md', ('# Current brief\n\n' + brief + '\n').encode())
            atomic_write(local / 'RELEVANT-CONTEXT.md', (
                '# Relevant context\n\nNo private context has been exported. '
                'Import only explicit scope-approved files; BLIND does not erase prior conversation content.\n').encode())
            self._render_session(record)
            return {'status': 'started', 'session': record, 'persistence': 'local_verified'}

    def export_context(self, session_id: str, entity_ids: list[str]) -> dict:
        with self._lock():
            sp = self._session_path(session_id)
            s = read_json(sp)
            if s['status'] != 'open':
                raise Conflict('Session is closed')
            if s['context_mode'] in {'NONE', 'BLIND', 'BLIND-FIRST'}:
                raise Conflict('Blind pass cannot read private context. Start a second contextualized session explicitly.')
            r = self.registry()
            scope = s['scope']
            # Not every same-owner client is allowed: only the task and its explicit relationships/ancestors.
            allowed = {scope['entity_id'], scope['owner_id'], *scope.get('activity_ids', [])}
            allowed.update(x for x in (scope.get('client_id'), scope.get('brand_id')) if x)
            ent = self.entity(scope['entity_id'], r)
            while ent.get('parent_id'):
                allowed.add(ent['parent_id'])
                ent = self.entity(ent['parent_id'], r)
            if set(entity_ids) - allowed:
                raise Conflict('Context export contains an entity outside this session scope')
            chunks, sources = [], []
            for eid in dict.fromkeys(entity_ids):
                ent = self.entity(eid, r)
                path = safe_path(self.root, ent['path']) / 'Context.md'
                no_symlinks(path)
                data = path.read_bytes()
                chunks.append(f'## {ent["name"]} ({eid})\n\n' + data.decode())
                sources.append({'entity_id': eid, 'sha256': digest(data), 'read_at': now()})
            local = Path(s['handoff_dir'])
            atomic_write(local / 'RELEVANT-CONTEXT.md', ('# Task-scoped context\n\n' + '\n\n'.join(chunks)).encode())
            s['context_sources'] = sources
            write_json(sp, s)
            write_json(local / 'SESSION.json', s)
            return {'status': 'exported', 'sources': sources, 'persistence': 'local_verified'}

    def checkpoint(self, session_id: str, entry: dict) -> dict:
        with self._lock():
            sp = self._session_path(session_id)
            s = read_json(sp)
            if s['status'] != 'open':
                raise Conflict('Closed session: start a new one for further work')
            e = copy.deepcopy(entry)
            unknown = set(e) - {'id', 'kind', 'status', 'summary', 'evidence', 'approval_ref',
                                'artifacts', 'tests', 'next_action', 'supersedes', 'loop_id'}
            if unknown:
                raise ACOError(f'Unknown event fields: {sorted(unknown)}')
            if e.get('kind') not in EVENT_KINDS or e.get('status') not in STATES or not e.get('summary', '').strip():
                raise ACOError('Event needs kind, status and nonempty summary')
            if e['kind'] == 'decision' and e['status'] == 'approved' and not e.get('approval_ref'):
                raise ACOError('Approved decisions require a reference to user approval')
            if e['status'] in {'verified', 'executed'} and not e.get('evidence'):
                raise ACOError('Executed/verified events require evidence, not just a claim')
            if e.get('supersedes') and not re.fullmatch(r'event-[a-z0-9_-]{1,80}', e['supersedes']):
                raise ACOError('Invalid superseded event ID')
            if e['kind'] == 'open_loop' and not e.get('loop_id'):
                raise ACOError('Open-loop events require a stable loop_id')
            for field in ('artifacts', 'tests'):
                if field in e and not isinstance(e[field], list):
                    raise ACOError(f'{field} must be a list')
            eid = e.setdefault('id', uid('event'))
            if not re.fullmatch(r'event-[a-z0-9_-]{1,80}', eid):
                raise ACOError('Invalid event ID')
            e.update({'schema_version': 1, 'session_id': session_id,
                      'scope': s['scope'], 'aco_version': VERSION})
            entity = self.entity(s['scope']['entity_id'])
            target = safe_path(self.root, entity['path']) / 'History/Events' / f'{eid}.json'
            # The outbox is global by ID, so reject reuse in another scope/session.
            outbox = self.system / 'Outbox' / f'{eid}.json'
            old_path = target if target.exists() else (outbox if outbox.exists() else None)
            if old_path:
                old = read_json(old_path)
                compared = {k: v for k, v in old.items() if k not in ('created_at', 'entity_sequence')}
                if compared != e:
                    raise Conflict('Event ID already exists with different content')
                e = old
            else:
                e['created_at'] = now()
                e['entity_sequence'] = max([x.get('entity_sequence', 0) for x in self.events(entity)] + [0]) + 1
            if e.get('supersedes'):
                previous = target.parent / (e['supersedes'] + '.json')
                if not previous.is_file():
                    raise Conflict('Superseded event is not present in this entity history')
            write_json(target, e)
            write_json(outbox, e)
            self._render_history(entity)
            self._render_session(s)
            return {'status': 'recorded', 'event_id': eid, 'session_id': session_id,
                    'persistence': 'local_verified', 'drive_status': 'pending'}

    def events(self, entity: dict, session_id: str | None = None) -> list[dict]:
        directory = safe_path(self.root, entity['path']) / 'History/Events'
        entries = [read_json(p) for p in directory.glob('*.json')]
        return sorted((e for e in entries if session_id is None or e['session_id'] == session_id),
                      key=lambda e: (e.get('entity_sequence', 0), e['created_at'], e['id']))

    def _render_history(self, entity: dict) -> None:
        entries = self.events(entity)
        hist = safe_path(self.root, entity['path']) / 'History'
        for fn, kind in [('WORK-LOG.md', None), ('DECISIONS.md', 'decision'),
                          ('CONTEXT-CHANGELOG.md', 'context_change'), ('OPEN-LOOPS.md', 'open_loop')]:
            picked = entries if kind is None else [e for e in entries if e['kind'] == kind]
            if kind == 'open_loop':
                latest = {e['loop_id']: e for e in picked}
                picked = [e for e in latest.values() if e['status'] not in {'closed', 'rejected', 'superseded'}]
            lines = ['# ' + fn.removesuffix('.md').replace('-', ' ').title(), '',
                     'Generated view; immutable JSON events are authoritative. Superseded history is retained.', '']
            for e in picked:
                lines += [f'## {e["created_at"]} · {e["id"]}',
                          f'Status: {e["status"]}; session: {e["session_id"]}', '', e['summary'], '']
                if e.get('supersedes'):
                    lines += ['Supersedes: ' + e['supersedes'], '']
                if e.get('loop_id'):
                    lines += ['Loop: ' + e['loop_id'], '']
            atomic_write(hist / fn, '\n'.join(lines).encode())

    def _render_session(self, session: dict) -> None:
        entity = self.entity(session['scope']['entity_id'])
        entries = self.events(entity, session['id'])
        local = Path(session['handoff_dir'])
        no_symlinks(local)
        for fn, kinds in [('WORK-LOG.md', EVENT_KINDS), ('DECISIONS.md', {'decision'}),
                          ('OPEN-LOOPS.md', {'open_loop'}), ('CHANGES.md', {'work', 'verification', 'context_change'})]:
            lines = ['# ' + fn.removesuffix('.md'), '', 'Generated from explicit session events, not inferred activity.', '']
            for e in entries:
                if e['kind'] in kinds:
                    lines += [f'## {e["id"]} [{e["status"]}]', e['summary'],
                              'Evidence: ' + str(e.get('evidence', 'not supplied')), '']
            atomic_write(local / fn, '\n'.join(lines).encode())
        handoff = ['# Handoff', '', f'Session: {session["id"]}', f'ACO version: {VERSION}',
                   'Scope: ' + json.dumps(session['scope']), 'Status: ' + session['status'], '',
                   '## Objective', session['brief'], '', '## Recorded work']
        handoff += [f'- [{e["status"]}] {e["summary"]}' for e in entries]
        handoff += ['', '## Next actions'] + [str(e['next_action']) for e in entries if e.get('next_action')]
        handoff += ['', '## Persistence', 'Local records verified. Consult sync receipts for Drive status; a local file is not a Drive write.', '']
        atomic_write(local / 'HANDOFF.md', '\n'.join(handoff).encode())

    def close(self, session_id: str) -> dict:
        with self._lock():
            path = self._session_path(session_id)
            s = read_json(path)
            if s['status'] != 'closed':
                s.update(status='closed', closed_at=now())
                write_json(path, s)
                write_json(Path(s['handoff_dir']) / 'SESSION.json', s)
            if not s.get('handoff_dir'):
                return {'status': 'closed', 'session_id': session_id, 'persistence': 'local_verified'}
            self._render_session(s)
            entity = self.entity(s['scope']['entity_id'])
            src = Path(s['handoff_dir']) / 'HANDOFF.md'
            dst = safe_path(self.root, entity['path']) / 'Handoffs' / (session_id + '.md')
            atomic_write(dst, src.read_bytes())
            return {'status': 'closed', 'session_id': session_id, 'handoff': str(src), 'persistence': 'local_verified'}

    def propose_context(self, entity_id: str, content: str, base_sha256: str, rationale: str) -> dict:
        if not rationale.strip():
            raise ACOError('A rationale is required')
        with self._lock():
            ent = self.entity(entity_id)
            folder = safe_path(self.root, ent['path'])
            no_symlinks(folder / 'Context.md')
            current = digest((folder / 'Context.md').read_bytes())
            if current != base_sha256:
                raise Conflict('Context changed since it was read. Re-read it and review the proposal.')
            p = {'id': uid('proposal'), 'entity_id': entity_id, 'base_sha256': base_sha256,
                 'new_sha256': digest(content.encode()), 'new_content': content,
                 'rationale': rationale, 'created_at': now(), 'status': 'proposed'}
            write_json(folder / 'History/Proposals' / (p['id'] + '.json'), p)
            return p

    def apply_context(self, entity_id: str, proposal_id: str, approval_ref: str) -> dict:
        if not approval_ref.strip() or not re.fullmatch(r'proposal-[0-9a-f]{32}', proposal_id):
            raise ACOError('Valid proposal ID and explicit approval reference required')
        with self._lock():
            if self.registry()['authority'] != 'local':
                raise Conflict('Drive is authoritative: apply there with revision control, then refresh the local snapshot.')
            ent = self.entity(entity_id)
            folder = safe_path(self.root, ent['path'])
            prop = read_json(folder / 'History/Proposals' / (proposal_id + '.json'))
            receipt = folder / 'History/Proposals' / (proposal_id + '.receipt.json')
            if receipt.exists():
                result = read_json(receipt)
                self._context_event(ent, prop, result)
                return result
            context = folder / 'Context.md'
            no_symlinks(context)
            old = context.read_bytes()
            old_hash = digest(old)
            backup = folder / 'History/ContextVersions' / (proposal_id + '.md')
            # Interrupted after atomic context replacement but before receipt: repair, do not replace again.
            if old_hash == prop['new_sha256'] and backup.exists() and digest(backup.read_bytes()) == prop['base_sha256']:
                pass
            elif old_hash != prop['base_sha256']:
                raise Conflict('Stale proposal: canonical context has changed. No overwrite performed.')
            else:
                ensure_file(backup, old)
                atomic_write(context, prop['new_content'].encode())
            if digest(context.read_bytes()) != prop['new_sha256']:
                raise ACOError('Context read-back verification failed')
            result = {'proposal_id': proposal_id, 'entity_id': entity_id, 'status': 'applied',
                      'approval_ref': approval_ref, 'verified_at': now(), 'sha256': prop['new_sha256']}
            write_json(receipt, result)
            self._context_event(ent, prop, result)
            return result

    def _context_event(self, ent: dict, proposal: dict, receipt: dict) -> None:
        """Idempotent audit event, including recovery after a lost final response."""
        eid = 'event-context-' + proposal['id'].split('-', 1)[1]
        sid = 'session-' + uuid.uuid5(uuid.NAMESPACE_URL, proposal['id']).hex
        scope = {'entity_id': ent['id'], 'owner_id': ent['owner_id']}
        event = {'schema_version': 1, 'id': eid, 'session_id': sid, 'scope': scope,
                 'aco_version': VERSION, 'kind': 'context_change', 'status': 'verified',
                 'summary': proposal['rationale'], 'created_at': receipt['verified_at'],
                 'approval_ref': receipt['approval_ref'],
                 'evidence': {'proposal_id': proposal['id'], 'before_sha256': proposal['base_sha256'],
                              'after_sha256': receipt['sha256']}}
        base = safe_path(self.root, ent['path'])
        existing_event = base / 'History/Events' / (eid + '.json')
        if existing_event.exists():
            event = read_json(existing_event)
        else:
            event['entity_sequence'] = max([x.get('entity_sequence', 0) for x in self.events(ent)] + [0]) + 1
        ensure_file(existing_event, json_bytes(event))
        ensure_file(self.system / 'Outbox' / (eid + '.json'), json_bytes(event))
        # This maintenance record has no browser/code workspace and is already closed.
        ensure_file(base / 'History/Sessions' / (sid + '.json'), json_bytes({
            'schema_version': 1, 'id': sid, 'scope': scope, 'status': 'closed',
            'aco_version': VERSION, 'created_at': receipt['verified_at'],
            'operation': 'approved_context_update', 'context_mode': 'FULL',
            'brief': proposal['rationale'], 'handoff_dir': None}))
        self._render_history(ent)

    def status(self) -> dict:
        r = self.registry()
        pending = []
        for f in sorted((self.system / 'Outbox').glob('event-*.json')):
            receipt = self.system / 'Receipts' / f.name
            if not receipt.exists():
                pending.append(f.stem)
        return {'authority': r['authority'], 'entities': list(r['entities'].values()),
                'pending_drive_events': pending, 'root': str(self.root)}
