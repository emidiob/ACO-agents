#!/usr/bin/env python3
"""Check actual video metadata against delivery settings; never certifies visual quality."""
import argparse
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path

def check(path, width, height, fps, duration, audio='either'):
    if width<=0 or height<=0 or not all(math.isfinite(x) and x>0 for x in (fps,duration)):
        raise ValueError('Expected dimensions, fps and duration must be positive and finite')
    path=Path(path).resolve(strict=True)
    run=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
    data=json.loads(run.stdout);video=next((s for s in data['streams'] if s.get('codec_type')=='video'),None)
    if video is None:raise ValueError('No video stream')
    actual_fps=float(Fraction(video.get('avg_frame_rate','0/1')))
    actual_duration=float(video.get('duration',data.get('format',{}).get('duration','nan')))
    has_audio=any(s.get('codec_type')=='audio' for s in data['streams'])
    errors=[]
    if video.get('width')!=width or video.get('height')!=height:errors.append('dimensions')
    if abs(actual_fps-fps)>0.01:errors.append('fps')
    if not math.isfinite(actual_duration) or abs(actual_duration-duration)>1/fps+0.01:errors.append('duration')
    if audio=='required' and not has_audio:errors.append('missing_audio')
    if audio=='absent' and has_audio:errors.append('unexpected_audio')
    return {'status':'metadata_matches' if not errors else 'metadata_mismatch','errors':errors,
            'actual':{'width':video['width'],'height':video['height'],'fps':actual_fps,'duration':actual_duration,'audio':has_audio},
            'visual_review':False,'playback_review':False,'audio_listened':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',type=Path);p.add_argument('--width',type=int,required=True);p.add_argument('--height',type=int,required=True)
    p.add_argument('--fps',type=float,required=True);p.add_argument('--duration',type=float,required=True);p.add_argument('--audio',choices=['required','absent','either'],default='either')
    try:
        a=p.parse_args();result=check(a.file,a.width,a.height,a.fps,a.duration,a.audio);print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as e:p.exit(1,str(e)+'\n')
