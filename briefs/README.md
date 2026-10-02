# Writing Briefs

One brief per planned post. Each brief is written so Claude (or any writer)
can draft a publishable post from it without further back-and-forth. This file
holds the rules every brief shares. Read it in full before drafting from any
brief.

The `briefs/` folder sits outside `src/`, so nothing here is built into the
site.

## How to Run a Brief

Give Claude a prompt like:

> Write the post in `briefs/01-90-90-hip-stretch.md`, following
> `briefs/README.md`. Open a PR with the draft.

Claude should then:

1. Read this file, the brief, and every existing post the brief names under
   **Internal links** and **Don't repeat** (so the new post doesn't
   contradict or duplicate them).
2. Read two recent posts for voice:
   `src/content/post/ankle-dorsiflexion-what-restricts-it-how-to-test-it-and-rebuild-it.md`
   and `src/content/post/hip-internal-rotation-the-range-most-people-lose.md`.
3. Research and verify every source before citing it (see **Sources** below).
4. Write `src/content/post/{slug}.md` with `published: false` and
   `featuredImage: "/images/posts/{slug}.jpg"`.
5. Run the voice checks below against the body. If the network allows it,
   also run `bun run build`.
6. Open a PR. In its body, list the target keyword, the word count, every
   source with a note on what it supports, and anything in the brief that
   couldn't be verified and was cut or softened.

Brian then adds the featured image (`public/images/posts/{slug}.jpg`, at most
1600px wide, 16:9 crops best), reads the draft, and flips it to
`published: true` with a `date` on merge.

The Drive queue (`.github/workflows/publish-from-drive.yml`) is the other way
in: a `{slug}.md` and `{slug}.jpg` pair dropped in the queue folder publishes
the next morning. The same rules apply. The queue's validator rejects a post
that breaks the voice checks, so run them first either way.

## Frontmatter

```yaml
---
title: "Title in Title Case"
metaTitle: "Shorter Search Title"   # 42 characters or fewer; the site appends " | The Mobility Blog"
description: "Meta description, 140 to 155 characters, containing the target keyword once, written as a reason to click."
date: "YYYY-MM-DDT12:00:00Z"
featuredImage: "/images/posts/{slug}.jpg"
imageAlt: "What the image literally shows, e.g. A coach demonstrating the 90/90 hip position on a gym floor"
categories:
  - "Mobility"
published: false
---
```

- Leave out `author` for Brian's posts. It defaults to Brian Murray, and the
  byline renders from it. Don't add an author bio to the body.
- Known categories: Mobility, Stretching, Isometrics, Posture. Use one of
  these unless the brief says otherwise.
- The slug (the file name) is set in each brief. Don't change it; internal
  links from other briefs depend on it.

## Voice Checks (Hard Rules)

The Drive publisher rejects posts that break these, and posts added by hand
are held to the same standard:

- No em dashes (`—`) anywhere in the body. Use a comma, a colon, parentheses,
  or two sentences.
- No exclamation points.
- No bold (`**`) in the body. Italics are fine, sparingly.
- No "it's not X, it's Y" antithesis constructions. The validator matches
  `it'?s not (just )?[^.]*,? it'?s` case-insensitively. Also avoid the
  pattern in spirit ("This isn't about X. It's about Y.").
- Headings never end with a period.
- `title` and every `##`/`###` heading are in Title Case, per the rule in the
  repo `README.md`.

## Voice (How the Site Sounds)

- First person, from Brian: a mobility coach with sixteen years of hands-on
  experience, running Motive Training in Austin, TX, trained in Functional
  Range Conditioning (FRC) and WeckMethod. Use "I" for his view and "we" for
  what Motive does with clients. Don't invent client stories, names, or
  numbers. Describe patterns ("people who come in with...") rather than
  specific people.
- Open with a concrete scene or a common frustration the reader recognizes,
  not a definition and not a question to the reader. The ankle and hip IR
  posts show the pattern.
- Explain the mechanism. The site's edge over generic fitness content is the
  *why*: which structure limits the range, what the nervous system is doing,
  why the common fix underdelivers.
- Be straight about evidence. When research is thin, mixed, or comes from
  small studies, say so in plain language. A section like "Where the Evidence
  Gets Messy" is on brand.
- Include a safety caveat that says when to stop and see a clinician (sharp or
  pinching pain, bony end feel, numbness or tingling, pain at night, history
  of dislocation). Keep it specific, not boilerplate.
- Plain, adult sentences. No hype words (unlock, game-changer, secret,
  hack, ultimate), no listicle filler, no "In this article we will".
- Recurring ideas the site has already argued, which can be referenced and
  linked rather than re-explained: flexibility is passive range and mobility
  is controlled, usable range; range needs load, intent, and frequency to
  stick; CARs maintain and assess rather than build range; end-range
  isometrics and PAILs/RAILs are how range gets converted into capacity;
  resistance training improves range of motion.

## Structure

- Answer the search intent early. If someone searched for exercises, the
  exercises (or a clear pointer to them) belong in the first third, not after
  1,000 words of theory.
- Exercise instructions: a `###` heading per exercise, then setup, the
  movement, what to feel, the most common fault, and a dose (holds, reps,
  sets, frequency). Plain numbered steps are fine.
- Give regressions for people who can't get into the position, and a
  progression for people who find it easy.
- End with a short practical wrap-up, not "Final Thoughts" filler. Then a
  `## References` section, numbered, matching inline `(1)` style citations as
  in the ankle post, or inline links as in the hip IR post. Pick one style per
  post.
- Word counts in each brief are targets, not quotas. Don't pad.

## Sources

- Every factual claim that isn't Brian's coaching opinion needs a source the
  writer has opened and read. Prefer PubMed, PMC, journal DOIs, and
  professional bodies (WHO, CDC, ACSM). Avoid content farms and other blogs.
- Never cite a study you haven't confirmed exists and says what you claim.
  The briefs suggest starting points, all marked "verify". A suggestion that
  doesn't check out gets dropped, not paraphrased from memory.
- Link the source itself (DOI or PubMed URL), never a proxy, library mirror,
  or institutional VPN URL.
- Don't give specific degree norms, percentages, or effect sizes without a
  source that states them.

## Internal Links

Every post links to at least three existing posts where they genuinely help,
using relative paths. Existing posts and what they cover:

| Path | Covers |
| :--- | :--- |
| `/what-is-mobility` | Definition of mobility (being expanded: see brief 00) |
| `/flexibility-is-range-mobility-is-what-you-can-do-with-it` | Flexibility vs mobility |
| `/mobility-as-capacity-not-a-category` | Mobility as capacity, the "more options" argument |
| `/mobility-isnt-a-warm-up-its-the-work` | Mobility as training, not warm-up |
| `/why-mobility-doesnt-stick` | Load, intent, frequency; hip flexor PAILs/RAILs walkthrough |
| `/what-cars-are-actually-for` | CARs: what they assess and maintain, where they're oversold |
| `/isometrics-infinite-tension-infinite-potential` | Isometrics and tension |
| `/hip-internal-rotation-the-range-most-people-lose` | Hip IR: why it's lost, testing, rebuilding |
| `/ankle-dorsiflexion-what-restricts-it-how-to-test-it-and-rebuild-it` | Ankle dorsiflexion |
| `/when-stretching-makes-pain-worse-how-to-spot-the-red-flags` | Hypermobility, when stretching backfires (guest post) |
| `/4-common-stretching-mistakes-and-how-to-correct-them` | Stretching mistakes (expert roundup) |
| `/how-do-you-structure-mobility-into-your-workout-routine` | Programming mobility (expert roundup) |
| `/what-does-mobility-mean-we-asked-the-pros` | What mobility means (expert roundup) |
| `/posture-an-ongoing-fight-against-gravity` | Posture, and how different systems approach it |

Once briefs are published, link between them too. Each brief lists its
planned slug.

## Calls to Action

At most one or two, placed where they help rather than as a sign-off:

- [Motive Mobility / KINSTRETCH Online](https://motive-mobility.circle.so/c/welcome-start-here): Brian's online classes.
- [Motive Training](https://www.movewithpurpose.com/): the sponsor, in-person training in Austin.
- Motive's deeper guides, when the post touches them:
  [PAILs and RAILs](https://www.movewithpurpose.com/pails-rails),
  [CARs guide](https://www.movewithpurpose.com/controlled-articular-rotations-guide),
  [Functional Range Assessment](https://www.movewithpurpose.com/functional-range-assessment),
  [ankle mobility foundations class](https://www.movewithpurpose.com/new-to-kinstretch-ankle-mobility-foundations).

## Keyword Data

Search volumes and difficulty (KD, 0 to 100) in each brief are US monthly
figures from Mangools KWFinder, pulled October 2026. Search Console wasn't
connected when these were written. Once it is, check each published post's
actual queries after 6 to 8 weeks and revise the headings and intro to match.

## Order

| # | Brief | Target keyword | Volume | KD |
| :-- | :--- | :--- | --: | --: |
| 00 | [What Is Mobility? (refresh)](00-what-is-mobility-refresh.md) | what is mobility | 1,500 | 23 |
| 01 | [The 90/90 hip stretch](01-90-90-hip-stretch.md) | 90 90 hip stretch | 14,400 | 27 |
| 02 | [Shoulder mobility exercises](02-shoulder-mobility-exercises.md) | shoulder mobility exercises | 7,200 | 36 |
| 03 | [Thoracic spine mobility](03-thoracic-spine-mobility.md) | thoracic mobility exercises | 2,000 | 29 |
| 04 | [PAILs and RAILs explained](04-pails-and-rails.md) | pails and rails | 650 | n/a |
| 05 | [What is FRC?](05-functional-range-conditioning.md) | functional range conditioning | 960 | n/a |
| 06 | [What is Kinstretch?](06-kinstretch.md) | kinstretch | 670 | 18 |
| 07 | [Mobility for older adults](07-mobility-exercises-for-older-adults.md) | mobility exercises for seniors | 630 | 21 |
| 08 | [Hip flexor mobility](08-hip-flexor-mobility.md) | hip flexor mobility exercises | 550 | 26 |
| 09 | [Strength training for mobility](09-strength-training-for-mobility.md) | mobility strength training | 360 | 26 |
| 10 | [Wrist mobility exercises](10-wrist-mobility-exercises.md) | wrist mobility exercises | 810 | 44 |

Do 00 first. It already ranks (position 81), and every later post links back
to it.
