/** Bounded, on-demand browser measurements. Nothing is sent to a remote service. */
export function summarizeFrames(intervals,expectedHz=60){
  if(!Number.isFinite(expectedHz)||expectedHz<20||expectedHz>360)throw Error('Expected refresh rate must be between 20 and 360 Hz');
  const valid=intervals.filter(x=>Number.isFinite(x)&&x>0),sorted=[...valid].sort((a,b)=>a-b),budget=1000/expectedHz;
  const percentile=p=>sorted.length?sorted[Math.max(0,Math.ceil(sorted.length*p)-1)]:null;
  return {samples:valid.length,expected_hz:expectedHz,budget_ms:budget,median_ms:percentile(.5),p95_ms:percentile(.95),maximum_ms:sorted.at(-1)??null,
    over_budget:valid.filter(x=>x>budget*1.5).length,estimated_missed_refreshes:valid.reduce((sum,x)=>sum+Math.max(0,Math.round(x/budget)-1),0),
    measured_callback_hz:valid.length?1000*valid.length/valid.reduce((a,b)=>a+b,0):null,
    interpretation:'Animation callback intervals, not GPU frames. Missed refreshes are an estimate against the selected refresh rate.'};
}
export function inspectTypography(element){
  const style=getComputedStyle(element),rect=element.getBoundingClientRect();
  return {tag:element.tagName.toLowerCase(),font_family:style.fontFamily,font_size:style.fontSize,font_weight:style.fontWeight,font_style:style.fontStyle,
    line_height:style.lineHeight,letter_spacing:style.letterSpacing,font_feature_settings:style.fontFeatureSettings,font_variation_settings:style.fontVariationSettings,
    text_transform:style.textTransform,direction:style.direction,writing_mode:style.writingMode,width:rect.width,height:rect.height,
    font_loading_status:document.fonts?.status??'unavailable',
    interpretation:'Computed CSS font stack; this does not identify which fallback font rendered each glyph.'};
}
export function collectRuntime({duration=3000,expectedHz=60}={}){
  summarizeFrames([],expectedHz);if(!Number.isFinite(duration)||duration<250||duration>10000)throw Error('Duration must be between 250 and 10000 ms');
  return new Promise(resolve=>{
    const start=performance.now(),intervals=[],entries=[],observers=[],supported=typeof PerformanceObserver==='undefined'?[]:PerformanceObserver.supportedEntryTypes||[];
    let previous=null,request=null,hidden=document.hidden,finished=false,droppedEntries=0;
    const consume=list=>{for(const entry of list){if(entry.startTime<start)continue;if(entries.length>=500){droppedEntries++;continue;}entries.push({type:entry.entryType,start_ms:entry.startTime-start,duration_ms:entry.duration,blocking_ms:entry.blockingDuration??null,value:entry.value??null,recent_input:entry.hadRecentInput??null});}};
    for(const type of ['longtask','long-animation-frame','layout-shift'])if(supported.includes(type)){try{const observer=new PerformanceObserver(list=>consume(list.getEntries()));observer.observe({type,buffered:false});observers.push(observer);}catch{}}
    const visibility=()=>{if(document.hidden)hidden=true;previous=null;};document.addEventListener('visibilitychange',visibility);
    const tick=time=>{if(finished)return;if(!document.hidden&&previous!==null&&intervals.length<5000)intervals.push(time-previous);previous=document.hidden?null:time;request=requestAnimationFrame(tick);};request=requestAnimationFrame(tick);
    setTimeout(()=>{finished=true;cancelAnimationFrame(request);document.removeEventListener('visibilitychange',visibility);for(const observer of observers){consume(observer.takeRecords());observer.disconnect();}
      resolve({schema:1,duration_ms:performance.now()-start,status:hidden?'inconclusive-hidden-document':intervals.length<10?'insufficient-samples':'measured',frames:summarizeFrames(intervals,expectedHz),events:entries,truncated_events:droppedEntries,
        supported_entry_types:supported.filter(type=>['longtask','long-animation-frame','layout-shift'].includes(type)),viewport:{width:innerWidth,height:innerHeight},reduced_motion:matchMedia('(prefers-reduced-motion: reduce)').matches});
    },duration);
  });
}
