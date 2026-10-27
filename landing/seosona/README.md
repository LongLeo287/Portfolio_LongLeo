# SEOSONA — rebuild archive

Landing page/case study cho dự án rebuild website SEOSONA. Trang dùng mô hình
`tv-interface` làm architecture dẫn đường: content-first shelves, focus state,
featured route và system map; nội dung vẫn là case study semantic, không phải
anime UI copy.

## Project links

- Bản rebuild: <https://seosona.vercel.app/>
- Repository triển khai: <https://github.com/LongLeo287/SEOSONA>
- Website gốc tham chiếu: <https://seosona.com/>
- Source implementation chính: `D:\LongLeo\SEOSONA AI\SEOSONA Website`

## Runtime

- `index.html` là semantic shell và no-JS reading path.
- `redesign.css` là visual system dark navy/mint/blue, responsive shelves,
  CSS 3D system map và motion tiers.
- `deploy-shim.js` xử lý menu mobile, shelf keyboard navigation, feature
  switching, reveal motion, pointer tilt và form lead progressive enhancement.
- `api/health.js` chỉ là deployment utility; không có health/status rail nào được
  render trên landing.
- `assets/seosona-logo-official.png` và `assets/screen-*.png` là brand/surface
  evidence từ bản rebuild.

Motion mặc định bật, không còn thanh chọn `Full / Soft / Off` trong UI. AFR
dùng chung cho portfolio và các landing: tự hạ `full → balanced → lite →
static` theo capability hint, frame-time/long-task pressure, visibility và
scroll; `prefers-reduced-motion` và Save-Data vẫn được tôn trọng. 3D là CSS
progressive enhancement, không bắt buộc WebGL.

## Verification

Serve repository qua HTTP rồi mở `/landing/seosona/`; không mở trực tiếp bằng
`file://`. Kiểm tra responsive ở 320, 390, 768, 1280 và 1440px, cùng keyboard,
reduced motion, AFR fallback và missing-image fallback.
