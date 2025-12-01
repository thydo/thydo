import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Each section has a header (00-*.md) and items (01-*.md, 02-*.md, etc.)
// Schema is permissive to allow varied frontmatter across sections
const resumeSections = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./resume/sections" }),
  schema: z.record(z.any()), // Fully flexible schema
});

export const collections = {
  resume: resumeSections,
};
