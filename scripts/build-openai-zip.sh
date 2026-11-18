#!/usr/bin/env bash
# Builds the two upload archives from the plugin folder (shootika/), nothing else:
#   dist/shootika-<version>-openai.zip   with .codex-plugin/  (platform.openai.com, With MCP)
#   dist/shootika-<version>-claude.zip   with .claude-plugin/ (claude.ai, Customize > Plugins > Upload)
# The version is the one in shootika/.claude-plugin/plugin.json. Run from anywhere.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
plugin="$repo/shootika"
version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$plugin/.claude-plugin/plugin.json")"
common=(.mcp.json README.md LICENSE assets skills)
excludes=(-x '*/.DS_Store' '.DS_Store' '*/__MACOSX/*' '*/__pycache__/*' '*/Thumbs.db')

rm -rf "$repo/dist"
mkdir -p "$repo/dist"

cd "$plugin"
zip -q -r "$repo/dist/shootika-$version-openai.zip" .codex-plugin "${common[@]}" "${excludes[@]}"
zip -q -r "$repo/dist/shootika-$version-claude.zip" .claude-plugin "${common[@]}" "${excludes[@]}"

for archive in "dist/shootika-$version-openai.zip" "dist/shootika-$version-claude.zip"; do
  echo "$archive"
  unzip -l "$repo/$archive" | tail -1
done
