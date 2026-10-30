"""Original ACO design tokens, user overrides and accessible contrast diagnostics."""
from __future__ import annotations

import json
import re
from pathlib import Path

SYSTEMS = {
    "editorial": {"background": "#f5f2eb", "foreground": "#20201e", "accent": "#b33427", "surface": "#fffdfa", "font": "Georgia, serif"},
    "utility": {"background": "#f4f6f9", "foreground": "#16202d", "accent": "#2451ad", "surface": "#ffffff", "font": "system-ui, sans-serif"},
    "dark": {"background": "#14191a", "foreground": "#f0f1ee", "accent": "#c5ed64", "surface": "#23292a", "font": "system-ui, sans-serif"},
    "minimal": {"background": "#ffffff", "foreground": "#121212", "accent": "#304b7d", "surface": "#f3f3f0", "font": "system-ui, sans-serif"},
    "forest": {"background": "#e9eee5", "foreground": "#1d3428", "accent": "#236646", "surface": "#f9faf6", "font": "Georgia, serif"},
    "electric": {"background": "#172bc5", "foreground": "#ffffff", "accent": "#e4ff71", "surface": "#253acb", "font": "system-ui, sans-serif"},
    "ink": {"background": "#ebe1d1", "foreground": "#241d20", "accent": "#713137", "surface": "#faf3e8", "font": "Georgia, serif"},
}
COLORS = ("background", "foreground", "accent", "surface")
FONTS = {"Georgia, serif", "system-ui, sans-serif", "Arial, sans-serif", "Verdana, sans-serif", "Times New Roman, serif"}


def validate_tokens(data: dict) -> dict:
    if not isinstance(data, dict) or set(data) != set(COLORS) | {"font"}:
        raise ValueError("Design system must declare background, foreground, accent, surface and font")
    for name in COLORS:
        if not isinstance(data[name], str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", data[name]):
            raise ValueError("Invalid CSS hex color: " + name)
    if data["font"] not in FONTS:
        raise ValueError("Unsupported font stack; use approved built-in values")
    return {k: data[k] for k in (*COLORS, "font")}


def resolve_system(system="editorial", custom: dict | None = None) -> dict:
    if custom is not None:
        return validate_tokens(custom)
    if system not in SYSTEMS:
        raise ValueError("Unknown design system: " + str(system))
    return dict(SYSTEMS[system])


def _luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(a * b for a, b in zip((0.2126, 0.7152, 0.0722), linear))


def contrast(a, b):
    light, dark = sorted((_luminance(a), _luminance(b)), reverse=True)
    return round((light + 0.05) / (dark + 0.05), 2)


def contrast_report(tokens):
    result = {"body": contrast(tokens["foreground"], tokens["background"]),
              "panel": contrast(tokens["foreground"], tokens["surface"])}
    return {"ratios": result, "wcag_aa_normal_text_candidate": all(v >= 4.5 for v in result.values()),
            "note": "Color-ratio check only; not a complete WCAG conformance audit."}


def load_system(path: str | Path) -> dict:
    return validate_tokens(json.loads(Path(path).read_text(encoding="utf-8")))
