# The Mobility Blog

Astro static site, rebuilt off WordPress. Deployed on Vercel at
[vercel.com/motive-a09ec8ec/themobilityblog](https://vercel.com/motive-a09ec8ec/themobilityblog).

## Commands

```bash
bun install
bun run dev      # local dev
bun run build    # astro check + astro build
bun run preview  # preview built output
```

## Adding a post

Create `src/content/post/{slug}.md`:

```yaml
---
title: "Post Title"
description: "Meta description, ~155 chars"
date: "2026-01-01T00:00:00Z"
dateModified: "2026-02-01T00:00:00Z"   # only when revising
featuredImage: "/images/posts/your-image.jpg"
categories:
  - "Mobility"
published: true
---

Body in Markdown.
```

The file name (`{slug}`) becomes the URL: `src/content/post/what-is-mobility.md` → `/what-is-mobility`.

## Publishing from Drive

Posts can also be filed by dropping a matched `{slug}.md` + `{slug}.{jpg,jpeg,png,webp}`
pair into a Drive queue folder. `.github/workflows/publish-from-drive.yml` runs
daily (and on manual dispatch) via `.github/scripts/publish_from_drive.py`,
which:

- Requires both files, filed together, same base name — there is no
  "photo to follow later" state on this pipeline.
- Fills in `featuredImage` from the paired image if left blank, and defaults
  `published` to `true` if omitted.
- Validates the frontmatter against `src/content.config.ts`'s `post` schema
  (`title`, `description`, `date`, non-empty `categories` are required;
  `metaTitle` and `dateModified` are optional) and drops any field the
  schema doesn't accept, so a typo doesn't silently vanish once merged.
- Holds a post with a future `date` in the queue until that date arrives,
  rather than publishing it early.
- Rejects (and leaves in the queue, with the reason in the Actions job
  summary) anything that fails validation, or a `.md`/image with no
  counterpart.

Needs three repo secrets: `GOOGLE_SERVICE_ACCOUNT_JSON` (a Drive-scoped
service account), `DRIVE_QUEUE_FOLDER_ID`, `DRIVE_PROCESSED_FOLDER_ID`
(where files move once published). These are separate from any secrets of
the same name in `motive-training` — each repo's secrets are its own, so
point `DRIVE_QUEUE_FOLDER_ID`/`DRIVE_PROCESSED_FOLDER_ID` at Drive folders
dedicated to this blog.

## Migration notes

- Content converted from a WordPress export (13 posts, 2 pages: About, Write With Us).
- Post images (featured + inline) live in `public/images/posts/`, pulled from
  the WordPress media library export.
- `src/content/page/` holds the About and Write With Us pages, rendered by
  `src/pages/[page].astro`.
- The original "Write With Us" page had a Jetpack contact form (name, email,
  message). Jetpack forms don't exist outside WordPress, so it's replaced here
  with a plain `mailto:` link. If you want a real submit-to-inbox form, that
  needs a backend (a Vercel serverless function, Formspree, or a Zapier
  webhook like the one `motive-training` uses) — a decision for later, not
  blocking launch.
