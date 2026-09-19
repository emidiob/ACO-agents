from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()

class ACOError(RuntimeError):
    """An actionable failure, not success with a warning."""

class Conflict(ACOError):
    """A conflicting value must not be overwritten silently."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def read_json(path: Path) -> Any:
    no_symlinks(path)
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ACOError(f'Cannot read valid JSON: {path}: {exc}') from exc


def safe_path(root: Path, relative: str | Path) -> Path:
    """Reject path traversal and existing symlink components, including leaf."""
    root = Path(root).absolute()
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ACOError(f'Unsafe relative path: {relative}')
    cursor = root
    for part in rel.parts:
        if part in ('', '.'):
            continue
        cursor /= part
        if cursor.is_symlink():
            raise ACOError(f'Refusing symlink: {cursor}')
    if not cursor.resolve(strict=False).is_relative_to(root.resolve(strict=False)):
        raise ACOError('Path escapes its approved root')
    return cursor


def no_symlinks(path: Path) -> None:
    path = path.absolute()
    for p in (path, *path.parents):
        if p.is_symlink():
            raise ACOError(f'Refusing symlink path component: {p}')


def atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.aco-tmp-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_json(path: Path, value: Any) -> None:
    atomic_write(path, json_bytes(value))


def ensure_file(path: Path, data: bytes) -> bool:
    """Create once. A repeated setup must never reset user content."""
    no_symlinks(path)
    if path.exists():
        if not path.is_file():
            raise Conflict(f'Expected a file, found another object: {path}')
        return False
    atomic_write(path, data)
    return True


@contextlib.contextmanager
def lock(path: Path) -> Iterator[None]:
    """OS lock for macOS/Linux. Released on exit or process termination."""
    try:
        import fcntl
    except ImportError as exc:
        raise ACOError('This command needs macOS/Linux; on Windows use WSL.') from exc
    no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        os.chmod(path, 0o600)
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Conflict(f'Another ACO operation is using {path.parent}. Retry after it finishes.') from exc
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def key_ok(key: str) -> str:
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', key):
        raise ACOError('Keys must be 1–64 lowercase letters, digits, _ or -, starting with a letter/digit.')
    return key


def uid(prefix: str) -> str:
    return prefix + '-' + uuid.uuid4().hex


def private_root() -> Path:
    return Path(os.environ.get('ACO_HOME', str(Path.home() / '.local/share/aco'))).expanduser()


def under_git(path: Path) -> bool:
    return any((p / '.git').exists() for p in (path, *path.parents))
