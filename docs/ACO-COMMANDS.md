# ACO Quick Commands — 1.0.5

Seven thin, first-party Agent Skills are added without duplicating ACO's 363 roles or the technical candidate bodies:

| Command (Claude Code) | Codex skill | Purpose |
|---|---|---|
| `/aco` | `$aco` | Concierge, main entry |
| `/aco-genjutsu` | `$aco-genjutsu` | Source video → prompt-only replica |
| `/aco-video` | `$aco-video` | Video prompt director |
| `/aco-image` | `$aco-image` | Image prompt director |
| `/aco-capture` | `$aco-capture` | ACO Capture methodology |
| `/aco-skills` | `$aco-skills` | Skills list & state |
| `/aco-help` | `$aco-help` | Quick menu |

Alternative: `/aco genjutsu`, `/aco video`, `/aco image`, `/aco capture`, `/aco skills`, `/aco help`.

**Status:** baseline 1.0.4 is 14 active + 29 candidate technical entries; this patch adds one new prompt-only Genjutsu candidate (44 total). All 30 candidates are *available for explicit experimental inspection* when invoked via ACO shortcuts; they are NOT silently promoted to active or independently validated. Source identity of the Mimic candidate remains unverified. This aligns with the owner's request to access every method without falsifying the library's technical verification controls.

**Claude Code:** Install the canonical ACO skill folders (including the 7 command entrypoints) under `~/.claude/skills/` or project `.claude/skills/`. Use `scripts/install_aco_claude_shortcuts.py --apply` to copy them conservatively after a dry run. No dependencies are downloaded. `/aco` availability depends on the host's skill discovery. Keep the original ACO library checkout intact so relative paths to other skills resolve.

**Codex:** From this complete checkout, `python3 scripts/aco_cli.py install --apply` installs all canonical skill folders under `~/.agents/skills/`, including these commands. Codex ordinarily invokes them as `$aco`, `$aco-genjutsu` etc., not guaranteed native `/aco` commands. Existing ACO installer must be patched to support owned `aco/` path (included in this kit).

**ChatGPT:** Typing `/aco` or `/aco-genjutsu` into chat is a textual instruction. This kit cannot register new native product slash commands by itself; the connected repository methods must remain accessible to the conversation.

**Provenance:** JutsuHQ MIT prompt-only workflow, independently adapted for ACO (see Genjutsu technical body). No upstream scripts or external APIs installed.

## Original prompt workflow

`aco-genjutsu` now routes to the complete [ACO method](../skills/aco-genjutsu/SKILL.md), with original notation, visual evidence, operation selection, appearance/camera guidance, worked cases and diagnosis. `aco-video` and `aco-image` reuse the relevant references. The local frame helper performs analysis only; no provider is invoked. Existing third-party material retains its original notices.
