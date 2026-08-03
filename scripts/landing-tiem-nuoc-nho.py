#!/usr/bin/env python3
"""Landing page riêng cho Tiệm Nước Nhỏ POS.

Đây là dự án duy nhất trong nhóm có **người dùng thật đang dùng hằng ngày**,
nên trang phải cho xem giao diện chứ không tả bằng chữ. Toàn bộ mockup vẽ bằng
HTML/CSS/SVG — repo không có ảnh chụp nào, mà ảnh chụp cũng sẽ lệch với bản
thật ngay lần cập nhật đầu.

Màu và phông lấy đúng từ ứng dụng đang chạy (đo trực tiếp trên
tiem-nuoc-nho.vercel.app/app/): Plus Jakarta Sans, đỏ #C9252C, bo góc 16px.
Nền tối giữ theo nhà chung của các trang labs, nhưng màu nhấn theo sản phẩm —
trang giới thiệu nên trông giống thứ nó giới thiệu.

    python scripts/landing-tiem-nuoc-nho.py

Số liệu đọc từ repo Tiem_Nuoc_Nho_v5 (package.json, cây thư mục src/ và gas/).
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "Tiem_Nuoc_Nho_v5")
SITE = "https://tiem-nuoc-nho.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/Tiem_Nuoc_Nho_v5"
APP = "/app/"

# --- số liệu đếm từ repo ---
N_COMPONENTS = 27       # src/components/**/*.tsx
N_SERVICES = 10         # gas/*Service.js
N_CONTEXTS = 5          # src/context/
N_SRC = 54              # src/**

STACK = ["React 19", "TypeScript", "Vite", "Tailwind CSS v4", "Framer Motion",
         "Lucide", "Recharts", "D3", "IndexedDB", "Google Apps Script",
         "Google Sheets", "VietQR"]

STATS = [
    (N_COMPONENTS, "", "component React"),
    (N_SERVICES, "", "service phía backend"),
    (2, "", "giao diện, một mã nguồn"),
    (0, "đ", "chi phí máy chủ mỗi tháng"),
]

STEPS = [
    ("cart", "Nhân viên bấm order",
     "Chạm vào món trên lưới, số lượng cộng dồn ngay. Vuốt ngang một dòng để sửa "
     "hoặc xoá. Chưa thanh toán thì lưu nháp, mở lại lúc nào cũng được."),
    ("qr", "Khách quét mã trả tiền",
     "Mã QR chuyển khoản sinh theo đúng số tiền của đơn, đúng chuẩn VietQR. Khách "
     "quét bằng app ngân hàng nào cũng được, không phải gõ lại số."),
    ("sheet", "Chủ quán mở bảng tính lên xem",
     "Dữ liệu nằm trong Google Sheets. Chủ quán sửa giá, thêm món, xem doanh thu "
     "ngay trong thứ họ vốn đã biết dùng — không cần học phần mềm mới."),
]

FEATURES = [
    ("phone", "Hai giao diện, một mã nguồn",
     "Trên điện thoại là thanh điều hướng dưới đáy, thao tác gọn trong một ngón tay. "
     "Trên máy tính tự mở thành sidebar cố định và lưới nhiều cột cho quầy thu ngân."),
    ("offline", "Mất mạng vẫn bán được",
     "Đơn ghi thẳng vào IndexedDB trong máy, worker nền đẩy lên khi có mạng lại. "
     "Có bộ giải xung đột cho trường hợp hai máy sửa cùng một đơn."),
    ("qr", "QR thanh toán tự sinh",
     "Dùng chuẩn VietQR nên mọi app ngân hàng đều quét được. Số tiền và nội dung "
     "chuyển khoản điền sẵn theo đơn, khách khỏi gõ tay."),
    ("swipe", "Vuốt để sửa, chạm để thêm",
     "Cử chỉ vuốt trên từng dòng giỏ hàng, hiệu ứng bay vào giỏ khi thêm món. "
     "Giờ cao điểm thì từng thao tác thừa đều thành hàng dài trước quầy."),
    ("list", "Hàng nghìn đơn vẫn cuộn mượt",
     "Danh sách lịch sử dựng bằng kỹ thuật ảo hoá — chỉ vẽ những dòng đang nhìn "
     "thấy, nên số đơn tăng bao nhiêu cũng không chậm đi."),
    ("chart", "Bảng doanh thu ngay trong app",
     "Biểu đồ dựng bằng Recharts và D3: doanh thu theo ngày, món bán chạy, "
     "tồn kho sắp hết có cảnh báo riêng."),
    ("lock", "Phân quyền theo vai trò",
     "Nhân viên pha chế, thu ngân và chủ quán thấy những màn hình khác nhau. "
     "Đăng nhập bằng tên và mã PIN, không cần email."),
    ("print", "In hoá đơn và xuất ảnh",
     "In thẳng ra máy in nhiệt, hoặc xuất hoá đơn thành ảnh để gửi qua Zalo cho "
     "khách đặt trước."),
    ("moon", "Có cả lịch âm",
     "Chi tiết nhỏ nhưng đúng thực tế buôn bán ở Việt Nam: mùng một, ngày rằm và "
     "dịp lễ âm lịch hiện ngay trên bảng theo dõi."),
]

LIMITS = [
    ("Làm riêng cho một quán, không phải sản phẩm bán đại trà",
     "Danh mục món, vai trò nhân viên và luồng thanh toán đều gắn với cách vận hành "
     "của đúng quán này. Muốn dùng cho quán khác thì phải sửa cấu hình, không phải cài là chạy."),
    ("Google Sheets là database — được và mất",
     "Được: chi phí bằng không, chủ quán tự sửa dữ liệu, sao lưu sẵn có. Mất: Apps "
     "Script có hạn mức gọi mỗi ngày, và bảng tính không hợp với quy mô hàng chục nghìn đơn mỗi tháng."),
    ("Bản chạy thật cần tài khoản",
     "Đường dẫn ứng dụng bên dưới mở ra màn hình đăng nhập của quán. Đây là hệ thống "
     "đang chạy thật với dữ liệu thật, không phải bản demo mở cho khách xem."),
]

FAQ = [
    ("Bấm vào ứng dụng thì có dùng thử được không?",
     "Không. Đó là hệ thống đang chạy thật của quán, mở ra sẽ thấy màn hình đăng nhập "
     "bằng tên và mã PIN. Muốn xem giao diện thì các mockup trên trang này dựng đúng "
     "theo bản thật."),
    ("Vì sao lại chọn Google Sheets làm database?",
     "Vì người dùng cuối là chủ một quán nước nhỏ. Họ đã biết dùng bảng tính, và không "
     "kham nổi tiền server hằng tháng cho một quán vài chục đơn mỗi ngày. Đổi lại là "
     "hạn mức gọi của Apps Script."),
    ("Mất mạng giữa lúc đông khách thì sao?",
     "Vẫn bán bình thường. Đơn ghi vào IndexedDB ngay trong trình duyệt, worker nền "
     "đẩy lên khi mạng có lại, và có bộ giải xung đột nếu hai máy cùng sửa một đơn."),
    ("Có chạy trên máy tính không hay chỉ điện thoại?",
     "Cả hai, cùng một mã nguồn. Dưới một ngưỡng bề rộng thì là thanh điều hướng đáy "
     "cho điện thoại, trên ngưỡng đó tự mở thành sidebar và lưới nhiều cột cho quầy."),
    ("Mã QR có phải chụp sẵn không?",
     "Không, sinh động theo từng đơn bằng thư viện VietQR — đúng số tiền, đúng nội dung "
     "chuyển khoản. Khách quét bằng app ngân hàng nào cũng được."),
    ("Mã nguồn có mở không?",
     "Có, toàn bộ nằm trên GitHub, cả phần frontend React lẫn phần Apps Script."),
]

# Menu giả trong mockup — giá và tên đặt cho giống một quán nước thật.
MENU = [("🧋", "Trà sữa trân châu", "32.000"), ("☕", "Cà phê sữa đá", "25.000"),
        ("🍵", "Trà đào cam sả", "30.000"), ("🥤", "Soda việt quất", "35.000"),
        ("🧉", "Trà tắc mật ong", "22.000"), ("🍫", "Cacao đá xay", "40.000")]

CART = [("Trà sữa trân châu", 2, "64.000"), ("Cà phê sữa đá", 1, "25.000")]

ICONS = {
    "cart": "M3 4h2l2.6 11h10.2L20 7H6M9 20a1 1 0 1 0 2 0 1 1 0 1 0-2 0m7 0a1 1 0 1 0 2 0 1 1 0 1 0-2 0",
    "qr": "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2z",
    "sheet": "M4 3h16v18H4zM4 9h16M4 15h16M10 3v18M16 3v18",
    "phone": "M7 2h10v20H7zM11 18.5h2",
    "offline": "M5 18a4 4 0 0 1 .6-8 6 6 0 0 1 11.2-1.6A3.5 3.5 0 0 1 19 18M3 3l18 18",
    "swipe": "M7 12h10m0 0-3-3m3 3-3 3M4 6v12M20 6v12",
    "list": "M4 6h16M4 12h16M4 18h10",
    "chart": "M4 20V10M10 20V4M16 20v-7M22 20H2",
    "lock": "M6 11h12v10H6zM9 11V7a3 3 0 0 1 6 0v4",
    "print": "M7 8V3h10v5M7 18H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2M7 15h10v6H7z",
    "moon": "M20 14a8 8 0 1 1-9.9-9.7A6.5 6.5 0 0 0 20 14Z",
}

def logo(uid):
    """Logo chèn hai chỗ nên gradient phải có id riêng — trùng id thì HTML
    không hợp lệ và trình duyệt chỉ nhận định nghĩa đầu tiên."""
    return LOGO.replace('"lg"', f'"lg-{uid}"').replace("url(#lg)", f"url(#lg-{uid})")


LOGO = ('<svg class="logo" viewBox="0 0 32 32" width="26" height="26" aria-hidden="true">'
        '<defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#f0575e"/><stop offset="1" stop-color="#c9252c"/>'
        '</linearGradient></defs>'
        '<path d="M8 9h16l-1.6 15.2A3 3 0 0 1 19.4 27h-6.8a3 3 0 0 1-3-2.8z" '
        'fill="url(#lg)"/><path d="M11.5 9V6.5a4.5 4.5 0 0 1 9 0V9" fill="none" '
        'stroke="#fcd34d" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M10.4 16h11.2" stroke="rgba(255,255,255,.45)" stroke-width="1.6" '
        'stroke-linecap="round"/></svg>')


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


def qr_svg(size=25):
    """Vẽ hoạ tiết giống mã QR. KHÔNG phải mã quét được — đây là minh hoạ, và
    nhúng một mã thật trỏ vào tài khoản ngân hàng nào đó mới là chuyện sai.
    Dùng bộ sinh số tuyến tính cho ra hoạ tiết cố định, không dùng random để
    mỗi lần dựng lại không ra một hình khác."""
    seed = 20260803
    cells = []

    def rnd():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        return seed / 0x7FFFFFFF

    def in_finder(x, y):
        for fx, fy in ((0, 0), (size - 7, 0), (0, size - 7)):
            if fx <= x < fx + 7 and fy <= y < fy + 7:
                return True
        return False

    for y in range(size):
        for x in range(size):
            if in_finder(x, y):
                continue
            if rnd() > .53:
                cells.append(f"M{x} {y}h1v1h-1z")
    for fx, fy in ((0, 0), (size - 7, 0), (0, size - 7)):
        cells.append(f"M{fx} {fy}h7v7h-7zM{fx+1} {fy+1}v5h5v-5z"
                     f"M{fx+2} {fy+2}h3v3h-3z")
    return (f'<svg class="qr" viewBox="0 0 {size} {size}" aria-hidden="true">'
            f'<path d="{"".join(cells)}" fill="#0c0a09" fill-rule="evenodd"/></svg>')


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0c0a09; --panel:#161211; --panel-2:#1d1817; --line:#2a2221; --line-2:#3a2e2c;
  --text:#fafaf9; --muted:#a8a29e; --dim:#89817c;
  --brand:#e8434a; --brand-deep:#c9252c; --amber:#fcd34d; --ok:#4ade80;
  --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
svg{display:block}
.wrap{width:min(1120px,100% - 2.5rem);margin-inline:auto}
h1,h2,h3{letter-spacing:-.025em}
:focus-visible{outline:2px solid var(--amber);outline-offset:3px;border-radius:6px}

/* ---------- dải thông báo + điều hướng ---------- */
.ticker{background:linear-gradient(90deg,rgba(201,37,44,.2),rgba(252,211,77,.08));
  border-bottom:1px solid var(--line);font-size:.8rem;color:var(--muted);
  text-align:center;padding:.5rem 1rem}
.ticker b{color:#ffb4b8;font-weight:700}
.bar{position:sticky;top:0;z-index:50;padding:.7rem 0;
  background:rgba(12,10,9,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.bar-in{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  width:min(1120px,100% - 2.5rem);margin-inline:auto}
.brand{display:inline-flex;align-items:center;gap:.6rem;min-height:44px;
  font-weight:800;font-size:.95rem;text-decoration:none}
.brand .logo{flex-shrink:0;transition:transform .4s var(--ease)}
.brand:hover .logo{transform:rotate(-8deg) scale(1.08)}
.bar-links{display:flex;align-items:center;gap:.35rem}
.bar-links a{padding:.5rem .8rem;font-size:.85rem;color:var(--muted);text-decoration:none;
  border-radius:8px;transition:color .25s var(--ease),background .25s var(--ease)}
.bar-links a:hover{color:var(--text);background:var(--panel)}
.bar-cta{display:inline-flex;align-items:center;gap:.5rem;padding:.55rem 1.05rem;
  border-radius:999px;border:1px solid var(--line-2);background:var(--panel);
  font-size:.85rem;font-weight:700;text-decoration:none;color:var(--text)!important;
  transition:border-color .25s var(--ease),transform .25s var(--ease),background .25s var(--ease)}
.bar-cta:hover{border-color:var(--brand);transform:translateY(-1px)}

/* ---------- hero ---------- */
.hero{position:relative;padding:clamp(2.5rem,6vw,4.5rem) 0 clamp(2rem,5vw,3rem);overflow:hidden}
.hero::before{content:'';position:absolute;inset:-25% -10% auto -10%;height:130%;z-index:0;
  pointer-events:none;
  background:radial-gradient(44% 40% at 16% 6%,rgba(201,37,44,.24),transparent 70%),
             radial-gradient(38% 34% at 84% 4%,rgba(252,211,77,.09),transparent 70%);
  animation:drift 20s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate3d(2.5%,1.5%,0) scale(1.07)}}
.hero .wrap{position:relative;z-index:1}
.hero-grid{display:grid;gap:clamp(2rem,5vw,3.5rem);align-items:center;
  grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}
.eyebrow{display:inline-flex;align-items:center;gap:.6rem;font-size:.74rem;font-weight:800;
  letter-spacing:.14em;text-transform:uppercase;color:#ffb4b8;margin:0 0 1.1rem;
  padding:.35rem .9rem .35rem .65rem;border:1px solid rgba(232,67,74,.3);border-radius:999px;
  background:rgba(201,37,44,.1)}
/* Vòng nhịp bằng transform trên lớp giả — animate box-shadow buộc vẽ lại. */
.dot{position:relative;width:7px;height:7px;border-radius:50%;background:var(--ok)}
.dot::after{content:'';position:absolute;inset:0;border-radius:50%;
  background:var(--ok);animation:pulse 2.4s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.5}70%,100%{transform:scale(3.4);opacity:0}}
h1{font-size:clamp(2.1rem,5vw,3.4rem);line-height:1.06;font-weight:800;margin:0 0 1.15rem}
h1 .hl{background:linear-gradient(90deg,var(--brand),var(--amber));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.tagline{font-size:clamp(1rem,1.9vw,1.18rem);color:var(--muted);margin:0 0 1.8rem;max-width:52ch}
.actions{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:1rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.85rem 1.5rem;border-radius:14px;
  font-size:.94rem;font-weight:700;text-decoration:none;border:1px solid transparent;
  transform:translateY(var(--lift,0)) scale(var(--press,1));
  transition:transform .25s var(--ease),background .25s var(--ease),
             border-color .25s var(--ease),box-shadow .25s var(--ease)}
.btn:hover{--lift:-2px}
.btn:active{--press:.97}
.btn-primary{background:var(--brand-deep);color:#fff}
.btn-primary:hover{background:var(--brand);box-shadow:0 12px 32px -12px rgba(232,67,74,.75)}
.btn-ghost{background:transparent;border-color:var(--line-2);color:var(--text)}
.btn-ghost:hover{border-color:var(--brand);background:rgba(201,37,44,.09)}
.note-inline{font-size:.82rem;color:var(--dim);margin:0 0 1.6rem}
.hero-facts{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:.85rem;color:var(--dim)}
.hero-facts b{color:var(--text);font-weight:700}

/* ---------- khung điện thoại ---------- */
.phone{width:min(300px,100%);margin-inline:auto;border-radius:34px;padding:9px;
  background:linear-gradient(160deg,#3a2e2c,#181413);
  box-shadow:0 40px 80px -34px rgba(0,0,0,.95);
  animation:mockIn 1s var(--ease) .3s both}
@keyframes mockIn{from{opacity:0;transform:translateY(28px) scale(.96)}to{opacity:1;transform:none}}
.screen{background:#fff;border-radius:26px;overflow:hidden;color:#1c1917;
  font-size:12px;line-height:1.4}
.st-bar{display:flex;justify-content:space-between;align-items:center;
  padding:.45rem .95rem .2rem;font-size:10px;font-weight:800;color:#57534e}
.app-head{display:flex;align-items:center;gap:.5rem;padding:.5rem .8rem .6rem}
.app-head .nm{font-weight:800;font-size:13px;flex:1}
.sync{display:inline-flex;align-items:center;gap:.3rem;font-size:9px;font-weight:800;
  color:#15803d;background:#dcfce7;border-radius:99px;padding:.15rem .45rem}
.sync i{width:5px;height:5px;border-radius:50%;background:#22c55e;
  animation:pulse2 1.8s ease-out infinite}
@keyframes pulse2{50%{opacity:.35}}
.cats{display:flex;gap:.3rem;padding:0 .8rem .6rem;overflow:hidden}
.cat{font-size:9.5px;font-weight:700;padding:.22rem .55rem;border-radius:99px;
  background:#f5f5f4;color:#756e69;white-space:nowrap}
.cat.on{background:#c9252c;color:#fff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;padding:0 .8rem}
.item{border:1px solid #e7e5e4;border-radius:12px;padding:.5rem;text-align:center;
  animation:pop .5s var(--ease) both}
@keyframes pop{from{opacity:0;transform:scale(.9)}to{opacity:1;transform:none}}
.item .em{font-size:19px;line-height:1.2}
.item .nm{font-size:9.5px;font-weight:700;margin-top:.15rem;line-height:1.25}
.item .pr{font-size:9.5px;font-weight:800;color:#c9252c;margin-top:.1rem}
.cartbar{margin:.65rem .8rem 0;background:#c9252c;color:#fff;border-radius:13px;
  padding:.5rem .7rem;display:flex;align-items:center;gap:.5rem;font-size:10.5px;
  font-weight:800;animation:slideUp .6s var(--ease) 1s both}
@keyframes slideUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.cartbar .n{background:rgba(255,255,255,.25);border-radius:99px;padding:.05rem .4rem}
.cartbar .go{margin-left:auto}
.nav{display:flex;justify-content:space-around;padding:.55rem .5rem .7rem;margin-top:.6rem;
  border-top:1px solid #e7e5e4}
.nav span{display:flex;flex-direction:column;align-items:center;gap:.15rem;
  font-size:8.5px;font-weight:700;color:#7b746f}
.nav span.on{color:#c9252c}
.nav svg{width:16px;height:16px}

/* ---------- băng công nghệ ---------- */
.marquee{border-block:1px solid var(--line);padding:1.05rem 0;overflow:hidden;
  background:linear-gradient(180deg,#100c0b,#0c0a09)}
.marquee-in{display:flex;width:max-content;animation:slide 40s linear infinite}
.marquee:hover .marquee-in{animation-play-state:paused}
@keyframes slide{to{transform:translateX(-50%)}}
.marquee span{display:inline-flex;align-items:center;gap:.65rem;padding-inline:1.7rem;
  font-size:.93rem;font-weight:700;color:#5f5853;white-space:nowrap;
  transition:color .3s var(--ease)}
.marquee span::before{content:'';width:6px;height:6px;border-radius:50%;
  background:var(--line-2);transition:background .3s var(--ease)}
.marquee span:hover{color:#ffb4b8}
.marquee span:hover::before{background:var(--brand)}

/* ---------- số liệu ---------- */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;
  background:var(--line);border-block:1px solid var(--line)}
.stat{background:var(--bg);padding:1.6rem 1.2rem;text-align:center}
.stat b{display:block;font-size:clamp(1.9rem,4.2vw,2.7rem);line-height:1;font-weight:800;
  background:linear-gradient(90deg,var(--brand),var(--amber));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  font-variant-numeric:tabular-nums}
.stat span{display:block;margin-top:.5rem;font-size:.82rem;color:var(--dim);line-height:1.4}

/* ---------- khối chung ---------- */
section{padding:clamp(3rem,7vw,5rem) 0}
.head{max-width:58ch;margin-bottom:2.4rem}
.kicker{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:var(--brand);margin:0 0 .8rem}
h2{font-size:clamp(1.55rem,3.4vw,2.25rem);line-height:1.2;margin:0 0 .8rem}
.head p{color:var(--muted);margin:0;font-size:1.05rem}

/* ---------- hai giao diện ---------- */
.two{display:grid;gap:1.4rem;grid-template-columns:minmax(0,1fr) minmax(0,1.65fr);
  align-items:end}
.pane{border:1px solid var(--line);border-radius:16px;background:var(--panel);padding:1.1rem}
.pane-lb{display:flex;align-items:center;gap:.5rem;font-size:.78rem;font-weight:800;
  letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-bottom:.9rem}
.pane-lb .ic{width:16px;height:16px;color:var(--brand)}
/* Bản thu nhỏ của giao diện quầy: sidebar cố định + lưới nhiều cột + giỏ bên phải */
.desk{background:#fff;border-radius:12px;overflow:hidden;color:#1c1917;display:grid;
  grid-template-columns:58px 1fr 132px;min-height:250px;font-size:11px}
.side{background:#1c1917;padding:.6rem .35rem;display:flex;flex-direction:column;gap:.45rem;
  align-items:center}
.side i{width:26px;height:26px;border-radius:9px;background:#37312f;display:block}
.side i.on{background:#c9252c}
.deck{padding:.7rem}
.deck-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:.55rem}
.deck-h b{font-size:12px}
.deck-h span{font-size:9.5px;color:#78716c}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem}
.right{background:#fafaf9;border-left:1px solid #e7e5e4;padding:.7rem .6rem;
  display:flex;flex-direction:column}
.right b{font-size:10.5px;letter-spacing:.05em;color:#78716c;text-transform:uppercase}
.line{display:flex;justify-content:space-between;gap:.4rem;font-size:9.5px;margin-top:.45rem;
  line-height:1.35}
.line span:first-child{flex:1;min-width:0}
.tot{margin-top:auto;padding-top:.5rem;border-top:1px dashed #d6d3d1;display:flex;
  justify-content:space-between;font-weight:800;font-size:11px}
.pay{margin-top:.5rem;background:#c9252c;color:#fff;border-radius:9px;text-align:center;
  padding:.35rem;font-size:10px;font-weight:800}

/* ---------- QR ---------- */
.qr-wrap{display:grid;gap:1.4rem;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);
  align-items:center}
.qr-wrap>*{min-width:0}
.qr-card{background:#fff;border-radius:18px;padding:1.1rem;text-align:center;color:#1c1917;
  max-width:250px;margin-inline:auto;box-shadow:0 24px 50px -26px rgba(0,0,0,.9)}
.qr-card .bank{font-size:10px;font-weight:800;letter-spacing:.1em;color:#78716c;
  text-transform:uppercase}
.qr{width:100%;height:auto;margin:.7rem 0 .5rem}
.qr-card .amt{font-size:19px;font-weight:800;color:#c9252c}
.qr-card .desc{font-size:10px;color:#78716c;margin-top:.15rem}
.qr-note{font-size:.78rem;color:var(--dim);margin:.8rem 0 0;text-align:center}

/* ---------- sơ đồ đồng bộ ---------- */
.sync-box{border:1px solid var(--line);border-radius:16px;background:var(--panel);padding:1rem}
.sync-scroll{overflow-x:auto;overscroll-behavior-x:contain}
.sync-box svg{width:100%;height:auto}
.sy-link{fill:none;stroke:var(--line-2);stroke-width:2;stroke-dasharray:5 7;
  animation:dash 1.7s linear infinite}
@keyframes dash{to{stroke-dashoffset:-24}}
.sy-box{fill:var(--panel-2);stroke:var(--line-2);stroke-width:1.5}
.sy-t{fill:var(--text);font-size:14px;font-weight:700;
  font-family:'Plus Jakarta Sans',system-ui,sans-serif}
.sy-s{fill:var(--dim);font-size:11px;font-family:'Plus Jakarta Sans',system-ui,sans-serif}
.sy-e{font-size:17px}
.sy-hint{display:none;margin:.6rem 0 0;font-size:.78rem;color:var(--dim)}
@media (max-width:780px){
  .sync-scroll svg{width:660px;max-width:none}
  .sy-hint{display:block}
}

/* ---------- các bước ---------- */
.steps{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));
  counter-reset:s}
.step{position:relative;padding:1.7rem 1.5rem;border:1px solid var(--line);border-radius:16px;
  background:var(--panel);counter-increment:s;
  transition:border-color .3s var(--ease),transform .3s var(--ease)}
.step:hover{border-color:var(--line-2);transform:translateY(-3px)}
.step::before{content:counter(s,decimal-leading-zero);position:absolute;top:1rem;right:1.2rem;
  font-size:2.6rem;font-weight:800;color:rgba(255,255,255,.05);line-height:1}
.step .ic{width:26px;height:26px;color:var(--brand);margin-bottom:.9rem}
.step h3{font-size:1.05rem;margin:0 0 .5rem}
.step p{margin:0;font-size:.93rem;color:var(--muted)}

/* ---------- tính năng ---------- */
.feats{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr))}
.feat{position:relative;overflow:hidden;padding:1.6rem 1.5rem;border:1px solid var(--line);
  border-radius:16px;background:var(--panel);
  transition:border-color .3s var(--ease),transform .3s var(--ease),background .3s var(--ease)}
.feat::after{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;opacity:0;
  background:radial-gradient(260px circle at var(--mx,50%) var(--my,50%),rgba(232,67,74,.12),transparent 66%);
  transition:opacity .3s var(--ease)}
.feat:hover{border-color:var(--line-2);transform:translateY(-3px);background:var(--panel-2)}
.feat:hover::after{opacity:1}
.feat .ic{width:26px;height:26px;color:var(--brand);margin-bottom:.9rem;
  transition:transform .35s var(--ease)}
.feat:hover .ic{transform:scale(1.12) rotate(-4deg)}
.feat .n{position:absolute;top:1.3rem;right:1.4rem;font-size:.7rem;font-weight:800;
  letter-spacing:.1em;color:rgba(255,255,255,.12)}
.feat h3{font-size:1.03rem;margin:0 0 .5rem}
.feat p{margin:0;font-size:.92rem;color:var(--muted)}

/* ---------- công nghệ ---------- */
.chips{display:flex;flex-wrap:wrap;gap:.5rem}
.chip{padding:.45rem 1rem;border-radius:10px;font-size:.85rem;font-weight:600;
  background:var(--panel);border:1px solid var(--line);color:var(--muted);
  transition:color .25s var(--ease),border-color .25s var(--ease),transform .25s var(--ease)}
.chip:hover{color:var(--text);border-color:var(--brand);transform:translateY(-2px)}

/* ---------- giới hạn ---------- */
.limits{border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:16px;
  background:var(--panel);padding:1.9rem 1.8rem}
.limit{padding:1.1rem 0;border-top:1px solid var(--line)}
.limit:first-of-type{border-top:0;padding-top:0}
.limit h3{font-size:1rem;margin:0 0 .4rem;color:var(--amber)}
.limit p{margin:0;font-size:.93rem;color:var(--muted)}

/* ---------- FAQ ---------- */
.faq{display:grid;gap:.6rem;max-width:74ch}
details{border:1px solid var(--line);border-radius:14px;background:var(--panel);
  transition:border-color .25s var(--ease)}
details[open]{border-color:var(--line-2)}
summary{cursor:pointer;list-style:none;padding:1.05rem 1.3rem;font-weight:700;font-size:.97rem;
  display:flex;align-items:center;justify-content:space-between;gap:1rem}
summary::-webkit-details-marker{display:none}
summary::after{content:'';width:9px;height:9px;flex-shrink:0;
  border-right:2px solid var(--dim);border-bottom:2px solid var(--dim);
  transform:rotate(45deg) translateY(-2px);transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(-135deg) translateY(-2px);border-color:var(--brand)}
details p{margin:0;padding:0 1.3rem 1.15rem;color:var(--muted);font-size:.93rem}

/* ---------- kết ---------- */
.cta{text-align:center;border-top:1px solid var(--line)}
.cta h2{margin-bottom:.8rem}
.cta p{color:var(--muted);max-width:52ch;margin:0 auto 2rem}
.cta .actions{justify-content:center;margin-bottom:0}
footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--dim);font-size:.85rem}
.foot-in{display:flex;flex-wrap:wrap;gap:1rem;justify-content:space-between;align-items:center}
.foot-brand{display:flex;align-items:center;gap:.6rem;color:var(--muted);font-weight:700}
footer a{display:inline-block;padding:.5rem .15rem;color:var(--muted);text-decoration:none;
  transition:color .25s var(--ease)}
footer a:hover{color:var(--brand)}

/* ---------- chuyển động ---------- */
.rise{opacity:0;transform:translateY(24px);
  transition:opacity .75s var(--ease),transform .75s var(--ease)}
.rise.in{opacity:1;transform:none}
.hero .eyebrow,.hero h1,.hero .tagline,.hero .actions,.hero .note-inline,.hero .hero-facts{
  opacity:0;animation:riseIn .85s var(--ease) forwards}
.hero .eyebrow{animation-delay:.05s}
.hero h1{animation-delay:.13s}
.hero .tagline{animation-delay:.22s}
.hero .actions{animation-delay:.31s}
.hero .note-inline{animation-delay:.37s}
.hero .hero-facts{animation-delay:.43s}
@keyframes riseIn{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.progress{position:fixed;top:0;left:0;height:2px;width:100%;z-index:60;transform:scaleX(0);
  transform-origin:0 50%;background:linear-gradient(90deg,var(--brand),var(--amber))}
@supports (animation-timeline:scroll()){
  .progress{animation:grow linear;animation-timeline:scroll(root block)}
  @keyframes grow{to{transform:scaleX(1)}}
}

@media (max-width:980px){
  .two{grid-template-columns:1fr}
}
@media (max-width:900px){
  .hero-grid,.qr-wrap{grid-template-columns:1fr}
  .bar-links{display:none}
}
@media (max-width:640px){
  .actions{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .limits{padding:1.4rem 1.25rem}
  .desk{grid-template-columns:44px 1fr}
  .desk .right{display:none}
}
"""

JS = """
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -10% 0px',threshold:.08});
document.querySelectorAll('.rise').forEach(function(el,i){
  el.style.transitionDelay=(Math.min(i%6,5)*55)+'ms'; io.observe(el);
});

// Số liệu đếm lên theo thời gian thật chứ không theo số khung hình, nên máy
// yếu vẫn dừng đúng lúc.
var cio=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting) return;
    cio.unobserve(e.target);
    var el=e.target, to=+el.dataset.to, suf=el.dataset.suffix||'', t0=0, dur=1100;
    if(!to){ el.textContent='0'+suf; return; }
    requestAnimationFrame(function step(t){
      if(!t0) t0=t;
      var p=Math.min((t-t0)/dur,1), e2=1-Math.pow(1-p,3);
      el.textContent=Math.round(to*e2)+suf;
      if(p<1) requestAnimationFrame(step);
    });
  });
},{threshold:.5});
document.querySelectorAll('[data-to]').forEach(function(el){ cio.observe(el); });

var pend=null,fr=0;
if(matchMedia('(pointer:fine)').matches){
  document.querySelectorAll('.feat').forEach(function(c){
    c.addEventListener('pointermove',function(ev){
      pend=[c,ev];
      if(!fr) fr=requestAnimationFrame(function(){
        fr=0; if(!pend) return;
        var el=pend[0],e=pend[1],r=el.getBoundingClientRect();
        el.style.setProperty('--mx',(e.clientX-r.left)+'px');
        el.style.setProperty('--my',(e.clientY-r.top)+'px');
      });
    });
  });
}
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


SY_NODES = [
    (20, 60, 170, 62, "Giao diện", "React 19 · Tailwind", "📱"),
    (250, 60, 170, 62, "IndexedDB", "ghi ngay, kể cả offline", "💾"),
    (250, 168, 170, 62, "Worker nền", "đẩy lên khi có mạng", "🔄"),
    (480, 114, 170, 62, "Apps Script", "10 service", "⚙️"),
    (700, 114, 160, 62, "Google Sheets", "database", "📊"),
]
SY_LINKS = ["M190 91 L250 91", "M335 122 L335 168", "M420 199 C450 199 450 145 480 145",
            "M420 91 C450 91 450 145 480 145", "M650 145 L700 145"]


def sync_svg():
    parts = ['<svg viewBox="0 0 880 260" role="img" aria-label="Sơ đồ đồng bộ: '
             'giao diện ghi vào IndexedDB, worker nền đẩy lên Apps Script, dữ liệu '
             'nằm trong Google Sheets">']
    for i, d in enumerate(SY_LINKS):
        parts.append(f'<path class="sy-link" d="{d}" style="animation-delay:{i * .2:.2f}s"/>')
    for x, y, w, h, t, s, em in SY_NODES:
        parts.append(
            f'<g><rect class="sy-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="13"/>'
            f'<text class="sy-e" x="{x + 15}" y="{y + 38}">{em}</text>'
            f'<text class="sy-t" x="{x + 45}" y="{y + 27}">{esc(t)}</text>'
            f'<text class="sy-s" x="{x + 45}" y="{y + 45}">{esc(s)}</text></g>')
    return "".join(parts) + "</svg>"


def build():
    title = "Tiệm Nước Nhỏ POS — phần mềm bán hàng cho quán nước"
    # Dưới 160 ký tự — Google cắt ở khoảng đó.
    desc = ("Phần mềm bán hàng cho quán nước, chạy trên điện thoại lẫn quầy thu ngân. "
            "Database là một file Google Sheets, chi phí máy chủ bằng không.")

    one = "".join(f"<span>{esc(t)}</span>" for t in STACK)
    stats = "".join(
        f'<div class="stat"><b data-to="{n}" data-suffix="{esc(suf)}">0{esc(suf)}</b>'
        f'<span>{esc(lab)}</span></div>' for n, suf, lab in STATS)
    steps = "".join(
        f'<article class="step rise">{icon(ic)}<h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for ic, t, d in STEPS)
    feats = "".join(
        f'<article class="feat rise"><span class="n">{i:02d}</span>{icon(ic)}'
        f'<h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (ic, t, d) in enumerate(FEATURES, 1))
    limits = "".join(
        f'<div class="limit"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in LIMITS)
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))
    chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in STACK)

    menu = "".join(
        f'<div class="item" style="animation-delay:{.5 + i * .07:.2f}s">'
        f'<div class="em">{em}</div><div class="nm">{esc(n)}</div>'
        f'<div class="pr">{p}đ</div></div>'
        for i, (em, n, p) in enumerate(MENU[:4]))
    menu3 = "".join(
        f'<div class="item" style="animation-delay:{.5 + i * .06:.2f}s">'
        f'<div class="em">{em}</div><div class="nm">{esc(n)}</div>'
        f'<div class="pr">{p}đ</div></div>'
        for i, (em, n, p) in enumerate(MENU))
    cart = "".join(
        f'<div class="line"><span>{esc(n)} ×{q}</span><span>{p}</span></div>'
        for n, q, p in CART)

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareApplication", "name": "Tiệm Nước Nhỏ POS",
             "applicationCategory": "BusinessApplication",
             "operatingSystem": "Web", "description": desc, "url": SITE + "/",
             "image": SITE + "/cover.jpg",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "VND"},
             "featureList": [t for _, t, _ in FEATURES],
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "SoftwareSourceCode", "name": "Tiệm Nước Nhỏ POS",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": ["TypeScript", "React", "Google Apps Script"]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        app=APP, css=CSS, js=JS, jsonld=jsonld,
        logo=logo('a'), logo2=logo('b'), marquee=one + one,
        stats=stats, steps=steps, feats=feats, limits=limits, faq=faq, chips=chips,
        menu=menu, menu3=menu3, cart=cart, qr=qr_svg(), sync=sync_svg(),
        n_components=N_COMPONENTS, n_services=N_SERVICES,
        i_phone=icon("phone"), i_list=icon("list"))


PAGE = Template("""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>$title</title>
<meta name="description" content="$desc" />
<meta name="author" content="Hà Đình Long" />
<meta name="theme-color" content="#0c0a09" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><path d='M8 9h16l-1.6 15.2A3 3 0 0 1 19.4 27h-6.8a3 3 0 0 1-3-2.8z' fill='%23c9252c'/><path d='M11.5 9V6.5a4.5 4.5 0 0 1 9 0V9' fill='none' stroke='%23fcd34d' stroke-width='2'/></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Tiệm Nước Nhỏ POS" />
<meta property="og:title" content="$title" />
<meta property="og:description" content="$desc" />
<meta property="og:url" content="$site/" />
<meta property="og:image" content="$site/cover.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="600" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="$title" />
<meta name="twitter:description" content="$desc" />
<meta name="twitter:image" content="$site/cover.jpg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300..800&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>

<div class="ticker">Đang chạy thật tại một quán nước · <b>React 19</b> · database là <b>một file Google Sheets</b></div>

<nav class="bar">
  <div class="bar-in">
    <a class="brand" href="#top">$logo Tiệm Nước Nhỏ POS</a>
    <div class="bar-links">
      <a href="#giao-dien">Giao diện</a>
      <a href="#thanh-toan">Thanh toán</a>
      <a href="#dong-bo">Đồng bộ</a>
      <a href="#tinh-nang">Tính năng</a>
      <a href="#hoi-dap">Hỏi đáp</a>
    </div>
    <a class="bar-cta" href="https://github.com/$repo" target="_blank" rel="noopener">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>
      Mã nguồn
    </a>
  </div>
</nav>

<header class="hero" id="top">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow"><span class="dot"></span> Ứng dụng đang chạy thật</p>
      <h1>Phần mềm bán hàng cho quán nước, <span class="hl">không tốn đồng máy chủ nào</span></h1>
      <p class="tagline">
        Nhân viên order bằng điện thoại, thu ngân dùng máy tính, chủ quán xem doanh thu
        ngay trong Google Sheets. Cùng một mã nguồn, không có máy chủ nào để trả tiền.
      </p>
      <div class="actions">
        <a class="btn btn-primary" href="https://github.com/$repo" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
        <a class="btn btn-ghost" href="$app">Mở ứng dụng thật ↗</a>
      </div>
      <p class="note-inline">Ứng dụng thật cần tài khoản của quán — mở ra sẽ thấy màn hình đăng nhập. Giao diện thì xem ngay bên đây.</p>
      <div class="hero-facts">
        <span><b>$n_components</b> component React</span>
        <span><b>$n_services</b> service backend</span>
        <span><b>0đ</b> hạ tầng</span>
      </div>
    </div>

    <!-- Toàn bộ mockup vẽ bằng HTML/CSS: repo không có ảnh chụp nào, mà ảnh
         chụp cũng sẽ lệch với bản thật ngay lần cập nhật đầu. Màu và phông
         lấy đúng từ ứng dụng đang chạy. -->
    <div class="phone" role="img" aria-label="Minh hoạ giao diện điện thoại: lưới món uống, thanh giỏ hàng và thanh điều hướng dưới đáy">
      <div class="screen">
        <div class="st-bar"><span>19:04</span><span>▮▮▮ 84%</span></div>
        <div class="app-head">
          <span class="nm">Tiệm Nước Nhỏ</span>
          <span class="sync"><i></i> ĐÃ ĐỒNG BỘ</span>
        </div>
        <div class="cats">
          <span class="cat on">Tất cả</span><span class="cat">Trà sữa</span>
          <span class="cat">Cà phê</span><span class="cat">Đá xay</span>
        </div>
        <div class="grid2">$menu</div>
        <div class="cartbar"><span class="n">3</span> món · 87.000đ <span class="go">Thanh toán ›</span></div>
        <div class="nav">
          <span class="on">$i_phone Bán</span>
          <span>$i_list Đơn</span>
          <span>$i_phone Kho</span>
          <span>$i_list Sổ</span>
        </div>
      </div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="marquee-in">$marquee</div></div>

<div class="stats">$stats</div>

<main>
  <section class="wrap" id="giao-dien">
    <div class="head">
      <p class="kicker rise">Hai giao diện</p>
      <h2 class="rise">Một mã nguồn, hai cách dùng khác hẳn nhau</h2>
      <p class="rise">Không phải một giao diện co giãn cho vừa màn hình. Dưới ngưỡng bề rộng là thanh điều hướng đáy cho nhân viên cầm điện thoại; trên ngưỡng đó tự mở thành sidebar cố định và lưới nhiều cột cho quầy thu ngân đứng yên một chỗ.</p>
    </div>
    <div class="two">
      <div class="pane rise">
        <div class="pane-lb">$i_phone Điện thoại · một ngón tay</div>
        <div class="screen" style="border-radius:12px">
          <div class="app-head"><span class="nm">Bán hàng</span><span class="sync"><i></i> LIVE</span></div>
          <div class="cats"><span class="cat on">Tất cả</span><span class="cat">Trà sữa</span><span class="cat">Cà phê</span></div>
          <div class="grid2">$menu</div>
          <div class="cartbar"><span class="n">3</span> món · 87.000đ <span class="go">›</span></div>
          <div class="nav"><span class="on">$i_phone Bán</span><span>$i_list Đơn</span><span>$i_phone Kho</span><span>$i_list Sổ</span></div>
        </div>
      </div>
      <div class="pane rise">
        <div class="pane-lb">$i_list Quầy thu ngân · nhiều cột</div>
        <div class="desk">
          <div class="side"><i class="on"></i><i></i><i></i><i></i><i></i></div>
          <div class="deck">
            <div class="deck-h"><b>Thực đơn</b><span>6 món đang bán</span></div>
            <div class="grid3">$menu3</div>
          </div>
          <div class="right">
            <b>Đơn #1042</b>
            $cart
            <div class="tot"><span>Tổng</span><span>89.000đ</span></div>
            <div class="pay">Thanh toán</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap" id="thanh-toan">
    <div class="head">
      <p class="kicker rise">Thanh toán</p>
      <h2 class="rise">Khách quét mã, không ai phải gõ lại số tiền</h2>
    </div>
    <div class="qr-wrap rise">
      <div>
        <div class="qr-card">
          <div class="bank">Chuyển khoản · VietQR</div>
          $qr
          <div class="amt">89.000đ</div>
          <div class="desc">TIEMNUOCNHO 1042</div>
        </div>
        <p class="qr-note">Hình minh hoạ — không phải mã quét được</p>
      </div>
      <div>
        <p style="color:var(--muted);margin:0 0 1rem">
          Mã sinh động theo từng đơn bằng thư viện VietQR: số tiền và nội dung chuyển khoản
          điền sẵn, khách chỉ mở app ngân hàng lên quét. Không phải in mã cố định rồi ngồi
          đọc số tiền cho khách gõ tay — thao tác dễ sai nhất ở quầy vào giờ cao điểm.
        </p>
        <div class="chips">
          <span class="chip">Đúng chuẩn VietQR</span>
          <span class="chip">Số tiền điền sẵn</span>
          <span class="chip">Nội dung theo mã đơn</span>
          <span class="chip">In hoặc xuất ảnh gửi Zalo</span>
        </div>
      </div>
    </div>
  </section>

  <section class="wrap" id="dong-bo">
    <div class="head">
      <p class="kicker rise">Kiến trúc</p>
      <h2 class="rise">Mất mạng giữa giờ cao điểm vẫn bán được</h2>
      <p class="rise">Đơn không đi thẳng lên mạng. Nó ghi vào IndexedDB ngay trong trình duyệt trước, rồi một worker nền mới đẩy lên khi có mạng lại — kèm bộ giải xung đột cho trường hợp hai máy cùng sửa một đơn.</p>
    </div>
    <div class="sync-box rise">
      <div class="sync-scroll">$sync</div>
      <p class="sy-hint">↔ Vuốt ngang để xem hết sơ đồ</p>
    </div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Ba bước</p>
      <h2 class="rise">Một đơn hàng đi qua những đâu</h2>
    </div>
    <div class="steps">$steps</div>
  </section>

  <section class="wrap" id="tinh-nang">
    <div class="head">
      <p class="kicker rise">Tính năng</p>
      <h2 class="rise">Những gì có trong bản đang chạy</h2>
    </div>
    <div class="feats">$feats</div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Công nghệ</p>
      <h2 class="rise">Dựng bằng gì</h2>
    </div>
    <div class="chips rise">$chips</div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Nói trước cho rõ</p>
      <h2 class="rise">Ba giới hạn bạn nên biết</h2>
      <p class="rise">Đây là hệ thống làm cho một quán cụ thể, không phải sản phẩm bán đại trà. Nói thẳng thì đỡ mất thời gian của cả hai bên.</p>
    </div>
    <div class="limits rise">$limits</div>
  </section>

  <section class="wrap" id="hoi-dap">
    <div class="head">
      <p class="kicker rise">Hỏi đáp</p>
      <h2 class="rise">Câu hỏi thường gặp</h2>
    </div>
    <div class="faq">$faq</div>
  </section>

  <section class="wrap cta">
    <h2 class="rise">Mã nguồn mở, cả frontend lẫn backend</h2>
    <p class="rise">Toàn bộ nằm trên GitHub — phần React và phần Apps Script chạy trên Google Sheets.</p>
    <div class="actions rise">
      <a class="btn btn-primary" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
      <a class="btn btn-ghost" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot-in">
    <span class="foot-brand">$logo2 Tiệm Nước Nhỏ POS</span>
    <span>© 2026 Hà Đình Long — Long Leo</span>
    <span><a href="$portfolio/">Portfolio</a> · <a href="https://github.com/$repo" target="_blank" rel="noopener">GitHub</a></span>
  </div>
</footer>

<script>$js</script>
</body>
</html>
""")


def main():
    d = os.path.join(OUT, "landing")
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "tiem-nuoc-nho.jpg"),
                    os.path.join(d, "cover.jpg"))
    print(f"  {len(html) // 1024} KB  landing/index.html")
    print(f"  {len(FEATURES)} tính năng · {len(STEPS)} bước · {len(FAQ)} câu hỏi · "
          f"{len(LIMITS)} giới hạn · {len(STACK)} công nghệ")
    print(f"  mockup: điện thoại, quầy thu ngân, QR, sơ đồ đồng bộ {len(SY_NODES)} khối")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
