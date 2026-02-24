import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join, basename } from 'path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';

const ARXIV_PLACEHOLDER = 'https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-fb.png';
const VISUALS_DIR = 'public/arxiv-visuals';
const BLOG_DIR = 'src/content/blog';

const PALETTES = [
  { tags: ['cs.cl', 'nlp'], from: '#3B82F6', to: '#6366F1' },
  { tags: ['cs.cv', 'vision', 'image'], from: '#8B5CF6', to: '#EC4899' },
  { tags: ['cs.lg', 'machine-learning'], from: '#14B8A6', to: '#10B981' },
  { tags: ['cs.ai', 'ai'], from: '#F97316', to: '#F59E0B' },
  { tags: ['cs.ro', 'robotics', 'robot'], from: '#64748B', to: '#06B6D4' },
  { tags: ['reinforcement-learning', 'rl', 'rlhf', 'grpo'], from: '#EF4444', to: '#F97316' },
  { tags: ['efficiency', 'lora', 'fine-tuning', 'quantization'], from: '#22C55E', to: '#84CC16' },
  { tags: ['transformer', 'attention'], from: '#6366F1', to: '#8B5CF6' },
];
const DEFAULT_PALETTE = { from: '#2CA64B', to: '#3d7d3b' };

function pickPalette(tags) {
  const lower = tags.map(t => t.toLowerCase());
  for (const p of PALETTES) {
    if (p.tags.some(t => lower.includes(t))) return p;
  }
  return DEFAULT_PALETTE;
}


function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const fm = match[1];
  const titleEnMatch = fm.match(/title:\s*\n\s+en:\s*"(.+?)"/);
  const titleZhMatch = fm.match(/zh:\s*"(.+?)"/);
  const tagsMatch = fm.match(/tags:\s*\[([^\]]+)\]/);
  const imageMatch = fm.match(/image:\s*"?(.+?)"?\s*$/m);
  return {
    titleEn: titleEnMatch?.[1] || '',
    titleZh: titleZhMatch?.[1] || '',
    tags: tagsMatch ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '')) : [],
    image: imageMatch?.[1] || '',
    raw: match[0],
  };
}

async function generateCover(titleEn, titleZh, tags, slug, fonts) {
  const palette = pickPalette(tags);
  const displayTags = tags.filter(t => t !== 'arxiv').slice(0, 3);

  const svg = await satori(
    {
      type: 'div',
      props: {
        style: {
          width: '1200px',
          height: '630px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '60px',
          fontFamily: 'Inter, Noto Sans SC',
          color: 'white',
          backgroundImage: `linear-gradient(135deg, ${palette.from}, ${palette.to})`,
        },
        children: [
          {
            type: 'div',
            props: {
              style: { display: 'flex', flexDirection: 'column', gap: '12px', maxWidth: '1000px' },
              children: [
                {
                  type: 'div',
                  props: {
                    style: { fontSize: '18px', opacity: 0.8, letterSpacing: '2px' },
                    children: 'ARXIV PAPER',
                  },
                },
                {
                  type: 'div',
                  props: {
                    style: { fontSize: '40px', fontWeight: 700, lineHeight: 1.2 },
                    children: titleEn,
                  },
                },
                {
                  type: 'div',
                  props: {
                    style: { fontSize: '28px', fontWeight: 700, lineHeight: 1.3, opacity: 0.85 },
                    children: titleZh,
                  },
                },
              ],
            },
          },
          {
            type: 'div',
            props: {
              style: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' },
              children: [
                {
                  type: 'div',
                  props: {
                    style: { display: 'flex', gap: '10px' },
                    children: displayTags.map(tag => ({
                      type: 'div',
                      props: {
                        style: {
                          background: 'rgba(255,255,255,0.2)',
                          borderRadius: '20px',
                          padding: '8px 18px',
                          fontSize: '18px',
                        },
                        children: tag,
                      },
                    })),
                  },
                },
                {
                  type: 'div',
                  props: {
                    style: { fontSize: '20px', opacity: 0.7 },
                    children: 'alanhou.org',
                  },
                },
              ],
            },
          },
        ],
      },
    },
    { width: 1200, height: 630, fonts }
  );

  const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } });
  return resvg.render().asPng();
}

async function main() {
  const fonts = [
    { name: 'Inter', data: readFileSync(new URL('./fonts/Inter-Bold.ttf', import.meta.url)), weight: 700, style: 'normal' },
    { name: 'Noto Sans SC', data: readFileSync(new URL('./fonts/NotoSansSC-Bold.ttf', import.meta.url)), weight: 700, style: 'normal' },
  ];

  if (!existsSync(VISUALS_DIR)) mkdirSync(VISUALS_DIR, { recursive: true });

  const files = readdirSync(BLOG_DIR)
    .filter(f => f.startsWith('arxiv-') && f.endsWith('.mdx'))
    .map(f => join(BLOG_DIR, f));

  let generated = 0, skipped = 0;

  for (const file of files) {
    const content = readFileSync(file, 'utf-8');
    const fm = parseFrontmatter(content);
    if (!fm) { skipped++; continue; }

    const slug = basename(file, '.mdx');
    const outPath = join(VISUALS_DIR, `${slug}.png`);
    const localImage = `/arxiv-visuals/${slug}.png`;

    // Skip if image is not the arxiv placeholder and not our generated cover
    if (fm.image !== ARXIV_PLACEHOLDER && fm.image !== localImage) { skipped++; continue; }

    // Skip if cover already generated (use --force to regenerate)
    if (existsSync(outPath) && !process.argv.includes('--force')) { skipped++; continue; }

    // Skip if Manim hero exists
    const manimHero = join(VISUALS_DIR, slug, 'HeroScene.png');
    if (existsSync(manimHero)) { skipped++; continue; }

    const png = await generateCover(fm.titleEn, fm.titleZh, fm.tags, slug, fonts);
    writeFileSync(outPath, png);

    // Patch frontmatter if still using placeholder
    if (fm.image === ARXIV_PLACEHOLDER) {
      const patched = content.replace(
        /image:\s*"?https:\/\/arxiv\.org\/static\/browse\/0\.3\.4\/images\/arxiv-logo-fb\.png"?/,
        `image: "${localImage}"`
      );
      writeFileSync(file, patched);
    }

    generated++;
    if (generated % 20 === 0) console.log(`  Generated ${generated} covers...`);
  }

  console.log(`Done: ${generated} generated, ${skipped} skipped (${files.length} total)`);
}

main().catch(err => { console.error(err); process.exit(1); });
