# Formatting Guide for Queued Posts

Hand this to Claude along with a draft (or a brief) when preparing a post for
the Drive queue. It covers format only: how the file has to look so the
publisher accepts it and the site renders it correctly. Voice, sourcing, and
structure live in `briefs/README.md`.

The Drive publisher checks every rule marked **(checked)** and rejects the
post if it fails, leaving it in the queue with the reason in the GitHub
Actions log.

## The Two Files

- A Markdown file and an image with the same name: `my-post-slug.md` and
  `my-post-slug.jpg`. **(checked)**
- The name is the URL: `my-post-slug.md` publishes at `/my-post-slug`.
  Lowercase, words joined by hyphens, no dates.
- Image: JPG for photos and illustrations, roughly 16:9. Any size is fine; the
  publisher shrinks it to 1600px wide and compresses it.

## Frontmatter

Start the file with this block, exactly this shape:

```yaml
---
title: "Title in Title Case"
metaTitle: "Shorter Search Title"      # optional; 42 characters or fewer
description: "140 to 155 characters, written as a reason to click."
date: "2026-11-05T12:00:00Z"            # a future date holds the post until then
featuredImage: "/images/posts/my-post-slug.jpg"
imageAlt: "What the image literally shows"
author: "Guest Name"                   # guest posts ONLY; leave out for Brian
authorUrl: "https://guest-site.com/"   # optional, guest posts only
categories:
  - "Mobility"
tags:
  - "stretching"
  - "assessment"
published: true
---
```

- `title`, `description`, and `date` are required. **(checked)**
- `title` and `metaTitle` never end with a period. A period mid-title is
  fine. **(checked)**
- `featuredImage` must be `/images/posts/` plus the image's file name.
  **(checked)**
- `author`: leave it out for Brian's posts; the byline and the About the
  Author box are added automatically. For a guest post it is required, or the
  post publishes under Brian's name. **(checked)**
- `tags`: 1 to 3, using these exact slugs only **(checked)**:
  `fundamentals`, `stretching`, `isometrics`, `assessment`, `programming`,
  `hips`, `ankles`, `spine`, `posture`, `frc-and-kinstretch`,
  `pain-and-hypermobility`, `coaching`, `expert-roundups`.
  The first tag is the post's main topic and shows in its breadcrumb.
- `categories`: one of `Mobility`, `Stretching`, `Isometrics`, `Posture`.

## Body

- No `#` heading in the body; the title is the page's H1.
- Sections use `##`, subsections `###`. Every heading is Title Case and never
  ends with a period. **(checked)**
- No em dashes (`—`), no exclamation points, no bold (`**`). Italics are fine,
  sparingly. **(checked)**
- No "it's not X, it's Y" constructions. **(checked)**
- No typed byline (`*By Name*`) and no author bio for Brian; both come from
  the site. **(checked)** Guest posts may end with a `## About the Author`
  section of two or three sentences.
- References: a final `## References` (or `## Sources`) section, numbered,
  matching `(1)` or `[1]` citations in the text, each with a working URL.
- Inline images: `![What the image shows](/images/posts/file.jpg)`. The image
  file has to be added to the repo separately; the queue only carries the
  featured image.

## Links

- Every link has a real target. No placeholders like `POST_URL` or `TODO`.
  **(checked)**
- Link to other posts with a relative path, `[Title](/slug)`, never the full
  `https://www.themobilityblog.com/...` URL. The path must be a post that
  exists. **(checked)**
- Topic pages: `/topics/<tag>`, for example `/topics/hips`. Site pages:
  `/about`, `/write-with-us`. **(checked)**
- Links to movewithpurpose.com are written as plain URLs; tracking tags are
  added automatically.

Current posts you can link to:

- 4 Common Stretching Mistakes and How to Correct Them: `/4-common-stretching-mistakes-and-how-to-correct-them`
- The 90/90 Hip Stretch: How to Do It Right, and What It's Actually Training: `/90-90-hip-stretch`
- Active Mobility, Flexibility, and Rehearsal Sets: Which Goal Are You Solving?: `/active-mobility-flexibility-rehearsal-sets`
- Ankle Dorsiflexion: What Restricts It, How to Test It, and How to Rebuild: `/ankle-dorsiflexion-what-restricts-it-how-to-test-it-and-rebuild-it`
- Fitness Is Something You Maintain: `/fitness-is-something-you-maintain`
- Flexibility Is Range. Mobility Is What You Can Do With It: `/flexibility-is-range-mobility-is-what-you-can-do-with-it`
- Hip Internal Rotation: The Range Most People Lose: `/hip-internal-rotation-the-range-most-people-lose`
- How Do You Structure Mobility Into Your Workout Routine?: `/how-do-you-structure-mobility-into-your-workout-routine`
- How Much Stretching Does It Take to Change Your Range?: `/how-much-stretching-does-it-take-to-change-your-range`
- Isometrics: Infinite Tension, Infinite Potential: `/isometrics-infinite-tension-infinite-potential`
- Mobility as Capacity, Not a Category: `/mobility-as-capacity-not-a-category`
- Mobility Isn’t a Warm-Up. It’s the Work: `/mobility-isnt-a-warm-up-its-the-work`
- Posture: An Ongoing Fight Against Gravity: `/posture-an-ongoing-fight-against-gravity`
- The Trunk Isn't Always a Brace: `/the-trunk-isnt-always-a-brace`
- What CARs Are Actually For: `/what-cars-are-actually-for`
- What Does Mobility Mean? We Asked the Pros: `/what-does-mobility-mean-we-asked-the-pros`
- What Is Mobility? A Coach's Definition, and How to Train It: `/what-is-mobility`
- What We Mean When We Say Tight: `/what-we-mean-when-we-say-tight`
- When Stretching Makes Pain Worse: How to Spot the Red Flags: `/when-stretching-makes-pain-worse-how-to-spot-the-red-flags`
- When the Method Becomes the Answer: `/when-the-method-becomes-the-answer`
- Why Mobility Doesn't Stick: `/why-mobility-doesnt-stick`

(This list is a snapshot. Anything published after it is also a valid link
target; the check looks at the repo when the queue runs.)

## Before It Goes in the Queue

- File names match, and `featuredImage` matches the image name.
- Guest post: `author:` set, no typed byline.
- 1 to 3 tags from the list.
- Every link points at a real post, topic, page, or full URL.
- Search the body for `—`, `!`, and `**`.
