#!/usr/bin/env python3
"""Đồng bộ video mới từ kênh YouTube vào portfolio.

Đọc RSS công khai của kênh (không cần API key, không cần đăng nhập), tìm
những video chưa có trong projects.json, rồi làm hộ toàn bộ phần việc tay:

  1. tải thumbnail về, đặt tên đúng theo video ID
  2. sinh bản -480.webp và -960.webp
  3. thêm một mục vào projects.json đúng định dạng song ngữ
  4. bump tham số ?v= của projects.json trong app.js — nếu quên bước này
     trình duyệt sẽ tiếp tục dùng bản JSON cũ trong cache và video mới
     không hiện ra

Mặc định chỉ LIỆT KÊ, không ghi gì. Phải thêm --add mới thực sự viết vào
projects.json. Lý do: không phải video nào lên kênh cũng thuộc portfolio —
tuyển tập nhạc, vlog cá nhân, video reup… đều sẽ lọt vào nếu đồng bộ mù.

Cách dùng:

    python scripts/sync-youtube.py                      # xem có gì mới
    python scripts/sync-youtube.py --url <link> --add   # thêm 1 video cụ thể
    python scripts/sync-youtube.py --add                # thêm tất cả video mới
    python scripts/sync-youtube.py --url <link> --add --featured

Sau khi chạy: sửa lại tiêu đề tiếng Anh nếu muốn (script để tạm bằng tiêu
đề gốc), rồi commit.

Yêu cầu: pip install Pillow
"""
import argparse
import io
import json
import os
import re
import sys
import urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDLE = "@LongLeo287"
PROJECTS = "assets/data/projects.json"
THUMBS = "assets/img/thumbnails"
APP_JS = "assets/js/app.js"
UA = {"User-Agent": "Mozilla/5.0 (portfolio-sync)"}

# Chất lượng thumbnail giảm dần — Shorts thường không có maxresdefault.
THUMB_QUALITIES = ("maxresdefault", "sddefault", "hqdefault")
WIDTHS = (480, 960)


def fetch(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def channel_id(handle):
    html = fetch(f"https://www.youtube.com/{handle}").decode("utf-8", "replace")
    m = re.search(r'"(?:channelId|externalId)"\s*:\s*"(UC[\w-]{22})"', html)
    if not m:
        raise SystemExit(f"Không tìm được channel ID cho {handle}")
    return m.group(1)


def latest_videos(cid):
    """RSS trả về 15 video mới nhất. Đủ cho nhịp đăng bình thường."""
    xml = fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}").decode("utf-8", "replace")
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    out = []
    for e in entries:
        vid = re.search(r"<yt:videoId>([\w-]{11})</yt:videoId>", e)
        title = re.search(r"<media:title>(.*?)</media:title>", e, re.S)
        pub = re.search(r"<published>(.*?)</published>", e)
        if vid and title:
            out.append({
                "id": vid.group(1),
                "title": unescape(title.group(1).strip()),
                "published": pub.group(1)[:10] if pub else "",
            })
    return out


def unescape(s):
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")):
        s = s.replace(a, b)
    return s


def video_title(vid):
    """oEmbed — dùng khi thêm một video cụ thể không nằm trong 15 mục RSS."""
    data = json.loads(fetch(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"))
    return data["title"]


def download_thumb(vid, dest):
    for q in THUMB_QUALITIES:
        try:
            data = fetch(f"https://img.youtube.com/vi/{vid}/{q}.jpg", timeout=25)
        except Exception:
            continue
        # YouTube trả ảnh placeholder xám 120x90 thay vì 404 trong vài trường hợp
        if len(data) < 2000:
            continue
        with open(dest, "wb") as fh:
            fh.write(data)
        return q
    return None


def make_derivatives(src):
    with Image.open(src) as im:
        im = im.convert("RGB")
        w0, h0 = im.size
        stem, _ = os.path.splitext(src)
        for w in WIDTHS:
            out = f"{stem}-{w}.webp"
            resized = im.copy() if w >= w0 else im.resize((w, round(h0 * w / w0)), Image.LANCZOS)
            resized.save(out, "WEBP", quality=80, method=5)


def next_id(projects):
    nums = [int(m.group(1)) for p in projects if (m := re.match(r"proj_(\d+)$", p.get("id", "")))]
    return f"proj_{max(nums) + 1:03d}" if nums else "proj_001"


def build_entry(pid, vid, title, featured):
    """Giữ đúng hình dạng các mục Video đang có, kể cả phần caseStudy."""
    return {
        "id": pid,
        "title": {"vi": title, "en": title},
        "category": "Video",
        "client": {"vi": "YouTube @LongLeo287", "en": "YouTube @LongLeo287"},
        "imgSrc": f"{THUMBS}/{vid}.jpg",
        "href": f"https://www.youtube.com/watch?v={vid}",
        "alt": title,
        "isFeatured": featured,
        "caseStudy": {
            "role": {"vi": "Video Editor / Cameraman", "en": "Video Editor / Cameraman"},
            "concept": {"vi": "", "en": ""},
            "challenge": {"vi": "", "en": ""},
            "solution": {"vi": "", "en": ""},
            "tools": ["Premiere Pro", "After Effects"],
        },
    }


def bump_cache_param(dry):
    """projects.json được fetch kèm ?v= — không bump thì trình duyệt dùng bản cũ."""
    path = os.path.join(ROOT, APP_JS)
    src = io.open(path, encoding="utf-8").read()
    m = re.search(r"projects\.json\?v=([\d.]+)", src)
    if not m:
        print("  ! không tìm thấy tham số ?v= trong app.js — hãy bump thủ công")
        return None
    old = m.group(1)
    parts = old.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    new = ".".join(parts)
    if not dry:
        io.open(path, "w", encoding="utf-8").write(src.replace(f"projects.json?v={old}", f"projects.json?v={new}"))
    return f"{old} → {new}"


def main():
    ap = argparse.ArgumentParser(description="Đồng bộ video YouTube mới vào portfolio")
    ap.add_argument("--url", help="Thêm đúng một video (link hoặc ID)")
    ap.add_argument("--add", action="store_true", help="Thực sự ghi vào projects.json (mặc định chỉ liệt kê)")
    ap.add_argument("--featured", action="store_true", help="Đánh dấu nổi bật")
    args = ap.parse_args()
    dry = not args.add

    os.chdir(ROOT)
    projects = json.load(io.open(PROJECTS, encoding="utf-8"))
    have = {m.group(1) for p in projects
            if (m := re.search(r"[?&]v=([\w-]{11})", p.get("href", "") or ""))}

    if args.url:
        m = re.search(r"([\w-]{11})", args.url)
        if not m:
            raise SystemExit("Không đọc được video ID từ tham số --url")
        vid = m.group(1)
        candidates = [{"id": vid, "title": video_title(vid), "published": ""}]
    else:
        cid = channel_id(HANDLE)
        print(f"Kênh {HANDLE} → {cid}")
        candidates = latest_videos(cid)
        print(f"RSS trả về {len(candidates)} video mới nhất")

    new = [c for c in candidates if c["id"] not in have]
    print(f"Đã có trong portfolio: {len(candidates) - len(new)} · Sẽ thêm: {len(new)}\n")

    if not new:
        print("Không có video nào mới. Xong.")
        return 0

    added = 0
    for c in new:
        vid, title = c["id"], c["title"]
        dest = os.path.join(THUMBS, f"{vid}.jpg")
        print(f"  {vid}  {title[:58]}")

        if dry:
            print("        (chưa thêm — chạy lại kèm --add)")
            added += 1
            continue

        q = download_thumb(vid, dest)
        if not q:
            print("        ! không tải được thumbnail — bỏ qua video này")
            continue
        make_derivatives(dest)
        pid = next_id(projects)
        projects.append(build_entry(pid, vid, title, args.featured))
        print(f"        thumbnail {q} · {pid} · đã sinh -480/-960")
        added += 1

    if not dry and added:
        with io.open(PROJECTS, "w", encoding="utf-8") as fh:
            json.dump(projects, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        bumped = bump_cache_param(False)
        print(f"\nĐã ghi {PROJECTS} — tổng {len(projects)} dự án")
        if bumped:
            print(f"Đã bump cache app.js: {bumped}")
        print("\nCòn lại: sửa tiêu đề tiếng Anh nếu muốn, rồi commit.")
    elif dry:
        print(f"\nCó {added} video có thể thêm — chưa ghi gì cả.")
        print("  Thêm tất cả      : python scripts/sync-youtube.py --add")
        print("  Chỉ thêm một cái : python scripts/sync-youtube.py --url <link> --add")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
