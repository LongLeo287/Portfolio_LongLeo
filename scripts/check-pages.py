#!/usr/bin/env python3
"""Kiểm cấu trúc và tiếp cận của các landing page đã sinh.

Đọc thẳng HTML thay vì đo qua trình duyệt — khung xem trước không dựng khung
hình nên nhiều phép đo trả giá trị cũ. Những gì kiểm được tĩnh thì kiểm tĩnh:
thứ bậc tiêu đề, neo chết, id trùng, alt, rel=noopener, độ dài meta, kích thước
ảnh, và animation có đụng tới layout hay không.

    python scripts/build-repo-landing.py && python scripts/check-pages.py

Tương phản màu nằm ở scripts/check-contrast.py.
"""
import io
import os
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "build", "repo-landing")


def check(name, s):
    loi, canh = [], []

    # --- thứ bậc tiêu đề ---
    hs = re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", s, re.S)
    lv = [int(h[0]) for h in hs]
    n1 = lv.count(1)
    if n1 != 1:
        loi.append(f"có {n1} thẻ h1 (phải đúng 1)")
    for i in range(1, len(lv)):
        if lv[i] - lv[i - 1] > 1:
            txt = re.sub(r"<[^>]+>", "", hs[i][1]).strip()[:32]
            loi.append(f"nhảy bậc h{lv[i-1]} → h{lv[i]}: “{txt}”")
    for h in hs:
        if not re.sub(r"<[^>]+>", "", h[1]).strip():
            loi.append("có tiêu đề rỗng")
            break

    # --- id trùng ---
    ids = re.findall(r'\sid="([^"]+)"', s)
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        loi.append(f"id trùng: {', '.join(sorted(dup))}")

    # --- neo chết ---
    anchors = {m for m in re.findall(r'href="#([^"]+)"', s) if m}
    dead = sorted(anchors - set(ids) - {"top"})
    dead = [d for d in dead if f'id="{d}"' not in s]
    if dead:
        loi.append(f"neo chết: {', '.join('#' + d for d in dead)}")

    # --- liên kết ra ngoài ---
    blanks = re.findall(r"<a\b[^>]*target=\"_blank\"[^>]*>", s)
    bad = [a for a in blanks if "noopener" not in a]
    if bad:
        loi.append(f"{len(bad)} liên kết _blank thiếu rel=noopener")

    # --- ảnh ---
    imgs = re.findall(r"<img\b[^>]*>", s)
    no_alt = [i for i in imgs if "alt=" not in i]
    if no_alt:
        loi.append(f"{len(no_alt)} ảnh không có alt")
    no_dim = [i for i in imgs if "width=" not in i or "height=" not in i]
    if no_dim:
        canh.append(f"{len(no_dim)} ảnh thiếu width/height (dễ gây nhảy layout)")
    no_lazy = [i for i in imgs if 'loading="lazy"' not in i]
    if len(imgs) > 3 and len(no_lazy) > 2:
        canh.append(f"{len(no_lazy)}/{len(imgs)} ảnh không tải lười")

    # --- meta ---
    if 'lang="vi"' not in s[:400]:
        loi.append("thẻ html thiếu lang=\"vi\"")
    if "name=\"viewport\"" not in s:
        loi.append("thiếu meta viewport")
    if 'rel="canonical"' not in s:
        loi.append("thiếu canonical")
    m = re.search(r'name="description" content="([^"]*)"', s)
    if not m:
        loi.append("thiếu meta description")
    elif len(m.group(1)) > 165:
        canh.append(f"meta description {len(m.group(1))} ký tự (Google cắt ~160)")
    for tag in ("og:title", "og:description", "og:image", "og:url"):
        if f'"{tag}"' not in s:
            loi.append(f"thiếu {tag}")

    # --- focus + landmark ---
    if ":focus-visible" not in s:
        loi.append("không có style :focus-visible")
    if "<main" not in s:
        canh.append("không có thẻ <main>")
    if "<footer" not in s:
        canh.append("không có thẻ <footer>")

    # --- animation đụng layout ---
    for kf in re.finditer(r"@keyframes\s+([\w-]+)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", s):
        body = kf.group(2)
        hit = re.findall(r"(?<![-\w])(width|height|top|left|right|bottom|margin|padding|"
                         r"background-position|box-shadow)\s*:", body)
        if hit:
            loi.append(f"@keyframes {kf.group(1)} động tới {', '.join(set(hit))} "
                       f"— chỉ nên động transform/opacity")

    # --- số liệu ---
    so = {
        "KB": len(s) // 1024,
        "tiêu đề": len(hs),
        "ảnh": len(imgs),
        "keyframes": len(re.findall(r"@keyframes", s)),
        "vô hạn": len(re.findall(r"infinite", s)),
    }
    return loi, canh, so


def main():
    if not os.path.isdir(BASE):
        print("Chưa dựng — chạy scripts/build-repo-landing.py trước.")
        return 1
    tong_loi = 0
    for d in sorted(os.listdir(BASE)):
        f = os.path.join(BASE, d, "landing", "index.html")
        if not os.path.exists(f):
            continue
        loi, canh, so = check(d, io.open(f, encoding="utf-8").read())
        tong_loi += len(loi)
        head = " · ".join(f"{v} {k}" for k, v in so.items())
        print(f"\n{'LỖI' if loi else 'OK '}  {d}")
        print(f"      {head}")
        for x in loi:
            print(f"      ✗ {x}")
        for x in canh:
            print(f"      ! {x}")
    print(f"\nTổng số lỗi: {tong_loi}")
    return 1 if tong_loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
