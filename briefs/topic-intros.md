# Brief: Topic Page Intros

Each topic page (`/topics/hips`, `/topics/stretching`, ...) currently shows a
one-line description and a grid of posts. That's an archive, and archives
rarely rank. A short intro in Brian's voice turns each page into a hub that
can rank for the broad term ("hip mobility", "stretching for mobility"),
which no single post targets, and that tells a new reader where to start.

## How to Use This Brief

Paste this whole file into a Claude chat with this prompt:

> Write the topic page intros described in this brief, one at a time,
> starting with Fundamentals. For each, give me the finished Markdown file
> contents in a code block, labeled with its file name. Follow every rule in
> the brief. Ask me before inventing anything about my coaching that isn't
> in the brief or the post descriptions.

Read and edit each draft. They should sound like you, so change anything
that doesn't. Then save it as `src/content/topic/{slug}.md` in the repo
(or ask Claude Code to commit them). An intro shows up on the page on the
next deploy, and a topic without one keeps its one-line description.

## Order of Work

Write the topics with the most posts first: Fundamentals, Stretching,
Assessment, Programming, Hips, Coaching, then the two-post topics
(Isometrics, Spine & Core, FRC & Kinstretch, Expert Roundups). Ankles,
Posture, and Pain & Hypermobility have one post each and are hidden from
Google until they get a second, so leave them for last or skip them for now.

## What Each Intro Is

- 120 to 250 words of body text. Two or three short paragraphs. No headings,
  no frontmatter, no title (the page already shows the topic name as its H1).
- Paragraph one: how Brian thinks about this topic, the stance the posts
  share, in plain terms. Work in the broad search term naturally once, near
  the start (for example "hip mobility" on Hips, "stretching" and "range of
  motion" on Stretching). Don't stuff it.
- Paragraph two: where to start. Name one or two posts as the entry point and
  link them, and say who each is for ("If you're new to this, start with...";
  "If you already stretch every day and nothing changes, read...").
- Optional third paragraph: how the topic connects to another topic, with a
  link to that topic page (`/topics/{slug}`).
- Link only to posts and topic pages listed below, with relative paths
  exactly as written (`/what-is-mobility`, `/topics/hips`). Two to four links
  total.
- Don't summarize every post: the cards below the intro already do that.
- Don't introduce new claims, studies, or statistics. Everything should
  already be argued in the posts listed. No references section.

## Voice Rules (Hard)

These match `briefs/README.md`, which governs every post on the site:

- First person as Brian, a mobility coach with sixteen years of experience,
  founder of Motive Training in Austin, TX, trained in FRC. "I" for his view,
  "we" for what Motive does with clients. No invented client stories or
  numbers.
- No em dashes. Use a comma, colon, parentheses, or two sentences.
- No exclamation points. No bold. Italics sparingly.
- No "it's not X, it's Y" constructions, in letter or in spirit ("This isn't
  about X. It's about Y.").
- No hype words (unlock, game-changer, secret, hack, ultimate) and no "On
  this page you'll find".
- Plain, adult sentences. Don't open with a question to the reader or a
  dictionary definition.

Ideas the site already argues, which intros can lean on: flexibility is
passive range and mobility is controlled, usable range; range needs load,
intent, and frequency to stick; CARs maintain and assess rather than build
range; end-range isometrics and PAILs/RAILs turn range into capacity;
resistance training improves range of motion.

## Example of the Shape (Placeholder Wording, Not Final)

```markdown
Most people meet hip mobility as a stretch they hold before squatting. The
way I coach it, the hip is ...

If you're starting from scratch, read [Hip Internal Rotation: The Range Most
People Lose](/hip-internal-rotation-the-range-most-people-lose) first ...

The positions on this page get tested before they get trained, which is
what the [Assessment](/topics/assessment) posts cover.
```

## The Topics

### Fundamentals (`fundamentals`)

File: `src/content/topic/fundamentals.md` · Page: `/topics/fundamentals` · 6 posts

Current one-line description: What mobility is, how it differs from flexibility, and the vocabulary the rest of the site uses.

Posts:

- [Fitness Is Something You Maintain](/fitness-is-something-you-maintain): Most of how we talk about fitness treats it as an activity with a start and end date. A coach's case for treating it as a set of capacities you either keep or lose, and what that changes about training.
- [Flexibility Is Range. Mobility Is What You Can Do With It](/flexibility-is-range-mobility-is-what-you-can-do-with-it): Flexibility and mobility aren't the same thing. Learn why owning your range under control matters more than how far you can passively stretch.
- [Mobility as Capacity, Not a Category](/mobility-as-capacity-not-a-category): Mobility isn’t a category of exercise. It’s capacity. Learn why real mobility means controlling your ranges—not just stretching more.
- [Mobility Isn’t a Warm-Up. It’s the Work.](/mobility-isnt-a-warm-up-its-the-work): Mobility isn’t just a warm-up. It’s the work. Learn why joint control and strength should be trained and not rushed before lifting.
- [What Does Mobility Mean? We Asked the Pros](/what-does-mobility-mean-we-asked-the-pros): Mobility means control, independence, safety, and adaptability. Coaches and clinicians worldwide share what mobility really is.
- [What Is Mobility? A Coach's Definition, and How to Train It](/what-is-mobility): What is mobility? It's the range a joint can reach and control on its own. How it differs from flexibility, how to test it, and how to train it.

### Stretching (`stretching`)

File: `src/content/topic/stretching.md` · Page: `/topics/stretching` · 5 posts

Current one-line description: How stretching changes range, how much it takes, and where it helps or backfires.

Posts:

- [4 Common Stretching Mistakes and How to Correct Them](/4-common-stretching-mistakes-and-how-to-correct-them): 4 common stretching mistakes that may be holding you back. Learn how to correct them and build real mobility instead of chasing flexibility.
- [The 90/90 Hip Stretch: How to Do It Right, and What It's Actually Training](/90-90-hip-stretch): How to do the 90/90 hip stretch: setup, what you should feel, how to adjust it to your own hips, and how to load it so the range becomes usable.
- [Flexibility Is Range. Mobility Is What You Can Do With It](/flexibility-is-range-mobility-is-what-you-can-do-with-it): Flexibility and mobility aren't the same thing. Learn why owning your range under control matters more than how far you can passively stretch.
- [How Much Stretching Does It Take to Change Your Range?](/how-much-stretching-does-it-take-to-change-your-range): Stretching not working? Why two minutes is a floor, what the research actually tested, and how long holds plus loading make new range stick.
- [When Stretching Makes Pain Worse: How to Spot the Red Flags](/when-stretching-makes-pain-worse-how-to-spot-the-red-flags): Can stretching make pain worse? Learn the red flags of hypermobility and why pain keeps returning when you chase more range.

### Isometrics (`isometrics`)

File: `src/content/topic/isometrics.md` · Page: `/topics/isometrics` · 2 posts

Current one-line description: End-range isometrics and loaded holds: how tension turns passive range into usable range.

Posts:

- [Isometrics: Infinite Tension, Infinite Potential](/isometrics-infinite-tension-infinite-potential): Isometrics build strength through controlled tension. Learn how they improve joint health, stability, and long-term resilience.
- [Why Mobility Doesn't Stick](/why-mobility-doesnt-stick): New range that disappears by your next session isn't a lack of effort, it's an incomplete signal. Here's what actually makes mobility gains stick.

### Assessment (`assessment`)

File: `src/content/topic/assessment.md` · Page: `/topics/assessment` · 5 posts

Current one-line description: Testing a joint before training it: what to look for and how to read what you find.

Posts:

- [Ankle Dorsiflexion: What Restricts It, How to Test It, and How to Rebuild](/ankle-dorsiflexion-what-restricts-it-how-to-test-it-and-rebuild-it): Ankle dorsiflexion isn't one problem. It can come from the capsule, the mortise, either calf muscle, or a bony block, and each one needs a different fix.
- [Hip Internal Rotation: The Range Most People Lose](/hip-internal-rotation-the-range-most-people-lose): Most people lose hip internal rotation without noticing. Here's why it matters, how to test it, and how to build the range back safely.
- [What CARs Are Actually For](/what-cars-are-actually-for): CARs don't build new range, they maintain what you have. What controlled articular rotations actually measure, and where the hype outruns the evidence.
- [What Is Mobility? A Coach's Definition, and How to Train It](/what-is-mobility): What is mobility? It's the range a joint can reach and control on its own. How it differs from flexibility, how to test it, and how to train it.
- [When the Method Becomes the Answer](/when-the-method-becomes-the-answer): PRI, FRC, McGill, and 90/90 all have real value. The trouble starts when any one of them gets sold as the answer. A coach's view on methods, certainty, and why assessment has to come first.

### Programming (`programming`)

File: `src/content/topic/programming.md` · Page: `/topics/programming` · 5 posts

Current one-line description: Where mobility work fits in a training week, how often to do it, and how to make the gains stick.

Posts:

- [Fitness Is Something You Maintain](/fitness-is-something-you-maintain): Most of how we talk about fitness treats it as an activity with a start and end date. A coach's case for treating it as a set of capacities you either keep or lose, and what that changes about training.
- [How Do You Structure Mobility Into Your Workout Routine?](/how-do-you-structure-mobility-into-your-workout-routine): What's the best way to structure your mobility routine? We asked the pros; here is what they had to say.
- [How Much Stretching Does It Take to Change Your Range?](/how-much-stretching-does-it-take-to-change-your-range): Stretching not working? Why two minutes is a floor, what the research actually tested, and how long holds plus loading make new range stick.
- [Mobility Isn’t a Warm-Up. It’s the Work.](/mobility-isnt-a-warm-up-its-the-work): Mobility isn’t just a warm-up. It’s the work. Learn why joint control and strength should be trained and not rushed before lifting.
- [Why Mobility Doesn't Stick](/why-mobility-doesnt-stick): New range that disappears by your next session isn't a lack of effort, it's an incomplete signal. Here's what actually makes mobility gains stick.

### Hips (`hips`)

File: `src/content/topic/hips.md` · Page: `/topics/hips` · 4 posts

Current one-line description: Hip rotation, hip flexors, and the positions most people lose first.

Posts:

- [The 90/90 Hip Stretch: How to Do It Right, and What It's Actually Training](/90-90-hip-stretch): How to do the 90/90 hip stretch: setup, what you should feel, how to adjust it to your own hips, and how to load it so the range becomes usable.
- [Hip Internal Rotation: The Range Most People Lose](/hip-internal-rotation-the-range-most-people-lose): Most people lose hip internal rotation without noticing. Here's why it matters, how to test it, and how to build the range back safely.
- [Mobility as Capacity, Not a Category](/mobility-as-capacity-not-a-category): Mobility isn’t a category of exercise. It’s capacity. Learn why real mobility means controlling your ranges—not just stretching more.
- [Why Mobility Doesn't Stick](/why-mobility-doesnt-stick): New range that disappears by your next session isn't a lack of effort, it's an incomplete signal. Here's what actually makes mobility gains stick.

### Ankles (`ankles`)

File: `src/content/topic/ankles.md` · Page: `/topics/ankles` · 1 post (page is hidden from Google until it has 2)

Current one-line description: Ankle dorsiflexion and the restrictions that show up in squats and gait.

Posts:

- [Ankle Dorsiflexion: What Restricts It, How to Test It, and How to Rebuild](/ankle-dorsiflexion-what-restricts-it-how-to-test-it-and-rebuild-it): Ankle dorsiflexion isn't one problem. It can come from the capsule, the mortise, either calf muscle, or a bony block, and each one needs a different fix.

### Spine & Core (`spine`)

File: `src/content/topic/spine.md` · Page: `/topics/spine` · 2 posts

Current one-line description: Trunk and spinal mobility, bracing, and training the spine to move as well as resist.

Posts:

- [Posture: An Ongoing Fight Against Gravity](/posture-an-ongoing-fight-against-gravity): Posture isn’t about perfection; it's about versatility. Learn why strength and movement matter more than rigid alignment.
- [The Trunk Isn't Always a Brace](/the-trunk-isnt-always-a-brace): Bracing has its place, but the trunk is built to flex, extend, rotate, and side-bend. Why core training should teach the spine to move as well as resist.

### Posture (`posture`)

File: `src/content/topic/posture.md` · Page: `/topics/posture` · 1 post (page is hidden from Google until it has 2)

Current one-line description: Posture as versatility rather than alignment, and what actually changes it.

Posts:

- [Posture: An Ongoing Fight Against Gravity](/posture-an-ongoing-fight-against-gravity): Posture isn’t about perfection; it's about versatility. Learn why strength and movement matter more than rigid alignment.

### FRC & Kinstretch (`frc-and-kinstretch`)

File: `src/content/topic/frc-and-kinstretch.md` · Page: `/topics/frc-and-kinstretch` · 2 posts

Current one-line description: Functional Range Conditioning tools like CARs, PAILs, and RAILs, and where they fit.

Posts:

- [What CARs Are Actually For](/what-cars-are-actually-for): CARs don't build new range, they maintain what you have. What controlled articular rotations actually measure, and where the hype outruns the evidence.
- [When the Method Becomes the Answer](/when-the-method-becomes-the-answer): PRI, FRC, McGill, and 90/90 all have real value. The trouble starts when any one of them gets sold as the answer. A coach's view on methods, certainty, and why assessment has to come first.

### Pain & Hypermobility (`pain-and-hypermobility`)

File: `src/content/topic/pain-and-hypermobility.md` · Page: `/topics/pain-and-hypermobility` · 1 post (page is hidden from Google until it has 2)

Current one-line description: When more range is the wrong goal, and the red flags that stretching isn't helping.

Posts:

- [When Stretching Makes Pain Worse: How to Spot the Red Flags](/when-stretching-makes-pain-worse-how-to-spot-the-red-flags): Can stretching make pain worse? Learn the red flags of hypermobility and why pain keeps returning when you chase more range.

### Coaching (`coaching`)

File: `src/content/topic/coaching.md` · Page: `/topics/coaching` · 3 posts

Current one-line description: Written for coaches: language, methods, and how to think about clients.

Posts:

- [The Trunk Isn't Always a Brace](/the-trunk-isnt-always-a-brace): Bracing has its place, but the trunk is built to flex, extend, rotate, and side-bend. Why core training should teach the spine to move as well as resist.
- [What We Mean When We Say Tight](/what-we-mean-when-we-say-tight): Written for coaches: tight, passive, activation, and weak are some of the least precise words in mobility, and each one quietly carries a theory about what's wrong. A case for getting the language right.
- [When the Method Becomes the Answer](/when-the-method-becomes-the-answer): PRI, FRC, McGill, and 90/90 all have real value. The trouble starts when any one of them gets sold as the answer. A coach's view on methods, certainty, and why assessment has to come first.

### Expert Roundups (`expert-roundups`)

File: `src/content/topic/expert-roundups.md` · Page: `/topics/expert-roundups` · 2 posts

Current one-line description: Coaches and clinicians answer one question each.

Posts:

- [How Do You Structure Mobility Into Your Workout Routine?](/how-do-you-structure-mobility-into-your-workout-routine): What's the best way to structure your mobility routine? We asked the pros; here is what they had to say.
- [What Does Mobility Mean? We Asked the Pros](/what-does-mobility-mean-we-asked-the-pros): Mobility means control, independence, safety, and adaptability. Coaches and clinicians worldwide share what mobility really is.

