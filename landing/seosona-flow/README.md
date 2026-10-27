# SEOSONA Flow — landing

Trang phát hành cho **SEOSONA Flow**. Đây **không phải web tĩnh**: nó có serverless
function, kiểm dữ liệu phía máy chủ và đọc dữ liệu lúc chạy.

## Cấu trúc

```
index.html          Trang, tự chứa (font đã nhúng)
deploy-shim.js      Nối form với API, dán trạng thái deployment vào chân trang
webgl-stage.js      Hạ tầng WebGL dùng chung, có quality ladder full/balanced/lite/static
data/site.json      Dữ liệu đọc lúc chạy — sửa file này không cần dựng lại trang
api/lead.js         POST /api/lead — nhận lead, kiểm dữ liệu, chống spam theo IP
api/health.js       GET /health — commit, region, env của deployment đang chạy
vercel.json         Header bảo mật, cache, rewrite /health
```

## Không có bước build

`framework: null`, `buildCommand: null`. Vercel phục vụ file tĩnh và chạy
function trong `api/`. Không npm install, không bundler.

## Kiểm sau khi deploy

```bash
curl https://<domain>/health
curl -X POST https://<domain>/api/lead \
  -H 'Content-Type: application/json' \
  -d '{"value":"ban@congty.vn"}'
```

Lead ghi vào **Vercel Runtime Logs**. Muốn chuyển tiếp đi đâu thì đặt biến môi
trường `LEAD_WEBHOOK_URL` — không đặt cũng chạy, chỉ là lead nằm trong log.

WebGL tự chọn quality theo reduced motion, `Save-Data`, pointer, device memory và
CPU hint. `static` chỉ dựng một frame; `balanced` và `lite` giảm pixel ratio và
nhịp render. Người dùng có thể tạm dừng/tiếp tục motion bằng control keyboard-
accessible trên hero. Nội dung DOM/fallback không phụ thuộc vào canvas.

Mockup side panel là demo fixture rõ ràng, không gọi extension thật: các nút tỷ lệ
có `aria-pressed`, nút `Sinh ảnh` hiển thị loading/ready, còn Image-to-Prompt có
copy action và thông báo success/error trong `aria-live`.

Khi WebGL mất context hoặc canvas bị ẩn, ordered-list fallback vẫn giữ đủ năm
nhóm workflow và tổng 26 node trong DOM.

Navigator DOM của workflow cung cấp năm anchor keyboard-accessible tới các card
nhóm HTML; nó hiện khi nhận focus để không cạnh tranh với hero visual. Đây là
điều hướng theo nhóm, không giả vờ biến từng node WebGL thành một control riêng.
