"""Artifact evidence, not aesthetic self-certification: independent of third-party packs."""
from __future__ import annotations
from pathlib import Path
from .routing import PROFILES
from .core import digest
import shutil, subprocess

REQUIRED_BY_MEDIUM={
 'web':('real rendered desktop screenshot','real rendered mobile screenshot','main action and content check','focus/keyboard check','existing brand preserved'),
 'ui':('rendered working screen','interactive/loading/error/empty states','keyboard/focus evidence','realistic data and sizing','approved design tokens preserved'),
 'image':('viewed final raster/vector/page','source/reference verified','visual hierarchy and specificity critique','image/font/rights record'),
 'photo':('viewed final photograph','composition, light and material critique','camera/crop and artifact inspection','identity and series consistency'),
 'video':('source and final video viewed over full timeline','subject/object/camera movement tracked','contact sheet or timecoded frame notes','continuity and sound review'),
 'motion':('actual animation viewed','intentional timing and spatial continuity','interruptibility and reduced-motion review','performance evidence'),
 'document':('exported pages visually inspected','typographic hierarchy/readability','margins, orphans and image crops','output legibility at target size'),
 'spatial':('actual render or installation photos inspected','scale, lighting and material critique','spatial relationships','technical feasibility noted'),
}

def evidence_gate(packet:dict):
    """Require a verifiable artifact receipt, not only self-reported checkbox flags."""
    if not isinstance(packet,dict):raise ValueError('review packet must be object')
    medium=packet.get('medium')
    if medium not in REQUIRED_BY_MEDIUM:raise ValueError('Unsupported visual medium')
    required=REQUIRED_BY_MEDIUM[medium]
    provided=packet.get('evidence',{})
    if not isinstance(provided,dict):raise ValueError('evidence must be object')
    observations=packet.get('observations',[])
    if not isinstance(observations,list):raise ValueError('observations must be list')
    missing=[item for item in required if not provided.get(item)]
    reviewer=packet.get('reviewed_by')
    user_approved=packet.get('user_approved') is True
    if user_approved and not packet.get('user_approval_source'):
        raise ValueError('user_approved true requires actual approval source')
    receipts=packet.get('artifacts',[])
    if not isinstance(receipts,list):raise ValueError('artifacts must be list')
    valid=[];rejected=[]
    for item in receipts:
        if not isinstance(item,dict):rejected.append('not an object');continue
        path=item.get('path');expected=item.get('sha256')
        if not path or not isinstance(path,str) or not isinstance(expected,str):
            rejected.append('path or SHA-256 missing');continue
        try:
            p=Path(path).expanduser().resolve(strict=True)
            if not p.is_file():raise ValueError('not file')
            if digest(p)!=expected:raise ValueError('hash mismatch')
            if not item.get('viewed_with') or not item.get('review_scope'):
                raise ValueError('actual viewing tool and inspection scope needed')
            valid.append({'path':str(p),'sha256':expected,'viewed_with':item['viewed_with'],'review_scope':item['review_scope']})
        except (OSError,ValueError) as exc:rejected.append(str(exc))
    real_evidence=bool(valid)
    complete=not missing and bool(reviewer) and real_evidence and bool(observations)
    return {'medium':medium,'status':'evidence-supported' if complete else 'review-incomplete',
      'declared_items':sum(bool(provided.get(x)) for x in required),'required_items':len(required),
      'missing':missing,'valid_artifact_receipts':valid,'rejected_artifact_receipts':rejected,
      'reviewed_by':reviewer,'user_approved':user_approved,'aesthetic_quality_certified':False,
      'next_action':'provide actual viewed artifact receipt, specific observations and missing checks' if not complete else 'human review/acceptance if consequential',
      'warnings':['A matching file hash proves identity of an artifact, not that a human loved it',
      'Visual inspection is based on a declared viewing tool/scope; independent reviewer or actual user approval is not implied',
      'Automatic code or source checks never certify aesthetic excellence']}

def media_preflight(path:str):
    p=Path(path).expanduser().resolve(strict=True)
    if not p.is_file():raise ValueError('Missing file')
    ext=p.suffix.lower();out={'file':str(p),'sha256':digest(p),'bytes':p.stat().st_size,'extension':ext,'visually_inspected':False}
    if ext in {'.png','.jpg','.jpeg','.webp','.gif','.tif','.tiff','.bmp'}:
        try:
            from PIL import Image
            with Image.open(p) as im:out['dimensions']=[im.width,im.height];out['mode']=im.mode
        except ImportError:out['dimensions']='Pillow not available';out['requires_manual_visual_inspection']=True
    elif ext in {'.mp4','.mov','.mkv','.webm'}:
        if shutil.which('ffprobe'):
            cp=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],capture_output=True,text=True,timeout=20)
            if cp.returncode==0:
                try:out['duration_seconds']=float(cp.stdout.strip())
                except ValueError:pass
        out['requires_full_timeline_review']=True
    return out

def audit_css(css: str):
    import re
    findings=[]
    def flag(id,severity,msg,evidence):findings.append({'rule':id,'severity':severity,'finding':msg,'evidence':evidence})
    if re.search(r'transition\s*:\s*all\b',css,re.I):flag('motion-all','warning','Transitions should name affected properties','transition: all')
    if re.search(r'(?:transition|animation)[^;}]*\b(?:width|height|top|left|margin|padding)\b',css,re.I):flag('layout-animation','review','Potential layout-bound animation; verify performance','layout property')
    if re.search(r'@keyframes|animation\s*:',css,re.I) and 'prefers-reduced-motion' not in css:flag('reduced-motion','warning','Provide reduced-motion alternative','missing prefers-reduced-motion')
    if re.search(r':hover\b',css) and not re.search(r':focus-visible\b',css):flag('focus-visibility','warning','Inspect keyboard focus where hover is used','hover without focus-visible in provided stylesheet')
    if re.search(r'overflow\s*:\s*hidden',css,re.I):flag('overflow','advisory','Check whether overflow hides useful controls or content','overflow: hidden')
    if re.search(r'(#(?:[0-9a-f]{3}|[0-9a-f]{6})\b)',css,re.I):flag('tokens','advisory','Check whether repeated colors should become project tokens','literal color detected')
    return {'findings':findings,'status':'static-checked','render_verified':False,'warnings':['CSS heuristics do not measure aesthetics or performance','Brand-directed exceptions remain possible']}

def audit_html(source: str):
    import re
    findings=[]
    patterns=[('placeholder-text',r'lorem ipsum|your (amazing|awesome) (product|brand)|\bcoming soon\b','Placeholder text may appear in the deliverable'),('unproven-metrics',r'\b(99\.9%|10,000\+|1,000\+|100k\+)\b','Numeric claims require real source evidence'),('decorative-emoji',r'[🚀✨💎🔥]','Decorative emoji may be unnecessary for this identity')]
    for key,rx,message in patterns:
        if re.search(rx,source,re.I):findings.append({'rule':key,'severity':'review','finding':message})
    if len(re.findall(r'<(?:h[1-6])\b',source,re.I))==0:findings.append({'rule':'heading','severity':'warning','finding':'No heading element found in source'})
    if len(re.findall(r'<main\b',source,re.I))==0:findings.append({'rule':'main','severity':'warning','finding':'No main landmark found in source'})
    return {'status':'static-checked','findings':findings,'visually_verified':False}
