#!/usr/bin/env python3
"""Landing page cho SEOSONA UX-UI — nền sáng, có công tắc sáng/tối.

Đây là trang duy nhất trong bộ tám để nền sáng làm mặc định, và đó là chủ ý:
sản phẩm là một hệ design token, nên cách tự giới thiệu thuyết phục nhất là
**chạy chính token đó ở cả hai chế độ ngay trên trang**. Bấm công tắc, cả trang
đổi màu bằng đúng cơ chế mà thư viện cung cấp cho người dùng nó.

Bố cục cũng khác ba trang anh em: kiểu trang tài liệu, sidebar dính bên trái,
nội dung bên phải. Phông Manrope.

    python scripts/landing-seosona-ux-ui.py
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "SEOSONA-UX-UI")
SITE = "https://seosona-ux-ui.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/SEOSONA-UX-UI"

N_COMPONENTS = 28
N_MOTION = 461
N_TOKENS = 14
N_PALETTES = 5

NAV = [("gioi-thieu", "Giới thiệu"), ("token", "Design token"), ("component", "Component"),
       ("motion", "Chuyển động"), ("dung-sao", "Dùng thế nào"),
       ("gioi-han", "Giới hạn"), ("hoi-dap", "Hỏi đáp")]

# 28 component thật, lấy từ 4_LIBRARY/components/ của repo.
CATALOG = [
    ("Thẻ", ["card-blog", "card-pricing", "card-service"]),
    ("Hero", ["hero-centered", "hero-split"]),
    ("Form", ["file-upload", "floating-labels", "form-lead-capture", "form-multistep"]),
    ("Điều hướng", ["mega-menu", "navbar-sticky"]),
    ("Tương tác", ["accordion-faq", "modal-dialog", "offcanvas-drawer",
                   "tabs-animated", "tooltip"]),
    ("Hiển thị dữ liệu", ["data-table", "timeline"]),
    ("Phản hồi", ["progress-bars", "toast-notifications"]),
    ("Media", ["masonry-grid", "parallax-section"]),
    ("Bằng chứng xã hội", ["testimonials-grid", "pricing-toggle"]),
    ("Chân trang", ["footer-full", "footer-minimal"]),
    ("Kêu gọi hành động", ["cta-fullwidth", "features-grid"]),
]

PALETTES = [
    ("B2B sáng", "#1d4ed8", "#0ea5e9", "#e2e8f0"),
    ("B2B tối", "#3b82f6", "#1e293b", "#0f172a"),
    ("B2C rực rỡ", "#ec4899", "#f59e0b", "#8b5cf6"),
    ("Fintech", "#059669", "#0f766e", "#134e4a"),
    ("Y tế", "#0891b2", "#22d3ee", "#cffafe"),
]

MOTION = [
    ("Tức thì", "100ms", "đổi màu khi rê chuột, phản hồi bấm"),
    ("Nhanh", "200ms", "hiện tooltip, đổi trạng thái nút"),
    ("Vừa", "300ms", "mở accordion, trượt drawer"),
    ("Chậm", "600ms", "hiện dần khi cuộn tới"),
    ("Điện ảnh", "1200ms", "chuyển cảnh cả trang, hiếm khi dùng"),
]

STEPS = [
    ("Chép file token", "Một file CSS custom property. Dán vào dự án, không cài gì."),
    ("Chép component cần dùng", "Mỗi component là một file HTML kèm CSS. Không có phụ thuộc."),
    ("Đổi biến màu", "Thương hiệu khác thì sửa lớp biến, cả thư viện đổi theo."),
]

LIMITS = [
    ("Không phải npm package",
     "Không có lệnh cài. Cách dùng là copy component vào dự án — đổi lại bạn sở hữu hoàn "
     "toàn đoạn mã đó và sửa được tuỳ ý."),
    ("Không có phiên bản hoá cho từng component",
     "Đã copy vào dự án thì bản đó là của bạn; thư viện cập nhật không tự đẩy sang. Đây là "
     "đánh đổi cố ý của cách làm copy-paste."),
    ("Token phản ánh nhận diện SEOSONA",
     "Bảng màu và thang chữ dựng theo hệ này. Dùng cho thương hiệu khác thì phải chỉnh lớp "
     "biến trước, không dùng thẳng được."),
]

FAQ = [
    ("Dùng được với React không?",
     "Được. Component là HTML và CSS thuần nên dán vào JSX chạy bình thường, không cần "
     "wrapper hay adapter nào."),
    ("Vì sao không đóng gói thành npm package?",
     "Vì mục tiêu là bạn sở hữu đoạn mã. Package tiện cập nhật nhưng khó sửa sâu; "
     "copy-paste thì ngược lại. Với một hệ thiết kế nội bộ, sửa sâu quan trọng hơn."),
    ("Công tắc sáng tối trên trang này chạy bằng gì?",
     "Bằng đúng cơ chế mà thư viện cung cấp: một thuộc tính trên thẻ gốc, các biến CSS đổi "
     "theo. Không có thư viện quản lý theme nào."),
    ("461 file chuyển động là những gì?",
     "Thư viện công thức motion kèm bảng thời lượng và đường cong easing chuẩn — chính bộ "
     "này cung cấp chuyển động cho trang portfolio của Long Leo."),
]

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#ffffff; --surface:#f8fafc; --surface-2:#f1f5f9; --line:#e2e8f0; --line-2:#cbd5e1;
  --text:#0f172a; --muted:#475569; --dim:#5e728e;
  --brand:#1d4ed8; --brand-soft:#dbeafe; --ok:#04845c; --warn:#b45309; --danger:#dc2626;
  --shadow:0 1px 2px rgba(15,23,42,.06),0 8px 24px -12px rgba(15,23,42,.12);
  --ease:cubic-bezier(.16,1,.3,1);
}
[data-theme="dark"]{
  --bg:#0b1120; --surface:#111c33; --surface-2:#16233d; --line:#1e293b; --line-2:#334155;
  --text:#e8eefb; --muted:#a3b3cc; --dim:#7c8ba0;
  --brand:#60a5fa; --brand-soft:#17284a; --ok:#34d399; --warn:#fbbf24; --danger:#f87171;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -12px rgba(0,0,0,.6);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;
  transition:background .35s var(--ease),color .35s var(--ease);
}
a{color:inherit}
svg{display:block}
h1,h2,h3{letter-spacing:-.03em}
:focus-visible{outline:2px solid var(--brand);outline-offset:2px;border-radius:6px}

/* ---------- khung trang tài liệu ---------- */
.top{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.top-in{display:flex;align-items:center;gap:1rem;padding:.7rem 1.4rem;max-width:1240px;
  margin-inline:auto}
.mark{display:flex;align-items:center;gap:.55rem;font-weight:800;font-size:.95rem;
  text-decoration:none}
.mark i{width:22px;height:22px;border-radius:7px;background:var(--brand);
  display:block;flex-shrink:0;
  background-image:linear-gradient(135deg,var(--brand),color-mix(in srgb,var(--brand) 50%,#22d3ee))}
.ver{font-size:.7rem;font-weight:700;color:var(--brand);background:var(--brand-soft);
  padding:.1rem .45rem;border-radius:5px}
.top .sp{margin-left:auto}
.tog{display:inline-flex;align-items:center;gap:.45rem;padding:.45rem .8rem;border-radius:8px;
  border:1px solid var(--line-2);background:var(--surface);color:var(--text);
  font:inherit;font-size:.82rem;font-weight:600;cursor:pointer;
  transition:border-color .25s,background .25s}
.tog:hover{border-color:var(--brand)}
.gh{padding:.45rem .9rem;border-radius:8px;background:var(--text);color:var(--bg);
  font-size:.82rem;font-weight:700;text-decoration:none;
  transition:opacity .25s}
.gh:hover{opacity:.85}

.shell{display:grid;grid-template-columns:212px minmax(0,1fr);gap:2.5rem;
  max-width:1240px;margin-inline:auto;padding:0 1.4rem}
.side{position:sticky;top:60px;align-self:start;padding:2rem 0;font-size:.87rem}
.side a{display:block;padding:.4rem .7rem;border-radius:7px;color:var(--muted);
  text-decoration:none;border-left:2px solid transparent;
  transition:color .2s,background .2s,border-color .2s}
.side a:hover{color:var(--text);background:var(--surface)}
.side a.on{color:var(--brand);border-left-color:var(--brand);font-weight:700}
.main{padding:2rem 0 3rem;min-width:0}

section{padding-bottom:clamp(2.5rem,5vw,3.6rem);scroll-margin-top:70px}
h1{font-size:clamp(1.9rem,4.4vw,2.9rem);line-height:1.1;margin:0 0 1rem;font-weight:800}
h1 .hl{color:var(--brand)}
.lede{color:var(--muted);font-size:clamp(1rem,1.8vw,1.12rem);max-width:60ch;margin:0 0 1.6rem}
h2{font-size:clamp(1.25rem,2.6vw,1.6rem);margin:0 0 .5rem;font-weight:700}
.sub{color:var(--muted);margin:0 0 1.5rem;max-width:64ch;font-size:.95rem}
.acts{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:2rem}
.btn{display:inline-flex;align-items:center;gap:.45rem;padding:.7rem 1.3rem;border-radius:10px;
  font-size:.9rem;font-weight:700;text-decoration:none;border:1px solid transparent;
  transition:transform .2s var(--ease),box-shadow .2s,background .2s,border-color .2s}
.btn:hover{transform:translateY(-2px)}
.btn.pri{background:var(--brand);color:#fff}
.btn.pri:hover{box-shadow:0 12px 26px -12px var(--brand)}
.btn.sec{border-color:var(--line-2);background:var(--bg)}
.btn.sec:hover{border-color:var(--brand);color:var(--brand)}

/* ---------- số liệu dạng dòng ---------- */
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));
  border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface)}
.fact{padding:1rem 1.1rem;border-right:1px solid var(--line)}
.fact:last-child{border-right:0}
.fact b{display:block;font-size:1.7rem;font-weight:800;line-height:1.15;color:var(--brand);
  font-variant-numeric:tabular-nums}
.fact span{font-size:.78rem;color:var(--dim);font-weight:600}

/* ---------- khối xem trước ---------- */
.demo{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--bg);
  box-shadow:var(--shadow)}
.demo-h{display:flex;align-items:center;gap:.5rem;padding:.5rem .9rem;
  border-bottom:1px solid var(--line);background:var(--surface);font-size:.75rem;
  color:var(--dim);font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.demo-b{padding:1.3rem;display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}
.d-btn{padding:.5rem 1.1rem;border-radius:9px;font-size:.85rem;font-weight:700;
  transition:transform .2s var(--ease),filter .2s}
.d-btn:hover{transform:translateY(-2px);filter:brightness(1.06)}
.d-btn.p{background:var(--brand);color:#fff}
.d-btn.s{background:var(--surface-2);color:var(--text);border:1px solid var(--line-2)}
.d-btn.g{color:var(--brand)}
.d-bd{padding:.22rem .7rem;border-radius:999px;font-size:.75rem;font-weight:700}
.d-bd.ok{background:color-mix(in srgb,var(--ok) 14%,transparent);color:var(--ok)}
.d-bd.wa{background:color-mix(in srgb,var(--warn) 14%,transparent);color:var(--warn)}
.d-bd.er{background:color-mix(in srgb,var(--danger) 14%,transparent);color:var(--danger)}
.d-in{flex:1;min-width:170px;padding:.55rem .85rem;border-radius:9px;
  border:1px solid var(--line-2);background:var(--bg);color:var(--dim);font-size:.85rem}
.d-pg{flex:1;min-width:130px;height:8px;border-radius:99px;background:var(--surface-2);
  overflow:hidden}
.d-pg i{display:block;height:100%;width:72%;border-radius:99px;background:var(--brand);
  transform-origin:0 50%;animation:gw 1.5s var(--ease) both}
@keyframes gw{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.d-card{flex:1;min-width:210px;border:1px solid var(--line);border-radius:12px;padding:1rem;
  background:var(--surface)}
.d-card b{display:block;font-size:.95rem;margin-bottom:.2rem}
.d-card em{font-style:normal;font-size:.83rem;color:var(--muted)}

/* ---------- token ---------- */
.pals{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(min(210px,100%),1fr))}
.pal{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--surface);
  transition:transform .25s var(--ease),border-color .25s}
.pal:hover{transform:translateY(-3px);border-color:var(--brand)}
.pal .sw{display:flex;height:52px}
.pal .sw i{flex:1}
.pal b{display:block;padding:.6rem .9rem;font-size:.86rem;font-weight:700}
.scale{display:grid;gap:.35rem;margin-top:1rem}
.sc{display:flex;align-items:baseline;gap:1rem;padding:.5rem .9rem;border-radius:9px;
  background:var(--surface);font-size:.8rem;color:var(--dim)}
.sc b{color:var(--text);font-weight:800;flex:1}

/* ---------- danh mục component ---------- */
.cat{border:1px solid var(--line);border-radius:12px;margin-bottom:.5rem;background:var(--surface)}
.cat summary{cursor:pointer;list-style:none;padding:.8rem 1.1rem;font-weight:700;font-size:.92rem;
  display:flex;align-items:center;gap:.7rem}
.cat summary::-webkit-details-marker{display:none}
.cat summary::after{content:attr(data-n);margin-left:auto;font-size:.75rem;color:var(--dim);
  font-weight:700}
.cat ul{list-style:none;margin:0;padding:0 1.1rem .9rem;display:flex;flex-wrap:wrap;gap:.35rem}
.cat li{font-family:ui-monospace,Menlo,monospace;font-size:.78rem;color:var(--muted);
  background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:.2rem .55rem}

/* ---------- bảng chuyển động ---------- */
.mo{width:100%;border-collapse:collapse;font-size:.87rem}
.mo th{text-align:left;padding:.55rem .8rem;border-bottom:1px solid var(--line-2);
  font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--dim)}
.mo td{padding:.6rem .8rem;border-bottom:1px solid var(--line)}
.mo tr:last-child td{border-bottom:0}
.mo .du{font-family:ui-monospace,Menlo,monospace;color:var(--brand);font-weight:700}
.mo .bar{display:block;height:6px;border-radius:99px;background:var(--brand);opacity:.3;
  width:var(--w)}

/* ---------- các bước ---------- */
.steps{counter-reset:s;display:grid;gap:.6rem}
.st{counter-increment:s;display:flex;gap:.9rem;padding:.95rem 1.1rem;border-radius:12px;
  border:1px solid var(--line);background:var(--surface)}
.st::before{content:counter(s);flex-shrink:0;width:24px;height:24px;border-radius:7px;
  background:var(--brand);color:#fff;display:grid;place-items:center;font-size:.78rem;
  font-weight:800}
.st b{display:block;font-size:.93rem}
.st em{font-style:normal;font-size:.86rem;color:var(--muted)}

/* ---------- giới hạn + hỏi đáp ---------- */
.lim{padding:1rem 0;border-top:1px solid var(--line)}
.lim:first-child{border-top:0}
.lim b{display:block;color:var(--warn);font-size:.97rem;margin-bottom:.2rem}
.lim p{margin:0;color:var(--muted);font-size:.9rem}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;padding:.95rem .1rem;font-weight:700;font-size:.94rem;
  display:flex;justify-content:space-between;gap:1rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+';color:var(--brand);font-size:1.15rem;flex-shrink:0;
  transition:transform .3s var(--ease)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq p{margin:0;padding:0 .1rem 1rem;color:var(--muted);font-size:.9rem}

footer{border-top:1px solid var(--line);padding:1.8rem 1.4rem;color:var(--dim);font-size:.84rem}
.foot{max-width:1240px;margin-inline:auto;display:flex;flex-wrap:wrap;gap:.8rem;
  justify-content:space-between}
footer a{display:inline-block;padding:.4rem .1rem;color:var(--muted);text-decoration:none}
footer a:hover{color:var(--brand)}

/* Bảng thời lượng tự diễn: mỗi thanh chạy đúng bằng thời lượng nó mô tả.
   Với một hệ design token thì đây là cách trung thực nhất — bảng không mô tả
   chuyển động, nó LÀ chuyển động. */
.mo .bar{transform-origin:0 50%;animation:demo 3.4s var(--ease) infinite}
.mo tr:nth-child(1) .bar{animation-duration:2.4s}
.mo tr:nth-child(2) .bar{animation-duration:2.6s}
.mo tr:nth-child(3) .bar{animation-duration:2.9s}
.mo tr:nth-child(4) .bar{animation-duration:3.4s}
.mo tr:nth-child(5) .bar{animation-duration:4.6s}
@keyframes demo{0%,8%{transform:scaleX(0);opacity:.28}
  55%,72%{transform:scaleX(1);opacity:.75}100%{transform:scaleX(1);opacity:.28}}

/* Khối chờ nhấp nháy — component thật của thư viện, và cũng là chuyển động. */
.skel{display:grid;gap:.45rem;flex:1;min-width:170px}
.skel i{position:relative;display:block;height:9px;border-radius:99px;overflow:hidden;
  background:var(--surface-2)}
/* Vệt sáng chạy bằng transform, KHÔNG bằng background-position: cái sau buộc
   trình duyệt vẽ lại nền mỗi khung hình, cái này chạy ngoài luồng chính. */
.skel i::after{content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,var(--line),transparent);
  transform:translateX(-100%);animation:shim 1.5s linear infinite}
.skel i:nth-child(2){width:78%}
.skel i:nth-child(3){width:52%}
@keyframes shim{to{transform:translateX(100%)}}

/* Thông báo trượt vào rồi lui ra, lặp lại. */
.toast{display:inline-flex;align-items:center;gap:.5rem;padding:.5rem .9rem;border-radius:10px;
  border:1px solid var(--line);background:var(--surface);font-size:.84rem;
  animation:toast 5.5s var(--ease) infinite}
.toast i{width:7px;height:7px;border-radius:50%;background:var(--ok);flex-shrink:0}
@keyframes toast{
  0%,4%{opacity:0;transform:translateY(10px)}
  12%,60%{opacity:1;transform:none}
  74%,100%{opacity:0;transform:translateY(-8px)}
}

/* Thanh tiến độ đọc trang. */
.prog{position:fixed;top:0;left:0;height:2px;width:100%;z-index:70;transform:scaleX(0);
  transform-origin:0 50%;background:var(--brand)}
@supports (animation-timeline:scroll()){
  .prog{animation:pgrow linear;animation-timeline:scroll(root block)}
  @keyframes pgrow{to{transform:scaleX(1)}}
}

/* Ô màu lật nhẹ khi rê chuột — đã có, thêm nhịp cho cả hàng. */
.pal:hover .sw i{animation:tilt .6s var(--ease)}
@keyframes tilt{50%{transform:translateY(-4px)}}

.rise{opacity:0;transform:translateY(16px);
  transition:opacity .6s var(--ease),transform .6s var(--ease)}
.rise.in{opacity:1;transform:none}
@media (max-width:900px){
  .shell{grid-template-columns:1fr;gap:0}
  .side{display:none}
}
@media (max-width:640px){
  .acts{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .fact{border-right:0;border-bottom:1px solid var(--line)}
}
"""

JS = """
// Công tắc sáng/tối chạy bằng đúng cơ chế thư viện cung cấp: một thuộc tính
// trên thẻ gốc, biến CSS đổi theo. Không thư viện quản lý theme nào.
var root=document.documentElement;
function setTheme(t){
  root.setAttribute('data-theme',t);
  try{ localStorage.setItem('sx-theme',t); }catch(e){}
  var b=document.getElementById('tog');
  b.textContent = t==='dark' ? '☀ Sáng' : '☾ Tối';
  b.setAttribute('aria-label', t==='dark' ? 'Chuyển sang nền sáng' : 'Chuyển sang nền tối');
}
// Cố ý KHÔNG theo chế độ của hệ điều hành. Bảy trang anh em đều nền tối; trang
// này mở ra sáng là một tuyên bố — một hệ design token tự chứng minh nó chạy
// được cả hai chế độ. Ai đã bấm công tắc thì tôn trọng lựa chọn của họ.
var saved=null;
try{ saved=localStorage.getItem('sx-theme'); }catch(e){}
setTheme(saved || 'light');
document.getElementById('tog').addEventListener('click',function(){
  setTheme(root.getAttribute('data-theme')==='dark' ? 'light' : 'dark');
});

var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -8% 0px',threshold:.06});
document.querySelectorAll('.rise').forEach(function(el){ io.observe(el); });

// Sidebar tự đánh dấu mục đang xem.
var links=[].slice.call(document.querySelectorAll('.side a'));
var spy=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting) return;
    links.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href')==='#'+e.target.id); });
  });
},{rootMargin:'-15% 0px -70% 0px'});
document.querySelectorAll('section[id]').forEach(function(s){ spy.observe(s); });

var cio=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting) return;
    cio.unobserve(e.target);
    var el=e.target,to=+el.dataset.to,t0=0,dur=1000;
    requestAnimationFrame(function step(t){
      if(!t0) t0=t;
      var p=Math.min((t-t0)/dur,1);
      el.textContent=Math.round(to*(1-Math.pow(1-p,3)));
      if(p<1) requestAnimationFrame(step);
    });
  });
},{threshold:.5});
document.querySelectorAll('[data-to]').forEach(function(el){ cio.observe(el); });
"""

PAGE = Template("""<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>$title</title>
<meta name="description" content="$desc" />
<meta name="author" content="Hà Đình Long" />
<meta name="theme-color" content="#ffffff" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%231d4ed8'/><rect x='7' y='7' width='8' height='8' rx='2' fill='%23fff'/><rect x='17' y='7' width='8' height='8' rx='2' fill='%23fff' fill-opacity='.55'/><rect x='7' y='17' width='8' height='8' rx='2' fill='%23fff' fill-opacity='.55'/><rect x='17' y='17' width='8' height='8' rx='2' fill='%23fff' fill-opacity='.3'/></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="SEOSONA UX-UI" />
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>

<div class="prog" aria-hidden="true"></div>

<div class="top">
  <div class="top-in">
    <a class="mark" href="#gioi-thieu"><i></i> SEOSONA UX-UI <span class="ver">v1.0</span></a>
    <span class="sp"></span>
    <button class="tog" id="tog" type="button">☾ Tối</button>
    <a class="gh" href="https://github.com/$repo" target="_blank" rel="noopener">GitHub ↗</a>
  </div>
</div>

<div class="shell">
  <aside class="side">$nav</aside>

  <main class="main">
    <section id="gioi-thieu">
      <h1>Component <span class="hl">không trói</span> bạn vào framework nào</h1>
      <p class="lede">
        Thư viện UI thường bắt bạn chọn phe. Cái này thì không: HTML, CSS custom property
        và Vanilla JS thuần, nên dán vào React, Next.js, Vue hay một trang tĩnh đều chạy
        như nhau.
      </p>
      <div class="acts">
        <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
        <a class="btn sec" href="#component">Xem 28 component</a>
      </div>
      <div class="facts">
        <div class="fact"><b data-to="$n_components">0</b><span>COMPONENT</span></div>
        <div class="fact"><b data-to="$n_motion">0</b><span>FILE CHUYỂN ĐỘNG</span></div>
        <div class="fact"><b data-to="$n_tokens">0</b><span>FILE TOKEN</span></div>
        <div class="fact"><b data-to="$n_palettes">0</b><span>BẢNG MÀU</span></div>
      </div>
      <p class="sub" style="margin-top:1.4rem">
        <b>Công tắc ở góc trên bên phải đổi cả trang này.</b> Nó chạy bằng đúng cơ chế mà
        thư viện cung cấp — một thuộc tính trên thẻ gốc, biến CSS đổi theo. Đó là cách
        trung thực nhất để một hệ design token tự giới thiệu.
      </p>
    </section>

    <section id="token">
      <h2 class="rise">Design token</h2>
      <p class="sub rise">Nền móng của cả hệ. Đổi thương hiệu là đổi lớp biến, không phải
        sửa từng component.</p>
      <div class="pals rise">$pals</div>
      <div class="scale rise">$scale</div>
    </section>

    <section id="component">
      <h2 class="rise">Component</h2>
      <p class="sub rise">Xem trước dựng ngay tại đây bằng chính token bên trên — đổi công
        tắc sáng tối thì những thứ dưới đây đổi theo.</p>
      <div class="demo rise">
        <div class="demo-h">Nút · Huy hiệu · Ô nhập · Tiến độ · Thẻ</div>
        <div class="demo-b">
          <span class="d-btn p">Bắt đầu</span>
          <span class="d-btn s">Tài liệu</span>
          <span class="d-btn g">Huỷ</span>
          <span class="d-bd ok">Đang chạy</span>
          <span class="d-bd wa">Chờ duyệt</span>
          <span class="d-bd er">Lỗi</span>
        </div>
        <div class="demo-b" style="border-top:1px solid var(--line)">
          <span class="d-in">Nhập địa chỉ email…</span>
          <span class="d-pg"><i></i></span>
        </div>
        <div class="demo-b" style="border-top:1px solid var(--line)">
          <span class="skel"><i></i><i></i><i></i></span>
          <span class="toast"><i></i> Đã lưu thay đổi</span>
        </div>
        <div class="demo-b" style="border-top:1px solid var(--line)">
          <span class="d-card"><b>Thẻ dịch vụ</b><em>Một trong 28 component, dùng chung token với mọi thứ còn lại.</em></span>
          <span class="d-card"><b>Thẻ bảng giá</b><em>Có sẵn trạng thái hover, focus và disabled.</em></span>
        </div>
      </div>
      <p class="sub rise" style="margin-top:1.5rem">Toàn bộ danh mục, phân theo chức năng:</p>
      $catalog
    </section>

    <section id="motion">
      <h2 class="rise">Chuyển động</h2>
      <p class="sub rise">Bảng thời lượng chuẩn. Chuyển động trong một sản phẩm phải cùng
        nhịp, không mỗi chỗ một kiểu.</p>
      <div class="rise"><table class="mo">
        <thead><tr><th>Tên</th><th>Thời lượng</th><th>Dùng cho</th><th></th></tr></thead>
        <tbody>$motion</tbody>
      </table></div>
    </section>

    <section id="dung-sao">
      <h2 class="rise">Dùng thế nào</h2>
      <p class="sub rise">Ba bước, không có bước cài đặt.</p>
      <div class="steps rise">$steps</div>
    </section>

    <section id="gioi-han">
      <h2 class="rise">Ba giới hạn bạn nên biết</h2>
      <div class="rise">$limits</div>
    </section>

    <section id="hoi-dap">
      <h2 class="rise">Câu hỏi thường gặp</h2>
      <div class="faq rise">$faq</div>
    </section>

    <section>
      <h2 class="rise">Mã nguồn mở, copy là dùng</h2>
      <p class="sub rise">Không có lệnh cài, không có phụ thuộc. Toàn bộ nằm trên GitHub.</p>
      <div class="acts rise">
        <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
        <a class="btn sec" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
      </div>
    </section>
  </main>
</div>

<footer>
  <div class="foot">
    <span>© 2026 Hà Đình Long — Long Leo</span>
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
    title = "SEOSONA UX-UI — thư viện component không ràng buộc framework"
    desc = ("28 component và hệ design token viết bằng HTML, CSS custom property và Vanilla "
            "JS. Dán vào React, Next.js, Vue hay trang tĩnh đều chạy như nhau.")

    nav = "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t in NAV)
    pals = "".join(
        f'<div class="pal"><div class="sw"><i style="background:{a}"></i>'
        f'<i style="background:{b}"></i><i style="background:{c}"></i></div>'
        f'<b>{esc(n)}</b></div>' for n, a, b, c in PALETTES)

    scale = "".join(
        f'<div class="sc"><b style="font-size:{px}px">Thang chữ {lb}</b>'
        f'<span>{px}px · clamp()</span></div>'
        for lb, px in [("hero", 40), ("tiêu đề", 28), ("mục", 20), ("thân", 16), ("chú", 13)])

    catalog = "".join(
        f'<details class="cat"><summary data-n="{len(items)}">{esc(name)}</summary><ul>' +
        "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></details>"
        for name, items in CATALOG)

    motion = "".join(
        f'<tr><td>{esc(n)}</td><td class="du">{esc(d)}</td><td>{esc(u)}</td>'
        f'<td><i class="bar" style="--w:{min(100, int(d[:-2]) / 12)}%"></i></td></tr>'
        for n, d, u in MOTION)

    steps = "".join(
        f'<div class="st"><div><b>{esc(t)}</b><em>{esc(d)}</em></div></div>'
        for t, d in STEPS)
    limits = "".join(f'<div class="lim"><b>{esc(t)}</b><p>{esc(d)}</p></div>'
                     for t, d in LIMITS)
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareSourceCode", "name": "SEOSONA UX-UI", "description": desc,
             "url": SITE + "/", "image": SITE + "/cover.jpg",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": ["HTML", "CSS", "JavaScript"],
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        css=CSS, js=JS, jsonld=jsonld, nav=nav, pals=pals, scale=scale,
        catalog=catalog, motion=motion, steps=steps, limits=limits, faq=faq,
        n_components=N_COMPONENTS, n_motion=N_MOTION, n_tokens=N_TOKENS,
        n_palettes=N_PALETTES)


def main():
    d = os.path.join(OUT, "landing")
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "seosona-ux-ui.jpg"),
                    os.path.join(d, "cover.jpg"))
    total = sum(len(i) for _, i in CATALOG)
    print(f"  {len(html) // 1024} KB  SEOSONA UX-UI — nền sáng + công tắc")
    print(f"  {total} component / {len(CATALOG)} nhóm · {len(PALETTES)} bảng màu · "
          f"{len(MOTION)} mức chuyển động · phông Manrope")
    if total != N_COMPONENTS:
        print(f"  CẢNH BÁO: danh mục có {total} mục nhưng số liệu ghi {N_COMPONENTS}")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
