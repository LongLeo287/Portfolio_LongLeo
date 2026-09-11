#!/usr/bin/env python3
"""Chép tám gói landing từ landing/ sang build/repo-landing/ để chuẩn bị đẩy.

    python scripts/stage-landing.py          # xem sẽ chép gì
    python scripts/stage-landing.py --ghi    # chép thật
    python scripts/push-repo-landing.py --push

Thay cho scripts/build-repo-landing.py. Bộ cũ SINH RA trang bằng template
Python; bản redesign thì không sinh được — nó do công cụ soạn thảo xuất ra,
HTML thật nằm nén trong <script type="__bundler/template">. Nên bước này chỉ
còn là chép, không còn là dựng.

Vì sao có bước trung gian thay vì đẩy thẳng từ landing/: mỗi repo đích có cấu
trúc riêng — api/ phải nằm ở GỐC repo chứ không nằm trong landing/, vì Vercel
chỉ đọc serverless function từ thư mục api/ ở gốc. Ngày 10/09/2026 bốn site
trả 404 ở /api/lead đúng vì chuyện này.

landing/ là nguồn duy nhất. build/ nằm trong .gitignore và bị ghi đè mỗi lần
chạy — đừng sửa gì trong đó.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "landing")
OUT = os.path.join(ROOT, "build", "repo-landing")

# slug trong landing/  ->  (tên repo GitHub, tên project trên Vercel)
#
# Bảng này trước nằm trong scripts/build-repo-landing.py và
# scripts/push-repo-landing.py phải import cả bộ sinh cũ chỉ để lấy sáu dòng
# dữ liệu. Bộ sinh đó đã bỏ ngày 11/09/2026, bảng chuyển về đây.
TARGETS = {
    "omniclaw": ("OmniClaw", "omniclaw-longleo"),
    "seosona-flow": ("seosona-flow", "seosona-flow"),
    "seosona-os": ("SEOSONA-OS", "seosona-os"),
    "seosona-ux-ui": ("SEOSONA-UX-UI", "seosona-ux-ui"),
    "seosona-video-ai": ("SEOSONA-Video-AI", "seosona-video-ai"),
    "tiem-nuoc-nho": ("Tiem_Nuoc_Nho_v5", "tiem-nuoc-nho"),
}

# Hai trang có gói sẵn nhưng cố ý KHÔNG phát hành:
#   portfolio — là bản tài liệu hệ thống thiết kế, không phải trang chủ.
#               Long đã quyết giữ nguyên trang chủ ngày 11/09/2026.
#   seosona   — repo LongLeo287/SEOSONA là app Next.js đã chạy ở
#               seosona.vercel.app; nhét landing/ vào sẽ đụng cấu hình build
#               của chính nó, cần project Vercel riêng.
KHONG_PHAT_HANH = {"portfolio", "seosona"}


def chep(ghi):
    if not os.path.isdir(SRC):
        print("Khong thay " + SRC)
        return 1

    for slug in sorted(os.listdir(SRC)):
        goi = os.path.join(SRC, slug)
        if not os.path.isdir(goi):
            continue
        if slug in KHONG_PHAT_HANH:
            print("  %-18s bo qua — co y khong phat hanh" % slug)
            continue
        muc = TARGETS.get(slug)
        repo = muc[0] if muc else None
        if not repo:
            print("  %-18s KHONG BIET day vao repo nao" % slug)
            continue

        dich = os.path.join(OUT, repo)
        so = 0
        for dirpath, _, fns in os.walk(goi):
            for fn in fns:
                nguon = os.path.join(dirpath, fn)
                tuong_doi = os.path.relpath(nguon, goi).replace("\\", "/")
                # api/ phai nam o GOC repo, khong nam trong landing/
                if tuong_doi.startswith("api/"):
                    dest = os.path.join(dich, tuong_doi.replace("/", os.sep))
                else:
                    dest = os.path.join(dich, "landing",
                                        tuong_doi.replace("/", os.sep))
                if ghi:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copyfile(nguon, dest)
                so += 1
        print("  %-18s -> %-18s %2d file" % (slug, repo, so))

    print("\n" + ("Da chep." if ghi else "Chua ghi gi. Them --ghi de chep that."))
    return 0


if __name__ == "__main__":
    raise SystemExit(chep("--ghi" in sys.argv))
