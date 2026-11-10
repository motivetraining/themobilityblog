// Minutes to read a post, from its Markdown source. 230 words a minute is a
// typical pace for this kind of prose; links and Markdown syntax are close
// enough to noise at post length that they aren't stripped.
export function wordCount(markdown: string | undefined): number {
  return (markdown ?? "").split(/\s+/).filter(Boolean).length;
}

export function readingMinutes(markdown: string | undefined): number {
  return Math.max(1, Math.round(wordCount(markdown) / 230));
}

export const formatDate = (d: Date) =>
  d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });

export const formatShortDate = (d: Date) =>
  d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
