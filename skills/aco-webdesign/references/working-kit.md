# Executable kit

Python 3 standard library is sufficient. From this skill folder:

```bash
python3 scripts/directions.py --query "editorial culture archive"
python3 scripts/scaffold.py --layout editorial --output /new/project
python3 scripts/scaffold.py --layout workspace --output /another/new/project
python3 scripts/audit_html.py /new/project/index.html
python3 -m http.server 8768 --bind 127.0.0.1 --directory /new/project
```

Scaffolding refuses existing/symlink destinations, makes no installs and contacts no network. Both examples have local HTML/CSS/JS, realistic fictional content and working local interactions. Editorial demonstrates a publication/program page with category filtering and a dialog; Workspace demonstrates task search/status filtering with a result count and a clear empty state. Customize or replace them for the brief; don't mistake them for a universal website generator.

The audit emits JSON with file/line/code/severity findings. Exit 1 means findings exist, 2 means execution/input failure, 0 means no findings in the limited static checks. It reports `browser_verified: false` even when checks pass.

Standalone installation previews by default:

```bash
python3 scripts/install_standalone.py --host codex
python3 scripts/install_standalone.py --host claude --apply
```

Add `--project /absolute/project` for project-local installation. Use the integrated ACO installer to update a full existing ACO installation. Modified or unmanaged standalone targets are preserved. In source ACO, export with `python3 scripts/package_creative_skill.py --skill aco-webdesign --output /outside/library/aco-webdesign.zip`. The same canonical files are used in native and standalone packages.

## Extended native engines

See [native engines](native-engines.md) for independent BM25 search, checksum-pinned external data, design-system proposals and DOM snapshot analysis. See [operations](operations.md) for the 33 native agent methods.
