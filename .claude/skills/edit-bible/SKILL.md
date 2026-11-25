---
name: edit-bible
description: Build or update Kalid's channel edit bible (edit-bible.md) from 3-5 reference videos by creators he wants to match. Measures pacing, hook structure, zoom and b-roll rhythm, caption style and loudness, then writes hard targets every edit must hit. Use when he says "build my edit bible", "study these videos", "match this creator's style", or drops links or files into refs/.
---

# Edit bible

The edit bible is the taste layer. Every other skill in this studio can cut, zoom, caption and animate. This file tells them *how this channel cuts*, in numbers and rules, so edits stop looking generic. `edit-director` reads `edit-bible.md` before every edit.

## Inputs

3-5 reference videos (YouTube/Shorts/Reel links or local files). Ask once which format each represents (long-form talking head, voiceover explainer, Short/Reel) if it isn't obvious. Two references of the same format beat five mixed ones.

## Steps

1. **Get the files** into `refs/`. Links: `yt-dlp -f "bv*[height<=1080]+ba/b" -o "refs/%(uploader)s - %(title).60s.%(ext)s" <url>`. These are for private study only; never reuse their footage, audio or graphics in an edit.

2. **Measure each one:**
   ```bash
   python3 .claude/skills/edit-bible/scripts/analyze_reference.py "refs/<file>" --out refs/analysis
   ```
   Gives cuts/min, shot-length spread, hook cut density (first 5/15/30s), cuts per 30s window (shows whether pacing slows after the hook), loudness, and pause rate. Two contact sheets: `hook_sheet.jpg` (first 15s) and `body_sheet.jpg`.

3. **Transcribe the hook.** Run video-use's `transcribe.py` on the first 60s (or the whole thing if under 3 min). Get words per minute and the exact hook script.

4. **Look, don't guess.** Open both contact sheets and 6-10 frames you pull yourself (`ffmpeg -ss <t> -i <file> -frames:v 1 refs/analysis/<stem>/f_<t>.jpg`) around cut times. Note what scene detection misses: punch-in zooms on the same shot, caption style (font weight, case, size relative to frame, words per caption, highlight colour, position), text-on-screen frequency, b-roll vs face ratio, colour/grade, framing (centre/rule of thirds, headroom), graphics style.

5. **Break down each hook** in the first 5-15s: what's said, what's shown, the open loop (the question the viewer now needs answered), and when the first payoff lands.

6. **Write `edit-bible.md`** in the studio root using the template below. Use ranges taken from the references (for example "cuts/min 18-26, median shot 2.1-3.0s"), not single numbers. Where references disagree, pick the one Kalid named as the main target and note the others.

7. **Show Kalid a one-screen summary** (the targets table and the 5 signature moves) and save. On later runs, update the file rather than starting over, and keep a short changelog at the bottom.

## Template for edit-bible.md

```markdown
# Edit bible: <channel / format>
References: <creator — title (format)> ×3-5
Last updated: <date>

## Hard targets (measured)
| Metric | Long-form | Voiceover/explainer | Shorts/Reels |
|---|---|---|---|
| Cuts per minute (incl. punch-ins) | | | |
| Median shot length | | | |
| Longest allowed hold without a visual change | | | |
| Cuts in first 5s / 15s | | | |
| Speech rate (wpm) after tightening | | | |
| Max pause left in | | | |
| Integrated loudness / true peak | -14 LUFS / -1 dBTP | | |

## Hook formula
Structure, timing of the first payoff, open-loop pattern, 2-3 example hooks rewritten for Kalid's topics.

## Visual rhythm
Punch-in zoom pattern (on which words, scale %, hold), b-roll density and placement rules, text-on-screen rules, graphic style.

## Captions
Font, weight, case, size (% of frame height), words per line, highlight rule, position and safe zones, animation.

## Look
Grade, framing, background, colour palette.

## Sound (halal only)
SFX palette and density (hits per minute), what each is tied to. No music. No melodic stingers.

## 5 signature moves
The specific repeatable things that make these references feel like themselves.

## Never do
Things the references avoid that AI edits often do.

## Changelog
```

## Rules

- Measured numbers come from the script output, not memory. Say which metrics are estimates from looking at frames.
- Kalid's videos use halal sound effects only. If a reference relies on music for energy, write down what the music was *doing* (pace, tension, release) and how to get that with cutting, SFX and voice instead.
