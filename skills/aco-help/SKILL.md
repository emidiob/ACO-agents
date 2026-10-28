---
name: aco-help
description: "Show all ACO commands: creative shortcuts, offices, context tools and terminal/runtime discovery, with Claude Code and Codex syntax."
---

# ACO Help

Read [the complete generated command menu](references/commands.md) and show all ACO entry skills, grouped into creative shortcuts, offices and context. Use `/name` for Claude Code and `$name` for Codex. Do not omit offices by default; a requested short menu can show common shortcuts and link the full list.

The menu is generated from actual `skills/*/SKILL.md` files, not a fixed seven-command list. Explain that internal role IDs, technical registry entries and Python CLI subcommands are different things, not extra native slash commands. For a specific CLI command inspect its actual `--help` before suggesting flags. Third-party skill discovery must be checked in the current host before reporting it installed.

Before persistent writes follow `../aco-office-concierge/references/protocols/COMPACT-MEMORY.md`; keep private context outside the public library.
