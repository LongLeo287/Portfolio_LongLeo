#!/usr/bin/env python3
"""Landing page cho SEOSONA Video AI — mô-típ dải film.

Sản phẩm là một dây chuyền sản xuất video, nên trang được dựng như một cuộn
phim: dải khung 16:9 trôi ngang trong hero, lỗ răng cưa hai bên, bốn lớp kiến
trúc xếp thành các track trên trục thời gian, mười đặc vụ đánh số như cảnh
quay. Không có sidebar, không có quỹ đạo, không có terminal — những thứ đó
thuộc về ba trang anh em. Phông Be Vietnam Pro.

    python scripts/landing-seosona-video-ai.py
"""
import io
import json
import os
import shutil
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "SEOSONA-Video-AI")
SITE = "https://seosona-video-ai.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/SEOSONA-Video-AI"

N_AGENTS = 10
N_SOP = 34
N_FRAMEWORK = 913
N_FILES = 2352

# Khung trong dải film hero — mỗi khung một bước của dây chuyền.
FRAMES = [
    ("01", "Nghiên cứu", "bám xu hướng, gom tư liệu"),
    ("02", "Kịch bản", "viết theo giọng thương hiệu"),
    ("03", "Hình ảnh", "sinh cảnh, giữ nhân vật nhất quán"),
    ("04", "Lồng tiếng", "định tuyến giữa nhiều bộ đọc"),
    ("05", "Dựng", "cắt, chèn chữ, chuyển cảnh"),
    ("06", "Kết xuất", "9 bộ render, nhiều tỉ lệ khung"),
    ("07", "Thumbnail", "quy trình riêng cho ảnh đại diện"),
    ("08", "Đăng", "YouTube và Google Drive"),
    ("09", "Đo", "số liệu quay ngược vào vòng cải tiến"),
]

# Bốn lớp, vẽ thành bốn track trên trục thời gian.
TRACKS = [
    ("Nhận thức", "Cognitive", 0, 34, "nghiên cứu · ý tưởng · kịch bản"),
    ("Thực thi", "Execution", 18, 46, "10 đặc vụ · 7 kỹ năng Python"),
    ("Luồng công việc", "Workflow", 40, 40, "21 luồng · 34 quy trình vận hành"),
    ("Kết xuất", "Rendering", 62, 38, "9 bộ render · FFmpeg · TTS · Whisper"),
]

AGENTS = [
    ("Hermes", "điều phối toàn dây chuyền, có bản chạy nền và bản điều khiển qua Telegram"),
    ("Scraper", "thu thập tư liệu và nguồn tham khảo"),
    ("Trend Jacking", "theo dõi xu hướng để bám sóng đúng lúc"),
    ("SEO Writer", "viết nội dung tối ưu tìm kiếm"),
    ("Carousel Writer", "viết nội dung nhiều trang cho mạng xã hội"),
    ("Social Media", "biên tập lại cho từng nền tảng"),
    ("Repurposer", "phân tích phụ đề, cắt video dài thành video ngắn"),
    ("SEO Optimizer", "tối ưu tiêu đề, mô tả và thẻ cho YouTube"),
    ("Publisher", "đăng lên YouTube và Google Drive"),
    ("Analytics Feedback", "đọc số liệu sau khi đăng, đưa ngược vào vòng cải tiến"),
]

SOPS = ["Video tin tức", "Video không mặt", "Talking head", "Video khoá học",
        "Video quảng cáo", "Carousel", "Thumbnail", "Lồng tiếng và nhân bản giọng",
        "Cắt lại video dài", "Giọng thương hiệu", "Kiểm tra trước khi đăng",
        "Vận hành kênh YouTube"]

LIMITS = [
    ("Hệ thống nội bộ, không phải sản phẩm cài đặt",
     "Không bộ cài, không giao diện đồ hoạ. Muốn dùng phải đọc tài liệu kiến trúc rồi tự "
     "nối các mảnh vào quy trình của mình."),
    ("Phụ thuộc nhiều dịch vụ bên ngoài",
     "Bộ đọc giọng, mô hình sinh ảnh, API đăng bài — mỗi cái một tài khoản và một hạn mức "
     "riêng. Hệ chỉ điều phối, không đi kèm cái nào."),
    ("Tự động hoá phần lặp, không tự động hoá phần hay",
     "Nó lo cắt ghép, kết xuất và đặt tên file. Ý tưởng, giọng điệu và quyết định giữ hay "
     "bỏ vẫn là việc của người."),
]

FAQ = [
    ("Nó tự làm ra video hoàn chỉnh được không?",
     "Được, với những định dạng đã có quy trình sẵn như video tin tức hay video không mặt. "
     "Nhưng đầu ra vẫn cần người duyệt — hệ tối ưu cho tốc độ, không thay được con mắt biên tập."),
    ("Vì sao chia làm bốn lớp?",
     "Để đổi một phần không kéo sập phần khác. Bộ kết xuất thay đổi liên tục theo công cụ "
     "mới, còn phần nghiên cứu và viết kịch bản thì ổn định — nhốt chúng chung một chỗ là "
     "mỗi lần đổi công cụ lại phải sửa cả hệ."),
    ("34 quy trình vận hành là gì?",
     "Tài liệu quy định cách làm từng loại nội dung: chuẩn thẩm mỹ, thứ tự các bước, điều "
     "kiện dừng. Chúng giữ cho đầu ra tự động không trôi khỏi chuẩn qua thời gian."),
    ("Có chạy được trên máy người khác không?",
     "Mã nguồn mở nên tải về được, nhưng phải tự cấu hình các tài khoản dịch vụ và đường "
     "dẫn. Không phải cài là chạy."),
]

STACK = ["Python", "FFmpeg", "Puppeteer", "Whisper", "VieNeu-TTS", "HyperFrames",
         "MCP", "Google Drive API", "YouTube API"]

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0a0806; --film:#12100d; --film-2:#1a1613; --line:#272119; --line-2:#3b3126;
  --text:#fdf9f3; --muted:#b3a693; --dim:#8f8170;
  --hot:#f2683a; --gold:#fcd34d; --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Be Vietnam Pro',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;
}
a{color:inherit}
svg{display:block}
.wrap{width:min(1080px,100% - 2.4rem);margin-inline:auto}
h1,h2,h3{letter-spacing:-.03em;font-weight:800}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px}

/* ---------- thanh trên: kiểu slate quay phim ---------- */
.slate{display:flex;align-items:center;gap:.9rem;padding:.7rem 0;
  border-bottom:1px solid var(--line);background:var(--film);
  position:sticky;top:0;z-index:50}
.slate-in{display:flex;align-items:center;gap:.9rem;
  width:min(1080px,100% - 2.4rem);margin-inline:auto;font-size:.8rem}
.clap{width:26px;height:20px;flex-shrink:0;border-radius:3px;overflow:hidden;
  background:repeating-linear-gradient(115deg,#fdf9f3 0 6px,#0a0806 6px 12px)}
.slate b{font-weight:800;letter-spacing:-.01em}
.slate .meta{color:var(--dim);font-family:ui-monospace,Menlo,monospace;font-size:.74rem}
.slate a{margin-left:auto;padding:.4rem .9rem;border-radius:4px;background:var(--hot);
  color:#0a0806;font-weight:700;text-decoration:none;font-size:.8rem;
  transition:transform .2s var(--ease),box-shadow .2s}
.slate a:hover{transform:translateY(-1px);box-shadow:0 8px 20px -10px var(--hot)}

/* ---------- hero ---------- */
.hero{padding:clamp(2.5rem,6vw,4.5rem) 0 0;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:auto -20% -30% -20%;height:70%;
  background:radial-gradient(50% 60% at 50% 100%,rgba(242,104,58,.2),transparent 70%);
  pointer-events:none}
.hero .wrap{position:relative}
.tag{display:inline-flex;align-items:center;gap:.5rem;font-family:ui-monospace,Menlo,monospace;
  font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);
  margin:0 0 1.2rem}
.tag::before{content:'●';color:var(--hot);animation:rec 1.8s ease-in-out infinite}
@keyframes rec{50%{opacity:.25}}
h1{font-size:clamp(2rem,5.4vw,3.7rem);line-height:1.04;margin:0 0 1.1rem;max-width:17ch}
h1 .hl{color:var(--hot)}
.lede{color:var(--muted);font-size:clamp(1rem,1.9vw,1.16rem);max-width:58ch;margin:0 0 1.8rem}
.acts{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:2.4rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.5rem;border-radius:6px;
  font-size:.92rem;font-weight:700;text-decoration:none;border:1px solid transparent;
  transition:transform .22s var(--ease),background .22s,border-color .22s,box-shadow .22s}
.btn:hover{transform:translateY(-2px)}
.btn.pri{background:var(--hot);color:#0a0806}
.btn.pri:hover{box-shadow:0 14px 32px -14px var(--hot)}
.btn.sec{border-color:var(--line-2);color:var(--text)}
.btn.sec:hover{border-color:var(--gold);color:var(--gold)}

/* ---------- dải film trôi ngang ---------- */
.strip{position:relative;padding:.9rem 0;margin-bottom:clamp(2rem,5vw,3rem);
  background:var(--film);border-block:1px solid var(--line);overflow:hidden}
/* Lỗ răng cưa hai mép — vẽ bằng gradient lặp, không cần ảnh. */
.strip::before,.strip::after{content:'';position:absolute;left:0;right:0;height:11px;
  background:repeating-linear-gradient(90deg,transparent 0 9px,
    var(--bg) 9px 21px);opacity:.85;z-index:2}
.strip::before{top:0}
.strip::after{bottom:0}
.strip-in{display:flex;gap:.7rem;width:max-content;padding-block:.8rem;
  animation:roll 46s linear infinite}
.strip:hover .strip-in{animation-play-state:paused}
@keyframes roll{to{transform:translateX(-50%)}}
.fr{width:210px;flex-shrink:0;aspect-ratio:16/9;border:1px solid var(--line-2);
  border-radius:3px;background:linear-gradient(150deg,var(--film-2),#0d0b09);
  padding:.75rem .85rem;display:flex;flex-direction:column;justify-content:space-between;
  transition:border-color .25s var(--ease),transform .25s var(--ease)}
.fr:hover{border-color:var(--hot);transform:translateY(-3px)}
.fr .no{font-family:ui-monospace,Menlo,monospace;font-size:.68rem;color:var(--hot);
  letter-spacing:.1em}
.fr b{font-size:.95rem;line-height:1.25}
.fr em{font-style:normal;font-size:.75rem;color:var(--dim);line-height:1.4}

/* ---------- số liệu như bảng đọc máy ---------- */
.gauges{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--film)}
.ga{padding:1.05rem 1.15rem;border-right:1px solid var(--line)}
.ga:last-child{border-right:0}
.ga b{display:block;font-size:1.75rem;font-weight:800;color:var(--gold);line-height:1.15;
  font-variant-numeric:tabular-nums}
.ga span{font-size:.73rem;color:var(--dim);letter-spacing:.06em;font-weight:600}

/* ---------- mục ---------- */
section{padding:clamp(2.8rem,6vw,4.5rem) 0}
.shot{font-family:ui-monospace,Menlo,monospace;font-size:.72rem;letter-spacing:.14em;
  color:var(--hot);margin:0 0 .6rem}
h2{font-size:clamp(1.5rem,3.3vw,2.2rem);line-height:1.18;margin:0 0 .7rem;max-width:22ch}
.sub{color:var(--muted);max-width:64ch;margin:0 0 2rem;font-size:1rem}

/* ---------- bốn track trên trục thời gian ---------- */
.tl{border:1px solid var(--line);border-radius:8px;background:var(--film);padding:1.1rem}
.ruler{display:flex;justify-content:space-between;font-family:ui-monospace,Menlo,monospace;
  font-size:.66rem;color:var(--dim);padding:0 0 .6rem;border-bottom:1px solid var(--line);
  margin-bottom:.8rem}
.trk{display:grid;grid-template-columns:150px 1fr;gap:1rem;align-items:center;
  margin-bottom:.55rem}
.trk-lb b{display:block;font-size:.92rem;line-height:1.2}
.trk-lb em{font-style:normal;font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--dim)}
.trk-bar{position:relative;height:38px;border-radius:5px;background:#0d0b09;
  border:1px solid var(--line)}
.trk-bar i{position:absolute;top:4px;bottom:4px;left:calc(var(--s) * 1%);
  width:calc(var(--w) * 1%);border-radius:3px;display:flex;align-items:center;
  padding-inline:.7rem;font-size:.74rem;color:#0a0806;font-weight:600;white-space:nowrap;
  overflow:hidden;
  background:linear-gradient(90deg,var(--hot),var(--gold));
  transform-origin:0 50%;animation:grow 1s var(--ease) both;
  animation-delay:calc(var(--i) * .13s)}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
/* Đầu đọc chạy bằng transform, KHÔNG bằng left: động tới left buộc trình
   duyệt tính lại bố cục mỗi khung hình. Mẹo: cho phần tử rộng bằng cả khung
   rồi vẽ vạch sáng ở mép trái, lúc đó translateX(100%) đi đúng một khung. */
.playhead{position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(90deg,var(--gold) 0 1px,transparent 1px);
  filter:drop-shadow(0 0 6px var(--gold));
  animation:scrub 9s linear infinite}
@keyframes scrub{to{transform:translateX(100%)}}
.tl-wrap{position:relative}

/* ---------- đặc vụ, đánh số như cảnh quay ---------- */
.cast{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
  border-radius:8px;overflow:hidden}
.mem{display:grid;grid-template-columns:44px 170px 1fr;gap:1rem;align-items:center;
  padding:.85rem 1.1rem;background:var(--film);transition:background .25s var(--ease)}
.mem:hover{background:var(--film-2)}
.mem .n{font-family:ui-monospace,Menlo,monospace;font-size:.75rem;color:var(--hot)}
.mem b{font-size:.94rem}
.mem em{font-style:normal;font-size:.87rem;color:var(--muted)}

/* ---------- quy trình ---------- */
.sops{display:flex;flex-wrap:wrap;gap:.45rem}
.sops span{padding:.45rem 1rem;border-radius:4px;font-size:.85rem;color:var(--muted);
  border:1px solid var(--line);background:var(--film);
  transition:color .25s,border-color .25s,transform .25s var(--ease)}
.sops span:hover{color:var(--gold);border-color:var(--gold);transform:translateY(-2px)}
.stack{display:flex;flex-wrap:wrap;gap:.45rem}
.stack span{padding:.4rem .9rem;border-radius:999px;font-size:.83rem;color:var(--dim);
  border:1px solid var(--line-2);transition:color .25s,border-color .25s}
.stack span:hover{color:var(--hot);border-color:var(--hot)}

/* ---------- giới hạn + hỏi đáp ---------- */
.lims{border-left:3px solid var(--gold);padding-left:1.4rem}
.lim{padding:1rem 0;border-top:1px solid var(--line)}
.lim:first-child{border-top:0;padding-top:0}
.lim b{display:block;color:var(--gold);font-size:1rem;margin-bottom:.2rem}
.lim p{margin:0;color:var(--muted);font-size:.92rem}
details{border:1px solid var(--line);border-radius:6px;background:var(--film);
  margin-bottom:.5rem}
summary{cursor:pointer;list-style:none;padding:.95rem 1.1rem;font-weight:700;font-size:.95rem;
  display:flex;justify-content:space-between;gap:1rem}
summary::-webkit-details-marker{display:none}
summary::after{content:'▸';color:var(--hot);flex-shrink:0;transition:transform .3s var(--ease)}
details[open] summary::after{transform:rotate(90deg)}
details p{margin:0;padding:0 1.1rem 1rem;color:var(--muted);font-size:.9rem}

.end{border-top:1px solid var(--line);text-align:center}
.end .acts{justify-content:center}
footer{border-top:1px solid var(--line);padding:1.7rem 0;color:var(--dim);font-size:.83rem}
.foot{display:flex;flex-wrap:wrap;gap:.8rem;justify-content:space-between}
footer a{color:var(--muted);text-decoration:none;padding:.3rem 0}
footer a:hover{color:var(--hot)}

/* Hạt phim: một lớp phủ mảnh dịch chuyển liên tục. Dùng transform nên
   không buộc trình duyệt vẽ lại nền mỗi khung hình. */
body::after{content:'';position:fixed;inset:-150%;z-index:2;pointer-events:none;
  opacity:.035;
  background-image:radial-gradient(#fff 1px,transparent 1px),
                   radial-gradient(#fff 1px,transparent 1px);
  background-size:3px 3px,5px 5px;background-position:0 0,2px 2px;
  animation:grain 1.1s steps(4) infinite}
@keyframes grain{
  0%{transform:translate(0,0)} 25%{transform:translate(-3px,2px)}
  50%{transform:translate(2px,-3px)} 75%{transform:translate(-2px,-2px)}
  100%{transform:translate(0,0)}
}

/* Rung khung nhẹ — máy chiếu phim thật không bao giờ đứng yên tuyệt đối. */
.strip-in{animation:roll 46s linear infinite,weave 2.7s ease-in-out infinite}
@keyframes weave{50%{transform:translateY(1.2px)}}

/* Khung phim nhấp nháy độ sáng rất nhẹ, lệch pha theo vị trí. */
.fr{animation:flick 3.4s ease-in-out infinite;animation-delay:calc(var(--i,0) * .21s)}
@keyframes flick{45%{filter:brightness(1.07)}}

/* Thanh tiến độ đọc trang, kẻ như dải film. */
.prog{position:fixed;top:0;left:0;height:3px;width:100%;z-index:70;transform:scaleX(0);
  transform-origin:0 50%;
  background:repeating-linear-gradient(90deg,var(--hot) 0 8px,var(--gold) 8px 14px)}
@supports (animation-timeline:scroll()){
  .prog{animation:pgrow linear;animation-timeline:scroll(root block)}
  @keyframes pgrow{to{transform:scaleX(1)}}
}

/* Số cảnh trong bảng đội hình sáng lên khi rê chuột cả hàng. */
.mem:hover .n{color:var(--gold);transform:scale(1.15)}
.mem .n{transition:color .25s var(--ease),transform .25s var(--ease);display:inline-block}

.rise{opacity:0;transform:translateY(18px);
  transition:opacity .65s var(--ease),transform .65s var(--ease)}
.rise.in{opacity:1;transform:none}
@media (max-width:760px){
  .trk{grid-template-columns:1fr;gap:.3rem}
  .mem{grid-template-columns:36px 1fr;gap:.6rem}
  .mem em{grid-column:2}
}
@media (max-width:640px){
  .acts{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
  .ga{border-right:0;border-bottom:1px solid var(--line)}
}
"""

JS = """
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -8% 0px',threshold:.06});
document.querySelectorAll('.rise').forEach(function(el,i){
  el.style.transitionDelay=(Math.min(i%5,4)*55)+'ms'; io.observe(el);
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
<meta name="theme-color" content="#0a0806" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='5' fill='%230a0806'/><rect x='4' y='9' width='24' height='14' rx='2' fill='%23f2683a'/><rect x='6' y='5' width='3' height='3' fill='%23fcd34d'/><rect x='13' y='5' width='3' height='3' fill='%23fcd34d'/><rect x='20' y='5' width='3' height='3' fill='%23fcd34d'/></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="SEOSONA Video AI" />
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>

<div class="prog" aria-hidden="true"></div>

<div class="slate">
  <div class="slate-in">
    <span class="clap" aria-hidden="true"></span>
    <b>SEOSONA Video AI</b>
    <span class="meta">4 LỚP · 10 ĐẶC VỤ · 34 SOP</span>
    <a href="https://github.com/$repo" target="_blank" rel="noopener">Mã nguồn ↗</a>
  </div>
</div>

<header class="hero">
  <div class="wrap">
    <p class="tag">Nhà máy sản xuất video</p>
    <h1>Phần lặp đi lặp lại thì <span class="hl">giao cho máy</span></h1>
    <p class="lede">
      Cắt, chèn chữ, lồng tiếng, kết xuất, đặt tên file — những bước ngốn nhiều thời gian
      nhất khi dựng video lại chẳng liên quan gì tới sáng tạo. Hệ này đóng gói chúng thành
      quy trình chạy được, còn người giữ lại phần quyết định.
    </p>
    <div class="acts">
      <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
      <a class="btn sec" href="#kien-truc">Xem kiến trúc bốn lớp</a>
    </div>
  </div>
</header>

<div class="strip" aria-label="Chín bước của dây chuyền sản xuất">
  <div class="strip-in">$frames</div>
</div>

<div class="wrap">
  <div class="gauges">
    <div class="ga"><b data-to="$n_agents">0</b><span>ĐẶC VỤ AI</span></div>
    <div class="ga"><b data-to="$n_sop">0</b><span>QUY TRÌNH VẬN HÀNH</span></div>
    <div class="ga"><b data-to="$n_framework">0</b><span>FILE KHUNG XỬ LÝ</span></div>
    <div class="ga"><b data-to="$n_files">0</b><span>FILE TRONG REPO</span></div>
  </div>
</div>

<main>
  <section class="wrap" id="kien-truc">
    <p class="shot rise">CẢNH 01 — KIẾN TRÚC</p>
    <h2 class="rise">Bốn lớp chạy chồng lấn, không nối tiếp</h2>
    <p class="sub rise">Lớp sau bắt đầu khi lớp trước còn đang chạy — giống các track trong
      một timeline dựng phim. Đổi bộ kết xuất thì chỉ đụng track cuối, phần nghiên cứu và
      viết kịch bản không biết gì về chuyện đó.</p>
    <div class="tl rise">
      <div class="ruler"><span>00:00</span><span>25%</span><span>50%</span><span>75%</span><span>HOÀN TẤT</span></div>
      <div class="tl-wrap">
        $tracks
        <span class="playhead" aria-hidden="true"></span>
      </div>
    </div>
  </section>

  <section class="wrap">
    <p class="shot rise">CẢNH 02 — ĐỘI HÌNH</p>
    <h2 class="rise">Mười đặc vụ, mỗi con một vai</h2>
    <p class="sub rise">Bàn giao theo hợp đồng cố định, không phải mỗi con chạy một kiểu rồi
      tự thoả thuận với nhau.</p>
    <div class="cast rise">$agents</div>
  </section>

  <section class="wrap">
    <p class="shot rise">CẢNH 03 — QUY TRÌNH</p>
    <h2 class="rise">34 quy trình vận hành viết sẵn</h2>
    <p class="sub rise">Chúng quy định chuẩn thẩm mỹ, thứ tự các bước và điều kiện dừng —
      thứ giữ cho đầu ra tự động không trôi khỏi chuẩn qua thời gian.</p>
    <div class="sops rise">$sops</div>
  </section>

  <section class="wrap">
    <p class="shot rise">CẢNH 04 — CÔNG NGHỆ</p>
    <h2 class="rise">Dựng bằng gì</h2>
    <div class="stack rise">$stack</div>
  </section>

  <section class="wrap">
    <p class="shot rise">CẢNH 05 — NÓI TRƯỚC CHO RÕ</p>
    <h2 class="rise">Ba giới hạn bạn nên biết</h2>
    <div class="lims rise">$limits</div>
  </section>

  <section class="wrap">
    <p class="shot rise">CẢNH 06 — HỎI ĐÁP</p>
    <h2 class="rise">Câu hỏi thường gặp</h2>
    <div class="rise">$faq</div>
  </section>

  <section class="end">
    <div class="wrap">
      <h2 class="rise" style="max-width:none">Mã nguồn mở, đọc được toàn bộ</h2>
      <p class="sub rise" style="margin-inline:auto">Cả bốn lớp, mười đặc vụ và ba mươi tư quy trình đều nằm trên GitHub.</p>
      <div class="acts rise">
        <a class="btn pri" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
        <a class="btn sec" href="$portfolio/#labs">Các dự án khác của Long Leo</a>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot">
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
    title = "SEOSONA Video AI — dây chuyền sản xuất video vận hành bằng AI"
    desc = ("Hệ sản xuất video tự động: kiến trúc bốn lớp, 10 đặc vụ AI, 34 quy trình vận "
            "hành, 913 file khung xử lý. Từ ý tưởng tới video hoàn chỉnh.")

    # Dải film lặp hai lần để vòng chạy liền mạch, không thấy mối nối.
    one = "".join(
        f'<div class="fr" style="--i:{i}"><span class="no">{esc(n)}</span>'
        f'<div><b>{esc(t)}</b><br /><em>{esc(d)}</em></div></div>'
        for i, (n, t, d) in enumerate(FRAMES))

    tracks = "".join(
        f'<div class="trk"><div class="trk-lb"><b>{esc(vi)}</b><em>{esc(en)}</em></div>'
        f'<div class="trk-bar"><i style="--s:{s};--w:{w};--i:{i}">{esc(note)}</i></div></div>'
        for i, (vi, en, s, w, note) in enumerate(TRACKS))

    agents = "".join(
        f'<div class="mem"><span class="n">{i:02d}</span><b>{esc(n)}</b>'
        f'<em>{esc(d)}</em></div>' for i, (n, d) in enumerate(AGENTS, 1))

    sops = "".join(f"<span>{esc(s)}</span>" for s in SOPS)
    stack = "".join(f"<span>{esc(s)}</span>" for s in STACK)
    limits = "".join(f'<div class="lim"><b>{esc(t)}</b><p>{esc(d)}</p></div>'
                     for t, d in LIMITS)
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(FAQ))

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "SoftwareSourceCode", "name": "SEOSONA Video AI", "description": desc,
             "url": SITE + "/", "image": SITE + "/cover.jpg",
             "codeRepository": f"https://github.com/{REPO}",
             "programmingLanguage": ["Python"],
             "author": {"@type": "Person", "name": "Hà Đình Long",
                        "alternateName": "Long Leo", "url": PORTFOLIO + "/"}},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ],
    }, ensure_ascii=False)

    return PAGE.substitute(
        title=esc(title), desc=esc(desc), site=SITE, portfolio=PORTFOLIO, repo=REPO,
        css=CSS, js=JS, jsonld=jsonld, frames=one + one, tracks=tracks, agents=agents,
        sops=sops, stack=stack, limits=limits, faq=faq,
        n_agents=N_AGENTS, n_sop=N_SOP, n_framework=N_FRAMEWORK, n_files=N_FILES)


def main():
    d = os.path.join(OUT, "landing")
    os.makedirs(d, exist_ok=True)
    html = build()
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", "seosona-video-ai.jpg"),
                    os.path.join(d, "cover.jpg"))
    print(f"  {len(html) // 1024} KB  SEOSONA Video AI — mô-típ dải film")
    print(f"  {len(FRAMES)} khung phim · {len(TRACKS)} track · {len(AGENTS)} đặc vụ · "
          f"{len(SOPS)} quy trình · phông Be Vietnam Pro")
    if len(AGENTS) != N_AGENTS:
        print(f"  CẢNH BÁO: liệt kê {len(AGENTS)} đặc vụ nhưng số liệu ghi {N_AGENTS}")
    print(f"\n{SITE}")


if __name__ == "__main__":
    raise SystemExit(main())
