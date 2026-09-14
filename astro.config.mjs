import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel";

export default defineConfig({
  site: "https://www.themobilityblog.com",
  output: "static",
  trailingSlash: "never",
  adapter: vercel(),
  integrations: [tailwind({ applyBaseStyles: false }), mdx(), sitemap()],
});
