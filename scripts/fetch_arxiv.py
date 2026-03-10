#!/usr/bin/env python3
"""Fetch recent arxiv papers, select interesting ones via LLM, and generate bilingual MDX blog posts."""

import glob
import os
import re
import sys
import traceback
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import time

import requests
from openai import OpenAI

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from manim_prompts import (
    CONCEPT_GIF_SYSTEM,
    CONCEPT_GIF_USER,
    HERO_IMAGE_SYSTEM,
    HERO_IMAGE_USER,
)
from render_manim import VISUALS_DIR, render_scene, validate_scene_code

BLOG_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "blog"
LAST_FETCH_FILE = Path(__file__).resolve().parent / ".last_fetch"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
ARXIV_IMAGE = "https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-fb.png"


def get_llm_client():
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL")
    model = os.environ.get("LLM_MODEL_NAME")
    provider = os.environ.get("LLM_PROVIDER", "").lower()

    if not all([api_key, model]):
        print("Error: LLM_API_KEY and LLM_MODEL_NAME must be set")
        sys.exit(1)

    # Auto-detect provider: explicit env var > base_url implies openai > model name
    if not provider:
        if base_url:
            provider = "openai"
        elif model.startswith("claude"):
            provider = "anthropic"
        else:
            provider = "openai"

    if provider == "anthropic":
        if not ANTHROPIC_AVAILABLE:
            print("Error: anthropic package not installed. Run: pip install anthropic")
            sys.exit(1)
        client = Anthropic(api_key=api_key, base_url=base_url) if base_url else Anthropic(api_key=api_key)
        return client, model, "anthropic"
    else:
        if not base_url:
            print("Error: LLM_BASE_URL must be set for OpenAI-compatible APIs")
            sys.exit(1)
        return OpenAI(api_key=api_key, base_url=base_url), model, "openai"


def load_last_fetch():
    if LAST_FETCH_FILE.exists():
        text = LAST_FETCH_FILE.read_text().strip()
        if text:
            return datetime.fromisoformat(text)
    return datetime.now(timezone.utc) - timedelta(hours=24)


def save_last_fetch():
    LAST_FETCH_FILE.write_text(datetime.now(timezone.utc).isoformat())


def fetch_recent_papers(categories, max_results=20):
    """Query arxiv API for recent papers in given categories."""
    cat_query = " OR ".join(f"cat:{c}" for c in categories)
    query = f"({cat_query})"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # Retry logic for rate limiting
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            resp = requests.get(ARXIV_API_URL, params=params, timeout=30)
            resp.raise_for_status()
            break  # Success, exit retry loop
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    print(f"Rate limited by arxiv API. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Arxiv API rate limit exceeded.")
                    raise
            else:
                raise
        except Exception as e:
            print(f"Error fetching papers: {e}")
            raise

    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(resp.text)
    papers = []
    for entry in root.findall("atom:entry", ns):
        arxiv_id_url = entry.find("atom:id", ns).text.strip()
        arxiv_id = arxiv_id_url.split("/abs/")[-1]
        # Strip version suffix (e.g. v1, v2)
        arxiv_id = re.sub(r"v\d+$", "", arxiv_id)
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        title = re.sub(r"\s+", " ", title)
        summary = entry.find("atom:summary", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        categories_found = [c.get("term") for c in entry.findall("atom:category", ns)]
        published = entry.find("atom:published", ns).text.strip()
        papers.append({
            "id": arxiv_id,
            "title": title,
            "summary": summary,
            "authors": authors,
            "categories": categories_found,
            "published": published,
        })
    return papers


def get_existing_arxiv_ids():
    """Scan existing MDX files for arxiv paper IDs."""
    ids = set()
    for filepath in glob.glob(str(BLOG_DIR / "arxiv-*.mdx")):
        with open(filepath, "r") as f:
            content = f.read()
        # Match patterns like [2602.04998] or [arXiv:2106.09685]
        for m in re.finditer(r"arxiv\.org/abs/([\d.]+)", content):
            ids.add(m.group(1))
    return ids


def slugify(title):
    """Generate a filename slug from paper title."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    # Truncate to reasonable length
    parts = slug.split("-")
    if len(parts) > 6:
        slug = "-".join(parts[:6])
    return slug


def call_llm(client, model, provider, messages, temperature=0.5, max_tokens=4096, retries=3):
    """Unified LLM call supporting both Anthropic and OpenAI APIs with retry logic."""
    for attempt in range(retries):
        try:
            if provider == "anthropic":
                response = client.messages.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.content[0].text
            else:  # openai
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                # Debug: check response type
                if isinstance(response, str):
                    print(f"  WARNING: OpenAI client returned string instead of object")
                    return response
                return response.choices[0].message.content
        except Exception as e:
            err_str = str(e)
            # Retry on transient errors (timeouts, server errors, rate limits)
            is_transient = any(code in err_str for code in ["524", "529", "500", "502", "503", "429", "overloaded"])
            if is_transient and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  LLM call failed (attempt {attempt + 1}/{retries}): {err_str[:120]}")
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise


def select_papers(client, model, provider, papers, count=5):
    """Use LLM to select the most interesting papers."""
    paper_list = "\n\n".join(
        f"[{i+1}] ID: {p['id']}\nTitle: {p['title']}\nAbstract: {p['summary'][:500]}"
        for i, p in enumerate(papers)
    )
    prompt = f"""You are an AI research curator. From the following {len(papers)} recent arxiv papers, select the {count} most interesting and impactful ones for a technical blog audience.

Consider: novelty, practical impact, broad interest, and technical depth.

Papers:
{paper_list}

Reply with ONLY the numbers of your selected papers, one per line. Example:
1
5
7"""

    content = call_llm(
        client, model, provider,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024
    )
    if not content:
        print(f"Warning: LLM returned empty response for paper selection, falling back to first {count}")
        return papers[:count]
    text = content.strip()
    selected_indices = []
    for line in text.split("\n"):
        line = line.strip().rstrip(".")
        nums = re.findall(r"\d+", line)
        if nums:
            idx = int(nums[0]) - 1
            if 0 <= idx < len(papers):
                selected_indices.append(idx)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for idx in selected_indices:
        if idx not in seen:
            seen.add(idx)
            unique.append(idx)
    return [papers[i] for i in unique[:count]]


def generate_blog_post(client, model, provider, paper):
    """Use LLM to generate a full bilingual MDX blog post."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    authors_str = ", ".join(paper["authors"][:10])
    cats_str = ", ".join(paper["categories"][:5])

    prompt = f"""You are reading an academic paper and explaining it to a smart colleague over coffee. Your goal: help them understand what gap this paper fills, what's actually new, and whether it's worth their attention.

Paper ID: {paper['id']}
Title: {paper['title']}
Authors: {authors_str}
Categories: {cats_str}
Abstract: {paper['summary']}

Output a bilingual MDX blog post following this EXACT structure:

---
title:
  en: "[English title based on paper]"
  zh: "[Chinese title]"
description:
  en: "[1-2 sentence English description]"
  zh: "[1-2 sentence Chinese description]"
date: {today}
tags: ["arxiv", "ai", {', '.join(f'"{c.lower()}"' for c in paper['categories'][:5])}]
image: "{ARXIV_IMAGE}"
---

:::en
**Paper**: [{paper['id']}](https://arxiv.org/abs/{paper['id']})
**Authors**: {authors_str}
**Categories**: {cats_str}

## The Gap

[Where has existing research reached? What specific boundary or limitation does this paper address? Be precise — name the prior approaches and their shortcomings. Then show the logical path from gap → method → evidence → conclusion using a simple ASCII diagram.]

```
[ASCII logic topology showing: Problem → Assumption → Method → Evidence → Conclusion]
[Use only: + - | / \\ > < v ^ * = ~ . : # [ ] ( ) _]
[NO Unicode box drawing characters]
```

## The Increment

**One sentence**: [Before this paper vs after this paper — what changed in the world?]

### Core Mechanism

[Explain the method's internal structure in 2-3 paragraphs. What are the components? How does data flow? What operations happen?]

```
[ASCII diagram of method internals: components, data flow, operations]
[This is the X-ray of how it works inside]
```

[Now explain using a **structural metaphor**: find something familiar where each part of the method maps to a part of the analogy. Walk through the method using this metaphor so the reader can retell it in their own words. The metaphor must be load-bearing — without it, the reader is back to staring at diagrams.]

### Key Concepts

[Pick 1-3 concepts essential to understanding this paper. For each:]
- **[Concept name]**: [Explain Feynman-style from zero. Build intuition. Give a concrete example. Don't use jargon to explain jargon.]

## Framework Shift

[Draw a "napkin sketch" comparing the old way vs this paper's way. The goal: let the reader see the gestalt shift at a glance.]

```
Before (mainstream approach):        After (this paper):
[ASCII diagram]                      [ASCII diagram]
[Show structural difference, not feature list]
```

[One sentence: From X to Y, the core shift is ___.]

## Expert Assessment

[You're a senior researcher who's seen thousands of papers. Evaluate honestly in plain language:]

**Problem choice**: [Is this a real gap or manufactured? Where does it sit in the field's trajectory?]

**Method maturity**: [Clever insight or brute force? Are there simpler approaches being overlooked?]

**Experimental integrity**: [Are baselines fair? Do the numbers hold up under scrutiny? Any red flags?]

**Writing quality**: [Where did the authors cut corners? Which section, if rewritten, would elevate the whole paper?]

**Verdict**: [strong accept / weak accept / borderline / weak reject / strong reject] — [one-sentence reason]

## Takeaways

[What can a practitioner steal from this paper? Not generic insights — specific ideas, techniques, or framings that transfer to other domains. If there's nothing concrete to take, say so honestly.]
:::

:::zh
**论文**: [{paper['id']}](https://arxiv.org/abs/{paper['id']})
**作者**: {authors_str}
**分类**: {cats_str}

## 缺口

[现有研究到达了什么边界？这篇论文要解决什么具体的局限或问题？要精准——指出此前的方法及其不足。然后用简单的 ASCII 图展示从缺口到方法到证据到结论的逻辑路径。]

```
[ASCII 逻辑拓扑图：问题 → 假设 → 方法 → 证据 → 结论]
[只用：+ - | / \\ > < v ^ * = ~ . : # [ ] ( ) _]
[禁用 Unicode 制表符]
```

## 增量

**一句话**: [这篇论文之前 vs 之后——世界多了什么？]

### 核心机制

[用2-3段解释方法的内部结构。有哪些组件？数据如何流动？发生了什么操作？]

```
[方法内部的 ASCII 图：组件、数据流、操作]
[这是方法内部运作的X光片]
```

[现在用**核喻**（结构性比喻）来解释：找一个熟悉的事物，方法的每个部分都能映射到比喻的某个部分。沿着这个比喻把方法走一遍，让读者能用自己的话复述。核喻必须承重——没有它，读者就回到盯着图发呆的状态。]

### 关键概念

[选1-3个理解本文必需的概念。对每个概念：]
- **[概念名]**: [费曼式讲解，从零开始。建立直觉。给具体例子。不用术语解释术语。]

## 框架转变

[画一张"餐巾纸速写"对比旧方法和本文方法。目标：让读者一眼看出思维方式的转变。]

```
之前（主流方法）：                之后（本文方法）：
[ASCII 图]                        [ASCII 图]
[展示结构差异，而非功能清单]
```

[一句话：从 X 到 Y，核心转变是___。]

## 专家评审

[你是见过数千篇论文的资深研究者。用白话坦率评估：]

**选题眼光**: [这是真缺口还是人造缺口？在该领域的发展轨迹中处于什么位置？]

**方法成熟度**: [巧劲还是蛮力？有没有被忽略的更简单方法？]

**实验诚意**: [基线公平吗？数字经得起推敲吗？有无值得警惕之处？]

**写作功力**: [作者在哪里偷懒了？哪一段重写能让整篇论文升一个档次？]

**判决**: [强接收 / 弱接收 / 临界 / 弱拒绝 / 强拒绝] — [一句话理由]

## 要点总结

[实践者能从这篇论文"偷"走什么？不要泛泛的洞见——要具体的想法、技术或思维框架，能迁移到其他领域的。如果没有具体可取之处，诚实地说没有。]
:::

CRITICAL CONSTRAINTS:
- ASCII diagrams: ONLY use + - | / \\ > < v ^ * = ~ . : # [ ] ( ) _ and spaces
- NEVER use Unicode box drawing: ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╔ ╗ ╚ ╝ ● ○ ■ □ ◆ ◇ ▼ ▲ ► ◄ → ← ↑ ↓
- Chinese paragraphs: Add line breaks after periods (。) to prevent horizontal scrolling
- Structural metaphor: Must be load-bearing (method components map to analogy parts), not decorative
- Expert assessment: Be honest and calibrated, not uniformly positive
- Tone: Like explaining to a colleague over coffee, not writing a review
- Chinese content: Parallel composition, NOT translation
- Output ONLY the complete MDX file, nothing else
- DO NOT include <thinking> tags or any other XML tags in your output
- Start your response directly with the --- frontmatter delimiter"""

    content = call_llm(
        client, model, provider,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=8192
    )
    if not content:
        print(f"Warning: LLM returned empty response for post generation ({paper['id']})")
        return None

    # Strip thinking tags if present
    content = strip_thinking_tags(content)
    return content.strip()


def _yaml_double_quote(value: str) -> str:
    """Safely double-quote a YAML string value, escaping \\ and \"."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _fix_frontmatter_quotes(frontmatter: str) -> str:
    """Re-quote title/description en/zh values in frontmatter safely.

    Handles values that contain quotes, colons, or other YAML-special chars
    by extracting the raw value and re-wrapping with proper escaping.
    """
    def _requote(m):
        prefix = m.group(1)  # e.g. "  en: " or "  zh: "
        raw = m.group(2)
        # Strip surrounding quotes (ASCII or smart quotes) if present
        if len(raw) >= 2:
            first, last = raw[0], raw[-1]
            if (first == '"' and last == '"') or \
               (first == '\u201c' and last == '\u201d') or \
               (first == "'" and last == "'"):
                raw = raw[1:-1]
        return prefix + _yaml_double_quote(raw)

    # Match indented en:/zh: lines under title: or description:
    return re.sub(
        r'^(  (?:en|zh):\s+)(.+)$',
        _requote,
        frontmatter,
        flags=re.MULTILINE,
    )


def sanitize_mdx(content):
    """Fix common LLM-generated MDX issues.

    - Fix YAML frontmatter quoting for special characters
    - Collapse multi-line $$...$$ math blocks onto single lines
      (prevents \\nabla etc. from being split as \\n + abla)
    - Escape bare < followed by digits (MDX parses as JSX)
    - Repair mismatched bold markers (**text* → **text**)
    - Replace ASCII colons with full-width Chinese colons in :::zh sections
    """
    # Fix frontmatter quoting before anything else
    fm_match = re.match(r'^---\n(.*?\n)---', content, re.DOTALL)
    if fm_match:
        original_fm = fm_match.group(1)
        fixed_fm = _fix_frontmatter_quotes(original_fm)
        if fixed_fm != original_fm:
            content = "---\n" + fixed_fm + "---" + content[fm_match.end():]

    # Collapse multi-line $$ blocks onto single lines
    def _collapse_math(m):
        inner = m.group(1)
        return "$$" + " ".join(inner.split()) + "$$"

    content = re.sub(r"\$\$([\s\S]*?)\$\$", _collapse_math, content)

    lines = content.split("\n")
    result = []
    in_code_block = False
    in_zh_section = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        # Track :::zh sections
        if line.strip() == ":::zh":
            in_zh_section = True
        elif line.strip() == ":::" and in_zh_section:
            in_zh_section = False

        if not in_code_block:
            # Escape < followed by a digit (not a valid HTML/JSX tag)
            line = re.sub(r"<(\d)", r"&lt;\1", line)
            # Fix **text* → **text** (bold opened with ** but closed with single *)
            line = re.sub(r"\*\*([^*\n]+)\*(?!\*)", r"**\1**", line)

            # Fix MDX orphaned punctuation: add space after **text**: and **text**,
            # Replace ASCII colons with full-width colons in Chinese sections
            if in_zh_section:
                line = re.sub(r'(\*\*[^*]+\*\*):(?! )', r'\1: ', line)
                line = re.sub(r'(\*\*[^*]+\*\*),(?! )', r'\1, ', line)

                # Replace ASCII colons with full-width Chinese colons
                # Skip metadata lines, URLs, and ::: directive markers
                stripped = line.strip()
                if not (stripped.startswith('**论文**:') or
                       stripped.startswith('**作者**:') or
                       stripped.startswith('**分类**:') or
                       stripped.startswith(':::') or
                       'http:' in line or 'https:' in line):
                    # Replace colons not preceded by ** (bold markers)
                    new_line = ''
                    i = 0
                    while i < len(line):
                        if line[i] == ':':
                            # Check if preceded by **
                            if i >= 2 and line[i-2:i] == '**':
                                new_line += ':'
                            else:
                                new_line += '：'
                        else:
                            new_line += line[i]
                        i += 1
                    line = new_line

        result.append(line)

    return "\n".join(result)


def extract_code_block(text: str) -> str:
    """Extract Python code from LLM response, stripping markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[-1].strip() == "```":
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines)
    return text.strip()


def strip_thinking_tags(text: str) -> str:
    """Remove <thinking>...</thinking> tags from LLM output."""
    text = text.strip()
    # Remove thinking tags at the beginning
    if text.startswith("<thinking>"):
        end_tag = "</thinking>"
        end_idx = text.find(end_tag)
        if end_idx != -1:
            text = text[end_idx + len(end_tag):].strip()
    return text


def extract_title_zh(mdx_content: str) -> str:
    """Extract Chinese title from generated MDX frontmatter."""
    m = re.search(r'^\s*zh:\s*"(.+)"', mdx_content, re.MULTILINE)
    if not m:
        return ""
    # Unescape YAML double-quote escapes
    return m.group(1).replace('\\"', '"').replace('\\\\', '\\')


def generate_manim_code(client, model, provider, paper, scene_type: str, title_zh: str = "") -> str | None:
    """Generate Manim scene code via LLM with 1 retry on validation failure."""
    if scene_type == "hero":
        system_prompt = HERO_IMAGE_SYSTEM
        user_template = HERO_IMAGE_USER
        class_name = "HeroScene"
    else:
        system_prompt = CONCEPT_GIF_SYSTEM
        user_template = CONCEPT_GIF_USER
        class_name = "ConceptScene"

    user_prompt = user_template.format(
        title=paper["title"], title_zh=title_zh, summary=paper["summary"][:800],
    )

    for attempt in range(2):
        if provider == "anthropic":
            # Anthropic doesn't support system messages in the same way
            # Prepend system prompt to user message
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            content = call_llm(
                client, model, provider,
                messages=[{"role": "user", "content": combined_prompt}],
                temperature=0.3,
                max_tokens=2048
            )
        else:
            content = call_llm(
                client, model, provider,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=2048
            )

        if not content:
            return None

        code = extract_code_block(content)
        if validate_scene_code(code):
            # Verify the expected class name exists
            if f"class {class_name}" in code:
                return code
        if attempt == 0:
            print(f"    Retry {scene_type} code generation (validation failed)")

    return None


def generate_paper_visuals(client, model, provider, paper, slug: str, title_zh: str = "") -> dict:
    """Orchestrate hero PNG + concept GIF generation. Returns dict of paths."""
    output_dir = VISUALS_DIR / slug
    results = {}

    # Hero image (static PNG)
    print(f"  Generating hero image...")
    hero_code = generate_manim_code(client, model, provider, paper, "hero", title_zh=title_zh)
    if hero_code:
        path = render_scene(hero_code, "HeroScene", output_dir, "png")
        if path:
            results["hero"] = f"/arxiv-visuals/{slug}/HeroScene.png"

    # Concept animation (GIF)
    print(f"  Generating concept animation...")
    gif_code = generate_manim_code(client, model, provider, paper, "concept", title_zh=title_zh)
    if gif_code:
        path = render_scene(gif_code, "ConceptScene", output_dir, "gif")
        if path:
            results["concept"] = f"/arxiv-visuals/{slug}/ConceptScene.gif"

    return results


def patch_frontmatter_image(mdx: str, image_url: str) -> str:
    """Replace the frontmatter image: field with a local path."""
    return re.sub(
        r'^(image:\s*)"[^"]*"',
        f'\\1"{image_url}"',
        mdx,
        count=1,
        flags=re.MULTILINE,
    )


def insert_after_frontmatter(mdx: str, content: str) -> str:
    """Insert content after the closing --- of frontmatter."""
    parts = mdx.split("---", 2)
    if len(parts) >= 3:
        return parts[0] + "---" + parts[1] + "---\n\n" + content + parts[2]
    return mdx


def main():
    client, model, provider = get_llm_client()
    last_fetch = load_last_fetch()
    print(f"Last fetch: {last_fetch.isoformat()}")
    print(f"Using {provider} provider with model: {model}")

    # Fetch recent papers
    print("Fetching recent papers from arxiv...")
    papers = fetch_recent_papers(CATEGORIES, max_results=20)
    print(f"Found {len(papers)} papers")

    if not papers:
        print("No papers found, exiting")
        save_last_fetch()
        return

    # Filter out already-covered papers
    existing_ids = get_existing_arxiv_ids()
    print(f"Found {len(existing_ids)} existing arxiv IDs in blog")
    papers = [p for p in papers if p["id"] not in existing_ids]
    print(f"{len(papers)} new papers after filtering")

    if not papers:
        print("No new papers to process")
        save_last_fetch()
        return

    # Select most interesting papers
    print("Selecting most interesting papers via LLM...")
    selected = select_papers(client, model, provider, papers, count=min(5, len(papers)))
    print(f"Selected {len(selected)} papers:")
    for p in selected:
        print(f"  - {p['title']}")

    # Generate blog posts
    for paper in selected:
        slug = slugify(paper["title"])
        filename = f"arxiv-{slug}.mdx"
        filepath = BLOG_DIR / filename
        if filepath.exists():
            print(f"Skipping {filename} (already exists)")
            continue

        print(f"Generating post for: {paper['title']}...")
        try:
            content = generate_blog_post(client, model, provider, paper)
        except Exception:
            print(f"  Blog post generation failed, skipping:")
            traceback.print_exc()
            continue
        if not content:
            continue

        # Strip markdown code fences if the LLM wrapped the output
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first line (```mdx or ```) and last line (```)
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            content = "\n".join(lines)

        content = sanitize_mdx(content)

        # Generate visuals (never blocks text post)
        try:
            print(f"  Generating visuals for: {paper['title']}...")
            title_zh = extract_title_zh(content)
            visuals = generate_paper_visuals(client, model, provider, paper, slug, title_zh=title_zh)
            if visuals.get("hero"):
                content = patch_frontmatter_image(content, visuals["hero"])
                hero_md = f"![Hero diagram]({visuals['hero']})\n\n"
                content = insert_after_frontmatter(content, hero_md)
            if visuals.get("concept"):
                concept_md = f"![Concept animation]({visuals['concept']})\n\n"
                content = insert_after_frontmatter(content, concept_md)
        except Exception:
            print(f"  Visual generation failed, continuing with text-only post:")
            traceback.print_exc()

        filepath.write_text(content + "\n")
        print(f"Wrote {filepath}")

    save_last_fetch()
    print("Done!")


if __name__ == "__main__":
    main()
