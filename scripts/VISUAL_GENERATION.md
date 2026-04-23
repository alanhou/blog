# ArXiv Blog Visual Generation

This document explains how visual assets (animations and cover images) are generated for arxiv blog posts.

## Visual Assets

Each arxiv blog post should have:

1. **ConceptScene.gif** - Animated GIF showing key concepts (embedded in post)
2. **Cover Image PNG** - Static cover image for social sharing (1200x630, extracted from GIF at 5s)
3. **HeroScene.png** (optional) - Static diagram (legacy, now replaced by cover image)

## File Structure

```
public/arxiv-visuals/
├── {slug}/
│   ├── ConceptScene.gif          # Animation embedded in post
│   └── animation.mp4              # Source MP4 (if manually created)
└── arxiv-{slug}.png               # Cover image for frontmatter
```

## Automated Generation

### New Posts (fetch_arxiv.py)

When creating new posts, the script automatically:
1. Generates manim code via LLM
2. Renders ConceptScene.gif
3. Extracts cover PNG from GIF (frame at 5 seconds to avoid black frames)
4. Updates frontmatter with cover image path
5. Embeds animation after frontmatter

```bash
python scripts/fetch_arxiv.py
```

### Existing Posts (generate_visuals_only.py)

To add visuals to an existing post:

```bash
python scripts/generate_visuals_only.py <slug>
```

Example:
```bash
python scripts/generate_visuals_only.py agentic-critical-training
```

## Manual Visual Creation

If you create animations manually with manim:

1. Create your scene file (e.g., `my_scene.py`)
2. Render to GIF:
   ```bash
   conda activate llm
   manim -ql my_scene.py ConceptScene
   ```
3. Copy output:
   ```bash
   cp media/videos/my_scene/480p15/ConceptScene.gif public/arxiv-visuals/{slug}/
   ```
4. Run fix script to generate cover and update post:
   ```bash
   python scripts/fix_visuals.py
   ```

## Fixing Visual Issues

If posts are missing cover images or animations aren't embedded:

```bash
python scripts/fix_visuals.py
```

This script:
- Checks all arxiv posts for ConceptScene.gif
- Generates cover PNG from GIF (frame at 5s, not black frame)
- Updates frontmatter to use cover image
- Ensures animation is embedded after frontmatter

## Cover Image Generation

**Important:** Cover images are extracted at 5 seconds into the animation, not the first frame, to avoid black backgrounds (manim animations start with black frames).

The extraction command:
```bash
ffmpeg -ss 5 -i ConceptScene.gif -vframes 1 \
  -vf "scale=1200:630:force_original_aspect_ratio=decrease,pad=1200:630:(ow-iw)/2:(oh-ih)/2:black" \
  arxiv-{slug}.png -y
```

## Troubleshooting

### Black cover images
- Run `python scripts/fix_visuals.py` to regenerate covers from frame at 5s

### Missing animations in posts
- Run `python scripts/fix_visuals.py` to embed animations

### Animation not rendering
- Check manim is installed: `conda activate llm && manim --version`
- Verify scene code syntax
- Check render logs for errors

### LLM API issues
- Set environment variables:
  ```bash
  export LLM_API_KEY="your-key"
  export LLM_MODEL_NAME="claude-3-5-sonnet-20241022"
  export LLM_PROVIDER="anthropic"
  ```

## Best Practices

1. **Always run fix_visuals.py after manual animation creation** to ensure proper cover images
2. **Use frame at 5 seconds** for cover extraction (not first frame)
3. **Keep animations under 60 seconds** for reasonable file sizes
4. **Use 480p15 quality** for web performance (manim -ql flag)
5. **Test locally** before committing visual assets

## Workflow Summary

### Automated (Recommended)
```bash
# Fetch new papers and generate visuals
python scripts/fetch_arxiv.py

# Fix any visual issues
python scripts/fix_visuals.py
```

### Manual
```bash
# 1. Create manim scene
vim my_scene.py

# 2. Render animation
conda activate llm
manim -ql my_scene.py ConceptScene

# 3. Copy to public directory
cp media/videos/my_scene/480p15/ConceptScene.gif public/arxiv-visuals/{slug}/

# 4. Generate cover and update post
python scripts/fix_visuals.py

# 5. Commit
git add public/arxiv-visuals/{slug}/ public/arxiv-visuals/arxiv-{slug}.png src/content/blog/arxiv-{slug}.mdx
git commit -m "Add visuals for {slug}"
```
