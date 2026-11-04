// The site's topic tags. This list is the only source of valid tags: the post
// schema rejects anything not named here, so a typo fails the build instead of
// quietly creating a one-post topic page. To add a topic, add it here (and to
// KNOWN_TAGS in .github/scripts/publish_from_drive.py so queued posts can use it).
export const TOPICS = {
  fundamentals: {
    label: "Fundamentals",
    description: "What mobility is, how it differs from flexibility, and the vocabulary the rest of the site uses.",
  },
  stretching: {
    label: "Stretching",
    description: "How stretching changes range, how much it takes, and where it helps or backfires.",
  },
  isometrics: {
    label: "Isometrics",
    description: "End-range isometrics and loaded holds: how tension turns passive range into usable range.",
  },
  assessment: {
    label: "Assessment",
    description: "Testing a joint before training it: what to look for and how to read what you find.",
  },
  programming: {
    label: "Programming",
    description: "Where mobility work fits in a training week, how often to do it, and how to make the gains stick.",
  },
  hips: {
    label: "Hips",
    description: "Hip rotation, hip flexors, and the positions most people lose first.",
  },
  ankles: {
    label: "Ankles",
    description: "Ankle dorsiflexion and the restrictions that show up in squats and gait.",
  },
  spine: {
    label: "Spine & Core",
    description: "Trunk and spinal mobility, bracing, and training the spine to move as well as resist.",
  },
  posture: {
    label: "Posture",
    description: "Posture as versatility rather than alignment, and what actually changes it.",
  },
  "frc-and-kinstretch": {
    label: "FRC & Kinstretch",
    description: "Functional Range Conditioning tools like CARs, PAILs, and RAILs, and where they fit.",
  },
  "pain-and-hypermobility": {
    label: "Pain & Hypermobility",
    description: "When more range is the wrong goal, and the red flags that stretching isn't helping.",
  },
  coaching: {
    label: "Coaching",
    description: "Written for coaches: language, methods, and how to think about clients.",
  },
  "expert-roundups": {
    label: "Expert Roundups",
    description: "Coaches and clinicians answer one question each.",
  },
} as const;

export type TopicSlug = keyof typeof TOPICS;
export const TOPIC_SLUGS = Object.keys(TOPICS) as [TopicSlug, ...TopicSlug[]];

// Topic pages with fewer posts than this are noindexed: a one-post archive is
// thin content to a search engine, but it's still useful to a reader.
export const MIN_INDEXABLE_TOPIC_POSTS = 2;
