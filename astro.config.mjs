import { defineConfig } from "astro/config";
import { fileURLToPath } from "node:url";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel";
import * as pagefind from "pagefind";

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
  adapter: vercel(),
  integrations: [tailwind({ applyBaseStyles: false }), mdx(), sitemap(), searchIndex()],
});
