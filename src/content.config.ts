import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const post = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/post" }),
  schema: z.object({
    title: z.string(),
    metaTitle: z.string().optional(),
    description: z.string(),
    date: z.coerce.date(),
    dateModified: z.coerce.date().optional(),
    featuredImage: z.string().optional(),
    categories: z.array(z.string()).default([]),
    published: z.boolean().default(true),
  }),
});

const page = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/page" }),
  schema: z.object({
    title: z.string(),
  }),
});

export const collections = { post, page };
