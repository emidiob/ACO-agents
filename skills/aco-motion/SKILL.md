---
name: aco-motion
description: "Design and implement motion graphics, animated typography, explainers and UI animation. Route to Remotion for video or Motion/CSS/GSAP for interactive work, with visual verification and editable source."
---

# ACO Motion

Invoke `/aco-motion` in Claude Code or `$aco-motion` in Codex; `aco motion <task>` is also routed by Concierge. This is a workflow, not a renderer or proof that dependencies are installed.

## Choose the deliverable

Read the existing brief, assets and project before choosing tools. For a video or animated graphic, use Production's `motion_designer` and `remotion_video_engineer` methods when needed. For interactive UI, use Product's frontend methods. Roles do not imply spawned agents.

- **Video / typography / explainers:** read [video workflow](references/video.md). Prefer the official `remotion-best-practices` skill when installed, then only its task-specific references.
- **UI / web / scroll / SVG:** read [interactive workflow](references/interactive.md). Prefer the official `motion` skill for Motion/CSS; keep an existing GSAP implementation when it fits.
- **Commercial / launch film:** use the video workflow with a story and audio pass. Motion Video Kit is an optional research reference, not a universal style specification.
- **Recreate a supplied live-action video:** route to `../aco-genjutsu/SKILL.md`; motion graphics are not reference-video generation.

Locate external skills in the selected host's actual skills root (`~/.agents/skills`, `~/.codex/skills`, `~/.claude/skills`, or project equivalents). Read files before claiming to use them. ACO does not bundle third-party skill bodies; [sources and selection](references/sources.md) records inspected upstream revisions and installation paths. Missing external skills do not block drafting the brief or using the original methods below. Do not invent tool availability.

## Working contract

For substantial work, state the visual idea and timing in a compact storyboard, then implement a representative motion proof before extending the sequence. Use supplied references at actual timestamps. Avoid generic effect lists: specify what moves, why, when, and how the next state becomes readable. Preserve brand and creative intent; no mandatory cinematic look, scene count, bounce or transitions.

Deliver the requested artifact plus editable source. A user request for an MP4 or export authorizes the necessary local render; do not ask again merely because a source skill prefers preview. Preview-only requests remain preview-only. Check current dependencies and license terms before adding a renderer to a project. Installation of instruction files is not installation of Node packages, a paid service, or an MCP connection.

Inspect representative frames and playback/interaction with available tools, repair observable failures, and report what was actually viewed, rendered, or measured. If only stills were inspected, do not claim temporal quality. Audio must be listened to before claiming its quality. Tests passing is not creative approval.

Before persistent writes follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`; client footage and deliverables stay outside the public ACO library.
