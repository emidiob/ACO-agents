"""Optional explicit Drive REST event bridge; no bundled account access.

The preferred ChatGPT integration is its separately connected Drive tools.
This bridge transfers immutable session events, not canonical context edits.
Set a short-lived OAuth access token in ACO_GOOGLE_ACCESS_TOKEN locally; never
paste credentials into chat or source control. No token is stored by this module.
"""
from __future__ import annotations
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from .common import ACOError, Conflict, digest, json_bytes, lock, now, read_json, write_json
from .memory import Memory

class DriveREST:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get('ACO_GOOGLE_ACCESS_TOKEN')
        if not self.token:
            raise ACOError('No local OAuth access token. Prefer connected Drive tools, or set ACO_GOOGLE_ACCESS_TOKEN locally. Do not paste it in chat.')

    def request(self, method: str, path: str, data: bytes | None = None,
                content_type: str = 'application/json', raw: bool = False):
        if not path.startswith(('/drive/v3/', '/upload/drive/v3/')):
            raise ACOError('Drive bridge endpoint outside allowlist')
        request = urllib.request.Request('https://www.googleapis.com' + path, data=data, method=method,
                                         headers={'Authorization': 'Bearer ' + self.token,
                                                  'Content-Type': content_type})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                raise ACOError('Response exceeds the event-bridge size limit')
            return body if raw else json.loads(body or b'{}')
        except urllib.error.HTTPError as exc:
            # Do not print credentials or provider bodies containing private content.
            raise ACOError(f'Drive HTTP {exc.code}. No success claimed; pending data is preserved.') from exc
        except urllib.error.URLError as exc:
            raise ACOError('Drive is unreachable; pending data is preserved.') from exc

    def metadata(self, file_id: str):
        return self.request('GET', '/drive/v3/files/' + urllib.parse.quote(file_id, safe='') +
                            '?fields=id,name,mimeType,parents,trashed&supportsAllDrives=true')

    def list_named(self, parent: str, name: str) -> list[dict]:
        escaped = name.replace('\\', '\\\\').replace("'", "\\'")
        parent = parent.replace("'", "\\'")
        query = f"'{parent}' in parents and trashed = false and name = '{escaped}'"
        files, page = [], None
        while True:
            args = {'q': query, 'fields': 'nextPageToken,files(id,name,mimeType,parents)',
                    'pageSize': 100, 'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}
            if page:
                args['pageToken'] = page
            answer = self.request('GET', '/drive/v3/files?' + urllib.parse.urlencode(args))
            files.extend(answer.get('files', []))
            page = answer.get('nextPageToken')
            if not page:
                return files

    def read(self, file_id: str) -> bytes:
        return self.request('GET', '/drive/v3/files/' + urllib.parse.quote(file_id, safe='') + '?alt=media', raw=True)

    def generate_id(self) -> str:
        return self.request('GET', '/drive/v3/files/generateIds?count=1&space=drive&type=files')['ids'][0]

    def create_folder(self, parent: str, name: str) -> dict:
        return self.request('POST', '/drive/v3/files?fields=id,name,mimeType,parents&supportsAllDrives=true',
                            json_bytes({'name': name, 'parents': [parent], 'mimeType': 'application/vnd.google-apps.folder'}))

    def upload(self, parent: str, file_id: str, name: str, data: bytes) -> dict:
        boundary = 'aco-' + digest(data)[:32]
        metadata = json_bytes({'id': file_id, 'name': name, 'parents': [parent], 'mimeType': 'application/json'})
        payload = (f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode() + metadata +
                   f'\r\n--{boundary}\r\nContent-Type: application/json\r\n\r\n'.encode() + data +
                   f'\r\n--{boundary}--\r\n'.encode())
        return self.request('POST', '/upload/drive/v3/files?uploadType=multipart&fields=id,name,parents&supportsAllDrives=true',
                            payload, 'multipart/related; boundary=' + boundary)

class DriveBridge:
    def __init__(self, memory: Memory, provider: DriveREST):
        self.memory, self.provider = memory, provider
        self.config = memory.system / 'DRIVE-BINDING.json'

    def _within(self, file_id: str, root_id: str) -> bool:
        visited, queue = set(), [file_id]
        for _ in range(100):
            if not queue:
                return False
            current = queue.pop()
            if current == root_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            metadata = self.provider.metadata(current)
            if metadata.get('trashed'):
                return False
            queue.extend(metadata.get('parents', []))
        raise ACOError('Unexpectedly deep/cyclic Drive parent chain')

    def bind(self, root_id: str, approval_ref: str) -> dict:
        if not root_id or not approval_ref.strip():
            raise ACOError('Explicit approved root and approval reference required')
        with self.memory._lock():
            meta = self.provider.metadata(root_id)
            if meta.get('trashed') or meta.get('mimeType') != 'application/vnd.google-apps.folder':
                raise ACOError('Approved Drive root is not an accessible folder')
            if self.config.exists():
                cfg = read_json(self.config)
                if cfg['root_id'] != root_id:
                    raise Conflict('Already bound to another root. Changing it requires a reviewed migration.')
                return cfg
            # Exact scoped search only. Bootstrap is single-writer; Drive has no atomic unique folder names.
            matches = self.provider.list_named(root_id, 'ACO Session Events')
            if len(matches) > 1:
                raise Conflict('Duplicate ACO Session Events folders; resolve before binding')
            folder = matches[0] if matches else self.provider.create_folder(root_id, 'ACO Session Events')
            if folder.get('mimeType') not in (None, 'application/vnd.google-apps.folder'):
                raise Conflict('ACO Session Events is not a folder')
            matches = self.provider.list_named(root_id, 'ACO Session Events')
            if len(matches) != 1 or matches[0]['id'] != folder['id']:
                raise Conflict('Concurrent Drive setup detected. Reconcile; no duplicate is selected silently.')
            cfg = {'schema_version': 1, 'root_id': root_id, 'events_folder_id': folder['id'],
                   'approval_ref': approval_ref, 'bound_at': now(), 'purpose': 'immutable_session_events_only'}
            write_json(self.config, cfg)
            return cfg

    def sync(self, session_id: str | None = None) -> dict:
        with self.memory._lock():
            cfg = read_json(self.config)
            folder = cfg['events_folder_id']
            if not self._within(folder, cfg['root_id']):
                raise Conflict('Drive destination moved outside the approved root')
            results = []
            for p in sorted((self.memory.system / 'Outbox').glob('event-*.json')):
                event = read_json(p)
                if session_id and event['session_id'] != session_id:
                    continue
                payload = json_bytes(event)
                if len(payload) > 1_000_000:
                    raise ACOError('Event too large; store artifact links rather than full private files')
                receipt_path = self.memory.system / 'Receipts' / p.name
                if receipt_path.exists():
                    receipt = read_json(receipt_path)
                    if receipt['sha256'] != digest(payload) or receipt['root_id'] != cfg['root_id']:
                        raise Conflict('Existing receipt does not match the current event/root')
                    if not self._within(receipt['file_id'], cfg['root_id']) or self.provider.read(receipt['file_id']) != payload:
                        raise Conflict('A previously synced remote event changed or moved; receipt needs reconciliation')
                    results.append({'id': event['id'], 'status': 'already_synced_verified'})
                    continue
                mapping = self.memory.system / 'Sync' / p.name
                matches = self.provider.list_named(folder, p.name)
                if len(matches) > 1:
                    raise Conflict(f'Duplicate remote event: {p.name}')
                if matches:
                    file_id = matches[0]['id']
                else:
                    if mapping.exists():
                        prior = read_json(mapping)
                        if prior['root_id'] != cfg['root_id']:
                            raise Conflict('Upload journal belongs to another root')
                        file_id = prior['file_id']
                    else:
                        file_id = self.provider.generate_id()
                        write_json(mapping, {'file_id': file_id, 'root_id': cfg['root_id']})
                    try:
                        self.provider.upload(folder, file_id, p.name, payload)
                    except ACOError:
                        # A lost response may mean create succeeded. Only exact read-back can confirm it.
                        try:
                            if self.provider.read(file_id) != payload:
                                raise Conflict('Remote content does not match the pending event')
                        except Exception:
                            raise ACOError('Upload unconfirmed. Event remains pending; retry with the same generated ID.')
                if not self._within(file_id, cfg['root_id']):
                    raise Conflict('Remote event is outside the approved folder tree')
                if folder not in self.provider.metadata(file_id).get('parents', []):
                    raise Conflict('Remote event is not in the exact bound event folder')
                check = self.provider.list_named(folder, p.name)
                if len(check) != 1 or check[0]['id'] != file_id:
                    raise Conflict('Concurrent duplicate event detected; no receipt written')
                remote = self.provider.read(file_id)
                if remote != payload:
                    raise Conflict('Remote event differs; no overwrite or success receipt written')
                receipt = {'event_id': event['id'], 'session_id': event['session_id'],
                           'root_id': cfg['root_id'], 'file_id': file_id,
                           'sha256': digest(payload), 'verified_at': now(), 'status': 'drive_verified'}
                write_json(receipt_path, receipt)
                results.append({'id': event['id'], 'status': 'drive_verified', 'file_id': file_id})
            return {'status': 'sync_completed', 'events': results}
