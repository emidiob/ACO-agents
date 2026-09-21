# Studio readiness checks

These commands are optional, side-effect-free consistency checks. They perform **no network calls, file writes, source verification, scheduling, publication or professional judgement**. Their result `ready_for_review` means no structural blocker was found in the supplied data. It is not authorization or proof of truth. The host must inspect the real records, permissions and outcomes.

Use natural conversation first. The assistant may assemble JSON when a structured check materially helps. Do not make every user complete a form.

## 1. Local capability presence

```bash
python3 scripts/aco_cli.py capability-audit
```

A fixed allowlist is looked up with `shutil.which`: Git, Python, FFmpeg/ffprobe, Pandoc, Quarto, oiiotool, Gitleaks, Semgrep, Promptfoo and Lighthouse. No binary is run; no token or configuration file is read. `found: true` means a PATH entry was found, not that the program works or is safe. Remote accounts are `not_checked`.

Use actual host connector discovery for connected tools. Obtain a fresh provider snapshot only from a real read/check; do not manufacture it from registry names.

## 2. Artist development plan

```bash
python3 scripts/aco_cli.py practice-check --input examples/studio/practice.json
```

Input fields: `scope_id`, `current_question`, `available_hours_per_week`, optional `other_commitments_hours`, `protected_making_research_hours`, `review_date`; `priorities` contains one to three objects with `id`, `title`, `next_action`, `learning_signal`, `category` (making/research/career/revenue/operations), and `hours_per_week`.

Capacity is the total time budget before subtracting `other_commitments_hours`. Do not deduct the same commitments twice. Decimal arithmetic rejects negative, non-finite and Boolean numbers. Checks include duplicate IDs, oversubscription and protected making/research time. It does not grade art, predict grants or create calendar events.

## 3. Opportunity fit

```bash
python3 scripts/aco_cli.py opportunity-check --input examples/studio/opportunity.json --as-of 2026-09-20T12:00:00+00:00
```

The example is fictional. `--as-of` freezes time for tests; live use should use current time and actual fresh sources.

Input: `scope_id`, `title`, `practice_need`, clean HTTPS `official_source`, `source_evidence_ref`, `checked_on`, `cost_support_summary`; explicit eligibility criteria with `result` pass/fail/unknown and evidence references. A fixed deadline needs a timezone-aware `deadline_at`; rolling needs `rolling_evidence_ref`. Attendance/capacity evidence can be recorded as `availability_evidence_ref`.

Review older than seven days or in the future is flagged. This is an ACO conservative recheck threshold, not a provider guarantee. Unknown eligibility is not a pass. A failed criterion or expired deadline prevents recommending submission as eligible. Recommendation remains `consider_with_artist`, `investigate` or `do_not_submit_as_eligible`; no acceptance probability. **Always pipeline-only, never a project-creation trigger.**

## 4. Brand evidence

```bash
python3 scripts/aco_cli.py brand-check --input examples/studio/brand.json
```

Input: scope/brand IDs, objective, audience, proposition; claims with unique IDs, text, support (`assumed`, `researched`, `validated`) and evidence references; `decision_status` proposed/approved with an approval reference if approved. Optional applications and candidate names.

Approval is not validation. A validated label requires evidence but this offline tool cannot authenticate that evidence. Candidate-name clearance can be `not_assessed`, `pending_review` or `professional_review_recorded` with the real review reference. A domain search cannot turn into a trademark-clearance assertion.

## 5. Social publication packet

```bash
python3 scripts/aco_cli.py social-check --input examples/studio/social-draft.json
```

The example is draft-only. A packet requires scope, brand, account, platform, version, action and posts. Each post has a distinct ID and text or media. Media binds to a reviewed SHA-256 digest plus a reference; for intended publication, rights must be confirmed with a reference. Publication claims and privacy/accessibility/disclosure reviews need references.

Scheduling requires a future ISO timestamp with explicit offset plus an IANA timezone. The offset is checked against that date. Changing account, copy, media, version or time changes the packet hash.

For a real publication request, an `approval` object must refer to the exact `packet_sha256`, scope and account with the user approval reference; optional expiry is enforced. A `capability` snapshot must refer to the same scope/account/platform, requested operation, evidence reference, `verified_available` state and timestamp within the last 24 hours. This freshness threshold is a local conservative policy, not proof of remote availability. A prior accepted/sent/scheduled result blocks duplication; a timeout/unknown result requires reconciliation.

**Do not manually invent authorization or capability evidence to satisfy this check.** The exported packet hash is for review binding only, never a bearer credential. A host must check actual bytes, permissions and receipts. The tool always returns `publication_authorized: false`, `provider_called: false`, `executed: false`.

The synthetic test suite deliberately supplies fictional evidence strings to test structure, not real provider access. The distributed example omits any publish approval.

## Exit status and integration

Malformed input raises a clear CLI error. A valid request with blockers returns a JSON report; callers must inspect `status` and `blockers` rather than treating process exit 0 as acceptance. Do not parse a report as automatic permission to call another tool.

All methods preserve compact memory. Save one material decision/result in the existing canonical section only if useful and authorized. Do not create a file per check.
