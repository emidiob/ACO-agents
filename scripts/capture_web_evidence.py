#!/usr/bin/env python3
"""Optional passive browser capture for a trusted, authorized loopback dev site.
Requires separately installed Playwright + Chromium. No dependency installation.
HTTP(S) requests are limited to the exact supplied loopback origin and GET/HEAD.
This guard is NOT a sandbox for malicious JavaScript. Use trusted fixture/dev code.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


def validate_target(url):
    u=urlsplit(url)
    if u.scheme not in ('http','https') or u.hostname not in ('127.0.0.1','localhost','::1') or u.username or u.password:
        raise ValueError('Only a trusted authorized loopback HTTP(S) dev site is supported; no credentials in URL')
    _=u.port
    return u


def capture(url, output, revision, widths=(360,1440), executable=None):
    base=validate_target(url)
    if not isinstance(revision,str) or not revision.strip():raise ValueError('Supply the actual build/revision label')
    if not widths or any(type(w) is not int or w<240 or w>4000 for w in widths) or len(set(widths))!=len(widths):raise ValueError('Unique integer widths between 240 and 4000 are required')
    out=Path(output).absolute()
    for p in (out,*out.parents):
        if p.is_symlink():raise ValueError('No symlink output paths')
    library=Path(__file__).resolve().parents[1]
    if out.resolve().is_relative_to(library):raise ValueError('Store project evidence outside the public ACO library')
    if out.exists():raise ValueError('Output directory already exists; use a fresh run directory')
    try:from playwright.sync_api import sync_playwright
    except ImportError as e:raise RuntimeError('Playwright is not installed; no browser check ran. Install separately only with authorization.') from e
    out.mkdir(parents=True,exist_ok=False);captures=[];blocked=[];console=[]
    with sync_playwright() as p:
        args={'headless':True}
        if executable:args['executable_path']=executable
        browser=p.chromium.launch(**args)
        try:
            context=browser.new_context(viewport={'width':widths[0],'height':900},device_scale_factor=1,locale='en-US',reduced_motion='reduce',service_workers='block',accept_downloads=False)
            def guard(route):
                req=route.request;u=urlsplit(req.url)
                if (u.scheme,u.netloc)==(base.scheme,base.netloc) and req.method in ('GET','HEAD'):route.continue_()
                else:
                    blocked.append({'method':req.method,'target':u.scheme+'://'+u.netloc+u.path});route.abort()
            context.route('**/*',guard)
            page=context.new_page()
            page.on('pageerror',lambda err:console.append(str(err)))
            page.on('dialog',lambda dialog:dialog.dismiss())
            for w in widths:
                page.set_viewport_size({'width':w,'height':900})
                response=page.goto(url,wait_until='load',timeout=20000)
                if response is None or response.status>=400:raise RuntimeError('Dev page did not load successfully')
                page.evaluate('() => document.fonts.ready')
                metric=page.evaluate('''() => ({title:document.title, viewport:innerWidth, scrollWidth:document.documentElement.scrollWidth, missingImageAlt:document.querySelectorAll('img:not([alt])').length})''')
                focus=[]
                for _ in range(3):
                    page.keyboard.press('Tab')
                    focus.append(page.evaluate('''() => ({tag:document.activeElement.tagName,id:document.activeElement.id,role:document.activeElement.getAttribute('role')})'''))
                name=f'viewport-{w}.png';page.screenshot(path=str(out/name),full_page=False)
                captures.append({'width':w,'path':name,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),
                                 'horizontal_overflow_observed':metric['scrollWidth']>w+1,'dom_metrics':metric,'tab_probe':focus})
            context.close()
            report={'status':'captured','revision':revision,'captured_at':datetime.now(timezone.utc).isoformat(),
                    'browser_version':browser.version,'reduced_motion':'reduce','captures':captures,'blocked_requests':blocked,'page_errors':console,
                    'limitations':'Trusted loopback dev pages only. Captures and a three-Tab probe are not full visual, accessibility, functional, performance or security acceptance. Some resources may be blocked. No inputs submitted, remote deployment or provider generation.'}
        finally:browser.close()
    (out/'capture-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--url',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--revision',required=True);p.add_argument('--widths',type=int,nargs='+',default=[360,1440]);p.add_argument('--executable')
    a=p.parse_args()
    try:report=capture(a.url,a.out,a.revision,a.widths,a.executable)
    except Exception as e:
        print(json.dumps({'status':'failed','error':str(e),'note':'No successful capture claimed; preserve any partial files for diagnosis.'}),file=sys.stderr);raise SystemExit(1)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
