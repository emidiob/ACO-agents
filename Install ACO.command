#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
command -v python3 >/dev/null || { echo 'Python 3.11+ is required. See BEGINNER-GUIDE.md.'; exit 1; }
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' || { echo 'Python 3.11+ is required. Nothing installed.'; exit 1; }
python3 scripts/aco_cli.py doctor
SKILLS="$(python3 -c 'import json; print(len(json.load(open("catalog.json"))["skills"]))')"
ROLES="$(python3 -c 'import json; print(len(json.load(open("catalog.json"))["agents"]))')"
printf '\nInstall the %s ACO skills for your user? [y/N] ' "$SKILLS"
read -r consent
case "$consent" in y|Y|yes|YES) ;; *) echo 'Nothing installed.'; exit 0;; esac
printf 'Also install all %s optional native Codex agent profiles? [y/N] ' "$ROLES"
read -r agents
case "$agents" in y|Y|yes|YES) offices=all;; *) offices=none;; esac
python3 scripts/aco_cli.py install --offices "$offices" --apply
printf '\nLocal files installed and verified. Start a new Codex session and confirm host discovery with: Use ACO.\n'
