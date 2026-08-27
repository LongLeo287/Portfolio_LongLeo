#!/usr/bin/env python3
"""Sinh landing page ĐỘC LẬP để đặt vào chính repo của từng dự án.

Khác với scripts/build-labs.py — bộ đó sinh các trang trong labs/ của portfolio,
dùng chung tokens.css + styles.css. Bộ này sinh trang tự chứa: CSS và JS nhúng
thẳng vào file, chỉ kèm một ảnh bìa. Mỗi repo vì thế deploy Vercel riêng được
mà không phải kéo theo tài sản của portfolio.

    python scripts/build-repo-landing.py

Xuất ra build/repo-landing/<repo>/ gồm landing/index.html, landing/cover.jpg và
vercel.json. Đẩy lên bằng scripts/push-repo-landing.py.

Nội dung lấy lại từ hằng LABS trong build-labs.py — sửa nội dung ở đúng một chỗ.
"""
import base64
import importlib.util
import io
import json
import os
import shutil
import sys
from string import Template

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing")
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
OWNER = "LongLeo287"

# slug trong LABS -> tên repo thật trên GitHub + tên project Vercel dự kiến.
# SEOSONA bị bỏ ra: đã có site thật ở seosona.vercel.app, đụng vào là hỏng.
# Portfolio_LongLeo bị bỏ ra: landing page của nó chính là portfolio.
# TẠM NGẮT: "omniclaw": ("OmniClaw", "omniclaw-longleo")
# Repo 14.879 file, sát hạn mức 15.000 file nguồn của Vercel nên build hỏng
# tức thì. Cần đặt Root Directory = landing trong Settings của project rồi mới
# bật lại. File landing/ vẫn nằm nguyên trong repo OmniClaw — bỏ dòng chú thích
# này và thêm lại một dòng vào TARGETS là chạy tiếp, không phải dựng lại gì.
# Thẻ OmniClaw trên portfolio vẫn trỏ labs/omniclaw.html nên không có link chết.
#
# Tên miền omniclaw.vercel.app và omni-claw.vercel.app đều đã bị người khác
# chiếm — .vercel.app là duy nhất toàn cầu, không phải theo tài khoản.
TARGETS = {
    "seosona-flow":     ("seosona-flow",     "seosona-flow"),
    "seosona-video-ai": ("SEOSONA-Video-AI", "seosona-video-ai"),
    "omniclaw":         ("OmniClaw",         "omniclaw-longleo"),
    "seosona-os":       ("SEOSONA-OS",       "seosona-os"),
    "seosona-ux-ui":    ("SEOSONA-UX-UI",    "seosona-ux-ui"),
    "tiem-nuoc-nho":    ("Tiem_Nuoc_Nho_v5", "tiem-nuoc-nho"),
}

# Repo này là ứng dụng Vite chạy được thật. Landing ở gốc, app ở /app —
# nên buildCommand phải dựng app rồi mới chép landing đè lên index gốc.
APP_AT_SUBPATH = {"tiem-nuoc-nho": "/app/"}

# Dự án có trang viết riêng — mẫu chung không được đụng vào index.html của nó.
# vercel.json, .vercelignore và ảnh bìa vẫn sinh bình thường ở đây.
# Repo sát hạn mức 15.000 file nguồn của Vercel. Cách duy nhất là bắt Vercel
# chỉ nhìn vào thư mục landing/ (đặt Root Directory trong Settings) — lúc đó nó
# đọc landing/vercel.json chứ không phải file ở gốc, nên phải sinh thêm một bản.
OVERSIZED = {"omniclaw"}   # vẫn giữ, dùng lại ngay khi bật lại TARGETS

CUSTOM = {
    "seosona-flow": "scripts/landing-seosona-flow.py",
    "tiem-nuoc-nho": "scripts/landing-tiem-nuoc-nho.py",
    "seosona-video-ai": "scripts/landing-seosona-video-ai.py",
    "omniclaw": "scripts/landing-omniclaw.py",
    "seosona-os": "scripts/landing-seosona-os.py",
    "seosona-ux-ui": "scripts/landing-seosona-ux-ui.py",
}


def load_labs():
    """build-labs.py có dấu gạch ngang nên import thường không gọi được."""
    path = os.path.join(ROOT, "scripts", "build-labs.py")
    spec = importlib.util.spec_from_file_location("build_labs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {e["slug"]: e for e in mod.LABS}


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#0c0a09; --panel:#141110; --line:#26211e;
  --text:#fafaf9; --muted:#a8a29e; --dim:#78716c;
  --primary:#ff7a00; --amber:#fcd34d;
  --dur:.6s; --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;
  overflow-x:hidden;
}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.wrap{width:min(1080px,100% - 2.5rem);margin-inline:auto}

/* ---------- thanh trên cùng ---------- */
.bar{
  position:sticky;top:0;z-index:50;
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  padding:.85rem 0;
  background:rgba(12,10,9,.82);backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line);
}
.bar-in{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  width:min(1080px,100% - 2.5rem);margin-inline:auto}
.back{
  display:inline-flex;align-items:center;gap:.55rem;min-height:44px;
  font-size:.875rem;font-weight:500;color:var(--muted);text-decoration:none;
  padding:.5rem .25rem;transition:color .25s var(--ease);
}
.back:hover{color:var(--text)}
.back svg{transition:transform .3s var(--ease)}
.back:hover svg{transform:translateX(-3px)}
.bar-cta{
  display:inline-flex;align-items:center;gap:.5rem;
  padding:.55rem 1.05rem;border-radius:999px;
  border:1px solid var(--line);background:var(--panel);
  font-size:.85rem;font-weight:600;text-decoration:none;color:var(--text);
  transition:border-color .25s var(--ease),transform .25s var(--ease),background .25s var(--ease);
}
.bar-cta:hover{border-color:var(--primary);background:#1c1815;transform:translateY(-1px)}

/* ---------- hero ---------- */
.hero{position:relative;padding:clamp(3.5rem,9vw,6.5rem) 0 clamp(2.5rem,6vw,4rem);overflow:hidden}
.hero::before{
  content:'';position:absolute;inset:-20% -10% auto -10%;height:120%;
  background:
    radial-gradient(48% 42% at 12% 8%,rgba(255,122,0,.16),transparent 70%),
    radial-gradient(38% 34% at 88% 0%,rgba(252,211,77,.09),transparent 70%);
  pointer-events:none;z-index:0;
  animation:glowDrift 18s ease-in-out infinite alternate;
}
@keyframes glowDrift{to{transform:translate3d(2%,1.5%,0) scale(1.06)}}
.hero .wrap{position:relative;z-index:1}
.eyebrow{
  display:inline-block;font-size:.75rem;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:var(--amber);margin:0 0 1.1rem;
  padding-bottom:.5rem;border-bottom:2px solid rgba(252,211,77,.45);
}
h1{
  font-size:clamp(2.25rem,6.5vw,4rem);line-height:1.06;letter-spacing:-.025em;
  font-weight:700;margin:0 0 1.25rem;
}
.tagline{font-size:clamp(1.05rem,2.4vw,1.3rem);color:var(--muted);max-width:60ch;margin:0 0 2rem}
.actions{display:flex;flex-wrap:wrap;gap:.75rem;margin-bottom:2.75rem}
.btn{
  display:inline-flex;align-items:center;gap:.55rem;
  padding:.85rem 1.6rem;border-radius:999px;
  font-size:.95rem;font-weight:600;text-decoration:none;
  border:1px solid transparent;
  transform:translateY(var(--lift,0)) scale(var(--press,1));
  transition:transform .25s var(--ease),background .25s var(--ease),
             border-color .25s var(--ease),box-shadow .25s var(--ease);
}
.btn:hover{--lift:-2px}
.btn:active{--press:.97}
.btn-primary{background:var(--primary);color:#0c0a09}
.btn-primary:hover{box-shadow:0 10px 30px -10px rgba(255,122,0,.6)}
.btn-ghost{background:transparent;color:var(--text);border-color:var(--line)}
.btn-ghost:hover{border-color:var(--primary);background:rgba(255,122,0,.07)}

/* ---------- chỉ số ---------- */
.meta{
  display:grid;gap:1px;background:var(--line);
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  border:1px solid var(--line);border-radius:14px;overflow:hidden;
}
.meta div{background:var(--panel);padding:1.1rem 1.25rem}
.meta dt{font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--dim);margin:0 0 .35rem}
.meta dd{margin:0;font-size:1.02rem;font-weight:600;color:var(--text)}

/* ---------- ảnh bìa ---------- */
.shot{margin:clamp(2.5rem,6vw,4rem) 0}
.shot img{
  width:100%;border-radius:16px;border:1px solid var(--line);
  box-shadow:0 30px 70px -35px rgba(0,0,0,.9);
}

/* ---------- khối nội dung ---------- */
section{padding:clamp(2.5rem,6vw,4rem) 0}
h2{font-size:clamp(1.5rem,3.4vw,2.1rem);line-height:1.2;letter-spacing:-.02em;margin:0 0 1.25rem}
.lead{font-size:1.075rem;color:var(--muted);max-width:68ch;margin:0}
.cards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(290px,100%),1fr));margin-top:1.75rem}
.card{
  position:relative;overflow:hidden;
  background:var(--panel);border:1px solid var(--line);border-radius:14px;
  padding:1.6rem 1.5rem 1.5rem;
  transition:border-color .3s var(--ease),transform .3s var(--ease),background .3s var(--ease);
}
.card::after{
  content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;
  background:radial-gradient(240px circle at var(--mx,50%) var(--my,50%),rgba(255,122,0,.09),transparent 68%);
  opacity:0;transition:opacity .3s var(--ease);
}
.card:hover{border-color:#3a322c;transform:translateY(-3px);background:#171412}
.card:hover::after{opacity:1}
.card .n{
  display:block;font-size:.72rem;font-weight:700;letter-spacing:.14em;
  color:var(--primary);margin-bottom:.7rem;
}
.card h3{font-size:1.075rem;margin:0 0 .55rem;line-height:1.35}
.card p{margin:0;font-size:.94rem;color:var(--muted);line-height:1.6}

/* ---------- công nghệ ---------- */
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.5rem}
.chip{
  padding:.45rem 1rem;border-radius:999px;font-size:.83rem;font-weight:500;
  background:var(--panel);border:1px solid var(--line);color:var(--muted);
  transition:color .25s var(--ease),border-color .25s var(--ease);
}
.chip:hover{color:var(--text);border-color:#3a322c}
.note{
  margin-top:2rem;padding:1.15rem 1.35rem;border-radius:12px;
  border:1px solid var(--line);border-left:3px solid var(--amber);
  background:var(--panel);color:var(--muted);font-size:.94rem;
}

/* ---------- kết ---------- */
.cta{
  text-align:center;padding:clamp(3rem,8vw,5rem) 0;
  border-top:1px solid var(--line);margin-top:clamp(2rem,5vw,3rem);
}
.cta h2{margin-bottom:.85rem}
.cta p{color:var(--muted);margin:0 auto 2rem;max-width:52ch}
footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--dim);font-size:.85rem}
.foot-in{display:flex;flex-wrap:wrap;gap:.75rem;justify-content:space-between;align-items:center}
footer a{
  display:inline-block;padding:.5rem .15rem;color:var(--muted);
  text-decoration:none;transition:color .25s var(--ease);
}
footer a:hover{color:var(--primary)}
:focus-visible{outline:2px solid var(--amber);outline-offset:3px;border-radius:4px}

/* ---------- chuyển động ---------- */
.rise{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.rise.in{opacity:1;transform:none}
.hero .eyebrow,.hero h1,.hero .tagline,.hero .actions,.hero .meta{
  opacity:0;animation:riseIn .85s var(--ease) forwards;
}
.hero .eyebrow{animation-delay:.05s}
.hero h1{animation-delay:.14s}
.hero .tagline{animation-delay:.23s}
.hero .actions{animation-delay:.32s}
.hero .meta{animation-delay:.41s}
@keyframes riseIn{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}

/* Thanh tiến độ cuộn — chạy bằng animation-timeline của trình duyệt,
   không listener, không rAF. Trình duyệt cũ đơn giản là không thấy nó. */
.progress{
  position:fixed;top:0;left:0;height:2px;width:100%;z-index:60;
  background:linear-gradient(90deg,var(--primary),var(--amber));
  transform-origin:0 50%;transform:scaleX(0);
}
@supports (animation-timeline:scroll()){
  .progress{animation:grow linear;animation-timeline:scroll(root block)}
  @keyframes grow{to{transform:scaleX(1)}}
}
@media (max-width:640px){
  .actions{flex-direction:column;align-items:stretch}
  .btn{justify-content:center}
}
"""

JS = """
// Hiện dần khi cuộn tới. IntersectionObserver thay vì nghe sự kiện scroll.
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{rootMargin:'0px 0px -10% 0px',threshold:.08});
document.querySelectorAll('.rise').forEach(function(el,i){
  el.style.transitionDelay=(Math.min(i,6)*55)+'ms'; io.observe(el);
});

// Vệt sáng theo con trỏ. Một vòng rAF dùng chung cho mọi thẻ, chỉ ghi
// biến CSS rồi để trình duyệt tự vẽ — không đụng vào layout.
var pending=null,frame=0;
if(matchMedia('(pointer:fine)').matches){
  document.querySelectorAll('.card').forEach(function(card){
    card.addEventListener('pointermove',function(ev){
      pending=[card,ev];
      if(!frame) frame=requestAnimationFrame(function(){
        frame=0; if(!pending) return;
        var c=pending[0],e=pending[1],r=c.getBoundingClientRect();
        c.style.setProperty('--mx',(e.clientX-r.left)+'px');
        c.style.setProperty('--my',(e.clientY-r.top)+'px');
      });
    });
  });
}
"""

PAGE = Template("""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>$page_title</title>
<meta name="description" content="$desc" />
<meta name="author" content="Hà Đình Long" />
<meta name="theme-color" content="#0c0a09" />
<link rel="canonical" href="$site/" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>$emoji</text></svg>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="$name" />
<meta property="og:title" content="$page_title" />
<meta property="og:description" content="$desc" />
<meta property="og:url" content="$site/" />
<meta property="og:image" content="$site/cover.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="600" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="$page_title" />
<meta name="twitter:description" content="$desc" />
<meta name="twitter:image" content="$site/cover.jpg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap" />
<style>$css</style>
<script type="application/ld+json">$jsonld</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>

<nav class="bar">
  <div class="bar-in">
    <a class="back" href="$portfolio/#labs">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      Portfolio Hà Đình Long
    </a>
    <a class="bar-cta" href="https://github.com/$repo" target="_blank" rel="noopener">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/></svg>
      Mã nguồn
    </a>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <p class="eyebrow">$eyebrow</p>
    <h1>$name</h1>
    <p class="tagline">$tagline</p>
    <div class="actions">$actions</div>
    <dl class="meta">$meta</dl>
  </div>
</header>

<div class="wrap shot rise">
  <img src="cover.jpg" width="1200" height="600" alt="Ảnh bìa dự án $name" fetchpriority="high" />
</div>

<main>
  <section class="wrap">
    <h2 class="rise">$why_h</h2>
    <p class="lead rise">$why</p>
  </section>

  <section class="wrap">
    <h2 class="rise">$cards_h</h2>
    <div class="cards">$cards</div>
  </section>

  <section class="wrap">
    <h2 class="rise">Công nghệ sử dụng</h2>
    <div class="chips rise">$chips</div>
    $note
  </section>

  <section class="wrap cta">
    <h2 class="rise">Muốn xem cách nó hoạt động?</h2>
    <p class="rise">Toàn bộ mã nguồn công khai trên GitHub. Có gì muốn hỏi hoặc muốn hợp tác, liên hệ qua portfolio.</p>
    <div class="actions rise" style="justify-content:center">
      <a class="btn btn-primary" href="https://github.com/$repo" target="_blank" rel="noopener">Xem trên GitHub</a>
      <a class="btn btn-ghost" href="$portfolio/#contact">Liên hệ</a>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot-in">
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


def build(slug, e, repo, vercel_name):
    site = f"https://{vercel_name}.vercel.app"
    repo = f"{OWNER}/{repo}"   # TARGETS giữ tên trần để gọi API, link cần cả chủ sở hữu

    # Mô tả cho thẻ meta: rút gọn tagline, cắt ở ranh giới từ cho khỏi cụt lủn.
    desc = e["tagline"].replace("\n", " ").strip()
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0] + "…"

    actions = [f'<a class="btn btn-primary" href="https://github.com/{repo}" '
               f'target="_blank" rel="noopener">Xem mã nguồn ↗</a>']
    if e.get("live"):
        actions.insert(0, f'<a class="btn btn-primary" href="{e["live"]}" '
                          f'target="_blank" rel="noopener">Xem website ↗</a>')
        actions[1] = actions[1].replace("btn-primary", "btn-ghost")
    if slug in APP_AT_SUBPATH:
        actions.insert(0, f'<a class="btn btn-primary" href="{APP_AT_SUBPATH[slug]}">Dùng thử ứng dụng ↗</a>')
        actions[1] = actions[1].replace("btn-primary", "btn-ghost")
    actions.append(f'<a class="btn btn-ghost" href="{PORTFOLIO}/#labs">Các dự án khác</a>')

    meta = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in e["meta"])
    cards = "".join(
        f'<article class="card rise"><span class="n">{i + 1:02d}</span>'
        f'<h3>{esc(t)}</h3><p>{esc(b)}</p></article>'
        for i, (t, b) in enumerate(e["cards"]))
    chips = "".join(f'<span class="chip">{esc(s)}</span>' for s in e["stack"])
    note = f'<p class="note rise">{esc(e["note"])}</p>' if e.get("note") else ""

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": e["name"],
        "description": desc,
        "url": site + "/",
        "image": site + "/cover.jpg",
        "codeRepository": f"https://github.com/{repo}",
        "programmingLanguage": e["stack"],
        "author": {"@type": "Person", "name": "Hà Đình Long",
                   "alternateName": "Long Leo", "url": PORTFOLIO + "/"},
    }, ensure_ascii=False, indent=None)

    # Dự án trùng tên với repo khác trên GitHub cần tiêu đề riêng để phân biệt.
    page_title = e.get("title") or f'{e["name"]} — dự án của Hà Đình Long'
    return PAGE.substitute(
        page_title=esc(page_title),
        name=esc(e["name"]), desc=esc(desc), site=site, portfolio=PORTFOLIO,
        repo=repo, emoji="🧩", css=CSS, js=JS, jsonld=jsonld,
        eyebrow=esc(e["eyebrow"]), tagline=esc(e["tagline"]),
        actions="".join(actions), meta=meta,
        why_h=esc(e["why_h"]), why=esc(e["why"]),
        cards_h=esc(e["cards_h"]), cards=cards, chips=chips, note=note,
    )


def vercel_config(slug):
    """Repo nào cũng phát hành thư mục landing/. Riêng repo có app thật thì
    dựng app trước, đẩy nó xuống /app rồi mới chép landing đè lên gốc."""
    if slug not in APP_AT_SUBPATH:
        return {
            "$schema": "https://openapi.vercel.sh/vercel.json",
            "framework": None,
            "installCommand": "echo 'khong can cai dat'",
            "buildCommand": "echo 'trang tinh, khong can build'",
            "outputDirectory": "landing",
            "cleanUrls": True,
        }
    # Vite build ra dist/ với đường dẫn tài sản tuyệt đối (/assets/…), nên
    # chuyển index.html xuống dist/app/ vẫn nạp đúng file. Nếu build hỏng thì
    # landing vẫn lên được — lệnh cuối cùng luôn thành công.
    return {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "buildCommand": (
            "npm run build || true; "
            "mkdir -p dist/app; "
            "if [ -f dist/index.html ]; then mv dist/index.html dist/app/index.html; fi; "
            "cp landing/index.html dist/index.html; "
            "cp landing/cover.jpg dist/cover.jpg"
        ),
        "outputDirectory": "dist",
        "cleanUrls": True,
    }


VERCELIGNORE = """# Chỉ giữ lại thư mục landing/ trong bản phát hành — phần còn lại của repo là
# mã nguồn dự án, không liên quan tới trang giới thiệu.
#
# Lưu ý cho ai đọc sau: file này KHÔNG ngăn Vercel tải repo về. Repo nối qua
# Git thì Vercel vẫn clone toàn bộ vào container build, rồi mới lọc. Muốn
# Vercel không phải đọc cả repo thì phải tách landing page sang một repo riêng
# — đổi lại trang không còn nằm trong repo của chính dự án nữa.
/*
!/landing/
!/vercel.json
"""


def main():
    labs = load_labs()
    # Dọn từng thư mục con thay vì xoá cả OUT — trên Windows chỉ cần một
    # tiến trình đang đứng trong OUT là rmtree ném PermissionError.
    # Repo có trang viết riêng thì bỏ qua: dọn ở đây là xoá mất trang đó,
    # và nó chỉ được sinh lại bởi script riêng của nó.
    keep = {repo for slug, (repo, _) in TARGETS.items() if slug in CUSTOM}
    for name in os.listdir(OUT) if os.path.isdir(OUT) else []:
        if name not in keep:
            shutil.rmtree(os.path.join(OUT, name), ignore_errors=True)

    for slug, (repo, vercel_name) in TARGETS.items():
        e = labs[slug]
        d = os.path.join(OUT, repo, "landing")
        os.makedirs(d, exist_ok=True)

        if slug in CUSTOM:
            html = None
            print(f"  --      {repo:<20} trang viết riêng, chạy {CUSTOM[slug]}")
        else:
            html = build(slug, e, repo, vercel_name)
            io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
        shutil.copyfile(os.path.join(ROOT, "assets", "img", "labs", f"{slug}.jpg"),
                        os.path.join(d, "cover.jpg"))

        cfg = json.dumps(vercel_config(slug), ensure_ascii=False, indent=2) + "\n"
        io.open(os.path.join(OUT, repo, "vercel.json"), "w", encoding="utf-8", newline="\n").write(cfg)

        # Repo quá nhiều file thì cần thêm một vercel.json ngay trong landing/,
        # để dùng được khi đặt Root Directory = landing.
        if slug in OVERSIZED:
            inner = json.dumps({
                "$schema": "https://openapi.vercel.sh/vercel.json",
                "framework": None,
                "installCommand": "echo 'khong can cai dat'",
                "buildCommand": "echo 'trang tinh, khong can build'",
                "outputDirectory": ".",
                "cleanUrls": True,
            }, ensure_ascii=False, indent=2) + "\n"
            io.open(os.path.join(d, "vercel.json"), "w", encoding="utf-8",
                    newline="\n").write(inner)

        # Repo có app thật thì build cần cả src/, package.json… nên không lọc.
        if slug not in APP_AT_SUBPATH:
            io.open(os.path.join(OUT, repo, ".vercelignore"), "w",
                    encoding="utf-8", newline="\n").write(VERCELIGNORE)

        if html is not None:
            print(f"  {len(html) // 1024:>3} KB  {repo:<20} -> https://{vercel_name}.vercel.app")

    print(f"\nĐã sinh {len(TARGETS)} landing page vào build/repo-landing/")


if __name__ == "__main__":
    raise SystemExit(main())
