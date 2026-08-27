#!/usr/bin/env python3
"""Landing page cho SEOSONA UX-UI — Swiss Precision Grid & Interactive Token Engine.

SEOSONA UX-UI là hệ thống design token thuần CSS và thư viện 28 component độc lập.
Trang được dựng theo phong cách Swiss Design & Bauhaus: Lưới tài liệu rõ ràng,
chuyển đổi sáng/tối tức thời bằng biến CSS gốc, bộ thử nghiệm bảng màu trực tiếp,
studio chuyển động 461 công thức và danh mục component sao chép 1-click.

    python scripts/landing-seosona-ux-ui.py
"""
import io
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "repo-landing", "SEOSONA-UX-UI")
SITE = "https://seosona-ux-ui.vercel.app"
PORTFOLIO = "https://portfolio-long-leo.vercel.app"
REPO = "LongLeo287/SEOSONA-UX-UI"

VERSION = "2.4.0"
N_COMPONENTS = 28
N_MOTION = 461
N_TOKENS = 14
N_PALETTES = 5

def generate_page():
    os.makedirs(OUT, exist_ok=True)
    assets_dir = os.path.join(OUT, "assets")
    landing_assets = os.path.join(OUT, "landing", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(landing_assets, exist_ok=True)

    # Đồng bộ assets giữa OUT và OUT/landing
    for src_dir, dst_dir in [(assets_dir, landing_assets), (landing_assets, assets_dir)]:
        if os.path.exists(src_dir):
            for f in os.listdir(src_dir):
                if not f.startswith("."):
                    shutil.copyfile(os.path.join(src_dir, f), os.path.join(dst_dir, f))

    html_content = f"""<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SEOSONA UX-UI — Hệ Thống Design Token & 28 Component Chuẩn Thụy Sĩ</title>
  <meta name="description" content="Hệ thống design token thuần CSS, 28 component sao chép 1-click, 461 công thức chuyển động và công tắc sáng/tối native không phụ thuộc framework." />
  <meta name="theme-color" content="#ffffff" />

  <!-- Canonical & Alternate Links -->
  <link rel="canonical" href="{SITE}" />
  <link rel="alternate" hreflang="vi" href="{SITE}/" />
  <link rel="alternate" hreflang="en" href="{SITE}/?lang=en" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="SEOSONA UX-UI — Hệ Thống Design Token & 28 Component Chuẩn Thụy Sĩ" />
  <meta property="og:description" content="Design token thuần CSS, 28 component HTML/CSS độc lập, 461 công thức chuyển động và bảng màu động." />
  <meta property="og:url" content="{SITE}" />
  <meta property="og:image" content="{SITE}/assets/seosona_ux_grid.webp" />

  <!-- Google Fonts: Plus Jakarta Sans & Be Vietnam Pro & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,600&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&display=swap" rel="stylesheet" />

  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    :root {{
      --bg: #ffffff;
      --surface: #f8fafc;
      --surface-2: #f1f5f9;
      --line: #e2e8f0;
      --line-2: #cbd5e1;
      --text: #0f172a;
      --muted: #475569;
      --dim: #5e728e;
      --brand: #1d4ed8;
      --brand-soft: #dbeafe;
      --ok: #04845c;
      --warn: #b45309;
      --danger: #dc2626;

      --font-display: 'Plus Jakarta Sans', 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-heading: 'Plus Jakarta Sans', 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-sans: 'Plus Jakarta Sans', 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, Menlo, monospace;

      --radius-sm: 6px;
      --radius-md: 12px;
      --radius-lg: 20px;
      --radius-full: 9999px;
      --dur-fast: 0.15s;
      --dur-norm: 0.3s;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}

    [data-theme="dark"] {{
      --bg: #0b1120;
      --surface: #111c33;
      --surface-2: #16233d;
      --line: #1e293b;
      --line-2: #334155;
      --text: #e8eefb;
      --muted: #a3b3cc;
      --dim: #7c8ba0;
      --brand: #60a5fa;
      --brand-soft: #17284a;
      --ok: #34d399;
      --warn: #fbbf24;
      --danger: #f87171;
    }}

    html {{
      scroll-behavior: smooth;
      -webkit-text-size-adjust: 100%;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 15.5px;
      line-height: 1.68;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
      transition: background 0.3s var(--ease), color 0.3s var(--ease);
      position: relative;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    :focus-visible {{
      outline: 2px solid var(--brand);
      outline-offset: 3px;
      border-radius: 4px;
    }}

    .wrap {{
      width: min(1200px, 100% - 2.8rem);
      margin-inline: auto;
    }}

    h1, h2, h3, h4 {{
      font-family: var(--font-heading);
      letter-spacing: -0.025em;
      font-weight: 800;
      line-height: 1.2;
    }}

    /* Swiss Clean Top Navigation Bar */
    .swiss-nav {{
      position: sticky;
      top: 0;
      z-index: 500;
      background: color-mix(in srgb, var(--bg) 90%, transparent);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-bottom: 1px solid var(--line);
      height: 70px;
      display: flex;
      align-items: center;
    }}

    .swiss-nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      width: min(1200px, 100% - 2.8rem);
      margin-inline: auto;
    }}

    .brand-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }}

    .swiss-cross {{
      width: 26px;
      height: 26px;
      border-radius: 7px;
      background: var(--brand);
      display: grid;
      place-items: center;
      color: #fff;
      font-weight: 900;
      font-size: 16px;
      box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
    }}

    .brand-title {{
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }}

    .brand-version {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--brand);
      background: var(--brand-soft);
      padding: 2px 7px;
      border-radius: var(--radius-full);
      border: 1px solid var(--line-2);
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .nav-link {{
      font-size: 13.5px;
      font-weight: 600;
      color: var(--muted);
      padding: 6px 11px;
      border-radius: var(--radius-sm);
      transition: all var(--dur-fast);
    }}

    .nav-link:hover {{
      color: var(--brand);
      background: var(--surface-2);
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}

    .nav-icon-btn {{
      height: 38px;
      border-radius: var(--radius-full);
      border: 1px solid var(--line-2);
      background: var(--surface);
      color: var(--muted);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      padding: 0 12px;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      transition: all var(--dur-fast);
    }}

    .nav-icon-btn:hover {{
      color: var(--brand);
      border-color: var(--brand);
      transform: translateY(-1px);
    }}

    .lang-toggle-btn {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text);
    }}

    .btn-cta {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--brand);
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 700;
      padding: 8px 18px;
      border-radius: var(--radius-full);
      box-shadow: 0 4px 18px rgba(29, 78, 216, 0.25);
      transition: all var(--dur-fast);
      cursor: pointer;
    }}

    .btn-cta:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(29, 78, 216, 0.4);
    }}

    /* HERO SECTION */
    .hero-section {{
      padding: 60px 0 40px;
      text-align: center;
    }}

    .swiss-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--brand);
      margin-bottom: 20px;
      padding: 4px 14px;
      background: var(--brand-soft);
      border: 1px solid var(--line-2);
      border-radius: var(--radius-full);
    }}

    .hero-title {{
      font-size: clamp(2.2rem, 5.5vw, 4.2rem);
      line-height: 1.08;
      max-width: 22ch;
      margin: 0 auto 22px;
    }}

    .gradient-swiss {{
      background: linear-gradient(135deg, var(--brand) 0%, #0ea5e9 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-desc {{
      color: var(--muted);
      font-size: clamp(1rem, 1.8vw, 1.18rem);
      max-width: 70ch;
      margin: 0 auto 34px;
      line-height: 1.7;
    }}

    .hero-acts {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      justify-content: center;
      margin-bottom: 40px;
    }}

    .btn-lg {{
      padding: 12px 24px;
      font-size: 15px;
      border-radius: var(--radius-full);
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all var(--dur-fast);
    }}

    .btn-swiss-pri {{
      background: var(--brand);
      color: #ffffff;
      box-shadow: 0 8px 24px rgba(29, 78, 216, 0.25);
    }}
    .btn-swiss-pri:hover {{
      transform: translateY(-2px);
      box-shadow: 0 12px 32px rgba(29, 78, 216, 0.4);
    }}

    .btn-swiss-sec {{
      background: var(--surface);
      border: 1px solid var(--line-2);
      color: var(--text);
    }}
    .btn-swiss-sec:hover {{
      border-color: var(--brand);
      color: var(--brand);
      transform: translateY(-2px);
    }}

    /* Machine Gauges */
    .gauges-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: var(--surface);
      margin-bottom: 70px;
    }}
    .gauge-item {{
      padding: 20px 24px;
      border-right: 1px solid var(--line);
    }}
    .gauge-item:last-child {{
      border-right: 0;
    }}
    .gauge-val {{
      font-size: 2rem;
      font-weight: 800;
      color: var(--brand);
      line-height: 1.1;
      font-family: var(--font-heading);
      margin-bottom: 4px;
    }}
    .gauge-label {{
      font-size: 12px;
      color: var(--dim);
      letter-spacing: 0.05em;
      font-weight: 600;
      text-transform: uppercase;
    }}

    /* SECTION HEADERS */
    .section-head {{
      text-align: center;
      max-width: 740px;
      margin: 0 auto 50px;
    }}
    .section-eyebrow {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--brand);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      display: inline-block;
      margin-bottom: 12px;
    }}
    .section-title {{
      font-size: clamp(1.8rem, 3.8vw, 2.7rem);
      margin-bottom: 16px;
    }}
    .section-desc {{
      color: var(--muted);
      font-size: 15.5px;
      line-height: 1.7;
    }}

    /* ==========================================================================
       1. INTERACTIVE LIVE TOKEN ENGINE & PALETTE TESTER
       ========================================================================== */
    .palettes-section {{
      padding: 40px 0 90px;
    }}
    .palette-swatches-wrap {{
      display: flex;
      justify-content: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 40px;
    }}
    .palette-card-btn {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all var(--dur-fast);
    }}
    .palette-card-btn:hover, .palette-card-btn.active {{
      border-color: var(--brand);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }}
    .swatch-dots {{
      display: flex;
      gap: 5px;
    }}
    .swatch-dot {{
      width: 14px;
      height: 14px;
      border-radius: 50%;
    }}
    .palette-title {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--text);
    }}

    .palette-preview-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      align-items: center;
    }}
    @media (max-width: 900px) {{
      .palette-preview-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .swiss-poster-box {{
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--line);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
    }}
    .swiss-poster-img {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .tokens-code-box {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 24px;
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.7;
      text-align: left;
    }}

    /* ==========================================================================
       2. 28-COMPONENT COPY-PASTE CATALOG
       ========================================================================== */
    .catalog-section {{
      padding: 40px 0 90px;
    }}
    .catalog-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
    }}
    .cat-item-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 20px;
      text-align: left;
      transition: all var(--dur-fast);
    }}
    .cat-item-card:hover {{
      border-color: var(--brand);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
    }}
    .cat-badge {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--brand);
      background: var(--brand-soft);
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      display: inline-block;
      margin-bottom: 8px;
    }}
    .cat-name {{
      font-size: 16px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 8px;
    }}
    .cat-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .cat-tag {{
      font-size: 11.5px;
      color: var(--muted);
      background: var(--surface-2);
      padding: 3px 8px;
      border-radius: var(--radius-sm);
    }}
    .btn-copy-code {{
      width: 100%;
      padding: 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--line-2);
      background: var(--bg);
      color: var(--text);
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all var(--dur-fast);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}
    .btn-copy-code:hover {{
      background: var(--brand);
      color: #fff;
      border-color: var(--brand);
    }}

    /* ==========================================================================
       3. 461 MOTION PHYSICS STUDIO
       ========================================================================== */
    .motion-section {{
      padding: 40px 0 90px;
    }}
    .motion-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      align-items: center;
    }}
    @media (max-width: 900px) {{
      .motion-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .motion-speeds-wrap {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      text-align: left;
    }}
    .motion-speed-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all var(--dur-fast);
    }}
    .motion-speed-card:hover, .motion-speed-card.active {{
      border-color: var(--brand);
      transform: translateX(4px);
    }}
    .motion-speed-val {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--brand);
      background: var(--brand-soft);
      padding: 2px 8px;
      border-radius: var(--radius-sm);
    }}

    /* Toast Notification */
    .toast-box {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--brand);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 999;
    }}
    .toast-box.show {{
      transform: translateY(0);
      opacity: 1;
    }}

    /* FAQ ACCORDION */
    .faq-section {{
      padding: 40px 0 90px;
    }}
    .faq-list {{
      max-width: 800px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      text-align: left;
    }}
    .faq-item {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: hidden;
      transition: border-color var(--dur-fast);
    }}
    .faq-item.open {{
      border-color: var(--brand);
    }}
    .faq-question {{
      padding: 16px 20px;
      font-weight: 700;
      font-size: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }}
    .faq-answer {{
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease-out;
      padding: 0 20px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.65;
    }}
    .faq-item.open .faq-answer {{
      padding-bottom: 16px;
    }}

    /* FOOTER */
    .footer {{
      border-top: 1px solid var(--line);
      background: var(--surface);
      padding: 50px 0 30px;
      text-align: center;
      font-size: 13px;
      color: var(--dim);
    }}
    .footer-links {{
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-bottom: 20px;
      font-weight: 600;
      color: var(--muted);
    }}
    .footer-links a:hover {{
      color: var(--brand);
    }}
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="swiss-nav" id="navbar">
    <div class="swiss-nav-inner">
      <div class="brand-box">
        <div class="swiss-cross">+</div>
        <a href="#hero" class="brand-title">SEOSONA UX-UI</a>
        <span class="brand-version">v{VERSION} TOKENS</span>
      </div>

      <nav class="nav-links">
        <a href="#tokens" class="nav-link" data-i18n="nav_tokens">Design Tokens</a>
        <a href="#catalog" class="nav-link" data-i18n="nav_catalog">28 Components</a>
        <a href="#motion" class="nav-link" data-i18n="nav_motion">461 Motion</a>
        <a href="#faq" class="nav-link" data-i18n="nav_faq">FAQ</a>
      </nav>

      <div class="nav-actions">
        <!-- Light / Dark Theme Switcher Button -->
        <button class="nav-icon-btn" id="themeToggleBtn" aria-label="Toggle Theme" title="Đổi chế độ Sáng / Tối">
          <span id="themeIcon">🌙</span>
          <span id="themeText" data-i18n="theme_btn">Chế độ tối</span>
        </button>

        <!-- 1-Click Language Flag Toggle -->
        <button class="nav-icon-btn lang-toggle-btn" id="langToggleBtn" aria-label="Toggle Language" title="Đổi ngôn ngữ (VI / EN)">
          <span id="flagIcon">🇻🇳</span>
          <span id="langText">VI</span>
        </button>

        <!-- GitHub Icon Button -->
        <a href="https://github.com/{REPO}" target="_blank" rel="noopener" class="nav-icon-btn" aria-label="GitHub Repository" title="GitHub Repository">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
        </a>

        <!-- CTA Button -->
        <a href="https://github.com/{REPO}" target="_blank" rel="noopener" class="btn-cta" data-i18n="btn_github_explore">
          <span>🎨 Khám phá Repo ↗</span>
        </a>
      </div>
    </div>
  </header>

  <main>
  <!-- HERO SECTION -->
  <section class="hero-section wrap" id="hero">
    <div class="swiss-pill" data-i18n="hero_pill">SWISS PRECISION GRID · 28 COMPONENTS · 461 MOTION CURVES · ZERO RUNTIME CSS</div>
    <h1 class="hero-title" data-i18n="hero_title">
      Hệ Thống Design Token & 28 Component Chuẩn Thụy Sĩ<br />
      <span class="gradient-swiss">Sao Chép Trực Tiếp Không Phụ Thuộc Vào Framework Hay Thư Viện Quản Lý Theme</span>
    </h1>
    <p class="hero-desc" data-i18n="hero_desc">
      Bộ quy chuẩn thiết kế thuần HTML/CSS được xây dựng theo triết lý Bauhaus và Swiss Typography: Chuyển đổi Dark / Light mode tức thời bằng CSS Variables, 5 bảng màu động kiểm thử trực tiếp, và 461 công thức chuyển động vật lý.
    </p>

    <div class="hero-acts">
      <a href="#tokens" class="btn-lg btn-swiss-pri" data-i18n="hero_cta_tokens">
        🎨 Trải Nghiệm Token Engine
      </a>
      <a href="#catalog" class="btn-lg btn-swiss-sec" data-i18n="hero_cta_catalog">
        📦 Khám Phá 28 Components
      </a>
    </div>

    <!-- MACHINE GAUGES -->
    <div class="gauges-grid">
      <div class="gauge-item">
        <div class="gauge-val">{N_TOKENS}</div>
        <div class="gauge-label" data-i18n="g_1">Nhóm Design Tokens lõi</div>
      </div>
      <div class="gauge-item">
        <div class="gauge-val">{N_COMPONENTS}</div>
        <div class="gauge-label" data-i18n="g_2">Component HTML/CSS độc lập</div>
      </div>
      <div class="gauge-item">
        <div class="gauge-val">{N_MOTION}</div>
        <div class="gauge-label" data-i18n="g_3">Công thức chuyển động vật lý</div>
      </div>
      <div class="gauge-item">
        <div class="gauge-val">{N_PALETTES}</div>
        <div class="gauge-label" data-i18n="g_4">Bảng màu chuẩn hoá đa ngành</div>
      </div>
    </div>
  </section>

  <!-- 1. INTERACTIVE LIVE TOKEN ENGINE & PALETTE TESTER -->
  <section class="wrap palettes-section" id="tokens">
    <div class="section-head">
      <span class="section-eyebrow" data-i18n="token_eyebrow">Interactive Palette Engine</span>
      <h2 class="section-title" data-i18n="token_title">Bộ Thử Nghiệm Bảng Màu & Token Trực Tiếp</h2>
      <p class="section-desc" data-i18n="token_desc">Bấm vào các bảng màu dưới đây để chứng kiến toàn bộ hệ thống token và giao diện đổi màu ngay lập tức mà không cần tải lại trang.</p>
    </div>

    <!-- Palette Swatches Selector -->
    <div class="palette-swatches-wrap">
      <button class="palette-card-btn active" data-brand="#1d4ed8" data-soft="#dbeafe">
        <div class="swatch-dots">
          <span class="swatch-dot" style="background:#1d4ed8;"></span>
          <span class="swatch-dot" style="background:#0ea5e9;"></span>
          <span class="swatch-dot" style="background:#e2e8f0;"></span>
        </div>
        <span class="palette-title">B2B Sáng</span>
      </button>

      <button class="palette-card-btn" data-brand="#3b82f6" data-soft="#1e293b">
        <div class="swatch-dots">
          <span class="swatch-dot" style="background:#3b82f6;"></span>
          <span class="swatch-dot" style="background:#1e293b;"></span>
          <span class="swatch-dot" style="background:#0f172a;"></span>
        </div>
        <span class="palette-title">B2B Tối</span>
      </button>

      <button class="palette-card-btn" data-brand="#ec4899" data-soft="#fce7f3">
        <div class="swatch-dots">
          <span class="swatch-dot" style="background:#ec4899;"></span>
          <span class="swatch-dot" style="background:#f59e0b;"></span>
          <span class="swatch-dot" style="background:#8b5cf6;"></span>
        </div>
        <span class="palette-title">B2C Rực Rỡ</span>
      </button>

      <button class="palette-card-btn" data-brand="#059669" data-soft="#d1fae5">
        <div class="swatch-dots">
          <span class="swatch-dot" style="background:#059669;"></span>
          <span class="swatch-dot" style="background:#0f766e;"></span>
          <span class="swatch-dot" style="background:#134e4a;"></span>
        </div>
        <span class="palette-title">Fintech</span>
      </button>

      <button class="palette-card-btn" data-brand="#0891b2" data-soft="#cffafe">
        <div class="swatch-dots">
          <span class="swatch-dot" style="background:#0891b2;"></span>
          <span class="swatch-dot" style="background:#22d3ee;"></span>
          <span class="swatch-dot" style="background:#cffafe;"></span>
        </div>
        <span class="palette-title">Y Tế</span>
      </button>
    </div>

    <!-- Palette Live Code & Graphic Grid -->
    <div class="palette-preview-grid">
      <div class="swiss-poster-box">
        <img src="assets/seosona_ux_grid.webp" class="swiss-poster-img" alt="Swiss Precision & Grid System Layout" width="1280" height="720" />
      </div>

      <div class="tokens-code-box">
        <div style="color:var(--brand);font-weight:700;margin-bottom:12px;">/* tokens.css — Zero-Runtime Tokens */</div>
        <div>:root {{</div>
        <div style="padding-left:18px;">--brand: <span id="codeBrand" style="color:var(--brand);font-weight:700;">#1d4ed8</span>;</div>
        <div style="padding-left:18px;">--brand-soft: <span id="codeSoft" style="color:var(--brand);font-weight:700;">#dbeafe</span>;</div>
        <div style="padding-left:18px;">--font-heading: 'Plus Jakarta Sans', sans-serif;</div>
        <div style="padding-left:18px;">--radius-md: 12px;</div>
        <div style="padding-left:18px;">--ease-out: cubic-bezier(0.16, 1, 0.3, 1);</div>
        <div>}}</div>
        <div style="margin-top:16px;color:var(--muted);font-size:12px;">
          ✦ Sửa biến CSS ở gốc, toàn bộ 28 component tự động thích ứng chuẩn xác mà không cần biên dịch lại.
        </div>
      </div>
    </div>
  </section>

  <!-- 2. 28-COMPONENT COPY-PASTE CATALOG -->
  <section class="wrap catalog-section" id="catalog">
    <div class="section-head">
      <span class="section-eyebrow" data-i18n="catalog_eyebrow">Component Library</span>
      <h2 class="section-title" data-i18n="catalog_title">Danh Mục 28 Component Độc Lập</h2>
      <p class="section-desc" data-i18n="catalog_desc">Mỗi component là một file HTML/CSS độc lập. Bấm sao chép và dán thẳng vào dự án bất kỳ (React, Vue, Astro, HTML thuần).</p>
    </div>

    <div class="catalog-grid">
      <div class="cat-item-card">
        <span class="cat-badge">THẺ & HIỂN THỊ</span>
        <div class="cat-name">Card Pricing & Blog</div>
        <div class="cat-tags">
          <span class="cat-tag">card-pricing</span>
          <span class="cat-tag">card-blog</span>
          <span class="cat-tag">card-service</span>
        </div>
        <button class="btn-copy-code" data-copy="card-pricing">📋 Sao chép Code HTML/CSS</button>
      </div>

      <div class="cat-item-card">
        <span class="cat-badge">HERO & BANNER</span>
        <div class="cat-name">Hero Centered & Split</div>
        <div class="cat-tags">
          <span class="cat-tag">hero-centered</span>
          <span class="cat-tag">hero-split</span>
        </div>
        <button class="btn-copy-code" data-copy="hero-split">📋 Sao chép Code HTML/CSS</button>
      </div>

      <div class="cat-item-card">
        <span class="cat-badge">FORM & INPUT</span>
        <div class="cat-name">Floating Labels & Multi-step</div>
        <div class="cat-tags">
          <span class="cat-tag">floating-labels</span>
          <span class="cat-tag">file-upload</span>
          <span class="cat-tag">form-multistep</span>
        </div>
        <button class="btn-copy-code" data-copy="floating-labels">📋 Sao chép Code HTML/CSS</button>
      </div>

      <div class="cat-item-card">
        <span class="cat-badge">ĐIỀU HƯỚNG</span>
        <div class="cat-name">Sticky Nav & Mega Menu</div>
        <div class="cat-tags">
          <span class="cat-tag">navbar-sticky</span>
          <span class="cat-tag">mega-menu</span>
        </div>
        <button class="btn-copy-code" data-copy="navbar-sticky">📋 Sao chép Code HTML/CSS</button>
      </div>

      <div class="cat-item-card">
        <span class="cat-badge">TƯƠNG TÁC</span>
        <div class="cat-name">Modal, Drawer & Accordion</div>
        <div class="cat-tags">
          <span class="cat-tag">modal-dialog</span>
          <span class="cat-tag">offcanvas-drawer</span>
          <span class="cat-tag">accordion-faq</span>
        </div>
        <button class="btn-copy-code" data-copy="modal-dialog">📋 Sao chép Code HTML/CSS</button>
      </div>

      <div class="cat-item-card">
        <span class="cat-badge">DỮ LIỆU & PHẢN HỒI</span>
        <div class="cat-name">Data Table & Toasts</div>
        <div class="cat-tags">
          <span class="cat-tag">data-table</span>
          <span class="cat-tag">toast-notifications</span>
          <span class="cat-tag">progress-bars</span>
        </div>
        <button class="btn-copy-code" data-copy="toast-notifications">📋 Sao chép Code HTML/CSS</button>
      </div>
    </div>
  </section>

  <!-- 3. 461 MOTION PHYSICS STUDIO -->
  <section class="wrap motion-section" id="motion">
    <div class="section-head">
      <span class="section-eyebrow" data-i18n="motion_eyebrow">Motion Physics Engine</span>
      <h2 class="section-title" data-i18n="motion_title">461 Công Thức Chuyển Động Vật Lý</h2>
      <p class="section-desc" data-i18n="motion_desc">Đường cong Bézier chuẩn mực và bảng thời lượng phân cấp chính xác từng tương tác micro-animation.</p>
    </div>

    <div class="motion-grid">
      <div class="motion-speeds-wrap">
        <div class="motion-speed-card active">
          <div>
            <div style="font-weight:700;margin-bottom:2px;">Tức thì (Micro Feedback)</div>
            <div style="font-size:12.5px;color:var(--muted);">Đổi màu khi rê chuột, phản hồi bấm nút tức thời.</div>
          </div>
          <span class="motion-speed-val">100ms</span>
        </div>

        <div class="motion-speed-card">
          <div>
            <div style="font-weight:700;margin-bottom:2px;">Nhanh (State Transition)</div>
            <div style="font-size:12.5px;color:var(--muted);">Hiện tooltip gợi ý, đổi trạng thái switch.</div>
          </div>
          <span class="motion-speed-val">200ms</span>
        </div>

        <div class="motion-speed-card">
          <div>
            <div style="font-weight:700;margin-bottom:2px;">Vừa (Layout Accordion)</div>
            <div style="font-size:12.5px;color:var(--muted);">Mở đóng FAQ accordion, trượt ngăn kéo drawer.</div>
          </div>
          <span class="motion-speed-val">300ms</span>
        </div>

        <div class="motion-speed-card">
          <div>
            <div style="font-weight:700;margin-bottom:2px;">Chậm (Scroll Reveal)</div>
            <div style="font-size:12.5px;color:var(--muted);">Hiện dần các khối nội dung khi cuộn màn hình tới.</div>
          </div>
          <span class="motion-speed-val">600ms</span>
        </div>

        <div class="motion-speed-card">
          <div>
            <div style="font-weight:700;margin-bottom:2px;">Điện ảnh (Cinematic Scene)</div>
            <div style="font-size:12.5px;color:var(--muted);">Chuyển cảnh toàn trang mượt mà.</div>
          </div>
          <span class="motion-speed-val">1200ms</span>
        </div>
      </div>

      <div class="swiss-poster-box">
        <img src="assets/seosona_ux_motion.webp" class="swiss-poster-img" alt="Motion Physics & Easing Curves" width="1280" height="720" />
      </div>
    </div>
  </section>

  <!-- FAQ ACCORDION -->
  <section class="wrap faq-section" id="faq">
    <div class="section-head">
      <span class="section-eyebrow" data-i18n="faq_eyebrow">Clear Answers</span>
      <h2 class="section-title" data-i18n="faq_title">Câu Hỏi Thường Gặp</h2>
    </div>

    <div class="faq-list">
      <div class="faq-item">
        <div class="faq-question">
          <span>Thư viện này có dùng được với React, Next.js hay Vue không?</span>
          <span>+</span>
        </div>
        <div class="faq-answer">
          Hoàn toàn tương thích 100%. Component là HTML và CSS thuần tuý nên bạn chỉ việc dán trực tiếp vào JSX hoặc template Vue mà không cần bất kỳ wrapper hay adapter phức tạp nào.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">
          <span>Vì sao không đóng gói thành npm package?</span>
          <span>+</span>
        </div>
        <div class="faq-answer">
          Vì mục tiêu là bạn sở hữu 100% mã nguồn. Đóng gói npm tiện cập nhật nhưng rất khó tuỳ biến sâu. Với một hệ thống thiết kế nội bộ chuyên nghiệp, khả năng tinh chỉnh từng pixel quan trọng hơn.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">
          <span>Cơ chế chuyển đổi Sáng / Tối hoạt động ra sao?</span>
          <span>+</span>
        </div>
        <div class="faq-answer">
          Chạy bằng thuộc tính <code>data-theme="dark"</code> trên thẻ gốc HTML. Toàn bộ biến màu CSS tự động chuyển đổi đồng bộ mà không cần phụ thuộc vào bất kỳ thư viện JS nặng nề nào.
        </div>
      </div>
    </div>
  </section>
  </main>

  <!-- Toast Notification Container -->
  <div class="toast-box" id="toastBox">
    ✓ Đã sao chép mã nguồn component vào bộ nhớ tạm!
  </div>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="wrap">
      <div class="footer-links">
        <a href="#hero">Về đầu trang ↑</a>
        <a href="https://github.com/{REPO}" target="_blank" rel="noopener">GitHub Repository ↗</a>
        <a href="{PORTFOLIO}" target="_blank" rel="noopener">SEOSONA Portfolio ↗</a>
      </div>
      <p>© {VERSION} SEOSONA UX-UI — Hệ Thống Design Token & 28 Component Chuẩn Thụy Sĩ.</p>
    </div>
  </footer>

  <!-- SCRIPT LOGIC -->
  <script>
    // 1. Language Dictionary (VI / EN)
    const I18N_DICT = {{
      "vi": {{
        "nav_tokens": "Design Tokens",
        "nav_catalog": "28 Components",
        "nav_motion": "461 Motion",
        "nav_faq": "FAQ",
        "btn_github_explore": "🎨 Khám phá Repo ↗",
        "theme_btn": "Chế độ tối",
        "hero_pill": "SWISS PRECISION GRID · 28 COMPONENTS · 461 MOTION CURVES · ZERO RUNTIME CSS",
        "hero_title": "Hệ Thống Design Token & 28 Component Chuẩn Thụy Sĩ<br><span class='gradient-swiss'>Sao Chép Trực Tiếp Không Phụ Thuộc Vào Framework Hay Thư Viện Quản Lý Theme</span>",
        "hero_desc": "Bộ quy chuẩn thiết kế thuần HTML/CSS được xây dựng theo triết lý Bauhaus và Swiss Typography: Chuyển đổi Dark / Light mode tức thời bằng CSS Variables, 5 bảng màu động kiểm thử trực tiếp, và 461 công thức chuyển động vật lý.",
        "hero_cta_tokens": "🎨 Trải Nghiệm Token Engine",
        "hero_cta_catalog": "📦 Khám Phá 28 Components",
        "g_1": "Nhóm Design Tokens lõi",
        "g_2": "Component HTML/CSS độc lập",
        "g_3": "Công thức chuyển động vật lý",
        "g_4": "Bảng màu chuẩn hoá đa ngành",
        "token_eyebrow": "Interactive Palette Engine",
        "token_title": "Bộ Thử Nghiệm Bảng Màu & Token Trực Tiếp",
        "token_desc": "Bấm vào các bảng màu dưới đây để chứng kiến toàn bộ hệ thống token và giao diện đổi màu ngay lập tức mà không cần tải lại trang.",
        "catalog_eyebrow": "Component Library",
        "catalog_title": "Danh Mục 28 Component Độc Lập",
        "catalog_desc": "Mỗi component là một file HTML/CSS độc lập. Bấm sao chép và dán thẳng vào dự án bất kỳ (React, Vue, Astro, HTML thuần).",
        "motion_eyebrow": "Motion Physics Engine",
        "motion_title": "461 Công Thức Chuyển Động Vật Lý",
        "motion_desc": "Đường cong Bézier chuẩn mực và bảng thời lượng phân cấp chính xác từng tương tác micro-animation.",
        "faq_eyebrow": "Clear Answers",
        "faq_title": "Câu Hỏi Thường Gặp"
      }},
      "en": {{
        "nav_tokens": "Design Tokens",
        "nav_catalog": "28 Components",
        "nav_motion": "461 Motion",
        "nav_faq": "FAQ",
        "btn_github_explore": "🎨 Explore Repo ↗",
        "theme_btn": "Dark Mode",
        "hero_pill": "SWISS PRECISION GRID · 28 COMPONENTS · 461 MOTION CURVES · ZERO RUNTIME CSS",
        "hero_title": "Swiss Precision Design Tokens & 28 Components<br><span class='gradient-swiss'>Pure Copy-Paste Architecture Free From Framework Dependencies</span>",
        "hero_desc": "Pure HTML/CSS design token foundation engineered on Bauhaus & Swiss typography: Instant Dark/Light mode switching via native CSS variables, 5 live interactive palettes, and 461 physics motion curves.",
        "hero_cta_tokens": "🎨 Launch Token Engine",
        "hero_cta_catalog": "📦 Explore 28 Components",
        "g_1": "Core Design Token Groups",
        "g_2": "Standalone HTML/CSS Components",
        "g_3": "Physics Motion Formulations",
        "g_4": "Multi-Industry Palettes",
        "token_eyebrow": "Interactive Palette Engine",
        "token_title": "Live Interactive Palette & Token Tester",
        "token_desc": "Click any palette below to witness real-time CSS variable updates across the entire design system without page reloads.",
        "catalog_eyebrow": "Component Library",
        "catalog_title": "28 Standalone Component Library",
        "catalog_desc": "Each component is an isolated HTML/CSS module ready to copy-paste into React, Vue, Astro, or vanilla HTML.",
        "motion_eyebrow": "Motion Physics Engine",
        "motion_title": "461 Physics Motion Curves",
        "motion_desc": "Standardized Bézier curves and layered duration hierarchy for ultra-precise micro-animation feedback.",
        "faq_eyebrow": "Clear Answers",
        "faq_title": "Frequently Asked Questions"
      }}
    }};

    let currentLang = localStorage.getItem('ux_lang') || 'vi';

    function setLanguage(lang) {{
      currentLang = lang;
      localStorage.setItem('ux_lang', lang);
      document.documentElement.lang = lang;

      const flagEl = document.getElementById('flagIcon');
      const langTextEl = document.getElementById('langText');
      if (flagEl) flagEl.textContent = lang === 'vi' ? '🇻🇳' : '🇬🇧';
      if (langTextEl) langTextEl.textContent = lang === 'vi' ? 'VI' : 'EN';

      const dict = I18N_DICT[lang];
      document.querySelectorAll('[data-i18n]').forEach(el => {{
        const key = el.dataset.i18n;
        if (dict[key]) el.innerHTML = dict[key];
      }});
    }}

    document.getElementById('langToggleBtn')?.addEventListener('click', () => {{
      const next = currentLang === 'vi' ? 'en' : 'vi';
      setLanguage(next);
    }});

    // 2. Light / Dark Theme Switcher
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    themeBtn?.addEventListener('click', () => {{
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (isDark) {{
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeIcon) themeIcon.textContent = '🌙';
        if (themeText) themeText.textContent = currentLang === 'vi' ? 'Chế độ tối' : 'Dark Mode';
      }} else {{
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeIcon) themeIcon.textContent = '☀️';
        if (themeText) themeText.textContent = currentLang === 'vi' ? 'Chế độ sáng' : 'Light Mode';
      }}
    }});

    // 3. Interactive Palette Swatches Tester
    const paletteButtons = document.querySelectorAll('.palette-card-btn');
    const codeBrand = document.getElementById('codeBrand');
    const codeSoft = document.getElementById('codeSoft');

    paletteButtons.forEach(btn => {{
      btn.addEventListener('click', function() {{
        paletteButtons.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        const brand = this.dataset.brand;
        const soft = this.dataset.soft;

        document.documentElement.style.setProperty('--brand', brand);
        document.documentElement.style.setProperty('--brand-soft', soft);

        if (codeBrand) codeBrand.textContent = brand;
        if (codeSoft) codeSoft.textContent = soft;
      }});
    }});

    // 4. Copy Code Toast Simulation
    const toastBox = document.getElementById('toastBox');
    document.querySelectorAll('.btn-copy-code').forEach(btn => {{
      btn.addEventListener('click', function() {{
        const name = this.dataset.copy;
        if (toastBox) {{
          toastBox.textContent = currentLang === 'vi' ? `✓ Đã sao chép code component '${{name}}'!` : `✓ Copied code for '${{name}}'!`;
          toastBox.classList.add('show');
          setTimeout(() => {{
            toastBox.classList.remove('show');
          }}, 2500);
        }}
      }});
    }});

    // 5. FAQ Accordion
    document.querySelectorAll('.faq-question').forEach(q => {{
      q.addEventListener('click', function() {{
        const item = this.parentElement;
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => {{
          i.classList.remove('open');
          i.querySelector('.faq-answer').style.maxHeight = null;
        }});
        if (!isOpen) {{
          item.classList.add('open');
          const ans = item.querySelector('.faq-answer');
          ans.style.maxHeight = ans.scrollHeight + "px";
        }}
      }});
    }});

    // Initialize Language
    setLanguage(currentLang);
  </script>
</body>
</html>"""

    index_path = os.path.join(OUT, "index.html")
    landing_index = os.path.join(OUT, "landing", "index.html")
    os.makedirs(os.path.dirname(landing_index), exist_ok=True)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(landing_index, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Da sinh SEOSONA UX-UI Swiss Precision Landing Page v2.4 tai: {index_path} ({len(html_content):,} bytes)")

if __name__ == "__main__":
    generate_page()
