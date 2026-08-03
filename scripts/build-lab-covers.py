#!/usr/bin/env python3
"""Sinh ảnh bìa cho các trang trong labs/.

Thay cho ảnh OG mặc định của GitHub — tám tấm chữ trắng nền xám giống hệt
nhau. Bộ này dùng đúng nhận diện amber/tối của portfolio, và mỗi dự án lệch
màu + lệch vị trí quầng sáng một chút để phân biệt được ngay trong lưới.

    python scripts/build-lab-covers.py

Xuất ra assets/img/labs/<slug>{.jpg,-480.webp,-960.webp}.
Yêu cầu: pip install Pillow
"""
import io
import math
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 600
FONTDIR = r"C:\Windows\Fonts"

BG = (12, 10, 9)
AMBER = (252, 211, 77)
ORANGE = (255, 122, 0)
TEXT = (250, 250, 249)
MUTED = (150, 143, 138)

# slug, tên, nhãn loại, dòng công nghệ, (màu quầng chính, màu quầng phụ), vị trí
COVERS = [
    ("seosona-flow",     "SEOSONA Flow",       "CHROME EXTENSION",
     "JavaScript · Chrome MV3 · Side Panel", ((249, 115, 22), (252, 211, 77)), 0),
    ("seosona-video-ai", "SEOSONA Video AI",   "NHÀ MÁY SẢN XUẤT VIDEO",
     "Python · FFmpeg · Puppeteer · Whisper", ((225, 80, 40), (249, 115, 22)), 1),
    ("omniclaw",         "OmniClaw",           "HỆ ĐIỀU HÀNH AGENT",
     "Python · 8 Daemons · MCP", ((247, 92, 30), (252, 180, 77)), 2),
    ("seosona-os",       "SEOSONA OS",         "BỘ NÃO TRUNG TÂM",
     "Python · Node.js · MCP", ((240, 140, 30), (252, 211, 77)), 3),
    ("seosona-ux-ui",    "SEOSONA UX-UI",      "HỆ THỐNG THIẾT KẾ",
     "HTML · CSS Variables · Vanilla JS", ((252, 180, 60), (255, 122, 0)), 4),
    ("tiem-nuoc-nho",    "Tiệm Nước Nhỏ POS",  "ỨNG DỤNG THỰC TẾ",
     "React 19 · TypeScript · Google Sheets", ((230, 120, 50), (252, 211, 77)), 5),
    ("seosona",          "SEOSONA",            "WEBSITE",
     "Next.js · Tailwind CSS · MDX", ((249, 115, 22), (230, 90, 60)), 6),
    ("portfolio",        "Portfolio_LongLeo",  "MÃ NGUỒN MỞ",
     "HTML · CSS · Vanilla JS", ((255, 122, 0), (252, 211, 77)), 7),
]


def font(px, bold=True):
    names = ("seguibl.ttf", "segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for n in names:
        path = os.path.join(FONTDIR, n)
        if os.path.exists(path):
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def glow(img, cx, cy, radius, color, peak):
    """Một quầng sáng mềm, ghép một lần nên alpha không cộng dồn thành khối đặc."""
    s = 150
    mask = Image.new("L", (s, s), 0)
    px = mask.load()
    for y in range(s):
        for x in range(s):
            d = math.hypot(x - s / 2, y - s / 2) / (s / 2)
            px[x, y] = 0 if d >= 1 else int(peak * (1 - d) ** 2.2)
    mask = mask.resize((radius * 2, radius * 2), Image.BICUBIC).filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.new("RGB", (radius * 2, radius * 2), color), (cx - radius, cy - radius), mask)


def grid_overlay(img, spacing=48, alpha=10):
    """Lưới mảnh, gần như không thấy — chỉ để nền không bị phẳng lì."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, spacing):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, alpha))
    for y in range(0, H, spacing):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, alpha))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))


def fit(draw, text, size, bold, max_width):
    """Thu nhỏ dần cho tới khi tên vừa một dòng — tên dài không được tràn."""
    while size > 30:
        f = font(size, bold)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 3
    return font(size, bold)


def build(slug, name, kind, tech, colors, idx):
    img = Image.new("RGB", (W, H), BG)
    main, accent = colors

    # Vị trí quầng lệch dần theo chỉ số để tám tấm không trùng bố cục
    angle = idx * (2 * math.pi / len(COVERS))
    glow(img, int(140 + 60 * math.cos(angle)), int(H - 40 + 40 * math.sin(angle)), 470, main, 138)
    glow(img, int(W - 180 + 70 * math.sin(angle)), int(60 + 50 * math.cos(angle)), 390, accent, 92)

    grid_overlay(img)

    # Số thứ tự lớn, rất mờ, nằm sau chữ. Phải vẽ trên lớp riêng rồi ghép:
    # vẽ thẳng bằng fill có alpha lên ảnh RGB ra chữ đặc, không mờ.
    nf = font(340)
    num = f"{idx + 1:02d}"
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    nw = ld.textlength(num, font=nf)
    num_left = W - nw - 52
    ld.text((num_left, 92), num, font=nf, fill=(255, 255, 255, 20))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))

    d = ImageDraw.Draw(img, "RGBA")
    x = 78
    # Nhãn loại + gạch amber
    kf = font(23)
    d.text((x, 150), kind, font=kf, fill=AMBER)
    kw = d.textlength(kind, font=kf)
    d.line([(x, 190), (x + kw, 190)], fill=AMBER + (110,), width=2)

    # Tên dự án
    # Tên phải dừng trước con số — chạm vào là chữ trông như bị bẩn
    nf2 = fit(d, name, 76, True, num_left - x - 28)
    d.text((x, 232), name, font=nf2, fill=TEXT)

    # Dòng công nghệ
    d.text((x, 342), tech, font=font(25, False), fill=MUTED)

    # Chân trang
    d.text((x, H - 78), "github.com/LongLeo287", font=font(20, False), fill=(120, 114, 110))
    bf = font(20)
    bw = d.textlength("HÀ ĐÌNH LONG", font=bf)
    d.text((W - bw - 78, H - 78), "HÀ ĐÌNH LONG", font=bf, fill=(120, 114, 110))

    return img


def main():
    os.chdir(ROOT)
    out = "assets/img/labs"
    os.makedirs(out, exist_ok=True)
    for slug, name, kind, tech, colors, idx in COVERS:
        img = build(slug, name, kind, tech, colors, idx)
        img.save(f"{out}/{slug}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        for w in (480, 960):
            img.resize((w, round(H * w / W)), Image.LANCZOS).save(
                f"{out}/{slug}-{w}.webp", "WEBP", quality=84, method=5)
        print(f"  {os.path.getsize(f'{out}/{slug}-960.webp') // 1024:>3} KB  {slug}")
    print(f"\nĐã sinh {len(COVERS)} ảnh bìa.")


if __name__ == "__main__":
    raise SystemExit(main())
