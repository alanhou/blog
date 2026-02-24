#!/usr/bin/env python3
"""Render Manim scenes to static images and GIFs for arxiv blog visuals."""

import ast
import shutil
import subprocess
import tempfile
from pathlib import Path

VISUALS_DIR = Path(__file__).resolve().parent.parent / "public" / "arxiv-visuals"
RENDER_TIMEOUT = 120

DANGEROUS_NAMES = frozenset({
    "os", "subprocess", "eval", "exec", "__import__", "open", "sys",
    "shutil", "pathlib", "importlib", "compile", "globals", "locals",
    "getattr", "setattr", "delattr", "breakpoint",
})


def validate_scene_code(code: str) -> bool:
    """Static checks: valid syntax, no dangerous imports/calls."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        # Block dangerous imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in DANGEROUS_NAMES:
                    return False
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in DANGEROUS_NAMES:
                return False
        # Block dangerous function calls
        if isinstance(node, ast.Call):
            func = node.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name in DANGEROUS_NAMES:
                return False

    return True


def render_scene(scene_code: str, scene_class_name: str, output_dir: Path,
                 output_format: str = "png") -> Path | None:
    """Write scene code to temp dir, run manim render, copy output.

    Args:
        scene_code: Valid Python source defining the scene class.
        scene_class_name: Name of the Scene subclass to render.
        output_dir: Destination directory (e.g. public/arxiv-visuals/{slug}/).
        output_format: "png" for static image, "gif" for animation.

    Returns:
        Path to the output file, or None on any failure.
    """
    if not validate_scene_code(scene_code):
        print(f"  Scene code failed validation for {scene_class_name}")
        return None

    fmt_flag = "--format=png" if output_format == "png" else "--format=gif"
    quality_flag = "-ql"  # low quality for speed

    with tempfile.TemporaryDirectory() as tmpdir:
        scene_file = Path(tmpdir) / "scene.py"
        scene_file.write_text(scene_code)

        cmd = [
            "manim", "render", quality_flag, fmt_flag,
            str(scene_file), scene_class_name,
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=RENDER_TIMEOUT,
                cwd=tmpdir,
            )
        except subprocess.TimeoutExpired:
            print(f"  Manim render timed out for {scene_class_name}")
            return None
        except FileNotFoundError:
            print("  Manim not found in PATH")
            return None

        if result.returncode != 0:
            print(f"  Manim render failed for {scene_class_name}:")
            print(f"  {result.stderr[-500:] if result.stderr else 'no stderr'}")
            return None

        # Find the rendered output
        media_dir = Path(tmpdir) / "media"
        ext = "png" if output_format == "png" else "gif"
        outputs = list(media_dir.rglob(f"*.{ext}"))
        if not outputs:
            print(f"  No .{ext} output found for {scene_class_name}")
            return None

        # Copy to destination
        output_dir.mkdir(parents=True, exist_ok=True)
        dest = output_dir / f"{scene_class_name}.{ext}"
        shutil.copy2(outputs[0], dest)
        print(f"  Rendered {dest}")
        return dest


if __name__ == "__main__":
    # Quick smoke test
    test_code = '''from manim import *

class HeroScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        label = Text("Test").scale(0.5)
        self.add(circle, label)
'''
    out = Path(__file__).resolve().parent.parent / "public" / "arxiv-visuals" / "_test"
    result = render_scene(test_code, "HeroScene", out, "png")
    if result:
        print(f"Success: {result}")
    else:
        print("Render failed (is manim installed?)")
