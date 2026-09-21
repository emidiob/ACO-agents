"""Replace only known ACO repository files. No git reset/clean/force-push."""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
from .common import (ACOError, Conflict, ROOT, VERSION, atomic_write, digest,
                     no_symlinks, now, read_json, safe_path)
from .install import verify_release


def git(target: Path, *args: str) -> str:
    p = subprocess.run(['git', '-C', str(target), *args], text=True, capture_output=True)
    if p.returncode:
        raise ACOError('Git command failed: ' + ' '.join(args[:3]) + '\n' + p.stderr.strip())
    return p.stdout.strip()


def migrate(target: Path, apply: bool = False) -> dict:
    target = target.expanduser().absolute()
    no_symlinks(target)
    if target == ROOT or target.is_relative_to(ROOT) or ROOT.is_relative_to(target):
        raise ACOError('Extract the new release outside the existing repository before migrating.')
    if Path(git(target, 'rev-parse', '--show-toplevel')).resolve() != target.resolve():
        raise ACOError('Target must be the root of the existing Git repository')
    if git(target, 'status', '--porcelain', '--untracked-files=no'):
        raise Conflict('Tracked changes/staged work exist. Commit or preserve them before migrating.')
    source = verify_release()['files']
    # The release manifest is itself copied (but is not self-hashed).
    sources = dict(source)
    sources['release/manifest.json'] = {'sha256': digest((ROOT / 'release/manifest.json').read_bytes()), 'mode': 0o644}
    baselines = read_json(ROOT / 'release/legacy-files.json')['files']
    tracked = set(git(target, 'ls-files', '-z').split('\0')) - {''}
    adds, removes, changes = [], [], []
    previous_managed = {}
    if 'release/manifest.json' in tracked:
        previous_managed = read_json(target / 'release/manifest.json').get('files', {})
        # It has no self-hash, but it is checked through a clean Git worktree and retained in the backup branch.
        previous_managed['release/manifest.json'] = {'sha256': digest((target / 'release/manifest.json').read_bytes())}
    known = set(baselines) | set(previous_managed)
    for rel in sorted(tracked & known):
        p = safe_path(target, rel)
        if not p.is_file():
            raise Conflict('Expected managed regular file: ' + rel)
        current = digest(p.read_bytes())
        allowed = set(baselines.get(rel, []))
        if rel in previous_managed:
            allowed.add(previous_managed[rel]['sha256'])
        if current not in allowed:
            raise Conflict('Managed file differs from all known baselines; review before replacing: ' + rel)
        if rel not in sources:
            removes.append(rel)
    for rel, meta in sorted(sources.items()):
        p = safe_path(target, rel)
        if rel not in tracked and p.exists():
            raise Conflict('Untracked file would be overwritten: ' + rel)
        if rel in tracked and rel not in known:
            raise Conflict('New release collides with a non-ACO tracked file: ' + rel)
        if rel not in tracked:
            adds.append(rel)
        elif digest(p.read_bytes()) != meta['sha256'] or (p.stat().st_mode & 0o777) != meta.get('mode', 0o644):
            changes.append(rel)
    result = {'status': 'dry_run', 'target': str(target), 'add': adds,
              'replace': changes, 'remove': removes,
              'preserve_unmanaged_tracked': sorted(tracked - known - set(sources)),
              'base_commit': git(target, 'rev-parse', 'HEAD')}
    if not apply:
        return result
    stamp = now().replace(':', '').replace('-', '')
    backup_branch = f'aco/backup-{stamp}'
    work_branch = f'aco/refactor-{VERSION}-{stamp}'
    git(target, 'branch', backup_branch)
    git(target, 'switch', '-c', work_branch)
    # Failures leave a reviewable branch and a backup; never discard user work to recover.
    for rel in removes:
        safe_path(target, rel).unlink()
    # Remove only now-empty ancestors of removed managed files. Never recurse
    # through unrelated/user content, and never remove the checkout root.
    obsolete_dirs = set()
    for rel in removes:
        parent = safe_path(target, rel).parent
        while parent != target:
            obsolete_dirs.add(parent)
            parent = parent.parent
    for folder in sorted(obsolete_dirs, key=lambda x: len(x.parts), reverse=True):
        if folder.exists() and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    for rel in adds + changes:
        src = safe_path(ROOT, rel)
        atomic_write(safe_path(target, rel), src.read_bytes(), sources[rel].get('mode', 0o644))
    paths = adds + changes + removes
    for start in range(0, len(paths), 100):
        git(target, 'add', '--', *paths[start:start + 100])
    result.update(status='staged_not_committed', backup_branch=backup_branch, branch=work_branch,
                  next='Run checks/tests, review staged diff, then commit and push the branch. Merge main without force after review.')
    return result
