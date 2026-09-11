#!/usr/bin/env bash
# Install reality-check v2 into Claude Code: skill symlink + mode shims. Idempotent; keeps the previous target as reality-check-v1.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SK=~/.claude/skills; CM=~/.claude/commands
mkdir -p "$SK" "$CM"
if [ -L "$SK/reality-check" ] && [ "$(readlink "$SK/reality-check")" != "$HERE" ]; then
  [ -e "$SK/reality-check-v1" ] || ln -s "$(readlink "$SK/reality-check")" "$SK/reality-check-v1"
fi
ln -sfn "$HERE" "$SK/reality-check"
rm -rf "$CM/reality-check"; mkdir -p "$CM/reality-check"; cp "$HERE"/commands/*.md "$CM/reality-check/"
# Cross-runtime: shared hub + Codex CLI + Cursor CLI (both read SKILL.md from a skills dir; modes are typed in chat, e.g. "reality-check :recheck TKT-003")
for d in ~/.agents/skills ~/.codex/skills ~/.cursor/skills; do mkdir -p "$d"; ln -sfn "$HERE" "$d/reality-check"; done
echo "installed: $SK/reality-check -> $HERE; shims: $(ls "$CM/reality-check" | tr '\n' ' ')"
echo "cross-runtime: ~/.agents/skills/reality-check, ~/.codex/skills/reality-check, ~/.cursor/skills/reality-check -> $HERE"
