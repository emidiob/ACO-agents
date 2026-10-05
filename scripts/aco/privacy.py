from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import urlsplit
from .common import ROOT, VERSION, read_json

_TEXT_SUFFIXES={'.md','.json','.toml','.txt','.yaml','.yml','.py','.sh','.command','.html','.css','.js','.ts'}
_EXCLUDE_PARTS={'.git','__pycache__','.venv','.pytest_cache'}


def _is_example_email(addr:str, example_domains:set[str])->bool:
    domain=addr.rsplit('@',1)[-1].lower().rstrip('.')
    return domain in example_domains or any(domain.endswith('.'+d) for d in example_domains)


def privacy_scan(root: Path | None=None) -> dict:
    root=(root or ROOT).expanduser().absolute()
    policy=read_json(root/'config/privacy-policy.json')
    example_domains=set(policy.get('example_domains',[]))
    allowed_local_hosts=set(policy.get('allowed_local_hosts',[]))
    owner_paths=set(policy.get('owner_name_allowed_paths',[]))
    owner=None
    license_path=root/'LICENSE'
    if license_path.is_file():
        lm=re.search(r'Copyright \u00a9 \d{4} (.+?)\. All rights reserved\.', license_path.read_text(encoding='utf-8'))
        if lm: owner=lm.group(1).strip()
    public_repo=policy.get('canonical_public_repository')
    findings=[]; scanned=0
    email_re=re.compile(r'(?<![\w.+-])([A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,}|example\.invalid))(?![\w.-])')
    phone_re=re.compile(r'(?<!\w)(\+\d{1,3}[\s().-]?(?:\d[\s().-]?){7,14})(?!\w)')
    user_path_re=re.compile(r'/(?:Users|home)/([A-Za-z0-9._-]+)/')
    cred_res=[
        ('private_key',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
        ('github_token',re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b')),
        ('openai_key',re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{35,}\b')),
        ('aws_key',re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
        ('slack_token',re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b')),
        ('credential_assignment',re.compile(r'(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*["\'][^"\'\n]{12,}["\']')),
    ]
    drive_re=re.compile(r'https://(?:drive\.google\.com/(?:drive/folders|file/d)/|docs\.google\.com/(?:document|spreadsheets|presentation)/d/)[A-Za-z0-9_-]{15,}')
    cred_url_re=re.compile(r'https?://[^\s/:]+:[^\s/@]+@[^\s]+')

    for p in root.rglob('*'):
        if not p.is_file() or any(x in _EXCLUDE_PARTS for x in p.relative_to(root).parts): continue
        rel=p.relative_to(root).as_posix()
        # Filename/path hygiene: actual home path fragments or email-like filenames.
        if '@' in p.name and not any(d in p.name for d in example_domains):
            findings.append({'type':'personal_filename','path':rel})
        if p.suffix not in _TEXT_SUFFIXES and p.name not in {'LICENSE','VERSION','.gitignore'}: continue
        try: text=p.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        scanned+=1
        if owner and owner in text and rel not in owner_paths:
            findings.append({'type':'public_owner_outside_allowed_path','path':rel})
        for m in email_re.finditer(text):
            addr=m.group(1)
            if not _is_example_email(addr,example_domains): findings.append({'type':'email','path':rel,'value':'[redacted]'})
        for _ in phone_re.finditer(text): findings.append({'type':'phone','path':rel,'value':'[redacted]'})
        for m in user_path_re.finditer(text):
            user=m.group(1)
            if user.lower() not in {'user','username','example','tmp','root'}:
                findings.append({'type':'local_user_path','path':rel,'value':'/[home]/[redacted]/'})
        if drive_re.search(text): findings.append({'type':'private_drive_id','path':rel,'value':'[redacted]'})
        for m in cred_url_re.finditer(text):
            try:
                host=urlsplit(m.group(0)).hostname or ''
            except ValueError:
                host=''
            if host.lower() not in example_domains and host.lower() not in allowed_local_hosts and not any(host.lower().endswith('.'+d) for d in example_domains):
                findings.append({'type':'credential_url','path':rel,'value':'[redacted]'})
        for kind,rx in cred_res:
            if rx.search(text): findings.append({'type':kind,'path':rel,'value':'[redacted]'})
    # De-duplicate without exposing sensitive values.
    seen=set(); uniq=[]
    for f in findings:
        key=(f['type'],f['path'])
        if key not in seen: seen.add(key); uniq.append(f)
    return {'status':'passed' if not uniq else 'failed','aco_version':VERSION,'root':str(root),'files_scanned':scanned,'findings':uniq,
            'allowed_public_identifiers':['copyright_holder_from_LICENSE'] + ([public_repo] if public_repo else []),
            'policy':'Release packaging must stop on unreviewed personal/private/credential findings. Synthetic fixtures and explicitly public identifiers are allowlisted narrowly.'}
