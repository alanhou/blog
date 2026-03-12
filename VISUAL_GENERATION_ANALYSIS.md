# Visual Generation Failure Analysis

## Problem Summary

The GitHub Actions workflow (`arxiv.yml`) successfully creates blog posts but frequently fails to generate visuals (HeroScene.png and ConceptScene.gif) for many posts.

## Evidence

### Commit 4919882 (March 11, 2026 14:00 UTC)
- **Created 5 posts:**
  - arxiv-create-testing-llms-for-associative-creativity
  - arxiv-from-data-statistics-to-feature-geometry
  - arxiv-generative-drifting-is-secretly-score-matching
  - arxiv-recosplat-autoregressive-feed-forward-gaussian-splatting
  - arxiv-task-aware-modulation-using-representation-learning

- **Visuals generated:** Only 1/5 (task-aware-modulation got ConceptScene.gif only)
- **Missing visuals:** 4 posts got no visuals at all

### Commit 9d07b80 (March 11, 2026 17:06 UTC)
- **Created 5 posts:** beacon, emotional-modulation, model-merging, think-before, understanding
- **Visuals generated:** 5/5 posts got visuals (though understanding-the-use-of-a-large only got HeroScene.png)

### Commit 930129b (March 12, 2026 03:05 UTC)
- **Created 3 posts:** beyond-the-illusion, dynvla, too-vivid
- **Visuals generated:** 1/3 (only too-vivid got both HeroScene.png and ConceptScene.gif)
- **Missing visuals:** 2 posts got no visuals

## Root Causes

The visual generation can fail at multiple points in the pipeline:

### 1. LLM Code Generation Failures
**Location:** `scripts/fetch_arxiv.py:generate_manim_code()`

- LLM API call fails or times out
- LLM returns invalid/incomplete code
- Code fails validation (syntax errors, dangerous imports)
- Generated code missing expected class name (HeroScene/ConceptScene)

**Retry logic:** Only 2 attempts per scene, then gives up

### 2. Manim Rendering Failures
**Location:** `scripts/render_manim.py:render_scene()`

- Manim not found in PATH (shouldn't happen in CI)
- Render timeout (120 seconds per scene)
- Runtime errors in generated code (invalid Manim API usage)
- Missing output files after render

### 3. Silent Failure Handling
**Location:** `scripts/fetch_arxiv.py:main()` lines 756-770

```python
try:
    print(f"  Generating visuals for: {paper['title']}...")
    visuals = generate_paper_visuals(...)
    # ... update content with visuals ...
except Exception:
    print(f"  Visual generation failed, continuing with text-only post:")
    traceback.print_exc()
```

**Issue:** The script catches all exceptions and continues, creating posts without visuals. This is by design ("never blocks text post") but makes debugging difficult.

## Why Some Posts Succeed and Others Fail

Likely reasons for inconsistent success:

1. **LLM variability:** The LLM (claude-sonnet-4-20250514) generates different quality code each time
2. **Paper complexity:** Some papers are harder to visualize, leading to more complex/buggy Manim code
3. **API rate limits:** Multiple posts in quick succession might hit rate limits
4. **Timeout issues:** Complex animations might exceed the 120-second render timeout
5. **Invalid Manim API usage:** LLM might use deprecated or non-existent Manim classes/methods

## Recommendations

### Short-term fixes:

1. **Add retry logic for entire visual generation:**
   - Currently only retries code generation (2 attempts)
   - Should retry the entire render process if it fails

2. **Increase timeouts:**
   - Current: 120 seconds per scene
   - Suggested: 180-240 seconds for complex animations

3. **Better error logging:**
   - Log which specific step failed (code gen vs render)
   - Save failed code attempts for debugging
   - Add structured logging to track success rates

4. **Fallback to simpler visuals:**
   - If complex animation fails, try generating a simpler static image
   - Use a template-based approach as last resort

### Long-term improvements:

1. **Separate visual generation job:**
   - Run visual generation as a separate workflow
   - Can retry failed visuals without regenerating posts
   - Allows manual triggering for specific posts

2. **Visual generation queue:**
   - Generate posts immediately
   - Queue visual generation as background jobs
   - Retry failed visuals automatically

3. **Pre-validation of generated code:**
   - Test generated code in a sandbox before rendering
   - Catch common errors (missing imports, invalid API calls)
   - Provide feedback to LLM for regeneration

4. **Monitoring and alerts:**
   - Track visual generation success rate
   - Alert when success rate drops below threshold
   - Dashboard showing which posts need visuals

## Immediate Action Taken

Manually generated missing visuals for:
- 4 March 11 posts (commit 809f678)
- 2 March 12 posts (commit cab5945)

All posts now have complete visuals.
