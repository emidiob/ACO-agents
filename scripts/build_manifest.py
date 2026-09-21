#!/usr/bin/env python3
"""Build a reproducible integrity manifest; no secrets or private data are included."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
excluded={'__pycache__','.git','.venv','.pytest_cache'}
files={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or any(x in excluded for x in p.relative_to(R).parts) or p.suffix=='.pyc':continue
 rel=p.relative_to(R).as_posix()
 if rel=='release/manifest.json':continue
 if p.is_symlink():raise SystemExit('Symlinks forbidden in release: '+rel)
 files[rel]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':p.stat().st_mode&0o777}
manifest={'schema_version':1,'aco_version':(R/'VERSION').read_text().strip(),'files':files}
(R/'release/manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('Manifest:',len(files),'files')
