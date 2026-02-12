#!/usr/bin/env python3
"""Fetch recent arxiv papers, select interesting ones via LLM, and generate bilingual MDX blog posts."""

import glob
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from openai import OpenAI

BLOG_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "blog"
LAST_FETCH_FILE = Path(__file__).resolve().parent / ".last_fetch"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
ARXIV_IMAGE = "https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-fb.png"


def get_llm_client():
    api_key = os.environ.get("LLM_API_KEY")
    base_url = os.environ.get("LLM_BASE_URL")
    model = os.environ.get("LLM_MODEL_NAME")
    if not all([api_key, base_url, model]):
        print("Error: LLM_API_KEY, LLM_BASE_URL, and LLM_MODEL_NAME must be set")
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url=base_url), model


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
    resp = requests.get(ARXIV_API_URL, params=params, timeout=30)
    resp.raise_for_status()

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


def select_papers(client, model, papers, count=5):
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

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = resp.choices[0].message.content.strip()
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


def generate_blog_post(client, model, paper):
    """Use LLM to generate a full bilingual MDX blog post."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    authors_str = ", ".join(paper["authors"][:10])
    cats_str = ", ".join(paper["categories"][:5])

    prompt = f"""Generate a bilingual (English + Chinese) MDX blog post for this arxiv paper.

Paper ID: {paper['id']}
Title: {paper['title']}
Authors: {authors_str}
Categories: {cats_str}
Abstract: {paper['summary']}

Use EXACTLY this format (no deviations):

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

## Abstract

[English abstract summary]

## Key Contributions

- [bullet points]

[2-4 more sections analyzing the paper in depth - methodology, results, implications, etc.]

## Takeaways

[numbered list of key takeaways]
:::

:::zh
**论文**: [{paper['id']}](https://arxiv.org/abs/{paper['id']})
**作者**: {authors_str}
**分类**: {cats_str}

## 摘要

[Chinese abstract summary]

## 主要贡献

- [bullet points in Chinese]

[2-4 more sections in Chinese - same structure as English]

## 要点总结

[numbered list of key takeaways in Chinese]
:::

IMPORTANT:
- The Chinese content should be a complete parallel version, not a translation
- Use LaTeX math notation where appropriate ($...$ inline, $$...$$ block)
- Keep the tone analytical and technical
- Output ONLY the complete MDX file content, nothing else"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return resp.choices[0].message.content.strip()


def main():
    client, model = get_llm_client()
    last_fetch = load_last_fetch()
    print(f"Last fetch: {last_fetch.isoformat()}")

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
    selected = select_papers(client, model, papers, count=min(5, len(papers)))
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
        content = generate_blog_post(client, model, paper)

        # Strip markdown code fences if the LLM wrapped the output
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first line (```mdx or ```) and last line (```)
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            content = "\n".join(lines)

        filepath.write_text(content + "\n")
        print(f"Wrote {filepath}")

    save_last_fetch()
    print("Done!")


if __name__ == "__main__":
    main()
