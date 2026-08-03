#!/usr/bin/env python3
"""Landing page cho OmniClaw — hình thức terminal.

Trước đây bốn dự án hạ tầng dùng chung một bộ sinh, giống nhau 83% về cấu trúc
và trùng nhau từng khối một về thứ tự. Giờ mỗi cái một hình thức riêng, do bản
chất sản phẩm quyết định.

OmniClaw là hệ điều hành agent chạy trong terminal, cai quản bằng daemon và
pipeline zero-trust. Nên trang của nó là một cửa sổ terminal: phông monospace,
chuỗi khởi động gõ dần, mỗi mục là một pane có thanh tiêu đề, dòng nhắc `$`
thay cho tiêu đề mục. Không có hero căn trái, không có băng logo chạy ngang,
không có lưới thẻ bo góc — những thứ đó thuộc về ba trang kia.

    python scripts/landing-omniclaw.py

Số liệu đọc từ repo OmniClaw; danh sách daemon lấy từ
core/docs/architecture/CORE_DAEMONS_AND_OER.md.
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "OmniClaw")
SITE = "https://omniclaw-longleo.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/OmniClaw"

N_FILES = 14879
N_SKILLS = 578
N_KNOWLEDGE = 2148
N_DAEMONS = 8

BOOT = [
    ("omniclaw --boot", None),
    (None, "oma_architect   lập bản đồ hạ tầng ......... OK"),
    (None, "oap_pipeline    phân luồng đầu vào ......... OK"),
    (None, "oer_registry    nạp sổ đăng ký ............. OK"),
    (None, "oiw_intake      chờ mã nguồn ngoài ......... OK"),
    (None, "osf_warden      dựng tường lửa biên ........ OK"),
    (None, "obd_harbor      khoá cổng ngoài 127.0.0.1 .. OK"),
    (None, "ohd_healer      quét sức khoẻ hệ thống ..... OK"),
    (None, "oa_academy      kiểm toán logic ............ OK"),
    (None, "8/8 daemon đang chạy · zero-trust ĐANG BẬT"),
]

DAEMONS = [
    ("oma_architect", "Map Architect", "vẽ bản đồ hạ tầng và định danh node", "daemons"),
    ("oap_pipeline", "Assimilation", "phân luồng mọi thứ đi vào hệ", "daemons"),
    ("oer_registry", "Ecosystem Registry", "giữ sổ đăng ký thực thể", "daemons"),
    ("oiw_intake", "Intake Worker", "thu thập mã nguồn từ bên ngoài", "daemons"),
    ("oa_academy", "Academy", "kiểm toán logic, tuyển agent mới", "daemons"),
    ("osf_warden", "Sandbox Firewall", "cách ly thứ chưa qua kiểm duyệt", "security"),
    ("obd_harbor", "Bridge Daemon", "không skill nào tự mở cổng mạng", "security"),
    ("ohd_healer", "Health Daemon", "tự vá lỗi, dọn rác, chữa lint", "health"),
]

PANES = [
    ("~/core", "Nhân hệ thống", [
        ("Luật toàn cục", "bộ luật kế thừa ở phạm vi máy, không cấu hình lại từng dự án"),
        ("Pipeline cứng", "agent không tự quyết đường đi, mọi thứ qua một luồng cố định"),
        ("Bảo vệ Git", "quét cache, dọn sqlite, làm sạch commit trước khi đẩy lên"),
        ("Cổng mạng khoá", "chỉ 127.0.0.1, mở 0.0.0.0 là vi phạm trừ khi được cấp phép"),
    ]),
    ("~/brain", "Trí nhớ", [
        ("MemPalace ba tầng", "ngữ cảnh sống qua nhiều phiên thay vì bốc hơi mỗi lần đóng cửa sổ"),
        ("2.148 file tri thức", "đã phân tích và lập chỉ mục, truy vấn được lúc chạy"),
        ("Đồ thị tri thức", "quan hệ giữa các mảnh, không phải một đống file phẳng"),
    ]),
    ("~/ecosystem", "Hệ sinh thái", [
        ("578 kỹ năng", "mỗi cái là một thực thể có đăng ký, không phải script thả bừa"),
        ("Cầu nối và plugin", "vào hệ phải qua cổng kiểm duyệt của OIW rồi OSF"),
        ("Workflow", "chuỗi tác vụ chạy được, gắn với node đã đăng ký"),
    ]),
]

LIMITS = [
    ("Không phải phần mềm cho người dùng cuối",
     "Hạ tầng cho máy của một lập trình viên. Không bộ cài, không giao diện đồ hoạ, "
     "đọc tài liệu là bắt buộc."),
    ("Tám daemon, ba cái đã hiện thực bằng Python",
     "Năm cái còn lại tồn tại dưới dạng node agent theo tài liệu kiến trúc. Đây là hệ "
     "đang phát triển, không phải bản đã đóng băng."),
    ("Repo nặng, sát hạn mức triển khai",
     "14.879 file — Vercel giới hạn 15.000 file nguồn mỗi lần triển khai. Chính trang "
     "này phải cấu hình riêng mới lên được."),
    ("Trùng tên với hơn mười dự án khác",
     "Trên GitHub có nhiều repo tên OmniClaw do trùng trào lưu đặt tên. Bản này của "
     "Long Leo, 135 commit tự viết, không fork của ai."),
]

FAQ = [
    ("Khác gì một tập script tự động hoá?",
     "Khác ở tầng cai quản. Script thì ai chạy lúc nào cũng được; ở đây mọi thứ qua "
     "pipeline có daemon kiểm soát, vượt quyền là bị chấm dứt phiên ngay."),
    ("Vì sao lại chia tám daemon?",
     "Để không con nào ôm quá nhiều quyền. Tám vai chia vào ba phòng ban — hạ tầng, "
     "an ninh, sức khoẻ hệ thống — mỗi cái một ranh giới cứng."),
    ("Có phải bản clone của dự án OmniClaw nào khác không?",
     "Không. Trên GitHub có hơn mười repo cùng tên, nhưng bản này không phải fork — "
     "135 commit tự viết từ tháng 3/2026."),
    ("Cần gì để chạy?",
     "Python, cộng Claude Code CLI hoặc Google Antigravity. Repo khoảng 110 MB vì mang "
     "theo cả kho tri thức và hệ sinh thái kỹ năng."),
]

# Dòng log chạy ở chân cửa sổ terminal. Sáu dòng, lặp lại — đủ để trang có
# nhịp sống mà không thành thứ gây rối mắt.
STREAM = [
    "oer_registry  đăng ký thực thể mới: skill/vision-ocr",
    "osf_warden    cách ly gói chưa ký: 1 mục vào khu chờ",
    "ohd_healer    dọn 214 file tạm · vá 3 lỗi lint",
    "obd_harbor    từ chối mở cổng 0.0.0.0:8080 — vi phạm luật",
    "oiw_intake    thu thập xong 2 repo, chuyển sang OAP",
    "oa_academy    kiểm toán 18 kỹ năng · 17 đạt · 1 trả lại",
]

STACK = ["Python", "Claude Code CLI", "Google Antigravity", "MCP", "SQLite",
         "TypeScript", "Rust"]

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#080a0b; --pane:#0e1214; --pane-2:#131a1d; --line:#1e282c; --line-2:#2b393e;
  --text:#dfe7ea; --muted:#8fa3aa; --dim:#748a93;
  --amber:#f75c1e; --lime:#7ee787; --warn:#f2c14e; --danger:#ff6b6b;
  --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:15px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
/* Lưới mảnh phía sau, gợi màn hình phosphor mà không làm chữ khó đọc. */
body::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.4;
  background-image:linear-gradient(rgba(126,231,135,.045) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(126,231,135,.045) 1px,transparent 1px);
  background-size:34px 34px;
  mask-image:radial-gradient(120% 90% at 50% 0%,#000 20%,transparent 75%);
}
body>*{position:relative;z-index:1}
a{color:inherit}
svg{display:block}
.wrap{width:min(980px,100% - 2.2rem);margin-inline:auto}
:focus-visible{outline:2px solid var(--lime);outline-offset:3px}

/* ---------- thanh trên cùng: dòng lệnh, không phải nav ---------- */
.top{border-bottom:1px solid var(--line);background:rgba(8,10,11,.9);
  backdrop-filter:blur(10px);position:sticky;top:0;z-index:50}
.top-in{display:flex;align-items:center;gap:1rem;padding:.6rem 0;
  width:min(980px,100% - 2.2rem);margin-inline:auto;font-size:.8rem}
.leds{display:flex;gap:.4rem}
.leds i{width:10px;height:10px;border-radius:50%;background:#2b393e}
.leds i:nth-child(1){background:#ff5f57}
.leds i:nth-child(2){background:#febc2e}
.leds i:nth-child(3){background:#28c840}
.top-path{color:var(--dim)}
.top-path b{color:var(--lime);font-weight:500}
.top a{margin-left:auto;color:var(--muted);text-decoration:none;padding:.4rem .7rem;
  border:1px solid var(--line-2);transition:color .2s,border-color .2s,background .2s}
.top a:hover{color:var(--bg);background:var(--lime);border-color:var(--lime)}

/* ---------- hero: chuỗi khởi động ---------- */
.boot{padding:clamp(2rem,5vw,3.5rem) 0 clamp(1.5rem,4vw,2.5rem)}
.term{border:1px solid var(--line-2);background:var(--pane);
  box-shadow:0 30px 70px -40px #000,0 0 0 1px rgba(126,231,135,.04) inset}
.term-bar{display:flex;align-items:center;gap:.6rem;padding:.5rem .8rem;
  border-bottom:1px solid var(--line);background:var(--pane-2);font-size:.76rem;
  color:var(--dim);letter-spacing:.02em}
.term-body{padding:1.1rem 1.2rem;font-size:.86rem;line-height:1.85}
.bl{white-space:pre;overflow:hidden;opacity:0;animation:blIn .01s linear forwards}
@keyframes blIn{to{opacity:1}}
.bl .p{color:var(--lime)}
.bl .c{color:var(--text)}
.bl .ok{color:var(--lime)}
.bl.last{color:var(--amber);font-weight:600;margin-top:.5rem}
.cursor{display:inline-block;width:8px;height:1em;background:var(--lime);
  vertical-align:text-bottom;animation:blink 1.05s step-end infinite}
@keyframes blink{50%{opacity:0}}

h1{font-size:clamp(1.75rem,4.4vw,2.9rem);line-height:1.15;font-weight:600;
  margin:clamp(1.8rem,4vw,2.6rem) 0 1rem;letter-spacing:-.02em}
h1 .hl{color:var(--amber)}
.lede{color:var(--muted);font-size:clamp(.95rem,1.7vw,1.05rem);max-width:66ch;margin:0 0 1.6rem}
.acts{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1.4rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.7rem 1.2rem;
  font-size:.85rem;font-weight:600;text-decoration:none;border:1px solid var(--line-2);
  transition:transform .2s var(--ease),background .2s,color .2s,border-color .2s}
.btn:hover{transform:translateY(-2px)}
.btn.pri{background:var(--amber);color:#080a0b;border-color:var(--amber)}
.btn.pri:hover{box-shadow:0 10px 26px -12px var(--amber)}
.btn.sec:hover{border-color:var(--lime);color:var(--lime)}

/* ---------- dải số liệu kiểu bảng ---------- */
.meters{border:1px solid var(--line);display:grid;
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.meter{padding:1rem 1.1rem;border-right:1px solid var(--line)}
.meter:last-child{border-right:0}
.meter b{display:block;font-size:1.6rem;font-weight:600;color:var(--lime);
  font-variant-numeric:tabular-nums;line-height:1.2}
.meter span{font-size:.74rem;color:var(--dim);letter-spacing:.04em}

/* ---------- mục: dòng nhắc thay cho tiêu đề ---------- */
section{padding:clamp(2.2rem,5vw,3.4rem) 0}
.prompt{font-size:.86rem;color:var(--dim);margin:0 0 .5rem}
.prompt b{color:var(--lime);font-weight:500}
h2{font-size:clamp(1.2rem,2.6vw,1.6rem);font-weight:600;margin:0 0 .7rem;
  letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 1.6rem;max-width:70ch;font-size:.92rem}

/* ---------- bảng daemon ---------- */
.tbl{border:1px solid var(--line);overflow-x:auto}
.tbl table{width:100%;border-collapse:collapse;font-size:.84rem;min-width:560px}
.tbl th{text-align:left;padding:.6rem .9rem;border-bottom:1px solid var(--line-2);
  color:var(--dim);font-weight:500;font-size:.74rem;letter-spacing:.08em;
  text-transform:uppercase;background:var(--pane-2)}
.tbl td{padding:.62rem .9rem;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:0}
.tbl tbody tr{transition:background .2s}
.tbl tbody tr:hover{background:var(--pane-2)}
.tbl .id{color:var(--amber);white-space:nowrap}
.tbl .nm{color:var(--text)}
.tbl .rl{color:var(--muted)}
.tag{display:inline-block;padding:.05rem .5rem;font-size:.7rem;border:1px solid;
  white-space:nowrap}
.tag.daemons{color:var(--amber);border-color:rgba(247,92,30,.4)}
.tag.security{color:var(--danger);border-color:rgba(255,107,107,.4)}
.tag.health{color:var(--lime);border-color:rgba(126,231,135,.4)}

/* ---------- pane thư mục ---------- */
.panes{display:grid;gap:1rem}
.pane{border:1px solid var(--line);background:var(--pane)}
.pane-h{display:flex;align-items:center;gap:.6rem;padding:.5rem .9rem;
  border-bottom:1px solid var(--line);background:var(--pane-2);font-size:.78rem}
.pane-h .dir{color:var(--lime)}
.pane-h .ttl{color:var(--dim);margin-left:auto}
.pane ul{list-style:none;margin:0;padding:.5rem 0}
.pane li{display:flex;gap:.8rem;padding:.5rem .9rem;font-size:.85rem;
  transition:background .2s}
.pane li:hover{background:var(--pane-2)}
.pane li::before{content:'├─';color:var(--dim);flex-shrink:0}
.pane li:last-child::before{content:'└─'}
.pane li b{color:var(--text);font-weight:600;flex-shrink:0;min-width:150px}
.pane li em{font-style:normal;color:var(--muted)}

/* ---------- công nghệ ---------- */
.stack{display:flex;flex-wrap:wrap;gap:.4rem}
.stack span{padding:.3rem .8rem;font-size:.8rem;border:1px solid var(--line-2);
  color:var(--muted);transition:color .2s,border-color .2s}
.stack span:hover{color:var(--lime);border-color:var(--lime)}

/* ---------- cảnh báo ---------- */
.warns{border:1px solid rgba(242,193,78,.28);background:rgba(242,193,78,.04)}
.warn{padding:1rem 1.1rem;border-bottom:1px solid rgba(242,193,78,.14);
  display:flex;gap:.8rem;font-size:.88rem}
.warn:last-child{border-bottom:0}
.warn::before{content:'!';color:var(--warn);font-weight:700;flex-shrink:0;
  width:20px;height:20px;border:1px solid rgba(242,193,78,.45);
  display:grid;place-items:center;font-size:.75rem}
.warn b{display:block;color:var(--warn);font-weight:600;margin-bottom:.15rem}
.warn em{font-style:normal;color:var(--muted)}

/* ---------- hỏi đáp ---------- */
details{border:1px solid var(--line);background:var(--pane);margin-bottom:.5rem}
details[open]{border-color:var(--line-2)}
summary{cursor:pointer;list-style:none;padding:.8rem 1rem;font-size:.88rem;
  color:var(--text);display:flex;gap:.7rem}
summary::-webkit-details-marker{display:none}
summary::before{content:'?';color:var(--lime);flex-shrink:0}
details[open] summary::before{content:'>'}
details p{margin:0;padding:0 1rem .9rem 2.2rem;color:var(--muted);font-size:.86rem}

/* ---------- kết ---------- */
.end{border-top:1px solid var(--line);padding:clamp(2.5rem,6vw,4rem) 0;text-align:center}
.end h2{margin-bottom:.6rem}
.end p{color:var(--muted);margin:0 auto 1.6rem;max-width:52ch;font-size:.92rem}
.end .acts{justify-content:center;margin-bottom:0}
footer{border-top:1px solid var(--line);padding:1.4rem 0;font-size:.78rem;color:var(--dim)}
.foot{display:flex;flex-wrap:wrap;gap:.8rem;justify-content:space-between}
footer a{color:var(--muted);text-decoration:none;padding:.3rem 0}
footer a:hover{color:var(--lime)}

/* Vệt quét ngang cửa sổ terminal — gợi màn hình CRT đang làm tươi. */
.term{position:relative;overflow:hidden}
.term::after{content:'';position:absolute;left:0;right:0;height:38%;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(126,231,135,.05),transparent);
  animation:sweep 6.5s linear infinite}
@keyframes sweep{0%{transform:translateY(-120%)}100%{transform:translateY(320%)}}

/* Đèn trạng thái từng daemon, nhấp theo phòng ban lệch pha nhau. */
.tbl .id{position:relative;padding-left:1.1rem}
.tbl .id::before{content:'';position:absolute;left:0;top:.62em;width:6px;height:6px;
  border-radius:50%;background:var(--lime);
  animation:beat 2.6s ease-in-out infinite;animation-delay:calc(var(--i,0) * .22s)}
.tbl tr[data-dept="security"] .id::before{background:var(--danger)}
.tbl tr[data-dept="health"] .id::before{background:var(--warn)}
@keyframes beat{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.72)}}

/* Thanh tiến độ đọc trang, mảnh như dòng lệnh. */
.prog{position:fixed;top:0;left:0;height:2px;width:100%;z-index:70;transform:scaleX(0);
  transform-origin:0 50%;background:linear-gradient(90deg,var(--lime),var(--amber))}
@supports (animation-timeline:scroll()){
  .prog{animation:pgrow linear;animation-timeline:scroll(root block)}
  @keyframes pgrow{to{transform:scaleX(1)}}
}

/* Con trỏ nhấp sau mỗi dòng nhắc của từng mục. */
.prompt b::after{content:'';display:inline-block;width:7px;height:.95em;margin-left:.35rem;
  background:var(--lime);vertical-align:text-bottom;animation:blink 1.05s step-end infinite}

/* Luồng log chạy ở chân pane — chỉ đổi transform nên không gây vẽ lại layout. */
.stream{overflow:hidden;height:1.6em;border-top:1px solid var(--line);
  background:var(--pane-2);font-size:.76rem;color:var(--dim)}
.stream ul{list-style:none;margin:0;padding:0;animation:roll2 12s steps(6) infinite}
.stream li{height:1.6em;line-height:1.6em;padding-inline:.9rem;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
@keyframes roll2{to{transform:translateY(-9.6em)}}

.rise{opacity:0;transform:translateY(14px);
  transition:opacity .6s var(--ease),transform .6s var(--ease)}
.rise.in{opacity:1;transform:none}
@media (max-width:640px){
  body{font-size:14px}
  .acts{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .term-body{font-size:.74rem}
  .pane li{flex-direction:column;gap:.15rem}
  .pane li b{min-width:0}
}
"""

JS = """
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -8% 0px',threshold:.06});
document.querySelectorAll('.rise').forEach(function(el){ io.observe(el); });

// Chuỗi khởi động gõ dần. Không dùng setInterval dài — mỗi dòng một hẹn giờ
// riêng, tính sẵn thời điểm, nên tab bị ẩn rồi hiện lại vẫn không lệch nhịp.
document.querySelectorAll('.bl').forEach(function(el,i){
  el.style.animationDelay=(0.25+i*0.16)+'s';
});

var cio=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting) return;
    cio.unobserve(e.target);
    var el=e.target,to=+el.dataset.to,t0=0,dur=1000;
    requestAnimationFrame(function step(t){
      if(!t0) t0=t;
      var p=Math.min((t-t0)/dur,1);
      el.textContent=Math.round(to*(1-Math.pow(1-p,3))).toLocaleString('vi-VN');
      if(p<1) requestAnimationFrame(step);
    });
  });
},{threshold:.5});
document.querySelectorAll('[data-to]').forEach(function(el){ cio.observe(el); });
"""

PAGE = Template("""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>$title</title>
<meta name="description" content="$desc" />
<meta name="author" content="Hà Đình Long" />
<meta name="theme-color" content="#080a0b" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23080a0b'/><text x='5' y='22' font-family='monospace' font-size='16' fill='%237ee787'>&gt;_</text></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="OmniClaw" />
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>

<div class="prog" aria-hidden="true"></div>

<div class="top">
  <div class="top-in">
    <span class="leds"><i></i><i></i><i></i></span>
    <span class="top-path">longleo@omniclaw:<b>~</b>$$</span>
    <a href="https://github.com/$repo" target="_blank" rel="noopener">git clone ↗</a>
  </div>
</div>

<header class="boot">
  <div class="wrap">
    <div class="term">
      <div class="term-bar">omniclaw · 8 daemon · zero-trust</div>
      <div class="term-body">$boot<span class="cursor"></span></div>
      <div class="stream" aria-hidden="true"><ul>$stream</ul></div>
    </div>

    <h1>Agent ở đây <span class="hl">không có ý chí tự do</span></h1>
    <p class="lede">
      Mọi thứ chạy qua một pipeline cứng, tám daemon canh gác. Không phải mấy con agent
      đóng vai nhân viên rồi tự quyết — mà là một tầng backend không né được, nằm dưới
      mọi công cụ AI trên máy.
    </p>
    <div class="acts">
      <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
      <a class="btn sec" href="#daemon">Đọc kiến trúc daemon</a>
    </div>

    <div class="meters">
      <div class="meter"><b data-to="$n_daemons">0</b><span>DAEMON LÕI</span></div>
      <div class="meter"><b data-to="$n_skills">0</b><span>KỸ NĂNG ĐÃ ĐĂNG KÝ</span></div>
      <div class="meter"><b data-to="$n_knowledge">0</b><span>FILE TRI THỨC</span></div>
      <div class="meter"><b data-to="$n_files">0</b><span>FILE TRONG REPO</span></div>
    </div>
  </div>
</header>

<main>
  <section class="wrap" id="daemon">
    <p class="prompt rise">$$ <b>omniclaw daemons --list</b></p>
    <h2 class="rise">Tám trụ cột, ba phòng ban</h2>
    <p class="sub rise">Mỗi daemon chỉ được làm đúng một việc và bị nhốt trong một phòng ban.
      Con nào chạy script ngoài phạm vi của mình thì bộ điều phối chấm dứt phiên ngay —
      đó là ý nghĩa của zero-trust ở đây.</p>
    <div class="tbl rise">
      <table>
        <thead><tr><th>Mã node</th><th>Tên</th><th>Vai trò</th><th>Phòng ban</th></tr></thead>
        <tbody>$daemons</tbody>
      </table>
    </div>
  </section>

  <section class="wrap">
    <p class="prompt rise">$$ <b>tree -L 1</b></p>
    <h2 class="rise">Ba thư mục, ba trách nhiệm</h2>
    <div class="panes">$panes</div>
  </section>

  <section class="wrap">
    <p class="prompt rise">$$ <b>cat DEPENDENCIES</b></p>
    <h2 class="rise">Dựng bằng gì</h2>
    <div class="stack rise">$stack</div>
  </section>

  <section class="wrap">
    <p class="prompt rise">$$ <b>omniclaw doctor --honest</b></p>
    <h2 class="rise">Bốn cảnh báo</h2>
    <p class="sub rise">Đây là dự án cá nhân đang phát triển, không phải sản phẩm thương mại.</p>
    <div class="warns rise">$limits</div>
  </section>

  <section class="wrap">
    <p class="prompt rise">$$ <b>man omniclaw</b></p>
    <h2 class="rise">Câu hỏi thường gặp</h2>
    <div class="rise">$faq</div>
  </section>

  <section class="end">
    <div class="wrap">
      <h2 class="rise">Mã nguồn mở, đọc được toàn bộ</h2>
      <p class="rise">Không có bản trả phí, không có phần đóng. Tất cả nằm trên GitHub.</p>
      <div class="acts rise">
        <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
        <a class="btn sec" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot">
    <span>longleo@omniclaw · © 2026 Hà Đình Long</span>
    <span><a href="$portfolio/">Portfolio</a> · <a href="https://github.com/$repo" target="_blank" rel="noopener">GitHub</a></span>
  </div>
</footer>

<script>$js</script>
</body>
</html>
""")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def build():
    title = "OmniClaw của Long Leo — hệ điều hành agent 8 daemon cho Claude Code"
    desc = ("Biến máy cá nhân thành dàn AI tự vận hành, cai quản bởi 8 daemon lõi theo mô "
            "hình zero-trust. 578 kỹ năng đã đăng ký, MemPalace ba tầng, bảo vệ Git.")

    boot = []
    for cmd, out in BOOT:
        if cmd:
            boot.append(f'<div class="bl"><span class="p">$</span> '
                        f'<span class="c">{esc(cmd)}</span></div>')
        elif out.startswith("8/8"):
            boot.append(f'<div class="bl last">{esc(out)}</div>')
        else:
            name, rest = out.split(" ", 1)
            boot.append(f'<div class="bl"><span class="ok">[✓]</span> '
                        f'<span class="c">{esc(name)}</span> {esc(rest)}</div>')

    daemons = "".join(
        f'<tr data-dept="{d}"><td class="id" style="--i:{i}">{esc(k)}</td>'
        f'<td class="nm">{esc(n)}</td>'
        f'<td class="rl">{esc(r)}</td><td><span class="tag {d}">{d}</span></td></tr>'
        for i, (k, n, r, d) in enumerate(DAEMONS))
    stream = "".join(f"<li>{esc(x)}</li>" for x in STREAM)

    panes = "".join(
        f'<div class="pane rise"><div class="pane-h"><span class="dir">{esc(path)}</span>'
        f'<span class="ttl">{esc(label)}</span></div><ul>' +
        "".join(f'<li><b>{esc(t)}</b><em>{esc(v)}</em></li>' for t, v in items) +
        '</ul></div>'
        for path, label, items in PANES)

    stack = "".join(f"<span>{esc(t)}</span>" for t in STACK)
    limits = "".join(
        f'<div class="warn"><div><b>{esc(t)}</b><em>{esc(d)}</em></div></div>'
        for t, d in LIMITS)
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareSourceCode", "name": "OmniClaw", "description": desc,
             "url": SITE + "/", "image": SITE + "/cover.jpg",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": STACK,
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        css=CSS, js=JS, jsonld=jsonld, boot="".join(boot), daemons=daemons,
        panes=panes, stack=stack, limits=limits, faq=faq, stream=stream,
        n_daemons=N_DAEMONS, n_skills=N_SKILLS, n_knowledge=N_KNOWLEDGE, n_files=N_FILES)


def main():
    d = os.path.join(OUT, "landing")
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "omniclaw.jpg"),
                    os.path.join(d, "cover.jpg"))
    print(f"  {len(html) // 1024} KB  OmniClaw — hình thức terminal")
    print(f"  {len(DAEMONS)} daemon · {len(PANES)} pane · {len(LIMITS)} cảnh báo · "
          f"{len(FAQ)} câu hỏi · phông IBM Plex Mono")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
