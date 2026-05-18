# Portfolio_LongLeo

Landing page portfolio cá nhân của Long Leo, dựng lại thành website tĩnh phù hợp để chạy trực tiếp trên GitHub Pages.

## Nguồn nội dung hiện tại

- Kênh YouTube: <https://www.youtube.com/@LongLeo287>
- Playlist portfolio: <https://youtube.com/playlist?list=PLhc6e124Y3Jw4qQYPAkfWcuIO-C3BsuG9&si=9m9mT4jTO_rroCMa>
- CV: đang chờ bổ sung ở vòng cập nhật tiếp theo.
Landing page portfolio cá nhân của Phạm Thành Vinh, dựng lại từ file HTML ban đầu thành cấu trúc tĩnh phù hợp để chạy trực tiếp trên GitHub Pages.

## Cấu trúc

```text
.
├── index.html              # Trang chính GitHub Pages sẽ tự nhận
├── assets/
│   ├── css/styles.css      # Toàn bộ style của landing page
│   └── js/main.js          # Menu mobile, filter portfolio, scroll UI
│   └── js/main.js          # Menu mobile, filter portfolio, form mailto, scroll UI
└── Portfolio Demo.html     # File HTML gốc để tham chiếu
```

## Xem local

Có thể mở trực tiếp `index.html` trong trình duyệt, hoặc chạy server tĩnh:

```bash
python3 -m http.server 8000
```

Sau đó truy cập `http://localhost:8000`.

## Deploy GitHub Pages

1. Push repository lên GitHub.
2. Vào **Settings → Pages**.
3. Ở **Build and deployment**, chọn **Deploy from a branch**.
4. Chọn branch đang dùng và thư mục `/ (root)`.
5. GitHub Pages sẽ phục vụ trang từ `index.html`.
