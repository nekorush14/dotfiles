#!/usr/bin/env bash
set -euo pipefail

EDITOR_BIN="${EDITOR_BIN:-code}"

extensions=(
  "anthropic.claude-code"
  "catppuccin.catppuccin-vsc-icons"
  "enkia.tokyo-night"
)

for id in "${extensions[@]}"; do
  "$EDITOR_BIN" --install-extension "$id"
done
