#!/usr/bin/env python3
"""Validate the portfolio's resource, landing and sitemap catalogs.

This is intentionally a read-only consistency check. It does not fetch remote
URLs and it does not rewrite generated pages.
"""
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://portfolio-longleo.vercel.app"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    errors = []
    resource_path = ROOT / "assets/data/resource-links.json"
    try:
        data = json.loads(resource_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL resource catalog: {exc}")
        return 1

    resources = data.get("resources", [])
    required = {"id", "name", "url", "kind", "status", "recommendedUse"}
    ids = [item.get("id") for item in resources]
    urls = [item.get("url") for item in resources]
    for label, values in (("id", ids), ("url", urls)):
        duplicates = sorted({value for value in values if value and values.count(value) > 1})
        if duplicates:
            errors.append(f"resource {label} trùng: {', '.join(duplicates)}")
    for item in resources:
        missing = sorted(required - item.keys())
        if missing:
            errors.append(f"resource {item.get('id', '<unknown>')} thiếu: {', '.join(missing)}")
        if item.get("url", "").startswith("http://"):
            errors.append(f"resource {item.get('id', '<unknown>')} dùng HTTP không an toàn")

    resource_ids = {item.get("id") for item in resources}

    evidence_path = ROOT / "assets/data/project-evidence.json"
    try:
        evidence_data = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL project evidence catalog: {exc}")
        return 1
    evidence_entries = evidence_data.get("entries", [])
    evidence_slugs = [item.get("slug") for item in evidence_entries]
    evidence_required = {
        "slug",
        "architecture",
        "sourceRepo",
        "sourceFiles",
        "documentedClaims",
        "contentLimits",
        "confidence",
    }
    duplicate_evidence = sorted(
        {slug for slug in evidence_slugs if slug and evidence_slugs.count(slug) > 1}
    )
    if duplicate_evidence:
        errors.append(f"project evidence slug duplicate: {', '.join(duplicate_evidence)}")
    for item in evidence_entries:
        missing = sorted(evidence_required - item.keys())
        if missing:
            errors.append(
                f"project evidence {item.get('slug', '<unknown>')} missing: {', '.join(missing)}"
            )
        if not item.get("sourceFiles"):
            errors.append(f"project evidence {item.get('slug', '<unknown>')} missing sourceFiles")
        if not item.get("documentedClaims"):
            errors.append(f"project evidence {item.get('slug', '<unknown>')} missing documentedClaims")
        if not item.get("contentLimits"):
            errors.append(f"project evidence {item.get('slug', '<unknown>')} missing contentLimits")
        for evidence in item.get("derivedEvidence", []):
            missing_derived = sorted({"tool", "repository", "evidenceId", "scope", "limits"} - evidence.keys())
            if missing_derived:
                errors.append(
                    f"project evidence {item.get('slug', '<unknown>')} derived evidence missing: {', '.join(missing_derived)}"
                )
    for required_id in {"aniboxvn-live", "anibox-release-repo"}:
        if required_id not in resource_ids:
            errors.append(f"resource catalog thiếu {required_id}")

    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    lab_cards = re.findall(r'<a\s+class="lab-tile\b', index_html)
    if len(lab_cards) != 8:
        errors.append(f"index.html có {len(lab_cards)} lab cards, expected=8")
    if 'href="https://aniboxvn.vercel.app"' not in index_html:
        errors.append("index.html thiếu external-only AniWeb card")

    build_labs = load_module(ROOT / "scripts/build-labs.py", "build_labs_catalog")
    expected_local = set(build_labs.IN_PORTFOLIO)
    actual_local = {path.stem for path in (ROOT / "labs").glob("*.html")}
    if expected_local != actual_local:
        errors.append(
            "labs/ lệch IN_PORTFOLIO: "
            f"expected={sorted(expected_local)} actual={sorted(actual_local)}"
        )

    stage_landing = load_module(ROOT / "scripts/stage-landing.py", "stage_landing_catalog")
    landing_slugs = {path.name for path in (ROOT / "landing").iterdir() if path.is_dir()}
    publishable = landing_slugs - stage_landing.KHONG_PHAT_HANH
    if publishable != set(stage_landing.TARGETS):
        errors.append(
            "landing/ lệch TARGETS: "
            f"expected={sorted(publishable)} actual={sorted(stage_landing.TARGETS)}"
        )

    qa_path = ROOT / "assets/data/landing-qa.json"
    try:
        qa_data = json.loads(qa_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"landing QA manifest không đọc được: {exc}")
        qa_data = {"entries": []}
    qa_entries = qa_data.get("entries", [])
    qa_by_slug = {item.get("slug"): item for item in qa_entries}
    expected_qa = set(stage_landing.TARGETS) | set(stage_landing.KHONG_PHAT_HANH) | {"anibox"}
    if set(qa_by_slug) != expected_qa:
        errors.append(
            "landing QA manifest lệch inventory: "
            f"expected={sorted(expected_qa)} actual={sorted(qa_by_slug)}"
        )
    qa_required = {
        "slug", "architecture", "domain", "scope", "staticStatus",
        "browserStatus", "liveStatus", "mediaStatus",
    }
    for item in qa_entries:
        missing = sorted(qa_required - item.keys())
        if missing:
            errors.append(f"landing QA {item.get('slug', '<unknown>')} thiếu: {', '.join(missing)}")
        if item.get("staticStatus") == "PASS" and item.get("scope") == "external-only":
            errors.append(f"landing QA {item.get('slug')} external-only không được nhận PASS static")

    # Each publishable child owns its own crawl boundary. The portfolio
    # sitemap intentionally remains limited to this repository's routes.
    child_seo = 0
    for slug, (_, vercel_project) in stage_landing.TARGETS.items():
        child = ROOT / "landing" / slug
        origin = f"https://{vercel_project}.vercel.app/"
        robots = child / "robots.txt"
        child_sitemap = child / "sitemap.xml"
        index = child / "index.html"
        if not robots.exists() or not child_sitemap.exists():
            errors.append(f"{slug} thiếu robots.txt hoặc sitemap.xml")
            continue
        if not index.exists():
            errors.append(f"{slug} thiếu index.html")
            continue
        index_html = index.read_text(encoding="utf-8")
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', index_html)
        if not canonical or canonical.group(1) != origin:
            errors.append(f"{slug} canonical lệch origin: expected={origin}")
        robots_text = robots.read_text(encoding="utf-8")
        if f"Sitemap: {origin}sitemap.xml" not in robots_text:
            errors.append(f"{slug} robots.txt lệch sitemap URL")
        try:
            child_root = ET.fromstring(child_sitemap.read_text(encoding="utf-8"))
            child_locs = [node.text for node in child_root.findall("sm:url/sm:loc", NS)]
        except (OSError, ET.ParseError) as exc:
            errors.append(f"{slug} sitemap.xml không đọc được: {exc}")
            child_locs = []
        if child_locs != [origin]:
            errors.append(f"{slug} sitemap lệch canonical: actual={child_locs}")
        child_seo += 1

    try:
        sitemap = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        locs = [node.text for node in sitemap.findall("sm:url/sm:loc", NS)]
    except (OSError, ET.ParseError) as exc:
        errors.append(f"sitemap.xml không đọc được: {exc}")
        locs = []

    expected_locs = {
        f"{SITE}/",
        f"{SITE}/cv.html",
        *(f"{SITE}/labs/{slug}.html" for slug in sorted(expected_local)),
    }
    if set(locs) != expected_locs:
        errors.append(
            "sitemap lệch các trang phát hành: "
            f"expected={sorted(expected_locs)} actual={sorted(locs)}"
        )

    if errors:
        print("FAIL catalog")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PASS catalog: {len(resources)} resource references")
    print(f"  project evidence entries: {len(evidence_entries)}")
    print(f"  local labs: {', '.join(sorted(actual_local))}")
    print(f"  staged landing repos: {len(stage_landing.TARGETS)}")
    print(f"  child SEO boundaries: {child_seo}")
    print(f"  landing QA manifest entries: {len(qa_entries)}")
    print(f"  sitemap URLs: {len(locs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
