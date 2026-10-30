"""Browser-based export. No browser download or installation is performed."""
from __future__ import annotations

import shutil
import re
import subprocess
from pathlib import Path


def available_browser(path: str | None = None) -> str | None:
    if path:
        candidate = Path(path).expanduser().resolve()
        if not candidate.is_file():
            raise FileNotFoundError("Browser executable does not exist: " + str(candidate))
        return str(candidate)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome", "msedge"):
        result = shutil.which(name)
        if result:
            return result
    return None


def export_artifact(source: Path, target: Path, *, browser: str | None = None,
                    width: int = 1440, height: int = 900, overwrite: bool = False) -> dict:
    source = source.resolve(strict=True)
    target = target.resolve()
    if not source.is_file() or source.suffix.lower() not in (".html", ".svg"):
        raise ValueError("Source must be a local HTML or SVG file")
    fmt = target.suffix.lower()
    if fmt not in (".pdf", ".png"):
        raise ValueError("Export supports PDF or PNG")
    if source == target:
        raise ValueError("Export target must differ from source")
    if target.exists() and not overwrite:
        raise FileExistsError("Export already exists; explicit overwrite required")
    if not (320 <= width <= 3840 and 320 <= height <= 3840):
        raise ValueError("Viewport dimensions outside 320–3840")
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".svg":
        if source.stat().st_size > 5_000_000:
            raise ValueError("SVG source too large for this local exporter")
        content = source.read_text(encoding="utf-8").lower()
        if re.search(r"<!doctype|<!entity|<script|<image|<foreignobject|\bhref\s*=|url\s*\(", content):
            raise ValueError("SVG contains external or executable content; use an original self-contained ACO vector")
        binary = shutil.which("inkscape")
        if not binary:
            raise RuntimeError("SVG export requires an existing Inkscape executable")
        command = [binary, str(source), "--export-filename=" + str(target)]
        engine = "inkscape"
    else:
        binary = available_browser(browser)
        if not binary:
            raise RuntimeError("HTML export requires an installed Chrome/Chromium/Edge browser")
        command = [binary, "--headless", "--disable-gpu", "--disable-extensions", "--disable-background-networking", "--no-first-run",
                   "--host-resolver-rules=MAP * 0.0.0.0",
                   f"--window-size={width},{height}", "--hide-scrollbars", "--virtual-time-budget=2000"]
        command.append(("--print-to-pdf=" if fmt == ".pdf" else "--screenshot=") + str(target))
        command.append(source.as_uri())
        engine = "browser"
    completed = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if completed.returncode != 0 or not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError("Export failed (exit " + str(completed.returncode) + "): " + completed.stderr[-400:])
    return {"output": str(target), "format": fmt[1:], "bytes": target.stat().st_size,
            "engine": engine, "visual_quality_reviewed": False}
