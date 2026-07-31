# 🎬 Portfolio — Hà Đình Long (Long Leo)

Portfolio cá nhân của **Hà Đình Long** (Long Leo) — Video Editor & Motion Graphic Artist, hành trình sáng tạo từ **2019**.

🌐 **Live:** [https://portfolio-long-leo.vercel.app](https://portfolio-long-leo.vercel.app)

Trang tĩnh thuần HTML/CSS/JS — **không có bước build**, mở file là chạy.

---

## 👤 Thông tin

| | |
|---|---|
| **Họ tên** | Hà Đình Long (Long Leo) |
| **Vai trò** | Video Editor · Motion Graphic · UI/UX Designer |
| **Kinh nghiệm** | 5+ năm (từ 2019) |
| **Email** | Longdragon287@gmail.com |
| **SĐT** | 0906 964 451 |
| **Khu vực** | Tân Phú, Hồ Chí Minh |
| **YouTube** | [@LongLeo287](https://www.youtube.com/@LongLeo287) |
| **Facebook** | [LongLeo97](https://www.facebook.com/LongLeo97) |

---

## 🗂️ Cấu trúc dự án

```text
Portfolio_LongLeo/
├── index.html                    # Trang chính
├── cv.html                       # CV (mở trong modal iframe, và là 1 URL riêng)
├── robots.txt · sitemap.xml
│
├── assets/
│   ├── css/
│   │   ├── tokens.css            # ⭐ Design tokens — load ĐẦU TIÊN
│   │   ├── styles.css            # Layout, component, responsive, light theme
│   │   ├── animations.css        # Keyframes, scroll reveal, hover
│   │   └── cv.css                # Riêng cho cv.html
│   │
│   ├── js/
│   │   ├── app.js                # Dữ liệu portfolio, i18n, modal, slider
│   │   ├── main.js               # Smooth scroll, theme, menu, form, scroll UI
│   │   ├── animations.js         # Reveal, spotlight, counter, typing
│   │   └── vendor/lenis-*.min.js # Self-host, đã pin version
│   │
│   ├── data/projects.json        # ⭐ NGUỒN DỮ LIỆU DUY NHẤT của portfolio
│   │
│   └── img/
│       ├── longleo_avatar*.webp  # Avatar + bản responsive
│       ├── og-cover.jpg          # Ảnh share mạng xã hội 1200×630
│       ├── logos/                # Logo đối tác
│       ├── tools/                # Icon phần mềm (self-host, không hotlink)
│       ├── thumbnails/ design/ photography/
│       └── **/*-480.webp, *-960.webp   # Bản responsive (sinh tự động)
│
├── scripts/
│   └── generate-image-sizes.py   # Sinh bản ảnh 480w/960w
│
└── .github/workflows/static.yml  # GitHub Pages auto-deploy
```

---

## ➕ Thêm một sản phẩm mới

Chỉ sửa **`assets/data/projects.json`** — không còn file dữ liệu nào khác.

```json
{
  "id": "proj_123",
  "category": "Video",
  "title": { "vi": "Tiêu đề tiếng Việt", "en": "English title" },
  "client": { "vi": "Tên khách hàng", "en": "Client name" },
  "imgSrc": "assets/img/thumbnails/VIDEO_ID.jpg",
  "href": "https://youtu.be/VIDEO_ID",
  "isFeatured": true,
  "caseStudy": {
    "role":      { "vi": "…", "en": "…" },
    "concept":   { "vi": "…", "en": "…" },
    "challenge": { "vi": "…", "en": "…" },
    "solution":  { "vi": "…", "en": "…" },
    "tools": ["Premiere Pro", "After Effects"]
  }
}
```

- `category`: `"Video"` · `"Design"` · `"Photography"` · `"Thumbnail"`
- `isFeatured: true` → hiện ở tab **Nổi bật** (tối đa 9 thẻ, xáo trộn ngẫu nhiên)
- Thẻ `Photography` cố ý chỉ hiện ảnh, không hiện tiêu đề
- Không có `caseStudy` → modal tự ẩn panel thông tin, thành lightbox thuần

**Sau khi thêm ảnh mới, bắt buộc chạy:**

```bash
python scripts/generate-image-sizes.py
```

Script sinh `-480.webp` và `-960.webp` cạnh mỗi ảnh. `app.js` dựng `srcset` từ đúng hai hậu tố này, nên **thiếu file là ảnh vỡ** — đừng bỏ qua bước này.

---

## 🎨 Design system

Tất cả token nằm ở **`assets/css/tokens.css`** và phải load trước `styles.css`.

**Màu thương hiệu** (`styles.css` `:root`)
`--primary #ff7a00` · `--amber #fcd34d` · `--orange #f97316` · `--cream #ffd9b5` · `--brown #7a4c25`
Dark (mặc định): `--bg-main #0c0a09` · `--bg-surface #1c1917` · `--bg-card #262220`

**Typography** — `Space Grotesk` (heading) + `Archivo` (body), tải dạng variable axis `wght@300..700` (2 file font thay vì 10).
Thang chữ fluid `--text-xs … --text-hero` bằng `clamp()`.

**Motion** — theo MOTION-SPEC:

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--dur-instant` | 100ms | Phản hồi nhấn/hover |
| `--dur-fast` | 180ms | Micro-interaction |
| `--dur-base` | 280ms | Chuyển cảnh chuẩn, card |
| `--dur-slow` | 420ms | Reveal lớn, section |
| `--dur-deliberate` | 640ms | Khoảnh khắc hero |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | **Mặc định** |

Ngân sách tiết chế: tối đa 3 phần tử vào cùng lúc, stagger 40–80ms, tối đa 1 animation lặp vô hạn trên màn hình.

`prefers-reduced-motion: reduce` được tôn trọng ở **cả CSS lẫn JS** — smooth scroll, spotlight, tilt, magnetic, typing, marquee và counter đều tự tắt.

---

## ♿ Accessibility

- Skip link; focus trap + Escape + trả focus cho cả 3 modal
- `aria-pressed` cho nút lọc & chuyển ngôn ngữ, `aria-expanded` cho menu mobile
- Label thật cho mọi field trong form liên hệ, `aria-live` cho thông báo gửi
- Vùng chạm tối thiểu 44×44px
- `html lang` đổi theo ngôn ngữ đang chọn

---

## 🌐 Song ngữ

Chuỗi tĩnh nằm trong object `translations` ở `assets/js/app.js`; nội dung dự án nằm trong `projects.json` dưới dạng `{ vi, en }`.

Thứ tự ưu tiên chọn ngôn ngữ: `?lang=` trên URL → `localStorage` → `vi`.
Nghĩa là `https://portfolio-long-leo.vercel.app/?lang=en` là một link chia sẻ được, và đã khai báo `hreflang`.

---

## 🚀 Chạy local

```bash
python -m http.server 8000
```

Mở `http://localhost:8000`. Phải chạy qua HTTP server — `projects.json` được nạp bằng `fetch`, mở trực tiếp bằng `file://` sẽ bị chặn.

---

## 🧹 Dọn dẹp repo (chưa làm — cần bạn quyết định)

Repo đang nặng ~272 MB. Trong đó **~108 MB là file nguồn website không dùng tới**: bản `.jpg`/`.png` gốc chưa nén nằm cạnh bản `.webp` đang dùng, cộng một file `.psb` nặng 16 MB.

Toàn bộ file vẫn còn nguyên trên máy. Để website ngừng deploy chúng và repo nhẹ lại:

1. **Sao lưu `assets/img/design/` ra nơi khác trước** (Drive, ổ ngoài). Đây là file gốc thiết kế, mất là không tạo lại được.
2. Bỏ theo dõi git:
   ```bash
   git rm -r --cached assets/img/design/PROJECTS/PSD
   ```
3. Muốn xoá hẳn khỏi lịch sử git (mới thực sự giảm dung lượng clone) thì cần `git filter-repo`. Thao tác này viết lại lịch sử — chỉ làm khi đã chắc chắn và đã backup.

---

## 📦 Deploy

- **Vercel** (đang dùng): auto-deploy khi push lên `main`
- **GitHub Pages**: `.github/workflows/static.yml`

⚠️ Site đang deploy song song ở cả hai nơi nhưng `canonical` / `og:url` / `sitemap.xml` đều trỏ về domain Vercel. Nếu chỉ dùng một nơi, hãy tắt cái còn lại để tránh nội dung trùng lặp.

---

## 📄 License

© 2026 Hà Đình Long. All rights reserved.
Icon phần mềm trong `assets/img/tools/` là thương hiệu của các hãng tương ứng, dùng để minh hoạ công cụ sử dụng.
