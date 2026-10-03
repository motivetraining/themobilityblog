import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

// llms.txt (https://llmstxt.org): a plain-Markdown index of the site for AI
// tools. Built from the post collection, so every published post appears here
// automatically, newest first.
export const GET: APIRoute = async ({ site }) => {
  const base = site!.href.replace(/\/$/, "");
  const posts = (await getCollection("post", ({ data }) => data.published)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
  );

  const line = (title: string, path: string, description: string) =>
    `- [${title}](${base}/${path}): ${description}`;

  const body = [
    "# The Mobility Blog",
    "",
    "> Practical, evidence-informed writing on mobility training, stretching, and joint health, mostly by Brian Murray, a mobility coach with sixteen years of experience who founded Motive Training in Austin, TX. Posts explain why methods work, cite their sources, and say plainly where the evidence is thin.",
    "",
    "Key ideas the site argues throughout: mobility is the range a joint can reach and control on its own, as distinct from passive flexibility; range needs load, intent, and frequency to last; controlled articular rotations (CARs) assess and maintain range rather than build it; end-range isometrics, PAILs and RAILs, and resistance training are how range becomes usable.",
    "",
    "## Start Here",
    "",
    line("What Is Mobility?", "what-is-mobility", "The site's definition of mobility, how it differs from flexibility, how to test it, and how it's trained. Links to every other topic."),
    "",
    "## Posts",
    "",
    ...posts
      .filter((post) => post.id !== "what-is-mobility")
      .map((post) => line(post.data.title, post.id, post.data.description)),
    "",
    "## About",
    "",
    line("About Brian Murray", "about", "The author's background, credentials, and the site's editorial standards."),
    line("Write With Us", "write-with-us", "How coaches and clinicians can submit guest posts."),
    "",
  ].join("\n");

  return new Response(body, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
};
