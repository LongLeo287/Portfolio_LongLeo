# Landing Page Studio

Đây là bộ khung để làm các landing page con trong mục **Mã nguồn mở**. Mỗi
landing page chọn một kiến trúc riêng theo bản chất sản phẩm; không dùng một
template đổi màu cho tất cả dự án.

Nguồn dữ liệu máy đọc được là
[`assets/data/landing-architectures.json`](../assets/data/landing-architectures.json).
Nguồn tham khảo, tiêu chuẩn và skill liên quan nằm trong
[`assets/data/resource-links.json`](../assets/data/resource-links.json).
Fixture an toàn để dựng prototype nằm trong
[`assets/data/landing-fixtures.json`](../assets/data/landing-fixtures.json); đây
không phải dữ liệu live và không được trình bày như số liệu production.

## Các kiến trúc hiện có

| Kiến trúc | Dùng cho | Bề mặt chính | Ví dụ |
|---|---|---|---|
| `product-mockup` | POS, extension, app | HTML/CSS/SVG device frame | Tiệm Nước Nhỏ, SEOSONA Flow |
| `workflow-canvas` | automation, agent, pipeline | SVG node graph + HTML labels | SEOSONA Flow |
| `data-dashboard` | metrics, monitoring, operations | KPI, chart, table, insight | SEOSONA OS, OmniClaw |
| `media-timeline` | video, editing, production | filmstrip, chapter rail, poster facade | SEOSONA Video AI |
| `spatial-3d` | system map, product explorer | progressive WebGL + DOM fallback | SEOSONA OS |
| `live-runtime` | daemon, API, deployment, health | status console + same-origin endpoint | OmniClaw |
| `design-workbench` | UI kit, token, component | token inspector + state matrix | SEOSONA UX-UI |
| `editorial-narrative` | agency, case study, brand story | long-form chapters + evidence | SEOSONA |
| `motion-narrative` | portfolio, reel, creative story | semantic DOM + scroll motion | Portfolio_LongLeo |
| `tv-interface` | Android TV, media library | remote-first shelves + focus states | AniBox |

Một dự án có thể dùng nhiều kỹ thuật, nhưng chỉ có một kiến trúc dẫn đường.
Ví dụ `spatial-3d` có thể có dashboard phụ; dashboard không được biến thành
canvas-only và 3D không được là điều kiện để đọc nội dung.

## Quy tắc chọn kiến trúc

1. Xác định điều người xem cần hiểu trong 5 giây đầu: sản phẩm, quy trình,
   số liệu, không gian, trạng thái live hay câu chuyện.
2. Chọn một `id` trong catalog và ghi rõ `examples`, `dataContract`, `motion`
   và `fallback` trước khi viết markup.
3. Tạo semantic HTML trước: heading, landmark, bảng, danh sách, form và text
   thay thế phải đọc được khi CSS/JS/media không tải.
4. Thêm hình ảnh, mockup, chart, canvas hoặc WebGL như lớp tăng cường; không
   dùng chúng để chứa thông tin duy nhất.
5. Chốt motion mode `full`, `balanced`, `lite`, `static`. `prefers-reduced-motion`
   và `Save-Data` là ràng buộc cứng.
6. Chỉ dùng live data sau khi có fixture, timeout, schema validation, stale
   state và error state.

## Contract dữ liệu

Landing page nên tách nội dung khỏi hiệu ứng. Một fixture tối thiểu nên có
version, timestamp và trạng thái:

```json
{
  "schemaVersion": 1,
  "updatedAt": "2026-10-17T00:00:00Z",
  "source": "demo-fixture",
  "status": "ready",
  "items": []
}
```

Với dashboard, mỗi metric cần `id`, `label`, `value`, `unit`, `delta`,
`timestamp` và `status`. Với live endpoint, trạng thái hiển thị phải phân biệt
`live`, `stale`, `offline` và `error`; không giả dữ liệu live bằng con số không
có timestamp.

Với media, mỗi asset cần `src`, `srcset` hoặc poster, `width`, `height`, `alt`,
`caption` và `credit` khi cần. Với 3D, scene manifest cần `model`, `objects`,
`labels`, `cameraPresets` và một DOM/SVG fallback tương đương.

Khi dựng prototype, dùng fixture tương ứng trong `landing-fixtures.json`; chỉ
đổi sang endpoint thật sau khi đã có schema, timeout, stale state và quyền truy
cập rõ ràng.

## Bề mặt hình ảnh và 3D

- Mockup: ưu tiên CSS frame, SVG và screen state HTML; screenshot chỉ là bằng
  chứng phụ.
- Dashboard: chart chỉ là lớp trực quan; table/text summary là nguồn sự thật.
- Image story: luôn có responsive derivative, dimensions, alt/caption và lazy
  loading dưới fold.
- 3D: lazy-load WebGL, giảm chất lượng theo capability/frame time, dừng khi
  hidden/off-screen và giữ DOM fallback.
- Video/live media: dùng poster/facade trước; không tải iframe hoặc autoplay
  nặng trước intent của người dùng.

## Ngân sách mặc định

Catalog đặt ngân sách theo từng kiến trúc. Homepage hiện giữ budget chung
`120 KB raw / 30 KB gzip CSS` và `110 KB raw / 32 KB gzip JS`; landing con nên
đặt runtime riêng, tránh đưa Three.js, chart engine hoặc video runtime vào
critical path nếu trang không cần chúng ở hero.

Kiểm tra bắt buộc: 320, 390, 414, 768, 1024, 1440 và 1920px; keyboard/focus;
reduced motion; slow network; hidden tab; lỗi API; lỗi ảnh; WebGL không hỗ trợ;
và không horizontal overflow.

## Workflow tạo landing page mới

Skill dự án nằm tại
`.agents/skills/landing-page-studio/SKILL.md`.

```text
brief sản phẩm
  → chọn architecture id
  → khai báo fixture/data contract
  → dựng semantic shell + fallback
  → thêm visual surface riêng
  → thêm motion theo quality tier
  → kiểm budget, accessibility, responsive và runtime states
```

`landing/` là source của các repo landing riêng. `build/` là output staging,
không sửa trực tiếp. Không chạy push/deploy nếu chưa có ủy quyền rõ ràng.
