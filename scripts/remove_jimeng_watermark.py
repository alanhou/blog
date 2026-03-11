#!/usr/bin/env python3
"""Remove 即梦AI (Jimeng AI) watermark from images using reverse alpha blending.

This is an experimental approach based on the Gemini watermark removal technique.
The key challenge is that we don't have a pre-computed alpha map, so we need to
estimate it from the watermarked image itself.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

# Watermark detection parameters
# 即梦AI watermark is 551x182 pixels in the bottom right corner
WATERMARK_CONFIG = {
    "logo_width": 551,
    "logo_height": 182,
}

# Brightness threshold for detecting watermark pixels
BRIGHTNESS_THRESHOLD = 180


def estimate_alpha_from_brightness(region: np.ndarray, brightness_threshold: float = 180) -> np.ndarray:
    """Detect watermark pixels based on brightness.

    Returns a binary mask where True indicates watermark pixels (bright pixels).
    """
    brightness = region.mean(axis=2)
    return brightness > brightness_threshold


def detect_watermark_region(image: Image.Image) -> dict:
    """Detect the watermark region in the image.

    For 即梦AI, the watermark is 551x182 pixels in the bottom right corner.
    """
    width, height = image.size
    config = WATERMARK_CONFIG

    return {
        "x": width - config["logo_width"],
        "y": height - config["logo_height"],
        "width": config["logo_width"],
        "height": config["logo_height"],
    }


def remove_watermark(image: Image.Image, background_estimate: str = "local") -> Image.Image:
    """Remove the 即梦AI watermark from an image.

    Uses an aggressive inpainting approach: replaces watermark pixels
    by sampling from the surrounding non-watermark area.

    Args:
        image: Input image with watermark
        background_estimate: Unused, kept for compatibility

    Returns:
        Image with watermark removed
    """
    width, height = image.size
    pos = detect_watermark_region(image)

    img_array = np.asarray(image.convert("RGB"), dtype=np.uint8)
    result = img_array.copy()

    x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
    region = result[y : y + h, x : x + w, :].copy()

    # Detect watermark pixels (bright pixels)
    watermark_mask = estimate_alpha_from_brightness(region.astype(np.float32))

    print(f"Removing {watermark_mask.sum()} watermark pixels...")

    # Get background samples from areas around the watermark (not inside it)
    # Sample from left, top, and top-left of watermark region
    background_samples = []

    # Sample from left side (50 pixels wide strip)
    if x > 50:
        left_strip = result[y:y+h, x-50:x, :]
        background_samples.append(left_strip.reshape(-1, 3))

    # Sample from top (50 pixels tall strip)
    if y > 50:
        top_strip = result[y-50:y, x:x+w, :]
        background_samples.append(top_strip.reshape(-1, 3))

    if background_samples:
        background_pixels = np.vstack(background_samples)

        # Replace each watermark pixel with a random sample from background
        for row in range(h):
            for col in range(w):
                if watermark_mask[row, col]:
                    # Pick a random background pixel
                    idx = np.random.randint(0, len(background_pixels))
                    region[row, col] = background_pixels[idx]
    else:
        # Fallback: use nearby non-watermark pixels
        for row in range(h):
            for col in range(w):
                if watermark_mask[row, col]:
                    # Look in larger radius
                    for radius in [15, 30, 50]:
                        row_min = max(0, row - radius)
                        row_max = min(h, row + radius + 1)
                        col_min = max(0, col - radius)
                        col_max = min(w, col + radius + 1)

                        window = region[row_min:row_max, col_min:col_max, :]
                        window_mask = watermark_mask[row_min:row_max, col_min:col_max]
                        dark_mask = ~window_mask

                        if dark_mask.any():
                            for c in range(3):
                                dark_values = window[:, :, c][dark_mask]
                                if len(dark_values) > 0:
                                    region[row, col, c] = np.median(dark_values)
                            break

    result[y : y + h, x : x + w, :] = region

    return Image.fromarray(result, "RGB")


def process_file(input_path: str | Path, output_path: str | Path | None = None) -> Path:
    """Remove watermark from a file."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    image = Image.open(input_path)
    cleaned = remove_watermark(image)

    if output_path:
        dest = Path(output_path)
    else:
        # Default: add "-cleaned" suffix
        stem = input_path.stem
        dest = input_path.parent / f"{stem}-cleaned{input_path.suffix}"

    cleaned.save(dest)
    print(f"Saved cleaned image to: {dest}")
    return dest


def main():
    parser = argparse.ArgumentParser(
        description="Remove 即梦AI watermark from images (experimental)."
    )
    parser.add_argument("images", nargs="+", help="Input image path(s)")
    parser.add_argument("-o", "--output", help="Output path (single image only)")
    parser.add_argument(
        "--method",
        choices=["brightness", "local"],
        default="brightness",
        help="Background estimation method"
    )
    args = parser.parse_args()

    if args.output and len(args.images) > 1:
        parser.error("-o/--output can only be used with a single input image")

    for path in args.images:
        try:
            process_file(path, args.output)
        except Exception as e:
            print(f"Error processing {path}: {e}")


if __name__ == "__main__":
    main()
