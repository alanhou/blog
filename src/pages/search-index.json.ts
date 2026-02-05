import { getCollection } from 'astro:content';

export async function GET() {
const posts = await getCollection('blog');

const searchIndex = posts.map(post => ({
  title: post.data.title.en,
  titleZh: post.data.title.zh,
  url: `/blog/${post.slug}`,
  excerpt: post.data.description?.en || post.data.description?.zh || '',
}));

return new Response(JSON.stringify(searchIndex), {
  headers: { 'Content-Type': 'application/json' },
});
}
