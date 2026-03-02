#!/usr/bin/env python3
"""Remove Gemini's visible watermark from images using reverse alpha blending."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# Constants matching the JS source
ALPHA_THRESHOLD = 0.002
MAX_ALPHA = 0.99
LOGO_VALUE = 255.0


def calculate_alpha_map(bg_path: Path) -> np.ndarray:
    """Load a reference background PNG and compute an alpha map.

    The alpha at each pixel is max(R, G, B) / 255, stored as float32.
    """
    bg = np.asarray(Image.open(bg_path).convert("RGB"), dtype=np.float32)
    return bg.max(axis=2) / 255.0


def detect_watermark_config(width: int, height: int) -> dict:
    """Choose watermark size and margin based on image dimensions."""
    if width > 1024 and height > 1024:
        return {"logo_size": 96, "margin_right": 64, "margin_bottom": 64}
    return {"logo_size": 48, "margin_right": 32, "margin_bottom": 32}


def calculate_watermark_position(width: int, height: int, config: dict) -> dict:
    """Compute the top-left corner and size of the watermark region."""
    size = config["logo_size"]
    return {
        "x": width - config["margin_right"] - size,
        "y": height - config["margin_bottom"] - size,
        "width": size,
        "height": size,
    }


def remove_watermark(image: Image.Image) -> Image.Image:
    """Remove the Gemini watermark from an image.

    Uses vectorized reverse alpha blending: original = (watermarked - a * 255) / (1 - a)
    """
    width, height = image.size
    config = detect_watermark_config(width, height)
    pos = calculate_watermark_position(width, height, config)

    bg_path = ASSETS_DIR / f"bg_{config['logo_size']}.png"
    if not bg_path.exists():
        raise FileNotFoundError(f"Reference background not found: {bg_path}")

    alpha_map = calculate_alpha_map(bg_path)

    img_array = np.asarray(image.convert("RGB"), dtype=np.float32)
    result = img_array.copy()

    x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
    region = result[y : y + h, x : x + w, :]

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
    """Remove watermark from a file. Overwrites in-place if no output_path given."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    image = Image.open(input_path)
    cleaned = remove_watermark(image)

    dest = Path(output_path) if output_path else input_path
    cleaned.save(dest)
    print(f"  Saved {dest}")
    return dest


def main():
    parser = argparse.ArgumentParser(
        description="Remove Gemini watermark from images."
    )
    parser.add_argument("images", nargs="+", help="Input image path(s)")
    parser.add_argument("-o", "--output", help="Output path (single image only)")
    args = parser.parse_args()

    if args.output and len(args.images) > 1:
        parser.error("-o/--output can only be used with a single input image")

    for path in args.images:
        try:
            process_file(path, args.output)
        except Exception as e:
            print(f"  Error processing {path}: {e}")


if __name__ == "__main__":
    main()
