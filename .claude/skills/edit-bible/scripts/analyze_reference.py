#!/usr/bin/env python3
"""Measure the pacing fingerprint of a reference video. Stdlib + ffmpeg/ffprobe only.

Usage: python3 analyze_reference.py <video> [--out DIR] [--scene 0.30]
Writes DIR/<stem>/metrics.json, hook_sheet.jpg (first 15s), body_sheet.jpg (whole video).
"""
import argparse, json, re, statistics, subprocess, sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.strip())


def video_info(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate", "-of", "json", str(path)])
    s = json.loads(r.stdout)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return {"width": s["width"], "height": s["height"], "fps": round(float(n) / float(d), 2)}


def scene_cuts(path, thresh):
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-an", "-vf",
             f"select='gt(scene,{thresh})',showinfo", "-f", "null", "-"])
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def loudness(path):
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[0-9.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", r.stderr)
    return {"integrated_lufs": float(i[-1]) if i else None, "true_peak_dbfs": float(p[-1]) if p else None}


def pauses(path, noise="-35dB", min_d=0.25):
    r = run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn", "-af",
             f"silencedetect=noise={noise}:d={min_d}", "-f", "null", "-"])
    return [float(x) for x in re.findall(r"silence_duration: ([0-9.]+)", r.stderr)]


def sheet(path, out, start, length, cols, rows, width=360):
    n = cols * rows
    fps = n / max(length, 0.1)
    run(["ffmpeg", "-hide_banner", "-y", "-ss", str(start), "-t", str(length), "-i", str(path),
         "-vf", f"fps={fps:.4f},scale={width}:-2,tile={cols}x{rows}:padding=4", "-frames:v", "1", str(out)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="refs/analysis")
    ap.add_argument("--scene", type=float, default=0.30)
    a = ap.parse_args()
    src = Path(a.video)
    out = Path(a.out) / src.stem
    out.mkdir(parents=True, exist_ok=True)

    dur = duration(src)
    cuts = scene_cuts(src, a.scene)
    bounds = [0.0] + cuts + [dur]
    shots = [b - a_ for a_, b in zip(bounds, bounds[1:]) if b - a_ > 0.04]
    q = statistics.quantiles(shots, n=10) if len(shots) >= 2 else shots

    def cuts_in(t0, t1):
        return sum(1 for c in cuts if t0 <= c < t1)

    windows = []
    t = 0.0
    while t < dur:
        t1 = min(t + 30, dur)
        windows.append({"from_s": round(t), "to_s": round(t1), "cuts": cuts_in(t, t1)})
        t = t1

    ps = pauses(src)
    m = {
        "file": src.name,
        "duration_s": round(dur, 2),
        **video_info(src),
        "scene_threshold": a.scene,
        "cuts_total": len(cuts),
        "cuts_per_minute": round(len(cuts) / dur * 60, 1) if dur else 0,
        "shot_length_s": {
            "mean": round(statistics.mean(shots), 2) if shots else None,
            "median": round(statistics.median(shots), 2) if shots else None,
            "p10": round(q[0], 2) if len(q) > 1 else None,
            "p90": round(q[-1], 2) if len(q) > 1 else None,
            "longest": round(max(shots), 2) if shots else None,
        },
        "hook": {
            "cuts_first_5s": cuts_in(0, 5),
            "cuts_first_15s": cuts_in(0, 15),
            "cuts_first_30s": cuts_in(0, 30),
            "first_cut_at_s": round(cuts[0], 2) if cuts else None,
        },
        "cuts_per_30s_window": windows,
        "audio": {
            **loudness(src),
            "pauses_over_0_25s": len(ps),
            "pauses_per_minute": round(len(ps) / dur * 60, 1) if dur else 0,
            "longest_pause_s": round(max(ps), 2) if ps else 0,
        },
        "cut_times_s": [round(c, 2) for c in cuts],
        "note": "Scene detection catches hard cuts and big visual changes; punch-in zooms on the same shot and "
                "subtle caption changes are often missed. Read the contact sheets for those.",
    }
    (out / "metrics.json").write_text(json.dumps(m, indent=2))
    sheet(src, out / "hook_sheet.jpg", 0, min(15, dur), 5, 3)
    sheet(src, out / "body_sheet.jpg", 0, dur, 6, 5, 300)
    print(json.dumps({k: m[k] for k in ("file", "duration_s", "cuts_per_minute", "shot_length_s", "hook", "audio")}, indent=2))
    print(f"\nWrote {out}/metrics.json, hook_sheet.jpg, body_sheet.jpg")


if __name__ == "__main__":
    sys.exit(main())
