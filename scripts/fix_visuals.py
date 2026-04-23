#!/usr/bin/env python3
"""
Post-processing script to ensure all arxiv blog posts have proper visuals.

This script:
1. Checks if ConceptScene.gif exists for each post
2. Generates cover PNG from GIF (frame at 5 seconds, not black frame)
3. Updates frontmatter to use the cover image
4. Ensures animation is embedded after frontmatter

Run after generate_visuals_only.py or fetch_arxiv.py to fix any visual issues.
"""

import re
import subprocess
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "blog"
VISUALS_DIR = Path(__file__).resolve().parent.parent / "public" / "arxiv-visuals"


def extract_cover_from_gif(gif_path: Path, output_path: Path) -> bool:
    """Extract a frame from GIF at 5 seconds (with visible content) as cover image."""
    try:
        # Extract frame at 5 seconds, scale to 1200x630 with padding
        cmd = [
            "ffmpeg", "-ss", "5", "-i", str(gif_path),
            "-vframes", "1",
            "-vf", "scale=1200:630:force_original_aspect_ratio=decrease,pad=1200:630:(ow-iw)/2:(oh-ih)/2:black",
            str(output_path), "-y"
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0 and output_path.exists()
    except Exception as e:
        print(f"  Error extracting cover: {e}")
        return False


def ensure_animation_embedded(content: str, slug: str) -> str:
    """Ensure animation is embedded after frontmatter."""
    animation_line = f"![Concept animation](/arxiv-visuals/{slug}/ConceptScene.gif)"

    # Check if already embedded
    if animation_line in content:
        return content

    # Insert after frontmatter (after second ---)
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return parts[0] + "---" + parts[1] + "---\n\n" + animation_line + "\n\n" + parts[2]

    return content


def update_cover_image(content: str, slug: str) -> str:
    """Update frontmatter to use custom cover image."""
    cover_path = f"/arxiv-visuals/arxiv-{slug}.png"

    # Replace image field in frontmatter
    updated = re.sub(
        r'^(image:\s*)"[^"]*"',
        f'\\1"{cover_path}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    return updated


def process_post(post_path: Path) -> bool:
    """Process a single blog post to ensure proper visuals."""
    # Extract slug from filename (arxiv-{slug}.mdx)
    slug = post_path.stem.replace("arxiv-", "")

    gif_path = VISUALS_DIR / slug / "ConceptScene.gif"
    cover_path = VISUALS_DIR / f"arxiv-{slug}.png"

    # Check if GIF exists
    if not gif_path.exists():
        print(f"⊙ {slug}: No ConceptScene.gif found, skipping")
        return False

    changes_made = False

    # Generate cover image from GIF if missing or outdated
    if not cover_path.exists() or cover_path.stat().st_mtime < gif_path.stat().st_mtime:
        print(f"  Generating cover image for {slug}...")
        if extract_cover_from_gif(gif_path, cover_path):
            print(f"  ✓ Created cover: {cover_path.name}")
            changes_made = True
        else:
            print(f"  ✗ Failed to create cover for {slug}")
            return False

    # Update blog post content
    content = post_path.read_text()
    original_content = content

    # Ensure animation is embedded
    content = ensure_animation_embedded(content, slug)

    # Update cover image in frontmatter
    content = update_cover_image(content, slug)

    # Write back if changed
    if content != original_content:
        post_path.write_text(content)
        print(f"✓ Updated: {post_path.name}")
        changes_made = True

    return changes_made


def main():
    """Process all arxiv blog posts."""
    print("Checking arxiv blog posts for visual issues...\n")

    posts = sorted(BLOG_DIR.glob("arxiv-*.mdx"))
    total = len(posts)
    processed = 0
    updated = 0

    for post_path in posts:
        processed += 1
        if process_post(post_path):
            updated += 1

    print(f"\n{'='*60}")
    print(f"Processed: {processed}/{total} posts")
    print(f"Updated: {updated} posts")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
