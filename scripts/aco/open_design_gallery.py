"""Original, read-only example catalogue with intentional remix into project briefs."""
from __future__ import annotations

import json
from pathlib import Path


def gallery_path() -> Path:
    return Path(__file__).resolve().parents[2] / "assets/open-design/gallery.json"


def list_examples(kind: str | None = None) -> list[dict]:
    data = json.loads(gallery_path().read_text(encoding="utf-8"))
    if data.get("schema") != "aco-open-design/gallery-v1":
        raise ValueError("Unsupported gallery format")
    examples = data["examples"]
    return [dict(e) for e in examples if kind is None or e["kind"] == kind]


def remix(example_id: str, overrides: dict | None = None) -> dict:
    example = next((x for x in list_examples() if x["id"] == example_id), None)
    if example is None:
        raise ValueError("Unknown example: " + example_id)
    result = {k: v for k, v in example.items() if k != "id"}
    overrides = overrides or {}
    if not isinstance(overrides, dict) or not set(overrides).issubset({"title", "description", "audience", "system", "tokens", "sections", "metrics", "cta", "language"}):
        raise ValueError("Unsupported override keys")
    result.update(overrides)
    return result
