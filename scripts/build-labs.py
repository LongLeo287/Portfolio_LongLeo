#!/usr/bin/env python3
"""Sinh các trang landing trong labs/ từ dữ liệu bên dưới.

Mỗi dự án mã nguồn mở có một trang riêng, dùng chung tokens.css + styles.css
với portfolio nên nhìn liền mạch, cộng thêm labs.css cho phần riêng.

    python scripts/build-labs.py

Thêm dự án mới: thêm một mục vào LABS rồi chạy lại. Nhớ thêm ảnh
assets/img/labs/<slug>{,-480,-960}.webp và một thẻ trong section
#labs của index.html.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://portfolio-long-leo.vercel.app"
VER = "1.90"

# Chỉ hai trang này còn nằm trong portfolio. Sáu dự án kia đã có landing
# page riêng trong chính repo của chúng, deploy Vercel độc lập —
# xem scripts/build-repo-landing.py. LABS vẫn giữ đủ tám mục vì bộ đó
# lấy nội dung từ đây.
IN_PORTFOLIO = {"omniclaw", "portfolio"}

LABS = [
    {
        "slug": "omniclaw",
        "name": "OmniClaw",
        "repo": "LongLeo287/OmniClaw",
        "eyebrow": "Hệ điều hành agent",
        "title": "OmniClaw của Long Leo — hệ điều hành agent 8 daemon cho Claude Code",
        "tagline": "Biến máy cá nhân thành một dàn AI tự vận hành, được cai quản bởi 8 daemon chạy nền — "
                   "không phải mấy con agent \"đóng vai nhân viên\".",
        "meta": [("Ngôn ngữ", "Python"), ("Phiên bản", "5.0"), ("Giấy phép", "MIT"),
                 ("Chạy trên", "Claude Code · Antigravity")],
        "why_h": "Vấn đề nó giải quyết",
        "why": "Mỗi công cụ AI lập trình có bộ luật riêng, trí nhớ riêng, và quên sạch sau mỗi phiên. "
               "Kết quả là cùng một máy nhưng mỗi công cụ hành xử một kiểu, và không có gì bắt chúng "
               "tuân theo kỷ luật chung. OmniClaw đặt một tầng backend không thể né phía dưới tất cả.",
        "cards_h": "Điểm cốt lõi",
        "cards": [
            ("Tính di động tuyệt đối",
             "Tương thích gốc với Claude Code CLI và Google Antigravity. Luật hệ thống được kế thừa "
             "ở phạm vi toàn cục, không phải cấu hình lại từng dự án."),
            ("Bảo vệ Git kiểu Zero-Trust",
             "Daemon chạy nền quét cache, dọn file .sqlite và làm sạch commit trước khi đẩy lên "
             "GitHub — để khoá API không bao giờ lọt ra ngoài."),
            ("Bootstrapper tự động",
             "Gõ một lệnh `omniclaw` là mở bảng điều khiển trung tâm. Nó tự lo NPM, extension "
             "VSCode và các pipeline logic."),
            ("8 daemon bất tử",
             "Agent ở đây không có \"ý chí tự do\". Toàn bộ chạy qua một pipeline cứng, được 8 daemon "
             "Python canh gác: kiến trúc sư, bộ phân luồng, bộ đăng ký thực thể, bộ thu thập…"),
            ("MemPalace — trí nhớ 3 tầng",
             "Kiến trúc bộ nhớ không gian ba lớp, để ngữ cảnh sống qua nhiều phiên làm việc thay vì "
             "bốc hơi mỗi lần đóng cửa sổ."),
        ],
        "stack": ["Python", "Claude Code CLI", "Google Antigravity", "MCP", "SQLite"],
    },
    {
        "slug": "seosona-os",
        "name": "SEOSONA OS",
        "repo": "LongLeo287/SEOSONA-OS",
        "eyebrow": "Bộ não trung tâm",
        "tagline": "Một bộ luật, một trí nhớ, dùng chung cho mọi công cụ AI trên máy — và nó tự "
                   "học thêm mà không cần ai dạy.",
        "meta": [("Ngôn ngữ", "Python · Node.js"), ("Giấy phép", "MIT"),
                 ("Tri thức", "3.000+ mục"), ("Vệ tinh", "4 dự án")],
        "why_h": "Vì sao nó tồn tại",
        "why": "Cursor, Claude Code, Codex, Windsurf, Aider — mỗi cái một bộ nhớ, một bộ luật. "
               "Chuyển công cụ là mất sạch ngữ cảnh. SEOSONA OS đóng vai bộ não chung: một bản "
               "doctrine duy nhất được tiêm vào tất cả, cùng một kho tri thức mà công cụ nào cũng "
               "truy vấn được.",
        "cards_h": "Năm việc nó làm",
        "cards": [
            ("Cai quản",
             "Một file doctrine duy nhất được tiêm vào Cursor, Claude Code, Codex, Windsurf, Aider — "
             "để tất cả dùng chung một bộ luật, một trí nhớ, một bộ kỹ năng."),
            ("Ghi nhớ",
             "Kho tri thức 3.000+ mục đã phân tích, mở ra cho mọi agent qua một MCP server tìm kiếm "
             "ngữ nghĩa và một đồ thị tri thức mã nguồn."),
            ("Tự lớn lên",
             "Pipeline UAP tự nạp repo bên ngoài về, phân tích, và biến những thứ thực sự hữu ích "
             "thành kỹ năng gọi được — hoàn toàn tự động."),
            ("Hành động",
             "Tầng định tuyến và điều phối tự chọn đúng kỹ năng cho từng việc, rồi thực thi — có "
             "hàng rào chặn các thao tác không thể hoàn tác."),
            ("Chỉ huy hệ sinh thái",
             "Bốn dự án vệ tinh — Video, Content, UX-UI, Flow — kết nối ngược về bộ não này và "
             "dùng chung tri thức của nó lúc chạy."),
        ],
        "stack": ["Python", "Node.js", "MCP", "Semantic search", "Knowledge graph"],
    },
    {
        "slug": "seosona-ux-ui",
        "name": "SEOSONA UX-UI",
        "repo": "LongLeo287/SEOSONA-UX-UI",
        "eyebrow": "Hệ thống thiết kế",
        "tagline": "Thư viện component và hệ design token thuần HTML/CSS/JS — copy vào đâu cũng chạy, "
                   "không ràng buộc framework.",
        "meta": [("Ngôn ngữ", "HTML · CSS · JS"), ("Component", "30+"),
                 ("Không phụ thuộc", "framework"), ("Showcase", "GitHub Pages")],
        "why_h": "Vấn đề nó giải quyết",
        "why": "Thư viện UI thường trói người dùng vào một framework. Cái này thì không: component "
               "viết bằng HTML, CSS custom property và Vanilla JS, nên dán vào React, Next.js, Vue "
               "hay một trang tĩnh đều chạy như nhau.",
        "cards_h": "Bên trong có gì",
        "cards": [
            ("Design token",
             "Nền móng của cả hệ: thang chữ fluid, nhịp khoảng cách, đổ bóng, gradient, và các bảng "
             "màu dựng sẵn cho từng loại thương hiệu."),
            ("Hơn 30 component",
             "Thẻ, bảng giá, form, điều hướng, modal, timeline, testimonial, chân trang — phân loại "
             "theo chức năng, có sẵn trạng thái và ràng buộc tiếp cận."),
            ("Công thức motion",
             "Thư viện công thức chuyển động kèm bảng thời lượng và đường cong easing chuẩn, dùng "
             "được ngay mà không phải tự chế."),
            ("Kiến trúc 7 tầng",
             "Thư mục tổ chức theo bảy tầng của SEOSONA — từ luật hệ thống, agent, kỹ năng, tri thức "
             "đến thư viện và không gian làm việc."),
        ],
        "stack": ["HTML", "CSS Variables", "Vanilla JS", "GitHub Pages"],
        "note": "Chính hệ thống này cung cấp bảng token chuyển động và các công thức motion đang "
                "chạy trên trang portfolio bạn vừa rời khỏi.",
    },
    {
        "slug": "seosona-flow",
        "name": "SEOSONA Flow",
        "repo": "LongLeo287/seosona-flow",
        "eyebrow": "Chrome Extension",
        "tagline": "Tự động hoá việc tạo ảnh và video AI ngay trong trình duyệt — Google Flow, ChatGPT, "
                   "Gemini, Grok — chạy hàng loạt thay vì ngồi bấm tay từng cái một.",
        "meta": [("Nền tảng", "Chrome MV3"), ("Chạy", "100% offline"),
                 ("API key", "không cần"), ("Bước build", "không có")],
        "why_h": "Vấn đề nó giải quyết",
        "why": "Tạo hàng chục ảnh hoặc video AI nghĩa là mở tab, dán prompt, chờ, tải về, lặp lại. "
               "Extension này điều khiển chính những tab đó thay bạn — chạy theo lô, ở chế độ side "
               "panel nên vẫn làm việc khác song song được.",
        "cards_h": "Vì sao nó nhẹ đến vậy",
        "cards": [
            ("Không backend",
             "Chạy hoàn toàn trong trình duyệt. Không server, không tài khoản SEOSONA, không đăng "
             "nhập, không giới hạn gói."),
            ("Không cần API key trả phí",
             "Nó điều khiển phiên đăng nhập sẵn có của chính bạn trên Flow, ChatGPT, Gemini, Grok — "
             "nên dùng đúng quota của tài khoản bạn, không phát sinh chi phí lạ."),
            ("Không có bước build",
             "Không npm install, không bundler. Thư viện đã vendor sẵn, mã nguồn nạp thẳng vào "
             "Chrome qua Load unpacked."),
            ("Image-to-Prompt",
             "Đưa vào một tấm ảnh, nhận lại prompt mô tả — dùng để tái tạo hoặc biến tấu phong cách "
             "của một hình đã có."),
            ("Side Panel",
             "Chạy ở khung bên phải trình duyệt thay vì cửa sổ popup, nên vẫn thao tác trên tab "
             "chính trong lúc nó làm việc."),
        ],
        "stack": ["JavaScript", "Chrome Manifest V3", "Side Panel API"],
        "note": "Extension không kèm tài khoản hay API key nào. Mỗi lần chạy sẽ tiêu credit của "
                "chính tài khoản bạn đang đăng nhập trong trình duyệt.",
    },
    {
        "slug": "seosona-video-ai",
        "name": "SEOSONA Video AI",
        "repo": "LongLeo287/SEOSONA-Video-AI",
        "eyebrow": "Nhà máy sản xuất video",
        "tagline": "Hệ sinh thái sản xuất truyền thông đa phương tiện vận hành bằng AI — từ kịch bản "
                   "tới video hoàn chỉnh, tự động phần lặp đi lặp lại.",
        "meta": [("Kiến trúc", "4 lớp"), ("Đặc vụ AI", "10"),
                 ("Luồng công việc", "21"), ("Bộ luật vận hành", "26")],
        "why_h": "Vấn đề nó giải quyết",
        "why": "Phần lớn thời gian dựng một video tin tức hay video không mặt không nằm ở sáng tạo — "
               "nó nằm ở những bước lặp: cắt, chèn chữ, lồng tiếng, kết xuất, đặt tên file. Hệ này "
               "đóng gói các bước đó thành quy trình chạy được, còn người thì lo phần quyết định.",
        "cards_h": "Bên trong có gì",
        "cards": [
            ("Kiến trúc bốn lớp",
             "Nhận thức, Thực thi, Luồng công việc và Kết xuất tách bạch — đổi một lớp không kéo "
             "sập ba lớp còn lại."),
            ("10 đặc vụ AI, 7 kỹ năng Python",
             "Mỗi đặc vụ giữ một vai trong dây chuyền, nối vào pipeline chung thay vì mỗi con chạy "
             "một kiểu."),
            ("21 luồng công việc",
             "Kèm 9 bộ kết xuất đồ hoạ, để cùng một kịch bản đúc ra được nhiều định dạng video "
             "khác nhau."),
            ("26 bộ luật vận hành",
             "Ràng buộc về thẩm mỹ, vận hành và nội dung — thứ giữ cho đầu ra tự động không trôi "
             "khỏi chuẩn."),
            ("7 quy trình mẫu",
             "Video tin tức, video không mặt, video quảng cáo… mỗi loại một đường đi đã được mổ xẻ "
             "chi tiết."),
        ],
        "stack": ["Python", "Puppeteer", "FFmpeg", "VieNeu-TTS", "Whisper"],
    },
    {
        "slug": "tiem-nuoc-nho",
        "name": "Tiệm Nước Nhỏ POS",
        "repo": "LongLeo287/Tiem_Nuoc_Nho_v5",
        "eyebrow": "Ứng dụng thực tế",
        "tagline": "Hệ thống bán hàng cho quán nước — chạy mượt trên điện thoại lẫn quầy thu ngân, "
                   "và database chỉ là một file Google Sheets.",
        "meta": [("Giao diện", "React 19 · TypeScript"), ("Backend", "serverless"),
                 ("Database", "Google Sheets"), ("Chi phí hạ tầng", "0đ")],
        "why_h": "Vấn đề nó giải quyết",
        "why": "Một quán nước nhỏ không kham nổi tiền server, cũng không có ai quản trị cơ sở dữ "
               "liệu. Hệ này chạy trên Google Apps Script với Google Sheets làm database — chủ quán "
               "sửa dữ liệu ngay trong bảng tính họ vốn đã biết dùng, còn chi phí hạ tầng bằng không.",
        "cards_h": "Điểm đáng nói",
        "cards": [
            ("Hai giao diện, một mã nguồn",
             "Trên điện thoại là thanh điều hướng dưới đáy, thao tác một ngón cho nhân viên pha chế "
             "đang di chuyển. Trên máy tính tự mở thành sidebar cố định và lưới nhiều cột cho quầy "
             "thu ngân."),
            ("Đơn nháp và mở khoá bàn",
             "Ghi order nhanh, lưu nháp, chuyển trạng thái — khớp với cách một quán thật vận hành "
             "trong giờ cao điểm."),
            ("Lịch sử hàng nghìn đơn",
             "Truy xuất lại trên bảng theo dõi rộng, kèm trạng thái thanh toán."),
            ("QR thanh toán tự sinh",
             "Tạo mã QR chuyển khoản ngân hàng theo đúng số tiền của đơn, khách quét là trả."),
            ("Đồng bộ realtime",
             "Ứng dụng và bảng tính luôn khớp nhau, nên chủ quán xem doanh thu ở đâu cũng được."),
        ],
        "stack": ["React 19", "TypeScript", "Vite", "Tailwind CSS v4", "Framer Motion", "Google Apps Script"],
        "note": "Đây là sản phẩm có người dùng thật, không phải bản demo — cũng là phần bằng chứng "
                "cụ thể nhất cho dịch vụ thiết kế giao diện trong portfolio.",
    },
    {
        "slug": "seosona",
        "name": "SEOSONA",
        "repo": "LongLeo287/SEOSONA",
        "live": "https://seosona.com",
        "eyebrow": "Website",
        "tagline": "Dựng lại toàn bộ website seosona.com bằng Next.js và Tailwind CSS, deploy trên Vercel.",
        "meta": [("Framework", "Next.js"), ("Giao diện", "Tailwind CSS"),
                 ("Nội dung", "MDX"), ("Deploy", "Vercel")],
        "why_h": "Bối cảnh",
        "why": "Website cũ cần một nền tảng dễ cập nhật nội dung và deploy được liên tục. Bản dựng "
               "lại chuyển sang Next.js với nội dung viết bằng MDX, để sửa bài không phải đụng vào "
               "mã nguồn.",
        "cards_h": "Điểm chính",
        "cards": [
            ("Nội dung tách khỏi mã",
             "Bài viết và trang tĩnh nằm trong file MDX, chỉnh sửa không cần chạm vào component."),
            ("Deploy liên tục",
             "Đẩy lên nhánh chính là Vercel tự dựng và phát hành, không có bước thủ công."),
            ("Tối ưu sẵn cho tìm kiếm",
             "Cấu trúc trang, metadata và sitemap được đặt ngay từ đầu thay vì vá về sau."),
        ],
        "stack": ["Next.js", "Tailwind CSS", "MDX", "Vercel"],
    },
    {
        "slug": "portfolio",
        "name": "Portfolio_LongLeo",
        "repo": "LongLeo287/Portfolio_LongLeo",
        "eyebrow": "Mã nguồn mở",
        "tagline": "Chính trang portfolio bạn vừa xem — toàn bộ mã nguồn công khai, không framework, "
                   "không bước build.",
        "meta": [("Ngôn ngữ", "HTML · CSS · JS"), ("Dự án hiển thị", "174"),
                 ("Tải lần đầu", "~226 KB"), ("Framework", "không có")],
        "why_h": "Được dựng thế nào",
        "why": "Không React, không bundler, không bước build. Toàn bộ 174 dự án nạp từ một file JSON "
               "duy nhất. Mở server tĩnh lên là chạy — mười năm nữa vẫn mở được, vì không có phụ "
               "thuộc nào để mà mục.",
        "cards_h": "Vài điểm đáng nói",
        "cards": [
            ("Chuyển động theo cuộn",
             "Bốn animation gắn thẳng vào vị trí cuộn bằng animation-timeline của trình duyệt — "
             "tính ngoài luồng chính, không listener, không rAF."),
            ("Chỉ hai origin bên ngoài",
             "Icon là SVG inline, thư viện cuộn mượt self-host và pin phiên bản. Chỉ còn Google "
             "Fonts và thumbnail YouTube là gọi ra ngoài."),
            ("Ảnh responsive tự sinh",
             "Mỗi ảnh có bản 480w và 960w kèm srcset, sinh bằng một script Python. Video mới trên "
             "YouTube cũng có script tự thêm vào."),
            ("Song ngữ chia sẻ được",
             "Việt/Anh chọn qua tham số trên URL, nên link tiếng Anh gửi đi được và đã khai báo "
             "hreflang cho công cụ tìm kiếm."),
        ],
        "stack": ["HTML", "CSS", "Vanilla JS", "Lenis", "Vercel"],
    },
]

PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#0c0a09" />
  <link rel="canonical" href="{site}/labs/{slug}.html" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎬</text></svg>" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{site}/labs/{slug}.html" />
  <meta property="og:image" content="{site}/assets/img/labs/{slug}.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{site}/assets/img/labs/{slug}.jpg" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@300..700&family=Space+Grotesk:wght@300..700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/tokens.css?v={ver}" />
  <link rel="stylesheet" href="../assets/css/styles.css?v={ver}" />
  <link rel="stylesheet" href="../assets/css/labs.css?v={ver}" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareSourceCode",
    "name": "{name}",
    "description": "{desc}",
    "codeRepository": "https://github.com/{repo}",
    "programmingLanguage": "{lang}",
    "author": {{ "@type": "Person", "name": "Hà Đình Long", "url": "{site}/" }}
  }}
  </script>

  <script>
    if (localStorage.getItem('portfolio_theme') === 'light') {{
      document.documentElement.classList.add('light-theme');
    }}
  </script>
</head>
<body class="lab-page">
  <a class="skip-link" href="#lab-main">Bỏ qua tới nội dung chính</a>

  <div class="lab-bar">
    <div class="container" style="display:flex;align-items:center;justify-content:space-between;gap:16px">
      <a class="lab-back" href="../index.html#labs">← Về portfolio</a>
      <a class="btn btn-primary" href="https://github.com/{repo}" target="_blank" rel="noopener">Xem trên GitHub ↗</a>
    </div>
  </div>

  <header class="lab-hero">
    <div class="container">
      <span class="lab-eyebrow">{eyebrow}</span>
      <h1>{name}</h1>
      <p class="lab-tagline">{tagline}</p>

      <div class="lab-meta">{meta}</div>

      <div class="lab-actions">
        {live_btn}<a class="btn {gh_class}" href="https://github.com/{repo}" target="_blank" rel="noopener">Xem mã nguồn ↗</a>
        <a class="btn btn-glass" href="../index.html#labs">Các dự án khác</a>
      </div>

      <div class="lab-shot">
        <img src="../assets/img/labs/{slug}.jpg"
             srcset="../assets/img/labs/{slug}-480.webp 480w, ../assets/img/labs/{slug}-960.webp 960w"
             sizes="(max-width: 900px) 92vw, 1100px"
             width="1200" height="600" alt="{name}" decoding="async" />
      </div>
    </div>
  </header>

  <main class="lab-body" id="lab-main">
    <div class="container">
      <section class="lab-section">
        <h2>{why_h}</h2>
        <p>{why}</p>
      </section>

      <section class="lab-section">
        <h2>{cards_h}</h2>
        <div class="lab-grid">{cards}</div>
      </section>

      <section class="lab-section">
        <h2>Công nghệ</h2>
        <div class="lab-meta">{stack}</div>
        {note}
      </section>

      <section class="lab-cta">
        <h2>Muốn xem sâu hơn?</h2>
        <p>Toàn bộ mã nguồn, tài liệu và lịch sử phát triển đều công khai trên GitHub.</p>
        <div class="lab-actions">
          <a class="btn btn-primary" href="https://github.com/{repo}" target="_blank" rel="noopener">Mở repo ↗</a>
          <a class="btn btn-glass" href="../index.html#contact">Liên hệ hợp tác</a>
        </div>
      </section>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p>Hà Đình Long © 2026 | All Rights Reserved.</p>
      <p>Video Editor Portfolio</p>
    </div>
  </footer>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build(lab):
    meta = "".join(f'<span class="lab-chip">{esc(k)} <b>{esc(v)}</b></span>' for k, v in lab["meta"])
    cards = "".join(
        f'<article class="lab-card"><span class="lab-num">{i:02d}</span>'
        f'<h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (t, d) in enumerate(lab["cards"], 1))
    stack = "".join(f'<span class="lab-chip"><b>{esc(s)}</b></span>' for s in lab["stack"])
    note = f'<p>{esc(lab["note"])}</p>' if lab.get("note") else ""
    # Mô tả meta phải dưới 160 ký tự để Google không cắt giữa chừng.
    desc = re.sub(r"\s+", " ", lab["tagline"]).strip()
    if len(desc) > 155:
        desc = desc[:152].rsplit(" ", 1)[0] + "…"
    live = lab.get("live")
    live_btn = ('<a class="btn btn-primary" href="%s" target="_blank" rel="noopener">Xem website ↗</a>\n        '
                % live) if live else ""
    page_title = lab.get("title") or f'{lab["name"]} — Dự án của Hà Đình Long'
    return PAGE.format(
        page_title=esc(page_title), live_btn=live_btn, gh_class="btn-glass" if live else "btn-primary",
        site=SITE, ver=VER, slug=lab["slug"], name=esc(lab["name"]), repo=lab["repo"],
        eyebrow=esc(lab["eyebrow"]), tagline=esc(lab["tagline"]), desc=esc(desc),
        lang=esc(lab["stack"][0]), meta=meta, why_h=esc(lab["why_h"]), why=esc(lab["why"]),
        cards_h=esc(lab["cards_h"]), cards=cards, stack=stack, note=note)


def main():
    os.chdir(ROOT)
    os.makedirs("labs", exist_ok=True)
    keep = [l for l in LABS if l["slug"] in IN_PORTFOLIO]
    for lab in keep:
        path = f"labs/{lab['slug']}.html"
        io.open(path, "w", encoding="utf-8").write(build(lab))
        print(f"  {os.path.getsize(path)//1024:>3} KB  {path}")
    print(f"\nĐã sinh {len(keep)} trang. "
          f"{len(LABS) - len(keep)} dự án còn lại có landing page trong repo riêng.")


if __name__ == "__main__":
    raise SystemExit(main())
