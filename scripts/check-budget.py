#!/usr/bin/env python3
"""Check the homepage's raw and gzip asset budgets without a build step."""
import gzip
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUDGETS = {
    "initial-css": (
        ["assets/css/tokens.css", "assets/css/styles.css", "assets/css/animations.css"],
        120 * 1024,
        30 * 1024,
    ),
    "initial-js": (
        ["assets/js/afr.js", "assets/js/app.js", "assets/js/main.js", "assets/js/animations.js"],
        110 * 1024,
        32 * 1024,
    ),
    "lazy-lenis": (["assets/js/vendor/lenis-1.1.13.min.js"], 14 * 1024, 4 * 1024),
}


def measure(files):
    data = b"\n".join((ROOT / path).read_bytes() for path in files)
    return len(data), len(gzip.compress(data, compresslevel=9))


def main():
    failed = False
    for label, (files, raw_limit, gzip_limit) in BUDGETS.items():
        raw, packed = measure(files)
        ok = raw <= raw_limit and packed <= gzip_limit
        failed |= not ok
        status = "PASS" if ok else "FAIL"
        print(
            f"{status} {label}: raw={raw / 1024:.1f} KB / {raw_limit / 1024:.0f} KB, "
            f"gzip={packed / 1024:.1f} KB / {gzip_limit / 1024:.0f} KB"
        )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
