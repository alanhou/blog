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

A local Codex automation checks for AI/ML research papers every 6 hours from this repository checkout, generates articles using the installed `alanhou-paper` skill, validates them, and then commits and pushes the results to GitHub. The GitHub Actions paper workflow is an optional manual fallback; it has no scheduled trigger.

1. **Fetch** — Queries the arXiv API for recent papers in cs.AI, cs.LG, cs.CL, cs.CV
2. **Select** — Curates new, uncovered papers by novelty, practical impact, and available evidence
3. **Generate** — Reads the original arXiv HTML (PDF text fallback) and produces bilingual MDX stories using the `alanhou-paper` structure, with evidence and scope requirements adapted from current `ljg-paper`
4. **Visualize** — Generates suitable covers and, when useful and available, Manim-based diagrams or animations
5. **Validate and publish** — Checks generated MDX and the site build locally, commits only the run's articles and assets, and pushes to GitHub to trigger deployment

The paper analysis prompt adapts `alanhou-paper`, derived from [ljg-paper](https://github.com/lijigang/ljg-skills/tree/master/skills/ljg-paper) by [@lijigang](https://github.com/lijigang). It keeps the local skill's accessible narrative while requiring source-backed claims, labeled illustrative examples, and explicit limits. See [the comparison and selected improvements](docs/PAPER_WORKFLOW_REVIEW.md). Articles use Problem / Explanation / Core Concepts / Insight / Critical Reading / What You Can Use, with the local skill's six Chinese section names. Text extraction does not inspect figures; any excerpting is disclosed. If neither original format is readable, the paper is retried rather than analyzed from the abstract alone.

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
├── arxiv.yml          # Manual paper pipeline fallback; no cron trigger
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
pip install requests openai 'anthropic<1.0' manim pyyaml beautifulsoup4 pypdf

export LLM_API_KEY="your-key"
export LLM_BASE_URL="https://api.example.com/v1"  # Optional for Claude, required for OpenAI-compatible APIs
export LLM_MODEL_NAME="claude-sonnet-4-6"  # or "gpt-4", etc.

python scripts/fetch_arxiv.py
```

The pipeline supports both:
- **Claude** (Anthropic API): Set `LLM_MODEL_NAME` to any model starting with "claude" (e.g., `claude-sonnet-4-6`, `claude-opus-4-6`). `LLM_BASE_URL` is optional.
- **OpenAI-compatible APIs**: Set `LLM_MODEL_NAME` to your model name and `LLM_BASE_URL` to your endpoint (e.g., `https://api.openai.com/v1`).

## Acknowledgments

- [ljg-paper](https://github.com/lijigang/ljg-skills/tree/master/skills/ljg-paper) by [@lijigang](https://github.com/lijigang) — The source-grounded explanation methodology behind `alanhou-paper` and this blog's adapted article prompt.
- [Astro](https://astro.build) — Static site framework.
- [Manim](https://www.manim.community) — Mathematical animation engine used for paper visualizations.

## License

MIT
