#!/usr/bin/env python3
"""Regenerate a single blog post."""
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
from fetch_arxiv import (
    get_llm_client, generate_blog_post, generate_paper_visuals,
    slugify, sanitize_mdx, extract_title_zh, patch_frontmatter_image,
    insert_after_frontmatter, strip_thinking_tags, BLOG_DIR, ARXIV_API_URL
)

if len(sys.argv) < 2:
    print("Usage: python regenerate_post.py <arxiv_id>")
    sys.exit(1)

arxiv_id = sys.argv[1]

client, model, provider = get_llm_client()
print(f"Using {provider} provider with model: {model}")

# Fetch paper from arxiv
print(f"Fetching paper {arxiv_id} from arxiv...")
resp = requests.get(f"{ARXIV_API_URL}?id_list={arxiv_id}", timeout=30)
resp.raise_for_status()

ns = {"atom": "http://www.w3.org/2005/Atom"}
root = ET.fromstring(resp.text)
entry = root.find("atom:entry", ns)

if not entry:
    print(f"Paper {arxiv_id} not found")
    sys.exit(1)

title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
title = re.sub(r"\s+", " ", title)
summary = entry.find("atom:summary", ns).text.strip()
authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
categories = [c.get("term") for c in entry.findall("atom:category", ns)]

paper = {
    "id": arxiv_id,
    "title": title,
    "summary": summary,
    "authors": authors,
    "categories": categories
}

print(f"Title: {paper['title']}")
print(f"Authors: {', '.join(authors[:3])}...")
print(f"Categories: {', '.join(categories[:3])}")

slug = slugify(paper["title"])
filepath = BLOG_DIR / f"arxiv-{slug}.mdx"

print(f"Generating post for: {paper['title']}")
content = generate_blog_post(client, model, provider, paper)

if not content:
    print("Failed to generate content")
    sys.exit(1)

content = sanitize_mdx(content)

# Generate visuals
try:
    print("Generating visuals...")
    title_zh = extract_title_zh(content)
    visuals = generate_paper_visuals(client, model, provider, paper, slug, title_zh=title_zh)
    if visuals.get("hero"):
        content = patch_frontmatter_image(content, visuals["hero"])
        hero_md = f"![Hero diagram]({visuals['hero']})\n\n"
        content = insert_after_frontmatter(content, hero_md)
    if visuals.get("concept"):
        concept_md = f"![Concept animation]({visuals['concept']})\n\n"
        content = insert_after_frontmatter(content, concept_md)
except Exception as e:
    print(f"Visual generation failed: {e}")
    import traceback
    traceback.print_exc()

filepath.write_text(content + "\n")
print(f"Wrote {filepath}")
