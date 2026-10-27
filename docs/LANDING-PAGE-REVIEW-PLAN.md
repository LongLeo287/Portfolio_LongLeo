# Landing Page Studio — review, audit và kế hoạch nâng cấp

> Trạng thái: kế hoạch triển khai cho buổi sáng tiếp theo · cập nhật 2026-10-17
>
> Phạm vi: các landing page con được giới thiệu trong mục **Mã nguồn mở**. Mỗi
> trang giữ một kiến trúc, nhịp kể chuyện, hệ màu, typography và motion riêng;
> chỉ chia sẻ các hợp đồng kỹ thuật chung về accessibility, responsive, SEO,
> performance và data safety.

## 1. Điểm dừng hiện tại

### Inventory

| Nhóm | Trang | Vai trò |
|---|---|---|
| Publishable source | `landing/omniclaw` | Runtime live / terminal |
| Publishable source | `landing/seosona-flow` | Workflow canvas / AI pipeline |
| Publishable source | `landing/seosona-os` | Spatial 3D / knowledge system |
| Publishable source | `landing/seosona-ux-ui` | Design-system workbench |
| Publishable source | `landing/seosona-video-ai` | Media timeline / video factory |
| Publishable source | `landing/tiem-nuoc-nho` | Product mockup / POS |
| Local portfolio only | `landing/seosona` | Editorial narrative |
| Local portfolio only | `landing/portfolio` | Motion narrative / portfolio |
| External-only card | AniBox | TV interface; source và release nằm ngoài repo này |

`build/` là output generated, không phải source để chỉnh trực tiếp. Sitemap của
portfolio hiện chỉ chứa 4 URL thuộc repo chính: homepage, CV và 2 local labs.
Các domain Vercel riêng của 6 landing publishable không được đưa vào sitemap của
portfolio chính; mỗi domain cần sitemap/robots/canonical riêng khi deploy.

### Baseline đã kiểm tra

- `python scripts/check-landing-architectures.py`: PASS — 10 recipe, 9 card map.
- `python scripts/check-catalog.py`: PASS — 114 resource references, 6 staged
  landing repos, 4 sitemap URLs.
- `python scripts/check-budget.py`: PASS — initial CSS 115.7/120 KB raw,
  23.8/30 KB gzip; initial JS 105.9/110 KB raw, 29.7/32 KB gzip; Lenis lazy
  13.2/14 KB raw, 3.7/4 KB gzip.
- `python scripts/check-pages.py`: PASS — 0 error trên 6 staged pages; còn
  warning `sc-shine` là keyframe dành cho editor, không chạy trên release.
- `node --check assets/js/app.js; node --check assets/js/main.js`: PASS.
- `git diff --check`: PASS.
- Contrast script hiện phát hiện 0 cặp fail nhưng 47 cặp không đo được vì màu
  nằm trong bundled/inline landing source. Đây là giới hạn kiểm tra tự động,
  chưa phải chứng nhận WCAG.
- Browser smoke local 2026-10-17 đã đi qua cả 8 route trong inventory (`omniclaw`,
  `seosona-flow`, `seosona-os`, `seosona-ux-ui`, `seosona-video-ai`,
  `tiem-nuoc-nho`, `seosona`, `portfolio`) ở desktop browser viewport và mobile
  390px: mỗi route có đúng ít nhất một `h1`/`main`, text render được và không
  horizontal overflow. Đây là smoke evidence, chưa thay thế audit scorecard
  riêng từng architecture.

### Issue register ban đầu

| ID | Mức | Trạng thái | Bằng chứng / hướng xử lý |
|---|---|---|---|
| `ISSUE-001` | P1 | Đã xác nhận | `check-pages.py` hiện kiểm 6 staged pages; `landing/seosona` và `landing/portfolio` chưa nằm trong coverage. Mở rộng audit source hoặc ghi rõ local-only scope. |
| `ISSUE-002` | P1 | Đã xác nhận | Contrast checker có 47 cặp `not measurable` do màu inline/bundled. Cần browser sampling theo selector trước khi kết luận WCAG. |
| `ISSUE-003` | P1 | Cần xác minh | Sitemap chính có 4 URL là đúng boundary hiện tại, nhưng sitemap/robots/canonical của 6 domain child nằm ngoài repo này và chưa được browser audit trong phiên này. |
| `ISSUE-004` | P1 | Cần xác minh | Source `landing/index.html` có bundler/unpack shell và fallback noscript; cần kiểm tra first paint, JS failure, loading timeout và DOM reading order trên browser. |
| `ISSUE-005` | P2 | Cần xác minh | Tám `data/site.json` cùng ghi `updated: 2026-09-10`; cần đối chiếu với nội dung/release thực tế trước khi hiển thị “updated/live”. |
| `ISSUE-006` | P2 | Cần xác minh | Các trang có motion/WebGL/media khác nhau; cần đo rAF, hidden-tab, reduced-motion, Save-Data, context-loss và disposal riêng từng architecture. |
| `ISSUE-007` | P2 | Cần xác minh | Static inventory không thấy `<img>` runtime trong source shell; cần browser inspect sau unpack để xác nhận alt, intrinsic dimensions, lazy loading và media fallback. |

Không issue nào ở nhóm “cần xác minh” được xem là bug release trước khi có
browser evidence. Mọi fix phải gắn với một ID để tránh sửa theo cảm giác hoặc
đồng nhất hóa các trang có bản chất khác nhau.

## 1.1 Status snapshot — 2026-10-22

The offline portion of the review is now closed:

- `check-pages.py` covers all 6 staged pages plus the 2 local-only source pages.
- `assets/data/landing-qa.json` records the 8 in-repo landing scopes plus AniBox external-only, with explicit static/browser/live/media status.
- `check-contrast.py` measures the declared landing palette pairs with 0 unknown pairs.
- Each publishable child source owns a matching `robots.txt` and one-URL `sitemap.xml`.
- All eight `data/site.json` snapshots use the current source update date; this is not a deployment claim.
- All six `webgl-stage.js` sources enforce reduced-motion/Save-Data quality fallback, coarse/narrow quality limits, hidden-tab pause, and disposal.
- Static checks pass: catalog, page, contrast, budget, architecture, SEO/content, profile, motion contract, JS syntax and diff check.
- Live read-only probe: 5 child domains return root/health `200` but their deployed `robots.txt`/`sitemap.xml` are `404`; OmniClaw returns `404` for root and health. Source SEO files are present locally but are not deployed.

The following remain intentionally unclosed because they require external evidence or
missing product assets: browser matrix/contrast sampling, live child-domain health and
lead requests, screen-reader smoke tests, Lighthouse, and the Flow media gallery
(`FLOW-05`, because the repository contains no 12-image manifest or source set).
The required BrowserSkill instance `3b097077` is currently disconnected; the available
instance is not an authorized substitute. No deploy or push was performed.

## 2. Mục tiêu review

Mỗi landing page phải được review theo cùng một scorecard, nhưng không bị ép vào
một template chung:

1. **Issue và cấu trúc:** hierarchy, reading order, CTA, dead-end, empty/error
   state, link/form contract, content truth.
2. **Sitemap và SEO:** `title`, description, canonical, OG/Twitter, cover,
   `lang`, heading structure, structured data phù hợp, robots và ranh giới
   sitemap.
3. **Nội dung:** vấn đề → quyết định → bằng chứng → giới hạn → CTA; không claim
   live hoặc số liệu nếu không có nguồn/timestamp.
4. **UX/UI:** visual hierarchy, affordance, focus, keyboard, touch target,
   form feedback, mobile information priority và fallback khi JS/WebGL hỏng.
5. **Motion/effect/animation:** motion phục vụ model sản phẩm; ưu tiên
   transform/opacity, không animate layout; có pause/reduced-motion/hidden-tab
   behavior và không tạo scroll ngang.
6. **Font và màu:** font role, Vietnamese glyph coverage, loading strategy,
   line-height, contrast của text nhỏ/disabled/focus/placeholder và sự khác
   biệt thật giữa các trang.
7. **AFR — adaptive/fallback rendering:** policy theo pointer, viewport,
   `prefers-reduced-motion`, Save-Data, WebGL/GPU, network và khả năng JS.
8. **Responsive/accessibility:** ma trận 320, 360, 390, 414, 768, 834, 1024,
   1280, 1440, 1920px; không rớt chữ quan trọng, không mất control, không
   horizontal overflow; kiểm tra keyboard và screen reader smoke test.
9. **Live/data/security:** API schema, loading/stale/error state, timeout,
   privacy của lead form, không hardcode secret, CSP/same-origin và nguồn dữ
   liệu demo phải được đánh dấu.
10. **Media/3D:** poster/cover, alt/caption, intrinsic dimensions, lazy-load,
    WebGL disposal, quality ladder, DOM reading order và static fallback.

### Severity

- **P0 — blocker:** trang không đọc được, CTA/form hỏng, lộ secret, claim live
  sai, overflow làm mất nội dung, WebGL là nguồn thông tin duy nhất.
- **P1 — release-critical:** SEO/metadata sai, keyboard/focus/reduced-motion
  thiếu, font vỡ tiếng Việt, mobile không dùng được, loading/error không rõ,
  performance vượt budget.
- **P2 — quality:** hierarchy, copy, contrast của text phụ, motion timing,
  asset density, thiếu bằng chứng hoặc thiếu trạng thái phụ.
- **P3 — enhancement:** polish visual, micro-interaction, thêm fixture,
  structured data nâng cao sau khi P0/P1 sạch.

## 3. Hợp đồng chung cho mọi landing

### Content và SEO

- Mỗi trang có một `h1` giải thích sản phẩm, không chỉ là tên thương hiệu.
- Hero phải trả lời trong 5 giây: đây là gì, dành cho ai, bằng chứng chính là
  gì và CTA tiếp theo là gì.
- Metadata không dùng nội dung placeholder/editor; cover phải có kích thước,
  alt/context và canonical đúng domain đích.
- Nội dung song ngữ nếu trang được gắn với portfolio: không dịch máy làm hỏng
  tên kỹ thuật; phải kiểm tra line-break ở cả `vi` và `en`.
- Claim số lượng, trạng thái live, tốc độ hoặc khả năng tích hợp phải có nguồn,
  fixture hoặc timestamp visible.

### UX/UI và a11y

- DOM reading order giữ được ý nghĩa khi CSS/JS/WebGL bị tắt.
- Mọi interactive element dùng native button/link/form khi có thể; focus ring
  nhìn thấy; icon-only có accessible name; `aria-live` chỉ dùng cho status.
- Touch target tối thiểu 44px, form lỗi có label và message liên kết bằng
  `aria-describedby`, focus không bị animation che khuất.
- `prefers-reduced-motion: reduce` tắt loop, parallax, camera/rAF không cần
  thiết; không chỉ giảm duration mà vẫn để effect chạy vô hạn.
- `Save-Data`, coarse pointer và máy yếu dùng mode nhẹ; tab hidden không giữ
  rAF/timer live không cần thiết.

### Responsive và AFR

- Test matrix: `320 / 360 / 390 / 414 / 768 / 834 / 1024 / 1280 / 1440 / 1920`.
- Chữ tiếng Việt/English không bị rớt ký tự, không bị cắt; code/token dài dùng
  wrap có chủ đích hoặc horizontal region có nhãn, không làm overflow document.
- Canvas/WebGL là enhancement. Mọi thông tin quan trọng phải có DOM/table/list
  tương ứng. Canvas có `aria-hidden` nếu chỉ trang trí.
- Kiểm tra fine/coarse pointer, zoom 200%, landscape mobile, keyboard-only,
  reduced motion, Save-Data và offline/failed API.

### Performance budget cho child landing

Mỗi trang sẽ có budget riêng theo architecture recipe trong
[`assets/data/landing-architectures.json`](../assets/data/landing-architectures.json):

- HTML initial phải chứa hero và reading order; không chờ WebGL để đọc nội dung.
- Ảnh dùng intrinsic ratio, `loading="lazy"` ngoài hero, `decoding="async"`,
  responsive derivative hoặc SVG/CSS khi hợp lý.
- WebGL/Three.js chỉ tải lazy sau nội dung hero/idle; dispose geometry/material,
  dừng loop khi hidden/unsupported.
- Không thêm framework/bundler chỉ để tạo effect; dùng DOM/CSS/SVG/vanilla và
  resource catalog đã có. SSE/WebSocket chỉ khi có lifecycle, stale state và
  fallback rõ ràng.

## 4. Backlog theo từng landing page

Các task dưới đây là backlog review → implement → QA. Mỗi trang phải hoàn thành
P0/P1 trước khi làm P2/P3.

### LP-01 — OmniClaw · `live-runtime`

**Ý tưởng riêng:** terminal/console của một hệ thống daemon; status live phải
đọc như runtime thật, không phải đèn nhấp nháy trang trí.

- [ ] `OMNI-01` Audit health/lead endpoint, timeout, retry, stale timestamp,
  success/error/disabled state; xác định phần nào là demo fixture.
- [ ] `OMNI-02` Biến danh sách daemon/log thành semantic DOM table/list có label,
  status text và keyboard; không để terminal animation là nguồn duy nhất.
- [ ] `OMNI-03` Tạo motion grammar: boot sequence một lần, pulse có lý do,
  live event stream có pause; dừng khi tab hidden/reduced motion.
- [ ] `OMNI-04` Kiểm tra IBM Plex Mono + font fallback, line length, log wrapping
  ở 320/390/768; bảo đảm command dài không làm document overflow.
- [ ] `OMNI-05` Rà soát green/amber/red contrast, focus ring, alert semantics,
  `aria-live` và copy security/zero-trust có bằng chứng.
- [ ] `OMNI-06` SEO + sitemap riêng của domain; thêm JSON-LD chỉ nếu schema
  phản ánh đúng sản phẩm, không đánh dấu fake software rating.

**Acceptance:** lỗi API vẫn có nội dung usable; live state có timestamp và stale
state; terminal không tự chạy vô hạn khi reduced motion/hidden tab; mobile đọc
được toàn bộ dòng.

**Pilot progress 2026-10-17:** đã thêm health strip có schema check, timeout,
offline/stale path, retry bằng keyboard, polling bằng `setTimeout` và pause khi
hidden/Save-Data; thêm guard chống hydrate trùng và mobile nav scroll có chủ đích.
Browser local đã xác nhận một strip duy nhất, form network error có feedback và
không horizontal overflow ở 390/1440px. Còn phải verify online response thật,
reduced-motion/Save-Data bằng browser profile và deploy endpoint trước khi đánh
dấu toàn bộ `OMNI-01..06` là hoàn tất.

### LP-02 — SEOSONA Flow · `workflow-canvas`

**Ý tưởng riêng:** pipeline/node graph là hero; mockup extension và thư viện ảnh
là bằng chứng, không phải gallery trang trí.

- [ ] `FLOW-01` Kiểm kê 26 node/5 nhóm/12 ảnh/9 tính năng: số liệu phải khớp
  giữa hero, graph, feature copy, fixture và repo.
- [ ] `FLOW-02` SVG graph có `title/desc`, labels DOM hoặc alternative list,
  focus/keyboard cho node tương tác; mobile có viewport graph rõ ràng.
- [ ] `FLOW-03` Tách animation graph thành enter/draw/active state; pause và
  reduced-motion; không animate `left/top`, không tạo reflow.
- [ ] `FLOW-04` Rà mockup side panel/Image-to-Prompt: field label, copy action,
  selected/loading/error state và screenshot/HTML mockup không gây hiểu nhầm là
  extension đang chạy thật.
- [ ] `FLOW-05` Ảnh dùng aspect ratio, `alt`, caption/source, lazy loading và
  fallback; gallery không khiến initial payload phình.
- [ ] `FLOW-06` Audit font, cyan/blue contrast, CTA lead form và canonical/OG.

**Acceptance:** người dùng hiểu workflow khi graph bị tắt; node không bị cắt ở
320px; mockup có trạng thái tương tác; 12 ảnh không tải đồng loạt lúc first paint.

**Pilot progress 2026-10-17:** đã harden `/api/health` với GET/HEAD-only,
JSON/no-store/nosniff headers; thêm deployment health strip có timeout, offline,
retry, polling và pause khi tab hidden/Save-Data. Canvas WebGL đã có accessible
name, containment mobile và ordered-list fallback khi context bị mất hoặc canvas
bị ẩn. Fallback hiện liệt kê đủ 5 nhóm/26 node với tag chính. Browser local xác
nhận health strip hiển thị đúng và không horizontal overflow ở 390px; WebGL stage đã có quality ladder
`full/balanced/lite/static`, pixel-ratio/frame-budget guard và cache-busted
module import. Hero WebGL có control pause/continue keyboard-accessible và pause
được stage thật; mockup side panel/Image-to-Prompt đã có semantic controls, selected
ratio, loading/ready, copy success/error và `aria-live`; browser local xác nhận
interaction ở 390px và responsive render ở 1440px, không horizontal overflow.
Smoke re-test browser sau cache-bust đã xác nhận chọn tỷ lệ `4:5`, generate
`loading -> ready` giữ đúng ratio, copy prompt success và pause control dừng
stage thật; mô phỏng `webglcontextlost` ẩn pause control, ẩn canvas và hiện
fallback 5 item.
Responsive matrix browser bổ sung ở 320/390/414/768/1024/1440/1920px đều không
overflow; canvas lần lượt co trong container và fallback vẫn có 5 item. Production
`GET` và `HEAD https://seosona-flow.vercel.app/api/health` đã trả `200`, JSON,
`Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, commit
`b08b24f...`, region `iad1`, env `production`. Tuy nhiên production page vẫn
đang ở rollout cũ: browser không thấy health strip hoặc fallback mới; WebGL
context loss thật trên production vẫn chưa verify. Không tự deploy khi chưa có
ủy quyền.

**FLOW-05 evidence:** hiện source có 0 `<img>`, 0 `<picture>`, 0 `srcset` và
không có media manifest/gallery trong `landing/seosona-flow`; thư mục chỉ có
`cover.jpg` dùng cho metadata. Copy/FAQ vẫn nói về 12 ảnh WebP, nên mục ảnh đang
`BLOCKED` cho tới khi có asset/fixture manifest thật để kiểm tra `alt`, dimensions,
caption/source, lazy loading và fallback. Không lặp `cover.jpg` để che blocker.

**FLOW-06 evidence:** source tĩnh có title, description, canonical, OG/Twitter
metadata; form có label và browser tree nhận đúng CTA/email control. Browser
sampling local lần đầu tìm thấy hai nút tỷ lệ chưa chọn (`4:5`, `16:9`) chỉ đạt
`2.87:1` vì giữ nền mặc định `#F0F0F0`; deploy shim đã sửa chúng sang nền panel
`#0D1A2D` và text `#EAF4FF` (`15.70:1`). Full rendered-text scan sau fix đo
165 text-bearing elements, 0 fail và 0 unmeasured; mobile 390px cũng giữ đúng
trạng thái. Các cặp đại diện khác đều pass AA: `#9FB6CE` trên `#060B14` = 9.44,
`#7591AD` = 6.01, `#4FDDF2` = 12.16, amber `#F59E0B` = 9.18. Tuy vậy static
checker vẫn ghi nhận 47 cặp source chưa đo được do bundle dùng màu literal/inline,
nên audit coverage toàn source vẫn `NOT VERIFIED`.

**FLOW-01..03 evidence:** `renderVals()` hiện khớp 6+7+8+5+0 = 26 node, 5 nhóm
và 9 feature; fallback DOM lặp lại 5 nhóm/26 node. Canvas có accessible name,
fallback có ordered list, quality ladder và control pause/continue đã được verify
local ở desktop/mobile. Narrow 320px cũng đã xác nhận canvas không bị cắt và
document không overflow. Navigator DOM thêm 5 anchor keyboard-accessible tới các
card nhóm HTML, nên keyboard navigation theo nhóm đã có; từng node WebGL hiện
chưa phải control tương tác riêng có focus/keyboard target, nên phần node-level
của `FLOW-02` vẫn `NOT VERIFIED`.

### LP-03 — SEOSONA OS · `spatial-3d` + `data-dashboard`

**Ý tưởng riêng:** hệ điều hành tri thức dạng orbit; dữ liệu/nhãn DOM phải neo
được ý nghĩa của không gian 3D.

- [ ] `OS-01` Audit scene graph, camera, pixel ratio, WebGL capability, context
  loss và disposal; thêm quality ladder cho GPU yếu/Save-Data.
- [ ] `OS-02` Viết DOM fallback cho core/orbit/memory rings/năm năng lực; keyboard
  order không phụ thuộc vị trí camera.
- [ ] `OS-03` Kiểm tra camera motion, pointer tilt, orbit rotation, idle loop và
  reduced-motion; có nút pause nếu animation mang tính trải nghiệm kéo dài.
- [ ] `OS-04` Chuyển các số liệu/quan hệ chính thành KPI/list/timeline có nguồn,
  timestamp hoặc nhãn “demo fixture”.
- [ ] `OS-05` Rà Lexend + monospace role, gold/purple/light-blue contrast,
  text wrapping và spacing khi màn hình thấp/landscape.
- [ ] `OS-06` SEO/social preview mô tả đúng “knowledge system”, không biến visual
  3D thành claim sản phẩm đã chạy live nếu chưa có bằng chứng.

**Acceptance:** WebGL fail vẫn đọc đủ; scene không tự làm document cao/rộng bất
thường; mobile có một focal point rõ; dashboard numbers có context.

### LP-04 — SEOSONA UX-UI · `design-workbench`

**Ý tưởng riêng:** workbench/token inspector; trang phải chứng minh hệ thống bằng
component states chứ không chỉ khoe gradient.

- [ ] `UX-01` Audit light theme, dark toggle, persistence, system preference và
  FOUC; kiểm tra mọi token foreground/background/focus.
- [ ] `UX-02` Chuẩn hóa component state: default, hover, focus-visible, active,
  disabled, loading, error, empty; mỗi state phải có text/visual distinction.
- [ ] `UX-03` Sidebar responsive: collapse/scroll/focus restoration; không mất
  context khi đổi component hoặc theme.
- [ ] `UX-04` Kiểm tra Manrope Vietnamese glyph, type scale, code/token wrap và
  contrast trong cả light/dark ở 320/390/768.
- [ ] `UX-05` Motion chuyển theme/view transition chỉ là enhancement; reduced
  motion vẫn giữ state change rõ và không flash trắng.
- [ ] `UX-06` Nội dung: thêm token provenance, usage rule, anti-pattern và CTA
  tới repo/design file; không gọi component là production-ready nếu chỉ fixture.

**Acceptance:** theme switch không làm mất focus/setting; component states dùng
được bằng keyboard; contrast pass bằng browser sampling, không chỉ static parser.

### LP-05 — SEOSONA Video AI · `media-timeline`

**Ý tưởng riêng:** filmstrip/timeline; motion mô phỏng quá trình dựng, không
được biến thành video autoplay nặng.

- [ ] `VIDEO-01` Kiểm kê 10 agent/4 layer/queue/chapter; đối chiếu với repo và
  `landing-fixtures.json`; đánh dấu phần mô phỏng.
- [ ] `VIDEO-02` Filmstrip có chapter navigation, timecode accessible, keyboard
  scrub/skip và DOM transcript; không phụ thuộc playhead WebGL.
- [ ] `VIDEO-03` Poster/media facade lazy-load; không autoplay có âm thanh; thêm
  poster/error/unsupported state và caption/transcript khi có video thật.
- [ ] `VIDEO-04` Một rAF chung cho progress/playhead; pause hidden/reduced-motion;
  kiểm tra scroll-driven fallback ở browser chưa hỗ trợ timeline API.
- [ ] `VIDEO-05` Rà Be Vietnam Pro + JetBrains Mono, timecode wrapping, amber
  contrast, focus và 16:9 overflow ở mobile.
- [ ] `VIDEO-06` SEO mô tả workflow/benefit; OG cover không hứa “zero wait” nếu
  đó chỉ là visual metaphor.

**Acceptance:** người dùng hiểu bốn lớp khi media không tải; timeline có điểm
đầu/cuối rõ; không autoplay nặng; 320/390 không cắt playhead/chapter.

### LP-06 — Tiệm Nước Nhỏ · `product-mockup`

**Ý tưởng riêng:** POS thật cho quán nhỏ; hai mặt phone + cashier và offline-first
phải ưu tiên task bán hàng.

- [ ] `TIEM-01` Map task “mở ca → chọn món → thanh toán → đồng bộ”; mockup phải
  thể hiện trạng thái trước/sau chứ không chỉ là khung thiết bị.
- [ ] `TIEM-02` Kiểm tra phone/cashier layout ở mobile; touch target, sticky CTA,
  keyboard form và focus không bị che bởi mockup.
- [ ] `TIEM-03` Offline-first có badge offline/syncing/conflict/error và timestamp;
  không claim Google Sheets là database an toàn nếu chưa nêu giới hạn.
- [ ] `TIEM-04` QR/VietQR chỉ là illustration fixture nếu chưa có tài khoản thật;
  không render thông tin ngân hàng thật hoặc secret trong source.
- [ ] `TIEM-05` Audit red accent/cream contrast, font role, numeric alignment,
  currency/diacritics và wrapping ở 320/390.
- [ ] `TIEM-06` Lead form `tel`: validation, privacy copy, success/error và
  endpoint contract; sitemap/OG/canonical theo domain riêng.

**Acceptance:** task order rõ trong một viewport nhỏ; không cần hover để hiểu
trạng thái; offline/sync error có đường phục hồi; QR không bị hiểu là thanh toán
thật nếu chỉ là demo.

### LP-07 — SEOSONA · `editorial-narrative` (local only)

**Ý tưởng riêng:** case study/editorial; dùng làm chuẩn về storytelling và bằng
chứng, không stage/publish như một repo landing riêng khi chưa có quyết định.

- [ ] `SEO-01` Audit long-form outline: context, problem, decision, result,
  limitation, next step; giảm claim chung chung.
- [ ] `SEO-02` Image chapter có alt/caption/credit/intrinsic size, lazy loading,
  lightbox/focus/escape nếu có interaction.
- [ ] `SEO-03` Typography: Archivo/JetBrains Mono/Space Grotesk role, measure,
  Vietnamese punctuation và heading wrap.
- [ ] `SEO-04` Structured data chỉ dùng dạng phù hợp với case study; canonical
  local route không được phát hành nhầm thành `seosona.com`.
- [ ] `SEO-05` Motion scroll reveal có static path; kiểm tra section anchors,
  back-to-top, reading progress và reduced-motion.

**Acceptance:** đọc liền mạch không cần effect; hình có ngữ cảnh; local-only
boundary không lọt vào sitemap/domain publishable.

### LP-08 — Portfolio · `motion-narrative` (local only)

**Ý tưởng riêng:** motion narrative cho chính portfolio; đây là reference để
đồng bộ với homepage, không phải landing độc lập cần stage lại.

- [ ] `PORT-01` Audit relationship giữa landing portfolio và homepage/labs:
  không trùng CTA, metadata hoặc canonical.
- [ ] `PORT-02` Review scroll-driven motion, hover/tilt/magnetic CTA, loader,
  view transition và Lenis lazy-load theo AFR.
- [ ] `PORT-03` Kiểm tra content density: 5 case study sâu, phần còn lại gallery;
  bổ sung evidence/result thật thay vì thêm animation thay cho nội dung.
- [ ] `PORT-04` Keyboard/touch/reduced-motion/Save-Data parity; no overflow ở
  320/390/1440; font loading và cache-busting.
- [ ] `PORT-05` Giữ sitemap hiện tại chỉ cho route portfolio chính và local labs;
  mọi thay đổi URL phải cập nhật catalog trước.

**Acceptance:** motion làm rõ narrative; tắt motion vẫn còn portfolio hoàn chỉnh;
homepage và child cards không có vòng lặp điều hướng.

### LP-09 — AniBox · `tv-interface` (external-only)

- [ ] `ANIBOX-01` Chỉ audit metadata/link/release status của card và resource map.
- [ ] `ANIBOX-02` Không sửa source Android/repo khác từ workspace này; nếu cần
  nâng cấp TV interface, mở task riêng ở repo AniBox.

## 5. Task cross-cutting và sitemap

### Cross-cutting IDs

- [ ] `CORE-01` Chuẩn hóa landing QA manifest: slug, architecture, domain,
  publish state, owner, last audit, risk, fixture/live.
- [ ] `CORE-02` Mở rộng static audit để kiểm tra metadata, h1, lang, viewport,
  canonical/OG, headings, inline event, animation properties, media dimensions,
  form labels và fallback markers theo source `landing/` — không chỉ `build/`.
- [ ] `CORE-03` Browser QA matrix theo 10 breakpoint; chụp evidence cho desktop
  1440, mobile 390 và narrow 320 trước/sau mỗi page.
- [ ] `CORE-04` Browser contrast sampling cho literal/inline colors; ghi rõ cặp
  fail và selector, không coi `not measurable` là pass.
- [ ] `CORE-05` Font/performance audit: request count, font bytes, image bytes,
  long task, layout shift, WebGL init time; lưu baseline trước khi tối ưu.
- [ ] `CORE-06` Kiểm tra live/API: same-origin, no secret, CORS/CSP, rate limit,
  timeout, stale/error, privacy copy và honeypot/validation.
- [ ] `CORE-07` Chốt sitemap contract: portfolio sitemap chỉ list portfolio
  routes/local labs; mỗi domain landing publishable tự sở hữu canonical,
  robots và sitemap khi được phép deploy.
- [ ] `CORE-08` Review generated output bằng `build-labs.py`/`stage-landing.py`
  sau khi source thay đổi; không patch tay vào `build/`.

### Sitemap decision table

| URL class | Sitemap portfolio chính | Sitemap domain child |
|---|---:|---:|
| `/` và `cv.html` | Có | Không |
| `/labs/omniclaw.html`, `/labs/portfolio.html` | Có | Không |
| 6 domain Vercel publishable | Không | Có, sau khi deploy được duyệt |
| Source `landing/<slug>` | Không | Không phải public URL |
| AniBox external domain | Không | Do repo/site AniBox quản lý |

## 6. Trình tự làm buổi sáng

### Block A — 30 phút: freeze baseline

- [ ] Chụp `git status --short`, không reset/clean dirty work.
- [ ] Chạy 5 check baseline ở mục 1.
- [ ] Mở manifest/catalog, xác nhận domain và publish boundary.
- [ ] Chọn một trang pilot. Khuyến nghị: **OmniClaw** nếu ưu tiên live/API;
  **SEOSONA Flow** nếu ưu tiên mockup/workflow; **SEOSONA OS** chỉ bắt đầu khi
  có thời gian cho WebGL fallback.

### Block B — 60–90 phút: audit pilot

- [ ] Desktop 1440: screenshot hero, content flow, CTA, console/scene.
- [ ] Mobile 390 và narrow 320: overflow, wrapping, focus, touch target.
- [ ] Reduced motion + Save-Data + no WebGL/JS fallback.
- [ ] Ghi issue theo `P0/P1/P2/P3`, không sửa lan sang trang khác.

### Block C — 2–3 giờ: implement một page hoàn chỉnh

- [ ] Sửa content/data contract trước effect.
- [ ] Sửa semantic DOM, responsive layout và state/error.
- [ ] Sau đó mới polish font/color/motion/3D.
- [ ] Regenerate/stage đúng script; không chỉnh generated output trực tiếp.

### Block D — 45 phút: verify và nhân bản quy trình

- [ ] Chạy page checks, budget, catalog, diff check.
- [ ] Browser evidence 320/390/1440.
- [ ] Cập nhật issue log/scorecard.
- [ ] Chọn page tiếp theo theo risk, không mở đồng thời cả 8 trang.

## 7. Definition of Done cho từng trang

- [ ] Architecture ID và data contract khớp `landing-architectures.json` +
  fixture/live boundary.
- [ ] Có hero/h1/CTA/case evidence/limitation/fallback đọc được khi effect tắt.
- [ ] Metadata, canonical, OG/Twitter, sitemap boundary và link domain đúng.
- [ ] Keyboard/focus/labels/aria-live/reduced-motion đã test.
- [ ] Responsive matrix tối thiểu 320, 390, 768, 1440; không horizontal overflow
  và không mất nội dung khi text dài.
- [ ] Font, color, focus và text nhỏ được browser contrast sampling.
- [ ] Image/media/WebGL lazy, fallback, disposal và error state đã kiểm tra.
- [ ] Budget không vượt recipe; không thêm dependency ngoài scope.
- [ ] `check-pages`, `check-catalog`, `check-budget`, `node --check` và
  `git diff --check` PASS; browser evidence được ghi lại.
- [ ] Chỉ sau khi DoD PASS mới cân nhắc stage/deploy; push cần user authorization.

## 8. Không làm trong phiên lập kế hoạch này

- Không sửa trực tiếp `build/` hoặc generated `labs/*.html` nếu chưa thay source
  và chạy generator.
- Không push/deploy 6 repo landing, không gọi GitHub/Vercel API.
- Không thêm framework, bundler, CDN font hoặc WebGL dependency mới chỉ để tạo
  hiệu ứng.
- Không dùng mock data để mô tả là live data; mọi fixture phải được ghi nhãn.
- Không gom 8 trang về một template chung; chỉ dùng shared contract và tooling.
