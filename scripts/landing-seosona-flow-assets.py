#!/usr/bin/env python3
"""Chuẩn bị ảnh thư viện mẫu cho landing page SEOSONA Flow.

Ảnh gốc là 88 file PNG 512×512 nằm trong repo seosona-flow
(`seosona-flow/assets/templates/thumb_*.png`) — ảnh thật do chính extension
sinh ra, không phải ảnh stock. Script kéo về, chọn lọc, đổi sang WebP hai cỡ.

    python scripts/landing-seosona-flow-assets.py

Ảnh gốc KHÔNG chép vào repo portfolio (mỗi tấm ~100 KB, tổng gần 9 MB). Bản
đã nén nằm ở build/ và chỉ được đẩy sang repo seosona-flow.

Yêu cầu: gh đã đăng nhập, pip install Pillow.
"""
import base64
import io
import json
import os
import subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "build", "cache", "flow-thumbs")
OUT = os.path.join(ROOT, "build", "repo-landing", "seosona-flow", "landing", "gallery")
SRC = "seosona-flow/assets/templates"
REPO = "LongLeo287/seosona-flow"

# Chọn thủ công 12 tấm: đa dạng thể loại và KHÔNG dính hình ảnh của bên thứ ba.
# Đã loại #1005 (chân dung người nổi tiếng + logo thương hiệu trong ảnh ghép
# pop-culture) và #1 (biển quảng cáo hãng xe trong sân bóng) — ảnh do AI sinh
# nhưng vẫn là nhãn hiệu và chân dung của người khác, không đáng mạo hiểm
# trên một trang giới thiệu công khai.
PICKS = [
    (1003, "Bảng thiết kế nhân vật", "6 tư thế từ một thiết kế gốc, giữ nguyên trang phục"),
    (1001, "Phác thảo đến thành phẩm", "Bốn bước từ nét chì tới ảnh điện ảnh"),
    (1004, "Ba phong cách kiến trúc", "Cyberpunk, Solarpunk, Art Deco cùng một khung"),
    (1006, "Quảng cáo nước hoa", "Ảnh sản phẩm kèm bố cục chú thích"),
    (1007, "Bản đồ ý tưởng", "Sơ đồ khám phá sáng tạo phát sáng"),
    (1009, "Trang bán hàng", "Ảnh sản phẩm và các khối tính năng"),
    (1010, "Bộ ảnh món ăn", "Chín món, cùng ánh sáng và tông màu"),
    (1012, "Bộ nhận diện thương hiệu", "Danh thiếp, bảng màu, phông chữ"),
    (1013, "Giao diện ứng dụng", "Ba màn hình điện thoại cùng phong cách"),
    (1014, "Ảnh Tết", "Hộp quà, câu đối, đèn lồng"),
    (1017, "Các bước làm bánh", "Bốn khoảnh khắc liền mạch một quy trình"),
    (1018, "Lookbook thời trang", "Bốn bối cảnh, cùng một người mẫu"),
]

SIZES = (320, 480)


def fetch(n):
    """Tải một thumbnail về cache. Contents API trả base64 nên phải giải mã."""
    dst = os.path.join(CACHE, f"thumb_{n}.png")
    if os.path.exists(dst):
        return dst
    os.makedirs(CACHE, exist_ok=True)
    r = subprocess.run(
        ["gh", "api", f"repos/{REPO}/contents/{SRC}/thumb_{n}.png", "-q", ".content"],
        capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"khong tai duoc thumb_{n}: {r.stderr.strip()}")
    open(dst, "wb").write(base64.b64decode(r.stdout))
    return dst


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    manifest = []
    for i, (n, title, sub) in enumerate(PICKS, 1):
        im = Image.open(fetch(n)).convert("RGB")
        for w in SIZES:
            out = os.path.join(OUT, f"g{i:02d}-{w}.webp")
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(
                out, "WEBP", quality=76, method=6)
            total += os.path.getsize(out)
        manifest.append({"i": i, "src": n, "title": title, "sub": sub,
                         "w": im.width, "h": im.height})
        print(f"  g{i:02d}  {os.path.getsize(os.path.join(OUT, f'g{i:02d}-480.webp'))//1024:>3} KB  "
              f"{title}")

    io.open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"\n{len(PICKS)} ảnh × {len(SIZES)} cỡ = {total // 1024} KB tổng "
          f"(tải lười, nằm dưới màn hình đầu)")


if __name__ == "__main__":
    raise SystemExit(main())
