"""Original ACO taste-deepening checks; stdlib only, no third-party code bundled.

These are *evidence* checks, not a visual aesthetic model. Neither metadata nor
self-reported review can certify a rendered artifact's quality.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re


STRUCTURAL = ("structure", "imagery_role", "content_sequence", "interaction_model", "hierarchy")


def _normalize(value):
    if value is None or value == "":
        return None
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return " ".join(str(value).lower().split())


def evaluate_variants(packet: dict) -> dict:
    """Detect palette-only variants; do not infer visual quality from metadata."""
    if not isinstance(packet, dict):
        raise ValueError("Variant packet must be an object")
    variants = packet.get("directions", packet.get("variants"))
    if not isinstance(variants, list) or not 2 <= len(variants) <= 6:
        raise ValueError("Provide 2–6 directions or variants")
    if any(not isinstance(v, dict) for v in variants):
        raise ValueError("Each variant must be an object")
    ids = [str(v.get("id", f"V{i+1}")) for i, v in enumerate(variants)]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate variant IDs")
    pairs = []
    for i, left in enumerate(variants):
        for j in range(i + 1, len(variants)):
            right = variants[j]
            changed = [field for field in STRUCTURAL if
                       _normalize(left.get(field)) is not None and
                       _normalize(right.get(field)) is not None and
                       _normalize(left[field]) != _normalize(right[field])]
            missing = [field for field in STRUCTURAL if
                       _normalize(left.get(field)) is None or _normalize(right.get(field)) is None]
            # A changed colour, font or mood is not a new composition.
            if "structure" in missing:
                verdict = "unverifiable-structure"
            elif "structure" not in changed:
                verdict = "same-template-risk"
            elif len(changed) < 2:
                verdict = "weak-structural-separation"
            else:
                verdict = "distinct-on-declared-dimensions"
            pairs.append({"left": ids[i], "right": ids[j], "verdict": verdict,
                          "changed_dimensions": changed, "missing_dimensions": missing})
    good = all(p["verdict"] == "distinct-on-declared-dimensions" for p in pairs)
    return {"status": "structurally-distinct-on-paper" if good else "needs-concept-revision",
            "pairwise": pairs, "anchor_confidence": packet.get("anchor_confidence", "not-reported"),
            "requires_rendered_comparison": True, "aesthetic_quality_certified": False,
            "decision": "Proceed to rendered comparisons" if good else
                        "Revise weak/same-template concepts before rendering",
            "caution": "A structural fingerprint is not a screenshot, UX audit or human preference"}


def _tokens(value: str) -> set[str]:
    return {x for x in re.findall(r"[^\W_]+", value.casefold(), flags=re.UNICODE) if len(x) > 1}


def query_feedback(project: str | Path, query: str, *, scope="current-project",
                   aspect: str | None = None, limit: int = 5) -> dict:
    """Read authoritative project feedback without leaking other scopes or rewriting it."""
    if not isinstance(query, str) or not query.strip() or len(query) > 300:
        raise ValueError("A nonempty query up to 300 characters is required")
    if not isinstance(scope, str) or not scope.strip():
        raise ValueError("An explicit scope is required")
    if not isinstance(limit, int) or not 1 <= limit <= 20:
        raise ValueError("limit must be 1..20")
    project = Path(project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project is not a directory")
    journal = project / ".aco-taste" / "feedback.jsonl"
    if journal.is_symlink() or journal.parent.is_symlink():
        raise ValueError("Refusing symlinked feedback journal")
    rows = []
    if journal.exists():
        for line_number, line in enumerate(journal.read_text(encoding="utf-8").splitlines(), 1):
            try:
                row = json.loads(line)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid feedback at line {line_number}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"Feedback object expected at line {line_number}")
            rows.append(row)
    words = _tokens(query)
    matches = []
    for row in rows:
        if row.get("scope") != scope:
            continue
        aspects = row.get("aspects") if isinstance(row.get("aspects"), list) else []
        if aspect and aspect.casefold() not in [str(a).casefold() for a in aspects]:
            continue
        haystack = " ".join(str(x) for x in [row.get("reason", ""), row.get("variant_id", ""), *aspects])
        score = len(words & _tokens(haystack))
        if not score:
            continue
        matches.append({"id": row.get("id"), "variant_id": row.get("variant_id"),
                        "judgment": row.get("judgment"), "reason": row.get("reason"),
                        "aspects": aspects, "time": row.get("time"), "artifact": row.get("artifact"),
                        "scope": scope, "query_overlap": score})
    matches.sort(key=lambda x: (x["query_overlap"], str(x["time"] or "")), reverse=True)
    return {"status": "scoped-matches" if matches else "no-scoped-match", "scope": scope,
            "query": query, "total_matches": len(matches), "evidence": matches[:limit],
            "memory_updated": False, "model_trained": False,
            "caution": "Evidence is contextual, potentially contradictory, and not a universal style rule"}


def _receipt(obj):
    if not isinstance(obj, dict):
        return None, "missing receipt"
    path, expected = obj.get("path"), obj.get("sha256")
    if not isinstance(path, str) or not isinstance(expected, str):
        return None, "path or SHA-256 missing"
    if not obj.get("viewed_with") or not obj.get("review_scope"):
        return None, "viewing tool and review scope missing"
    try:
        candidate = Path(path).expanduser()
        if candidate.is_symlink():
            raise ValueError("symlink refused")
        p = candidate.resolve(strict=True)
        if not p.is_file():
            raise ValueError("not a file")
        h = hashlib.sha256()
        with p.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(chunk)
        if h.hexdigest() != expected:
            raise ValueError("hash mismatch")
        return {"sha256": expected, "viewed_with": obj["viewed_with"],
                "review_scope": obj["review_scope"]}, None
    except (OSError, ValueError) as exc:
        return None, str(exc)


def check_review_cycle(packet: dict) -> dict:
    """Trace before/after review evidence; matching receipts alone cannot verify a fix."""
    if not isinstance(packet, dict):
        raise ValueError("Review cycle packet must be an object")
    findings = packet.get("findings")
    if not isinstance(findings, list) or not 1 <= len(findings) <= 30:
        raise ValueError("Provide 1–30 review findings")
    result = []
    for index, item in enumerate(findings):
        if not isinstance(item, dict):
            raise ValueError("Review finding must be an object")
        before, err1 = _receipt(item.get("before"))
        after, err2 = _receipt(item.get("after"))
        note = str(item.get("observed_result") or "").strip()
        correction = str(item.get("correction") or "").strip()
        same = bool(before and after and before["sha256"] == after["sha256"])
        issues = [x for x in (err1, err2) if x]
        if not correction:
            issues.append("correction missing")
        if not note:
            issues.append("observed result missing")
        if not item.get("region_or_timecode"):
            issues.append("region or timecode missing")
        if same:
            issues.append("before and after artifacts identical")
        result.append({"id": item.get("id", f"F{index+1}"),
                       "severity": item.get("severity", "unspecified"),
                       "status": "receipt-supported-needs-visual-judgment" if not issues else "incomplete",
                       "issues": issues, "observed_result": note})
    complete = all(f["status"].startswith("receipt-supported") for f in result)
    return {"status": "receipt-supported" if complete else "review-incomplete",
            "findings": result, "aesthetic_quality_certified": False,
            "human_approval_inferred": False,
            "caution": "Hashes establish artifact identity; viewed_with and observations are declarations, not automated visual inspection"}


def motion_triage(packet: dict) -> dict:
    """Decision-first UI motion gate, not a replacement for playback testing."""
    if not isinstance(packet, dict):
        raise ValueError("Motion packet must be an object")
    frequency = packet.get("frequency")
    if frequency not in {"very-frequent", "frequent", "occasional", "rare"}:
        raise ValueError("frequency must be very-frequent, frequent, occasional or rare")
    trigger = packet.get("trigger", "pointer")
    if trigger not in {"keyboard", "pointer", "gesture", "automatic", "system"}:
        raise ValueError("Invalid motion trigger")
    purpose = str(packet.get("purpose") or "").strip()
    if trigger == "keyboard" or frequency == "very-frequent":
        return {"decision": "do-not-animate", "why": "High-frequency or keyboard action must remain immediate",
                "playback_verified": False}
    if not purpose:
        return {"decision": "do-not-animate", "why": "No functional motion purpose supplied",
                "playback_verified": False}
    findings = []
    if packet.get("reduced_motion") is not True:
        findings.append("Provide a reduced-motion alternative")
    duration = packet.get("duration_ms")
    if duration is not None:
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError("duration_ms must be nonnegative number")
        if duration > 300:
            findings.append("Review UI duration over 300ms against interaction frequency and task")
    properties = packet.get("properties", [])
    if not isinstance(properties, list):
        raise ValueError("properties must be a list")
    risky = {"width", "height", "top", "left", "margin", "padding"}
    if any(str(p).lower() in risky for p in properties):
        findings.append("Inspect layout-bound properties; prefer transform/opacity where appropriate")
    return {"decision": "revise-before-implementation" if findings else "candidate-for-rendered-review",
            "why": purpose, "findings": findings, "playback_verified": False,
            "caution": "This is a UI interaction heuristic, not a film/motion graphics timing rule"}
