#!/usr/bin/env python3
"""Validate the default-on adaptive motion contract without running a browser."""
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    afr = (ROOT / "assets/js/afr.js").read_text(encoding="utf-8")
    motion = (ROOT / "assets/js/animations.js").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/animations.css").read_text(encoding="utf-8") + (ROOT / "assets/css/styles.css").read_text(encoding="utf-8")
    errors = []
    stage_files = sorted((ROOT / "landing").glob("*/webgl-stage.js"))
    for mode in ("full", "balanced", "lite", "static"):
        if mode not in afr:
            errors.append(f"AFR mode missing: {mode}")
    if "prefers-reduced-motion" not in afr or "saveData" not in afr:
        errors.append("AFR hard constraints are incomplete")
    if "portfolioMotion" not in motion or "portfolioAFR" not in motion:
        errors.append("shared motion/AFR interface is missing")
    if "data-afr-heavy" not in html or "data-afr-loop" not in html:
        errors.append("HTML has no opt-in heavy/loop motion surfaces")
    if "data-depth" not in html:
        errors.append("editorial stage has no progressive depth hook")
    if "html[data-afr=\"static\"]" not in css:
        errors.append("static AFR CSS fallback is missing")
    if "@media (prefers-reduced-motion: reduce)" not in css:
        errors.append("reduced-motion CSS fallback is missing")
    if re.search(r">\s*(Motion|Full|Soft|Off)\s*<", html, re.IGNORECASE):
        errors.append("visible motion mode control remains")
    for stage_path in stage_files:
        stage = stage_path.read_text(encoding="utf-8")
        missing = [
            marker for marker in (
                "saveDataEnabled", "getQualityMode", "prefersReducedMotion",
                "visibilitychange", "IntersectionObserver", "dispose()",
                "static", "balanced", "lite", "full",
            ) if marker not in stage
        ]
        if missing:
            errors.append(f"{stage_path.parent.name} WebGL contract missing: {', '.join(missing)}")
    if errors:
        print("FAIL motion contract")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS motion contract: homepage AFR + {len(stage_files)} WebGL quality/fallback stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
