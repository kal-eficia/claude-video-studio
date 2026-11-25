#!/usr/bin/env bash
# Installs the open-source editing skills this studio builds on into .claude/skills.
# Safe to re-run: existing skills are updated with git pull.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p .claude/skills
get() { # name repo
  if [ -d ".claude/skills/$1/.git" ]; then git -C ".claude/skills/$1" pull --ff-only -q && echo "  updated $1"
  else git clone -q --depth 1 "$2" ".claude/skills/$1" && echo "  installed $1"; fi
}
echo "== Editing skills"
get video-use     https://github.com/browser-use/video-use
get cut-video     https://github.com/louisedesadeleer/cut-video
get add-zooms     https://github.com/louisedesadeleer/add-zooms
get b-roll-finder https://github.com/louisedesadeleer/b-roll-finder
get clipify       https://github.com/louisedesadeleer/clipify
echo "== HyperFrames skills"
npx -y skills add heygen-com/hyperframes --all --agent claude-code -y </dev/null
echo "Done. Start Claude Code here with: claude"
