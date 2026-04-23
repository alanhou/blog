#!/usr/bin/env python3
"""Generate styled cover images for arxiv blog posts."""

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Post titles and slugs
posts = [
    ("Act Wisely: Meta-Cognitive Tool Use", "act-wisely-cultivating-meta-cognitive-tool"),
    ("Ads in AI Chatbots: An Analysis", "ads-in-ai-chatbots-an-analysis"),
    ("BAS: Decision-Theoretic LLM Confidence", "bas-a-decision-theoretic-approach-to"),
    ("ClawBench: Real-World AI Agents", "clawbench-can-ai-agents-complete-everyday"),
    ("Demystifying OPD: Length Inflation", "demystifying-opd-length-inflation-and-stabilization"),
    ("Faithful GRPO: Visual Reasoning", "faithful-grpo-improving-visual-spatial-reasoning"),
    ("Gradient Boosting in Attention", "gradient-boosting-within-a-single-attention"),
    ("Meta-Learning: Training-Free Brain Decoding", "meta-learning-in-context-enables-training-free"),
    ("OpenVLThinkerV2: Multimodal Reasoning", "openvlthinkerv2-a-generalist-multimodal-reasoning"),
    ("PIArena: Prompt Injection Platform", "piarena-a-platform-for-prompt-injection"),
    ("Ψ: Shared State for AI Instruments", "psi-shared-state-for-coherent-ai-instruments"),
    ("Refined Detection: Gumbel Watermarking", "refined-detection-for-gumbel-watermarking"),
    ("Seeing But Not Thinking: Routing Distraction", "seeing-but-not-thinking-routing-distraction"),
    ("SUPERNOVA: General Reasoning via RLVR", "supernova-eliciting-general-reasoning-in-llms"),
    ("Target Policy Optimization", "target-policy-optimization"),
    ("TextTTYC-Bench: AI Agent Benchmark", "textttyc-bench-benchmarking-ai-agents-for"),
    ("What Drives Representation Steering?", "what-drives-representation-steering-a-mechanistic"),
]

# Color schemes (gradient backgrounds)
colors = [
    ("#667eea", "#764ba2"),  # Purple gradient
    ("#f093fb", "#f5576c"),  # Pink gradient
    ("#4facfe", "#00f2fe"),  # Blue gradient
    ("#43e97b", "#38f9d7"),  # Green gradient
    ("#fa709a", "#fee140"),  # Warm gradient
]

def create_gradient(width, height, color1, color2):
    """Create a vertical gradient."""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def create_cover_image(title, slug, color_idx):
    """Create a styled cover image."""
    width, height = 1200, 630
    color1, color2 = colors[color_idx % len(colors)]

    # Create gradient background
    img = create_gradient(width, height, color1, color2)
    draw = ImageDraw.Draw(img)

    # Try to load a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # Add "arXiv Paper" label at top
    label_text = "arXiv Paper"
    label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((width - label_width) // 2, 80), label_text, fill="white", font=label_font)

    # Wrap and draw title
    wrapped_lines = textwrap.wrap(title, width=25)
    y_offset = 250

    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_offset), line, fill="white", font=title_font)
        y_offset += 90

    # Save
    output_path = f"public/arxiv-visuals/arxiv-{slug}.png"
    img.save(output_path, "PNG")
    print(f"✓ Created: {output_path}")

# Generate all cover images
for idx, (title, slug) in enumerate(posts):
    create_cover_image(title, slug, idx)

print(f"\n✓ Generated {len(posts)} cover images!")
