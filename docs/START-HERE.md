# Start here — ACO 1.0.6

ACO supplies instructions and optional local tools. Start with the route that matches how you work.

## I use ChatGPT

1. Make the ACO instructions available through an authorized repository/file tool, or attach the required files.
2. Paste [the project instructions](CHATGPT-PROJECT-INSTRUCTIONS.txt) into your private project's instructions.
3. Ask: “Use ACO. Read the available VERSION and CHATGPT.md, then help me with [my task].”

No local installation is required for reading instructions. If retrieval fails, provide the requested files. ACO cannot connect accounts by itself.

## I use Codex on my computer

1. Extract the complete **1.0.6** ZIP into a new folder and check `VERSION`.
2. Open a terminal in the extracted `ACO-agents` folder. Use Python 3.11 or newer:

   ```bash
   python3 scripts/aco_cli.py doctor
   python3 scripts/aco_cli.py validate
   python3 scripts/aco_cli.py install
   ```

3. Review the installation preview. To install the 23 skills:

   ```bash
   python3 scripts/aco_cli.py install --apply
   python3 scripts/aco_cli.py install-status
   ```

4. Start a fresh Codex session and ask it to read the relevant ACO skill for your task. Installed files do not prove that a session loaded them.

On macOS, `Install ACO.command` provides the prompted installation route. Optional native profiles can be selected later. Keep client work in its own folder.

## I already have an older ACO

Follow [Upgrading](UPGRADING.md) from the new package. Extracting a ZIP, pushing GitHub and updating installed skills are separate steps. Preserve private state and unrelated files; avoid overlaying the archive onto the old checkout.

## I want the plain-language explanation

Read the [Beginner Guide](../BEGINNER-GUIDE.md) for daily requests, memory, troubleshooting and resuming work. The [README](../README.md) explains the library; [CLI](CLI.md) describes optional commands. You do not need to install the resource catalogue or connect Drive to start.

The [1.0.6 report](../ACO-TEST-REPORT-v1.0.6.md) records release checks. Earlier test reports describe their own versions.

## Quick command skills (ACO 1.0.6 command pack)

The merged package includes 23 source skill folders, including seven lightweight shortcuts such as `/aco` and `/aco-genjutsu`. Claude Code and Codex support their own native invocation only after installing and confirming discovery. In regular ChatGPT, typing these is a conversational cue; see [ACO Quick Commands](ACO-COMMANDS.md). Technical candidates can be examined explicitly, but they are not production-validated.
