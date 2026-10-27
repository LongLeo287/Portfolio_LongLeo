# Child landing redesign plan

Updated: 2026-10-17

## Mục tiêu

Đưa các child landing lên cùng quality bar với Portfolio LongLeo: hero có chủ đích,
typography/editorial rhythm rõ, bằng chứng sản phẩm thật, CTA dễ hiểu và responsive
không phụ thuộc vào WebGL hay animation để đọc nội dung.

Không dùng một template giống nhau cho mọi dự án. Chỉ dùng chung các hợp đồng về
accessibility, responsive, metadata, performance và content provenance.

## Thứ tự triển khai

| Bước | Trang | Art direction | Artifact chính | Trạng thái |
|---|---|---|---|---|
| 1 | `tiem-nuoc-nho` | editorial POS / quầy bán hàng | mobile POS, desktop dashboard, VietQR, offline queue | Pilot visual layer đã thêm |
| 2 | `seosona-flow` | workflow canvas | node graph, provider adapters, local/offline mode | Visual layer đã thêm |
| 3 | `omniclaw` | control room / terminal | daemon registry, health state, log stream | Visual layer đã thêm |
| 4 | `seosona-ux-ui` | design workbench | token sheet, component specimen, motion rules | Visual layer đã thêm |
| 5 | `seosona-video-ai` | media timeline | HyperFrames, agent lanes, FFmpeg/Whisper pipeline | Visual layer đã thêm |
| 6 | `seosona-os` | knowledge operating system | doctrine, memory layers, MCP/knowledge map | Visual layer đã thêm |

## Mỗi trang phải hoàn thành

1. Hero trả lời rõ: đây là gì, dành cho ai, bằng chứng nào và CTA tiếp theo.
2. Tối đa 5–7 section chính; FAQ/limitations chỉ giữ nội dung giúp ra quyết định.
3. Có ít nhất một artifact trực quan từ source repo, nhưng thông tin quan trọng vẫn
   nằm trong DOM khi JavaScript/WebGL bị tắt.
4. Claim số lượng/version/live status phải trỏ về `assets/data/project-evidence.json`
   hoặc có timestamp/fixture rõ ràng.
5. Kiểm tra 320, 390, 768, 1280 và 1440px; reduced motion, keyboard, focus,
   overflow, fallback và loading/error state.

## Pilot đã làm

`landing/tiem-nuoc-nho/redesign.css` là enhancement layer được mount bởi
`deploy-shim.js` sau hydration. Nó bổ sung editorial hero, grid texture, card depth,
section rhythm, CTA treatment, mobile breakpoint và reduced-motion behavior; không
thay thế nội dung semantic hoặc WebGL fallback hiện có.

## Không làm

- Không copy nguyên theme Portfolio LongLeo lên mọi dự án.
- Không thêm claim sản phẩm chỉ vì có thể mô phỏng bằng CSS/WebGL.
- Không sửa generated output ngoài `landing/` như thể đó là source.
- Không deploy/push khi chưa có xác nhận riêng.
