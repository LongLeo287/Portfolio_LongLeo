#!/usr/bin/env python3
"""Validate the shared personal-profile contract used by the portfolio and CV."""
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "assets/data/profile.json"
EXPECTED_ORDER = [
    ("SEOSONA", "06/2026", "10/2026"),
    ("Vua2Hand", "03/2025", "05/2026"),
    ("MyGear", "05/2024", "02/2025"),
    ("Vie Production", "11/2023", "05/2024"),
    ("Topskills", "03/2022", "11/2023"),
    ("Thế Giới In Ấn", "10/2018", "08/2020"),
]


def fail(message):
    print(f"FAIL profile: {message}")
    return 1


def main():
    if not PROFILE.exists():
        return fail("assets/data/profile.json is missing")
    try:
        data = json.loads(PROFILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(str(exc))

    required = {
        "identity", "titles", "bio", "contact", "skills", "strengths",
        "specialties", "experience", "education", "brand"
    }
    missing = sorted(required - data.keys())
    if missing:
        return fail(f"missing top-level keys: {', '.join(missing)}")

    identity = data["identity"]
    titles = data["titles"]
    if identity.get("name") != "Hà Đình Long":
        return fail("identity.name must be Hà Đình Long")
    if titles.get("primary") != "VIDEO EDITOR / MOTION GRAPHICS / POST-PRODUCTION":
        return fail("titles.primary is not synchronized with the supplied CV")

    experience = data["experience"]
    actual_order = [(item.get("company"), item.get("start"), item.get("end")) for item in experience]
    if actual_order != EXPECTED_ORDER:
        return fail(f"experience order mismatch: {actual_order!r}")
    seosona = experience[0]
    if seosona.get("role", {}).get("vi") != "Nhân viên Media":
        return fail("SEOSONA role mismatch")
    if len(seosona.get("description", {}).get("vi", [])) < 2:
        return fail("SEOSONA must have the two verified CV bullets")

    required_skills = {"Premiere Pro", "After Effects", "Photoshop", "Illustrator", "CapCut"}
    if not required_skills.issubset(set(data["skills"].get("software", []))):
        return fail("profile is missing one or more CV software skills")

    if len(data["strengths"]) != 3 or any(
        not item.get("title") or not item.get("description") for item in data["strengths"]
    ):
        return fail("profile strengths must contain three titled, described items")
    if len(data["specialties"]) != 3 or any(
        not item.get("title") or not item.get("description") for item in data["specialties"]
    ):
        return fail("profile specialties must contain three titled, described items")
    if not data["education"] or not data["education"][0].get("description"):
        return fail("profile education must include a verified description")

    logo = data["brand"].get("seosonaLogo")
    if not logo or logo.startswith("http") or not (ROOT / logo).exists():
        return fail("brand.seosonaLogo must point to a local asset")

    if "Portfolio_LongLeo" in json.dumps(data, ensure_ascii=False):
        return fail("profile must not expose Portfolio_LongLeo as a visible project")

    print(f"PASS profile: {len(experience)} experience entries, local logo={logo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
