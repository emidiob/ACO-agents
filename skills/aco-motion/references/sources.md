# Motion skill selection — reviewed 2026-10-28

These are scoped recommendations from source inspection, not a comparative render benchmark. External skills remain separate from the ACO technical registry; no candidate was promoted. Installation instructions below refer to original upstream skill directories, not republished bodies.

| Source | Strength | Decision / limitation |
|---|---|---|
| [Remotion official skills](https://github.com/remotion-dev/skills) | Project creation, frame-based React graphics, preview, render, captions, maps and media | Selected video foundation. 12 coordinated skills; install together because the router and specialist references are related. Officially supports Claude Code and Codex. Node/project packages are separate. |
| [Motion official AI Kit](https://github.com/motiondivision/ai-kit) | CSS/Motion animation guidance, platform-specific APIs, UI state and layout | Selected web/UI foundation. Local best practices work without MCP. Search/editor/MotionScore need actual services and some features require Motion+. |
| [Motion Video Kit](https://github.com/echris6/motion-video-kit) | Commercial storyboarding, reference analysis, deterministic scenes, audio and render critique | Reference only by default: fixed pacing, 1080p60 and mandatory critic loops are specific creative choices. Scripts include output-overwriting ffmpeg calls and require task-specific review before execution. |
| [Design Motion Principles](https://github.com/kylezantos/design-motion-principles) | Purposeful UI motion and creation/audit heuristics | Useful complementary reference, already linked in ACO motion resources. Community interpretation, not endorsement by named designers. Avoid imposing its aesthetic rules on all work. |

Inspected revisions: Remotion `30d4553ecd46fbc5212fd0ff006ae43af522158b`; Motion AI Kit `1e424943582cbbdb6e3f410687e39f96451447bb`; Motion Video Kit `e4b1c0004080fe6a0deb883631bad5eba1e5f339`. Design Motion Principles README inspected through GitHub; not installed or benchmarked in this update.

## Installation and provenance

The reviewed Remotion path is `skills/` (all 12 immediate skill folders). Motion is `plugins/motion/skills/motion/`. Copy complete skill directories into the actual host root, preserving files and notices. Do not run upstream installers just to copy instructions: they can also configure MCP or download code. Refuse unrelated file collisions; record revision and file hashes outside the public library for local installations.

[Remotion installation documentation](https://www.remotion.dev/docs/ai/skills) explicitly distributes these instructions for agents. Its skills snapshot has no root LICENSE file; it is not bundled or relicensed as ACO. The renderer has [separate licensing](https://github.com/remotion-dev/remotion/blob/main/packages/core/LICENSE.md), which must be checked for the actual user/project.

[Motion's installation guide](https://motion.dev/docs/ai-kit-install) declares the installer and skill MIT; the inspected package manifest also declares MIT, but this snapshot has no LICENSE file. Preserve the source metadata; do not invent a copyright notice. Motion Video Kit has an MIT LICENSE file. ACO's existing LICENSE and third-party notices remain unchanged.

For new API work recheck official docs at the installed version. Local skill installation does not validate artistic results, activate premium services, or install the animation libraries themselves.
