css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# ── FIX: Add comprehensive light-theme overrides ──────────────────────────────
# The Phase 2 overrides block only covers header, hero, stat, and a few elements.
# Missing: experience, filter-btn, service cards, tools, portfolio cards, footer, about.

LIGHT_THEME_OVERRIDES = """

/* ==========================================================================
   COMPREHENSIVE LIGHT-THEME OVERRIDES — All missing sections
   ========================================================================== */

/* ── Experience Section ── */
:root.light-theme .experience {
  background: var(--bg-surface);
  color: var(--text-main);
}
:root.light-theme .experience .eyebrow {
  background: rgba(252, 211, 77, 0.2);
  border-color: rgba(252, 211, 77, 0.35);
  color: #92400e;
}
:root.light-theme .experience .section-title h2 {
  color: var(--text-main);
}
:root.light-theme .experience .section-title p {
  color: var(--text-muted);
}
:root.light-theme .experience-card {
  border: 1px solid rgba(28, 25, 23, 0.1);
  background: #ffffff;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}
:root.light-theme .experience-card:hover {
  border-color: rgba(245, 158, 11, 0.5);
  background: #fffbf5;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.12);
}
:root.light-theme .experience-title-area h3 {
  color: var(--text-main);
}
:root.light-theme .experience-role {
  color: var(--text-muted);
}
:root.light-theme .experience-year {
  color: #92400e;
  background: rgba(252, 211, 77, 0.18);
}
:root.light-theme .experience-body p {
  color: var(--text-muted);
}
:root.light-theme .link-line {
  color: #b45309;
}
:root.light-theme .experience-logo-box {
  background: #f9fafb;
  border-color: rgba(28, 25, 23, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* ── Filter Buttons ── */
:root.light-theme .filter-btn {
  border-color: rgba(28, 25, 23, 0.12);
  background: #ffffff;
  color: var(--text-muted);
}
:root.light-theme .filter-btn:hover {
  border-color: rgba(245, 158, 11, 0.5);
  color: var(--text-main);
  background: #fffbf5;
}
:root.light-theme .filter-btn.active {
  border-color: #1c1917;
  background: #1c1917;
  color: #ffffff;
  box-shadow: 0 6px 20px rgba(28, 25, 23, 0.2);
}

/* ── Service Cards ── */
:root.light-theme .service-card {
  background: #ffffff;
  border-color: rgba(28, 25, 23, 0.09);
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}
:root.light-theme .service-card:hover {
  border-color: rgba(245, 158, 11, 0.5);
  background: #fffbf5;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.12);
}
:root.light-theme .service-icon {
  background: #f5f5f4;
  color: #b45309;
}
:root.light-theme .service-card:hover .service-icon {
  background: var(--amber);
  color: #1c1917;
}
:root.light-theme .service-card h3 {
  color: var(--text-main);
}
:root.light-theme .service-card p {
  color: var(--text-muted);
}

/* ── Portfolio Cards ── */
:root.light-theme .portfolio-card {
  background: #ffffff;
  border: 1px solid rgba(28, 25, 23, 0.09);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
:root.light-theme .portfolio-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}
:root.light-theme .portfolio-title {
  color: var(--text-main);
}
:root.light-theme .portfolio-client {
  color: var(--text-muted);
}
:root.light-theme .portfolio-cat {
  background: rgba(252, 211, 77, 0.18);
  color: #92400e;
}

/* ── About Section ── */
:root.light-theme .about-copy h2 {
  color: var(--text-main);
}
:root.light-theme .about-copy p {
  color: var(--text-muted);
}
:root.light-theme .skill-badge {
  background: rgba(28, 25, 23, 0.06);
  border-color: rgba(28, 25, 23, 0.1);
  color: var(--text-main);
}

/* ── Tools Section ── */
:root.light-theme .tool-item {
  background: #ffffff;
  border: 1px solid rgba(28, 25, 23, 0.09);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}
:root.light-theme .tool-item:hover {
  border-color: rgba(245, 158, 11, 0.4);
  box-shadow: 0 6px 24px rgba(245, 158, 11, 0.1);
}
:root.light-theme .tool-item h5 {
  color: var(--text-main);
}
:root.light-theme .tool-item span {
  color: var(--text-muted);
}
:root.light-theme .tools-group-title {
  color: var(--text-main);
}

/* ── Portfolio Section Background ── */
:root.light-theme .bg-soft {
  background: #f5f5f4;
}
:root.light-theme .bg-white {
  background: #ffffff;
}

/* ── Showcase Slider ── */
:root.light-theme .showcase-slider {
  background: #ffffff;
  border: 1px solid rgba(28, 25, 23, 0.09);
}
:root.light-theme .showcase-slide-title {
  color: var(--text-main);
}
:root.light-theme .showcase-slide-meta {
  color: var(--text-muted);
}
:root.light-theme .slider-btn {
  background: rgba(28, 25, 23, 0.08);
  color: var(--text-main);
  border-color: rgba(28, 25, 23, 0.12);
}
:root.light-theme .slider-btn:hover {
  background: rgba(28, 25, 23, 0.14);
}
:root.light-theme .slider-dot {
  background: rgba(28, 25, 23, 0.2);
}
:root.light-theme .slider-dot.active {
  background: #1c1917;
}

/* ── Section Titles (global) ── */
:root.light-theme .section-title h2 {
  color: var(--text-main);
}
:root.light-theme .section-title p {
  color: var(--text-muted);
}

/* ── Case Study Modal ── */
:root.light-theme .modal-tag {
  background: rgba(28, 25, 23, 0.07);
  color: var(--text-main);
}

/* ── Lang Toggle ── */
:root.light-theme .lang-btn {
  color: var(--text-muted);
}
:root.light-theme .lang-btn.active {
  color: var(--text-main);
  font-weight: 800;
}
:root.light-theme .lang-sep {
  color: var(--text-muted);
}

/* ── Back to Top Button ── */
:root.light-theme .back-top {
  background: #1c1917;
  color: #ffffff;
  border-color: #1c1917;
}
:root.light-theme .back-top:hover {
  background: var(--brown);
}
"""

# Find the right place to insert — after the existing Phase 2 overrides block
# (after the site-footer light-theme override)
insert_after = """:root.light-theme .site-footer {
  background: var(--bg-main) ;
  color: var(--text-muted) ;
  border-top: 1px solid var(--line) ;
}"""

if insert_after in css:
    css = css.replace(insert_after, insert_after + LIGHT_THEME_OVERRIDES)
    print("SUCCESS: Injected comprehensive light-theme overrides after site-footer override")
else:
    # Try to append at end
    css = css + LIGHT_THEME_OVERRIDES
    print("WARNING: Appended at end (could not find anchor)")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Verify
opens = css.count('{')
closes = css.count('}')
print(f"Brace balance: {opens} open / {closes} close / net: {opens - closes}")
print(f"Total size: {len(css)} bytes")
