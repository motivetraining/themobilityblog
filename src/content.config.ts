import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";
import { TOPIC_SLUGS } from "./lib/topics";

const post = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/post" }),
  schema: z.object({
    // Titles are headings: Title Case, and never ending with a period.
    title: z.string().refine((t) => !t.trim().endsWith("."), "title must not end with a period"),
    metaTitle: z
      .string()
      .refine((t) => !t.trim().endsWith("."), "metaTitle must not end with a period")
      .optional(),
    description: z.string(),
    date: z.coerce.date(),
    dateModified: z.coerce.date().optional(),
    featuredImage: z.string().optional(),
    imageAlt: z.string().optional(),
    author: z.string().default("Brian Murray"),
    authorUrl: z.string().url().optional(),
    categories: z.array(z.string()).default([]),
    // Topic tags, by slug. Must be one of the topics in src/lib/topics.ts.
    tags: z.array(z.enum(TOPIC_SLUGS)).default([]),
    published: z.boolean().default(true),
  }),
});

const page = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/page" }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
  }),
});

// Optional intro copy for topic pages: src/content/topic/{topic-slug}.md.
const topic = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/topic" }),
  schema: z.object({}),
});

export const collections = { post, page, topic };
