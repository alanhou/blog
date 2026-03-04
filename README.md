# Alan Hou's Blog

A bilingual (English/Chinese) technical blog built with [Astro](https://astro.build), featuring automated arXiv paper analysis, course series, developer tools, and AI prompt collections.

**Live site**: [alanhou.org](https://alanhou.org)

## Features

### Bilingual Content System

Blog posts use `:::en` / `:::zh` markdown directives to define language blocks. A client-side toggle lets readers switch between **Both** (side-by-side), **English only**, or **Chinese only** views. Preference is saved to localStorage.

```mdx
<BilingualContent>

:::en
English content here.
:::

:::zh
中文内容在这里。
:::

</BilingualContent>
```

### Automated arXiv Paper Pipeline

A GitHub Actions workflow runs every 8 hours to discover, curate, and publish AI/ML research papers:

1. **Fetch** — Queries the arXiv API for recent papers in cs.AI, cs.LG, cs.CL, cs.CV
2. **Select** — An LLM picks the ~5 most interesting papers by novelty and impact
3. **Generate** — Produces structured bilingual MDX posts with sections like Gap, Core Mechanism, Framework Shift, and Expert Assessment
4. **Visualize** — Generates Manim-based hero images and concept animation GIFs
5. **Publish** — Commits new posts and triggers a deploy

The paper analysis prompt is inspired by [ljg-skill-paper](https://github.com/lijigang/ljg-skill-paper) by [@lijigang](https://github.com/lijigang), a Claude Code skill that provides a structured multi-stage pipeline for academic paper analysis (Split, Squeeze, Plain, Feynman, Napkin Sketch, Advisor Review).

### Social Cover Generation

During build, [Satori](https://github.com/vercel/satori) generates 1200x630 OG image cards for each arXiv post, with tag-based color palettes and bilingual titles. Pre-existing Manim hero images take priority.

### Course Series

10+ structured series (Odoo, Python, Hung-yi Lee ML, Karpathy LLM, etc.) with in-series navigation.

### Developer Tools

Built-in tools at `/tools`: password generator, Base64 image converter, QR code generator, JSON viewer, Unix timestamp converter, and more.

### Search & Sharing

Full-text search (Cmd+K) with a pre-built JSON index. Social share buttons for X, LinkedIn, Facebook, Reddit, Hacker News, and WeChat (with QR code).

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [Astro 4](https://astro.build) with MDX |
| Math | remark-math + rehype-katex |
| Directives | remark-directive + custom remark-bilingual plugin |
| OG Images | Satori + @resvg/resvg-js |
| Visuals | Manim (Python) for diagrams and animations |
| Deploy | GitHub Pages via GitHub Actions |
| LLM | OpenAI-compatible API (configurable) |

## Project Structure

```
src/
├── components/        # BilingualContent, Header, SearchModal, ShareButtons, etc.
├── config/            # Series metadata
├── content/
│   ├── blog/          # MDX/MD posts (1000+ including 250+ arXiv papers)
│   ├── prompts/       # AI prompt collection
│   └── tools/         # Tool definitions (JSON)
├── layouts/           # Base layout with SEO meta tags
├── pages/             # Routes: blog, tools, prompts, search, RSS
├── plugins/           # remark-bilingual.mjs
└── styles/            # CSS variables, light/dark theme
scripts/
├── fetch_arxiv.py     # arXiv discovery + LLM generation pipeline
├── generate-covers.mjs # OG image generation
├── render_manim.py    # Manim scene rendering + validation
└── manim_prompts.py   # LLM prompts for visual generation
.github/workflows/
├── arxiv.yml          # Scheduled paper fetch (every 8h)
└── deploy.yml         # Build & deploy on push
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.10+ (for arXiv pipeline only)

### Development

```bash
npm install
npm run dev
```

### Build

```bash
npm run build    # generates OG covers, then builds static site
npm run preview  # preview the built site locally
```

### arXiv Pipeline (optional)

```bash
pip install requests openai manim

export LLM_API_KEY="your-key"
export LLM_BASE_URL="https://api.example.com/v1"
export LLM_MODEL_NAME="your-model"

python scripts/fetch_arxiv.py
```

The pipeline works with any OpenAI-compatible API endpoint.

## Acknowledgments

- [ljg-skill-paper](https://github.com/lijigang/ljg-skill-paper) by [@lijigang](https://github.com/lijigang) — The structured paper analysis methodology (Feynman explanation, napkin sketch comparison, advisor review) inspired the arXiv blog post generation prompt.
- [Astro](https://astro.build) — Static site framework.
- [Manim](https://www.manim.community) — Mathematical animation engine used for paper visualizations.

## License

MIT
