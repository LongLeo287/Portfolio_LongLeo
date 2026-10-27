#!/usr/bin/env python3
"""Validate the landing-page architecture catalog against the portfolio cards."""
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "assets/data/landing-architectures.json"
RESOURCE_PATH = ROOT / "assets/data/resource-links.json"
FIXTURE_PATH = ROOT / "assets/data/landing-fixtures.json"
INDEX_PATH = ROOT / "index.html"
KNOWN_EXTERNAL_EXAMPLES = {"anibox"}
REQUIRED_ARCHITECTURES = {
    "product-mockup",
    "workflow-canvas",
    "data-dashboard",
    "media-timeline",
    "spatial-3d",
    "live-runtime",
    "design-workbench",
    "editorial-narrative",
    "motion-narrative",
    "tv-interface",
}


def validate():
    errors = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        resources = json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))
        fixtures = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        index_html = INDEX_PATH.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"file read/parse error: {exc}"]

    architectures = catalog.get("architectures", [])
    by_id = {item.get("id"): item for item in architectures}
    fixture_ids = set(fixtures.get("fixtures", {}))
    if len(by_id) != len(architectures):
        errors.append("architecture id trùng")

    missing = sorted(REQUIRED_ARCHITECTURES - set(by_id))
    if missing:
        errors.append(f"catalog thiếu architecture: {', '.join(missing)}")
    fixture_missing = sorted(set(by_id) - fixture_ids)
    fixture_unknown = sorted(fixture_ids - set(by_id))
    if fixture_missing:
        errors.append(f"fixture thiếu architecture: {', '.join(fixture_missing)}")
    if fixture_unknown:
        errors.append(f"fixture có architecture không tồn tại: {', '.join(fixture_unknown)}")

    resource_ids = {item.get("id") for item in resources.get("resources", [])}
    for item in architectures:
        architecture_id = item.get("id", "<unknown>")
        required = {"id", "label", "visualSurface", "bestFor", "composition",
                    "dataContract", "assetPolicy", "motion", "resourceIds",
                    "budget", "examples"}
        missing_fields = sorted(required - item.keys())
        if missing_fields:
            errors.append(f"{architecture_id} thiếu: {', '.join(missing_fields)}")
        for resource_id in item.get("resourceIds", []):
            if resource_id not in resource_ids:
                errors.append(f"{architecture_id} tham chiếu resource không tồn tại: {resource_id}")
        budget = item.get("budget", {})
        for budget_key in ("initialCssKbGzip", "initialJsKbGzip", "mediaRequests"):
            if not isinstance(budget.get(budget_key), (int, float)):
                errors.append(f"{architecture_id} thiếu budget số: {budget_key}")

        for example in item.get("examples", []):
            if not (ROOT / "landing" / example).is_dir() and example not in KNOWN_EXTERNAL_EXAMPLES:
                errors.append(f"{architecture_id} có example không tồn tại: {example}")

    card_ids = re.findall(r'data-lab-architecture="([^"]+)"', index_html)
    if len(card_ids) != 8:
        errors.append(f"index.html có {len(card_ids)} architecture card, expected=8")
    if len(set(card_ids)) != len(card_ids):
        errors.append("index.html có architecture card trùng")
    unknown_cards = sorted(set(card_ids) - set(by_id))
    if unknown_cards:
        errors.append(f"index.html tham chiếu architecture không có trong catalog: {', '.join(unknown_cards)}")

    return errors


def main():
    errors = validate()
    if errors:
        print("FAIL landing architectures")
        for error in errors:
            print(f"  - {error}")
        return 1

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    print(f"PASS landing architectures: {len(catalog['architectures'])} recipes, 9 mapped cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
