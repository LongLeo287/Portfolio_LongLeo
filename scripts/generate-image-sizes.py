#!/usr/bin/env python3
"""Generate responsive WebP derivatives for portfolio images.

Every image referenced by assets/data/projects.json gets a -480.webp and a
-960.webp sibling. app.js builds its srcset from those exact suffixes, so both
files must exist for every source — sources narrower than a target width are
re-encoded at native width rather than skipped, which keeps every srcset
candidate resolvable instead of 404-ing.

Run after adding or replacing any portfolio image:

    python scripts/generate-image-sizes.py

Requires Pillow:  pip install Pillow
"""
import json
import os
import sys
import urllib.parse
from PIL import Image

WIDTHS = (480, 960)
QUALITY = 80

# Avatar is handled separately: it is the LCP image and has its own srcset.
AVATAR = ("assets/img/longleo_avatar.webp", (366, 732), 82)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def derivatives(src, widths, quality):
    """Write <stem>-<width>.webp for each width. Returns bytes written."""
    written = 0
    stem, _ = os.path.splitext(src)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        for w in widths:
            out = f"{stem}-{w}.webp"
            resized = im.copy() if w >= w0 else im.resize((w, round(h0 * w / w0)), Image.LANCZOS)
            resized.save(out, "WEBP", quality=quality, method=5)
            written += os.path.getsize(out)
    return written


def main():
    os.chdir(ROOT)

    with open("assets/data/projects.json", encoding="utf-8-sig") as fh:
        projects = json.load(fh)

    sources = sorted({
        urllib.parse.unquote(p["imgSrc"])
        for p in projects
        if p.get("imgSrc") and not p["imgSrc"].startswith("http")
    })

    total, missing = 0, []
    for src in sources:
        if not os.path.exists(src):
            missing.append(src)
            continue
        total += derivatives(src, WIDTHS, QUALITY)

    avatar_src, avatar_widths, avatar_quality = AVATAR
    if os.path.exists(avatar_src):
        total += derivatives(avatar_src, avatar_widths, avatar_quality)
    else:
        missing.append(avatar_src)

    print(f"sources processed : {len(sources) - len(missing) + 1}")
    print(f"derivatives size  : {total / 1048576:.1f} MB")

    if missing:
        print(f"\nMISSING {len(missing)} source(s) referenced by projects.json:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
