# Optional executable local tools

The library can be read directly in ChatGPT without running code. In Codex/terminal, Python 3.11+ tools implement local storage, installation, checks and handoffs. They do not invoke a model, authenticate user apps or execute in the background.

From the source checkout: `python3 scripts/aco_cli.py --help`.
From an installed native skill: `python3 <skills-root>/aco-office-concierge/runtime/scripts/aco_cli.py --help` (knowledge/session/event commands only).

Use scripts only after inspecting the task and the host's execution permissions. Keep knowledge outside the public repository. For meaningful file work, create a session, record checkpoints with evidence and close it. A documented test not executed must be marked untested.

Local authority uses atomic writes and OS file locks. Drive authority uses connected tools and provider revision controls; the CLI will not apply a local canonical-context proposal when Drive is declared authoritative. The optional REST bridge sends immutable events only; it is not a background Drive sync daemon and does not refresh canonical context. Read canonical context through connected tools, use the approved session snapshot, then reconcile at the end.
