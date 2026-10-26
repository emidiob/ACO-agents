#!/usr/bin/env python3
"""Extract timestamped analysis frames with existing ffprobe/ffmpeg; never render AI media."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess


def inspect(source, output, times):
    source = Path(source).expanduser().resolve(strict=True)
    output = Path(output).expanduser().absolute()
    if not source.is_file():
        raise ValueError('Source must be a file')
    if output.exists():
        raise ValueError('Output destination already exists; choose a new directory')
    for tool in ('ffprobe', 'ffmpeg'):
        if not shutil.which(tool):
            raise ValueError(f'{tool} must already be installed')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                            '-of', 'json', str(source)], check=True, capture_output=True, text=True)
    metadata = json.loads(probe.stdout)
    streams = metadata.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    if video is None:
        raise ValueError('Source has no video stream')
    duration = float(metadata.get('format', {}).get('duration', video.get('duration', 0)))
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('No usable positive duration found')
    times = list(times) if times else [duration * fraction for fraction in (0, .2, .4, .6, .8)]
    if not times or any(not math.isfinite(t) or t < 0 or t >= duration for t in times):
        raise ValueError('Every requested timestamp must be finite and within the video duration')
    if len(times) > 48:
        raise ValueError('Use at most 48 frames per inspection batch')
    output.mkdir(parents=True, exist_ok=False)
    frames = []
    report = {'source': str(source), 'duration_seconds': duration,
              'width': video.get('width'), 'height': video.get('height'),
              'average_frame_rate': video.get('avg_frame_rate'),
              'audio_stream_present': any(s.get('codec_type') == 'audio' for s in streams),
              'audio_reviewed': False, 'inspection': 'sampled frames; cuts and actions require visual review',
              'frames': frames, 'status': 'extracting'}
    try:
        for index, seconds in enumerate(times):
            target = output / f'frame-{index:02d}.png'
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(source),
                            '-ss', str(seconds), '-map', f"0:{video['index']}", '-frames:v', '1',
                            '-an', str(target)], check=True, capture_output=True)
            if not target.is_file() or target.stat().st_size == 0:
                raise ValueError(f'No decodable frame at requested time {seconds}')
            frames.append({'file': target.name, 'requested_time_seconds': seconds})
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
    parser.add_argument('--output', type=Path, required=True, help='New directory outside the ACO library')
    parser.add_argument('--times', type=float, nargs='+', help='Seconds from start; default: five evenly spaced samples')
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.source, args.output, args.times), indent=2))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, f'Inspection failed: {error}\n')
