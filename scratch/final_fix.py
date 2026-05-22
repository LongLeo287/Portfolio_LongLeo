css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

print("Applying final comprehensive fixes...")
changes = []

# ── FIX 1: .social-grid a white text (no light-theme override) ───────────────
old = """.social-grid a {
border-radius: 18px;
background: var(--bg-main);
color: var(--text-light);"""
new = """.social-grid a {
border-radius: 18px;
background: var(--bg-card);
color: var(--text-main);"""
if old in css:
    css = css.replace(old, new)
    changes.append("FIX 1: social-grid a - use semantic vars instead of hardcoded white")

# ── FIX 2: .lang-btn:hover white text ────────────────────────────────────────
old = """.lang-btn:hover {
color: var(--text-light);
}"""
new = """.lang-btn:hover {
color: var(--text-main);
}"""
if old in css:
    css = css.replace(old, new)
    changes.append("FIX 2: lang-btn:hover - use var(--text-main) for light mode compat")

# ── FIX 3: .site-footer hardcoded rgba white color ───────────────────────────
old = """.site-footer {
background: var(--bg-main);
color: rgba(255,255,255,.6);"""
new = """.site-footer {
background: var(--bg-main);
color: var(--text-muted);"""
if old in css:
    css = css.replace(old, new)
    changes.append("FIX 3: site-footer - use --text-muted instead of rgba white")

# ── FIX 4: Global .btn-dark needs light-theme override ───────────────────────
# btn-dark is currently #1c1917 background with white text globally.
# That's fine EXCEPT when on very dark backgrounds in dark mode.
# But we need to explicitly add light-theme btn-dark to ensure it's always visible.
LT_BTN_DARK = """
/* Global btn-dark light-theme override */
:root.light-theme .btn-dark {
  background: #1c1917;
  color: #ffffff;
}
:root.light-theme .btn-dark:hover {
  background: #292524;
  transform: translateY(-2px);
}
"""

# Add this before the contact-section light-theme specific override
anchor = ":root.light-theme .contact-section .btn-dark {"
if anchor in css and "/* Global btn-dark light-theme override */" not in css:
    css = css.replace(anchor, LT_BTN_DARK + anchor)
    changes.append("FIX 4: Added global :root.light-theme .btn-dark override")

# ── FIX 5: experience section background - use bg-surface not bg-main ─────────
# In dark mode, bg-main = #0c0a09 (pure black), bg-surface = #12100e (very dark)
# Experience section sets background: var(--bg-main) which in LIGHT mode is pure white
# The experience-card inside has no shadow/border making it invisible on white bg.
# Let's ensure the experience section uses bg-surface for a slight differentiation
old_exp_bg = """.experience {
      background: var(--bg-main);
      color: var(--text-light);
    }"""
new_exp_bg = """.experience {
      background: var(--bg-surface);
      color: var(--text-light);
    }"""
if old_exp_bg in css:
    css = css.replace(old_exp_bg, new_exp_bg)
    changes.append("FIX 5: experience section - use bg-surface for slight differentiation")

# ── FIX 6: light-theme .experience uses bg-surface → update to correct light color ──
old_lt_exp = """:root.light-theme .experience {
  background: var(--bg-surface);
  color: var(--text-main);
}"""
new_lt_exp = """:root.light-theme .experience {
  background: #f5f5f4;
  color: var(--text-main);
}"""
if old_lt_exp in css:
    css = css.replace(old_lt_exp, new_lt_exp)
    changes.append("FIX 6: light-theme experience uses #f5f5f4 for visible differentiation from white sections")

# ── FIX 7: modal-info h2, modal-body h4 should use --text-main not --text-light ──
old_modal_h2 = """.modal-info h2 {
font-size: 2rem;
margin-bottom: 0.5rem;
color: var(--text-light);
}"""
new_modal_h2 = """.modal-info h2 {
font-size: 2rem;
margin-bottom: 0.5rem;
color: var(--text-main);
}"""
if old_modal_h2 in css:
    css = css.replace(old_modal_h2, new_modal_h2)
    changes.append("FIX 7: modal-info h2 - use --text-main")

old_modal_h4 = """.modal-body h4 {
color: var(--text-light);"""
new_modal_h4 = """.modal-body h4 {
color: var(--text-main);"""
if old_modal_h4 in css:
    css = css.replace(old_modal_h4, new_modal_h4)
    changes.append("FIX 7b: modal-body h4 - use --text-main")

# ── FIX 8: Add missing light-theme overrides for social links, modal ─────────
EXTRA_OVERRIDES = """
/* Social grid light theme */
:root.light-theme .social-grid a {
  background: #f5f5f4;
  color: var(--text-main);
  border: 1px solid rgba(28, 25, 23, 0.1);
}
:root.light-theme .social-grid a:hover {
  background: #e7e5e4;
}

/* Lang btn light theme */
:root.light-theme .lang-btn {
  color: var(--text-muted);
}
:root.light-theme .lang-btn:hover {
  color: var(--text-main);
}
:root.light-theme .lang-btn.active {
  color: var(--orange);
  font-weight: 800;
}

/* Back to top light theme */
:root.light-theme #backToTop {
  background: #1c1917;
  color: #ffffff;
  border-color: #1c1917;
}

/* Showcase slider light theme extended */
:root.light-theme .showcase-slide-overlay {
  background: linear-gradient(to top, rgba(255,255,255,0.95), transparent);
}
:root.light-theme .showcase-info {
  background: rgba(255, 255, 255, 0.9);
}
:root.light-theme .showcase-slide-title {
  color: var(--text-main);
}
:root.light-theme .showcase-slide-category {
  color: var(--text-muted);
}

/* Skills/about section badges light theme */
:root.light-theme .skills-list span,
:root.light-theme .skill-tag {
  background: rgba(28, 25, 23, 0.06);
  color: var(--text-main);
  border-color: rgba(28, 25, 23, 0.12);
}

/* Section eyebrow in dark sections (experience, contact) */
:root.light-theme .contact-section .eyebrow {
  background: rgba(122, 76, 37, 0.12);
  border-color: rgba(122, 76, 37, 0.2);
  color: var(--brown);
}

/* Portfolio section (bg-soft) section title */
:root.light-theme #portfolio .section-title h2 {
  color: var(--text-main);
}
:root.light-theme #portfolio .section-title p {
  color: var(--text-muted);
}
"""

# Append these overrides at the end
css = css + EXTRA_OVERRIDES
changes.append("FIX 8: Added extra missing light-theme overrides (social, lang-btn, back-to-top, slider, skills)")

# ── Write file ─────────────────────────────────────────────────────────────────
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print(f"\nApplied {len(changes)} fixes:")
for c in changes:
    print(f"  + {c}")

opens = css.count('{')
closes = css.count('}')
print(f"\nBrace balance: {opens} open / {closes} close / net: {opens-closes}")
print(f"Total size: {len(css)} bytes / {len(css.splitlines())} lines")
