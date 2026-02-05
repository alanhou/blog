import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context: any) {
const posts = await getCollection('blog');
return rss({
  title: "Alan Hou's Blog",
  description: '用行动赢得尊重 - Coding, AI and Technology',
  site: context.site || 'https://alanhou.org',
  items: posts.map(post => ({
    title: post.data.title.en || post.data.title.zh || '',
    pubDate: post.data.date,
    link: `/blog/${post.slug}/`,
  })),
});
}
