#!/usr/bin/env python3
"""Check the public homepage/CV SEO and factual content contract."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.h1 = []
        self.meta = {}
        self.canonical = None
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1.append([])
            self._in_h1 = True
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key and attrs.get("content") is not None:
                self.meta[key] = attrs["content"]
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_title:
            self.title.append(data)
        if self._in_h1:
            self.h1[-1].append(data)


def inspect(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main():
    errors = []
    homepage = inspect(ROOT / "index.html")
    cv = inspect(ROOT / "cv.html")

    title = "".join(homepage.title).strip()
    description = homepage.meta.get("description", "")
    h1 = " ".join(" ".join(value) for value in homepage.h1).split()
    h1 = " ".join(h1)
    if "Video Editor" not in title or "Motion Graphics" not in title:
        errors.append("homepage title must target Video Editor and Motion Graphics")
    if not 120 <= len(description) <= 165:
        errors.append(f"homepage meta description length is {len(description)}, expected 120-165")
    if len(homepage.h1) != 1 or "Video Editor" not in h1:
        errors.append("homepage must expose exactly one H1 containing Video Editor")
    if homepage.canonical != "https://portfolio-longleo.vercel.app/":
        errors.append("homepage canonical is incorrect")
    for key in ("og:title", "og:description", "og:image", "og:url"):
        if key not in homepage.meta:
            errors.append(f"homepage missing {key}")

    source = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "assets/js/app.js").read_text(encoding="utf-8")
    for stale in ("Hơn 5 năm", "hơn 5 năm", "5+ years", "5+ năm", "bắt đầu hành trình sáng tạo từ năm 2019"):
        if stale in source or stale in app:
            errors.append(f"stale factual copy remains: {stale}")

    if "hơn 6 năm" not in source or "more than 6" not in app:
        errors.append("public experience copy must use the approved verified-six-year wording")
    if "Arena Multimedia" not in source or "năm 2015" not in source or "năm 2018" not in source:
        errors.append("homepage education/work timeline is incomplete")
    if "Video Editor / Motion Graphics / Post-Production" not in source:
        errors.append("homepage does not expose the primary service phrase")

    cv_title = "".join(cv.title).strip()
    cv_description = cv.meta.get("description", "")
    if "Video Editor" not in cv_title or "Motion Graphics" not in cv_title:
        errors.append("CV title must target Video Editor and Motion Graphics")
    if not 100 <= len(cv_description) <= 165:
        errors.append(f"CV meta description length is {len(cv_description)}, expected 100-165")
    if not (ROOT / "robots.txt").exists() or not (ROOT / "sitemap.xml").exists():
        errors.append("robots.txt and sitemap.xml are required")

    if errors:
        print("FAIL SEO/content contract")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS SEO/content contract: title, H1, metadata and factual timeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
