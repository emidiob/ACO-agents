# Start here

**ChatGPT only:** configure the project instructions in CHATGPT-PROJECT-INSTRUCTIONS.txt and give the host access to the authorized GitHub repository. Optional private memory uses your separately connected Drive and a user-selected root. No Python or native-agent installation is required merely to read methods.

**Codex/VS Code:** use Install ACO.command on a Mac, or run `python3 scripts/aco_cli.py doctor`, then `install` for a dry run and `install --apply` to install skills. Add `--offices all` only when you want all optional native profiles. Python 3.11+ is required for scripts; macOS/Linux (WSL for Windows).

**Existing ACO repository (0.3.x or older plugin):** read CODEX-MIGRATION-PROMPT.txt. Do not delete the Git repository. Extract the new release outside the checkout and use the safe migration preview first.

First request: “Use ACO. Help me define the task, choose only the relevant roles and context, and tell me what was actually saved.”

All private IDs, user context and account tokens stay outside the public library. Never send credentials to a maintainer or paste them into chat. Runtime capability varies; when an action is unavailable, preserve the output and report pending/not saved.

Default behavior: clarify essential gaps early, then keep action updates brief. Finance, Commercial, HR, Delivery, Administration, Production and Publishing are now first-class offices. WhatsApp, email and calls use only actual authorized actions, otherwise copy-ready drafts. See [Upgrade 0.4](UPGRADE-0.4.0.md), [integrations](INTEGRATIONS.md), [task recipes](ACTIVITY-RECIPES.md) and the [beginner step-by-step guide](../BEGINNER-GUIDE.md).
