import re

css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_root = """:root {
  /* Layout & Brand */
  --radius-lg: 36px;
  --radius-md: 24px;
  --max: 1200px;
  --amber: #fcd34d;
  --amber-2: #f59e0b;
  --orange: #f97316;
  --cream: #ffd9b5;
  --brown: #7a4c25;
  --shadow-glow: 0 20px 40px rgba(245, 158, 11, 0.16);

  /* DARK THEME (Default) */
  --bg-main: #0c0a09;
  --bg-surface: #12100e;
  --bg-card: #181513;
  --text-main: #fafaf9;
  --text-muted: #a8a29e;
  --text-light: #ffffff;
  --line: rgba(255, 255, 255, 0.1);
  --shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

:root.light-theme {
  /* LIGHT THEME */
  --bg-main: #ffffff;
  --bg-surface: #fafaf9;
  --bg-card: #ffffff;
  --text-main: #1c1917;
  --text-muted: #6b625d;
  --text-light: #ffffff;
  --line: #e7e5e4;
  --shadow: 0 4px 6px -1px rgba(28, 25, 23, 0.05), 0 10px 15px -3px rgba(28, 25, 23, 0.08), 0 20px 25px -5px rgba(28, 25, 23, 0.12), 0 30px 50px -10px rgba(28, 25, 23, 0.15);
}
"""

css = re.sub(r':root\s*\{.*?\-\-max:\s*1200px;[ \n\r\t]*\}', new_root, css, flags=re.DOTALL)

# Remove Phase 2 declarations at bottom
css = re.sub(r':root\s*\{\s*/\* Dynamic Theme Variables.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r':root\.light-theme\s*\{\s*--body-bg:.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'/\* Apply Theme variables dynamically to override light components \*/.*?(?=/\* Header & Navigation theme switcher support \*/)', '', css, flags=re.DOTALL)

css = css.replace('!important', '')

css = css.replace('var(--white)', 'var(--bg-card)')
css = css.replace('color: var(--bg-card)', 'color: var(--text-light)')

css = css.replace('var(--bg-dark)', 'var(--bg-main)')
css = css.replace('var(--text-dark)', 'var(--text-main)')
css = css.replace('var(--bg-soft)', 'var(--bg-surface)')

css = css.replace('.bg-white {\n      background: var(--bg-card);\n    }', '.bg-white {\n      background: var(--bg-card);\n    }\n    .bg-white_old {')

contact_css_old = """    .contact-section {
      background: var(--cream);
      color: var(--brown);
      padding: 96px 0;
    }"""
contact_css_new = """    .contact-section {
      background: #18110b;
      color: var(--cream);
      padding: 96px 0;
      border-top: 1px solid rgba(252, 211, 77, 0.1);
      transition: background-color 0.4s ease, color 0.4s ease;
    }
    
    :root.light-theme .contact-section {
      background: var(--cream);
      color: var(--brown);
      border-top: none;
    }"""
css = css.replace(contact_css_old, contact_css_new)

mobile_layout_css = """
/* Mobile Header Controls */
.header-controls {
  display: flex;
  align-items: center;
}

.desktop-lang {
  display: flex;
}

.mobile-lang-row {
  display: none;
}

@media (max-width: 1024px) {
  .desktop-lang {
    display: none;
  }
  .mobile-lang-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid var(--line);
  }
  .mobile-nav {
    padding: 24px 0;
  }
}
"""
css += mobile_layout_css

# fix loader
css = css.replace('background: #0c0a09;', 'background: var(--bg-main);')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Done.")
