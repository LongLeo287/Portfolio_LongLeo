#!/usr/bin/env python3
"""Kiểm tương phản của các landing page theo chuẩn WCAG AA.

    python scripts/build-repo-landing.py && python scripts/check-contrast.py

Không đo qua trình duyệt: pane không dựng khung hình nên getComputedStyle trả
giá trị cũ sau khi đổi thuộc tính theme, cho ra số vô lý (#475569 trên #f8fafc
ra 2.48:1). Đọc file thì kết quả tất định.
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

BASE = r"D:\SEOSONA AI\LongLeo Profolio\build\repo-landing"

# trang -> (thu muc, [(ten bien chu, ten bien nen, co chu px, mo ta)])
PAGES = {
    "OmniClaw": ("OmniClaw", "", [
        ("--text", "--bg", 15, "thân"), ("--muted", "--pane", 14, "phụ"),
        ("--dim", "--pane", 12, "mờ trên pane"), ("--dim", "--pane-2", 12, "mờ trên pane-2"),
        ("--dim", "--bg", 12, "mờ trên nền"), ("--lime", "--pane", 14, "nhấn xanh"),
        ("--amber", "--pane", 14, "nhấn cam"), ("--warn", "--bg", 14, "cảnh báo"),
    ]),
    "SEOSONA OS": ("SEOSONA-OS", "", [
        ("--text", "--bg", 16, "thân"), ("--muted", "--panel", 15, "phụ"),
        ("--dim", "--panel", 13, "mờ trên panel"), ("--dim", "--bg", 13, "mờ trên nền"),
        ("--gold", "--bg", 12, "nhấn vàng"), ("--amber", "--panel", 16, "amber"),
    ]),
    "Video AI": ("SEOSONA-Video-AI", "", [
        ("--text", "--bg", 16, "thân"), ("--muted", "--film", 15, "phụ"),
        ("--dim", "--film", 12, "mờ trên film"), ("--dim", "--bg", 12, "mờ trên nền"),
        ("--dim", "--film-2", 12, "mờ trên film-2"),
        ("--gold", "--film", 14, "nhấn vàng"), ("--hot", "--bg", 12, "nhấn cam"),
    ]),
    "UX-UI sáng": ("SEOSONA-UX-UI", "", [
        ("--text", "--bg", 16, "thân"), ("--muted", "--bg", 15, "phụ"),
        ("--muted", "--surface", 15, "phụ trên surface"),
        ("--dim", "--bg", 12, "mờ"), ("--dim", "--surface", 12, "mờ trên surface"),
        ("--brand", "--bg", 14, "nhấn"), ("--warn", "--bg", 15, "cảnh báo"),
        ("--ok", "--bg", 12, "ok"), ("--danger", "--bg", 12, "lỗi"),
    ]),
    "Flow": ("seosona-flow", "", [
        ("--text", "--bg", 16, "thân"), ("--text-muted", "--bg", 15, "phụ"),
        ("--text-dim", "--bg", 12, "mờ"), ("--cyan", "--bg", 14, "nhấn cyan"),
        ("--emerald", "--bg", 14, "nhấn emerald"),
    ]),
    "Tiệm Nước": ("Tiem_Nuoc_Nho_v5", "", [
        ("--text", "--bg", 16, "thân"), ("--muted", "--panel", 15, "phụ"),
        ("--dim", "--panel", 12, "mờ trên panel"), ("--dim", "--bg", 12, "mờ trên nền"),
        ("--dim", "--panel-2", 12, "mờ trên panel-2"),
        ("--brand", "--bg", 14, "đỏ nhấn"), ("--amber", "--panel", 14, "amber"),
    ]),
    "UX-UI tối": ("SEOSONA-UX-UI", "dark", [
        ("--text", "--bg", 16, "thân"), ("--muted", "--bg", 15, "phụ"),
        ("--dim", "--surface", 12, "mờ trên surface"),
        ("--brand", "--bg", 14, "nhấn"), ("--warn", "--bg", 15, "cảnh báo"),
    ]),
}


def lum(hexc):
    hexc = hexc.lstrip("#")
    if len(hexc) == 3:
        hexc = "".join(c * 2 for c in hexc)
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in (r, g, b)]
    return .2126 * f[0] + .7152 * f[1] + .0722 * f[2]


def ratio(a, b):
    l1, l2 = lum(a), lum(b)
    return (max(l1, l2) + .05) / (min(l1, l2) + .05)


def vars_of(css, block):
    """Lấy biến trong :root hoặc [data-theme=dark]."""
    if block == "dark":
        m = re.search(r'\[data-theme="dark"\]\s*\{(.*?)\}', css, re.S)
    else:
        m = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if not m:
        return {}
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})", m.group(1)))


total_fail = 0
for label, (d, block, checks) in PAGES.items():
    f = os.path.join(BASE, d, "landing", "index.html")
    if not os.path.exists(f):
        print(f"=== {label}  (chưa dựng, bỏ qua)\n")
        continue
    css = io.open(f, encoding="utf-8").read()
    root = vars_of(css, "")
    v = dict(root)
    if block == "dark":
        v.update(vars_of(css, "dark"))
    print(f"=== {label}")
    for fg, bg, px, desc in checks:
        if fg not in v or bg not in v:
            print(f"   ?  {fg} / {bg}  (khong tim thay bien)")
            continue
        r = ratio(v[fg], v[bg])
        need = 3 if px >= 24 else 4.5
        ok = r >= need
        if not ok:
            total_fail += 1
        print(f"   {'OK ' if ok else 'LOI'} {r:5.2f}:1  cần {need}  {px}px  "
              f"{fg}={v[fg]} trên {bg}={v[bg]}  — {desc}")
    print()

print(f"Tổng số cặp không đạt: {total_fail}")
