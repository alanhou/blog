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

# Watermark detection parameters (may need tuning)
WATERMARK_CONFIG = {
    "logo_width": 200,
    "logo_height": 60,
    "margin_right": 20,
    "margin_bottom": 20,
}

# Alpha blending parameters
ALPHA_THRESHOLD = 0.01
MAX_ALPHA = 0.95
LOGO_VALUE = 255.0  # Assuming white watermark


def estimate_alpha_from_brightness(region: np.ndarray, min_brightness: float = 100, max_brightness: float = 255) -> np.ndarray:
    """Estimate alpha channel from brightness.

    This assumes the watermark is lighter than the background.
    Higher brightness = higher alpha (more watermark).
    """
    brightness = region.mean(axis=2)
    alpha = np.clip((brightness - min_brightness) / (max_brightness - min_brightness), 0, 1)
    return alpha


def detect_watermark_region(image: Image.Image) -> dict:
    """Detect the watermark region in the image.

    For 即梦AI, the watermark is typically in the bottom-right corner.
    """
    width, height = image.size
    config = WATERMARK_CONFIG

    return {
        "x": width - config["margin_right"] - config["logo_width"],
        "y": height - config["margin_bottom"] - config["logo_height"],
        "width": config["logo_width"],
        "height": config["logo_height"],
    }


def remove_watermark(image: Image.Image, background_estimate: str = "local") -> Image.Image:
    """Remove the 即梦AI watermark from an image.

    Args:
        image: Input image with watermark
        background_estimate: Method to estimate background
            - "local": Use surrounding pixels to estimate background
            - "brightness": Use brightness-based alpha estimation

    Returns:
        Image with watermark removed
    """
    width, height = image.size
    pos = detect_watermark_region(image)

    img_array = np.asarray(image.convert("RGB"), dtype=np.float32)
    result = img_array.copy()

    x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
    region = result[y : y + h, x : x + w, :]

    if background_estimate == "brightness":
        # Method 1: Estimate alpha from brightness
        alpha_map = estimate_alpha_from_brightness(region)
    else:
        # Method 2: Estimate background from surrounding pixels
        # This is more sophisticated but requires more computation
        # For now, fall back to brightness method
        alpha_map = estimate_alpha_from_brightness(region)

    # Broadcast alpha to (h, w, 1) for per-channel operation
    alpha = alpha_map[:, :, np.newaxis]

    # Build mask: only process pixels above threshold
    mask = alpha_map >= ALPHA_THRESHOLD

    # Clamp alpha for division safety
    alpha_clamped = np.clip(alpha, 0.0, MAX_ALPHA)
    one_minus_alpha = 1.0 - alpha_clamped

    # Reverse alpha blending: original = (watermarked - alpha * LOGO_VALUE) / (1 - alpha)
    restored = (region - alpha_clamped * LOGO_VALUE) / one_minus_alpha

    # Apply only where alpha is significant
    mask_3d = mask[:, :, np.newaxis]
    region[:] = np.where(mask_3d, np.clip(np.round(restored), 0, 255), region)

    return Image.fromarray(result.astype(np.uint8), "RGB")


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
