css_path = 'assets/css/styles.css'

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()
    lines = css.splitlines()

print("=" * 60)
print("FULL CSS AUDIT REPORT")
print("=" * 60)

# ── 1. Root CSS variables ────────────────────────────────────────
print("\n── 1. CSS VARIABLE DEFINITIONS ──")
in_root = False
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith(':root {') or stripped.startswith(':root.light-theme {'):
        in_root = True
        print(f"\n  L{i}: {stripped}")
        continue
    if in_root:
        if stripped == '}':
            in_root = False
            print(f"  L{i}: }}")
        elif '--' in stripped:
            print(f"  L{i}: {stripped}")

# ── 2. Light-theme overrides coverage ───────────────────────────
print("\n── 2. LIGHT-THEME OVERRIDES COVERAGE ──")
key_selectors = [
    '.experience', '.experience-card', '.experience-title-area h3',
    '.experience-role', '.experience-body p', '.link-line',
    '.filter-btn', '.filter-btn.active',
    '.service-card', '.service-icon',
    '.portfolio-card',
    '.tool-item',
    '.section-title h2', '.section-title p',
    '.site-footer',
    '.contact-section', '.btn-dark',
    '.about', '.partners-section',
    '.hero', '.stat-card',
    '.bg-soft', '.bg-white',
]
covered = []
missing = []
for sel in key_selectors:
    lt_sel = f':root.light-theme {sel}'
    if lt_sel in css:
        covered.append(sel)
    else:
        missing.append(sel)

print(f"\n  COVERED ({len(covered)}):")
for s in covered:
    print(f"    ✅ {s}")
print(f"\n  MISSING light-theme override ({len(missing)}):")
for s in missing:
    print(f"    ❌ {s}")

# ── 3. Hardcoded white text colors ──────────────────────────────
print("\n── 3. HARDCODED WHITE TEXT COLORS (may break in light mode) ──")
problem_lines = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if 'light-theme' in stripped:
        continue
    if ('color:' in stripped or 'color :' in stripped):
        if ('rgba(255,255,255' in stripped or 'rgba(255, 255, 255' in stripped):
            # Only flag if opacity < 0.5 means actually white text
            problem_lines.append((i, stripped))
        elif 'var(--text-light)' in stripped and i < 2300:
            problem_lines.append((i, stripped))

print(f"  Found {len(problem_lines)} potentially problematic lines:")
for lineno, content in problem_lines:
    print(f"    L{lineno}: {content}")

# ── 4. Sections using experience dark background ────────────────
print("\n── 4. SECTION BACKGROUNDS (dark hardcoded) ──")
dark_hardcoded = ['#0c0a09', '#12100e', '#181513', '#18110b', '#1c1917', '#292524']
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if any(color in stripped for color in dark_hardcoded):
        if 'background' in stripped and 'light-theme' not in lines[max(0,i-3):i+1]:
            print(f"  L{i}: {stripped}")

# ── 5. Check for duplicate CSS rules ────────────────────────────
print("\n── 5. IMPORTANT SELECTORS WITH DUPLICATE DEFINITIONS ──")
import re
selector_counts = {}
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if re.match(r'^[.#][\w-]+\s*\{', stripped) or re.match(r'^:root[\.\s]', stripped):
        sel = stripped.split('{')[0].strip()
        if sel not in selector_counts:
            selector_counts[sel] = []
        selector_counts[sel].append(i)

dups = {k: v for k, v in selector_counts.items() if len(v) > 1}
for sel, occurrences in sorted(dups.items()):
    if not any(x in sel for x in ['@', 'keyframe', 'media', 'hover', 'focus', 'active', 'before', 'after', 'not']):
        print(f"  {sel}: lines {occurrences}")

print("\n── AUDIT COMPLETE ──")
