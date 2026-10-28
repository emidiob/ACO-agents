# ACO Motion executable kit

## Create and run

Run the included `scripts/scaffold.py --output NEW_PROJECT` with Python 3.11+. It copies [the original starter](../assets/starter/package.json) into a new directory and refuses existing outputs. It does not install dependencies. In that directory run `npm ci` after verifying Node and installation scope. Versions and dependency resolution are pinned in package.json/package-lock.json.

- `npm run preview`: open the printed Studio URL with the host's browser tool.
- `npm run render`: render the eight-second Typography composition into `out/typography.mp4`.
- `npm run reference`: render the controlled ReferenceStudy composition.
- `ui.html`: serve through a local HTTP server to inspect the original responsive interaction prototype.

The starter's frame-driven JSX, typography and UI are original editable examples, not mandatory ACO style. Replace them according to the brief. Remotion remains an external engine with its own license. A compatible browser is needed: if using installed Chrome, confirm the CLI's `--browser-executable` option for that version. Do not claim browser installation from Node package installation.

Run `python3 scripts/check_export.py FILE --width 1280 --height 720 --fps 30 --duration 8 --audio absent` from the skill folder to compare a real output against its delivery settings. This needs ffprobe. A mismatch exits nonzero. The report explicitly leaves visual/playback/audio review unverified.

The ReferenceSource and ReferenceStudy compositions form a controlled graphics test: two interpolation implementations use known anchor geometry. Compare rendered source/reconstruction frames and report the sampling scope. It is not a blind reverse-engineering benchmark and does not establish live-action reconstruction fidelity.

## Same source, two distributions

In the full ACO library, use the normal ACO installers. For a standalone artifact the maintainer runs `python3 scripts/package_motion_skill.py --output OUTSIDE_LIBRARY.zip` from the complete source checkout. The archive contains this same skill, original assets/scripts, the existing ACO license and source hashes. No ACO office or external agent skill is required.

After extracting the archive, from `aco-motion/` preview with `python3 scripts/install_standalone.py --host claude` or `--host codex`. Add `--project PROJECT` for project-scoped installation and `--apply` to apply the reviewed plan. Claude uses `.claude/skills`; Codex uses `.agents/skills`. The installer refuses unmanaged/modified collisions and keeps the previous managed version as a hidden backup on update. Do not install standalone over a full ACO installation; use its installer instead. Avoid multiple copies of the same skill at different scopes.

## Host adapters

- **Claude Code:** `/aco-motion`; use actual Read/Edit/Bash/browser capabilities available in that session. Install globally or in the project.
- **Codex:** `$aco-motion`; use actual file/exec/browser tools and the host's sandbox. Keep artifacts in an authorized project directory.
- **VS Code with Claude Code or Codex:** use the corresponding extension and the same project/global skill folder. VS Code itself is not an agent host. Discovery and GUI behavior must be confirmed in a real extension session; file installation tests alone do not prove it.
- **Other VS Code assistants:** give the self-contained SKILL.md as context only until that assistant's skill format/discovery is verified. Do not claim Copilot compatibility by assumption.

No automatic config rewriting, MCP provisioning, account changes or external skill download occurs. If execution tools are unavailable, provide editable source and the exact unexecuted command; do not claim a render.
