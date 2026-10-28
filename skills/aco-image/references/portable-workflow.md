# Portable creative workflow

This skill works independently in Claude Code or Codex, including their VS Code extensions. Use `python3 scripts/install_standalone.py --host claude` or `--host codex` from this skill folder to preview installation; add `--apply` to install, optionally `--project /absolute/project` for project-local discovery. Use the integrated ACO installer for existing full installations; the standalone installer preserves modified or unowned destinations.

For Capture, Image and Video, `python3 scripts/reference_inventory.py /absolute/reference.png --output /new/private/references.json` records existing files and SHA-256 hashes. Inspect each image separately, assign purpose, and map provider bindings only after verifying the interface. The inventory never claims visual review or upload. Genjutsu instead uses its richer `inspect_video.py` and `check_reference_pack.py` workflow.

The package contains original ACO methods and local helpers, not model weights or upstream skills. Python 3 is required for helpers; Genjutsu extraction additionally needs ffmpeg/ffprobe. Actual image/video generation needs a connected tool. Packaging and unit tests do not prove generation quality or fresh host discovery.
