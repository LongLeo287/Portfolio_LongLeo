css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

original_size = len(css)
changes = []

# =============================================================================
# TARGETED BASE-STYLE FIXES (change semantic vars so both modes work correctly)
# =============================================================================

# FIX 1: .tag badge — color: var(--bg-main) = WHITE in light mode (invisible!)
# Change to a fixed dark color that works on both dark/light bg
old = """    .tag {
      position: absolute;
      left: 18px;
      top: 18px;
      z-index: 1;
      border-radius: 999px;
      background: rgba(255,255,255,.92);
      color: var(--bg-main);
      padding: 5px 11px;
      font-size: 12px;
      font-weight: 900;
      backdrop-filter: blur(10px);
    }"""
new = """    .tag {
      position: absolute;
      left: 18px;
      top: 18px;
      z-index: 1;
      border-radius: 999px;
      background: rgba(255,255,255,.92);
      color: #1c1917;
      padding: 5px 11px;
      font-size: 12px;
      font-weight: 900;
      backdrop-filter: blur(10px);
    }"""
if old in css:
    css = css.replace(old, new)
    changes.append("FIX 1: .tag color — hardcode #1c1917 (visible in both modes)")

# FIX 2: .portfolio-thumb::after — dark overlay too heavy in light mode
# Add a lighter version for light mode via light-theme override
PORTFOLIO_LIGHT_OVERRIDES = """
/* ── Portfolio light mode ── */
:root.light-theme .portfolio-thumb::after {
  background: linear-gradient(to top, rgba(28,25,23,0.7), rgba(28,25,23,0.04), transparent);
}
:root.light-theme .tag {
  background: rgba(255, 255, 255, 0.95);
  color: #1c1917;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
:root.light-theme .portfolio-body {
  background: #ffffff;
}
:root.light-theme .portfolio-body h3 {
  color: var(--text-main);
}
:root.light-theme .client {
  color: #a16207;
}

/* ── Skill cards light mode ── */
:root.light-theme .skill-card {
  background: #ffffff;
  border-color: rgba(28, 25, 23, 0.09);
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}
:root.light-theme .skill-card p {
  color: var(--text-main);
}

/* ── About section full light mode ── */
:root.light-theme .about-content h2 {
  color: var(--text-main);
}
:root.light-theme .about-text {
  color: var(--text-muted);
}
:root.light-theme .about-image-inner {
  background: #ffffff;
  box-shadow: 0 8px 40px rgba(0,0,0,0.10);
}

/* ── Contact items light mode ── */
:root.light-theme .contact-item {
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(28,25,23,0.08);
}
:root.light-theme .contact-item .ci-icon {
  color: var(--brown);
}
:root.light-theme .contact-item small {
  color: #92400e;
}
:root.light-theme .contact-item strong,
:root.light-theme .contact-item a {
  color: var(--brown);
}

/* ── Social grid full light mode ── */
:root.light-theme .social-grid a {
  background: rgba(255,255,255,0.6);
  color: var(--brown);
  border: 1px solid rgba(122,76,37,0.15);
}
:root.light-theme .social-grid a:hover {
  background: var(--amber);
  color: #1c1917;
  border-color: transparent;
}

/* ── Back to top light ── */
:root.light-theme .back-to-top {
  background: #1c1917;
  color: #fcd34d;
  border-color: #1c1917;
}
:root.light-theme .back-to-top:hover {
  background: var(--brown);
}

/* ── Eyebrow in services/tools section ── */
:root.light-theme #services .eyebrow,
:root.light-theme #about .eyebrow,
:root.light-theme #tools .eyebrow,
:root.light-theme #portfolio .eyebrow {
  background: rgba(252, 211, 77, 0.2);
  border-color: rgba(252, 211, 77, 0.35);
  color: #92400e;
}

/* ── Cursor spotlight light ── */
:root.light-theme .cursor-spotlight {
  background: radial-gradient(circle, rgba(245,158,11,0.08) 0%, transparent 70%);
}

/* ── Scroll progress bar ── */
:root.light-theme .scroll-progress {
  background: var(--orange);
}

/* ── Hero actions btn-primary light ── */
:root.light-theme .btn-primary {
  background: #1c1917;
  color: #ffffff;
}
:root.light-theme .btn-primary:hover {
  background: #292524;
}

/* ── Empty state light ── */
:root.light-theme .empty-state {
  background: rgba(28,25,23,0.04);
  border-color: rgba(28,25,23,0.15);
  color: var(--text-muted);
}

/* ── Portfolio filter section wrapper ── */
:root.light-theme #portfolio {
  background: #f5f5f4;
}

/* ── Showcase slide overlay gradient ── */
:root.light-theme .showcase-slide-wrapper {
  background: #f5f5f4;
}

/* ── Tools section wrapper ── */
:root.light-theme .tools-grid-wrapper {
  background: transparent;
}
:root.light-theme .tools-group-title {
  color: var(--text-muted);
  border-bottom-color: rgba(28,25,23,0.1);
}

/* ── Form label text ── */
:root.light-theme label {
  color: var(--brown);
}

/* ── Contact form area ── */
:root.light-theme .contact-form input,
:root.light-theme .contact-form textarea {
  background: rgba(255,255,255,0.8);
  border-color: rgba(122,76,37,0.2);
  color: var(--brown);
}
:root.light-theme .contact-form input::placeholder,
:root.light-theme .contact-form textarea::placeholder {
  color: rgba(122,76,37,0.5);
}
:root.light-theme .contact-form input:focus,
:root.light-theme .contact-form textarea:focus {
  border-color: var(--brown);
  background: #ffffff;
}
"""

# Find the final override block and append after it
ANCHOR = "/* Social grid light theme */"
if ANCHOR in css:
    # Already added some, just append
    css = css + PORTFOLIO_LIGHT_OVERRIDES
    changes.append("FIX 2-N: Added portfolio, skills, about, contact-item, eyebrow, form, btn-primary light overrides")
else:
    css = css + PORTFOLIO_LIGHT_OVERRIDES
    changes.append("FIX 2-N: Added comprehensive portfolio and section light overrides (appended)")

# FIX: site-footer base color (was rgba white, now semantic var)
old_footer = """    .site-footer {
      background: var(--bg-main);
      color: rgba(255,255,255,.6);
      padding: 30px 0;
      font-size: 14px;
    }"""
new_footer = """    .site-footer {
      background: var(--bg-main);
      color: var(--text-muted);
      padding: 30px 0;
      font-size: 14px;
    }"""
if old_footer in css:
    css = css.replace(old_footer, new_footer)
    changes.append("FIX: site-footer base color → --text-muted")

# Write file
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

opens = css.count('{')
closes = css.count('}')
print(f"Applied {len(changes)} fixes:")
for c in changes:
    print(f"  + {c}")
print(f"\nBrace balance: {opens}/{closes} = {opens-closes}")
print(f"Size: {original_size} → {len(css)} (+{len(css)-original_size} bytes)")
