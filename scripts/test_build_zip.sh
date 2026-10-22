#!/usr/bin/env bash
# Tests scripts/build-openai-zip.sh on a copy of the committed tree with a planted .DS_Store and a
# stale dist/ entry: both archives exist, carry the right manifest, and carry nothing they should not.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
version="$(tr -d '[:space:]' < "$repo/VERSION")"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

git -C "$repo" archive HEAD | tar -x -C "$tmp"
cp "$repo/scripts/build-openai-zip.sh" "$tmp/scripts/build-openai-zip.sh" 2>/dev/null || true
printf '\0' > "$tmp/.DS_Store"
printf '\0' > "$tmp/skills/.DS_Store"
mkdir -p "$tmp/dist" && printf 'stale' > "$tmp/dist/old.zip"

(cd "$tmp" && bash scripts/build-openai-zip.sh > /dev/null)

fail=0
problem() { echo "FAIL: $1"; fail=1; }
# Each archive is listed once into a file; grepping a pipe from unzip under pipefail is racy
# (grep -q exits early, unzip dies of SIGPIPE, the pipeline fails at random).
listing() { local f="$1.list"; [ -f "$f" ] || unzip -Z1 "$1" > "$f"; echo "$f"; }
contains() { grep -qx "$2" "$(listing "$1")" || problem "$1 lacks $2"; }
lacks_prefix() { if grep -q "^$2" "$(listing "$1")"; then problem "$1 contains $2"; fi; }
lacks_name() { if grep -q "$2" "$(listing "$1")"; then problem "$1 contains $2"; fi; }

openai="$tmp/dist/shootika-$version-openai.zip"
claude="$tmp/dist/shootika-$version-claude.zip"
[ -f "$openai" ] || problem "missing $openai"
[ -f "$claude" ] || problem "missing $claude"
[ ! -e "$tmp/dist/old.zip" ] || problem "stale dist/old.zip survived"

if [ "$fail" -eq 0 ]; then
  contains "$openai" ".codex-plugin/plugin.json"
  lacks_prefix "$openai" ".claude-plugin/"
  contains "$claude" ".claude-plugin/plugin.json"
  lacks_prefix "$claude" ".codex-plugin/"
  for z in "$openai" "$claude"; do
    for f in .mcp.json README.md LICENSE assets/icon.png; do contains "$z" "$f"; done
    for s in "$tmp"/skills/*/; do contains "$z" "skills/$(basename "$s")/SKILL.md"; done
    for p in .git .github .claude/ docs/ listing/ scripts/ dist/; do lacks_prefix "$z" "$p"; done
    lacks_name "$z" ".DS_Store"
  done
fi

[ "$fail" -eq 0 ] && echo "ok" || exit 1
