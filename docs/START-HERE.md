# Start here — ACO 1.0.9

For a plain-language walkthrough, open the [interactive guide](GUIDA.html). It works as a local HTML file, with separate steps for ChatGPT and Codex, examples to copy and common questions.

ACO is a library of instructions and optional local tools. It does not connect accounts or install itself merely because you mention it in a chat.

## ChatGPT

Make the ACO instructions available through an authorized repository/file tool, or attach the relevant files. You can put [these project instructions](CHATGPT-PROJECT-INSTRUCTIONS.txt) in a private ChatGPT project, or work in a normal chat. Ask the assistant to read the available `VERSION` and `CHATGPT.md`, then describe your actual task. If it cannot read the files, it should say so.

## Codex on your computer

Open the complete ACO checkout or extracted release and check that `VERSION` says `1.0.9`. Python 3.11+ is needed for local ACO tools. From the source folder, `python3 scripts/aco_cli.py doctor` checks prerequisites, `python3 scripts/aco_cli.py validate` checks the package, and `python3 scripts/aco_cli.py install` previews installation. Use `install --apply` only after reviewing the preview. Start a new Codex session to check that the installed skills are discovered. See the [README](../README.md#updating-github-and-local-installs) for the full procedure.

If you have an older checkout, use [Upgrading](UPGRADING.md) and preserve your Git history, private files and unrelated work.

## Your first request

> Use ACO to help me with [your actual task]. Read the relevant instructions you can access, prepare a concrete first result, and tell me what you verified.

You do not need every skill, optional resource or a permanent memory system to begin.
