import { defineCollection, z } from 'astro:content';

const bilingualText = z.object({
en: z.string().optional(),
zh: z.string().optional(),
});

const blog = defineCollection({
type: 'content',
schema: z.object({
  title: bilingualText,
  description: bilingualText.optional(),
  date: z.date(),
  tags: z.array(z.string()).optional(),
  image: z.string().optional(),
  series: z.string().optional(),
  seriesOrder: z.number().optional(),
}),
});

const prompts = defineCollection({
type: 'content',
schema: z.object({
  title: bilingualText,
  description: bilingualText.optional(),
  category: z.string(),
  tags: z.array(z.string()).optional(),
}),
});

const tools = defineCollection({
type: 'data',
schema: z.object({
  title: bilingualText,
  description: bilingualText.optional(),
  url: z.string(),
  pricing: z.enum(['free', 'freemium', 'paid']),
  category: z.string(),
}),
});

export const collections = { blog, prompts, tools };
