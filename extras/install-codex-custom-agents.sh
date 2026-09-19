#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/codex-custom-agents"
DEST="${CODEX_HOME:-$HOME/.codex}/agents"
mkdir -p "$DEST"
find "$SRC" -type f -name '*.toml' -exec cp {} "$DEST"/ \;
echo "Installed Agent Office custom agents to $DEST"
