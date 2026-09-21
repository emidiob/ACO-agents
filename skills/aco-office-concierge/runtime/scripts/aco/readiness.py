"""Side-effect-free studio readiness checks. No network, writes, execution or scoring people/art.

Evidence references and connector snapshots are caller supplied. They are not
credentials or proof of truth. The host must enforce real permissions and
verify sources and receipts before taking any external action.
"""
from __future__ import annotations
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import shutil
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .common import ACOError, VERSION

COMMANDS = {
    'git': 'version_control', 'python3': 'local_python',
    'ffmpeg': 'media_processing', 'ffprobe': 'media_inspection',
    'pandoc': 'document_conversion', 'quarto': 'publishing',
    'oiiotool': 'image_pipeline', 'gitleaks': 'secret_scanning',
    'semgrep': 'static_analysis', 'promptfoo': 'model_evaluation',
    'lighthouse': 'web_audit',
}


def _obj(value, label='input'):
    if not isinstance(value, dict):
        raise ACOError(label + ' must be an object')
    return value


def _list(value, label, max_items=1000):
    if not isinstance(value, list) or len(value) > max_items:
        raise ACOError(f'{label} must be a list of at most {max_items} items')
    return value


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _num(value, label):
    if isinstance(value, bool):
        raise ACOError(label + ' must be a non-negative finite number')
    try:
        out = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ACOError(label + ' must be a non-negative finite number')
    if not out.is_finite() or out < 0:
        raise ACOError(label + ' must be a non-negative finite number')
    return out


def _dt(value, label):
    if not isinstance(value, str):
        raise ACOError(label + ' must be an ISO timestamp with timezone')
    try:
        out = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ACOError(label + ' must be an ISO timestamp with timezone')
    if out.tzinfo is None or out.utcoffset() is None:
        raise ACOError(label + ' needs an explicit timezone offset')
    return out


def _now(value=None):
    out = value or datetime.now(timezone.utc)
    if not isinstance(out, datetime) or out.tzinfo is None or out.utcoffset() is None:
        raise ACOError('as_of must be a timezone-aware datetime')
    return out


def _result(kind, blockers, warnings, **extra):
    return dict(check=kind, status='needs_review' if blockers else 'ready_for_review',
                blockers=blockers, warnings=warnings, executed=False,
                knowledge_files_created=0, **extra)


def capability_audit(which=None):
    """Locate a fixed allowlist of commands without running them or reading credentials."""
    which = which or shutil.which
    checks = []
    for command, purpose in COMMANDS.items():
        path = which(command)
        checks.append(dict(command=command, purpose=purpose, found=bool(path),
                           path=path, runnable_verified=False, version_checked=False))
    return dict(aco_version=VERSION, checked_at=datetime.now(timezone.utc).isoformat(),
                status='local_presence_only', commands=checks, executed=False,
                remote_integrations='not_checked', credentials_read=False,
                note='PATH discovery is not an execution test. Discover actual connector schemas in the host; no service is connected by this check.')


def practice_check(data):
    d = _obj(data); blockers = []; warnings = []
    for k in ('scope_id', 'current_question'):
        if not _text(d.get(k)):
            blockers.append('Clarify ' + k)
    priorities = _list(d.get('priorities', []), 'priorities')
    if not 1 <= len(priorities) <= 3:
        blockers.append('Choose one to three priorities instead of an unbounded development plan.')
    known = set(); allocated = Decimal(0); making = Decimal(0)
    for n, raw in enumerate(priorities):
        p = _obj(raw, 'priority'); pid = p.get('id')
        if not _text(pid) or pid in known:
            blockers.append('Priority IDs must be non-empty and distinct.')
        if _text(pid): known.add(pid)
        for k in ('title', 'next_action', 'learning_signal'):
            if not _text(p.get(k)): blockers.append(f'Priority {n+1} needs {k}.')
        cat = p.get('category')
        if cat not in ('making', 'research', 'career', 'revenue', 'operations',):
            blockers.append(f'Priority {n+1} needs a supported category.')
        if p.get('hours_per_week') is None:
            blockers.append(f'Priority {n+1} needs an effort estimate.')
        else:
            h = _num(p['hours_per_week'], 'hours_per_week'); allocated += h
            if cat in ('making', 'research',): making += h
    if making == 0:
        warnings.append('No making/research time is protected in this plan; confirm that an operations-only interval is intentional.')
    capacity = d.get('available_hours_per_week')
    if capacity is None:
        blockers.append('Clarify available_hours_per_week before calling this plan feasible.')
    elif allocated + _num(d.get('other_commitments_hours', 0), 'other_commitments_hours') > _num(capacity, 'available_hours_per_week'):
        blockers.append('Planned hours exceed supplied capacity, including other commitments.')
    protected = _num(d.get('protected_making_research_hours', 0), 'protected_making_research_hours')
    if making < protected: blockers.append('Allocated making/research is below the user protected-time requirement.')
    if not _text(d.get('review_date')): warnings.append('Set a review date; this does not create a schedule.')
    return _result('practice', blockers, warnings, allocated_hours_per_week=str(allocated),
                   making_research_hours=str(making), artistic_quality='not_scored',
                   retention='chat_or_existing_artist_ACO_section',
                   limitation='Arithmetic and declared-plan checks only; not a judgement of artistic value or a verified calendar.')


def opportunity_check(data, as_of=None):
    d = _obj(data); now = _now(as_of); blockers = []; warnings = []
    for k in ('scope_id', 'title', 'practice_need', 'official_source', 'source_evidence_ref'):
        if not _text(d.get(k)): blockers.append('Clarify ' + k)
    if _text(d.get('official_source')):
        try:
            u = urlsplit(d['official_source'])
            if u.scheme != 'https' or not u.netloc or u.username or u.password:
                raise ValueError('unsupported source')
        except ValueError:
            blockers.append('Use a clean HTTPS official source, not credentials or an unsupported URI.')
    try:
        checked = date.fromisoformat(d.get('checked_on', ''))
        age = (now.date()-checked).days
        if not 0 <= age <= 7: blockers.append('Recheck current call evidence; review date is stale or in the future.')
    except (ValueError, TypeError): blockers.append('Provide checked_on as an ISO date.')
    eligibility = _list(d.get('eligibility', []), 'eligibility')
    if not eligibility: blockers.append('Verify actual eligibility criteria; an empty list is not a pass.')
    hard_fail = False
    for criterion in eligibility:
        c = _obj(criterion, 'eligibility item')
        state = c.get('result')
        if state not in ('pass', 'fail', 'unknown',): raise ACOError('Eligibility result must be pass, fail or unknown')
        if not _text(c.get('criterion')): blockers.append('Name each eligibility criterion.')
        if state == 'fail': hard_fail = True; blockers.append('Eligibility failed: '+str(c.get('criterion', 'unnamed')))
        if state == 'unknown': blockers.append('Resolve eligibility: '+str(c.get('criterion', 'unnamed')))
        if state != 'unknown' and not _text(c.get('evidence_ref')): blockers.append('Eligibility assertions need evidence references.')
    expired = False
    if d.get('deadline_kind') not in ('fixed', 'rolling'):
        blockers.append('Declare deadline_kind as fixed or rolling, based on the actual call.')
    if d.get('deadline_kind') == 'rolling':
        if not _text(d.get('rolling_evidence_ref')): blockers.append('A rolling deadline needs explicit current provider evidence.')
    else:
        if not _text(d.get('deadline_at')): blockers.append('Verify the deadline with timezone; do not infer it.')
        else:
            deadline = _dt(d['deadline_at'], 'deadline_at')
            if deadline <= now: expired = True; blockers.append('The supplied deadline has passed.')
    if not _text(d.get('cost_support_summary')): blockers.append('Clarify artist fee, production support, costs and payment timing.')
    if not _text(d.get('availability_evidence_ref')): warnings.append('Attendance/capacity has not been evidenced.')
    recommendation = 'do_not_submit_as_eligible' if hard_fail or expired else 'investigate' if blockers else 'consider_with_artist'
    return _result('opportunity', blockers, warnings, recommendation=recommendation,
                   retention='pipeline_row_only', creates_project=False,
                   submission_authorized=False,
                   limitation='Source/eligibility assertions are supplied, not remotely verified. No acceptance probability or submission is produced.')


def brand_check(data):
    d = _obj(data); blockers = []; warnings = []
    for k in ('scope_id', 'brand_id', 'objective', 'audience', 'proposition'):
        if not _text(d.get(k)): blockers.append('Clarify ' + k)
    claims = _list(d.get('claims', []), 'claims')
    seen = set()
    for c in claims:
        c = _obj(c, 'claim')
        if not _text(c.get('id')) or c['id'] in seen: blockers.append('Claims need distinct IDs.')
        if _text(c.get('id')): seen.add(c['id'])
        if not _text(c.get('text')): blockers.append('Claim text is missing.')
        state = c.get('support')
        if state not in ('assumed', 'researched', 'validated',): raise ACOError('Claim support must be assumed, researched or validated')
        refs = _list(c.get('evidence_refs', []), 'evidence_refs')
        if state in ('researched', 'validated',) and not any(_text(x) for x in refs): blockers.append('Supported claims require evidence references.')
        if state == 'assumed': warnings.append('Assumed claim must not be presented as verified: '+str(c.get('id')))
    if d.get('decision_status') not in ('proposed', 'approved',): blockers.append('Decision status must distinguish proposed from approved.')
    elif d['decision_status'] == 'approved' and not _text(d.get('approval_ref')): blockers.append('Approved brand decisions need an approval reference.')
    if not _list(d.get('applications', []), 'applications'): warnings.append('Define representative real applications for identity testing.')
    for name in _list(d.get('names', []), 'names'):
        n = _obj(name, 'name'); status = n.get('clearance', 'not_assessed')
        if status not in ('not_assessed', 'pending_review', 'professional_review_recorded',):
            raise ACOError('Do not label a name cleared from an informal availability search')
        if status == 'professional_review_recorded' and not _text(n.get('review_ref')):
            blockers.append('Professional name review needs its actual reference.')
    return _result('brand', blockers, warnings, retention='existing_owner_Brand_section',
                   trademark_clearance_verified=False,
                   limitation='Checks evidence labels and required context, not whether a strategy is good or a trademark is legally available.')


def social_packet_hash(packet):
    p = _obj(packet, 'packet')
    try:
        raw = json.dumps(p, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    except (ValueError, TypeError):
        raise ACOError('Packet must be finite JSON data')
    return sha256(raw).hexdigest()


def social_check(data, as_of=None):
    d = _obj(data); p = _obj(d.get('packet'), 'packet'); now = _now(as_of)
    h = social_packet_hash(p); blockers = []; warnings = []
    for k in ('scope_id', 'brand_id', 'account_id', 'platform', 'version'):
        if not _text(p.get(k)): blockers.append('Clarify '+k)
    action = p.get('action')
    if action not in ('draft', 'prepare', 'publish', 'schedule',): raise ACOError('Action must be draft, prepare, publish or schedule')
    execution_intent = action in ('publish', 'schedule',)
    posts = _list(p.get('posts', []), 'posts', 100)
    if not posts: blockers.append('No posts in the packet.')
    ids = set()
    for raw in posts:
        post = _obj(raw, 'post'); pid = post.get('id')
        if not _text(pid) or pid in ids: blockers.append('Posts need distinct non-empty IDs.')
        if _text(pid): ids.add(pid)
        media = _list(post.get('media', []), 'media', 100)
        if not _text(post.get('text')) and not media: blockers.append('Each post needs actual text or media.')
        for raw_asset in media:
            asset = _obj(raw_asset, 'media asset')
            if not _text(asset.get('uri')): blockers.append('Media requires an actual reference.')
            digest = asset.get('sha256')
            if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
                blockers.append('Media needs a lowercase SHA-256 of the reviewed bytes; a mutable URL alone is not approval binding.')
            if asset.get('rights_status') not in ('confirmed', 'unknown', 'not_applicable',): blockers.append('Declare media rights status.')
            if execution_intent and (asset.get('rights_status') != 'confirmed' or not _text(asset.get('rights_ref'))): blockers.append('Confirm rights for media before publication.')
        for raw_claim in _list(post.get('claims', []), 'claims'):
            claim = _obj(raw_claim, 'claim')
            if execution_intent and not _text(claim.get('verified_source_ref')): blockers.append('Publication claims need verified source references.')
        if execution_intent:
            for field in ('privacy_review_ref', 'accessibility_review_ref', 'disclosure_review_ref'):
                if not _text(post.get(field)): blockers.append('Review '+field+' for '+str(pid))
    if action == 'schedule':
        scheduled = _dt(p.get('schedule_at'), 'schedule_at')
        if scheduled <= now: blockers.append('Scheduled time must be in the future.')
        try:
            tz = ZoneInfo(p.get('timezone', ''))
            if scheduled.astimezone(tz).utcoffset() != scheduled.utcoffset():
                blockers.append('Schedule offset does not match the declared timezone at that date.')
        except (ValueError, TypeError, ZoneInfoNotFoundError): blockers.append('Provide a valid IANA timezone, such as UTC or Europe/Rome.')
    if execution_intent:
        a = d.get('approval'); cap = d.get('capability')
        if not isinstance(a, dict): blockers.append('Exact publication approval is missing.')
        else:
            for k in ('scope_id','account_id'):
                if a.get(k) != p.get(k): blockers.append('Approval scope/account does not match.')
            if a.get('packet_sha256') != h: blockers.append('Approval hash differs from the final content/media/timing packet.')
            if not _text(a.get('approval_ref')): blockers.append('Approval requires an actual user reference.')
            if a.get('denied') is True: blockers.append('Publication denied; do not evade through another route.')
            if a.get('expires_at') is not None and _dt(a['expires_at'],'approval expires_at') <= now: blockers.append('Publication approval expired.')
        if not isinstance(cap,dict): blockers.append('Inspect actual connected provider capabilities.')
        else:
            for k in ('scope_id', 'account_id', 'platform'):
                if cap.get(k) != p.get(k): blockers.append('Capability scope/account/platform does not match.')
            operations = _list(cap.get('operations',[]),'operations')
            if action not in operations: blockers.append('This provider snapshot does not support the requested action.')
            if cap.get('status') != 'verified_available' or not _text(cap.get('evidence_ref')): blockers.append('Capability needs verified host evidence, not a registry entry.')
            try:
                delta=now-_dt(cap.get('checked_at'),'capability checked_at')
                if not timedelta(0) <= delta <= timedelta(hours=24): blockers.append('Recheck stale/future capability evidence.')
            except ACOError: blockers.append('Capability checked_at needs a timestamp with timezone.')
        prior=d.get('previous_receipt')
        if isinstance(prior,dict) and prior.get('packet_sha256') == h:
            if prior.get('state') in ('published','scheduled','accepted','sent',): blockers.append('This packet already has an accepted result; inspect it instead of duplicating the action.')
            elif prior.get('state') in ('unknown','timeout',): blockers.append('Prior result is uncertain; reconcile with the provider before retrying.')
    else: warnings.append('Draft/preparation only: no publication approval or connection is implied.')
    return _result('social', blockers, warnings, packet_sha256=h, action=action,
                   publication_authorized=False, provider_called=False,
                   next='host_review_required' if not blockers else 'resolve_blockers_or_return_draft',
                   limitation='Offline packet consistency only. Evidence authenticity, actual bytes at media references, current platform rules, credentials and provider results must be verified by the host.')
