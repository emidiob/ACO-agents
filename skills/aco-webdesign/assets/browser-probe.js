() => {
  // ACO read-only DOM probe. Run through the host's authorized browser API.
  // It never clicks, edits, fetches, reads application stores or uploads data.
  const visible = el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const elements = Array.from(document.querySelectorAll('body *')).filter(visible).map((el, index) => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    const labelIds = (el.getAttribute('aria-labelledby') || '').trim().split(/\s+/).filter(Boolean);
    const labels = labelIds.map(id => document.getElementById(id)?.textContent || '').join(' ');
    const ownText = Array.from(el.childNodes).filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent).join(' ').trim();
    const name = el.getAttribute('aria-label') || labels || Array.from(el.labels || []).map(x => x.textContent).join(' ') || el.textContent?.trim() || el.getAttribute('alt') || '';
    return {index, tag:el.tagName.toLowerCase(), id:el.id, role:el.getAttribute('role'),
      text:ownText.slice(0,200), name:name.slice(0,200),
      alt:el.getAttribute('alt'), href:el.getAttribute('href'), type:el.getAttribute('type'),
      disabled:el.matches(':disabled'), tabindex:el.getAttribute('tabindex'),
      width:r.width,height:r.height,left:r.left,right:r.right,
      scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,
      fontSize:+s.fontSize.replace('px',''),lineHeight:s.lineHeight,
      color:s.color,background:s.backgroundColor,backgroundImage:s.backgroundImage,
      overflowX:s.overflowX,whiteSpace:s.whiteSpace,animation:s.animationName,
      animationDuration:s.animationDuration,transition:s.transitionProperty};
  });
  return {schema:1,url:location.origin+location.pathname,title:document.title,
    lang:document.documentElement.lang,viewport:{width:innerWidth,height:innerHeight},
    scrollWidth:document.documentElement.scrollWidth,
    viewportMeta:document.querySelector('meta[name="viewport"]')?.content || '',
    reducedMotion:matchMedia('(prefers-reduced-motion: reduce)').matches,
    elements};
}
