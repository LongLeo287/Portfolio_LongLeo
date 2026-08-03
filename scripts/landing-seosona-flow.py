#!/usr/bin/env python3
"""Landing page riêng cho SEOSONA Flow — không dùng mẫu chung.

Năm dự án kia dùng một khuôn: hero, ảnh bìa, vấn đề, thẻ tính năng, CTA. Khuôn
đó đủ cho một repo hạ tầng, nhưng SEOSONA Flow là phần mềm có người dùng thật,
nên trang của nó cần *cho xem* sản phẩm chứ không chỉ tả bằng chữ.

Bố cục học từ labs.toby.vn — sản phẩm cùng loại, trang bán hàng của họ làm tốt.
Giao diện thì giữ nhận diện tối/amber của SEOSONA, không mượn hình thức của họ.

Ba loại hình ảnh trên trang, mỗi loại một lý do:
  1. Mockup vẽ bằng HTML/CSS/SVG — side panel, sơ đồ workflow, Image-to-Prompt.
     Ảnh chụp màn hình sẽ lệch với bản thật ngay lần cập nhật đầu tiên; mockup
     sửa được như sửa văn bản và không tốn byte tải về.
  2. Ảnh thật do chính extension sinh ra — 12 tấm lấy từ assets/templates của
     repo, xem scripts/landing-seosona-flow-assets.py.
  3. Icon và logo vẽ bằng SVG nội tuyến — không gọi thư viện icon nào.

    python scripts/landing-seosona-flow-assets.py   # ảnh trước
    python scripts/landing-seosona-flow.py          # rồi tới trang

Mọi con số trên trang đọc từ chính repo seosona-flow (manifest.json,
node-catalog.json, BundledPrompts.js) — sửa thì kiểm lại nguồn.
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "seosona-flow")
SITE = "https://seosona-flow.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/seosona-flow"

# --- số liệu, tất cả lấy từ repo ---
VERSION = "1.1.37"          # manifest.json
N_NODES = 26                # src/workflow/framework/node-catalog.json
N_PROMPTS = 410             # src/prompts/BundledPrompts.js
N_TEMPLATES = 88            # assets/templates/thumb_*.png
N_PLATFORMS = 4             # host_permissions

PROVIDERS = ["Google Flow", "ChatGPT", "Gemini", "Grok", "Veo 3.1",
             "Nano Banana", "Imagen", "Sora", "Claude"]

STATS = [
    (N_PLATFORMS, "", "nền tảng AI điều khiển được"),
    (N_NODES, "", "loại node dựng workflow"),
    (N_PROMPTS, "", "prompt và skill đóng gói sẵn"),
    (N_TEMPLATES, "", "mẫu có ảnh xem trước"),
    (0, "đ", "phí API, phí gói, phí tài khoản"),
]

# 26 node gom theo nhóm. Emoji ở đây làm nhãn nhóm — quét mắt nhanh hơn chữ.
NODE_GROUPS = [
    ("🎨", "Sinh nội dung", [
        "Tạo ảnh/video", "AI Agent", "ChatGPT", "Grok", "Image", "Ghép ảnh"]),
    ("🧬", "Giữ nhất quán", [
        "Style Anchor", "Bảng thực thể", "Prompt Sequence", "Variant Expand"]),
    ("🔀", "Điều khiển luồng", [
        "Loop / Batch", "Condition", "Switch", "Merge", "Random Pick", "Cổng chất lượng"]),
    ("📝", "Xử lý chữ", [
        "Text", "Text Template", "Text Extract", "Text Overlay", "Text QA", "Xuất file text"]),
    ("📤", "Đầu ra", [
        "Download", "Telegram", "Wait", "Ghi chú"]),
]

# 7 nhóm trong kho prompt, số liệu đếm từ BundledPrompts.js
PROMPT_GROUPS = [
    ("🖼️", "Image/Video Prompting", 290),
    ("✍️", "Content Creation", 49),
    ("🎬", "Video Prompting", 25),
    ("🤖", "Agent Skills / Prompt Ops", 18),
    ("📣", "Ad Video", 15),
    ("🔍", "SEO / Marketing", 9),
    ("📦", "Product Photo", 4),
]

STEPS = [
    ("login", "Đăng nhập sẵn",
     "Mở và đăng nhập những trang bạn định dùng — Google Flow, ChatGPT, Gemini, Grok. "
     "Extension không kèm tài khoản nào, nó mượn đúng phiên đăng nhập của bạn."),
    ("paste", "Dán prompt hàng loạt",
     "Bấm icon, side panel mở bên phải. Dán cả danh sách prompt, chọn model, tỉ lệ khung "
     "hình, số lượng. Alt+S mở panel, Alt+G chạy ngay."),
    ("run", "Bấm chạy rồi làm việc khác",
     "Extension tự gõ prompt vào tab provider, chờ kết quả, tải file về theo đúng mẫu tên "
     "bạn đặt — 1K, 2K hay 4K. Panel hiện tiến độ từng job."),
]

FEATURES = [
    ("layers", "Chạy prompt theo lô",
     "Nhập một lúc hàng chục prompt, chạy tuần tự hoặc song song. Có humanized delay, "
     "giới hạn đồng thời và tự thử lại khi lỗi."),
    ("nodes", f"Workflow {N_NODES} loại node",
     "Kéo thả dựng chuỗi xử lý: tạo ảnh, ghép, kiểm chất lượng, gắn chữ, tải về, "
     "báo Telegram — chạy một mạch không cần ngồi canh."),
    ("i2p", "Ảnh ra prompt",
     "Chuột phải ảnh bất kỳ trên web, chọn vùng màn hình, hoặc tải ảnh từ máy. Gemini hoặc "
     "ChatGPT phân tích thành prompt, xuất ba dạng JSON / English / Tiếng Việt."),
    ("download", "Tự tải kết quả",
     "Ảnh và video tự lưu theo mẫu tên file bạn đặt, phân thư mục khớp với dự án. "
     "Không phải ngồi bấm tải từng cái."),
    ("grid", f"{N_PLATFORMS} nền tảng, một chỗ",
     "Mỗi trang một adapter riêng. Extension tự tìm tab provider đang đăng nhập, hoặc mở "
     "tab mới nếu chưa có."),
    ("panel", "Side panel, không popup",
     "Chạy ở khung bên phải trình duyệt nên tab chính vẫn dùng bình thường. Popup thì "
     "bấm ra ngoài là mất, panel thì không."),
    ("pack", f"{N_PROMPTS} prompt dựng sẵn",
     "Kho prompt và skill đóng gói ngay trong extension, chia bảy nhóm và xếp hạng. "
     "Hoàn toàn ngoại tuyến, không gọi mạng."),
    ("shield", "Chạy cục bộ mặc định",
     "Cấu hình, lịch sử và hạn mức đều nằm trong máy. Tầng gọi mạng ra backend bị chặn "
     "ngay trong mã nguồn, không phải bằng thiết lập."),
    ("wrench", "Sửa được khi trang AI đổi giao diện",
     "Có hệ thống selector override: chỉnh bằng cấu hình chứ không phải chờ bản vá, và "
     "bộ chẩn đoán tự báo selector nào hỏng."),
]

LIMITS = [
    ("Bám vào giao diện thật của bốn trang AI",
     "Đây không phải API — extension điều khiển DOM. Khi Google hay OpenAI đổi giao diện, "
     "thao tác có thể hỏng. Có sẵn selector override để sửa mà không cần đụng mã nguồn."),
    ("Image-to-Prompt chỉ chạy với Gemini và ChatGPT",
     "Hai trang này là những nơi duy nhất tải ảnh lên được qua content script. Grok và "
     "Claude không dùng cho tính năng đó."),
    ("Tiêu quota của chính tài khoản bạn",
     "Extension không tặng credit. Mỗi prompt trừ vào gói bạn đang trả cho Google, OpenAI "
     "hay xAI — đúng như khi bạn tự gõ tay."),
]

FAQ = [
    ("Có phải trả tiền API không?",
     "Không. Extension không gọi API tính phí nào — nó điều khiển phiên đăng nhập sẵn có "
     "của bạn trong trình duyệt, nên chi phí đúng bằng gói bạn đang dùng."),
    ("Dữ liệu của tôi có bị gửi đi đâu không?",
     "Không. Chế độ cục bộ là mặc định: mọi cấu hình, lịch sử và hạn mức đều lưu trong "
     "máy, và tầng gọi mạng ra backend bị chặn ngay trong mã nguồn."),
    ("Cài đặt có phức tạp không?",
     "Không có bước build. Tải repo về, vào chrome://extensions, bật Developer mode, "
     "Load unpacked rồi chọn thư mục seosona-flow — thư mục con chứa manifest.json, "
     "không phải thư mục gốc."),
    ("Có cần npm install không?",
     "Không. Thư viện đã đóng gói sẵn trong repo, mã nguồn nạp thẳng vào Chrome."),
    ("Giao diện tiếng Việt hay tiếng Anh?",
     "Cả hai, đổi ngay trong panel."),
    ("Nếu ChatGPT đổi giao diện thì sao?",
     "Thao tác có thể hỏng — đó là đánh đổi của cách làm không dùng API. Bù lại có hệ "
     "thống selector override: sửa bằng cấu hình, không phải chờ bản vá."),
]

# --- icon SVG nội tuyến, 24×24, nét 1.7 ---
ICONS = {
    "layers": "M12 3 3 8l9 5 9-5-9-5ZM3 13l9 5 9-5M3 17.5l9 5 9-5",
    "nodes": "M6 5h4v4H6zM14 15h4v4h-4zM14 5h4v4h-4zM10 7h4M8 9v6h6M6 15h4v4H6z",
    "i2p": "M3 5h10v9H3zM6 11l2.5-3 2 2.5 1.5-2 1 2.5M17 8h4M19 6v4M15 17h6m-3-2v4",
    "download": "M12 3v11m0 0 4-4m-4 4-4-4M4 18v2h16v-2",
    "grid": "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z",
    "panel": "M3 4h18v16H3zM15 4v16M17.5 9h2M17.5 12h2M17.5 15h2",
    "pack": "M4 7 12 3l8 4v10l-8 4-8-4zM4 7l8 4 8-4M12 11v10",
    "shield": "M12 3 5 6v6c0 4 3 7 7 9 4-2 7-5 7-9V6zM9 12l2 2 4-4",
    "wrench": "M15 3a5 5 0 0 0-4.6 7L3 17.4 6.6 21l7.4-7.4A5 5 0 0 0 21 9l-3 3-3-3 3-3a5 5 0 0 0-3-3Z",
    "login": "M15 3h4v18h-4M10 8l4 4-4 4M14 12H3",
    "paste": "M9 4h6v3H9zM7 5H5v16h14V5h-2M8 12h8M8 16h5",
    "run": "M8 5v14l11-7z",
}

def logo(uid):
    """Logo chèn hai chỗ nên gradient phải có id riêng — trùng id thì HTML
    không hợp lệ và trình duyệt chỉ nhận định nghĩa đầu tiên."""
    return LOGO.replace('"lg"', f'"lg-{uid}"').replace("url(#lg)", f"url(#lg-{uid})")


LOGO = ('<svg class="logo" viewBox="0 0 32 32" width="26" height="26" aria-hidden="true">'
        '<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#ff7a00"/><stop offset="1" stop-color="#fcd34d"/>'
        '</linearGradient></defs>'
        '<rect x="1.4" y="1.4" width="29.2" height="29.2" rx="9" fill="none" '
        'stroke="url(#lg)" stroke-width="2"/>'
        '<path d="M18.4 6 9.6 17.6h4.8L12.8 26l9-11.8h-5z" fill="url(#lg)"/></svg>')

# Sơ đồ workflow: toạ độ tuyệt đối trong viewBox nên co giãn theo khung mà
# không lệch. Nét đứt chạy dọc đường nối tạo cảm giác dữ liệu đang đi qua.
WF_NODES = [
    (30, 40, 150, 54, "Prompt", "🎨", 0),
    (30, 168, 150, 54, "Style Anchor", "🧬", 1),
    (250, 104, 170, 54, "Tạo ảnh/video", "⚡", 2),
    (490, 34, 170, 54, "Cổng chất lượng", "✅", 3),
    (490, 174, 170, 54, "Text Overlay", "📝", 3),
    (720, 104, 150, 54, "Download", "📤", 4),
    (720, 232, 150, 54, "Telegram", "📨", 5),
]
WF_LINKS = [
    "M180 67 C215 67 215 131 250 131",
    "M180 195 C215 195 215 131 250 131",
    "M420 131 C455 131 455 61 490 61",
    "M420 131 C455 131 455 201 490 201",
    "M660 61 C690 61 690 131 720 131",
    "M660 201 C690 201 690 131 720 131",
    "M795 158 L795 232",
]


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0c0a09; --panel:#141110; --panel-2:#1a1614; --line:#26211e; --line-2:#332b26;
  --text:#fafaf9; --muted:#a8a29e; --dim:#877f7a;
  --primary:#ff7a00; --amber:#fcd34d; --ok:#4ade80;
  --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
svg{display:block}
.wrap{width:min(1120px,100% - 2.5rem);margin-inline:auto}
h1,h2,h3{letter-spacing:-.022em}
:focus-visible{outline:2px solid var(--amber);outline-offset:3px;border-radius:6px}

/* ---------- dải thông báo + thanh điều hướng ---------- */
.ticker{background:linear-gradient(90deg,rgba(255,122,0,.14),rgba(252,211,77,.09));
  border-bottom:1px solid var(--line);font-size:.8rem;color:var(--muted);
  text-align:center;padding:.5rem 1rem}
.ticker b{color:var(--amber);font-weight:600}
.bar{position:sticky;top:0;z-index:50;padding:.7rem 0;
  background:rgba(12,10,9,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.bar-in{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  width:min(1120px,100% - 2.5rem);margin-inline:auto}
.brand{display:inline-flex;align-items:center;gap:.6rem;min-height:44px;
  font-weight:700;font-size:.95rem;text-decoration:none;letter-spacing:-.01em}
.brand .logo{flex-shrink:0;transition:transform .4s var(--ease)}
.brand:hover .logo{transform:rotate(-8deg) scale(1.08)}
.bar-links{display:flex;align-items:center;gap:.35rem}
.bar-links a{padding:.5rem .8rem;font-size:.85rem;color:var(--muted);text-decoration:none;
  border-radius:8px;transition:color .25s var(--ease),background .25s var(--ease)}
.bar-links a:hover{color:var(--text);background:var(--panel)}
.bar-cta{display:inline-flex;align-items:center;gap:.5rem;padding:.55rem 1.05rem;
  border-radius:999px;border:1px solid var(--line);background:var(--panel);
  font-size:.85rem;font-weight:600;text-decoration:none;color:var(--text)!important;
  transition:border-color .25s var(--ease),transform .25s var(--ease),background .25s var(--ease)}
.bar-cta:hover{border-color:var(--primary);background:var(--panel-2)!important;transform:translateY(-1px)}

/* ---------- hero ---------- */
.hero{position:relative;padding:clamp(2.5rem,6vw,4.5rem) 0 clamp(2rem,5vw,3rem);overflow:hidden}
.hero::before{content:'';position:absolute;inset:-25% -10% auto -10%;height:130%;z-index:0;
  pointer-events:none;
  background:radial-gradient(46% 40% at 14% 6%,rgba(255,122,0,.18),transparent 70%),
             radial-gradient(40% 36% at 86% 2%,rgba(252,211,77,.10),transparent 70%);
  animation:drift 20s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate3d(2.5%,1.5%,0) scale(1.07)}}
.hero .wrap{position:relative;z-index:1}
.hero-grid{display:grid;gap:clamp(2rem,5vw,3.5rem);align-items:center;
  grid-template-columns:minmax(0,1fr) minmax(0,1.05fr)}
.eyebrow{display:inline-flex;align-items:center;gap:.6rem;font-size:.74rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;color:var(--amber);margin:0 0 1.1rem;
  padding:.35rem .9rem .35rem .65rem;border:1px solid rgba(252,211,77,.28);border-radius:999px;
  background:rgba(252,211,77,.06)}
/* Vòng nhịp bằng transform trên lớp giả. Animate box-shadow buộc trình duyệt
   vẽ lại vùng quanh chấm mỗi khung hình. */
.dot{position:relative;width:7px;height:7px;border-radius:50%;background:var(--ok)}
.dot::after{content:'';position:absolute;inset:0;border-radius:50%;
  background:var(--ok);animation:pulse 2.4s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.5}70%,100%{transform:scale(3.4);opacity:0}}
h1{font-size:clamp(2.1rem,5vw,3.5rem);line-height:1.05;font-weight:700;margin:0 0 1.15rem}
h1 .hl{background:linear-gradient(90deg,var(--primary),var(--amber));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.tagline{font-size:clamp(1rem,1.9vw,1.18rem);color:var(--muted);margin:0 0 1.8rem;max-width:52ch}
.actions{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:1.6rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.85rem 1.5rem;border-radius:999px;
  font-size:.94rem;font-weight:600;text-decoration:none;border:1px solid transparent;
  transform:translateY(var(--lift,0)) scale(var(--press,1));
  transition:transform .25s var(--ease),background .25s var(--ease),
             border-color .25s var(--ease),box-shadow .25s var(--ease)}
.btn:hover{--lift:-2px}
.btn:active{--press:.97}
.btn-primary{background:var(--primary);color:#0c0a09}
.btn-primary:hover{box-shadow:0 12px 32px -12px rgba(255,122,0,.7)}
.btn-ghost{background:transparent;border-color:var(--line-2);color:var(--text)}
.btn-ghost:hover{border-color:var(--primary);background:rgba(255,122,0,.07)}
.hero-facts{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:.85rem;color:var(--dim)}
.hero-facts b{color:var(--text);font-weight:600}

/* ---------- mockup chung ---------- */
.mock{border:1px solid var(--line-2);border-radius:16px;overflow:hidden;background:var(--panel);
  box-shadow:0 40px 80px -40px rgba(0,0,0,.95),0 0 0 1px rgba(255,255,255,.02) inset}
.hero .mock{animation:mockIn 1s var(--ease) .35s both}
@keyframes mockIn{from{opacity:0;transform:translateY(28px) scale(.97)}to{opacity:1;transform:none}}
.mock-top{display:flex;align-items:center;gap:.5rem;padding:.7rem .9rem;
  border-bottom:1px solid var(--line);background:var(--panel-2)}
.led{width:10px;height:10px;border-radius:50%;background:#3a322c}
.mock-title{margin-left:.4rem;font-size:.78rem;font-weight:600;color:var(--muted)}
.mock-badge{margin-left:auto;font-size:.68rem;font-weight:700;letter-spacing:.08em;
  color:var(--amber);border:1px solid rgba(252,211,77,.3);border-radius:999px;padding:.15rem .55rem}
.mock-body{padding:.9rem}
.mock-foot{display:flex;justify-content:space-between;font-size:.7rem;color:var(--dim);
  padding:.55rem .9rem;border-top:1px solid var(--line);background:var(--panel-2)}
.chips{display:flex;gap:.4rem;margin-bottom:.85rem;flex-wrap:wrap}
.chip-s{font-size:.72rem;font-weight:600;padding:.32rem .7rem;border-radius:999px;
  border:1px solid var(--line-2);color:var(--dim)}
.chip-s.on{color:#0c0a09;background:var(--amber);border-color:var(--amber)}
.q-head{display:flex;justify-content:space-between;font-size:.7rem;letter-spacing:.1em;
  text-transform:uppercase;color:var(--dim);margin-bottom:.5rem}
.row{display:flex;align-items:center;gap:.6rem;padding:.55rem .65rem;border-radius:9px;
  border:1px solid var(--line);margin-bottom:.35rem;background:#100d0c;font-size:.8rem}
.row .txt{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted)}
.row .st{font-size:.68rem;font-weight:700;flex-shrink:0}
.row .ic{width:15px;height:15px;border-radius:50%;flex-shrink:0;border:2px solid var(--line-2)}
.row.run .ic{border-color:var(--amber);border-top-color:transparent;animation:spin .8s linear infinite}
.row.done .ic{border-color:var(--ok);background:var(--ok)}
@keyframes spin{to{transform:rotate(360deg)}}
.row.done{border-color:rgba(74,222,128,.22)}
.row.run{border-color:rgba(252,211,77,.35);background:#151110}
.row.done .st{color:var(--ok)}
.row.run .st{color:var(--amber)}
.row.wait .st{color:var(--dim)}
.bar-prog{height:4px;border-radius:99px;background:var(--line);overflow:hidden;margin-top:.7rem}
.bar-prog i{display:block;height:100%;width:100%;transform-origin:0 50%;
  background:linear-gradient(90deg,var(--primary),var(--amber));
  animation:fill 9s var(--ease) infinite}
@keyframes fill{0%{transform:scaleX(.08)}45%{transform:scaleX(.62)}90%,100%{transform:scaleX(1)}}

/* ---------- băng nền tảng ---------- */
.marquee{border-block:1px solid var(--line);padding:1.05rem 0;overflow:hidden;
  background:linear-gradient(180deg,#0e0b0a,#0c0a09)}
.marquee-in{display:flex;width:max-content;animation:slide 36s linear infinite}
.marquee:hover .marquee-in{animation-play-state:paused}
@keyframes slide{to{transform:translateX(-50%)}}
.marquee span{display:inline-flex;align-items:center;gap:.65rem;padding-inline:1.8rem;
  font-size:.95rem;font-weight:600;color:#5f5853;white-space:nowrap;
  transition:color .3s var(--ease)}
.marquee span::before{content:'';width:6px;height:6px;border-radius:1px;
  background:var(--line-2);transform:rotate(45deg);transition:background .3s var(--ease)}
.marquee span:hover{color:var(--amber)}
.marquee span:hover::before{background:var(--amber)}

/* ---------- dải số liệu ---------- */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;
  background:var(--line);border-block:1px solid var(--line)}
.stat{background:var(--bg);padding:1.6rem 1.2rem;text-align:center}
.stat b{display:block;font-size:clamp(1.9rem,4.2vw,2.7rem);line-height:1;font-weight:800;
  background:linear-gradient(90deg,var(--primary),var(--amber));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  font-variant-numeric:tabular-nums}
.stat span{display:block;margin-top:.5rem;font-size:.82rem;color:var(--dim);line-height:1.4}

/* ---------- khối chung ---------- */
section{padding:clamp(3rem,7vw,5rem) 0}
.head{max-width:58ch;margin-bottom:2.4rem}
.kicker{display:inline-flex;align-items:center;gap:.5rem;font-size:.72rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;color:var(--primary);margin:0 0 .8rem}
h2{font-size:clamp(1.55rem,3.4vw,2.3rem);line-height:1.18;margin:0 0 .8rem}
.head p{color:var(--muted);margin:0;font-size:1.05rem}

/* ---------- các bước ---------- */
.steps{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));
  counter-reset:s}
.step{position:relative;padding:1.7rem 1.5rem;border:1px solid var(--line);border-radius:14px;
  background:var(--panel);counter-increment:s;
  transition:border-color .3s var(--ease),transform .3s var(--ease)}
.step:hover{border-color:var(--line-2);transform:translateY(-3px)}
.step::before{content:counter(s,decimal-leading-zero);position:absolute;top:1rem;right:1.2rem;
  font-size:2.6rem;font-weight:800;color:rgba(255,255,255,.045);line-height:1}
.step .ic{width:26px;height:26px;color:var(--amber);margin-bottom:.9rem}
.step h3{font-size:1.06rem;margin:0 0 .5rem}
.step p{margin:0;font-size:.93rem;color:var(--muted)}

/* ---------- sơ đồ workflow ---------- */
.wf{border:1px solid var(--line-2);border-radius:16px;background:
  radial-gradient(60% 80% at 30% 20%,rgba(255,122,0,.07),transparent 70%),var(--panel);
  padding:1rem;overflow:hidden}
.wf-scroll{overflow-x:auto;overscroll-behavior-x:contain}
.wf svg{width:100%;height:auto}
.wf-hint{display:none;margin:.6rem 0 0;font-size:.78rem;color:var(--dim)}
@media (max-width:780px){
  /* Thà cuộn ngang còn hơn chữ 5px không ai đọc được. */
  .wf-scroll svg{width:700px;max-width:none}
  .wf-hint{display:block}
}
.wf-link{fill:none;stroke:var(--line-2);stroke-width:2;stroke-dasharray:5 7;
  animation:dash 1.6s linear infinite}
@keyframes dash{to{stroke-dashoffset:-24}}
.wf-box{fill:var(--panel-2);stroke:var(--line-2);stroke-width:1.5}
.wf-box.act{stroke:var(--amber)}
.wf-t{fill:var(--text);font-size:15px;font-weight:600;
  font-family:'Inter',system-ui,sans-serif}
.wf-e{font-size:19px}
.wf-port{fill:var(--primary)}
.wf-g{opacity:0;animation:wfIn .6s var(--ease) forwards}
@keyframes wfIn{to{opacity:1}}
.wf-legend{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;margin-top:1rem;font-size:.82rem;
  color:var(--dim)}
.wf-legend b{color:var(--muted);font-weight:600}

/* ---------- nhóm node ---------- */
.groups{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(310px,100%),1fr))}
.group{padding:1.4rem 1.4rem 1.2rem;border:1px solid var(--line);border-radius:14px;
  background:var(--panel);transition:border-color .3s var(--ease),transform .3s var(--ease)}
.group:hover{border-color:var(--line-2);transform:translateY(-3px)}
.group-h{display:flex;align-items:center;gap:.65rem;margin-bottom:.9rem}
.group-h .em{font-size:1.25rem;line-height:1}
.group-h h3{font-size:1rem;margin:0;flex:1}
.group-h .n{font-size:.72rem;font-weight:700;color:var(--dim);
  border:1px solid var(--line-2);border-radius:999px;padding:.1rem .5rem}
.nodes{display:flex;flex-wrap:wrap;gap:.4rem}
.node{display:inline-flex;align-items:center;gap:.4rem;padding:.35rem .7rem;border-radius:8px;
  border:1px solid var(--line);background:#100d0c;font-size:.8rem;color:var(--muted);
  transition:color .25s var(--ease),border-color .25s var(--ease),transform .25s var(--ease)}
.node::before{content:'';width:5px;height:5px;border-radius:1px;background:var(--primary);opacity:.5}
.node:hover{color:var(--text);border-color:var(--line-2);transform:translateY(-2px)}
.node:hover::before{opacity:1}

/* ---------- Image-to-Prompt ---------- */
.i2p{display:grid;gap:1.5rem;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);
  align-items:center}
/* Con lưới mặc định min-width:auto — khối <pre> có bề rộng tối thiểu bằng dòng
   dài nhất nên kéo cả cột rộng ra, tràn cả trang. Cho phép co lại thì
   overflow-x:auto của .code mới có tác dụng. */
.i2p>*{min-width:0}
.i2p-src{border:1px solid var(--line-2);border-radius:14px;overflow:hidden;background:var(--panel-2);
  position:relative}
.i2p-src img{width:100%;aspect-ratio:1;object-fit:cover}
.i2p-scan{position:absolute;left:0;right:0;top:0;height:34%;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(252,211,77,.16),transparent);
  border-top:1px solid rgba(252,211,77,.5);animation:scan 3.6s ease-in-out infinite}
/* Cao 34% khung, nên đi từ -100% (khuất trên) tới 294% (khuất dưới) theo
   chính chiều cao của nó là quét trọn khung. */
@keyframes scan{0%{transform:translateY(-100%)}55%,100%{transform:translateY(294%)}}
.tabs{display:flex;gap:.35rem;margin-bottom:.7rem}
.tab{font-size:.75rem;font-weight:600;padding:.35rem .8rem;border-radius:7px;
  border:1px solid var(--line-2);color:var(--dim)}
.tab.on{background:var(--amber);color:#0c0a09;border-color:var(--amber)}
.code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.79rem;line-height:1.7;
  color:var(--muted);background:#100d0c;border:1px solid var(--line);border-radius:10px;
  padding:.9rem 1rem;overflow-x:auto;margin:0}
.code .k{color:var(--amber)}
.code .s{color:#8fd6a0}

/* ---------- thư viện ảnh ---------- */
.gal{display:grid;gap:.85rem;grid-template-columns:repeat(auto-fill,minmax(min(230px,100%),1fr))}
.shot{position:relative;overflow:hidden;border-radius:13px;border:1px solid var(--line);
  background:var(--panel);transition:border-color .3s var(--ease),transform .35s var(--ease)}
.shot img{width:100%;aspect-ratio:1;object-fit:cover;transition:transform .55s var(--ease)}
.shot:hover{border-color:var(--line-2);transform:translateY(-4px)}
.shot:hover img{transform:scale(1.05)}
.shot figcaption{position:absolute;inset:auto 0 0 0;padding:1.7rem .9rem .8rem;
  background:linear-gradient(180deg,transparent,rgba(8,6,5,.93));
  font-size:.85rem;font-weight:600}
.shot figcaption em{display:block;font-style:normal;font-weight:400;font-size:.76rem;
  color:var(--muted);margin-top:.15rem}

/* ---------- kho prompt ---------- */
.packs{display:grid;gap:.7rem;grid-template-columns:repeat(auto-fill,minmax(min(250px,100%),1fr))}
.pack{display:flex;align-items:center;gap:.85rem;padding:.95rem 1.1rem;border-radius:12px;
  border:1px solid var(--line);background:var(--panel);
  transition:border-color .25s var(--ease),transform .25s var(--ease)}
.pack:hover{border-color:var(--line-2);transform:translateY(-2px)}
.pack .em{font-size:1.35rem;line-height:1}
.pack .t{flex:1;font-size:.9rem;font-weight:600;line-height:1.3}
.pack .c{font-size:1.05rem;font-weight:800;color:var(--amber);font-variant-numeric:tabular-nums}

/* ---------- tính năng ---------- */
.feats{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr))}
.feat{position:relative;overflow:hidden;padding:1.6rem 1.5rem;border:1px solid var(--line);
  border-radius:14px;background:var(--panel);
  transition:border-color .3s var(--ease),transform .3s var(--ease),background .3s var(--ease)}
.feat::after{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;opacity:0;
  background:radial-gradient(260px circle at var(--mx,50%) var(--my,50%),rgba(255,122,0,.1),transparent 66%);
  transition:opacity .3s var(--ease)}
.feat:hover{border-color:var(--line-2);transform:translateY(-3px);background:var(--panel-2)}
.feat:hover::after{opacity:1}
.feat .ic{width:26px;height:26px;color:var(--primary);margin-bottom:.9rem;
  transition:transform .35s var(--ease)}
.feat:hover .ic{transform:scale(1.12) rotate(-4deg)}
.feat .n{position:absolute;top:1.3rem;right:1.4rem;font-size:.7rem;font-weight:800;
  letter-spacing:.1em;color:rgba(255,255,255,.12)}
.feat h3{font-size:1.04rem;margin:0 0 .5rem}
.feat p{margin:0;font-size:.92rem;color:var(--muted)}

/* ---------- giới hạn ---------- */
.limits{border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:14px;
  background:var(--panel);padding:1.9rem 1.8rem}
.limit{padding:1.1rem 0;border-top:1px solid var(--line)}
.limit:first-of-type{border-top:0;padding-top:0}
.limit h3{font-size:1rem;margin:0 0 .4rem;color:var(--amber)}
.limit p{margin:0;font-size:.93rem;color:var(--muted)}

/* ---------- FAQ ---------- */
.faq{display:grid;gap:.6rem;max-width:74ch}
details{border:1px solid var(--line);border-radius:12px;background:var(--panel);
  transition:border-color .25s var(--ease)}
details[open]{border-color:var(--line-2)}
summary{cursor:pointer;list-style:none;padding:1.05rem 1.3rem;font-weight:600;font-size:.98rem;
  display:flex;align-items:center;justify-content:space-between;gap:1rem}
summary::-webkit-details-marker{display:none}
summary::after{content:'';width:9px;height:9px;flex-shrink:0;
  border-right:2px solid var(--dim);border-bottom:2px solid var(--dim);
  transform:rotate(45deg) translateY(-2px);transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(-135deg) translateY(-2px);border-color:var(--amber)}
details p{margin:0;padding:0 1.3rem 1.15rem;color:var(--muted);font-size:.93rem}

/* ---------- kết ---------- */
.cta{text-align:center;border-top:1px solid var(--line)}
.cta h2{margin-bottom:.8rem}
.cta p{color:var(--muted);max-width:52ch;margin:0 auto 2rem}
.cta .actions{justify-content:center}
footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--dim);font-size:.85rem}
.foot-in{display:flex;flex-wrap:wrap;gap:1rem;justify-content:space-between;align-items:center}
.foot-brand{display:flex;align-items:center;gap:.6rem;color:var(--muted);font-weight:600}
footer a{display:inline-block;padding:.5rem .15rem;color:var(--muted);text-decoration:none;
  transition:color .25s var(--ease)}
footer a:hover{color:var(--primary)}

/* ---------- chuyển động ---------- */
.rise{opacity:0;transform:translateY(24px);
  transition:opacity .75s var(--ease),transform .75s var(--ease)}
.rise.in{opacity:1;transform:none}
.hero .eyebrow,.hero h1,.hero .tagline,.hero .actions,.hero .hero-facts{
  opacity:0;animation:riseIn .85s var(--ease) forwards}
.hero .eyebrow{animation-delay:.05s}
.hero h1{animation-delay:.13s}
.hero .tagline{animation-delay:.22s}
.hero .actions{animation-delay:.31s}
.hero .hero-facts{animation-delay:.4s}
@keyframes riseIn{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.progress{position:fixed;top:0;left:0;height:2px;width:100%;z-index:60;transform:scaleX(0);
  transform-origin:0 50%;background:linear-gradient(90deg,var(--primary),var(--amber))}
@supports (animation-timeline:scroll()){
  .progress{animation:grow linear;animation-timeline:scroll(root block)}
  @keyframes grow{to{transform:scaleX(1)}}
}

@media (max-width:900px){
  .hero-grid,.i2p{grid-template-columns:1fr}
  .bar-links{display:none}
}
@media (max-width:640px){
  .actions{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .limits{padding:1.4rem 1.25rem}
}
"""

JS = """
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -10% 0px',threshold:.08});
document.querySelectorAll('.rise').forEach(function(el,i){
  el.style.transitionDelay=(Math.min(i%6,5)*55)+'ms'; io.observe(el);
});

// Số liệu đếm lên khi cuộn tới. Chạy theo thời gian thật chứ không theo số
// khung hình, nên máy yếu vẫn dừng đúng lúc.
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

// Vệt sáng theo con trỏ: một vòng rAF dùng chung, chỉ ghi biến CSS rồi để
// trình duyệt tự vẽ — không đụng vào layout.
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


def workflow_svg():
    """Sơ đồ dựng bằng SVG toạ độ tuyệt đối — co giãn theo khung, không lệch."""
    parts = ['<svg viewBox="0 0 900 300" role="img" aria-label="Sơ đồ workflow: '
             'Prompt và Style Anchor vào node tạo ảnh, ra cổng chất lượng và text '
             'overlay, rồi tải về và báo Telegram">']
    for i, d in enumerate(WF_LINKS):
        parts.append(f'<path class="wf-link" d="{d}" style="animation-delay:{i * .18:.2f}s"/>')
    for x, y, w, h, label, em, order in WF_NODES:
        parts.append(
            f'<g class="wf-g" style="animation-delay:{.15 + order * .12:.2f}s">'
            f'<rect class="wf-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="11"/>'
            f'<text class="wf-e" x="{x + 16}" y="{y + h / 2 + 7}">{em}</text>'
            f'<text class="wf-t" x="{x + 46}" y="{y + h / 2 + 5}">{esc(label)}</text>'
            f'<circle class="wf-port" cx="{x}" cy="{y + h / 2}" r="3.5"/>'
            f'<circle class="wf-port" cx="{x + w}" cy="{y + h / 2}" r="3.5"/></g>')
    parts.append("</svg>")
    return "".join(parts)


def build():
    title = "SEOSONA Flow — chạy prompt AI hàng loạt trên Chrome"
    # Dưới 160 ký tự — Google cắt ở khoảng đó.
    desc = (f"Chrome extension tạo ảnh và video AI hàng loạt trên Google Flow, ChatGPT, "
            f"Gemini, Grok. {N_NODES} loại node workflow, {N_PROMPTS} prompt sẵn, "
            f"không cần API key.")

    # Băng logo lặp hai lần: animation dịch -50% nên nửa sau lấp đúng chỗ nửa
    # đầu vừa trôi ra, thành vòng liền mạch không thấy mối nối.
    one = "".join(f"<span>{esc(p)}</span>" for p in PROVIDERS)

    stats = "".join(
        f'<div class="stat"><b data-to="{n}" data-suffix="{esc(suf)}">0{esc(suf)}</b>'
        f'<span>{esc(lab)}</span></div>' for n, suf, lab in STATS)

    steps = "".join(
        f'<article class="step rise">{icon(ic)}<h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for ic, t, d in STEPS)

    groups = "".join(
        f'<article class="group rise"><div class="group-h"><span class="em">{em}</span>'
        f'<h3>{esc(name)}</h3><span class="n">{len(items)}</span></div>'
        f'<div class="nodes">' +
        "".join(f'<span class="node">{esc(x)}</span>' for x in items) +
        '</div></article>'
        for em, name, items in NODE_GROUPS)

    packs = "".join(
        f'<div class="pack rise"><span class="em">{em}</span>'
        f'<span class="t">{esc(name)}</span><span class="c">{n}</span></div>'
        for em, name, n in PROMPT_GROUPS)

    feats = "".join(
        f'<article class="feat rise"><span class="n">{i:02d}</span>{icon(ic)}'
        f'<h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (ic, t, d) in enumerate(FEATURES, 1))

    limits = "".join(
        f'<div class="limit"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in LIMITS)

    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))

    man = json.load(io.open(os.path.join(OUT, "landing", "gallery", "manifest.json"),
                            encoding="utf-8"))
    gallery = "".join(
        f'<figure class="shot rise">'
        f'<img src="gallery/g{m["i"]:02d}-480.webp" '
        f'srcset="gallery/g{m["i"]:02d}-320.webp 320w, gallery/g{m["i"]:02d}-480.webp 480w" '
        f'sizes="(max-width:640px) 92vw, (max-width:1000px) 44vw, 260px" '
        f'width="480" height="480" loading="lazy" decoding="async" '
        f'alt="{esc(m["title"])} — {esc(m["sub"])}" />'
        f'<figcaption>{esc(m["title"])}<em>{esc(m["sub"])}</em></figcaption></figure>'
        for m in man)

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareApplication", "name": "SEOSONA Flow",
             "applicationCategory": "BrowserApplication", "operatingSystem": "Chrome",
             "softwareVersion": VERSION, "description": desc, "url": SITE + "/",
             "image": SITE + "/cover.jpg",
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "VND"},
             "featureList": [t for _, t, _ in FEATURES],
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "SoftwareSourceCode", "name": "SEOSONA Flow",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": ["JavaScript", "Chrome Manifest V3"]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        version=VERSION, css=CSS, js=JS, jsonld=jsonld,
        logo=logo('a'), logo2=logo('b'),
        marquee=one + one, stats=stats, steps=steps, workflow=workflow_svg(),
        groups=groups, packs=packs, feats=feats, limits=limits, faq=faq, gallery=gallery,
        n_nodes=N_NODES, n_prompts=N_PROMPTS, n_templates=N_TEMPLATES,
        i_layers=icon("layers"), i_run=icon("run"))


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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect x='1.4' y='1.4' width='29.2' height='29.2' rx='9' fill='none' stroke='%23fcd34d' stroke-width='2'/><path d='M18.4 6 9.6 17.6h4.8L12.8 26l9-11.8h-5z' fill='%23ff7a00'/></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="SEOSONA Flow" />
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300..800&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>

<div class="ticker">Phiên bản <b>$version</b> · Chrome Manifest V3 · chạy <b>100% offline</b>, không cần API key trả phí</div>

<nav class="bar">
  <div class="bar-in">
    <a class="brand" href="#top">$logo SEOSONA Flow</a>
    <div class="bar-links">
      <a href="#cach-dung">Cách dùng</a>
      <a href="#workflow">Workflow</a>
      <a href="#thu-vien">Thư viện</a>
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
      <p class="eyebrow"><span class="dot"></span> Chrome Extension</p>
      <h1>Chạy prompt <span class="hl">hàng loạt</span><br />thay vì ngồi bấm từng cái</h1>
      <p class="tagline">
        SEOSONA Flow điều khiển chính những tab AI bạn đã đăng nhập — Google Flow, ChatGPT,
        Gemini, Grok — để tạo ảnh và video theo lô, rồi tự tải kết quả về máy.
      </p>
      <div class="actions">
        <a class="btn btn-primary" href="https://github.com/$repo" target="_blank" rel="noopener">Tải về từ GitHub ↗</a>
        <a class="btn btn-ghost" href="#cach-dung">Xem cách dùng</a>
      </div>
      <div class="hero-facts">
        <span><b>$n_nodes</b> loại node</span>
        <span><b>$n_prompts</b> prompt dựng sẵn</span>
        <span><b>$n_templates</b> mẫu có ảnh</span>
        <span><b>0đ</b> phí API</span>
      </div>
    </div>

    <!-- Mockup side panel: vẽ hoàn toàn bằng HTML/CSS nên không bao giờ lệch
         với bản thật, và không tốn thêm một byte ảnh nào. -->
    <div class="mock" role="img" aria-label="Minh hoạ side panel của SEOSONA Flow đang chạy hàng đợi 4 prompt trên Google Flow">
      <div class="mock-top">
        <i class="led"></i><i class="led"></i><i class="led"></i>
        <span class="mock-title">SEOSONA Flow · Side Panel</span>
        <span class="mock-badge">ĐANG CHẠY</span>
      </div>
      <div class="mock-body">
        <div class="chips">
          <span class="chip-s on">Google Flow</span>
          <span class="chip-s">ChatGPT</span>
          <span class="chip-s">Gemini</span>
          <span class="chip-s">Grok</span>
        </div>
        <div class="q-head"><span>Hàng đợi prompt</span><span>4 job</span></div>
        <div class="row done"><i class="ic"></i><span class="txt">phố đêm điện ảnh, đèn neon, 9:16</span><span class="st">XONG</span></div>
        <div class="row done"><i class="ic"></i><span class="txt">chân dung phi hành gia, ánh sáng studio</span><span class="st">XONG</span></div>
        <div class="row run"><i class="ic"></i><span class="txt">ảnh sản phẩm, tối giản, bóng đổ mềm</span><span class="st">ĐANG TẠO</span></div>
        <div class="row wait"><i class="ic"></i><span class="txt">nhân vật hoạt hình, dáng động</span><span class="st">CHỜ</span></div>
        <div class="bar-prog"><i></i></div>
      </div>
      <div class="mock-foot"><span>Tự tải về · 4K</span><span>Alt+G để chạy</span></div>
    </div>
  </div>
</header>

<div class="marquee" aria-hidden="true"><div class="marquee-in">$marquee</div></div>

<div class="stats">$stats</div>

<main>
  <section class="wrap" id="cach-dung">
    <div class="head">
      <p class="kicker rise">Ba bước</p>
      <h2 class="rise">Không có bước cài đặt phức tạp</h2>
      <p class="rise">Không npm install, không bundler, không tài khoản SEOSONA. Tải repo về, nạp vào Chrome là chạy.</p>
    </div>
    <div class="steps">$steps</div>
  </section>

  <section class="wrap" id="workflow">
    <div class="head">
      <p class="kicker rise">Workflow</p>
      <h2 class="rise">Kéo thả dựng dây chuyền sản xuất</h2>
      <p class="rise">Nối các bước lại thành một quy trình chạy tự động. Ảnh sinh ra đi qua cổng chất lượng, được gắn chữ, tải về đúng thư mục, rồi báo về Telegram — không cần ngồi canh.</p>
    </div>
    <div class="wf rise">
      <div class="wf-scroll">$workflow</div>
      <p class="wf-hint">↔ Vuốt ngang để xem hết sơ đồ</p>
      <div class="wf-legend">
        <span><b>Nhiều đầu vào</b> — gộp prompt và style anchor vào một node</span>
        <span><b>Rẽ nhánh</b> — một kết quả đi hai đường xử lý khác nhau</span>
        <span><b>@node</b> — lấy đầu ra của node trước làm biến cho node sau</span>
      </div>
    </div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">$n_nodes loại node</p>
      <h2 class="rise">Đủ mảnh để ghép gần như mọi quy trình</h2>
    </div>
    <div class="groups">$groups</div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Image-to-Prompt</p>
      <h2 class="rise">Thấy tấm ảnh đẹp, lấy luôn prompt của nó</h2>
      <p class="rise">Chuột phải một ảnh bất kỳ trên web, khoanh vùng màn hình, hoặc tải ảnh từ máy. Kết quả xuất ba dạng để dùng ngay.</p>
    </div>
    <div class="i2p rise">
      <div class="i2p-src">
        <img src="gallery/g04-480.webp" width="480" height="480" loading="lazy" decoding="async"
             alt="Ảnh nguồn đang được phân tích thành prompt" />
        <div class="i2p-scan"></div>
      </div>
      <div>
        <div class="tabs"><span class="tab on">JSON</span><span class="tab">English</span><span class="tab">Tiếng Việt</span></div>
        <pre class="code"><span class="k">"subject"</span>: <span class="s">"chai nước hoa thuỷ tinh, nắp vàng"</span>,
<span class="k">"lighting"</span>: <span class="s">"studio mềm, hắt sáng từ trái"</span>,
<span class="k">"background"</span>: <span class="s">"be trung tính, hoa mờ"</span>,
<span class="k">"camera"</span>:  <span class="s">"85mm, khẩu f/4, chính diện"</span>,
<span class="k">"grade"</span>:   <span class="s">"ấm, tương phản thấp"</span>,
<span class="k">"ratio"</span>:   <span class="s">"1:1"</span></pre>
      </div>
    </div>
  </section>

  <section class="wrap" id="thu-vien">
    <div class="head">
      <p class="kicker rise">Thư viện mẫu</p>
      <h2 class="rise">$n_templates mẫu, đây là mười hai tấm</h2>
      <p class="rise">Ảnh thật do chính extension sinh ra, kèm sẵn trong bản tải về. Mỗi mẫu là một prompt đã chỉnh xong — đổi chủ đề rồi chạy lại là ra bộ của bạn.</p>
    </div>
    <div class="gal">$gallery</div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Kho prompt</p>
      <h2 class="rise">$n_prompts prompt và skill đóng gói sẵn</h2>
      <p class="rise">Nằm ngay trong extension, chia bảy nhóm và xếp hạng theo chất lượng. Hoàn toàn ngoại tuyến — không gọi mạng, không tải thêm.</p>
    </div>
    <div class="packs">$packs</div>
  </section>

  <section class="wrap" id="tinh-nang">
    <div class="head">
      <p class="kicker rise">Tính năng</p>
      <h2 class="rise">Những gì nó làm thay bạn</h2>
    </div>
    <div class="feats">$feats</div>
  </section>

  <section class="wrap">
    <div class="head">
      <p class="kicker rise">Nói trước cho rõ</p>
      <h2 class="rise">Ba giới hạn bạn nên biết</h2>
      <p class="rise">Cách làm nào cũng có đánh đổi. Đây là những điểm yếu thật của SEOSONA Flow — biết trước thì đỡ mất thời gian.</p>
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
    <h2 class="rise">Mã nguồn mở, tải về là dùng</h2>
    <p class="rise">Không có bản trả phí, không có giới hạn gói, không có tài khoản nào để đăng ký. Toàn bộ nằm trên GitHub.</p>
    <div class="actions rise">
      <a class="btn btn-primary" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
      <a class="btn btn-ghost" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot-in">
    <span class="foot-brand">$logo2 SEOSONA Flow</span>
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
    if not os.path.exists(os.path.join(d, "gallery", "manifest.json")):
        print("Chưa có ảnh thư viện — chạy scripts/landing-seosona-flow-assets.py trước.")
        return 1
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "seosona-flow.jpg"),
                    os.path.join(d, "cover.jpg"))
    print(f"  {len(html) // 1024} KB  landing/index.html")
    print(f"  {N_NODES} node / {len(NODE_GROUPS)} nhóm · {len(FEATURES)} tính năng · "
          f"{len(FAQ)} câu hỏi · {len(LIMITS)} giới hạn")
    print(f"  {len(WF_NODES)} node trong sơ đồ · {len(PROMPT_GROUPS)} nhóm prompt · "
          f"12 ảnh thư viện")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
