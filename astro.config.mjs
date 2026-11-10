import { defineConfig } from "astro/config";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel";
import * as pagefind from "pagefind";
import { rehypeMotiveUtm } from "./src/lib/utm.mjs";
import { rehypeContent } from "./src/lib/rehype-content.mjs";

// The sitemap reads each page's own built HTML, so it can't drift from what
// the page says about itself:
// - pages marked noindex (search, 404, one-post topic pages) are left out,
//   since listing a URL that asks not to be indexed sends mixed signals;
// - lastmod comes from the post's article:modified_time, so search engines
//   can tell which posts were revised and are worth recrawling.
// The sitemap integration runs before the Vercel adapter moves dist/.
function builtHtml(url) {
  const path = new URL(url).pathname.replace(/\/$/, "");
  const file = `dist${path || ""}/index.html`;
  return existsSync(file) ? readFileSync(file, "utf8") : existsSync(`dist${path}.html`) ? readFileSync(`dist${path}.html`, "utf8") : "";
}

const sitemapOptions = {
  filter: (page) => !/<meta name="robots" content="noindex"/.test(builtHtml(page)),
  serialize: (item) => {
    const modified = builtHtml(item.url).match(/<meta property="article:modified_time" content="([^"]+)"/)?.[1];
    if (modified) item.lastmod = modified;
    return item;
  },
};

// Builds the site search index (served from /pagefind) once the HTML exists.
// Only post pages are indexed: their <article> carries data-pagefind-body.
// This runs before the Vercel adapter copies dist/ into .vercel/output/static,
// so the index ships with the rest of the static files.
function searchIndex() {
  return {
    name: "pagefind-search-index",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const site = fileURLToPath(dir);
        const { index } = await pagefind.createIndex();
        const { errors } = await index.addDirectory({ path: site });
        if (errors.length) throw new Error(`Search indexing failed: ${errors.join("; ")}`);
        await index.writeFiles({ outputPath: `${site}/pagefind` });
        logger.info("Search index written to /pagefind");
        await pagefind.close();
      },
    },
  };
}

export default defineConfig({
  site: "https://www.themobilityblog.com",
  output: "static",
  trailingSlash: "never",
  // Featured images go through Vercel's image optimizer in production, which
  // serves each one as AVIF/WebP at the width the layout needs instead of the
  // full 1600px JPG. Locally (dev and preview) Astro uses sharp instead.
  adapter: vercel({
    imageService: true,
    imagesConfig: {
      sizes: [400, 640, 800, 1200, 1600],
      formats: ["image/avif", "image/webp"],
      minimumCacheTTL: 2592000,
    },
  }),
  image: {
    responsiveStyles: false,
  },
  // Starts fetching a page when a link is hovered or touched, so the click
  // that follows lands on HTML that's already downloaded.
  prefetch: {
    prefetchAll: true,
    defaultStrategy: "hover",
  },
  markdown: {
    rehypePlugins: [rehypeMotiveUtm, rehypeContent],
  },
  integrations: [tailwind({ applyBaseStyles: false }), mdx(), sitemap(sitemapOptions), searchIndex()],
});
