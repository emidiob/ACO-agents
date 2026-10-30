"""Original SVG composition for portable editable vector handoff."""
from __future__ import annotations

import math
import textwrap
from xml.sax.saxutils import escape


def _lines(value: str, max_chars: int, max_lines: int) -> list[str]:
    lines = textwrap.wrap(value, width=max_chars, break_long_words=True, break_on_hyphens=False)
    if len(lines) > max_lines:
        raise ValueError("Text does not fit vector export; shorten the brief or use HTML")
    return lines


def vector_svg(contract: dict, *, width: int = 1080, height: int = 1080, slide_index: int = 0) -> str:
    if not (600 <= width <= 3840 and 600 <= height <= 3840):
        raise ValueError("Vector dimensions must be in the 600–3840 range")
    if slide_index < 0 or (contract["kind"] != "deck" and slide_index != 0):
        raise ValueError("Slide index is only available for a deck")
    if contract["kind"] == "deck" and slide_index > len(contract["sections"]):
        raise ValueError("Slide index outside deck")
    title = contract["title"]
    description = contract["description"]
    if contract["kind"] == "deck" and slide_index:
        selected = contract["sections"][slide_index - 1]
        title, description = selected["heading"], selected["body"]
    t = contract["tokens"]
    pad = round(width * 0.065)
    title_size = round(min(width * .078, height * .092))
    if len(title) > 65:
        title_size = round(title_size * .7)
    title_char_cap = max(9, int((width - 2 * pad) / (title_size * .58)))
    title_lines = _lines(title, title_char_cap, 6)
    desc_size = round(min(width * .028, height * .034))
    desc_lines = _lines(description, max(14, int((width - 2 * pad) / (desc_size * .57))), 9)
    title_advance = title_size * 1.1
    desc_advance = desc_size * 1.48
    total = len(title_lines) * title_advance + 38 + len(desc_lines) * desc_advance
    y = max(round(height * .28), round((height - total) / 2))
    if y + total > height - pad * 1.4:
        raise ValueError("Text does not fit vector canvas")
    tspan_title = "".join(f'<tspan x="{pad}" dy="{0 if i == 0 else title_advance:.0f}">{escape(line)}</tspan>' for i,line in enumerate(title_lines))
    desc_y = y + title_size + (len(title_lines) - 1) * title_advance + 38
    tspan_desc = "".join(f'<tspan x="{pad}" dy="{0 if i == 0 else desc_advance:.0f}">{escape(line)}</tspan>' for i,line in enumerate(desc_lines))
    brand = escape(contract["audience"])
    kind = escape(contract["kind"].upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<rect width="{width}" height="{height}" fill="{t['background']}"/>
<rect x="{pad}" y="{pad}" width="{round(width*.095)}" height="{round(height*.008)}" fill="{t['accent']}"/>
<text x="{pad}" y="{pad*2}" font-family="Arial, sans-serif" font-weight="700" font-size="{round(width*.018)}" letter-spacing="3" fill="{t['foreground']}">{brand}</text>
<text x="{pad}" y="{y}" font-family="{escape(t['font'])}" font-size="{title_size}" font-weight="700" letter-spacing="-1" fill="{t['foreground']}">{tspan_title}</text>
<text x="{pad}" y="{desc_y}" font-family="Arial, sans-serif" font-size="{desc_size}" fill="{t['foreground']}">{tspan_desc}</text>
<line x1="{pad}" y1="{height-pad*1.35:.0f}" x2="{width-pad}" y2="{height-pad*1.35:.0f}" stroke="{t['accent']}" stroke-width="3"/>
<text x="{pad}" y="{height-pad*.7:.0f}" font-family="Arial, sans-serif" font-size="{round(width*.014)}" fill="{t['foreground']}">ACO OPEN DESIGN / {kind}</text>
</svg>'''
