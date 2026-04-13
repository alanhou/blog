#!/usr/bin/env python3
"""Generate visuals for an existing blog post."""
import sys
from pathlib import Path
from fetch_arxiv import (
    get_llm_client, generate_paper_visuals, extract_title_zh,
    patch_frontmatter_image, insert_after_frontmatter, BLOG_DIR
)

if len(sys.argv) < 2:
    print("Usage: python generate_visuals_only.py <slug>")
    print("Example: python generate_visuals_only.py agentic-critical-training")
    sys.exit(1)

slug = sys.argv[1]
filepath = BLOG_DIR / f"arxiv-{slug}.mdx"

if not filepath.exists():
    print(f"Error: {filepath} does not exist")
    sys.exit(1)

# Read existing post
content = filepath.read_text()

# Extract paper info from the post
import re
paper_match = re.search(r'\*\*Paper\*\*: \[([\d.]+)\]', content)
if not paper_match:
    print("Error: Could not find paper ID in post")
    sys.exit(1)

arxiv_id = paper_match.group(1)
print(f"Found paper ID: {arxiv_id}")

# Extract title from frontmatter
title_match = re.search(r'title:\s*\n\s*en:\s*"([^"]+)"', content)
if not title_match:
    print("Error: Could not find title in frontmatter")
    sys.exit(1)

title = title_match.group(1)
print(f"Title: {title}")

# Extract summary from post (first paragraph after "## The Gap")
summary_match = re.search(r'## The Gap\s*\n\s*(.+?)(?:\n\n|\n```)', content, re.DOTALL)
summary = summary_match.group(1).strip() if summary_match else ""

paper = {
    "id": arxiv_id,
    "title": title,
    "summary": summary,
    "authors": [],
    "categories": []
}

client, model, provider = get_llm_client()
print(f"Using {provider} provider with model: {model}")

# Generate visuals
try:
    print("Generating visuals...")
    title_zh = extract_title_zh(content)
    print(f"Chinese title: {title_zh}")

    visuals = generate_paper_visuals(client, model, provider, paper, slug, title_zh=title_zh)

    # Use cover image (from GIF) as frontmatter image, fallback to hero
    if visuals.get("cover"):
        print(f"✓ Cover image generated: {visuals['cover']}")
        content = patch_frontmatter_image(content, visuals["cover"])
    elif visuals.get("hero"):
        print(f"✓ Hero image generated: {visuals['hero']}")
        content = patch_frontmatter_image(content, visuals["hero"])
        hero_md = f"![Hero diagram]({visuals['hero']})\n\n"
        content = insert_after_frontmatter(content, hero_md)
    else:
        print("✗ Hero/cover image generation failed")

    if visuals.get("concept"):
        print(f"✓ Concept animation generated: {visuals['concept']}")
        concept_md = f"![Concept animation]({visuals['concept']})\n\n"
        content = insert_after_frontmatter(content, concept_md)
    else:
        print("✗ Concept animation generation failed")

    if visuals:
        filepath.write_text(content)
        print(f"\n✓ Updated {filepath}")
    else:
        print("\n✗ No visuals were generated")

except Exception as e:
    print(f"Visual generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
