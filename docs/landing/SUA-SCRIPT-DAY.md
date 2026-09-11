# Sửa `scripts/push-repo-landing.py` để đẩy đủ phần động

## Vấn đề

`local_files()` hiện đẩy một danh sách tên cứng cộng quét **một cấp** của
`gallery/` và `assets/`:

```python
names = ["index.html", "landing/index.html", "landing/cover.jpg", "landing/vercel.json",
         "vercel.json", ".vercelignore"]
for folder in ["landing/gallery", "gallery", "landing/assets", "assets"]:
    ...
    for f in os.listdir(p_dir):     # chỉ một cấp, không đệ quy
```

Nên những file sau **không bao giờ được đẩy**:

- `landing/api/lead.js`, `landing/api/health.js` → API không lên, `POST /api/lead` trả 404
- `landing/data/site.json` → dữ liệu đọc lúc chạy không có
- `landing/deploy-shim.js` → form không nối được API, chân trang không có dòng trạng thái
- `landing/webgl-stage.js` → 6 trang WebGL mất phần 3D
- `landing/README.md`

## Cách sửa

Thay **toàn bộ** hàm `local_files` (dòng 72–91) bằng bản đệ quy dưới đây. Nó quét
cả cây `landing/` thay vì đoán tên file, nên thêm file mới sau này không phải sửa
script nữa.

```python
def local_files(base):
    """Mọi file cần đẩy. Quét đệ quy cây landing/ cộng vài file ở gốc repo."""
    # Không đẩy: file tạm, file hệ thống, thư mục phụ thuộc
    SKIP_DIRS = {".git", ".vercel", "node_modules", "__pycache__", ".next"}
    SKIP_EXT = {".psd", ".psb", ".map", ".log", ".tmp"}
    MAX_BYTES = 20 * 1024 * 1024  # blob lớn hơn 20 MB thì bỏ, báo ra stdout

    names = []

    # 1. Vài file nằm ngay gốc repo
    for n in ["index.html", "vercel.json", ".vercelignore"]:
        if os.path.isfile(os.path.join(base, n)):
            names.append(n)

    # 2. Quét đệ quy toàn bộ landing/ — api/, data/, assets/, gallery/ đều vào đây
    landing_root = os.path.join(base, "landing")
    if os.path.isdir(landing_root):
        for root, dirs, filenames in os.walk(landing_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for f in filenames:
                if f.startswith("."):
                    continue
                if os.path.splitext(f)[1].lower() in SKIP_EXT:
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, base).replace(os.sep, "/")
                names.append(rel)

    # 3. Thư mục media để ngoài landing/ (giữ tương thích với bản cũ)
    for folder in ["gallery", "assets"]:
        p_dir = os.path.join(base, folder)
        if os.path.isdir(p_dir):
            for f in sorted(os.listdir(p_dir)):
                if not f.startswith("."):
                    p = os.path.join(p_dir, f)
                    if os.path.isfile(p):
                        names.append(folder + "/" + f)

    names = sorted(set(names))
    out = []
    for n in names:
        p = os.path.join(base, n.replace("/", os.sep))
        if not (os.path.exists(p) and os.path.isfile(p)):
            continue
        size = os.path.getsize(p)
        if size > MAX_BYTES:
            print(f"  [bo qua] {n} ({size/1024/1024:.1f} MB > 20 MB)")
            continue
        with open(p, "rb") as fh:
            out.append((n, fh.read()))
    return out
```

## Kiểm trước khi đẩy thật

```bash
python scripts/push-repo-landing.py
```

Bản xem trước phải liệt kê đủ, ví dụ với OmniClaw:

```
landing/index.html
landing/deploy-shim.js
landing/vercel.json
landing/README.md
landing/api/health.js
landing/api/lead.js
landing/data/site.json
```

Sáu trang WebGL phải có thêm `landing/webgl-stage.js`. Thiếu dòng nào thì file đó
chưa nằm trong `build/repo-landing/<REPO>/landing/` — chép lại bằng `xcopy` trước.

Thấy đủ rồi mới đẩy:

```bash
python scripts/push-repo-landing.py --push
```

## Kiểm sau khi Vercel deploy xong

```bash
curl https://<domain>/health
curl -X POST https://<domain>/api/lead -H 'Content-Type: application/json' -d '{"value":"ban@congty.vn"}'
```

`/health` trả `{"ok":true,...}` kèm commit sha, `/api/lead` trả
`{"ok":true,"id":"..."}`. Chân trang cũng phải hiện dòng
`… commit <sha> · region <region>`. Không thấy dòng đó nghĩa là `api/` hoặc
`data/` chưa lên.

`/api/lead` trả **404** = thư mục `api/` chưa được đẩy, quay lại bước sửa
`local_files` ở trên.
