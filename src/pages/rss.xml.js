import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context) {
  const posts = await getCollection("post", ({ data }) => data.published);
  return rss({
    title: "The Mobility Blog",
    description:
      "We're a collaborative community of mobility coaches, helping people move better one joint at a time.",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/${post.id}`,
    })),
  });
}
