#!/usr/bin/env python3
"""Prepare source frames, overview sheets and cut candidates using local media tools."""
import argparse
from bisect import bisect_left
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def sheet(folder, pattern, count, name, columns):
    run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-framerate', '1',
         '-i', str(folder / pattern), '-vf',
         f'scale=360:-1,tile={columns}x{math.ceil(count / columns)}',
         '-frames:v', '1', str(folder / name)])


def inspect(source, output, times=None):
    source = Path(source).expanduser().resolve(strict=True)
    output = Path(output).expanduser().absolute()
    if not source.is_file():
        raise ValueError('Source must be a file')
    if output.exists():
        raise ValueError('Output destination already exists; choose a new directory')
    for tool in ('ffprobe', 'ffmpeg'):
        if not shutil.which(tool):
            raise ValueError(f'{tool} must already be installed')
    metadata = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                               '-of', 'json', str(source)]).stdout)
    video = next((s for s in metadata.get('streams', []) if s.get('codec_type') == 'video'), None)
    if video is None:
        raise ValueError('Source has no video stream')
    duration = float(video.get('duration') or metadata.get('format', {}).get('duration', 0))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('No usable positive duration found')
    timestamps = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', str(video['index']),
        '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(source)]).stdout)['frames']
    raw_pts = [float(f['best_effort_timestamp_time']) for f in timestamps]
    if not raw_pts or any(not math.isfinite(t) for t in raw_pts):
        raise ValueError('Missing usable frame timestamps')
    pts = [t - raw_pts[0] for t in raw_pts]
    if pts != sorted(pts):
        raise ValueError('Non-monotonic frame timestamps need manual inspection')
    if times is not None:
        times = list(times)
        if not times or len(times) > 48 or any(not math.isfinite(t) or t < 0 or t >= duration for t in times):
            raise ValueError('Use 1–48 finite timestamps within the video duration')
        indexes = [min(bisect_left(pts, t), len(pts)-1) for t in times]
        # Deliver in chronology and avoid redundant references to the same decoded frame.
        chosen = sorted(dict(zip(indexes, times)).items())
    else:
        indexes = sorted({round((len(pts)-1)*fraction) for fraction in (0, .25, .5, .75, 1)})
        chosen = [(i, pts[i]) for i in indexes]
    output.mkdir(parents=True, exist_ok=False)
    frames = []
    report = {'source': str(source), 'duration_seconds': duration, 'frame_count': len(pts),
        'width': video.get('width'), 'height': video.get('height'), 'average_frame_rate': video.get('avg_frame_rate'),
        'audio_stream_present': any(s.get('codec_type') == 'audio' for s in metadata['streams']),
        'audio_reviewed': False, 'visual_reviewed': False,
        'inspection': 'Images extracted; actions, audio and cut candidates still require review',
        'frames': frames, 'status': 'extracting'}
    try:
        for index, (frame_number, requested) in enumerate(chosen):
            target = output / f'frame-{index:02d}.png'
            run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(source), '-map', f"0:{video['index']}",
                 '-vf', f'select=eq(n\\,{frame_number})', '-fps_mode', 'vfr', '-frames:v', '1', '-an', str(target)])
            if not target.is_file() or not target.stat().st_size:
                raise ValueError(f'No decoded frame {frame_number}')
            frames.append({'file': target.name, 'requested_time_seconds': requested,
                'source_time_seconds': pts[frame_number], 'frame_number': frame_number,
                'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        sheet(output, 'frame-%02d.png', len(frames), 'references.jpg', min(5, len(frames)))
        overview = output / 'overview'
        overview.mkdir()
        overview_indexes = sorted({round((len(pts)-1)*i/23) for i in range(24)})
        expression = '+'.join(f'eq(n\\,{i})' for i in overview_indexes)
        run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(source), '-map', f"0:{video['index']}",
             '-vf', f'select={expression},scale=360:-1', '-fps_mode', 'vfr', '-an',
             '-start_number', '0', str(overview / 'sample-%02d.png')])
        sheet(overview, 'sample-%02d.png', len(overview_indexes), 'contact-sheet.jpg', min(6, len(overview_indexes)))
        report['overview'] = [{'file': f'overview/sample-{i:02d}.png', 'source_time_seconds': pts[n],
                               'frame_number': n} for i, n in enumerate(overview_indexes)]
        cuts = run(['ffmpeg', '-nostdin', '-hide_banner', '-nostats', '-copyts', '-i', str(source),
                    '-map', f"0:{video['index']}", '-vf', "select=gt(scene\\,0.25),showinfo", '-an', '-f', 'null', '-'])
        report['cut_candidates_seconds'] = [float(t)-raw_pts[0] for t in re.findall(r'pts_time:([\d.eE+\-]+)', cuts.stderr)]
        report['cut_detection_note'] = 'Heuristic threshold 0.25; an empty list is not proof of a continuous shot.'
        bindings = {'source': source.name, 'intent': 'unresolved', 'provider_bindings': 'unresolved',
            'references': [{'file': f['file'], 'source_time_seconds': f['source_time_seconds'],
                'sha256': f['sha256'], 'type': 'extracted_original', 'purpose': '', 'visually_reviewed': False} for f in frames]}
        (output / 'reference-map.json').write_text(json.dumps(bindings, indent=2) + '\n')
        report['status'] = 'extracted'
    except Exception:
        report['status'] = 'partial_failure'
        raise
    finally:
        (output / 'inspection.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True, help='New task directory outside the ACO library')
    parser.add_argument('--times', type=float, nargs='+', help='Source seconds; default includes first and last decoded frame')
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.source, args.output, args.times), indent=2))
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Inspection failed: {error}\n')
