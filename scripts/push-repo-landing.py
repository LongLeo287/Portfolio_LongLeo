#!/usr/bin/env python3
"""Đẩy landing page đã sinh vào chính repo của từng dự án.

Không clone repo nào — mấy repo kia nặng hàng trăm MB, clone chỉ để thêm vài
file là phí.

    python scripts/build-repo-landing.py     # sinh trước
    python scripts/push-repo-landing.py      # xem sẽ làm gì (mặc định)
    python scripts/push-repo-landing.py --push   # đẩy thật

**Mỗi repo chỉ tạo ĐÚNG MỘT COMMIT**, kể cả khi thay mười file. Đây không phải
chuyện thẩm mỹ. Contents API chỉ ghi được một file mỗi lần và mỗi lần là một
commit, mà mỗi commit lại kích hoạt một deployment Vercel. Gói Hobby giới hạn
100 deployment mỗi ngày — đẩy 5 file vào 6 repo theo kiểu đó là 30 deployment
cho MỘT lần chạy, vài vòng là hết hạn mức và Vercel khoá 24 giờ (đã xảy ra thật
ngày 03/08/2026). Dùng Git Data API (blob → tree → commit → ref) thì bao nhiêu
file cũng chỉ một deployment.

Idempotent: file nào nội dung đã giống hệt thì bỏ qua; không có gì đổi thì
không tạo commit. Ghi vào nhánh mặc định của repo — có repo dùng master.

Yêu cầu: gh đã đăng nhập, token có scope repo.
"""
import base64
import importlib.util
import json
import os
import subprocess
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing")
OWNER = "LongLeo287"

MSG = "Cập nhật landing page"


def load_targets():
    path = os.path.join(ROOT, "scripts", "build-repo-landing.py")
    spec = importlib.util.spec_from_file_location("build_repo_landing", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TARGETS


def gh(*args, inp=None, check=True):
    r = subprocess.run(["gh", *args], input=inp, capture_output=True,
                       text=True, encoding="utf-8")
    if check and r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip())
    return r


def api(path, method=None, payload=None, check=True):
    args = ["api", path]
    if method:
        args += ["--method", method]
    if payload is not None:
        args += ["--input", "-"]
    r = gh(*args, inp=json.dumps(payload) if payload is not None else None, check=check)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout) if r.stdout.strip() else {}


def local_files(base):
    """Mọi file cần đẩy. Quét toàn bộ thư mục landing, assets và gallery."""
    names = ["index.html", "landing/index.html", "landing/cover.jpg", "landing/vercel.json",
             "vercel.json", ".vercelignore"]
    
    # Quét mọi thư mục media / assets
    for folder in ["landing/gallery", "gallery", "landing/assets", "assets"]:
        p_dir = os.path.join(base, folder.replace("/", os.sep))
        if os.path.isdir(p_dir):
            for f in os.listdir(p_dir):
                if not f.startswith("."):
                    names.append(folder + "/" + f)
                    
    names = sorted(list(set(names)))
    out = []
    for n in names:
        p = os.path.join(base, n.replace("/", os.sep))
        if os.path.exists(p) and os.path.isfile(p):
            out.append((n, open(p, "rb").read()))
    return out


def remote_blob(repo, path):
    d = api(f"repos/{OWNER}/{repo}/contents/{path}", check=False)
    if not d or "content" not in d:
        return None
    return base64.b64decode(d["content"])


def push_one(repo, files, dry):
    """Một commit cho toàn bộ thay đổi: so sánh tree trong 1 API call, upload blob và commit."""
    repo_info = api(f"repos/{OWNER}/{repo}")
    if not repo_info or "default_branch" not in repo_info:
        return 0
    branch = repo_info["default_branch"]
    head_ref = api(f"repos/{OWNER}/{repo}/git/ref/heads/{branch}")
    if not head_ref or "object" not in head_ref:
        return 0
    head = head_ref["object"]["sha"]
    base_commit = api(f"repos/{OWNER}/{repo}/git/commits/{head}")
    base_tree = base_commit["tree"]["sha"]

    # Lấy toàn bộ cây remote trong ĐÚNG 1 request
    tree_data = api(f"repos/{OWNER}/{repo}/git/trees/{base_tree}?recursive=1", check=False)
    remote_shas = {}
    if tree_data and "tree" in tree_data:
        for item in tree_data["tree"]:
            remote_shas[item["path"]] = item["sha"]

    changed = []
    tree = []
    for path, blob in files:
        # Tính sha git blob cục bộ: sha1("blob " + size + "\0" + content)
        import hashlib
        header = f"blob {len(blob)}\0".encode()
        local_sha = hashlib.sha1(header + blob).hexdigest()

        if remote_shas.get(path) != local_sha:
            changed.append((path, blob, path in remote_shas))

    for path, blob, existed in changed:
        print(f"   {'~' if existed else '+'}  {path}  ({len(blob) // 1024 or 1} KB)")
    if not changed:
        print("   =  không có gì đổi")
        return 0
    if dry:
        return len(changed)

    # Upload blob cho các file thực sự thay đổi
    for path, blob, _ in changed:
        sha = api(f"repos/{OWNER}/{repo}/git/blobs", "POST",
                  {"content": base64.b64encode(blob).decode(),
                   "encoding": "base64"})["sha"]
        tree.append({"path": path, "mode": "100644", "type": "blob", "sha": sha})

    new_tree = api(f"repos/{OWNER}/{repo}/git/trees", "POST",
                   {"base_tree": base_tree, "tree": tree})["sha"]
    commit = api(f"repos/{OWNER}/{repo}/git/commits", "POST",
                 {"message": MSG, "tree": new_tree, "parents": [head]})["sha"]
    api(f"repos/{OWNER}/{repo}/git/refs/heads/{branch}", "PATCH", {"sha": commit})
    print(f"   →  1 commit {commit[:7]} trên {branch} ({len(changed)} file)")
    return len(changed)


def rebuild(repo, dry):
    """Tạo một commit rỗng để bắt Vercel dựng lại.

    Cần khi nội dung trong repo đã đúng nhưng bản đang phục vụ vẫn cũ — chẳng
    hạn deployment trước bị chặn vì hết hạn mức. Lúc đó đẩy thêm nội dung là vô
    ích vì không có gì khác để đẩy; phải có một commit mới thì Vercel mới chạy.
    Commit rỗng dùng lại đúng cây của HEAD nên không đổi một byte nào.
    """
    branch = api(f"repos/{OWNER}/{repo}")["default_branch"]
    head = api(f"repos/{OWNER}/{repo}/git/ref/heads/{branch}")["object"]["sha"]
    tree = api(f"repos/{OWNER}/{repo}/git/commits/{head}")["tree"]["sha"]
    print(f"\n{repo}: commit rỗng trên {branch} để dựng lại")
    if dry:
        print("   (bản thử)")
        return
    c = api(f"repos/{OWNER}/{repo}/git/commits", "POST",
            {"message": "Dựng lại landing page", "tree": tree, "parents": [head]})["sha"]
    api(f"repos/{OWNER}/{repo}/git/refs/heads/{branch}", "PATCH", {"sha": c})
    print(f"   →  {c[:7]}")


def main():
    dry = "--push" not in sys.argv

    # --rebuild <repo> [...] : chỉ kích hoạt dựng lại, không đụng nội dung.
    if "--rebuild" in sys.argv:
        i = sys.argv.index("--rebuild")
        repos = [a for a in sys.argv[i + 1:] if not a.startswith("--")]
        if not repos:
            print("Dùng: --rebuild <tên-repo> [tên-repo ...] [--push]")
            return 1
        for r in repos:
            rebuild(r, dry)
        if dry:
            print("\nĐây mới là bản thử. Thêm --push để làm thật.")
        return 0

    targets = load_targets()
    if not os.path.isdir(OUT):
        print("Chưa có build/repo-landing — chạy scripts/build-repo-landing.py trước.")
        return 1

    total, repos = 0, 0
    for slug, (repo, vercel_name) in targets.items():
        files = local_files(os.path.join(OUT, repo))
        print(f"\n{repo}  ->  https://{vercel_name}.vercel.app")
        n = push_one(repo, files, dry)
        total += n
        repos += 1 if n else 0

    print(f"\n{total} file đổi trên {repos} repo = {repos} commit = {repos} deployment.")
    if dry:
        print("Đây mới là bản thử. Thêm --push để đẩy thật.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
