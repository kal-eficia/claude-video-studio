#!/usr/bin/env bash
# One-time setup for Kalid's video studio (macOS, Apple silicon).
# Safe to re-run. Claude Code runs this itself on the first session in this folder.
set -euo pipefail

STUDIO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
cd "$STUDIO"
ok()   { printf "  \033[32m✓\033[0m %s\n" "$1"; }
warn() { printf "  \033[33m!\033[0m %s\n" "$1"; }

echo "== Media tools"
mkdir -p bin
link_tool() { # name, candidate paths...
  local name="$1"; shift
  for p in "$@"; do
    if [ -x "$p" ]; then
      ln -sfn "$p" "bin/$name"
      xattr -d com.apple.quarantine "$p" 2>/dev/null || true
      ok "$name -> $p"; return 0
    fi
  done
  if command -v "$name" >/dev/null 2>&1; then ok "$name (system: $(command -v "$name"))"; return 0; fi
  if command -v brew >/dev/null 2>&1; then brew install "$name" && ok "$name (brew)" && return 0; fi
  warn "$name not found"; return 1
}
link_tool ffmpeg  "$HOME/tools/ffmpeg-dl/ffmpeg"
link_tool ffprobe "$HOME/tools/ffmpeg-dl/ffprobe"
link_tool yt-dlp  "$HOME/tools/ytdlp-dl/yt-dlp_macos"
[ -x "$HOME/tools/ytdlp-dl/deno" ] && ln -sfn "$HOME/tools/ytdlp-dl/deno" bin/deno
export PATH="$STUDIO/bin:$PATH"
ffmpeg -hide_banner -version | head -1

echo "== Python environment (.venv)"
PY="$(command -v python3.12 || command -v python3.11 || command -v python3)"
[ -d .venv ] || "$PY" -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q requests librosa matplotlib pillow numpy praatio mlx-whisper
.venv/bin/python -c "import librosa, mlx_whisper, PIL; print('  python deps ok')"

echo "== HyperFrames (motion graphics engine)"
if command -v npx >/dev/null 2>&1; then
  npx -y skills add heygen-com/hyperframes --all --agent claude-code -y </dev/null \
    && ok "HyperFrames skills installed in .claude/skills" \
    || warn "HyperFrames skill install failed; run: npx skills add heygen-com/hyperframes --all"
  npx -y hyperframes --version </dev/null >/dev/null 2>&1 && ok "HyperFrames CLI ready" || warn "HyperFrames CLI will download on first use"
else
  warn "Node.js not found. Install Node 20+ (nodejs.org) for HyperFrames."
fi

echo "== Transcription"
if grep -qE '^ELEVENLABS_API_KEY=.+' .claude/skills/video-use/.env 2>/dev/null; then
  ok "ElevenLabs key present (best accuracy + speaker labels)"
else
  ok "Using free on-device transcription (mlx-whisper). Add ELEVENLABS_API_KEY to .claude/skills/video-use/.env for speaker labels."
fi

echo
echo "Studio ready: $STUDIO"
