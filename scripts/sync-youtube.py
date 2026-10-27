#!/usr/bin/env python3
"""Sync the selected public YouTube playlist into the static portfolio.

The portfolio uses a curated playlist instead of the whole channel. A sync
refreshes the title, upload date and thumbnail for playlist videos, adds new
playlist entries, and removes old Video cards that are no longer in the
playlist. The browser sorts the resulting Video tab by upload date.

The playlist and watch pages are public, so this workflow does not require an
API key. It is intentionally manual: run it from GitHub Actions or locally
when the playlist changes, then review and deploy the generated catalog.
"""

import argparse
import html
import io
import json
import os
import re
import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError

from PIL import Image


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYLIST_ID = os.environ.get("YOUTUBE_PLAYLIST_ID", "PLhc6e124Y3Jw4qQYPAkfWcuIO-C3BsuG9")
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"
PROJECTS = "assets/data/projects.json"
THUMBS = "assets/img/thumbnails"
APP_JS = "assets/js/app.js"
UA = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (compatible; PortfolioLongLeoSync/2.0)",
}
RETRYABLE_HTTP_STATUS = {408, 429, 500, 502, 503, 504}
FETCH_ATTEMPTS = 4
THUMB_QUALITIES = ("maxresdefault", "sddefault", "hqdefault")
WIDTHS = (480, 960)


def fetch(url, timeout=30, attempts=FETCH_ATTEMPTS):
    """Fetch a public YouTube resource with bounded transient retries."""
    last_error = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(request, timeout=timeout).read()
        except HTTPError as error:
            last_error = error
            retry_after = error.headers.get("Retry-After")
            if error.code not in RETRYABLE_HTTP_STATUS or attempt == attempts - 1:
                raise
            try:
                delay = max(1, min(30, int(retry_after))) if retry_after else 2**attempt
            except ValueError:
                delay = 2**attempt
            print(
                f"  ! YouTube HTTP {error.code}; retry {attempt + 1}/{attempts} in {delay}s",
                file=sys.stderr,
            )
        except (OSError, URLError, TimeoutError) as error:
            last_error = error
            if attempt == attempts - 1:
                raise
            delay = min(30, 2**attempt)
            print(
                f"  ! YouTube network error ({error}); retry {attempt + 1}/{attempts} in {delay}s",
                file=sys.stderr,
            )
        time.sleep(delay)
    raise last_error


def configure_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def extract_assignment_json(source, variable):
    """Extract one balanced JSON object from a YouTube JS assignment."""
    marker = f"var {variable} = "
    start = source.find(marker)
    if start < 0:
        raise RuntimeError(f"Không tìm thấy {variable} trong trang YouTube")
    start += len(marker)
    while start < len(source) and source[start].isspace():
        start += 1
    if start >= len(source) or source[start] != "{":
        raise RuntimeError(f"{variable} không bắt đầu bằng JSON object")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(source[start : index + 1])
    raise RuntimeError(f"Không thể kết thúc JSON {variable}")


def walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def lockup_title(node):
    metadata = node.get("metadata", {})
    lockup = metadata.get("lockupMetadataViewModel", {})
    title = lockup.get("title", {})
    return title.get("content", "")


def lockup_watch_endpoint(node):
    command = node.get("rendererContext", {}).get("commandContext", {})
    on_tap = command.get("onTap", {}).get("innertubeCommand", {})
    return on_tap.get("watchEndpoint", {})


def playlist_videos():
    """Read all currently rendered public videos from the chosen playlist."""
    page = fetch(PLAYLIST_URL, timeout=45).decode("utf-8", "replace")
    data = extract_assignment_json(page, "ytInitialData")
    found = {}
    for node in walk_dicts(data):
        if node.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO":
            continue
        video_id = node.get("contentId")
        endpoint = lockup_watch_endpoint(node)
        if not video_id or endpoint.get("playlistId") != PLAYLIST_ID:
            continue
        found[video_id] = {
            "id": video_id,
            "title": html.unescape(lockup_title(node)).strip(),
        }
    if not found:
        raise RuntimeError(
            f"Không đọc được video từ playlist {PLAYLIST_ID}; playlist có thể private hoặc YouTube đổi cấu trúc"
        )
    return list(found.values())


def video_page_metadata(video_id, fallback_title):
    """Read exact title and ISO upload date from a public watch page."""
    page = fetch(
        f"https://www.youtube.com/watch?v={video_id}", timeout=45
    ).decode("utf-8", "replace")
    title_match = re.search(
        r'<meta[^>]+itemprop=["\']name["\'][^>]+content=["\']([^"\']+)',
        page,
        re.I,
    )
    date_match = re.search(
        r'<meta[^>]+itemprop=["\'](?:datePublished|uploadDate)["\'][^>]+content=["\']([^"\']+)',
        page,
        re.I,
    )
    title = html.unescape(title_match.group(1)).strip() if title_match else fallback_title
    published_at = date_match.group(1).strip() if date_match else ""
    return {"id": video_id, "title": title, "publishedAt": published_at}


def youtube_id_from_href(value):
    if not isinstance(value, str):
        return None
    match = re.search(r"[?&]v=([\w-]{11})", value)
    if match:
        return match.group(1)
    match = re.search(r"youtu\.be/([\w-]{11})", value)
    return match.group(1) if match else None


def download_thumb(video_id, destination):
    for quality in THUMB_QUALITIES:
        try:
            data = fetch(
                f"https://img.youtube.com/vi/{video_id}/{quality}.jpg", timeout=25
            )
        except Exception:
            continue
        if len(data) < 2000:
            continue
        changed = True
        try:
            with open(destination, "rb") as handle:
                changed = handle.read() != data
        except FileNotFoundError:
            pass
        if changed:
            with open(destination, "wb") as handle:
                handle.write(data)
        return quality, changed
    return None, False


def make_derivatives(source):
    with Image.open(source) as image:
        image = image.convert("RGB")
        source_width, source_height = image.size
        stem, _ = os.path.splitext(source)
        for width in WIDTHS:
            output = f"{stem}-{width}.webp"
            resized = (
                image.copy()
                if width >= source_width
                else image.resize(
                    (width, round(source_height * width / source_width)), Image.LANCZOS
                )
            )
            resized.save(output, "WEBP", quality=80, method=5)


def next_id(projects):
    numbers = [
        int(match.group(1))
        for project in projects
        if (match := re.match(r"proj_(\d+)$", project.get("id", "")))
    ]
    return f"proj_{max(numbers) + 1:03d}" if numbers else "proj_001"


def build_entry(project_id, metadata, featured=False):
    video_id = metadata["id"]
    title = metadata["title"]
    return {
        "id": project_id,
        "title": {"vi": title, "en": title},
        "category": "Video",
        "client": {"vi": "YouTube @LongLeo287", "en": "YouTube @LongLeo287"},
        "imgSrc": f"{THUMBS}/{video_id}.jpg",
        "href": f"https://www.youtube.com/watch?v={video_id}",
        "alt": title,
        "publishedAt": metadata["publishedAt"],
        "sourcePlaylist": PLAYLIST_ID,
        "isFeatured": featured,
        "caseStudy": {
            "role": {"vi": "Video Editor / Cameraman", "en": "Video Editor / Cameraman"},
            "concept": {"vi": "", "en": ""},
            "challenge": {"vi": "", "en": ""},
            "solution": {"vi": "", "en": ""},
            "tools": ["Premiere Pro", "After Effects"],
        },
    }


def bump_cache_param():
    path = os.path.join(ROOT, APP_JS)
    source = io.open(path, encoding="utf-8").read()
    match = re.search(r"assets/data/projects\.json\?v=([\d.]+)", source)
    if not match:
        print("  ! Không tìm thấy tham số cache của projects.json trong app.js")
        return None
    old = match.group(1)
    parts = old.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    new = ".".join(parts)
    io.open(path, "w", encoding="utf-8").write(
        source.replace(
            f"assets/data/projects.json?v={old}",
            f"assets/data/projects.json?v={new}",
        )
    )
    return f"{old} → {new}"


def update_title(project, remote_title):
    title = project.get("title")
    if isinstance(title, dict):
        old_vi = title.get("vi", "")
        old_en = title.get("en", "")
        changed = old_vi != remote_title
        title["vi"] = remote_title
        if not old_en or old_en == old_vi:
            changed = changed or old_en != remote_title
            title["en"] = remote_title
    else:
        changed = title != remote_title
        project["title"] = {"vi": remote_title, "en": remote_title}
    if project.get("alt") != remote_title:
        project["alt"] = remote_title
        changed = True
    return changed


def refresh_thumbnail(project, video_id):
    image_source = project.get("imgSrc", "")
    if not image_source.startswith(f"{THUMBS}/") or not image_source.endswith(".jpg"):
        return False
    destination = os.path.join(ROOT, image_source)
    quality, source_changed = download_thumb(video_id, destination)
    if not quality:
        print(f"  ! {video_id}: không tải được thumbnail")
        return False
    derivatives_missing = any(
        not os.path.exists(f"{os.path.splitext(destination)[0]}-{width}.webp")
        for width in WIDTHS
    )
    if source_changed or derivatives_missing:
        make_derivatives(destination)
        return True
    return False


def main():
    configure_stdio()
    parser = argparse.ArgumentParser(description="Sync the selected YouTube playlist")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="authoritatively sync the playlist and write the catalog",
    )
    parser.add_argument(
        "--add",
        action="store_true",
        help="compatibility alias for --sync",
    )
    args = parser.parse_args()
    if args.add and args.sync:
        raise SystemExit("Dùng --sync hoặc --add, không dùng đồng thời")
    write_changes = args.sync or args.add

    os.chdir(ROOT)
    projects = json.load(io.open(PROJECTS, encoding="utf-8"))
    print(f"Playlist: {PLAYLIST_URL}")
    candidates = playlist_videos()
    print(f"Playlist trả về {len(candidates)} video")

    metadata = []
    for index, candidate in enumerate(candidates, start=1):
        try:
            item = video_page_metadata(candidate["id"], candidate["title"])
        except Exception as error:
            print(f"  ! {candidate['id']}: không đọc được ngày upload ({error})")
            item = {
                "id": candidate["id"],
                "title": candidate["title"],
                "publishedAt": "",
            }
        metadata.append(item)
        print(
            f"  [{index}/{len(candidates)}] {item['publishedAt'] or 'unknown'} "
            f"{item['title'][:72]}"
        )

    playlist_ids = {item["id"] for item in metadata}
    projects_by_video = {
        youtube_id_from_href(project.get("href")): project
        for project in projects
        if project.get("category") == "Video" and youtube_id_from_href(project.get("href"))
    }

    removed = [
        project
        for project in projects
        if project.get("category") == "Video"
        and youtube_id_from_href(project.get("href")) not in playlist_ids
    ]
    if not write_changes:
        print(f"Dry run: {len(removed)} video ngoài playlist sẽ bị loại khi chạy --sync")
        return 0

    changed = bool(removed)
    if removed:
        projects = [project for project in projects if project not in removed]

    added = 0
    title_updates = 0
    date_updates = 0
    thumb_updates = 0
    for item in metadata:
        project = projects_by_video.get(item["id"])
        if project is None:
            destination = os.path.join(THUMBS, f"{item['id']}.jpg")
            quality, _ = download_thumb(item["id"], destination)
            if not quality:
                print(f"  ! {item['id']}: bỏ qua vì không tải được thumbnail")
                continue
            make_derivatives(destination)
            project = build_entry(next_id(projects), item)
            projects.append(project)
            projects_by_video[item["id"]] = project
            added += 1
            changed = True
        if update_title(project, item["title"]):
            title_updates += 1
            changed = True
        if project.get("publishedAt") != item["publishedAt"]:
            project["publishedAt"] = item["publishedAt"]
            date_updates += 1
            changed = True
        if project.get("sourcePlaylist") != PLAYLIST_ID:
            project["sourcePlaylist"] = PLAYLIST_ID
            changed = True
        if refresh_thumbnail(project, item["id"]):
            thumb_updates += 1
            changed = True

    if not changed:
        print("Không có thay đổi. Xong.")
        return 0

    with io.open(PROJECTS, "w", encoding="utf-8") as handle:
        json.dump(projects, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(
        f"Đã đồng bộ: thêm {added}, xóa {len(removed)}, title {title_updates}, "
        f"ngày upload {date_updates}, thumbnail {thumb_updates}"
    )
    bumped = bump_cache_param()
    if bumped:
        print(f"Đã bump cache app.js: {bumped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
