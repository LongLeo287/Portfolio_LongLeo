#!/usr/bin/env python3
"""Validate the work-first homepage structure and project ordering."""
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"


def main():
    source = HTML.read_text(encoding="utf-8")
    errors = []
    for marker in ("data-editorial-hero", "data-editorial-selected-work", "data-editorial-capabilities", "data-editorial-experience", "data-editorial-projects"):
        if marker not in source:
            errors.append(f"missing {marker}")
    selected = source.find('data-editorial-selected-work')
    seosona = source.find('href="https://seosona.vercel.app/"', selected)
    aniweb = source.find('href="https://aniboxvn.vercel.app"', selected)
    if selected < 0 or seosona < 0 or aniweb < 0 or seosona > aniweb:
        errors.append("selected work must order AniWeb/SEOSONA before AniWeb")
    if "Portfolio_LongLeo" in source:
        errors.append("homepage must not expose Portfolio_LongLeo")
    if re.search(r"health|live build|endpoint", source, re.IGNORECASE):
        errors.append("homepage contains a health/status rail")
    if 'data-lab-collapsible="true" hidden' not in source and 'hidden data-lab-collapsible="true"' not in source:
        errors.append("collapsible project cards need a static hidden fallback")
    if 'data-labs-expand' not in source or 'aria-controls="labsGrid"' not in source:
        errors.append("project expansion control is missing")
    if errors:
        print("FAIL homepage contract")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS homepage contract: editorial sections, project order and static expansion fallback")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
