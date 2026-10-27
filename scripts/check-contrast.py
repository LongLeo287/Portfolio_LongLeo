#!/usr/bin/env python3
"""Static WCAG AA spot checks for the staged landing-page palettes.

    python scripts/stage-landing.py --ghi && python scripts/check-contrast.py

This checker reads the HTML/template and extracted resources shipped by the
staged bundle. It does not claim to replace browser/computed-style QA.
"""
import importlib.util
import os
import re
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "build", "repo-landing")
CHECK_PAGES = os.path.join(ROOT, "scripts", "check-pages.py")
spec = importlib.util.spec_from_file_location("check_pages", CHECK_PAGES)
check_pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_pages)

# Each tuple is (foreground, background, nominal text size, description).
# The landing sources currently use literal colors, prefixed custom
# properties, and a JS token table. These explicit pairs follow those current
# source palettes instead of an obsolete shared --text/--bg schema.
PAGES = {
    "OmniClaw": ("OmniClaw", [
        ("#E8FFF2", "#04120C", 15, "primary text on background"),
        ("#9FD8B8", "#04120C", 14, "muted text on background"),
        ("#6FAE8C", "#04120C", 12, "dim text on background"),
        ("#7EE787", "#04120C", 14, "green accent on background"),
        ("#F75C1E", "#04120C", 14, "warning on background"),
    ]),
    "SEOSONA OS": ("SEOSONA-OS", [
        ("#F4EFFF", "#100B1F", 16, "primary text on background"),
        ("#C7BDDF", "#100B1F", 15, "muted text on background"),
        ("#9485B2", "#100B1F", 13, "dim text on background"),
        ("#F5C15F", "#100B1F", 12, "gold accent on background"),
    ]),
    "Video AI": ("SEOSONA-Video-AI", [
        ("#F2E7D5", "#120D08", 16, "primary text on background"),
        ("#C0AB90", "#120D08", 15, "muted text on background"),
        ("#96826A", "#120D08", 12, "dim text on background"),
        ("#F7C455", "#120D08", 14, "gold accent on background"),
        ("#E8734A", "#120D08", 12, "coral accent on background"),
    ]),
    "UX-UI light": ("SEOSONA-UX-UI", [
        ("#0F172A", "#F7F9FC", 16, "primary text on light background"),
        ("#475569", "#F7F9FC", 15, "muted text on light background"),
        ("#5E728E", "#F7F9FC", 12, "dim text on light background"),
        ("#1D4ED8", "#F7F9FC", 14, "accent on light background"),
        ("#FFFFFF", "#1D4ED8", 14, "text on light accent button"),
    ]),
    "Flow": ("seosona-flow", [
        ("#EAF4FF", "#060B14", 16, "primary text on background"),
        ("#9FB6CE", "#060B14", 15, "muted text on background"),
        ("#7591AD", "#060B14", 12, "dim text on background"),
        ("#4FDDF2", "#060B14", 14, "cyan accent on background"),
        ("#2DD4BF", "#060B14", 14, "emerald accent on background"),
    ]),
    "Tiem Nuoc": ("Tiem_Nuoc_Nho_v5", [
        ("#241B17", "#EFE9E1", 16, "primary text on background"),
        ("#5C4A43", "#EFE9E1", 15, "muted text on background"),
        ("#6B554B", "#EFE9E1", 12, "dim text on background"),
        ("#B01F26", "#EFE9E1", 14, "red accent on background"),
        ("#FFF9F2", "#B01F26", 14, "text on red accent button"),
    ]),
    "UX-UI dark": ("SEOSONA-UX-UI", [
        ("#E8EEF7", "#0B1120", 16, "primary text on dark background"),
        ("#A8B6CC", "#0B1120", 15, "muted text on dark background"),
        ("#8496AE", "#0B1120", 12, "dim text on dark background"),
        ("#60A5FA", "#0B1120", 14, "accent on dark background"),
        ("#0B1120", "#60A5FA", 14, "text on dark accent button"),
    ]),
}


def lum(color):
    value = color.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        channel / 12.92 if channel <= 0.03928
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(foreground, background):
    first, second = lum(foreground), lum(background)
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)


def color_present(bundle, color):
    return re.search(re.escape(color), bundle, re.IGNORECASE) is not None


def external_styles(directory):
    """Include CSS files copied beside the bundled landing index."""
    chunks = []
    landing_dir = os.path.dirname(directory)
    for name in os.listdir(landing_dir):
        if not name.lower().endswith(".css"):
            continue
        path = os.path.join(landing_dir, name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as stream:
                chunks.append(stream.read())
    return "\n".join(chunks)


total_fail = 0
total_unknown = 0

for label, (directory, checks) in PAGES.items():
    path = os.path.join(BASE, directory, "landing", "index.html")
    if not os.path.exists(path):
        print(f"=== {label} (not staged; skipped)\n")
        continue

    frame, assets = check_pages.giai_nen(path)
    bundle = frame + "\n" + assets + "\n" + external_styles(path)
    print(f"=== {label}")
    for foreground, background, px, description in checks:
        if not color_present(bundle, foreground) or not color_present(bundle, background):
            print(f"   ?  {foreground} / {background} (color not found in bundle)")
            total_unknown += 1
            continue

        measured = ratio(foreground, background)
        required = 3 if px >= 24 else 4.5
        passed = measured >= required
        if not passed:
            total_fail += 1
        status = "OK " if passed else "FAIL"
        print(
            f"   {status} {measured:5.2f}:1  need {required}  {px}px  "
            f"{foreground} on {background} -- {description}"
        )
    print()

print(f"Total contrast failures: {total_fail}")
print(f"Total pairs not measured: {total_unknown}")
if total_unknown:
    print("NOT VERIFIED: one or more palette colors were not found in the staged bundle.")
raise SystemExit(1 if total_fail else (2 if total_unknown else 0))
