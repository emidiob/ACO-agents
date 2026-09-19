#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
command -v python3 >/dev/null || { echo 'Python 3.11+ is required. See START-HERE-IT.md.'; exit 1; }
python3 scripts/aco_cli.py doctor
printf '\nInstall the 9 ACO skills for your user? [y/N] '
read -r consent
case "$consent" in y|Y|yes|YES|s|S|si|SI) ;; *) echo 'Nothing installed.'; exit 0;; esac
printf 'Also install all 246 optional native Codex agent profiles? [y/N] '
read -r agents
case "$agents" in y|Y|yes|YES|s|S|si|SI) offices=all;; *) offices=none;; esac
python3 scripts/aco_cli.py install --offices "$offices" --apply
printf '\nInstallation verified. Restart Codex and try: Use ACO.\n'
