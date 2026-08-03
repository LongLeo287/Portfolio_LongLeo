<div align="center">

# 🎬 Hà Đình Long — Video Editor Portfolio

**Quay dựng · Motion Graphic · Thiết kế đồ họa · UI/UX**
Hành trình sáng tạo từ 2019 · Tân Phú, TP. Hồ Chí Minh

[**Xem live →**](https://portfolio-long-leo.vercel.app) · [Xem CV](https://portfolio-long-leo.vercel.app/cv.html) · [English](https://portfolio-long-leo.vercel.app/?lang=en)

[![YouTube](https://img.shields.io/badge/YouTube-@LongLeo287-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@LongLeo287)
[![Facebook](https://img.shields.io/badge/Facebook-LongLeo97-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/LongLeo97)
[![Email](https://img.shields.io/badge/Email-Longdragon287-EA4335?logo=gmail&logoColor=white)](mailto:Longdragon287@gmail.com)

</div>

---

Trang tĩnh thuần **HTML / CSS / JavaScript**. Không framework, không bundler, **không có bước build** — clone về mở server tĩnh là chạy.

| | |
|---|---|
| Dự án trong portfolio | **174** (55 video · 59 thiết kế · 35 thumbnail · 25 ảnh chụp) |
| Dung lượng tải lần đầu | **~226 KB** · 20 request |
| Phụ thuộc bên thứ ba | 2 — Google Fonts, thumbnail YouTube |
| Thư viện JS | 1 — [Lenis](https://github.com/darkroomengineering/lenis) 1.1.13, self-host |
| Ngôn ngữ | Tiếng Việt (mặc định) + English |

---

## Mục lục

- [Chạy trên máy](#-chạy-trên-máy)
- [Cấu trúc dự án](#️-cấu-trúc-dự-án)
- [Thêm sản phẩm mới](#-thêm-sản-phẩm-mới)
- [Labs — dự án mã nguồn mở](#-labs--dự-án-mã-nguồn-mở)
- [Design system](#-design-system)
- [Motion](#-motion)
- [Accessibility](#-accessibility)
- [Song ngữ](#-song-ngữ)
- [SEO](#-seo)
- [Deploy](#-deploy)
- [Việc còn tồn đọng](#-việc-còn-tồn-đọng)

---

## 🚀 Chạy trên máy

```bash
python -m http.server 8000
```

Mở `http://localhost:8000`.

> ⚠️ **Bắt buộc chạy qua HTTP server.** Danh sách dự án được nạp bằng `fetch()` từ `projects.json`; mở trực tiếp bằng `file://` sẽ bị CORS chặn và lưới portfolio sẽ trống.

---

## 🗂️ Cấu trúc dự án

```text
Portfolio_LongLeo/
├── index.html                     50 KB  Trang chính
├── cv.html                        29 KB  CV — vừa là URL riêng, vừa mở trong modal
│
├── labs/                                 Landing page cho từng dự án mã nguồn mở
│   ├── seosona-flow.html                 Chrome extension tạo ảnh/video AI
│   ├── seosona-video-ai.html             Nhà máy sản xuất video tự động
│   ├── omniclaw.html                     Hệ điều hành 8 daemon
│   ├── seosona-os.html                   Bộ não trung tâm
│   ├── seosona-ux-ui.html                Hệ thống thiết kế
│   ├── tiem-nuoc-nho.html                Ứng dụng POS
│   ├── seosona.html                      Website (có bản live)
│   └── portfolio.html                    Chính trang này
├── robots.txt · sitemap.xml              SEO
│
├── assets/
│   ├── css/
│   │   ├── tokens.css              4 KB  ⭐ Design token — PHẢI load trước styles.css
│   │   ├── styles.css             84 KB  Layout, component, responsive, light theme
│   │   ├── animations.css         18 KB  Keyframe, scroll reveal, scroll-driven motion
│   │   ├── labs.css                6 KB  Riêng cho các trang trong labs/
│   │   └── cv.css                  5 KB  Riêng cho cv.html
│   │
│   ├── js/
│   │   ├── app.js                 55 KB  Dữ liệu portfolio, i18n, modal, slider, bộ lọc
│   │   ├── main.js                11 KB  Smooth scroll, theme, menu, form, scroll UI
│   │   ├── animations.js          15 KB  Reveal, spotlight, counter, typing, rail
│   │   └── vendor/
│   │       └── lenis-1.1.13.min.js       Self-host, đã pin version
│   │
│   ├── data/
│   │   └── projects.json         288 KB  ⭐ NGUỒN DỮ LIỆU DUY NHẤT
│   │
│   └── img/                              604 file
│       ├── longleo_avatar*.webp          Avatar + bản responsive
│       ├── og-cover.jpg                  Ảnh share mạng xã hội 1200×630
│       ├── labs/                         Ảnh bìa dự án — tự sinh, xem scripts/
│       ├── logos/                        Logo đối tác
│       ├── tools/                        Icon phần mềm — self-host, không hotlink
│       ├── thumbnails/ design/ photography/
│       └── **/*-480.webp · *-960.webp    Bản responsive (sinh tự động)
│
└── scripts/
    ├── generate-image-sizes.py           Sinh bản ảnh 480w / 960w
    ├── sync-youtube.py                   Thêm video mới từ kênh YouTube
    ├── build-labs.py                     Sinh các trang trong labs/
    ├── build-lab-covers.py               Sinh ảnh bìa cho các trang labs/
    ├── build-repo-landing.py             Sinh landing page tự chứa cho từng repo
    ├── landing-seosona-flow.py           Trang viết riêng cho SEOSONA Flow
    ├── landing-seosona-flow-assets.py    Ảnh thư viện cho trang đó
    ├── landing-tiem-nuoc-nho.py          Trang viết riêng cho Tiệm Nước Nhỏ POS
    ├── landing-seosona-video-ai.py       Trang dải film
    ├── landing-seosona-os.py             Trang hướng tâm
    ├── landing-seosona-ux-ui.py          Trang nền sáng có công tắc
    ├── landing-omniclaw.py               Trang terminal (tạm ngắt)
    ├── check-contrast.py                 Kiểm tương phản WCAG AA
    ├── check-pages.py                    Kiểm cấu trúc, tiếp cận, animation
    └── push-repo-landing.py              Đẩy chúng vào repo qua GitHub API
```

---

## ➕ Thêm sản phẩm mới

Chỉ sửa **`assets/data/projects.json`**. Không còn file dữ liệu nào khác.

```json
{
  "id": "proj_174",
  "category": "Video",
  "title":  { "vi": "Tiêu đề tiếng Việt", "en": "English title" },
  "client": { "vi": "Tên khách hàng",     "en": "Client name" },
  "imgSrc": "assets/img/thumbnails/VIDEO_ID.jpg",
  "href":   "https://youtu.be/VIDEO_ID",
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

| Trường | Ghi chú |
|---|---|
| `category` | `Video` · `Design` · `Photography` · `Thumbnail` |
| `isFeatured` | `true` → hiện ở tab **Nổi bật** (tối đa 9 thẻ, xáo trộn mỗi lần tải) |
| `href` | Có `youtube.com` → thẻ hiện nút play và mở trình phát trong modal |
| `caseStudy` | Thiếu `role` và `concept` → modal tự ẩn panel chữ, thành lightbox ảnh thuần |
| Thẻ `Photography` | Cố ý chỉ hiện ảnh, không hiện tiêu đề — để phần này đọc như một gallery |

### ⚠️ Sau khi thêm ảnh, bắt buộc chạy

```bash
python scripts/generate-image-sizes.py
```

`app.js` dựng `srcset` bằng cách nối hậu tố `-480.webp` / `-960.webp` vào tên file gốc. **Không chạy script = ảnh vỡ.** Script cố ý mã hoá lại cả những ảnh nhỏ hơn kích thước đích ở đúng chiều rộng gốc, để mọi ứng viên trong `srcset` luôn tồn tại.

Yêu cầu: `pip install Pillow`

### 🎬 Video YouTube — thêm tự động

Portfolio **không tự cập nhật** khi có video mới trên kênh: `projects.json` là
file tĩnh. Script này làm hộ toàn bộ phần việc tay.

```bash
python scripts/sync-youtube.py                      # xem kênh có gì mới
python scripts/sync-youtube.py --url <link> --add   # thêm đúng một video
python scripts/sync-youtube.py --add                # thêm tất cả video mới
```

Nó đọc RSS công khai của kênh (**không cần API key, không cần đăng nhập**),
tải thumbnail chất lượng cao nhất còn tồn tại, sinh bản `-480`/`-960`, thêm mục
vào `projects.json`, và bump `?v=` của `projects.json` trong `app.js` — bước
cuối rất dễ quên, và quên là trình duyệt vẫn dùng bản JSON cũ trong cache.

> Mặc định **chỉ liệt kê**, phải thêm `--add` mới ghi. Vì không phải video nào
> lên kênh cũng thuộc portfolio — tuyển tập nhạc, vlog, video reup sẽ lọt vào
> hết nếu đồng bộ mù.

Sau khi thêm: tiêu đề tiếng Anh để tạm bằng tiêu đề gốc, sửa lại nếu muốn.
`isFeatured` mặc định `false` để video mới không chiếm chỗ tab Nổi bật.

---

## 🧪 Labs — dự án mã nguồn mở

Section `#labs` trên trang chủ liệt kê các dự án tự phát triển. Bấm vào một thẻ
sẽ **mở tab mới** dẫn tới landing page riêng của dự án đó.

Landing page nằm ở **hai nơi khác nhau**, và đây là chỗ dễ nhầm nhất:

| Kiểu | Trang nằm ở đâu | Sinh bằng | Dùng cho |
|---|---|---|---|
| Trong repo dự án | `landing/index.html` của chính repo đó, Vercel riêng | `build-repo-landing.py` | Dự án có repo công khai riêng |
| Trong portfolio | `labs/<slug>.html` ngay repo này | `build-labs.py` | Dự án chưa deploy được |

Nội dung của **cả hai** đều lấy từ đúng một hằng `LABS` trong `build-labs.py`,
nên sửa mô tả một chỗ là cả hai đổi theo. `IN_PORTFOLIO` quyết định slug nào
còn sinh ra file trong `labs/`.

### Trang viết riêng

Mẫu chung đủ cho một repo hạ tầng, nhưng dự án có người dùng thật thì cần trang
*cho xem* sản phẩm chứ không chỉ tả bằng chữ. Những dự án đó khai trong hằng
`CUSTOM` của `build-repo-landing.py`, trỏ tới script sinh riêng của nó:

| Dự án | Script | Có gì thêm |
|---|---|---|
| SEOSONA Flow | `landing-seosona-flow.py` + `landing-seosona-flow-assets.py` | 10 khối: mockup side panel, sơ đồ workflow SVG, Image-to-Prompt, thư viện 12 ảnh thật, kho prompt, 26 node theo 5 nhóm, 9 tính năng, giới hạn, FAQ |
| Tiệm Nước Nhỏ POS | `landing-tiem-nuoc-nho.py` | 9 khối: mockup điện thoại và quầy thu ngân đặt cạnh nhau, thẻ QR VietQR, sơ đồ đồng bộ offline-first, 9 tính năng, giới hạn, FAQ |
| SEOSONA Video AI | `landing-seosona-video-ai.py` | **Mô-típ dải film.** Cuộn phim 16:9 trôi ngang có lỗ răng cưa, bốn lớp kiến trúc vẽ thành track chồng lấn trên trục thời gian có đầu đọc chạy, mười đặc vụ đánh số như cảnh quay. Phông Be Vietnam Pro |
| SEOSONA OS | `landing-seosona-os.py` | **Bố cục hướng tâm.** Toàn trang căn giữa, quỹ đạo xoay quanh lõi, ba tầng trí nhớ là ba vòng thu dần, năm năng lực xếp dọc một trục lệch trái phải. Phông Lexend |
| SEOSONA UX-UI | `landing-seosona-ux-ui.py` | **Nền sáng + công tắc sáng/tối.** Trang duy nhất trong bộ tám để nền sáng. Bố cục kiểu tài liệu có sidebar dính, component dựng thật bằng chính token. Phông Manrope |
| OmniClaw | `landing-omniclaw.py` | **Hình thức terminal.** Chuỗi khởi động tám daemon gõ dần, mỗi mục là một dòng nhắc `$`, bảng daemon thay cho lưới thẻ, cảnh báo thay cho mục giới hạn. Phông IBM Plex Mono |

**Sáu trang, sáu hình thức, sáu phông chữ.** Không trang nào dùng chung khung với
trang nào — hình thức do bản chất sản phẩm quyết định, không phải do màu nhấn.

> **Vì sao bỏ bộ sinh dùng chung.** Bản đầu tôi gộp bốn dự án hạ tầng vào một
> script `landing-rich.py`, mỗi cái chỉ khác màu nhấn, hình đặc trưng và chữ. Đo
> bằng chỉ số Jaccard trên tập lớp CSS thì **bốn trang giống nhau 83,3%**, và thứ
> tự khối trùng nhau từng mục một. Sau khi tách thành bốn script riêng, mức giống
> nhau cao nhất trong cả sáu trang còn **29,5%**.
>
> Kịch bản đo nằm ở `scratchpad`, chạy lại được bất cứ lúc nào để kiểm tra xem
> các trang có bị trôi về giống nhau sau này không.

> **UX-UI cố ý không theo chế độ sáng/tối của hệ điều hành.** Bảy trang anh em
> đều nền tối; trang này mở ra sáng là một tuyên bố — một hệ design token tự
> chứng minh nó chạy được cả hai chế độ. Nếu theo hệ điều hành thì phần lớn người
> xem (đang để chế độ tối) sẽ thấy nó giống hệt các trang kia, mất luôn điểm khác
> biệt. Ai đã bấm công tắc thì lựa chọn của họ được nhớ lại.

> **Hình đặc trưng chỉ hiện một lần.** Bản đầu tôi để nó ở cả hero lẫn mục kiến
> trúc — tám daemon thành mười sáu, và lần thứ hai chẳng nói thêm được gì. Giờ
> hero là thẻ thông số gọn, hình lớn để dành cho mục kiến trúc nơi có đủ chỗ và
> có đoạn giải thích đi kèm.

> **Số liệu đọc từ cây thư mục, không lấy từ README.** README hay nói quá. Chỗ nào
> README và mã nguồn lệch nhau thì tin mã nguồn — trừ khi có tài liệu kiến trúc nói
> rõ, như tám daemon của OmniClaw (chỉ ba cái đã hiện thực bằng Python, năm cái còn
> lại là node agent; `core/docs/architecture/CORE_DAEMONS_AND_OER.md` định nghĩa đủ
> tám). Điểm lệch đó được ghi thẳng vào mục giới hạn của trang.

> **Trang giới thiệu nên trông giống thứ nó giới thiệu.** Trang Tiệm Nước Nhỏ
> dùng phông `Plus Jakarta Sans` và đỏ `#C9252C` — đo trực tiếp từ ứng dụng đang
> chạy ở `/app/` chứ không phải đoán. Nền tối vẫn giữ theo nhà chung, nhưng màu
> nhấn theo sản phẩm, nên mockup trên trang khớp với bản thật khi người ta mở lên.
>
> Mã QR trên trang là **hoạ tiết minh hoạ, không quét được** — sinh bằng bộ số
> tuyến tính có seed cố định. Nhúng một mã VietQR thật trỏ vào tài khoản ngân hàng
> nào đó lên trang công khai mới là chuyện sai.

Ba loại hình ảnh trên trang đó, mỗi loại một lý do:

1. **Mockup vẽ bằng HTML/CSS/SVG** — side panel, sơ đồ workflow, Image-to-Prompt.
   Ảnh chụp màn hình sẽ lệch với bản thật ngay lần cập nhật extension đầu tiên;
   mockup sửa được như sửa văn bản và không tốn byte tải về.
2. **Ảnh thật do chính extension sinh ra** — `landing-seosona-flow-assets.py` kéo
   12 tấm từ `assets/templates/` của repo seosona-flow, đổi sang WebP hai cỡ.
   Ảnh gốc **không** chép vào repo này (88 tấm, gần 9 MB).
3. **Icon và logo vẽ bằng SVG nội tuyến** — không gọi thư viện icon nào.

> **Chọn ảnh phải xem từng tấm.** Trong 88 mẫu có tấm chứa chân dung người nổi
> tiếng và logo thương hiệu (ảnh ghép pop-culture, biển quảng cáo trong sân bóng).
> Ảnh do AI sinh nhưng vẫn là nhãn hiệu và hình ảnh của người khác — đã cố ý loại
> khỏi danh sách `PICKS`.

Bố cục học từ `labs.toby.vn` — sản phẩm cùng loại, trang bán hàng của họ làm tốt.
Giao diện thì giữ nhận diện tối/amber của SEOSONA.

**Mockup vẽ bằng HTML/CSS, không phải ảnh chụp màn hình.** Ảnh chụp sẽ lệch với
bản thật ngay lần cập nhật đầu tiên, còn mockup thì sửa được như sửa văn bản và
không tốn thêm byte tải về.

Khi thêm một slug vào `CUSTOM`, bộ chung sẽ **bỏ qua `index.html`** của repo đó
*và* không dọn thư mục của nó nữa — không có vế thứ hai thì bước dọn đầu mỗi lần
chạy sẽ xoá mất trang riêng.

### Kiểm trước khi đẩy

```bash
python scripts/check-contrast.py   # tương phản WCAG AA
python scripts/check-pages.py      # cấu trúc, tiếp cận, animation
```

`check-pages.py` bắt: thứ bậc tiêu đề nhảy cóc, id trùng, neo chết, `_blank`
thiếu `rel=noopener`, ảnh thiếu `alt`/`width`/`height`, meta quá dài, thiếu
`:focus-visible`, và **animation động tới layout hoặc paint**.

> Đợt kiểm 08/08/2026 bắt được 6 lỗi mà mắt không thấy: `id="lg"` trùng vì logo
> SVG chèn hai chỗ mà cùng khai một gradient (trình duyệt chỉ nhận cái đầu),
> `@keyframes scrub` động tới `left`, `@keyframes scan` động tới `top`,
> `@keyframes pulse` động tới `box-shadow` — ba cái sau buộc trình duyệt tính
> lại bố cục hoặc vẽ lại mỗi khung hình. Đã đổi hết sang `transform`.
>
> Mẹo cho vạch chạy ngang: đừng animate `left`. Cho phần tử rộng bằng cả khung
> rồi vẽ vạch ở mép trái, lúc đó `translateX(100%)` đi đúng một khung.

Đọc thẳng biến CSS trong file đã sinh rồi tính tỉ lệ tương phản theo WCAG AA.
**Cố ý không đo qua trình duyệt:** khung xem trước không dựng khung hình nên
`getComputedStyle` trả giá trị cũ sau khi đổi thuộc tính theme, cho ra số vô lý
(`#475569` trên `#f8fafc` ra 2.48:1). Đọc file thì kết quả tất định.

> Đợt kiểm 03/08/2026 tìm ra **12 cặp không đạt trên 4 trang, rồi thêm 6 cặp
> trên Flow và Tiệm Nước Nhỏ** — tất cả đều là biến `--dim`, đúng loại chữ nhỏ
> nhất trên trang. Màu thay thế tính bằng dò nhị phân **chỉ đổi độ sáng trong
> HSL**, giữ nguyên sắc độ nên không phá nhận diện từng trang. Chạy lại script
> trước mỗi lần đẩy.

### Dựng lại và đẩy lên

```bash
python scripts/build-labs.py            # trang nằm trong portfolio
python scripts/build-repo-landing.py    # trang theo mẫu chung
python scripts/landing-seosona-flow-assets.py  # ảnh thư viện, chạy trước
python scripts/landing-seosona-flow.py        # rồi tới trang
python scripts/landing-tiem-nuoc-nho.py       # trang viết riêng thứ hai
python scripts/landing-seosona-video-ai.py    # dải film
python scripts/landing-seosona-os.py          # hướng tâm
python scripts/landing-seosona-ux-ui.py       # nền sáng
python scripts/landing-omniclaw.py            # terminal — TẠM NGẮT, xem TARGETS
python scripts/push-repo-landing.py     # xem trước sẽ ghi gì
python scripts/push-repo-landing.py --push

# Nội dung đã đúng nhưng bản đang phục vụ vẫn cũ (deployment trước hỏng):
python scripts/push-repo-landing.py --rebuild SEOSONA-UX-UI --push
```

> **Deployment hỏng thì đẩy thêm nội dung không cứu được.** Nếu file trong repo
> đã đúng mà trang vẫn phục vụ bản cũ thì `--push` sẽ báo *"không có gì đổi"* và
> không làm gì cả — vì đúng là không có gì để đổi. Thứ còn thiếu là một commit
> mới để Vercel chạy lại. `--rebuild` tạo một commit rỗng dùng lại đúng cây của
> HEAD, không đổi một byte nào.

`push-repo-landing.py` ghi qua GitHub API nên **không phải clone** — mấy repo
kia nặng cả trăm MB, clone chỉ để thêm vài file là phí. Nó so nội dung trước
khi ghi, chạy lại nhiều lần không tạo commit rác.

> **Mỗi repo chỉ được tạo ĐÚNG MỘT COMMIT mỗi lần đẩy.** Bản đầu dùng Contents
> API, mà API đó chỉ ghi được một file mỗi lần và **mỗi lần là một commit** —
> mỗi commit lại kích hoạt một deployment Vercel. Đẩy 5 file vào 6 repo = 30
> deployment cho một lần chạy. Gói Hobby giới hạn **100 deployment mỗi ngày**,
> nên vài vòng là Vercel khoá 24 giờ với thông báo *"Deployment rate limited"*.
> Chuyện này đã xảy ra thật ngày 03/08/2026.
>
> Bản hiện tại dùng Git Data API: tạo blob cho từng file, gộp vào một tree, tạo
> một commit, rồi cập nhật ref. Bao nhiêu file cũng chỉ một commit và một
> deployment. Đừng đổi ngược lại vì thấy Contents API viết ngắn hơn.

Thêm một dự án mới:

1. Thêm một mục vào `LABS` — thêm khoá `"live"` nếu dự án đã có website chạy
2. Thêm một mục cùng slug vào `COVERS` trong `scripts/build-lab-covers.py`
   rồi chạy `python scripts/build-lab-covers.py` để sinh ảnh bìa
3. Thêm vào `TARGETS` trong `build-repo-landing.py` nếu dự án có repo riêng,
   hoặc vào `IN_PORTFOLIO` trong `build-labs.py` nếu chưa
4. Thêm một thẻ vào section `#labs` trong `index.html`
5. Thêm URL vào `sitemap.xml` — **chỉ khi** trang nằm trong repo này

> **Tên miền `.vercel.app` là duy nhất toàn cầu, không phải theo tài khoản.**
> `omniclaw.vercel.app` và `omni-claw.vercel.app` đều đã bị người lạ chiếm, nên
> project đó phải đổi sang tên khác. URL được nhúng thẳng vào thẻ `canonical`
> và `og:image` của trang, nên đặt sai tên project là hỏng cả hai — kiểm tra tên
> còn trống trước khi thêm vào `TARGETS`.

> **Vercel giới hạn 15.000 file nguồn mỗi deployment.** OmniClaw có **14.879** file
> — 99,2% hạn mức — và build hỏng trong vòng một giây, tức là hỏng trước cả bước
> build. `vercel.json` và `.vercelignore` đều vô tác dụng vì lỗi xảy ra sớm hơn
> lúc chúng được đọc. Repo lớn thứ nhì trong nhóm là SEOSONA-OS với 8.763 file,
> chạy bình thường.
>
> Cách sửa: đặt **Root Directory = `landing`** trong Settings của project. Vercel
> khi đó chỉ thấy vài file thay vì gần mười lăm nghìn, và đọc `landing/vercel.json`
> chứ không phải file ở gốc — nên `OVERSIZED` trong `build-repo-landing.py` sinh
> thêm một bản cấu hình đặt ngay trong `landing/`.

> **`.vercelignore` không ngăn Vercel đọc cả repo.** Repo nối qua Git thì Vercel
> vẫn clone toàn bộ vào container build — kể cả repo 108 MB — rồi mới lọc và lấy
> `landing/` ra phát hành. File này chỉ thu gọn bản phát hành, không thu gọn thứ
> Vercel phải kéo về. Muốn tránh hẳn thì phải tách landing page sang repo riêng,
> đổi lại trang không còn nằm trong repo của chính dự án.
>
> Repo nào có ứng dụng thật (`APP_AT_SUBPATH`) thì **không** lọc, vì build cần
> `src/` và `package.json`.
>
> Và dung lượng repo không phải nguyên nhân build hỏng: SEOSONA-Video-AI nặng
> 108 MB, bằng đúng OmniClaw, vẫn deploy bình thường.

> Ảnh bìa **tự sinh**, không lấy ảnh OG mặc định của GitHub — tám tấm chữ trắng
> nền xám giống hệt nhau là điểm yếu nhất của cả section, với một portfolio làm
> hình ảnh thì càng không dùng được. `build-lab-covers.py` vẽ đúng nhận diện
> amber/tối của trang, mỗi dự án lệch màu và lệch vị trí quầng sáng để phân biệt
> ngay trong lưới. Cần `pip install Pillow`.
>
> Hai cái bẫy trong script, đừng gỡ ra: chữ có alpha **phải** vẽ lên một lớp
> `RGBA` riêng rồi `alpha_composite` — vẽ thẳng `fill=(255,255,255,20)` lên ảnh
> RGB cho ra chữ đặc, không mờ. Và bề rộng tên dự án tính theo mép trái con số
> thứ tự, nếu không tên dài sẽ đè lên nó.
>
> **Không phải repo nào cũng nên lên đây.** Công cụ bypass, crack, hay giải mã
> script được bảo vệ đều là tín hiệu xấu với một người sống bằng nội dung có
> bản quyền — chúng được cố ý để ngoài danh sách.

Các trang `labs/` dùng chung `tokens.css` + `styles.css` với portfolio nên
đổi thương hiệu ở một chỗ là đổi hết, cộng `labs.css` cho phần riêng.

---

## 🎨 Design system

Toàn bộ token nằm ở **`assets/css/tokens.css`**, phải load **trước** `styles.css`.

### Màu

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--primary` | `#ff7a00` | Nhấn chính, CTA |
| `--amber` | `#fcd34d` | Nhấn phụ, eyebrow, mốc timeline |
| `--orange` | `#f97316` | Gradient |
| `--bg-main` | `#0c0a09` | Nền (dark, mặc định) |
| `--bg-surface` | `#1c1917` | Nền section |
| `--bg-card` | `#262220` | Nền thẻ |

Light theme override toàn bộ qua `:root.light-theme`, lưu lựa chọn vào `localStorage`, và áp trong `<head>` **trước khi vẽ khung hình đầu tiên** nên không bị chớp trắng.

### Chữ

`Space Grotesk` (tiêu đề) + `Archivo` (nội dung), tải theo **trục biến thiên** `wght@300..700` — 2 file font thay vì 10 weight tĩnh.

Thang chữ fluid `--text-xs` → `--text-hero` bằng `clamp()`. Đo dòng giới hạn `68ch` — tiếng Việt nhiều từ đơn âm nên dễ mồ côi cuối dòng hơn tiếng Anh.

### Khoảng cách & tầng

Nhịp 4px (`--space-1` → `--space-24`). Thang `z-index` đặt tên (`--z-modal`, `--z-overlay`…) để tránh lỗi kinh điển lightbox chui dưới thanh nav.

---

## 🎞️ Motion

Token thời lượng và tiết tấu theo MOTION-SPEC:

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--dur-instant` | 100ms | Phản hồi nhấn |
| `--dur-fast` | 180ms | Micro-interaction |
| `--dur-base` | 280ms | Chuyển cảnh chuẩn, thẻ |
| `--dur-slow` | 420ms | Reveal lớn |
| `--dur-deliberate` | 640ms | Khoảnh khắc hero |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | **Mặc định** |

### Ba quy tắc bắt buộc

1. **Chỉ animate `transform` và `opacity`.** Mọi thứ khác gây relayout hoặc repaint mỗi khung hình. Thanh scroll progress dùng `scaleX` chứ không phải `width`; shimmer dùng `translateX` chứ không phải `left` hay `background-position`.
2. **Không dùng `transition: all`.** Mọi transition phải gọi tên thuộc tính.
3. **Hiệu ứng con trỏ dùng chung một vòng `requestAnimationFrame`** và ghi vào CSS custom property, không restyle mỗi lần `mousemove`.

### Scroll-driven

Bốn animation gắn thẳng vào vị trí cuộn bằng `animation-timeline` — tính ngoài luồng chính, không listener, không rAF: thanh progress, đường rail timeline, hero lùi khi cuộn qua, và ảnh phần "Về mình" trôi ngược. Bọc trong `@supports`; trình duyệt chưa hỗ trợ thì có nhánh JS thay thế.

Đổi bộ lọc portfolio chạy qua **View Transitions API**, tự rơi về render thường nếu không hỗ trợ.

### Giảm chuyển động

**Không có.** Đây là quyết định có chủ ý của chủ sở hữu: motion chạy đầy đủ cho mọi người, kể cả khi hệ điều hành bật `prefers-reduced-motion`.

> ⚠️ Đánh đổi: người có rối loạn tiền đình sẽ thấy dải logo và dải chữ chạy ngang không dừng — đây là dạng chuyển động dễ gây khó chịu nhất. Muốn bật lại lớp an toàn thì thêm khối này vào `styles.css`, không cần sửa gì khác:
>
> ```css
> @media (prefers-reduced-motion: reduce) {
>   .marquee-track, .kinetic-row { animation: none !important; }
> }
> ```

Từng có phiên bản đặt `transform: none !important` cho `.fade-up` trong nhánh reduced-motion. `.service-card`, `.experience-card` và `.portfolio-card` đều mang class đó, nên `!important` đè lên mọi rule `:hover` — **toàn bộ hover của site chết lặng**. Nếu bao giờ thêm lại nhánh giảm chuyển động: bỏ *chuyển động*, đừng bỏ *phản hồi trạng thái*.

Một bẫy tương tự trong JS: `startPillTyping()` đặt `pill.style.animation = 'none'` trước khi gõ chữ. Inline style đè lên class, nên phải `removeProperty('animation')` trước khi thêm `.pill-float`, không thì hiệu ứng trôi không bao giờ chạy.

---

## ♿ Accessibility

- Skip link là điểm dừng Tab đầu tiên
- Cả 3 modal: focus trap, `Escape`, trả focus về nơi xuất phát, khoá cuộn nền, `aria-hidden`
- `aria-pressed` cho nút lọc và nút ngôn ngữ · `aria-expanded` cho menu mobile
- Label thật cho mọi field liên hệ, `aria-live` cho thông báo gửi
- Vùng chạm tối thiểu 44×44px
- Thuộc tính `lang` của `<html>` đổi theo ngôn ngữ đang chọn
- Icon là SVG inline, không phụ thuộc font icon hay CDN

Kiểm bằng công cụ: 1 `h1`, không nhảy cấp heading, đủ 4 landmark, 0 ảnh thiếu `alt`, 0 field thiếu label, 0 `id` trùng, 0 `iframe` thiếu `title`.

> Chưa test bằng screen reader thật (NVDA / VoiceOver).

---

## 🌐 Song ngữ

Chuỗi giao diện nằm trong object `translations` ở `app.js`; nội dung dự án nằm trong `projects.json` dưới dạng `{ vi, en }`.

Thứ tự ưu tiên: **`?lang=` trên URL → `localStorage` → `vi`**

Nghĩa là `https://portfolio-long-leo.vercel.app/?lang=en` là link chia sẻ được, và đã khai báo `hreflang`.

> Lớp i18n ghi đè `innerHTML` của mọi phần tử `[data-i18n]`. Hiệu ứng tách chữ tiêu đề tạo ra các `<span>` bên trong chính những phần tử đó, nên `app.js` phải gọi lại `refreshTextReveal()` sau mỗi lần dịch — nếu không, hiệu ứng biến mất im lặng.

---

## 🔍 SEO

`canonical` · `hreflang` vi/en/x-default · Open Graph + Twitter Card với ảnh 1200×630 thật · JSON-LD `ProfilePage` → `Person` (kèm địa chỉ, `alumniOf`, `sameAs`) · `robots.txt` · `sitemap.xml` có `xhtml:link` cho từng ngôn ngữ.

---

## 📦 Deploy

**Vercel** — auto-deploy mỗi khi push lên `main`. Đây là nơi deploy duy nhất.

GitHub Pages đã tắt và workflow của nó đã xoá: trước đây site chạy song song ở hai domain trong khi `canonical`, `og:url` và `sitemap.xml` đều trỏ về Vercel — Google sẽ coi bản GitHub Pages là nội dung trùng lặp không khai báo.

Đổi file trong `assets/` phải bump tham số `?v=` trong `index.html` và `cv.html`, nếu không trình duyệt sẽ dùng bản cache cũ.

---

## 📋 Việc còn tồn đọng

Ghi lại thẳng thắn để không quên.

### Nội dung — ưu tiên cao nhất

Case study hiện đang là **template điền theo danh mục, không viết theo dự án**:

```
173 dự án  →  7 giá trị "vai trò"  ·  11 đoạn "giải pháp"  ·  9 số liệu đo được
1 đoạn giải pháp dùng lại cho 46 dự án
```

Nên chọn **5 dự án viết sâu** (bối cảnh → vấn đề và cái giá → quyết định đã cân nhắc → kết quả có số), phần còn lại để dạng gallery. 3–5 case study sâu có sức thuyết phục hơn 173 mô tả giống nhau.

Chưa có **testimonial** nào. Ba câu nhận xét thật kèm tên, chức danh và một con số đo được sẽ có giá trị hơn toàn bộ lớp animation.

### Kỹ thuật

| Việc | Hiện trạng |
|---|---|
| Dung lượng CSS | 108 KB / ngân sách 100 KB — cần minify |
| Dung lượng JS | 83 KB / ngân sách 80 KB |
| Lighthouse | Chưa chạy trên môi trường thật |
| Screen reader | Chưa test bằng NVDA / VoiceOver |

### Kho git

Đã dọn. Repo chỉ track những gì trang thật sự phục vụ — clone về **72 MB** (trước là 299 MB), một commit duy nhất.

> ⚠️ **Git không còn là bản sao dự phòng cho file gốc thiết kế.** File `.psd`/`.psb` và ảnh gốc chưa nén bị `.gitignore` loại ra — chúng vẫn nằm trên máy nhưng không còn được đẩy lên GitHub. Hãy sao lưu `assets/img/design/` ra Drive hoặc ổ ngoài.

---

## 📄 License

© 2026 Hà Đình Long. All rights reserved.

Icon phần mềm trong `assets/img/tools/` là thương hiệu của các hãng tương ứng, dùng để minh hoạ công cụ sử dụng. Lenis phát hành theo giấy phép MIT.
