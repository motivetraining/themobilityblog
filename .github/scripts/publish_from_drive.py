#!/usr/bin/env python3
"""
Publish from Drive.

Scans a Drive queue folder for matched .md + image pairs (same base name,
image is .jpg/.jpeg/.png/.webp), validates the markdown frontmatter against
the site's content schema (src/content.config.ts), places the post and its
image in the repo, commits, and moves the source files in Drive to a
processed/ folder. Validation failures leave files in place and fail the
run so it is never silently missed.

Unlike motive-training's publisher, every post here is filed with its photo
already attached -- there is no "photo to follow later" state. A .md or
image with no counterpart is always reported as a problem, never as
expected and waiting.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from io import BytesIO
from pathlib import Path

import yaml
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


# === CONFIGURE TO MATCH YOUR REPO ===
# Astro content collection directory. Each post is a single file:
# src/content/post/<slug>.md. The file name is the URL slug.
POSTS_DIR = Path("src/content/post")
# Where featured/inline images live, referenced from frontmatter as
# /images/posts/<file>.
PUBLIC_IMAGES_DIR = Path("public/images/posts")
# ====================================

IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")

# Required by src/content.config.ts's `post` schema. metaTitle and
# dateModified are optional there. featuredImage is optional in the schema
# too, but every post filed through this pipeline arrives with its image, so
# it is required here.
REQUIRED_FIELDS = {"title", "description", "date", "categories"}

# Every field the site schema accepts. Zod strips anything else without
# warning once the file reaches the site -- this is how motive-training lost
# 65 posts' worth of dateModified values -- so the pipeline drops unknown
# keys here instead, where it shows up in the run log.
SCHEMA_FIELDS = {
    "title", "metaTitle", "description", "date", "dateModified",
    "featuredImage", "categories", "published",
}

QUEUE_FOLDER_ID = os.environ["DRIVE_QUEUE_FOLDER_ID"]
PROCESSED_FOLDER_ID = os.environ["DRIVE_PROCESSED_FOLDER_ID"]


def drive_service():
    creds_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def list_queue(svc):
    result = svc.files().list(
        q=f"'{QUEUE_FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name, mimeType, size)",
        pageSize=200,
    ).execute()
    return result.get("files", [])


def find_pairs(files):
    """Return (pairs, unpaired) for the queue.

    A post needs both its markdown and its image, always -- this pipeline
    has no "photo to follow" state. Anything with no counterpart is
    reported as unpaired so it is never left silently unpublished.
    """
    by_stem = {}
    ignored = []
    for f in files:
        name = f["name"]
        suffix = Path(name).suffix.lower()
        if suffix != ".md" and suffix not in IMAGE_SUFFIXES:
            if f.get("mimeType") != "application/vnd.google-apps.folder":
                ignored.append((name, "not a .md or image file"))
            continue
        stem = Path(name).stem
        by_stem.setdefault(stem, {})[suffix] = f

    pairs, unpaired = [], list(ignored)
    for stem, items in by_stem.items():
        md_file = items.get(".md")
        image_files = [items[s] for s in IMAGE_SUFFIXES if s in items]
        if md_file and image_files:
            if len(image_files) > 1:
                unpaired.append((
                    md_file["name"],
                    f"more than one image matches stem '{stem}': "
                    f"{[f['name'] for f in image_files]}",
                ))
                continue
            pairs.append((md_file, image_files[0]))
        elif md_file:
            unpaired.append((md_file["name"], f"no matching image for '{stem}' in the queue"))
        else:
            for img in image_files:
                unpaired.append((img["name"], f"no matching {stem}.md in the queue"))
    return pairs, unpaired


def download(svc, file_id):
    request = svc.files().get_media(fileId=file_id)
    buf = BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def parse_frontmatter(md_bytes):
    text = md_bytes.decode("utf-8")
    if not text.startswith("---\n"):
        return None, None, "Missing opening frontmatter delimiter"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, None, "Unclosed frontmatter block"
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError as e:
        return None, None, f"YAML parse error: {e}"
    body = text[end + 5:]
    return fm, body, None


def normalize_frontmatter(fm, image_name):
    """Adapt frontmatter to the site schema and fill in the image.

    `published` defaults true when absent, matching the schema default.
    `featuredImage` is filled in from the paired image when the filer left
    it empty; a value already present is left untouched (and checked
    against the actual image in validate()).

    Anything the site schema doesn't accept is dropped here rather than
    carried into the repo, because Zod would discard it silently downstream.
    """
    if "published" not in fm:
        fm["published"] = True
    if not fm.get("featuredImage"):
        fm["featuredImage"] = f"/images/posts/{image_name}"

    unknown = sorted(set(fm) - SCHEMA_FIELDS)
    if unknown:
        print(f"  dropping fields not in the post schema: {unknown}")
        for key in unknown:
            del fm[key]

    return fm


def serialize_frontmatter(fm, body):
    """Rebuild a markdown file from a (possibly normalized) frontmatter dict."""
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    return f"---\n{front}---\n{body}"


def coerce_date(raw_date):
    """Normalize a frontmatter date to a tz-aware datetime, or None if unparseable.

    PyYAML's safe_load implicitly parses unquoted ISO-8601-looking scalars into
    datetime.date/datetime.datetime, so `raw_date` may already be one of those
    instead of a string.
    """
    if isinstance(raw_date, datetime):
        return raw_date if raw_date.tzinfo else raw_date.replace(tzinfo=timezone.utc)
    if isinstance(raw_date, date):
        return datetime(raw_date.year, raw_date.month, raw_date.day, tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(raw_date))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def validate(fm, image_name, md_name):
    errors = []

    missing = REQUIRED_FIELDS - set(fm.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {sorted(missing)}")

    if not isinstance(fm.get("categories"), list) or not fm.get("categories"):
        errors.append("categories must be a non-empty list")

    expected_image = f"/images/posts/{image_name}"
    if fm.get("featuredImage") != expected_image:
        errors.append(
            f"featuredImage mismatch: frontmatter='{fm.get('featuredImage')}' "
            f"but image is '{image_name}' (expected '{expected_image}')"
        )

    md_stem = Path(md_name).stem
    img_stem = Path(image_name).stem
    if md_stem != img_stem:
        errors.append(f"Filename stem mismatch: {md_stem} vs {img_stem}")

    raw_date = fm.get("date")
    if raw_date is not None and coerce_date(raw_date) is None:
        errors.append(f"Invalid date format: {raw_date}")

    raw_modified = fm.get("dateModified")
    if raw_modified is not None and coerce_date(raw_modified) is None:
        errors.append(f"Invalid dateModified format: {raw_modified}")

    return errors


def held_until(fm):
    """Return the post's publish date if it has not arrived yet, else None.

    A future date is a schedule, not a defect: the post stays in the Drive
    queue and the first run on or after that date picks it up.
    """
    post_date = coerce_date(fm.get("date"))
    if post_date is not None and post_date > datetime.now(timezone.utc):
        return post_date
    return None


def move_to_processed(svc, file_id):
    f = svc.files().get(fileId=file_id, fields="parents").execute()
    previous = ",".join(f.get("parents", []))
    svc.files().update(
        fileId=file_id,
        addParents=PROCESSED_FOLDER_ID,
        removeParents=previous,
        fields="id, parents",
    ).execute()


def report_failures(failures):
    """Surface rejected posts and flag the run as failed.

    Written into the Actions job summary plus a marker file; the workflow's
    final step turns that marker into a non-zero exit, which fires GitHub's
    built-in failed-run email so a bad post never sits unnoticed in the queue.
    """
    lines = ["## ⚠️ Posts rejected — left in the Drive queue", ""]
    for name, reason in failures:
        lines.append(f"- **{name}** — {reason}")
    report = "\n".join(lines) + "\n"
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(report)
    Path("publish_failures.txt").write_text(report)


def report_unpaired(unpaired):
    """Surface queue files that never reach validation.

    A .md with no image, or an image with no .md, is always a problem here:
    every post is filed with its photo attached.
    """
    lines = ["## Queue files missing their counterpart", ""]
    for name, reason in unpaired:
        lines.append(f"- **{name}** — {reason}")
    report = "\n".join(lines) + "\n"
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(report)


def report_held(held):
    """Note scheduled posts in the job summary, without failing the run."""
    lines = ["## Posts held for a future publish date", ""]
    for name, when in held:
        lines.append(f"- **{name}** — scheduled for {when:%Y-%m-%d}")
    report = "\n".join(lines) + "\n"
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(report)


def archive_published(path="published_ids.txt"):
    """Move the Drive files for posts whose push has landed.

    Called from the workflow after git push succeeds, so a rejected push
    leaves the queue untouched and the post publishes on the next run.
    """
    ids_file = Path(path)
    if not ids_file.exists():
        print("No published ids to archive.")
        return
    svc = drive_service()
    moved = 0
    for line in ids_file.read_text().splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        for file_id in parts:
            try:
                move_to_processed(svc, file_id)
                moved += 1
            except Exception as exc:  # noqa: BLE001
                # A file that cannot be moved is not worth failing the run
                # over: the post is already published, and the leftover shows
                # up in the next run's unpaired report.
                print(f"Could not move {file_id} to Processed: {exc}")
    print(f"Archived {moved} file(s) to Processed.")


def main():
    svc = drive_service()
    files = list_queue(svc)
    pairs, unpaired = find_pairs(files)

    if not pairs and not unpaired:
        print("No complete pairs in queue.")
        return

    published = []
    failures = []
    held = []

    for md_file, img_file in pairs:
        stem = Path(md_file["name"]).stem
        print(f"\n--- Processing: {stem} ---")

        md_bytes = download(svc, md_file["id"])
        fm, body, err = parse_frontmatter(md_bytes)
        if err:
            print(f"Frontmatter error in {md_file['name']}: {err}")
            failures.append((md_file["name"], err))
            continue

        fm = normalize_frontmatter(fm, img_file["name"])
        errors = validate(fm, img_file["name"], md_file["name"])
        if errors:
            print(f"Validation failed for {md_file['name']}: {errors}")
            failures.append((md_file["name"], "; ".join(errors)))
            continue

        publish_on = held_until(fm)
        if publish_on:
            print(f"Held until {publish_on:%Y-%m-%d}: {md_file['name']}")
            held.append((md_file["name"], publish_on))
            continue

        md_path = POSTS_DIR / f"{stem}.md"
        img_path = PUBLIC_IMAGES_DIR / img_file["name"]
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        PUBLIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        img_bytes = download(svc, img_file["id"])
        md_path.write_bytes(serialize_frontmatter(fm, body).encode("utf-8"))
        img_path.write_bytes(img_bytes)

        subprocess.run(
            ["git", "add", str(md_path), str(img_path)],
            check=True,
        )
        published.append((stem, md_file["id"], img_file["id"]))
        print(f"Staged: {md_path}, {img_path}")

    if published:
        lines = ["Publish from Drive queue", ""]
        for stem, _, _ in published:
            lines.append(f"- {stem}")
        subprocess.run(["git", "commit", "-m", "\n".join(lines)], check=True)

        # The Drive files are deliberately NOT moved here. A commit is not a
        # publish: the push can still be rejected, and when it is, the commit
        # dies with the runner. The ids are handed to the workflow instead,
        # which moves them only after the push lands. Until then the post
        # stays in the queue, and the worst case is that the next run
        # publishes it again.
        Path("published_ids.txt").write_text(
            "".join(f"{md_id} {img_id}\n" for _, md_id, img_id in published)
        )
        print(f"\nStaged {len(published)} post(s) for publish.")
    elif held and not failures:
        print("\nNothing due yet; every queued post is held for a later date.")
    else:
        print("\nNothing valid to publish.")

    # Files with no counterpart never reached validation; name them so a post
    # cannot sit in the queue indefinitely without anyone hearing about it.
    if unpaired:
        report_unpaired(unpaired)

    # Held posts stay in the queue and publish themselves once their date
    # arrives -- reported, but never a reason to fail the run.
    if held:
        report_held(held)

    # Rejected posts stay in the queue; flag the run so the failure is noticed.
    if failures:
        report_failures(failures)


if __name__ == "__main__":
    if "--archive-published" in sys.argv:
        archive_published()
    else:
        main()
