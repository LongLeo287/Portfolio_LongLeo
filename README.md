# Portfolio_LongLeo

Landing page portfolio cá nhân của Long Leo, dựng lại thành website tĩnh phù hợp để chạy trực tiếp trên GitHub Pages.

## Nguồn nội dung hiện tại

- Kênh YouTube: <https://www.youtube.com/@LongLeo287>
- Playlist portfolio: <https://youtube.com/playlist?list=PLhc6e124Y3Jw4qQYPAkfWcuIO-C3BsuG9&si=9m9mT4jTO_rroCMa>
- CV: đang chờ bổ sung ở vòng cập nhật tiếp theo.

## Cấu trúc

```text
.
├── index.html              # Trang chính GitHub Pages sẽ tự nhận
├── assets/
│   ├── css/styles.css      # Toàn bộ style của landing page
│   └── js/main.js          # Menu mobile, filter portfolio, scroll UI
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

## Ghi chú xử lý conflict PR

Nếu GitHub báo **This branch has conflicts that must be resolved**, nguyên nhân thường là branch PR cũ được tạo từ commit trước khi `main` có các file static (`index.html`, `assets/css/styles.css`, `assets/js/main.js`). Hãy dùng branch/PR đã được cập nhật sau khi merge `main`, hoặc đóng PR cũ và mở PR mới từ branch mới nhất để GitHub so sánh các file này dưới dạng chỉnh sửa thay vì thêm mới trùng đường dẫn.
