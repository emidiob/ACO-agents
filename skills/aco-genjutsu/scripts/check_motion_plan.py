#!/usr/bin/env python3
"""Check declared temporal coverage and prompt correspondence, not visual motion recognition."""
import json
import math
from pathlib import Path


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def interval(value, duration):
    return (isinstance(value, list) and len(value) == 2 and all(number(x) for x in value)
            and 0 <= value[0] < value[1] <= duration + 1e-6)


def covers(spans, duration):
    end = 0
    for start, stop in sorted(spans):
        if start > end + 1e-6:
            return False
        end = max(end, stop)
    return end >= duration - 1e-6


def check_motion(folder, prompt, references):
    folder = Path(folder)
    path = folder/'motion-plan.json'
    if not path.is_file():
        return ['Missing motion-plan.json: reference images alone do not describe motion']
    try:
        plan = json.loads(path.read_text())
        if not isinstance(plan, dict):
            raise ValueError()
    except (ValueError, OSError):
        return ['Invalid motion-plan.json']
    errors = []
    duration = plan.get('source_duration_seconds')
    target = plan.get('target_duration_seconds')
    if not all(number(x) and x > 0 for x in (duration, target)):
        return ['Motion plan needs positive source and target durations']
    inspection = folder/'inspection.json'
    if inspection.is_file():
        measured = json.loads(inspection.read_text()).get('duration_seconds')
        if number(measured) and abs(measured - duration) > 1e-6:
            errors.append('Motion source duration differs from inspection.json')
    reviewed = plan.get('reviewed_intervals', [])
    if (not isinstance(reviewed, list) or not all(interval(x, duration) for x in reviewed)
            or not covers(reviewed, duration)):
        errors.append('Source review does not cover the complete duration')
    entities = plan.get('entities', {})
    if not isinstance(entities, dict) or not entities or not all(isinstance(v, str) and v.strip() for v in entities.values()):
        errors.append('Missing source-to-target entity mapping')
        entities = {}
    events = plan.get('events', [])
    if not isinstance(events, list) or not events:
        return errors + ['No motion events recorded']
    names = {r.get('file') for r in references}
    ids = set(); spans = []; target_spans = []; tracks = set(); action_spans = []; target_actions = []
    for event in events:
        if not isinstance(event, dict):
            errors.append('Invalid motion event'); continue
        label = event.get('id')
        if not isinstance(label, str) or not label.strip() or label in ids:
            errors.append('Missing or duplicate motion event ID')
        else:
            ids.add(label)
        if not isinstance(event.get('actor'), str) or event['actor'] not in entities:
            errors.append(f'{label}: unmapped actor')
        track = event.get('track')
        if track not in ('subject', 'object', 'camera'):
            errors.append(f'{label}: invalid motion track')
        else:
            tracks.add(track)
        for field in ('observed', 'target_action'):
            if not isinstance(event.get(field), str) or not event[field].strip():
                errors.append(f'{label}: missing {field}')
        if event.get('certainty') != 'observed':
            errors.append(f'{label}: unresolved motion observation')
        evidence = event.get('evidence', [])
        if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or x not in names for x in evidence):
            errors.append(f'{label}: missing or unknown frame evidence')
        source_span = event.get('source_interval')
        if interval(source_span, duration):
            spans.append(source_span)
            if track in ('subject', 'object'): action_spans.append(source_span)
        else:
            errors.append(f'{label}: invalid source interval')
        disposition = event.get('disposition', 'transfer')
        if disposition == 'omitted':
            if not all(isinstance(event.get(x), str) and event[x].strip() for x in ('omission_reason', 'requested_change')):
                errors.append(f'{label}: omission lacks reason and requested change')
        elif disposition == 'transfer':
            target_span = event.get('target_interval')
            if interval(target_span, target):
                target_spans.append(target_span)
                if track in ('subject', 'object'): target_actions.append(target_span)
            else:
                errors.append(f'{label}: invalid target interval')
            excerpt = event.get('prompt_excerpt')
            if not isinstance(excerpt, str) or not excerpt.strip() or excerpt not in prompt:
                errors.append(f'{label}: movement excerpt missing from final prompt')
        else:
            errors.append(f'{label}: unknown disposition')
    if 'camera' not in tracks:
        errors.append('Camera motion or observed static camera not recorded')
    if not covers(spans, duration):
        errors.append('Motion events leave source intervals unaccounted for')
    if not covers(target_spans, target):
        errors.append('Transferred motion leaves target intervals unaccounted for')
    if not covers(action_spans, duration):
        errors.append('Subject/object motion leaves source intervals unaccounted for')
    if not covers(target_actions, target):
        errors.append('Subject/object motion leaves target intervals unaccounted for')
    return errors
