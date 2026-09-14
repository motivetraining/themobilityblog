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
