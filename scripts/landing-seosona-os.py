#!/usr/bin/env python3
"""Landing page cho SEOSONA OS — bố cục hướng tâm.

Sản phẩm là một bộ não trung tâm mà mọi công cụ AI nối vào. Nên trang không có
hero căn trái như trang bán hàng thông thường: mọi thứ xoay quanh một lõi ở
giữa. Vòng quỹ đạo quay chậm, các tầng trí nhớ là vòng tròn đồng tâm, các năng
lực xếp dọc theo một trục giữa lệch trái phải xen kẽ.

Không có bảng, không có terminal, không có dải film — những thứ đó thuộc về ba
trang anh em. Phông Lexend, khác cả bốn trang kia.

    python scripts/landing-seosona-os.py
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "SEOSONA-OS")
SITE = "https://seosona-os.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/SEOSONA-OS"

N_KNOWLEDGE = 2422
N_MEMORY = 3560
N_CORE = 159
N_FILES = 8763

TOOLS = ["Claude Code", "Cursor", "Codex", "Windsurf", "Aider"]
SATELLITES = [("Video AI", "dây chuyền sản xuất video"), ("Content", "nội dung và SRT"),
              ("UX-UI", "hệ thống thiết kế"), ("Flow", "tự động hoá trình duyệt")]

# Ba tầng trí nhớ, vẽ thành ba vòng đồng tâm.
RINGS = [
    ("Lõi", "1_CORE", f"{N_CORE} file", "bộ luật và cấu hình gốc, thứ được tiêm vào mọi công cụ"),
    ("Tri thức", "2_KNOWLEDGE", f"{N_KNOWLEDGE} file", "đã phân tích và lập chỉ mục, truy vấn bằng ngôn ngữ tự nhiên"),
    ("Bộ nhớ", "3_MEMORY", f"{N_MEMORY} file", "ngữ cảnh dài hạn theo từng dự án, sống qua nhiều phiên"),
]

# Năm năng lực, xếp dọc trục giữa lệch trái phải xen kẽ.
SPINE = [
    ("Cai quản", "Một bản doctrine duy nhất được tiêm vào Claude Code, Cursor, Codex, "
     "Windsurf và Aider. Viết một lần, không phải dạy lại từng công cụ."),
    ("Ghi nhớ", "Kho tri thức mở ra cho agent qua một MCP server tìm kiếm ngữ nghĩa. "
     "Hỏi bằng câu tự nhiên thay vì phải biết trước tên file."),
    ("Tự lớn lên", "Pipeline kéo repo bên ngoài về, đọc, đánh giá, và chỉ giữ lại thứ "
     "thực sự dùng được — biến chúng thành kỹ năng gọi được, không cần người chép tay."),
    ("Hành động", "Tầng định tuyến tự chọn đúng kỹ năng cho từng việc rồi thực thi. "
     "Thao tác không hoàn tác được — xoá file, đẩy commit, gọi API tính tiền — phải qua cổng riêng."),
    ("Chỉ huy", "Bốn dự án vệ tinh nối ngược về đây và dùng chung tri thức lúc chạy, "
     "nên sửa một chỗ là cả bốn đổi theo."),
]

LIMITS = [
    ("Cài đặt không nhẹ nhàng",
     "Hạ tầng cho máy làm việc của một người, không phải ứng dụng bấm là chạy. Phải cấu "
     "hình đường dẫn, khoá API và từng công cụ AI muốn nối vào."),
    ("Kho tri thức là của một người",
     "2.422 file kia phản ánh cách làm việc và lĩnh vực của Long Leo. Người khác dùng "
     "được phần khung, nhưng nội dung phải tự nuôi."),
    ("Càng nhiều công cụ càng nhiều điểm gãy",
     "Mỗi công cụ AI đổi định dạng cấu hình là một chỗ phải sửa. Đó là cái giá của việc "
     "bắc cầu qua năm hệ khác nhau."),
]

FAQ = [
    ("Khác gì với việc tự viết file quy tắc cho từng công cụ?",
     "Khác ở chỗ chỉ có một bản. Viết riêng cho từng công cụ thì sau vài tháng chúng lệch "
     "nhau, và không ai nhớ bản nào mới nhất."),
    ("Trí nhớ được lưu thế nào?",
     "Ba tầng đồng tâm: lõi luật, kho tri thức đã phân tích, và bộ nhớ dài hạn theo dự án. "
     "Agent truy vấn qua MCP chứ không đọc thẳng file."),
    ("Tự học nghĩa là sao?",
     "Có pipeline nạp repo bên ngoài về, phân tích, và biến phần hữu ích thành kỹ năng "
     "gọi được — hoàn toàn tự động."),
    ("Chạy trên hệ điều hành nào?",
     "Windows, macOS và Linux. Cần Python 3.11 trở lên và Node 18 trở lên."),
]

STACK = ["Python 3.11+", "Node.js 18+", "MCP", "Tìm kiếm ngữ nghĩa", "Đồ thị tri thức",
         "SQLite", "Windows · macOS · Linux"]

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0b0a08; --panel:#151209; --panel-2:#1d180e; --line:#2a2318; --line-2:#3d3320;
  --text:#faf7ef; --muted:#b0a692; --dim:#8a7f6b;
  --gold:#f0a63c; --amber:#fcd34d; --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Lexend',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;
  text-align:center;
}
/* Vòng tròn đồng tâm phía sau — nhắc lại ý "mọi thứ xoay quanh một lõi". */
body::before{
  content:'';position:fixed;left:50%;top:14%;width:min(190vw,1500px);aspect-ratio:1;
  transform:translateX(-50%);z-index:0;pointer-events:none;opacity:.5;
  background:
    radial-gradient(circle,transparent 0 17%,rgba(240,166,60,.09) 17% 17.25%,transparent 17.25%),
    radial-gradient(circle,transparent 0 27%,rgba(240,166,60,.07) 27% 27.2%,transparent 27.2%),
    radial-gradient(circle,transparent 0 38%,rgba(240,166,60,.05) 38% 38.15%,transparent 38.15%),
    radial-gradient(circle,rgba(240,166,60,.11),transparent 46%);
}
body>*{position:relative;z-index:1}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
svg{display:block}
.wrap{width:min(980px,100% - 2.4rem);margin-inline:auto}
h1,h2,h3{letter-spacing:-.028em;font-weight:600}
:focus-visible{outline:2px solid var(--amber);outline-offset:3px;border-radius:6px}

/* ---------- điều hướng gọn, căn giữa ---------- */
.nav{padding:1.1rem 0;display:flex;justify-content:center;gap:1.4rem;font-size:.85rem}
.nav a{display:inline-block;padding:.45rem .3rem;color:var(--muted);
  text-decoration:none;transition:color .25s var(--ease)}
.nav a:hover{color:var(--amber)}
.nav .gh{color:var(--text);font-weight:600}

/* ---------- hero hướng tâm ---------- */
.hero{padding:clamp(1.5rem,4vw,3rem) 0 clamp(2.5rem,6vw,4rem)}
.kick{display:inline-block;font-size:.72rem;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gold);margin:0 0 1.4rem}
h1{font-size:clamp(2rem,5.2vw,3.5rem);line-height:1.08;margin:0 auto 1.2rem;max-width:16ch}
h1 .hl{background:linear-gradient(100deg,var(--gold),var(--amber));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.lede{color:var(--muted);font-size:clamp(1rem,1.9vw,1.15rem);max-width:56ch;
  margin:0 auto 2rem}
.acts{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center;margin-bottom:2.6rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.6rem;border-radius:999px;
  font-size:.92rem;font-weight:600;text-decoration:none;border:1px solid transparent;
  transition:transform .25s var(--ease),background .25s,border-color .25s,box-shadow .25s}
.btn:hover{transform:translateY(-2px)}
.btn.pri{background:var(--gold);color:#0b0a08}
.btn.pri:hover{box-shadow:0 14px 34px -14px var(--gold)}
.btn.sec{border-color:var(--line-2);color:var(--text)}
.btn.sec:hover{border-color:var(--gold);background:rgba(240,166,60,.07)}

/* ---------- sơ đồ quỹ đạo ---------- */
.orbit{position:relative;width:min(560px,100%);aspect-ratio:1;margin:0 auto}
.ring{position:absolute;inset:0;border:1px dashed var(--line-2);border-radius:50%;
  animation:spin 46s linear infinite}
.ring.r2{inset:13%;animation-duration:34s;animation-direction:reverse;
  border-style:solid;border-color:var(--line)}
.ring.r3{inset:26%;animation-duration:26s;border-color:rgba(240,166,60,.18)}
@keyframes spin{to{transform:rotate(360deg)}}
.node{position:absolute;left:50%;top:50%;width:0;height:0;
  transform:rotate(var(--a)) translateY(calc(var(--r) * -1))}
.node span{position:absolute;left:50%;top:50%;translate:-50% -50%;
  transform:rotate(calc(var(--a) * -1));white-space:nowrap;
  padding:.42rem .9rem;border-radius:999px;font-size:.8rem;font-weight:500;
  background:var(--panel-2);border:1px solid var(--line-2);color:var(--muted);
  transition:color .25s var(--ease),border-color .25s var(--ease)}
.node span:hover{color:var(--text);border-color:var(--gold)}
/* Nhãn quay ngược lại đúng bằng góc của quỹ đạo nên luôn nằm ngang, dù vòng
   ngoài đang xoay. Không có mẹo này thì chữ lộn ngược ở nửa dưới. */
.orbit-wrap{position:absolute;inset:0;animation:spin 46s linear infinite}
.core{position:absolute;left:50%;top:50%;translate:-50% -50%;
  width:min(46%,240px);aspect-ratio:1;border-radius:50%;display:grid;
  place-content:center;gap:.15rem;
  background:radial-gradient(circle at 34% 30%,var(--amber),var(--gold) 58%,#b8720f);
  color:#1a1206;box-shadow:0 0 90px -12px rgba(240,166,60,.55)}
.core b{font-size:clamp(1rem,2.6vw,1.35rem);font-weight:700;letter-spacing:-.02em}
.core em{font-style:normal;font-size:.72rem;opacity:.86;font-weight:600}

/* ---------- ba vòng trí nhớ ---------- */
section{padding:clamp(2.8rem,6vw,4.5rem) 0}
h2{font-size:clamp(1.45rem,3.2vw,2.1rem);line-height:1.22;margin:0 auto .8rem;max-width:22ch}
.sub{color:var(--muted);max-width:60ch;margin:0 auto 2.4rem;font-size:1rem}
.rings{display:grid;gap:.8rem;max-width:760px;margin-inline:auto}
.rg{display:grid;grid-template-columns:auto 1fr;gap:1.1rem;align-items:center;
  text-align:left;padding:1.2rem 1.5rem;border-radius:999px;
  border:1px solid var(--line);background:var(--panel);
  transition:border-color .3s var(--ease),transform .3s var(--ease)}
.rg:nth-child(1){width:100%}
.rg:nth-child(2){width:94%;margin-inline:auto}
.rg:nth-child(3){width:88%;margin-inline:auto}
.rg:hover{border-color:var(--gold);transform:scale(1.015)}
.rg .disc{width:38px;height:38px;border-radius:50%;flex-shrink:0;
  background:radial-gradient(circle at 35% 30%,var(--amber),var(--gold));
  opacity:calc(1 - var(--i) * .26)}
.rg b{display:block;font-size:1rem}
.rg code{font-size:.74rem;color:var(--gold);font-family:ui-monospace,Menlo,monospace}
.rg em{font-style:normal;display:block;font-size:.88rem;color:var(--muted);margin-top:.15rem}
.rg .cnt{margin-left:auto;font-size:.8rem;color:var(--dim);white-space:nowrap}

/* ---------- trục giữa, lệch trái phải ---------- */
.spine{position:relative;max-width:820px;margin-inline:auto;padding-top:.5rem}
.spine::before{content:'';position:absolute;left:50%;top:0;bottom:0;width:1px;
  background:linear-gradient(var(--gold),var(--line),transparent);opacity:.45}
.sp{position:relative;width:calc(50% - 2.2rem);padding:1.3rem 1.5rem;margin-bottom:1.1rem;
  border:1px solid var(--line);border-radius:16px;background:var(--panel);text-align:left;
  transition:border-color .3s var(--ease),transform .3s var(--ease)}
.sp:hover{border-color:var(--gold);transform:translateY(-3px)}
.sp:nth-child(odd){margin-right:auto}
.sp:nth-child(even){margin-left:auto}
.sp::after{content:'';position:absolute;top:1.9rem;width:11px;height:11px;border-radius:50%;
  background:var(--gold);box-shadow:0 0 0 4px var(--bg)}
.sp:nth-child(odd)::after{right:-2.75rem}
.sp:nth-child(even)::after{left:-2.75rem}
.sp b{display:block;font-size:1.05rem;margin-bottom:.35rem}
.sp p{margin:0;font-size:.92rem;color:var(--muted)}

/* ---------- vệ tinh ---------- */
.sats{display:grid;gap:.8rem;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));
  max-width:820px;margin-inline:auto}
.sat{padding:1.2rem 1rem;border-radius:16px;border:1px dashed var(--line-2);
  background:var(--panel);transition:border-color .3s var(--ease),transform .3s var(--ease)}
.sat:hover{border-color:var(--gold);border-style:solid;transform:translateY(-3px)}
.sat b{display:block;font-size:.98rem}
.sat em{font-style:normal;font-size:.82rem;color:var(--muted)}

/* ---------- công nghệ ---------- */
.stack{display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center;max-width:700px;
  margin-inline:auto}
.stack span{padding:.42rem 1rem;border-radius:999px;font-size:.84rem;color:var(--muted);
  border:1px solid var(--line);background:var(--panel);
  transition:color .25s,border-color .25s,transform .25s var(--ease)}
.stack span:hover{color:var(--text);border-color:var(--gold);transform:translateY(-2px)}

/* ---------- giới hạn + hỏi đáp ---------- */
.lims{max-width:760px;margin-inline:auto;text-align:left}
.lim{padding:1.2rem 0;border-top:1px solid var(--line)}
.lim:first-child{border-top:0}
.lim b{display:block;color:var(--amber);font-size:1rem;margin-bottom:.25rem}
.lim p{margin:0;color:var(--muted);font-size:.92rem}
.faq{max-width:760px;margin-inline:auto;text-align:left}
details{border-bottom:1px solid var(--line)}
summary{cursor:pointer;list-style:none;padding:1.05rem .2rem;font-weight:600;font-size:.97rem;
  display:flex;align-items:center;justify-content:space-between;gap:1rem}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';color:var(--gold);font-size:1.2rem;flex-shrink:0;
  transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(45deg)}
details p{margin:0;padding:0 .2rem 1.1rem;color:var(--muted);font-size:.91rem}

/* ---------- kết ---------- */
.end{border-top:1px solid var(--line)}
footer{border-top:1px solid var(--line);padding:1.8rem 0;color:var(--dim);font-size:.84rem}
footer a{color:var(--muted);text-decoration:none;padding:.3rem}
footer a:hover{color:var(--gold)}

/* Sóng lan ra từ lõi — nhắc lại ý mọi thứ toả ra từ một trung tâm. */
.orbit::before,.orbit::after{content:'';position:absolute;left:50%;top:50%;
  width:46%;aspect-ratio:1;translate:-50% -50%;border-radius:50%;
  border:1px solid rgba(240,166,60,.5);pointer-events:none;
  animation:wave 4.6s ease-out infinite}
.orbit::after{animation-delay:2.3s}
@keyframes wave{
  0%{transform:scale(1);opacity:.55}
  100%{transform:scale(2.15);opacity:0}
}
/* Lõi thở nhẹ — biên độ nhỏ để không thành thứ gây khó chịu khi đọc. */
.core{animation:breathe 5.5s ease-in-out infinite}
@keyframes breathe{50%{transform:translate(-50%,-50%) scale(1.035)}}

/* Chấm trên trục sáng dần khi cuộn tới, thay vì sáng sẵn từ đầu. */
.sp::after{background:var(--line-2);transition:background .5s var(--ease),
  box-shadow .5s var(--ease)}
.sp.in::after{background:var(--gold);box-shadow:0 0 0 4px var(--bg),0 0 16px -2px var(--gold)}

/* Thanh tiến độ đọc trang. */
.prog{position:fixed;top:0;left:0;height:2px;width:100%;z-index:70;transform:scaleX(0);
  transform-origin:0 50%;background:linear-gradient(90deg,var(--gold),var(--amber))}
@supports (animation-timeline:scroll()){
  .prog{animation:pgrow linear;animation-timeline:scroll(root block)}
  @keyframes pgrow{to{transform:scaleX(1)}}
}

/* Vệ tinh trôi nhẹ, lệch pha nhau. */
.sat{animation:float 6s ease-in-out infinite;animation-delay:calc(var(--i) * .7s)}
@keyframes float{50%{transform:translateY(-5px)}}

.rise{opacity:0;transform:translateY(20px);
  transition:opacity .7s var(--ease),transform .7s var(--ease)}
.rise.in{opacity:1;transform:none}
@media (max-width:760px){
  .spine::before{left:11px}
  /* Phải trừ đúng phần lề trái, để 100% là tràn ra ngoài đúng bằng lề đó. */
  .sp{width:calc(100% - 2.2rem);margin-left:2.2rem!important;margin-right:0!important}
  .sp::after{left:-2.75rem!important;right:auto!important}
  .rg{border-radius:16px;width:100%!important}
  .rg .cnt{margin-left:0}
}
@media (max-width:640px){
  .acts{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .rg{grid-template-columns:1fr}
  .rg .disc{display:none}
}
"""

JS = """
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -8% 0px',threshold:.06});
document.querySelectorAll('.rise').forEach(function(el,i){
  el.style.transitionDelay=(Math.min(i%5,4)*60)+'ms'; io.observe(el);
});
var cio=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting) return;
    cio.unobserve(e.target);
    var el=e.target,to=+el.dataset.to,t0=0,dur=1100;
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
<meta name="theme-color" content="#0b0a08" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='16' cy='16' r='14' fill='none' stroke='%233d3320'/><circle cx='16' cy='16' r='9' fill='none' stroke='%23f0a63c' stroke-opacity='.5'/><circle cx='16' cy='16' r='5' fill='%23f0a63c'/></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="SEOSONA OS" />
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@300..700&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>

<div class="prog" aria-hidden="true"></div>

<nav class="nav">
  <a href="#tri-nho">Trí nhớ</a>
  <a href="#nang-luc">Năng lực</a>
  <a href="#ve-tinh">Vệ tinh</a>
  <a href="#hoi-dap">Hỏi đáp</a>
  <a class="gh" href="https://github.com/$repo" target="_blank" rel="noopener">GitHub ↗</a>
</nav>

<header class="hero">
  <div class="wrap">
    <p class="kick">Bộ não trung tâm</p>
    <h1>Đổi công cụ AI mà <span class="hl">không mất trí nhớ</span></h1>
    <p class="lede">
      Cursor, Claude Code, Codex, Windsurf, Aider — mỗi cái một bộ luật, một bộ nhớ, và
      quên sạch sau mỗi phiên. SEOSONA OS đặt một bộ não chung phía dưới tất cả.
    </p>
    <div class="acts">
      <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
      <a class="btn sec" href="#tri-nho">Ba tầng trí nhớ</a>
    </div>

    <div class="orbit" role="img" aria-label="Sơ đồ: bộ não SEOSONA OS ở tâm, năm công cụ AI trên quỹ đạo quanh nó">
      <div class="ring"></div><div class="ring r2"></div><div class="ring r3"></div>
      <div class="orbit-wrap">$nodes</div>
      <div class="core"><b>SEOSONA OS</b><em>một luật · một trí nhớ</em></div>
    </div>
  </div>
</header>

<main>
  <section class="wrap" id="tri-nho">
    <h2 class="rise">Trí nhớ xếp thành ba vòng đồng tâm</h2>
    <p class="sub rise">Càng vào trong càng ít thay đổi. Lõi là bộ luật, ngoài cùng là bộ nhớ
      dự án — thứ sinh ra và mất đi liên tục.</p>
    <div class="rings">$rings</div>
  </section>

  <section class="wrap" id="nang-luc">
    <h2 class="rise">Năm việc bộ não này làm</h2>
    <div class="spine">$spine</div>
  </section>

  <section class="wrap" id="ve-tinh">
    <h2 class="rise">Bốn dự án vệ tinh</h2>
    <p class="sub rise">Chúng không tự nuôi tri thức riêng. Tất cả nối ngược về đây và truy
      vấn lúc chạy, nên sửa một chỗ là cả bốn đổi theo.</p>
    <div class="sats">$sats</div>
  </section>

  <section class="wrap">
    <h2 class="rise">Dựng bằng gì</h2>
    <div class="stack rise">$stack</div>
  </section>

  <section class="wrap">
    <h2 class="rise">Ba giới hạn bạn nên biết</h2>
    <p class="sub rise">Đây là dự án cá nhân đang phát triển, không phải sản phẩm thương mại.</p>
    <div class="lims rise">$limits</div>
  </section>

  <section class="wrap" id="hoi-dap">
    <h2 class="rise">Câu hỏi thường gặp</h2>
    <div class="faq rise">$faq</div>
  </section>

  <section class="end">
    <div class="wrap">
      <h2 class="rise">Mã nguồn mở, đọc được toàn bộ</h2>
      <p class="sub rise">Giấy phép MIT. Chạy trên Windows, macOS và Linux.</p>
      <div class="acts rise">
        <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
        <a class="btn sec" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    © 2026 Hà Đình Long — Long Leo ·
    <a href="$portfolio/">Portfolio</a> ·
    <a href="https://github.com/$repo" target="_blank" rel="noopener">GitHub</a>
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
    title = "SEOSONA OS — bộ não chung cho mọi công cụ AI trên máy"
    desc = ("Một bộ luật, một trí nhớ dùng chung cho Claude Code, Cursor, Codex, Windsurf "
            "và Aider. 2.422 file tri thức, 3.560 file bộ nhớ, tự học thêm qua pipeline.")

    step = 360 / len(TOOLS)
    nodes = "".join(
        f'<div class="node" style="--a:{i * step:.1f}deg;--r:42%">'
        f'<span>{esc(t)}</span></div>' for i, t in enumerate(TOOLS))

    rings = "".join(
        f'<div class="rg rise" style="--i:{i}"><span class="disc"></span>'
        f'<div><b>{esc(n)}</b> <code>{esc(path)}</code><em>{esc(d)}</em></div>'
        f'<span class="cnt">{esc(cnt)}</span></div>'
        for i, (n, path, cnt, d) in enumerate(RINGS))

    spine = "".join(
        f'<div class="sp rise"><b>{esc(t)}</b><p>{esc(d)}</p></div>' for t, d in SPINE)

    sats = "".join(
        f'<div class="sat rise" style="--i:{i}"><b>{esc(n)}</b><em>{esc(d)}</em></div>'
        for i, (n, d) in enumerate(SATELLITES))

    stack = "".join(f"<span>{esc(t)}</span>" for t in STACK)
    limits = "".join(f'<div class="lim"><b>{esc(t)}</b><p>{esc(d)}</p></div>'
                     for t, d in LIMITS)
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareSourceCode", "name": "SEOSONA OS", "description": desc,
             "url": SITE + "/", "image": SITE + "/cover.jpg",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": ["Python", "Node.js"],
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        css=CSS, js=JS, jsonld=jsonld, nodes=nodes, rings=rings, spine=spine,
        sats=sats, stack=stack, limits=limits, faq=faq)


def main():
    d = os.path.join(OUT, "landing")
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "seosona-os.jpg"),
                    os.path.join(d, "cover.jpg"))
    print(f"  {len(html) // 1024} KB  SEOSONA OS — bố cục hướng tâm")
    print(f"  {len(TOOLS)} công cụ trên quỹ đạo · {len(RINGS)} vòng trí nhớ · "
          f"{len(SPINE)} mục trên trục · {len(SATELLITES)} vệ tinh · phông Lexend")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
