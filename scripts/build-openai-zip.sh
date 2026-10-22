#!/usr/bin/env bash
# Builds the two upload archives from the files the directories load, nothing else:
#   dist/shootika-<VERSION>-openai.zip   with .codex-plugin/  (platform.openai.com, With MCP)
#   dist/shootika-<VERSION>-claude.zip   with .claude-plugin/ (claude.ai, Customize > Plugins > Upload)
# Run from anywhere; it works on the repository that contains it.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo"
version="$(tr -d '[:space:]' < VERSION)"
common=(.mcp.json README.md LICENSE assets skills)
excludes=(-x '*/.DS_Store' '.DS_Store' '*/__MACOSX/*' '*/__pycache__/*' '*/Thumbs.db')

rm -rf dist
mkdir -p dist

zip -q -r "dist/shootika-$version-openai.zip" .codex-plugin "${common[@]}" "${excludes[@]}"
zip -q -r "dist/shootika-$version-claude.zip" .claude-plugin "${common[@]}" "${excludes[@]}"

for archive in "dist/shootika-$version-openai.zip" "dist/shootika-$version-claude.zip"; do
  echo "$archive"
  unzip -l "$archive" | tail -1
done
