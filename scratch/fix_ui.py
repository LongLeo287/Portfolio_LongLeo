css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# ── FIX 1: Remove duplicate contact-form CSS block at the bottom ──────────────
# The duplicate at lines 2562-2604 conflicts with the original block defined
# inside the indented section (lines 1035-1063). The bottom one overrides
# background:var(--bg-card) which is dark in dark mode but contact-section is cream/light.
duplicate_marker = '\n/* Contact Form UI */\n.contact-form {\n  display: flex;\n  flex-direction: column;\n  gap: 16px;\n}'
if duplicate_marker in css:
    # Remove the entire duplicate block
    start = css.find(duplicate_marker)
    css = css[:start] + '\n'
    print('FIX 1: Removed duplicate contact-form CSS block')
else:
    print('FIX 1: Duplicate block not found (may already be removed)')

# ── FIX 2: Fix btn-dark in light mode (Contact section) ─────────────────────
# In light mode: contact section bg = --cream (#ffd9b5)
# btn-dark = bg: var(--bg-main) → in light mode = #ffffff (WHITE ON PEACH = invisible!)
# Must override to use dark/brown background in light mode
old_btn_dark = """    .btn-dark {
      background: var(--bg-main);
      color: var(--text-light);
    }

    .btn-light {
      border: 1px solid rgba(122,76,37,.18);
      background: rgba(255,255,255,.58);
      color: var(--brown);
    }"""

new_btn_dark = """    .btn-dark {
      background: #1c1917;
      color: #ffffff;
    }

    .btn-light {
      border: 1px solid rgba(122,76,37,.18);
      background: rgba(255,255,255,.58);
      color: var(--brown);
    }

    :root.light-theme .contact-section .btn-dark {
      background: var(--brown);
      color: #ffffff;
    }

    :root.light-theme .contact-section .btn-dark:hover {
      background: #1c1917;
    }

    :root.light-theme .contact-section .btn-light {
      border: 1px solid rgba(122,76,37,.35);
      background: rgba(255,255,255,.8);
      color: var(--brown);
    }"""

if old_btn_dark in css:
    css = css.replace(old_btn_dark, new_btn_dark)
    print('FIX 2: Fixed btn-dark/btn-light for light mode contact section')
else:
    print('FIX 2: btn-dark block not found as expected')

# ── FIX 3: contact-form inputs must be readable in contact-section ────────────
# In light mode: contact section bg = cream, card bg = white
# contact-form inputs: bg: var(--bg-card) → white on cream = ok BUT border is too faint
# Also fix placeholder color for cream bg context
old_contact_form_inputs = """    .contact-form input,
    .contact-form textarea {
      width: 100%;
      border: 1px solid rgba(122,76,37,.12);
      border-radius: 18px;
      background: var(--bg-card);
      color: var(--text-main);
      padding: 14px 16px;
      outline: none;
      font: inherit;
      transition: .2s ease;
    }"""

new_contact_form_inputs = """    .contact-form input,
    .contact-form textarea {
      width: 100%;
      border: 1px solid rgba(122,76,37,.25);
      border-radius: 18px;
      background: rgba(255,255,255,0.75);
      color: #1c1917;
      padding: 14px 16px;
      outline: none;
      font: inherit;
      transition: .2s ease;
    }

    .contact-form input::placeholder,
    .contact-form textarea::placeholder {
      color: rgba(122, 76, 37, 0.55);
    }"""

if old_contact_form_inputs in css:
    css = css.replace(old_contact_form_inputs, new_contact_form_inputs)
    print('FIX 3: Fixed contact form inputs')
else:
    print('FIX 3: Contact form input block not found exactly')

# ── FIX 4: partners-section light-theme override ──────────────────────────────
# In dark mode: var(--bg-card) = #181513 (very dark) - correct
# In light mode: var(--bg-card) = #ffffff (white) - correct
# But we need to confirm the light-theme footer override also exists
# Add explicit light-theme override for better control
partners_fix = """
:root.light-theme .partners-section {
  background: #f5f5f4;
  border-top: 1px solid #e7e5e4;
  border-bottom: 1px solid #e7e5e4;
}

:root.light-theme .partners-title {
  color: rgba(28, 25, 23, 0.4);
}
"""

# Insert before the mobile header controls comment
insert_marker = '/* Mobile Header Controls */'
if insert_marker in css:
    css = css.replace(insert_marker, partners_fix + insert_marker)
    print('FIX 4: Added partners-section light-theme override')
else:
    css += partners_fix
    print('FIX 4: Appended partners-section light-theme override')

# ── FIX 5: contact-card in light mode (form card contrast) ───────────────────
old_contact_card = """    .contact-card {
      border: 1px solid rgba(122,76,37,.1);
      border-radius: 42px;
      background: rgba(255,255,255,.65);
      padding: 28px;
      box-shadow: 0 28px 80px rgba(185,133,83,.22);
      backdrop-filter: blur(16px);
    }"""

new_contact_card = """    .contact-card {
      border: 1px solid rgba(122,76,37,.18);
      border-radius: 42px;
      background: rgba(255,255,255,.8);
      padding: 28px;
      box-shadow: 0 28px 80px rgba(185,133,83,.22);
      backdrop-filter: blur(16px);
    }

    :root:not(.light-theme) .contact-card {
      border: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(30, 25, 20, 0.8);
    }

    :root:not(.light-theme) .contact-form input,
    :root:not(.light-theme) .contact-form textarea {
      background: rgba(255,255,255,0.06);
      color: var(--cream);
      border-color: rgba(252, 211, 77, 0.15);
    }

    :root:not(.light-theme) .contact-form input::placeholder,
    :root:not(.light-theme) .contact-form textarea::placeholder {
      color: rgba(255, 217, 181, 0.45);
    }"""

if old_contact_card in css:
    css = css.replace(old_contact_card, new_contact_card)
    print('FIX 5: Fixed contact-card for dark mode')
else:
    print('FIX 5: Contact card block not found exactly')

# ── FIX 6: Eyebrow pill contrast in light mode ───────────────────────────────
# The eyebrow (section labels) currently use amber bg with dark-amber text
# In light mode the amber bg is fine, but let's ensure text contrast
old_eyebrow = """    .eyebrow {
      display: inline-flex;
      margin-bottom: 16px;
      border-radius: 999px;
      background: rgba(252,211,77,.18);
      color: #a16207;
      padding: 5px 15px;
      font-size: 14px;
      font-weight: 850;
    }"""

new_eyebrow = """    .eyebrow {
      display: inline-flex;
      margin-bottom: 16px;
      border-radius: 999px;
      background: rgba(252,211,77,.2);
      color: #92400e;
      padding: 5px 15px;
      font-size: 14px;
      font-weight: 850;
      border: 1px solid rgba(252,211,77,.3);
    }

    :root:not(.light-theme) .eyebrow {
      background: rgba(252,211,77,.15);
      color: var(--amber);
      border-color: rgba(252,211,77,.2);
    }"""

if old_eyebrow in css:
    css = css.replace(old_eyebrow, new_eyebrow)
    print('FIX 6: Fixed eyebrow contrast for both modes')
else:
    print('FIX 6: Eyebrow block not found exactly')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print('\nAll fixes applied. Checking brace balance...')
opens = css.count('{')
closes = css.count('}')
print(f'Braces: {opens} open / {closes} close / balance: {opens - closes}')
