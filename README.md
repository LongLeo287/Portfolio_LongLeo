# 🎬 Portfolio — Hà Đình Long (Long Leo)

Portfolio cá nhân của **Hà Đình Long** (Long Leo) — Video Editor & Motion Graphic Artist với 7+ năm kinh nghiệm trong sản xuất video, thiết kế đồ họa, motion graphic và UI/UX.

🌐 **Live:** [https://portfolio-long-leo.vercel.app](https://portfolio-long-leo.vercel.app)

---

## 👤 Thông tin cá nhân

| | |
|---|---|
| **Họ tên** | Hà Đình Long (Long Leo) |
| **Vai trò** | Video Editor · Motion Graphic · UI/UX Designer |
| **Kinh nghiệm** | 7+ năm (2015 – nay) |
| **Email** | Longdragon287@gmail.com |
| **SĐT** | 0906 964 451 |
| **Khu vực** | Tân Phú, Hồ Chí Minh |
| **YouTube** | [@LongLeo287](https://www.youtube.com/@LongLeo287) |
| **Facebook** | [LongLeo97](https://www.facebook.com/LongLeo97) |

---

## ✨ Tính năng

- **Hero section** — Animated background orbs, typing effect, counter animation
- **Partners marquee** — Logo cuộn tự động (Vua2Hand, MyGear, Vie, TopSkills, Thế Giới In Ấn)
- **Về mình** — Avatar, bio, skill cards, công cụ & AI stack
- **Dịch vụ** — 6 dịch vụ với hover 3D tilt effect
- **Kinh nghiệm** — 5 công ty với card có logo, vai trò, mô tả
- **Portfolio** — Showcase slider + bộ lọc theo danh mục (Video, Thiết kế, Chụp ảnh) + lightbox
- **Liên hệ** — Form mailto + thông tin liên hệ + mạng xã hội
- **Animation Engine** — Scroll reveal, cursor spotlight, magnetic buttons, parallax thumbnail
- **Responsive** — Tối ưu cho desktop, tablet và điện thoại
- **Custom scrollbar** — Đồng bộ phong cách thương hiệu

---

## 🗂️ Cấu trúc dự án

```text
Portfolio_LongLeo/
├── index.html                    # Trang chính
├── Portfolio Demo.html           # File demo tham chiếu
├── README.md
│
├── assets/
│   ├── css/
│   │   ├── styles.css            # Design system, layout, responsive
│   │   └── animations.css        # Keyframes, scroll reveals, hover effects
│   │
│   ├── js/
│   │   ├── main.js               # Portfolio filter, lightbox, form, scroll UI
│   │   └── animations.js         # Animation engine: reveal, tilt, counter, typing
│   │
│   └── img/
│       ├── longleo_avatar.jpg    # Ảnh đại diện
│       ├── logos/                # Logo đối tác & công ty
│       │   ├── mygear.png
│       │   ├── vua2hand.png
│       │   ├── vie.png
│       │   ├── topskills.png
│       │   └── thegioiinan.png
│       ├── thumbnails/           # Thumbnail YouTube (54 ảnh)
│       ├── design/               # Ảnh thiết kế đồ họa
│       └── photography/          # Ảnh chụp sản phẩm
│
└── .github/
    └── workflows/
        └── static.yml            # GitHub Pages auto-deploy
```

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|---|---|
| **HTML5 semantic** | Cấu trúc trang, SEO |
| **CSS3 Vanilla** | Design system, animations, responsive |
| **JavaScript ES6+** | Portfolio filter, lightbox, animation engine |
| **Intersection Observer API** | Scroll-triggered reveals |
| **CSS Custom Properties** | Design tokens (màu sắc, spacing) |
| **CSS Grid & Flexbox** | Layout responsive |

---

## 🎨 Design System

**Màu sắc thương hiệu:**
- `--bg-dark` `#0c0a09` — Nền tối (Hero, Experience, Footer)
- `--amber` `#fcd34d` — Màu nhấn chính
- `--orange` `#f97316` — Màu nhấn phụ
- `--cream` `#ffd9b5` — Nền Contact section
- `--brown` `#7a4c25` — Text màu đất

**Typography:** `Inter` (Google Fonts) — font-weight từ 400 đến 950

---

## 🔌 Công cụ & AI tích hợp trong portfolio

**Phần mềm sáng tạo:**
Adobe Premiere Pro · After Effects · Photoshop · Illustrator · Lightroom · Figma · CapCut · Canva

**Trợ lý AI:**
Google Gemini · Google AI Studio · Google Antigravity · Claude Code · Codex

---

## ⚡ Animation Engine (`animations.js`)

| Feature | Mô tả |
|---|---|
| **Scroll Reveal** | Fade-up + stagger delay khi cuộn đến |
| **Cursor Spotlight** | Vầng sáng bám theo con trỏ (desktop only) |
| **Counter Animation** | Số liệu đếm lên khi hiện ra |
| **Typing Effect** | Text pill gõ từng ký tự |
| **Magnetic Buttons** | CTA bị hút nhẹ theo chuột |
| **3D Card Tilt** | Service/Portfolio card nghiêng 3D khi hover |
| **Parallax Thumbnail** | Ảnh portfolio trượt theo chuột |
| **Tool Shimmer** | Ánh sáng chạy qua khi hover tool item |

---

## 🚀 Chạy local

```bash
# Cách 1 — Python
python3 -m http.server 8000

# Cách 2 — Node.js
npx serve .

# Cách 3 — VS Code
# Dùng extension Live Server, click "Go Live"
```

Truy cập: `http://localhost:8000`

---

## 📦 Deploy

### Vercel (đang dùng)
```bash
# Auto-deploy khi push lên main
git push origin main
```

### GitHub Pages
> Settings → Pages → Source: `Deploy from a branch` → Branch: `main` / `/ (root)`

Workflow tự động tại `.github/workflows/static.yml`

---

## 📁 Quản lý ảnh portfolio

Thumbnail YouTube được đặt tại `assets/img/thumbnails/` với tên file là **YouTube Video ID** (ví dụ: `FFs4bqjNmjU.jpg`).

Để thêm video mới vào portfolio, thêm entry vào array `portfolioItems` trong `assets/js/main.js`:

```js
{
  id: "VIDEO_ID",
  title: "Tiêu đề video",
  category: "Video",   // "Video" | "Design" | "Photography"
  client: "Tên khách hàng",
  featured: true,      // Hiển thị ở tab "Nổi bật"
  link: "https://youtu.be/VIDEO_ID"
}
```

---

## 📄 License

© 2025 Hà Đình Long. All rights reserved.
