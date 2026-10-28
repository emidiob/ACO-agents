() => {
  // ACO read-only DOM probe. Run through the host's authorized browser API.
  // It never clicks, edits, fetches, reads application stores or uploads data.
  const elements = Array.from(document.querySelectorAll('body, body *')).filter(el => { const r=el.getBoundingClientRect(); return getComputedStyle(el).display !== 'none' && r.width>0 && r.height>0; });
  const indices = new Map(elements.map((el, index) => [el, index]));
  let lastHeading = 0;
  const rows = elements.map((el, index) => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    const labelIds = (el.getAttribute('aria-labelledby') || '').trim().split(/\s+/).filter(Boolean);
    const labels = labelIds.map(id => document.getElementById(id)?.textContent || '').join(' ');
    const ownText = Array.from(el.childNodes).filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent).join(' ').trim();
    const name = el.getAttribute('aria-label') || labels || Array.from(el.labels || []).map(x => x.textContent).join(' ') || el.textContent?.trim() || el.getAttribute('alt') || '';
    const px = value => +value.replace('px','') || 0;
    let ancestor = el, effectiveBackground = '';
    while (ancestor) {
      const a = getComputedStyle(ancestor);
      if (a.backgroundImage !== 'none' || +a.opacity < 1 || a.filter !== 'none' || a.backdropFilter && a.backdropFilter !== 'none') break;
      if (/^rgb\(/.test(a.backgroundColor)) { effectiveBackground = a.backgroundColor; break; }
      if (!/^rgba\([^,]+,[^,]+,[^,]+,\s*0\)$/.test(a.backgroundColor)) break;
      ancestor = ancestor.parentElement;
    }
    const level = /^H[1-6]$/.test(el.tagName) ? +el.tagName.slice(1) : 0;
    const headingGap = level && lastHeading && level > lastHeading + 1;
    if (level) lastHeading = level;
    // Geometry is collected only for leaf text. Nested text needs visual review.
    const lineWidths = [];
    if (ownText && !el.children.length) {
      const range = document.createRange(); range.selectNodeContents(el);
      const lines = new Map();
      Array.from(range.getClientRects()).forEach(rect => {
        const key = Math.round(rect.top);
        const prev = lines.get(key);
        lines.set(key, prev ? [Math.min(prev[0],rect.left),Math.max(prev[1],rect.right)] : [rect.left,rect.right]);
      });
      lines.forEach(pair => lineWidths.push(pair[1]-pair[0]));
    }
    const x = r.left+r.width/2, y=r.top+r.height/2;
    const hit = ownText && x>=0 && x<innerWidth && y>=0 && y<innerHeight ? document.elementFromPoint(x,y) : null;
    return {index, parent:indices.get(el.parentElement) ?? null, previous:indices.get(el.previousElementSibling) ?? null,
      top:r.top,bottom:r.bottom,position:s.position,display:s.display,visibility:s.visibility,opacity:+s.opacity,
      fontFamily:s.fontFamily,fontWeight:+s.fontWeight || 400,fontStyle:s.fontStyle,
      letterSpacing:px(s.letterSpacing),lineHeightPx:px(s.lineHeight),textTransform:s.textTransform,textAlign:s.textAlign,
      marginBottom:px(s.marginBottom),padding:[s.paddingTop,s.paddingRight,s.paddingBottom,s.paddingLeft].map(px),
      borders:[s.borderTopWidth,s.borderRightWidth,s.borderBottomWidth,s.borderLeftWidth].map(px),
      radius:px(s.borderTopLeftRadius),shadow:s.boxShadow,backgroundClip:s.backgroundClip,backgroundSize:s.backgroundSize,
      clipPath:s.clipPath,timing:s.animationTimingFunction+','+s.transitionTimingFunction,effectiveBackground,
      lineWidths,occluded:hit ? hit!==el && !el.contains(hit) && !hit.contains(el) : null,
      headingGap:!!headingGap,hasIcon:!!el.querySelector('svg,img'),primitiveCount:el.querySelectorAll('rect,circle,ellipse,line,polygon').length,
      src:el.tagName==='IMG' ? el.getAttribute('src') : null,imageComplete:el.complete,naturalWidth:el.naturalWidth,
      ignoreRules:(el.getAttribute('data-aco-ignore') || '').split(/\s+/).filter(Boolean),
      tag:el.tagName.toLowerCase(), id:el.id, role:el.getAttribute('role'),
      text:ownText.slice(0,2000), name:name.slice(0,200),
      alt:el.getAttribute('alt'), href:el.getAttribute('href'), type:el.getAttribute('type'),
      disabled:el.matches(':disabled'), tabindex:el.getAttribute('tabindex'),
      width:r.width,height:r.height,left:r.left,right:r.right,
      scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,
      fontSize:+s.fontSize.replace('px',''),lineHeight:s.lineHeight,
      color:s.color,background:s.backgroundColor,backgroundImage:s.backgroundImage,
      overflowX:s.overflowX,whiteSpace:s.whiteSpace,animation:s.animationName,
      animationDuration:s.animationDuration,transition:s.transitionProperty};
  });
  return {schema:2,lineMeasurement:true,occlusionMeasurement:true,url:location.origin+location.pathname,title:document.title,
    lang:document.documentElement.lang,viewport:{width:innerWidth,height:innerHeight},
    scrollWidth:document.documentElement.scrollWidth,
    viewportMeta:document.querySelector('meta[name="viewport"]')?.content || '',
    reducedMotion:matchMedia('(prefers-reduced-motion: reduce)').matches,
    elements:rows};
}
