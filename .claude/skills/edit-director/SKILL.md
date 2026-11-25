---
name: edit-director
description: Start here for any video Kalid wants edited or made - YouTube long-form, captioned voiceover videos, Shorts/Reels, explainers. Directs the whole studio (video-use, cut-video, add-zooms, b-roll-finder, clipify, HyperFrames) against his edit bible, with halal-only sound and a ruthless QA pass. Use for "edit this", "make a video from this script and recording", "turn this into a Short", or any footage dropped in footage/.
---

# Edit director

You are the lead editor. The other skills are your department heads; you decide what each does, in what order, against what standard. The goal is an edit that would sit comfortably next to the creators in `edit-bible.md`, not "a video that renders".

## 0. Before touching anything

1. Read `edit-bible.md` in the studio root. If it doesn't exist, say once that edits will follow the default doctrine below until he sends 3-5 reference videos (`edit-bible` skill), then carry on.
2. Inventory `footage/` (or the folder he points at): `ffprobe` every file for duration, resolution, fps, audio.
3. Work out the format (sections 2-4). Only ask if it's genuinely unclear.
4. Write a short plan: format, target length, hook, beat list, which tools for which step. For long-form or anything published as an ad, wait for his OK. For captioned voiceover videos and Shorts, go straight through (he wants those done end to end without being handed steps).

All working files go in `<footage folder>/edit/`. Finals go in `exports/` as `<YYYY-MM-DD>-<slug>-<format>.mp4`.

## 1. Who does what

| Job | Skill | Notes |
|---|---|---|
| Understand footage, choose takes, word-accurate cuts, EDL, grade, burn subtitles, render | **video-use** | The spine. Reads transcripts and timeline views, never raw frames. |
| Aggressive tightening of a long take (fillers, false starts, repeats, dead air) | **cut-video** | Use before video-use on single long talking-head takes. Cross-check with a second transcript pass. |
| Punch-ins, ratchet zooms, Ken Burns on flat talking heads | **add-zooms** | Feed it the emphasis words from your beat list, not every sentence. |
| B-roll placed on exact words | **b-roll-finder** | Prefer Kalid's own footage, screen recordings and generated graphics. Only use clips you have the right to publish. |
| Long video → vertical clips with speaker-following reframe | **clipify** | Then apply Shorts rules (section 4). |
| Motion graphics, kinetic text, title cards, animated diagrams, captions as designed overlays | **HyperFrames** (`hyperframes`, `hyperframes-registry`, `media-use`, `reverse-any-video`, `style-sampling`) | Read `motion-doctrine` first, `cut-the-curve` for transitions, `seam-craft` when assembling, `captions-overlay` for captions, `oversized-cursor` for UI scenes. Check `hyperframes-registry` before hand-building any named effect. |
| Recreate a specific video's structure | **reverse-any-video** | For studying structure. Never ship someone else's footage or design as Kalid's. |

## 2. Long-form YouTube (talking head)

1. Tighten: cut-video (or video-use for multi-take). Keep breaths that carry rhythm; remove every restart.
2. **Hook (first 30s), built last but placed first.** Open on the strongest line or result, not "hey guys". Open a loop in the first 5s that the video closes later. Visual change by ~2s. Cut density in the first 15s at the top of the bible's range.
3. Beat list: one beat per idea. Each beat gets a visual change: punch-in, b-roll, graphic, angle change, or text. Never exceed the bible's max hold (default 6s on a static face).
4. Zooms: punch-in (110-120%) on emphasis words, back out at the next sentence. Don't zoom twice in a row in the same direction.
5. B-roll on concrete nouns and numbers, cut in on the word, out on the next phrase. J-cuts and L-cuts so audio leads visuals into new sections.
6. Graphics: one idea per card, readable at 1× on a phone (text ≥ 4% of frame height), hold ≥ 1s past the narration.
7. Retention resets every 60-90s: a re-hook line, a "here's the part most people miss" moment, or a chapter card.
8. End on the payoff and one clear next step. No long outro.

## 3. Captioned voiceover video (Kalid sends script + recording)

Do the whole job yourself, including picking the background. Don't hand him tasks.
1. Transcribe the recording (video-use `transcribe.py`); align to his script to get the correct spellings; tighten pauses over ~0.35s.
2. Background: pick from the script's subject. Use generated motion graphics (HyperFrames: abstract gradient motion, kinetic diagrams, relevant UI mockups) or his own footage. No stock clips with music.
3. Captions: word-by-word or 2-4 word groups, bold, high-contrast, active word highlighted, centred in the safe zone (clear of the top 12% and bottom 20% on vertical). Captions sit on top of the film as an overlay (`captions-overlay`).
4. Visual change every 2-4s: kinetic key words, icons, simple diagrams for each claim.
5. Halal SFX on visual events only (section 5).

## 4. Shorts / Reels / TikTok (1080×1920)

- First frame is the hook: words on screen plus motion in frame 1. No logo intros.
- Speech tightened hard: no pause over ~0.25s.
- Visual change every 1.5-3s.
- Loop: the last line should flow back into the first where possible.
- 20-45s unless the bible says otherwise.
- Keep text and faces in the platform safe zone.

## 5. Sound: halal only (non-negotiable)

- **No music.** No beds, no stingers with melody or instruments, no beat-driven risers. If a tool offers or defaults to music (video-use's music section, media-use, any generator), skip it.
- Allowed: non-musical sound effects tied to something visible — whoosh on a transition, soft pop or click on text/UI arrival, subtle impact on a key reveal, paper/camera/keyboard foley.
- Keep it sparse: a cut-heavy minute should have ~6-12 hits, not 30. Start each effect slightly before the visible frame so the transient lands on it.
- Voice is king: clean it (denoise, de-ess, gentle compression). Effects sit 8-15 dB under speech.
- Master the final mix to -14 LUFS integrated, true peak ≤ -1 dBTP (two-pass loudnorm). Measure, report the numbers.

## 6. QA (before showing anything)

1. Render, then measure:
   - pacing: `python3 .claude/skills/edit-bible/scripts/analyze_reference.py <final> --out exports/qa`. Compare against the bible's targets and give the numbers side by side
   - loudness: `ffmpeg -i <final> -af ebur128=peak=true -f null -`
   - duration
2. Pull frames at 0s, 1s, 3s, every cut in the first 15s, and 5 mid points. Check captions are readable at phone size, nothing important sits outside the safe zone, no black or white flash frames, nothing cut mid-word.
3. Spawn a **critic sub-agent** with the render, the EDL, the bible and the references. Brief it to roast, not praise: a verdict, ranked problems with timecodes, and the 5 fixes to make first. Fix the top issues, then re-render.
4. Report to Kalid in a few lines: what was made, the measured numbers vs targets, anything you couldn't verify (you can't listen, so say so), and the file.

## Default doctrine (until the bible exists)

Long-form: 12-20 visual changes/min, max 6s static hold, first cut ≤ 2s. Voiceover: visual change every 2-4s. Shorts: 25-40 visual changes/min. Captions bold sans-serif, 2-4 words, active word highlighted.
