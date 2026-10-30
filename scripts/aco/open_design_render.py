"""Distinct original HTML compositions for four ACO design deliverables."""
from __future__ import annotations

import html
from urllib.parse import urlsplit

from .open_design_systems import contrast_report


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def safe_href(value: str) -> str:
    if value.startswith("#") and len(value) > 1 and all(c.isalnum() or c in "-_" for c in value[1:]):
        return esc(value)
    parts = urlsplit(value)
    if parts.scheme == "https" and parts.netloc and not parts.username and not parts.password:
        return esc(value)
    if parts.scheme == "mailto" and parts.path and "@" in parts.path:
        return esc(value)
    raise ValueError("CTA href must be #anchor, HTTPS or mailto")


CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);line-height:1.52}
.skip{position:absolute;left:-100vw;top:0;padding:.8rem 1rem;background:var(--surface);color:var(--fg);z-index:30}.skip:focus{left:1rem}
a{color:inherit;text-underline-offset:.22em}a:focus-visible{outline:3px solid var(--focus);outline-offset:5px}
header,main,footer{max-width:1200px;margin:auto;padding:clamp(1rem,4vw,3rem)}
header{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
.eyebrow{font:700 .75rem system-ui,sans-serif;letter-spacing:.13em;text-transform:uppercase}
.logo{font-weight:800;letter-spacing:-.04em}.display{font-size:clamp(3rem,8vw,7.5rem);line-height:1.01;letter-spacing:-.055em;max-width:14ch;margin:2rem 0 1.5rem;overflow-wrap:anywhere}
.intro{font-size:clamp(1.15rem,2.4vw,1.65rem);max-width:47rem}.rule{width:5rem;border-top:5px solid var(--accent)}
h2{font-size:clamp(1.5rem,3vw,2.7rem);line-height:1.12;letter-spacing:-.02em}h3{line-height:1.2}p{max-width:70ch}
.sections{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1rem;margin:4rem 0}
.panel{background:var(--surface);padding:clamp(1.4rem,3vw,2.4rem);border:1px solid color-mix(in srgb,var(--fg) 15%,transparent);min-width:0}
.panel p{margin-bottom:0}.action{display:inline-block;margin:1rem 0;padding:.9rem 1.3rem;border:2px solid var(--fg);font:700 .875rem system-ui,sans-serif;text-decoration:none}
.dashboard{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1rem}.dashboard>.panel{grid-column:span 6}
.metric{grid-column:span 4!important;min-height:165px}.metric .value{font:700 clamp(2rem,4.5vw,4.5rem) system-ui,sans-serif;letter-spacing:-.04em;line-height:1.2}.metric small{display:block;margin-top:.7rem}
.dashboard-head{border-bottom:2px solid var(--fg);padding-bottom:1.5rem;margin-bottom:2rem}
.deck{max-width:none;padding:0}.slide{min-height:100svh;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(1.5rem,6vw,5rem);border-bottom:2px solid var(--fg);break-after:page}
.slide-number{font:700 .85rem system-ui,sans-serif;letter-spacing:.14em}.slide h1,.slide h2{font-size:clamp(2.5rem,7vw,7rem);max-width:15ch;margin:2rem 0}.slide p{font-size:clamp(1.15rem,2.4vw,1.9rem);max-width:40rem}
.social-wrap{display:grid;place-items:center;min-height:80svh}.poster{background:var(--surface);width:min(100%,780px);aspect-ratio:1/1;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(1.5rem,5vw,4rem);border:2px solid var(--fg);overflow:hidden}
.poster h1{font-size:clamp(3.3rem,9vw,7rem);line-height:.97;letter-spacing:-.055em;overflow-wrap:anywhere;margin:1rem 0;max-width:10ch}.poster p{font-size:clamp(1rem,2vw,1.5rem)}
footer{font:600 .75rem system-ui,sans-serif;opacity:.75}
@media(max-width:660px){.dashboard>.panel,.metric{grid-column:span 12!important}.slide{min-height:90svh}.deck .display{font-size:clamp(2.8rem,10vw,4.5rem)}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{margin:0;size:A4 landscape}body{print-color-adjust:exact;-webkit-print-color-adjust:exact}.skip,header,footer{display:none!important}.slide{min-height:100vh;break-after:page}.poster{border:none}.social-wrap{min-height:0}}
"""


def _cta(contract):
    cta = contract.get("cta")
    if not cta:
        return ""
    return f'<a class="action" href="{safe_href(cta["href"])}">{esc(cta["label"])}</a>'


def _landing(contract):
    sections = "".join(f'<section class="panel" id="feature-{i+1}"><span class="eyebrow">{i+1:02}</span><h2>{esc(s["heading"])}</h2><p>{esc(s["body"])}</p></section>' for i, s in enumerate(contract["sections"]))
    return (f'<main id="main"><div class="rule" aria-hidden="true"></div><h1 class="display">{esc(contract["title"])}</h1>'
            f'<p class="intro">{esc(contract["description"])}</p>{_cta(contract)}<div class="sections" id="features">{sections}</div></main>')


def _dashboard(contract):
    metrics = "".join(f'<section class="panel metric"><div class="eyebrow">{esc(m["label"])}</div><div class="value">{esc(m["value"])}</div><small>{esc(m.get("detail", ""))}</small></section>' for m in contract["metrics"])
    sections = "".join(f'<section class="panel"><h2>{esc(s["heading"])}</h2><p>{esc(s["body"])}</p></section>' for s in contract["sections"])
    return f'<main id="main"><div class="dashboard-head"><h1>{esc(contract["title"])}</h1><p>{esc(contract["description"])}</p></div><div class="dashboard">{metrics}{sections}</div></main>'


def _deck(contract):
    cover = (f'<section class="slide"><div class="slide-number">01 / {len(contract["sections"]) + 1:02} · {esc(contract["audience"])}</div>'
             f'<div><div class="rule" aria-hidden="true"></div><h1>{esc(contract["title"])}</h1><p>{esc(contract["description"])}</p></div><div class="slide-number">ACO DESIGN / PRESENTATION</div></section>')
    slides = "".join(f'<section class="slide"><div class="slide-number">{i+2:02} / {len(contract["sections"]) + 1:02}</div><div><h2>{esc(s["heading"])}</h2><p>{esc(s["body"])}</p></div><div class="rule" aria-hidden="true"></div></section>' for i,s in enumerate(contract["sections"]))
    return f'<main id="main" class="deck">{cover}{slides}</main>'


def _social(contract):
    note = contract["sections"][0]["body"] if contract["sections"] else contract["description"]
    return (f'<main id="main" class="social-wrap"><article class="poster" aria-label="Social design composition">'
            f'<div class="eyebrow">{esc(contract["audience"])}</div><div><div class="rule" aria-hidden="true"></div>'
            f'<h1>{esc(contract["title"])}</h1><p>{esc(contract["description"])}</p></div>'
            f'<div class="eyebrow">{esc(note)}</div></article></main>')


LAYOUTS = {"landing": _landing, "dashboard": _dashboard, "deck": _deck, "social": _social}


def render(contract: dict) -> str:
    tokens = contract["tokens"]
    css_tokens = ";".join(f"--{key}:{value}" for key, value in (("bg",tokens["background"]), ("fg",tokens["foreground"]),
              ("accent", tokens["accent"]), ("focus", tokens["accent"]), ("surface",tokens["surface"]), ("font",tokens["font"])))
    body = LAYOUTS[contract["kind"]](contract)
    lang = esc(contract.get("language", "en"))
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="description" content="{esc(contract["description"])}"><title>{esc(contract["title"])}</title>'
            f'<style>:root{{{css_tokens}}}{CSS}</style></head><body><a class="skip" href="#main">Skip to content</a>'
            f'<header><span class="logo">ACO / OPEN DESIGN</span><span class="eyebrow">{esc(contract["audience"])}</span></header>'
            f'{body}<footer>Original ACO prototype · {esc(contract["kind"])} · Design system: {esc(contract["system"])}</footer></body></html>')
