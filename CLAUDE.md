# Kalid's video studio

This folder is a video editing studio for Claude Code. Footage in, finished videos out.

## How to work here

- For any edit or new video, load the `edit-director` skill first. It routes to the other skills and holds the standards.
- `edit-bible.md` (once it exists) is the channel's style law. Every edit hits its targets. Build or update it with the `edit-bible` skill.
- Raw footage: `footage/<project>/`. Working files: `footage/<project>/edit/`. Finals: `exports/`. Reference videos for study: `refs/`.
- Do every step yourself (installs, renders, fixes, re-renders). Don't hand Kalid commands to run unless something genuinely needs his password or an API key.
- HyperFrames is the motion-graphics engine. Don't mix in Remotion unless Kalid asks.

## Non-negotiables

- **Halal sound only.** No music of any kind in any video: no beds, no melodic stingers, no beat-driven risers. Non-musical sound effects only. Turn off or skip any tool step that adds music.
- Don't mention birthdays in on-screen text or captions.
- Scripts Kalid reads aloud should sound like natural speech, not choppy written copy.
- Only use footage, images and audio Kalid owns or has the right to publish. Reference videos are for study only.
- Measure before claiming quality: pacing, loudness and frames. You can't hear the mix, so report numbers.

## Environment (Kalid's MacBook Air)

- First session in this folder: if `.venv/` or `bin/ffmpeg` is missing, run `./setup.sh` yourself before anything else.
- Start every shell command with `export PATH="$PWD/bin:$PWD/.venv/bin:$PATH"` (run from the studio root) so ffmpeg, ffprobe, yt-dlp and the studio Python are used.
- Transcription: if `.claude/skills/video-use/.env` has an ElevenLabs key, use video-use's `transcribe.py`. Otherwise use `helpers/transcribe_local.py` (free, on-device, same output format, no speaker labels). Where clipify or other skills call the `whisper` CLI, use `mlx_whisper` with `--word-timestamps True --output-format json` instead.
