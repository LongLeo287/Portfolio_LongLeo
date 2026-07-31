#!/usr/bin/env python3
"""Build the hero showreel loop from the portfolio's own images.

Renders a silent, seamless-looping 16:9 clip: a slow push-in on each shot,
dissolving between them, with the last shot dissolving back into the first so
the loop has no visible seam.

It plays in the hero's visual card as the main image, so it is graded to sit
in a dark UI rather than to hide behind text.

    python scripts/build-hero-reel.py

Requires Pillow and ffmpeg on PATH.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from PIL import Image, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The card renders at ~420px wide, ~840 on a 2x display. 960x540 is already
# more than it can show; 720p just spent bits nobody sees.
W, H = 960, 540
FPS = 24
SHOT_SECONDS = 2.0
CROSSFADE_SECONDS = 0.7
SHOT_COUNT = 10
ZOOM_FROM, ZOOM_TO = 1.0, 1.12
# The reel is the hero's main visual, not a backdrop, so it plays close to
# full strength — only knocked back enough to sit inside a dark UI without
# glaring, and to keep the avatar badge legible on top of it.
BRIGHTNESS = 0.88
SATURATION = 1.0

OUT_MP4 = "assets/video/hero-reel.mp4"
OUT_POSTER = "assets/video/hero-reel-poster.jpg"


def pick_sources():
    """Featured work first, then the largest remaining stills, alternating
    category so consecutive shots never look like the same job."""
    with open("assets/data/projects.json", encoding="utf-8") as fh:
        projects = json.load(fh)

    stills = [
        p for p in projects
        if p.get("category") in ("Design", "Photography", "Thumbnail")
        and p.get("imgSrc") and not p["imgSrc"].startswith("http")
    ]

    def usable(p):
        path = urllib.parse.unquote(p["imgSrc"])
        return path if os.path.exists(path) else None

    buckets = {}
    for p in sorted(stills, key=lambda p: (not p.get("isFeatured"),)):
        path = usable(p)
        if path:
            buckets.setdefault(p["category"], []).append(path)

    picked, order = [], ["Design", "Photography", "Thumbnail"]
    while len(picked) < SHOT_COUNT:
        progressed = False
        for cat in order:
            if buckets.get(cat):
                picked.append(buckets[cat].pop(0))
                progressed = True
                if len(picked) == SHOT_COUNT:
                    break
        if not progressed:
            break
    return picked


def render_shot(path, frames):
    """Yield `frames` frames of a slow push-in, cropped to fill the frame.

    Cover-cropping rather than fitting is deliberate: a letterboxed banner
    reads as "a picture of an ad", a crop reads as texture — which is what a
    backdrop should be."""
    with Image.open(path) as src:
        img = src.convert("RGB")

    # Pre-scale once at the maximum zoom, then crop a shrinking window out of
    # it — one LANCZOS resize instead of one per frame.
    scale = max(W / img.width, H / img.height) * ZOOM_TO
    big = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    big = ImageEnhance.Brightness(big).enhance(BRIGHTNESS)
    big = ImageEnhance.Color(big).enhance(SATURATION)

    out = []
    for i in range(frames):
        t = i / max(frames - 1, 1)
        z = ZOOM_TO - (ZOOM_TO - ZOOM_FROM) * t   # push in = window shrinks
        cw, ch = round(W * z), round(H * z)
        cw, ch = min(cw, big.width), min(ch, big.height)
        left = (big.width - cw) // 2
        top = (big.height - ch) // 2
        out.append(big.crop((left, top, left + cw, top + ch)).resize((W, H), Image.BILINEAR))
    return out


def main():
    os.chdir(ROOT)
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found on PATH", file=sys.stderr)
        return 1

    sources = pick_sources()
    if len(sources) < 4:
        print(f"only {len(sources)} usable stills — need at least 4", file=sys.stderr)
        return 1
    print(f"shots: {len(sources)}")

    os.makedirs("assets/video", exist_ok=True)
    frames_per_shot = max(1, round(SHOT_SECONDS * FPS))
    tmp = tempfile.mkdtemp(prefix="reel_")
    n = 0
    try:
        fade = max(1, round(CROSSFADE_SECONDS * FPS))
        prev_tail = None
        for idx, path in enumerate(sources):
            shot = render_shot(path, frames_per_shot)
            if prev_tail is not None:
                # Dissolve the previous shot's tail into this one's head.
                for k in range(fade):
                    a = Image.blend(prev_tail[k], shot[k], (k + 1) / (fade + 1))
                    a.save(os.path.join(tmp, f"f{n:05d}.jpg"), "JPEG", quality=86)
                    n += 1
                shot = shot[fade:]
            # Hold back this shot's tail to dissolve into the next one; the
            # last shot dissolves into the first so the loop has no seam.
            prev_tail = shot[-fade:]
            for frame in shot[:-fade]:
                frame.save(os.path.join(tmp, f"f{n:05d}.jpg"), "JPEG", quality=86)
                n += 1

        loop_head = render_shot(sources[0], frames_per_shot)[:fade]
        for k in range(fade):
            a = Image.blend(prev_tail[k], loop_head[k], (k + 1) / (fade + 1))
            a.save(os.path.join(tmp, f"f{n:05d}.jpg"), "JPEG", quality=86)
            n += 1
        print(f"frames: {n}  ({n / FPS:.1f}s)")

        common = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                  "-i", os.path.join(tmp, "f%05d.jpg")]

        subprocess.run(common + [
            "-c:v", "libx264", "-profile:v", "high", "-crf", "33",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", OUT_MP4
        ], check=True)

        # No WebM: VP9 encoded this material *larger* than H.264 at matching
        # quality, and H.264 plays everywhere including iOS. One file is both
        # smaller and simpler.

        # Poster = first frame, so the swap to video is invisible.
        Image.open(os.path.join(tmp, "f00000.jpg")).save(
            OUT_POSTER, "JPEG", quality=82, optimize=True, progressive=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for f in (OUT_MP4, OUT_POSTER):
        print(f"  {os.path.getsize(f)/1024:>7.0f} KB  {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
