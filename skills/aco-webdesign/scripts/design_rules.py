"""Original ACO design-review predicates. Not a classifier of authorship."""
import math
import re

def rgb(value):
    value=value.strip().lower()
    if '%' in value:return None
    if re.fullmatch(r'#[0-9a-f]{6}',value):return tuple(int(value[i:i+2],16) for i in (1,3,5))
    m=re.fullmatch(r'rgba?\(([^)]+)\)',value)
    if not m:return None
    values=re.findall(r'[-+]?[0-9]*\.?[0-9]+',m.group(1))
    if len(values) not in (3,4):return None
    if len(values)==4 and float(values[3])!=1:return None
    return tuple(float(x) for x in values[:3])
def colors(value):
    return [c for text in re.findall(r'rgba?\([^)]+\)|#[0-9a-fA-F]{6}',value) if (c:=rgb(text)) is not None]
def chroma(c):return max(c)-min(c) if c else 0
def cool(c):return c[2]>c[0]*1.15 and c[2]>100 or c[1]>150 and c[2]>150 and c[0]<100
def warm(value):
    c=rgb(value);return c is not None and c[0]>220 and c[0]>=c[1]>c[2] and 8<c[0]-c[2]<55
def contrast(a,b):
    a,b=rgb(a),rgb(b)
    if a is None or b is None:return None
    def lum(c):
        c=[v/255 for v in c];c=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
        return sum(x*y for x,y in zip(c,(.2126,.7152,.0722)))
    x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)
def card(e):return e.get('radius',0)>=4 and (max(e.get('borders',[0]))>0 or e.get('shadow','none')!='none')
def animated(e):return e.get('animation','none') not in ('none','') and e.get('animationDuration','0s')!='0s'
def kicker(e):
    text=e.get('text','');return 0<len(text)<70 and e.get('fontSize',16)<=14 and (e.get('textTransform')=='uppercase' or text.isupper()) and e.get('letterSpacing',0)>=1
def shadows(value):
    out=[]
    value=re.sub(r'rgba?\([^)]+\)|#[0-9a-fA-F]+','',value)
    for part in value.split(','):
        nums=[float(x) for x in re.findall(r'(-?\d+(?:\.\d+)?)px',part)]
        if len(nums)>=3:out.append(tuple(nums[:3]))
    return out
def overshoot(value):
    for raw in re.findall(r'cubic-bezier\(([^)]+)\)',value):
        nums=[float(x.strip()) for x in raw.split(',')]
        if len(nums)==4 and (nums[1]<0 or nums[1]>1 or nums[3]<0 or nums[3]>1):return True
    return bool(re.search(r'bounce|elastic',value,re.I))

def rule_0(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(max(e.get('borders',[0]))>=4 and min(e.get('borders',[0]))<2)

def rule_1(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('radius',0)>=8 and max(e.get('borders',[0]))>=4)

def rule_2(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(re.search(r'\b(inter|roboto|geist|space grotesk|fraunces)\b',e.get('fontFamily',''),re.I)))

def rule_3(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h1','h2','h3') and body_size>0 and e.get('fontSize',0)/body_size<1.25)

def rule_4(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool('text' in e.get('backgroundClip','') and 'gradient(' in e.get('backgroundImage',''))

def rule_5(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(e.get('backgroundImage','').count('gradient')) and any(cool(c) for c in colors(e.get('backgroundImage',''))))

def rule_6(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('body','main') and warm(e.get('background','')))

def rule_7(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(card(e) and card(parent))

def rule_8(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='main' and len(spaces)>=5 and len(set(spaces))==1)

def rule_9(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(overshoot(e.get('timing','')))

def rule_10(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(0<e.get('width',0)<=20 and 0<e.get('height',0)<=20 and animated(e))

def rule_11(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('text','').strip() in ('|','▌','_') and e.get('tag') not in ('input','textarea') and animated(e))

def rule_12(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='svg' and e.get('primitiveCount',0)>=15 and e.get('width',0)>240)

def rule_13(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool('path(' in e.get('clipPath','') or ('polygon(' in e.get('clipPath','') and e['clipPath'].count(',')>10))

def rule_14(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool((e.get('tag')=='img' or 'url(' in e.get('backgroundImage','')) and e.get('opacity',1)<0.1)

def rule_15(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(any(max(abs(x),abs(y))>=4 and blur==0 for x,y,blur in shadows(e.get('shadow',''))))

def rule_16(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(any(blur>=12 for x,y,blur in shadows(e.get('shadow',''))) and any(chroma(c)>45 for c in colors(e.get('shadow',''))))

def rule_17(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool('radial-gradient(' in e.get('backgroundImage','') and any(chroma(c)>80 for c in colors(e.get('backgroundImage',''))))

def rule_18(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool('radial-gradient(' in e.get('backgroundImage','') and ('transparent' in e.get('backgroundImage','') or 'rgba(' in e.get('backgroundImage','')))

def rule_19(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='marquee' or (animated(e) and bool(re.search('marquee|scroll|ticker',e.get('animation',''),re.I))))

def rule_20(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h2','h3') and previous.get('hasIcon',False) and 16<=previous.get('width',0)<=80 and previous.get('radius',0)>=4)

def rule_21(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h1','h2') and e.get('fontSize',0)>=48 and e.get('fontStyle')=='italic' and 'serif' in e.get('fontFamily','') and 'sans-serif' not in e.get('fontFamily',''))

def rule_22(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='h1' and kicker(previous))

def rule_23(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h2','h3','h4') and kicker(previous))

def rule_24(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('fontSize',16)<14 and bool(re.fullmatch(r'\s*\d{1,2}[./—-]?\s*',e.get('text',''))))

def rule_25(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(len(e.get('text',''))>=100 and e.get('text','').count('—')>=8 and len(e['text'])/e['text'].count('—')<=500)

def rule_26(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(re.search(r'\b(streamline|supercharge|world.class|cutting.edge|next.generation|empower)\b',e.get('text',''),re.I)))

def rule_27(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(len(re.findall(r'(?:^|[.!?])\s*(?:Not|No|Just)\b',e.get('text','')))>=3)

def rule_28(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='h1' and len(e.get('text','').split())>=8 and e.get('fontSize',0)>min(96,width*0.12))

def rule_29(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('letterSpacing',0)<-0.055*e.get('fontSize',16))

def rule_30(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='img' and (not e.get('src') or (e.get('imageComplete') is True and e.get('naturalWidth')==0)))

def rule_31(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='body' and bool(snapshot.get('scriptErrors')))

def rule_32(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(len(e.get('text',''))>80 and (e.get('opacity',1)==0 or e.get('visibility')=='hidden') and e.get('display')!='none')

def rule_33(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(card(e) and parent.get('overflowX') in ('auto','scroll','hidden') and abs(e.get('left',0)-parent.get('left',0))<2)

def rule_34(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(e.get('text')) and e.get('occluded') is True)

def rule_35(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(parent.get('display') in ('grid','flex') and e.get('top',9999)<100 and e.get('height',0)>height and len(e.get('text',''))>120)

def rule_36(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(e.get('text')) and rgb(e.get('color','')) is not None and chroma(rgb(e['color']))<12 and rgb(e.get('effectiveBackground','')) is not None and chroma(rgb(e['effectiveBackground']))>65)

def rule_37(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(e.get('text')) and contrast(e.get('color',''),e.get('effectiveBackground','')) is not None and contrast(e['color'],e['effectiveBackground']) < (3 if e.get('fontSize',16)>=24 or (e.get('fontSize',16)>=18.66 and e.get('fontWeight',400)>=700) else 4.5))

def rule_38(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and len(e.get('text',''))>100 and e.get('width',0)/max(e.get('fontSize',16)*0.5,1)>90)

def rule_39(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(card(e) and len(e.get('text',''))>30 and min(e.get('padding',[99]))<8)

def rule_40(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and len(e.get('text',''))>40 and (e.get('left',99)<8 or width-e.get('right',0)<8))

def rule_41(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and 0<e.get('lineHeightPx',0)<1.3*e.get('fontSize',16))

def rule_42(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(e.get('headingGap')))

def rule_43(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h2','h3','h4') and previous.get('tag')=='p' and 0<=e.get('top',9999)-previous.get('bottom',0)<8)

def rule_44(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and e.get('textAlign')=='justify')

def rule_45(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(len(e.get('lineWidths',[]))>=3 and 0<e['lineWidths'][-1]<0.2*max(e['lineWidths']))

def rule_46(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('h1','h2','h3') and len(e.get('lineWidths',[]))>=2 and min(e['lineWidths'])<0.3*max(e['lineWidths']))

def rule_47(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and 0<e.get('fontSize',16)<12)

def rule_48(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag') in ('button','label','input','select','textarea') and 0<e.get('fontSize',16)<12)

def rule_49(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and len(e.get('text',''))>80 and (e.get('textTransform')=='uppercase' or e.get('text','').isupper()))

def rule_50(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('tag')=='p' and e.get('letterSpacing',0)>0.12*e.get('fontSize',16))

def rule_51(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('scrollWidth',0)>e.get('clientWidth',0)+2 and e.get('overflowX') not in ('auto','scroll'))

def rule_52(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(len(e.get('text',''))>20 and sibling_texts.count(e.get('text'))>=3)

def rule_53(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('position') in ('absolute','fixed') and parent.get('overflowX') in ('hidden','clip') and (e.get('left',0)<parent.get('left',0) or e.get('right',0)>parent.get('right',0)))

def rule_54(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(system.get('fonts')) and e.get('fontFamily','').split(',')[0].strip(' \"\'') not in system['fonts'])

def rule_55(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(system.get('colors')) and bool(e.get('text')) and rgb(e.get('color','')) is not None and rgb(e['color']) not in [rgb(c) for c in system['colors']])

def rule_56(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(system.get('radii')) and e.get('radius',0)>0 and e['radius'] not in system['radii'])

def rule_57(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(system.get('fontSizes')) and bool(e.get('text')) and e.get('fontSize',16) not in system['fontSizes'])

def rule_58(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(0<max(e.get('borders',[0]))<=1 and any(blur>=32 for x,y,blur in shadows(e.get('shadow',''))))

def rule_59(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool('repeating-linear-gradient(' in e.get('backgroundImage',''))

def rule_60(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(e.get('backgroundImage','').count('linear-gradient(')>=2 and e.get('backgroundSize') not in (None,'auto','auto, auto'))

def rule_61(e,parent,previous,snapshot,system,body_size,spaces,width,height,sibling_texts):
    return bool(bool(re.search(r'\b(the stage is set|step into the spotlight|take center stage|the curtain rises)\b',e.get('text',''),re.I)))

RULES = [
    ('accent-edge', 'One border dominates a surface', 'border', rule_0),
    ('rounded-accent', 'Strong border and curved corners', 'border', rule_1),
    ('common-font', 'Review whether the typeface suits the brief', 'type', rule_2),
    ('flat-hierarchy', 'Heading and body sizes have little separation', 'type', rule_3),
    ('gradient-ink', 'Text uses a gradient fill', 'style', rule_4),
    ('charged-palette', 'Saturated cool colors compete for attention', 'style', rule_5),
    ('warm-ground', 'Review the contextual purpose of a warm neutral ground', 'style', rule_6),
    ('nested-surfaces', 'Multiple nested framed surfaces', 'layout', rule_7),
    ('uniform-spacing', 'Repeated groups use the same spacing everywhere', 'layout', rule_8),
    ('overshoot-easing', 'Motion timing overshoots the settled state', 'motion', rule_9),
    ('animated-status', 'A small status marker animates continuously', 'motion', rule_10),
    ('decorative-caret', 'A non-editable element resembles an animated caret', 'motion', rule_11),
    ('primitive-scene', 'A large SVG uses many primitive shapes', 'media', rule_12),
    ('complex-clip', 'Complex clipping needs visual review', 'style', rule_13),
    ('dim-image', 'A raster image is almost invisible', 'media', rule_14),
    ('hard-shadow', 'Review the intentional use of displaced hard shadows', 'style', rule_15),
    ('colored-glow', 'Colored shadow creates a halo', 'style', rule_16),
    ('radial-wash', 'Saturated radial background wash', 'style', rule_17),
    ('radial-spotlight', 'A fading radial decoration sits behind content', 'style', rule_18),
    ('moving-banner', 'Continuously moving banner needs a pause strategy', 'motion', rule_19),
    ('icon-above-title', 'Repeated icon-over-heading composition', 'layout', rule_20),
    ('italic-display', 'Large italic serif display needs contextual review', 'type', rule_21),
    ('hero-label', 'Small label competes with the hero title', 'type', rule_22),
    ('heading-label', 'A heading has a separate tracked uppercase label', 'type', rule_23),
    ('section-index', 'Small section indexes may add redundant structure', 'type', rule_24),
    ('dash-density', 'Long dashes dominate the prose rhythm', 'copy', rule_25),
    ('vague-promise', 'Copy makes a generic promise instead of naming a benefit', 'copy', rule_26),
    ('rebuttal-pattern', 'Repeated short rebuttals deserve an editorial pass', 'copy', rule_27),
    ('large-sentence-title', 'Long title dominates the viewport', 'type', rule_28),
    ('compressed-tracking', 'Negative tracking may harm legibility', 'type', rule_29),
    ('failed-image', 'Image has no loaded raster', 'media', rule_30),
    ('runtime-error', 'Browser reported a JavaScript error', 'runtime', rule_31),
    ('invisible-content', 'Substantial content remains invisible', 'layout', rule_32),
    ('scroll-edge', 'Framed content touches the clipping edge', 'layout', rule_33),
    ('covered-text', 'Text is overlapped at a sampled visible point', 'layout', rule_34),
    ('tall-first-column', 'One column pushes introductory content below the fold', 'layout', rule_35),
    ('neutral-on-color', 'Neutral text sits on a chromatic background', 'color', rule_36),
    ('text-contrast', 'Opaque text/background contrast is below the text-size threshold', 'color', rule_37),
    ('long-measure', 'Text measure is unusually long', 'type', rule_38),
    ('tight-container', 'A framed text container has very small padding', 'layout', rule_39),
    ('viewport-text-edge', 'Body copy is too close to the viewport edge', 'layout', rule_40),
    ('tight-lines', 'Paragraph line height is tight', 'type', rule_41),
    ('heading-level-gap', 'Heading order skips a level', 'structure', rule_42),
    ('heading-top-gap', 'Heading is crowded against preceding content', 'layout', rule_43),
    ('justified-prose', 'Justified paragraphs can create uneven word spacing', 'type', rule_44),
    ('orphan-word', 'Last text line contains a single word', 'type', rule_45),
    ('uneven-title', 'Heading lines have a large width imbalance', 'type', rule_46),
    ('tiny-prose', 'Body copy is unusually small', 'type', rule_47),
    ('tiny-control-copy', 'Functional labels are unusually small', 'type', rule_48),
    ('uppercase-paragraph', 'Extended prose uses uppercase', 'type', rule_49),
    ('wide-prose-tracking', 'Body copy uses very wide tracking', 'type', rule_50),
    ('container-overflow', 'Content exceeds its container', 'layout', rule_51),
    ('duplicate-copy', 'Repeated sibling copy may be accidental', 'copy', rule_52),
    ('clipped-position', 'Positioned child extends beyond a clipping ancestor', 'layout', rule_53),
    ('system-font', 'Typeface is outside the supplied design system', 'system', rule_54),
    ('system-color', 'Text color is outside the supplied design system', 'system', rule_55),
    ('system-radius', 'Corner radius is outside the supplied scale', 'system', rule_56),
    ('system-type-size', 'Type size is outside the supplied scale', 'system', rule_57),
    ('fine-border-large-shadow', 'A fine border combines with a very wide shadow', 'style', rule_58),
    ('stripe-background', 'Repeating stripes need contextual review', 'style', rule_59),
    ('grid-background', 'Intersecting gradient lines form a decorative grid', 'style', rule_60),
    ('theatrical-copy', 'Copy uses theatrical framing instead of specific information', 'copy', rule_61),
]
