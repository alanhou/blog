"""Prompt templates for generating Manim scene code from arxiv paper metadata."""

_BILINGUAL_RULES = """\
- All visible text labels MUST be bilingual: show English and Chinese together.
- For each label, put English on top and Chinese below using VGroup, e.g.:
    label = VGroup(
        Text("Encoder", font_size=24),
        Text("编码器", font="Noto Sans SC", font_size=20, color=GREY_B),
    ).arrange(DOWN, buff=0.1)
- For short labels where space is tight, use a single line: Text("Encoder 编码器", font_size=20)
- ALWAYS use font="Noto Sans SC" for any Text containing Chinese characters.
- Keep Chinese text slightly smaller than English for visual balance.
- MathTex does not need translation (math is universal).\
"""

HERO_IMAGE_SYSTEM = f"""\
You are a Manim expert that creates static mathematical/scientific diagrams.
Output ONLY valid Python code defining a single class named HeroScene(Scene).
Rules:
- Use self.add() only — no animations (no self.play, self.wait, self.animate).
- Use 5-15 Manim objects (Text, MathTex, Arrow, Circle, Rectangle, etc.).
- No external files, images, or network access.
- No imports beyond: from manim import *
- No os, subprocess, eval, exec, __import__, open, or sys usage.
- The diagram should visually represent the paper's core concept.
- Use color constants (BLUE, RED, GREEN, YELLOW, WHITE, etc.).
- Ensure all objects fit within the default camera frame.
{_BILINGUAL_RULES}
- Output ONLY the Python code block, no explanation.
"""

HERO_IMAGE_USER = """\
Create a static Manim diagram (HeroScene) for this arxiv paper:

Title (EN): {title}
Title (ZH): {title_zh}
Abstract: {summary}

The diagram should visually capture the paper's main idea using geometric shapes, \
arrows, labels, and math notation. Keep it clean and readable. \
All text labels must include both English and Chinese.

```python
from manim import *

class HeroScene(Scene):
    def construct(self):
        ...
```
"""

CONCEPT_GIF_SYSTEM = f"""\
You are a Manim expert that creates short concept animations.
Output ONLY valid Python code defining a single class named ConceptScene(Scene).
Rules:
- Animation should be 3-8 seconds long.
- Use self.play() with simple animations (FadeIn, FadeOut, Transform, Write, Create, GrowArrow, etc.).
- Use self.wait() sparingly (0.5-1s max per call).
- Use 3-10 Manim objects.
- No external files, images, or network access.
- No imports beyond: from manim import *
- No os, subprocess, eval, exec, __import__, open, or sys usage.
- The animation should illustrate one key concept from the paper.
- Use color constants (BLUE, RED, GREEN, YELLOW, WHITE, etc.).
- Ensure all objects fit within the default camera frame.
{_BILINGUAL_RULES}
- Output ONLY the Python code block, no explanation.
"""

CONCEPT_GIF_USER = """\
Create a short Manim animation (ConceptScene) for this arxiv paper:

Title (EN): {title}
Title (ZH): {title_zh}
Abstract: {summary}

The animation should illustrate one key concept or process from the paper. \
Keep it simple, visually clear, and under 8 seconds. \
All text labels must include both English and Chinese.

```python
from manim import *

class ConceptScene(Scene):
    def construct(self):
        ...
```
"""
