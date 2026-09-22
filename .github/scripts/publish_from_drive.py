#!/usr/bin/env python3
"""
Publish from Drive.

Scans a Drive queue folder for matched .md + image (.jpg/.jpeg/.png/.webp)
pairs (same base name), validates the markdown frontmatter against
themobilityblog's schema and voice rules, writes the post and its image
into the Astro content collection, commits, and moves the source files in
Drive to a processed/ folder. Validation failures leave files in place and
fail the run so the Actions failed-run email fires.

Adapted from motive-training's publish_from_drive.py. themobilityblog's
post schema is flatter: one .md file per post (not a directory), and a
single featuredImage field instead of a split featuredMedia/imageType/OG
system, so this version is simpler.
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
# Astro content collection directory. Each post is a single file,
# src/content/post/<slug>.md. The file name is the URL slug.
POSTS_DIR = Path("src/content/post")
# Where featuredImage paths ("/images/posts/<file>") resolve to on disk.
IMAGES_DIR = Path("public/images/posts")
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")
# ====================================


# Categories seen across existing posts. Not enforced by the Zod schema
# (categories has a default), but kept here so the queue catches a typo
# before it ships as a new, uninentional category.
KNOWN_CATEGORIES = {"Mobility", "Stretching", "Isometrics", "Posture"}

# Required by src/content.config.ts's post schema: fields with no .optional()
# or .default(). metaTitle, dateModified, and featuredImage are optional
# there; categories and published both have defaults, so neither is required.
REQUIRED_FIELDS = {"title", "description", "date"}

# Every field the post schema accepts. Anything else is dropped here rather
# than carried into the repo, where Astro's Zod schema would silently strip
# it -- see motive-training's publish_from_drive.py for what happens when
# that's not caught upstream.
SCHEMA_FIELDS = {
    "title", "metaTitle", "description", "date", "dateModified",
    "featuredImage", "categories", "published",
}

# Spellings seen for the last-updated date, in case a queued draft uses one.
UPDATED_DATE_ALIASES = ("DateModified", "date_modified", "modifiedDate", "lastModified", "updatedDate")

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

    A post needs both its markdown and an image. Anything with only one half
    is returned as unpaired rather than dropped, since a doc whose image
    never got uploaded looks identical, from here, to one nobody meant to
    publish yet -- but it's the first case in practice, and dropping it
    silently means the post never ships and nothing ever says so.
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
        kind = "md" if suffix == ".md" else "img"
        by_stem.setdefault(stem, {})[kind] = f

    pairs, unpaired = [], list(ignored)
    for stem, items in by_stem.items():
        if "md" in items and "img" in items:
            pairs.append((items["md"], items["img"]))
        elif "md" in items:
            unpaired.append((items["md"]["name"], f"no matching image for {stem} in the queue"))
        else:
            unpaired.append((items["img"]["name"], f"no matching {stem}.md in the queue"))
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
    """Adapt a queued draft's frontmatter to the site schema.

    Fills in featuredImage from the paired image if the draft omitted it,
    folds date-modified aliases onto dateModified, and drops anything the
    schema doesn't accept rather than letting Zod silently strip it later.
    """
    if not fm.get("featuredImage"):
        fm["featuredImage"] = f"/images/posts/{image_name}"

    for alias in UPDATED_DATE_ALIASES:
        value = fm.pop(alias, None)
        if value and not fm.get("dateModified"):
            fm["dateModified"] = value

    if "published" not in fm:
        fm["published"] = True

    unknown = sorted(set(fm) - SCHEMA_FIELDS)
    if unknown:
        print(f"  dropping fields not in post schema: {unknown}")
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
    datetime.date/datetime.datetime, so raw_date may already be one of those
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


def validate(fm, body, image_name, md_name):
    errors = []

    missing = REQUIRED_FIELDS - set(fm.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {sorted(missing)}")

    expected_image = f"/images/posts/{image_name}"
    if fm.get("featuredImage") != expected_image:
        errors.append(
            f"featuredImage mismatch: frontmatter='{fm.get('featuredImage')}' "
            f"but queued image is '{image_name}' (expected '{expected_image}')"
        )

    md_stem = Path(md_name).stem
    img_stem = Path(image_name).stem
    if md_stem != img_stem:
        errors.append(f"Filename stem mismatch: {md_stem} vs {img_stem}")

    categories = fm.get("categories") or []
    if not isinstance(categories, list):
        errors.append("categories must be a list")
    else:
        unknown_categories = sorted(set(categories) - KNOWN_CATEGORIES)
        if unknown_categories:
            print(f"  note: new categories not seen before: {unknown_categories}")

    raw_date = fm.get("date")
    if raw_date is not None and coerce_date(raw_date) is None:
        errors.append(f"Invalid date format: {raw_date}")

    raw_modified = fm.get("dateModified")
    if raw_modified is not None and coerce_date(raw_modified) is None:
        errors.append(f"Invalid dateModified format: {raw_modified}")

    # Voice rule checks against body only.
    if "—" in body:
        errors.append("Em dash found in body")
    if "!" in body:
        errors.append("Exclamation point found in body")
    if "**" in body:
        errors.append("Bold markdown found in body")

    # Checked across frontmatter as well as body: description ships as
    # rendered prose (meta description, OG description), so a body-only
    # check would let "whether" through the queue in the one field that
    # actually reaches the page's <head>.
    fm_text = " ".join(str(v) for v in fm.values() if isinstance(v, str))
    if "whether" in body.lower():
        errors.append("Forbidden word 'whether' found in body")
    if "whether" in fm_text.lower():
        errors.append("Forbidden word 'whether' found in frontmatter")

    if re.search(r"it'?s not (just )?[^.]*,? it'?s", body, re.IGNORECASE):
        errors.append("Antithesis construction found in body (not X, it's Y)")

    for line in body.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("#") and stripped.rstrip().endswith("."):
            errors.append(f"Heading ends with period: {stripped.strip()}")
            break

    return errors


def held_until(fm):
    """Return the post's publish date if it has not arrived yet, else None.

    A future date is a schedule, not a defect: the post stays in the Drive
    queue and the first daily run on or after that date picks it up.
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

    Written into the Actions job summary and a marker file the workflow's
    final step turns into a non-zero exit, which fires GitHub's built-in
    failed-run email so a bad post never sits unnoticed in the queue.
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

    Not a rejection -- nothing about them was judged -- but a file sitting
    here is a post that will never publish, so it has to be visible.
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
        errors = validate(fm, body, img_file["name"], md_file["name"])
        if errors:
            print(f"Validation failed for {md_file['name']}: {errors}")
            failures.append((md_file["name"], "; ".join(errors)))
            continue

        publish_on = held_until(fm)
        if publish_on:
            print(f"Held until {publish_on:%Y-%m-%d}: {md_file['name']}")
            held.append((md_file["name"], publish_on))
            continue

        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        md_path = POSTS_DIR / f"{stem}.md"
        img_path = IMAGES_DIR / img_file["name"]

        img_bytes = download(svc, img_file["id"])
        md_path.write_bytes(serialize_frontmatter(fm, body).encode("utf-8"))
        img_path.write_bytes(img_bytes)

        subprocess.run(["git", "add", str(md_path), str(img_path)], check=True)
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
        # which moves them only after the push lands.
        Path("published_ids.txt").write_text(
            "".join(f"{md_id} {img_id}\n" for _, md_id, img_id in published)
        )
        print(f"\nStaged {len(published)} post(s) for publish.")
    elif held and not failures:
        print("\nNothing due yet; every queued post is held for a later date.")
    else:
        print("\nNothing valid to publish.")

    if unpaired:
        report_unpaired(unpaired)

    if held:
        report_held(held)

    if failures:
        report_failures(failures)


if __name__ == "__main__":
    if "--archive-published" in sys.argv:
        archive_published()
    else:
        main()
