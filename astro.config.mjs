import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkDirective from 'remark-directive';
import { remarkBilingualDirective } from './src/plugins/remark-bilingual.mjs';

export default defineConfig({
  site: 'https://alanhou.org',
  output: 'static',
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath, remarkDirective, remarkBilingualDirective],
    rehypePlugins: [rehypeKatex],
  },
});
