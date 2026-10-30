"""Prepare an external design handoff without contacting a provider."""
from __future__ import annotations

import hashlib
from pathlib import Path

TARGETS = {
    "figma": {"formats": (".svg", ".png", ".pdf"), "operation": "import_design"},
    "canva": {"formats": (".svg", ".png", ".pdf"), "operation": "import_design"},
    "drive": {"formats": (".html", ".svg", ".png", ".pdf"), "operation": "upload_file"},
}


def prepare_handoff(artifact: Path, target: str) -> dict:
    if target not in TARGETS:
        raise ValueError("Unsupported design destination")
    artifact = artifact.resolve(strict=True)
    if not artifact.is_file() or artifact.suffix.lower() not in TARGETS[target]["formats"]:
        raise ValueError("Unsupported artifact format for destination")
    content_sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    return {"schema": "aco-open-design/handoff-v1", "status": "pending_external_action",
            "target": target, "operation": TARGETS[target]["operation"], "artifact": str(artifact),
            "sha256": content_sha, "size_bytes": artifact.stat().st_size,
            "approval_required": True, "provider_receipt": None,
            "note": "Use the actual connected host adapter with scoped approval; this command does not upload."}
