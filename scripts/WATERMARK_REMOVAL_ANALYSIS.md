# Watermark Removal Analysis: Generalizing from Gemini to 即梦AI

## Overview

This document analyzes the technical approach used in the Gemini Watermark Remover and explores how it can be generalized to other AI-generated image watermarks, specifically 即梦AI (Jimeng AI).

## Gemini Watermark Removal Technique

### Core Algorithm: Reverse Alpha Blending

The Gemini watermark remover uses a mathematical approach based on **reverse alpha blending**:

**Forward alpha blending (how watermarks are applied):**
```
watermarked = original × (1 - α) + logo × α
```

**Reverse alpha blending (how to remove them):**
```
original = (watermarked - logo × α) / (1 - α)
```

Where:
- `watermarked` = the pixel value in the watermarked image
- `original` = the pixel value we want to recover
- `logo` = the watermark logo pixel value (255 for white)
- `α` = the alpha/transparency value (0-1)

### Key Components

1. **Pre-computed Alpha Maps**
   - Gemini provides reference background images (`bg_48.png`, `bg_96.png`)
   - These contain the exact alpha values used during watermarking
   - Alpha is computed as: `α = max(R, G, B) / 255`

2. **Position Detection**
   - Watermark is always in the bottom-right corner
   - Size depends on image dimensions:
     - Images > 1024×1024: 96×96 logo, 64px margins
     - Smaller images: 48×48 logo, 32px margins

3. **Vectorized Processing**
   - Uses NumPy for efficient pixel-wise operations
   - Only processes pixels where α > threshold (0.002)
   - Clamps α to max 0.99 to avoid division by zero

### Implementation Details

**Python version** (`remove_gemini_watermark.py`):
```python
# Reverse alpha blending formula
alpha_clamped = np.clip(alpha, 0.0, MAX_ALPHA)
one_minus_alpha = 1.0 - alpha_clamped
restored = (region - alpha_clamped * LOGO_VALUE) / one_minus_alpha
```

**JavaScript version** (in `gemini-watermark.astro`):
```javascript
const watermarked = imageData.data[imgIdx + c];
const original = (watermarked - alpha * LOGO_VALUE) / oneMinusAlpha;
imageData.data[imgIdx + c] = Math.max(0, Math.min(255, Math.round(original)));
```

## Challenges in Generalizing to Other Watermarks

### 1. No Pre-computed Alpha Maps

**Problem:** Unlike Gemini, most AI image generators don't provide alpha maps.

**Solutions:**
- **Brightness-based estimation:** Assume brighter pixels = higher alpha
- **Background estimation:** Estimate what the background should look like
- **Machine learning:** Train a model to predict alpha values
- **Manual extraction:** Extract alpha from sample images

### 2. Variable Watermark Positions

**Problem:** Watermarks may appear in different locations.

**Solutions:**
- Template matching to find watermark location
- Edge detection to identify watermark boundaries
- User-specified regions

### 3. Complex Watermark Designs

**Problem:** Some watermarks have:
- Gradients and shadows
- Multiple colors
- Non-uniform opacity
- Text with anti-aliasing

**Solutions:**
- Multi-channel alpha estimation
- Adaptive thresholding
- Inpainting for complex cases

## 即梦AI Watermark Analysis

### Characteristics

From analyzing the sample image:

1. **Position:** Bottom-right corner
2. **Size:** Approximately 200×60 pixels
3. **Margins:** ~20px from edges
4. **Color:** White/light colored logo and text
5. **Opacity:** Semi-transparent (estimated α range: 0-0.95)

### Experimental Implementation

Created `remove_jimeng_watermark.py` with:

```python
# Estimate alpha from brightness
brightness = region.mean(axis=2)
alpha = np.clip((brightness - min_brightness) / (max_brightness - min_brightness), 0, 1)

# Apply reverse alpha blending
restored = (region - alpha_clamped * LOGO_VALUE) / one_minus_alpha
```

### Results

Initial testing shows:
- Mean pixel difference: 15.4
- Max pixel difference: 184.0
- 4,247 pixels changed significantly (>10 intensity)

## Limitations and Improvements

### Current Limitations

1. **Alpha estimation is approximate** - Without ground truth alpha maps, we're guessing
2. **May darken background** - If background is naturally bright, it gets incorrectly darkened
3. **Edge artifacts** - Sharp transitions can create visible edges
4. **Not perfect for complex backgrounds** - Works best on uniform backgrounds

### Potential Improvements

1. **Better Alpha Estimation:**
   - Use surrounding pixels to estimate local background
   - Apply Gaussian blur to smooth alpha transitions
   - Use edge-aware filtering

2. **Adaptive Processing:**
   - Detect background complexity
   - Adjust parameters based on local image statistics
   - Use different strategies for different regions

3. **Machine Learning Approach:**
   - Train a model on pairs of watermarked/clean images
   - Use deep learning for alpha matte estimation
   - Implement blind watermark removal networks

4. **Hybrid Approach:**
   - Combine alpha blending with inpainting
   - Use content-aware fill for difficult regions
   - Apply post-processing to smooth artifacts

## Generalization Strategy

To adapt this technique to other AI watermarks:

### Step 1: Analyze the Watermark

```python
# Extract watermark region
# Analyze position, size, color, opacity
# Determine if it's alpha-blended or overlaid
```

### Step 2: Estimate Alpha Map

```python
# Method 1: Brightness-based
alpha = (brightness - min_val) / (max_val - min_val)

# Method 2: Background estimation
background = estimate_background(surrounding_pixels)
alpha = (watermarked - background) / (logo - background)

# Method 3: Manual extraction
alpha = extract_from_clean_sample()
```

### Step 3: Apply Reverse Blending

```python
# Use the same formula as Gemini
original = (watermarked - alpha * logo_value) / (1 - alpha)
```

### Step 4: Refine Results

```python
# Apply smoothing, edge refinement, color correction
# Handle edge cases and artifacts
```

## Conclusion

The Gemini watermark removal technique **can be generalized** to other AI-generated watermarks, but with varying degrees of success:

**Works well when:**
- Watermark is alpha-blended (not hard-overlaid)
- Watermark is uniform color (especially white)
- Position is predictable
- Background is relatively uniform

**Challenging when:**
- No alpha map available (requires estimation)
- Complex watermark design
- Variable positioning
- Complex backgrounds

**Best approach:**
1. Start with reverse alpha blending (proven technique)
2. Estimate alpha from brightness or background
3. Refine with post-processing
4. For production use, consider ML-based approaches

The experimental 即梦AI remover shows promise but needs refinement for production use.
