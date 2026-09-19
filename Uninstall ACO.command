#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 scripts/aco_cli.py uninstall
printf '\nRemove only the listed ACO-managed files? Private knowledge is preserved. [y/N] '
read -r consent
case "$consent" in y|Y|yes|YES|s|S|si|SI) python3 scripts/aco_cli.py uninstall --apply;; *) echo 'Nothing removed.';; esac
