import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

const ink = '#17251e', paper = '#f0efe8', acid = '#d4fa62';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const ease = x => 1 - Math.pow(1 - x, 3);
export const phase = (frame, start, length) => ease(Math.max(0, Math.min(1, (frame-start)/length)));
const Label = ({children, style={}}) => <div style={{fontFamily:'Arial, sans-serif', fontSize:18, letterSpacing:3, ...style}}>{children}</div>;

export const Typography = ({headline='LE IDEE', second='PRENDONO', final='FORMA.'}) => {
  const f=useCurrentFrame(); const {fps}=useVideoConfig();
  const a=phase(f,0,0.8*fps), b=phase(f,1.1*fps,0.8*fps), c=phase(f,2.2*fps,0.8*fps);
  const shift=phase(f,4.2*fps,0.9*fps), end=phase(f,5.1*fps,0.8*fps);
  const line=(text,p,color=ink)=><div style={{overflow:'hidden'}}><div style={{transform:`translateY(${(1-p)*110}%)`,color}}>{text}</div></div>;
  return <AbsoluteFill style={{background:paper,color:ink,padding:64,fontFamily:'Arial, sans-serif'}}>
    <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><Label>ACO / MOTION STUDY 01</Label><Label>IDEA → MOVIMENTO</Label></div>
    <div style={{position:'absolute',width:480,height:480,borderRadius:'50%',background:acid,right:-80+shift*80,top:130,transform:`scale(${0.45+a*.55})`}}/>
    <div style={{position:'absolute',left:64,top:130,fontWeight:900,fontSize:105,lineHeight:1.02,letterSpacing:-5,transform:`translateX(${-shift*1500}px)`}}>
      {line(headline,a)}{line(second,b)}{line(final,c)}
    </div>
    <div style={{position:'absolute',left:64,top:170,opacity:end,transform:`translateY(${(1-end)*45}px)`}}>
      <div style={{fontWeight:900,fontSize:148,letterSpacing:-9}}>ACO.</div>
      <div style={{fontSize:38,marginTop:18}}>Un metodo. Infinite possibilità.</div>
      <Label style={{marginTop:32}}>DIREZIONE / COSTRUZIONE / VERIFICA</Label>
    </div>
    <div style={{position:'absolute',left:64,right:64,bottom:55,display:'flex',justifyContent:'space-between',borderTop:'1px solid #17251e44',paddingTop:18}}><Label>STUDIO DI TIPOGRAFIA IN MOVIMENTO</Label><Label>01 — 08</Label></div>
  </AbsoluteFill>;
};

// A controlled graphic reference, not a live-action or blind reconstruction benchmark.
export const referenceKeys = [
  {t:0,x:170,y:360,r:0,s:1}, {t:1,x:470,y:360,r:45,s:1},
  {t:2,x:790,y:240,r:90,s:1.3}, {t:3,x:1080,y:360,r:180,s:1},
];
export const ReferenceStudy = ({mode='reconstruction'}) => {
 const f=useCurrentFrame(), {fps}=useVideoConfig(), t=f/fps;
 let x,y,r,s;
 if(mode==='source') {
   // Source uses segment interpolation.
   const k=Math.min(2,Math.floor(t)), q=Math.min(1,t-k), a=referenceKeys[k], b=referenceKeys[k+1];
   x=a.x+(b.x-a.x)*q;y=a.y+(b.y-a.y)*q;r=a.r+(b.r-a.r)*q;s=a.s+(b.s-a.s)*q;
 } else {
   // Reconstruction uses the declared anchor table, not a captured source image.
   const times=referenceKeys.map(k=>k.t*fps);
   const sample=key=>interpolate(f,times,referenceKeys.map(k=>k[key]),clamp);
   x=sample('x');y=sample('y');r=sample('r');s=sample('s');
 }
 return <AbsoluteFill style={{background:ink,color:paper,fontFamily:'Arial, sans-serif'}}>
   <Label style={{position:'absolute',left:64,top:50}}>ACO / REFERENCE STUDY 02</Label>
   <div style={{position:'absolute',left:64,top:100,fontSize:48,fontWeight:700}}>Una traiettoria. Quattro ancore.</div>
   <svg width="1280" height="720" style={{position:'absolute'}}><path d="M170 360 L470 360 L790 240 L1080 360" fill="none" stroke="#f0efe844" strokeWidth="2" strokeDasharray="5 10"/>{referenceKeys.map((k,i)=><g key={i}><circle cx={k.x} cy={k.y} r="6" fill={paper}/><text x={k.x} y={k.y+105} fill={paper} fontFamily="Arial" fontSize="20">{k.t.toFixed(1)} s</text></g>)}</svg>
   <div style={{position:'absolute',left:x-35,top:y-35,width:70,height:70,background:acid,borderRadius:12,transform:`rotate(${r}deg) scale(${s})`}}/>
   <Label style={{position:'absolute',left:64,bottom:50}}>POSIZIONE / ROTAZIONE / SCALA — TEST CONTROLLATO</Label>
 </AbsoluteFill>;
};
const Root=()=> <><Composition id="Typography" component={Typography} width={1280} height={720} fps={30} durationInFrames={240}/><Composition id="ReferenceSource" component={ReferenceStudy} defaultProps={{mode:'source'}} width={1280} height={720} fps={30} durationInFrames={91}/><Composition id="ReferenceStudy" component={ReferenceStudy} width={1280} height={720} fps={30} durationInFrames={91}/></>;
registerRoot(Root);
