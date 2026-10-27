# Đưa 8 trang lên Vercel — không phải web tĩnh

Tám trang đã dựng lại hoàn toàn. Mỗi trang là **một project Vercel có phần chạy
trên máy chủ**: serverless function, kiểm dữ liệu phía máy chủ, đọc dữ liệu lúc
chạy. Nhưng **vẫn không có bước build** — `framework: null`, `buildCommand: null`,
không npm install, không bundler. Thế mạnh cũ giữ nguyên, phần tĩnh thì không còn.

## Mỗi thư mục là một project hoàn chỉnh

```
index.html          Trang, tự chứa (font đã nhúng)
deploy-shim.js      Nối form với API + dán trạng thái deployment vào chân trang
webgl-stage.js      Hạ tầng WebGL dùng chung (6 trang có 3D WebGL)
data/site.json      Dữ liệu đọc lúc chạy — sửa file này KHÔNG cần dựng lại trang
api/lead.js         POST /api/lead — nhận lead, kiểm dữ liệu, chống spam theo IP
api/health.js       GET /health — commit, region, env của deployment đang chạy
vercel.json         Header bảo mật, cache, rewrite /health
README.md           Hướng dẫn riêng của project đó
```

| Thư mục | Trang | Hình thức | 3D |
|---|---|---|---|
| `omniclaw/` | OmniClaw — Phosphor Console | Terminal lân quang, IBM Plex Mono | CSS 3D — chồng 8 daemon trên trục Z |
| `seosona-os/` | SEOSONA OS — Observatory | Phòng quan sát, nền tím chàm, Lexend | CSS 3D — orrery 3 vòng |
| `seosona-video-ai/` | SEOSONA Video AI — Film Gate | Buồng phim, nền nâu nhựa phim | **WebGL** — 26 khung phim trên vòng |
| `tiem-nuoc-nho/` | Tiệm Nước Nhỏ — Counter | Nền sáng, đỏ đo từ app thật | **WebGL** — điện thoại, cốc, bóng mềm |
| `seosona-flow/` | SEOSONA Flow — Ink Blueprint | Bản vẽ trên nền mực xanh | **WebGL** — mạng node có photon |
| `seosona-ux-ui/` | SEOSONA UX-UI — Specimen Sheet | Tờ mẫu in, sáng/tối | **WebGL** — 12 khối token đổi màu |
| `seosona/` | SEOSONA Website — Signal | Nhà chung cam, dải chữ động | **WebGL** — lưới sóng 22×9 |
| `portfolio/` | Portfolio — House | Hệ mẹ | **WebGL** — 4 hàng thẻ trôi ngược chiều |
| `_tai-lieu/` | Audit + Design System | Tài liệu, **không** phát hành | — |

## Phần nào là phần động

**`POST /api/lead`** — form trên trang gửi thật tới đây. Có kiểm định dạng phía
máy chủ (email và số điện thoại kiểm riêng), chống spam 5 lượt mỗi phút theo IP,
trả về mã tác vụ để người gửi biết đã nhận. Lead ghi vào **Vercel Runtime Logs**;
đặt biến môi trường `LEAD_WEBHOOK_URL` thì chuyển tiếp sang Zalo/Slack/Apps Script.

**`GET /health`** — trả về commit sha, region, env của deployment đang chạy. Dùng
để biết Vercel đang phục vụ bản nào, thay vì đoán.

**`data/site.json`** — đọc lúc chạy, không nhúng vào HTML. Sửa tên, tagline hay
ngày cập nhật là trang đổi theo mà **không cần dựng lại và không cần deploy**.
Header đã đặt `s-maxage=60, stale-while-revalidate=300`.

## Đẩy lên

### Cách 1 — script bạn đã có

`scripts/push-repo-landing.py` ghi qua Git Data API nên **một commit cho mỗi lần
đẩy** dù bao nhiêu file. Đừng đổi sang Contents API — README của bạn đã ghi lại
vụ 30 deployment trong một lần chạy và bị Vercel khoá 24 giờ ngày 03/08/2026.

```bat
set SRC=<thư mục gói này>
set OUT=D:\SEOSONA AI\LongLeo Profolio\build\repo-landing

xcopy "%SRC%\omniclaw\*"          "%OUT%\OmniClaw\landing\"          /E /I /Y
xcopy "%SRC%\seosona-os\*"        "%OUT%\SEOSONA-OS\landing\"        /E /I /Y
xcopy "%SRC%\seosona-video-ai\*"  "%OUT%\SEOSONA-Video-AI\landing\"  /E /I /Y
xcopy "%SRC%\seosona-flow\*"      "%OUT%\SEOSONA-Flow\landing\"      /E /I /Y
xcopy "%SRC%\seosona-ux-ui\*"     "%OUT%\SEOSONA-UX-UI\landing\"     /E /I /Y
xcopy "%SRC%\tiem-nuoc-nho\*"     "%OUT%\Tiem-Nuoc-Nho\landing\"     /E /I /Y
xcopy "%SRC%\seosona\*"           "%OUT%\SEOSONA\landing\"           /E /I /Y
```

```bash
python scripts/push-repo-landing.py            # xem trước sẽ ghi gì
python scripts/push-repo-landing.py --push     # đẩy thật
```

> **Lưu ý:** script hiện đẩy `index.html` và asset. Giờ mỗi trang còn có
> `api/`, `data/`, `vercel.json`, `deploy-shim.js` — kiểm lại danh sách file
> trong script để nó đẩy đủ, nếu không thì API không lên và form quay về trạng
> thái không gửi được.

`portfolio/` thuộc repo `Portfolio_LongLeo`, commit như bình thường.

### Cách 2 — git thủ công

```bash
cd <repo>
xcopy "<gói>\<slug>\*" landing\ /E /I /Y
git add landing
git commit -m "landing: bản redesign + API lead"
git push
```

### Cách 3 — Vercel CLI, không cần git

```bash
cd <gói>/<slug>
npx vercel --prod
```

## Bắt buộc cho từng project trên Vercel

**Root Directory = `landing`** (Settings → General). Với OmniClaw đây là điều
kiện sống còn: repo có **14.879 file**, tức 99,2% hạn mức 15.000 file mỗi
deployment, nên build hỏng **trước cả bước build** — `vercel.json` và
`.vercelignore` đều vô tác dụng vì lỗi xảy ra sớm hơn lúc chúng được đọc. Đây là
lý do trang OmniClaw đang tạm ngắt, và đẩy thêm nội dung không sửa được.

## Kiểm sau khi deploy

```bash
curl https://<domain>/health
curl -X POST https://<domain>/api/lead \
  -H 'Content-Type: application/json' \
  -d '{"value":"ban@congty.vn"}'
```

`/health` phải trả `{"ok":true,...}` kèm commit sha. `/api/lead` phải trả
`{"ok":true,"id":"..."}`. Nếu `/api/lead` trả 404 thì thư mục `api/` chưa được
đẩy lên — xem lại lưu ý ở Cách 1.

Chân trang mỗi trang sẽ tự hiện một dòng `… commit <sha> · region <region>` khi
API sống. Không thấy dòng đó nghĩa là phần động chưa lên.

## Nếu nội dung đã đúng mà trang vẫn phục vụ bản cũ

```bash
python scripts/push-repo-landing.py --rebuild OmniClaw --push
```

Deployment trước hỏng thì đẩy thêm nội dung không cứu được: `--push` báo *"không
có gì đổi"* vì đúng là không có gì để đổi. Thứ còn thiếu là một commit mới để
Vercel chạy lại; `--rebuild` tạo commit rỗng dùng lại đúng cây của HEAD.

## Kiểm chất lượng trước khi đẩy

```bash
python scripts/check-contrast.py   # tương phản WCAG AA
python scripts/check-pages.py      # cấu trúc, tiếp cận, animation
```

Tám trang đã tự đạt các mục `check-pages.py` bắt: một `h1` duy nhất, không nhảy
cấp heading, mọi `_blank` có `rel="noopener"`, `:focus-visible` khai rõ, không
`id` trùng, và **không animation nào động tới layout hay paint** — chỉ `transform`
và `opacity`.

## Đã sửa gì so với bản cũ

- **Phông chữ**: mỗi trang một cặp riêng và chỉ nạp cặp đó — IBM Plex Mono cho
  OmniClaw, Lexend cho OS, Manrope cho UX-UI, Be Vietnam Pro cho Video AI,
  Space Grotesk + Archivo cho Flow / SEOSONA / Portfolio, Plus Jakarta Sans cho
  POS. Bản cũ nạp ba họ chữ ở cả sáu trang nhưng thực tế chỉ dùng một.
- **Nền**: năm trang từng nằm trong dải `#06080e`–`#0c0a09`, mắt không phân biệt
  được. Giờ tách thật: `#04120C`, `#0A0714`, `#060B14`, `#120D08`, `#FFFBF7`,
  và `#0C0A09` giữ cho nhà chung.
- **FAQ**: `<button aria-expanded>` mở bằng `grid-template-rows`, bấm được bằng
  bàn phím. Bản cũ là `<div>` gắn click — lỗi WCAG 2.1.1 mức A.
- **Không emoji làm icon**: SVG nội tuyến stroke 1.75. Nút ngôn ngữ là chữ VI/EN,
  không dùng cờ vì Windows không render emoji cờ.
- **Chỉ số hero**: nói lợi ích thay vì đếm số file trong repo.
- **Thu lead**: cả tám trang đều có và **gửi được thật**; bản cũ không trang nào có.
- **`transition`** gọi tên thuộc tính, không còn `transition: all`.
- **`prefers-reduced-motion`**: chỉ tắt thứ chạy vô hạn, giữ nguyên phản hồi
  hover và focus. Bản cũ nhét `animation-duration: 0.01ms !important` cho `*`,
  nuke luôn `transition` — đúng cái bẫy README tự cảnh báo.

## Dung lượng và phụ thuộc

Font nhúng thẳng vào file nên trang chạy được cả khi offline, đổi lại `index.html`
nặng 334 KB – 641 KB. Muốn nhẹ, thay khối `@font-face` đã nhúng bằng lại thẻ
`<link href="https://fonts.googleapis.com/...">`; trang về khoảng 40–60 KB.

three.js nạp từ `unpkg.com`, đã ghim `0.184.0`. Sáu trang WebGL cần mạng ở lần
tải đầu. Không có mạng hoặc máy không hỗ trợ WebGL thì canvas tự ẩn, bố cục
không hụt chỗ, toàn bộ nội dung vẫn đọc đủ.
