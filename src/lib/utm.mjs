// UTM tagging for links to Motive Training (movewithpurpose.com), so its
// analytics can attribute visits and sign-ups to this blog. Those pages carry
// canonical tags, so the tagged URLs don't create duplicates in search.
//
// utm_source is always "themobilityblog"; utm_medium says where on the blog
// the link sits (nav, footer, post); utm_content names the post or page.
// Existing utm_* parameters on a link are left alone.

const MOTIVE_HOST = /(^|\.)movewithpurpose\.com$/;
export const UTM_SOURCE = "themobilityblog";

export function withUtm(href, { medium, content, campaign = "blog" }) {
  let url;
  try {
    url = new URL(href);
  } catch {
    return href;
  }
  if (!MOTIVE_HOST.test(url.hostname) || url.searchParams.has("utm_source")) return href;
  url.searchParams.set("utm_source", UTM_SOURCE);
  url.searchParams.set("utm_medium", medium);
  url.searchParams.set("utm_campaign", campaign);
  if (content) url.searchParams.set("utm_content", content);
  return url.href;
}

// Rehype plugin: tags movewithpurpose.com links in post and page Markdown with
// utm_medium=post (or page) and utm_content set to the file's slug.
export function rehypeMotiveUtm() {
  return (tree, file) => {
    const path = file.path ?? file.history?.[0] ?? "";
    const slug = path.split("/").pop()?.replace(/\.mdx?$/, "");
    const medium = path.includes("/content/page/") ? "page" : "post";
    const walk = (node) => {
      if (node.type === "element" && node.tagName === "a" && typeof node.properties?.href === "string") {
        node.properties.href = withUtm(node.properties.href, { medium, content: slug });
      }
      node.children?.forEach(walk);
    };
    walk(tree);
  };
}
