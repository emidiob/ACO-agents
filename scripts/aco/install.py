"""Managed, collision-safe installation and rollback for Codex skills/agents."""
from __future__ import annotations
import json
import os
import shutil
from pathlib import Path
from typing import Any
from .common import (ACOError, Conflict, ROOT, VERSION, atomic_write, digest,
                     json_bytes, lock, no_symlinks, now, private_root, read_json,
                     safe_path, uid, write_json)


def catalog() -> dict:
    return read_json(ROOT / 'catalog.json')


def verify_release() -> dict:
    manifest = read_json(ROOT / 'release/manifest.json')
    for rel, meta in manifest['files'].items():
        p = safe_path(ROOT, rel)
        if not p.is_file() or digest(p.read_bytes()) != meta['sha256']:
            raise ACOError(f'Release integrity check failed: {rel}. Rebuild/download the complete release.')
    return manifest


def agent_set(offices: list[str]) -> set[str]:
    c = catalog()
    available = set(c['offices'])
    if offices == ['none']:
        return set()
    chosen = available if 'all' in offices else set(offices)
    if not chosen <= available:
        raise ACOError('Unknown office. Choose: ' + ', '.join(sorted(available)) + ', all, or none')
    selected = {key for key, a in c['agents'].items() if a['office'] in chosen or a['office'] == 'shared'}
    # Explicit office dependencies select reused roles without duplicating their source definitions.
    for office in chosen:
        selected.update(c['offices'][office].get('dependencies', []))
    return selected


class Installer:
    def __init__(self, home: Path | None = None, project: Path | None = None,
                 codex_home: Path | None = None):
        self.home = (home or Path.home()).expanduser().absolute()
        self.project = project.expanduser().absolute() if project else None
        if self.project and not self.project.is_dir():
            raise ACOError('Project installation requires an existing directory')
        self.skill_root = (self.project or self.home) / '.agents/skills'
        self.agent_root = ((self.project / '.codex') if self.project else
                           (codex_home or (self.home / '.codex'))) / 'agents'
        identity = str(self.skill_root) + '\n' + str(self.agent_root)
        self.install_id = digest(identity.encode())[:16]
        # State is private even for project installations.
        self.state_root = self.home / '.local/share/aco/installations' / self.install_id
        self.state_file = self.state_root / 'state.json'
        self.journal = self.state_root / 'transaction.json'
        for path in (self.skill_root, self.agent_root, self.state_root):
            no_symlinks(path)

    def desired(self, offices: list[str]) -> dict[str, tuple[bytes, int]]:
        release = verify_release()
        result = {}
        # Install only fingerprinted release files, never untracked local material
        # or Python caches found inside a source checkout's skills folder.
        for name, meta in release['files'].items():
            if name.startswith('skills/'):
                rel = Path(name).relative_to('skills')
                p = safe_path(ROOT, name)
                result[str(safe_path(self.skill_root, rel))] = (p.read_bytes(), meta.get('mode', 0o644))
        selected = agent_set(offices)
        for key in selected:
            source = safe_path(ROOT, catalog()['agents'][key]['codex_path'])
            dest = safe_path(self.agent_root, source.name)
            result[str(dest)] = (source.read_bytes(), 0o644)
        return result

    def _state(self) -> dict:
        if self.state_file.exists():
            state = read_json(self.state_file)
            if state.get('install_id') != self.install_id:
                raise Conflict('Installation state does not match the selected destination')
            for value in state.get('files', {}):
                p = Path(value)
                if not p.is_absolute() or '..' in p.parts:
                    raise Conflict('Invalid path in installation inventory')
                skill_ok = p.is_relative_to(self.skill_root) and p.relative_to(self.skill_root).parts and p.relative_to(self.skill_root).parts[0].startswith('aco-')
                agent_ok = p.parent == self.agent_root and p.name.startswith('aco-') and p.suffix == '.toml'
                if not (skill_ok or agent_ok):
                    raise Conflict('Inventory path is outside ACO installation ownership; no writes performed')
            return state
        return {'install_id': self.install_id, 'files': {}}

    def _preflight(self, desired: dict, old: dict, backup_modified: bool) -> list[dict]:
        changes = []
        for path in sorted(set(old['files']) | set(desired)):
            p = Path(path)
            no_symlinks(p)
            if p.exists() and not p.is_file():
                raise Conflict(f'A directory or special object blocks installation: {p}')
            current = digest(p.read_bytes()) if p.exists() else None
            previous = old['files'].get(path, {}).get('sha256')
            target = digest(desired[path][0]) if path in desired else None
            if previous is None and current is not None:
                raise Conflict(f'Unmanaged file exists; it will NOT be overwritten: {p}')
            if previous and current not in (None, previous) and not backup_modified:
                raise Conflict(f'An installed ACO file was modified locally: {p}. Back it up or use --backup-modified explicitly.')
            if current != target:
                changes.append({'path': path, 'old_sha256': current, 'new_sha256': target,
                                'action': 'remove' if target is None else ('replace' if current else 'create')})
        return changes

    def install(self, offices: list[str] | None = None, apply: bool = False, backup_modified: bool = False) -> dict:
        with lock(self.state_root / '.lock'):
            if self.journal.exists():
                raise Conflict('Interrupted installation detected. Run install-recover for this destination first.')
            old = self._state()
            offices = offices if offices is not None else old.get('offices', ['none'])
            desired = self.desired(offices)
            changes = self._preflight(desired, old, backup_modified)
            plan = {'version': VERSION, 'install_id': self.install_id, 'offices': offices,
                    'skill_root': str(self.skill_root), 'agent_root': str(self.agent_root),
                    'changes': changes, 'desired_files': len(desired)}
            if not apply:
                return {'status': 'dry_run', **plan}
            new = {'schema_version': 1, 'install_id': self.install_id, 'version': VERSION,
                   'offices': offices, 'updated_at': now(),
                   'files': {path: {'sha256': digest(data), 'mode': mode} for path, (data, mode) in desired.items()}}
            self._transaction(changes, desired, old, new)
            return {'status': 'installed_verified', **plan, 'files_verified': len(desired)}

    def _transaction(self, changes: list[dict], desired: dict, old: dict, new: dict) -> None:
        backup_dir = self.state_root / 'backups' / uid('transaction')
        backup_dir.mkdir(parents=True, exist_ok=True)
        records = []
        for i, change in enumerate(changes):
            p = Path(change['path'])
            record = dict(change)
            record['backup'] = None
            record['old_mode'] = (p.stat().st_mode & 0o777) if p.exists() else None
            if p.exists():
                backup = backup_dir / str(i)
                atomic_write(backup, p.read_bytes())
                record['backup'] = str(backup)
            records.append(record)
        tx = {'records': records, 'old_state': old, 'new_state': new, 'created_at': now()}
        write_json(self.journal, tx)
        try:
            for record in records:
                p = Path(record['path'])
                # Refuse a race between planning/backups and the write.
                observed = digest(p.read_bytes()) if p.exists() else None
                if observed != record['old_sha256']:
                    raise Conflict(f'File changed during installation: {p}')
                if record['action'] == 'remove':
                    p.unlink(missing_ok=True)
                else:
                    data, mode = desired[str(p)]
                    atomic_write(p, data, mode)
            for path, metadata in new['files'].items():
                p = Path(path)
                if not p.is_file() or digest(p.read_bytes()) != metadata['sha256']:
                    raise ACOError(f'Installation verification failed: {p}')
            write_json(self.state_file, new)
            self.journal.unlink()
        except Exception:
            self._recover_locked()
            raise

    def _recover_locked(self) -> dict:
        if not self.journal.exists():
            return {'status': 'nothing_to_recover'}
        tx = read_json(self.journal)
        # No broad directory removal; unknown third-party files survive.
        for record in reversed(tx['records']):
            p = Path(record['path'])
            no_symlinks(p)
            current = digest(p.read_bytes()) if p.exists() and p.is_file() else None
            if current not in (record['old_sha256'], record['new_sha256']):
                raise Conflict(f'Recovery stopped: externally modified {p}; backups retained at {self.state_root}')
            if record['backup']:
                atomic_write(p, Path(record['backup']).read_bytes(), record['old_mode'] or 0o644)
            elif p.exists():
                p.unlink()
        write_json(self.state_file, tx['old_state'])
        self.journal.unlink()
        return {'status': 'rolled_back', 'install_id': self.install_id}

    def recover(self) -> dict:
        with lock(self.state_root / '.lock'):
            return self._recover_locked()

    def uninstall(self, apply: bool = False, backup_modified: bool = False) -> dict:
        with lock(self.state_root / '.lock'):
            if self.journal.exists():
                raise Conflict('Recover interrupted installation before uninstalling')
            old = self._state()
            changes = self._preflight({}, old, backup_modified)
            if not apply:
                return {'status': 'dry_run', 'changes': changes}
            new = {'install_id': self.install_id, 'version': VERSION, 'files': {}}
            self._transaction(changes, {}, old, new)
            # Remove only now-empty ACO directories; never recurse over user material.
            for root in (self.skill_root, self.agent_root):
                if root.exists():
                    for p in sorted(root.rglob('*'), key=lambda x: len(x.parts), reverse=True):
                        if p.is_dir() and not p.is_symlink() and not any(p.iterdir()):
                            # ACO-created skill directories only, or no-op for agents.
                            if p.is_relative_to(self.skill_root) and p.relative_to(self.skill_root).parts[0].startswith('aco-'):
                                p.rmdir()
            return {'status': 'uninstalled_verified', 'removed_files': len(changes), 'backups_preserved': str(self.state_root)}

    def status(self) -> dict:
        old = self._state()
        problems = []
        for path, meta in old['files'].items():
            p = Path(path)
            if not p.is_file() or p.is_symlink() or digest(p.read_bytes()) != meta['sha256']:
                problems.append(path)
        return {'install_id': self.install_id, 'version': old.get('version'),
                'managed_files': len(old['files']), 'offices': old.get('offices', ['none']), 'modified_or_missing': problems,
                'recovery_required': self.journal.exists(), 'codex_available': bool(shutil.which('codex'))}
