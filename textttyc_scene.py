from manim import *

class TextTTYCScene(Scene):
    def construct(self):
        title = Text("TextTTYC-Bench", font_size=36)
        subtitle = Text("Benchmarking AI Agents", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        content = VGroup(
            Text("Terminal-based benchmark for AI agents", font_size=20),
            Text("", font_size=14),
            Text("Tests:", font_size=22, color=BLUE),
            Text("• Command-line interaction", font_size=18),
            Text("• Tool usage", font_size=18),
            Text("• Task completion", font_size=18),
            Text("", font_size=14),
            Text("Real-world CLI scenarios", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(content, run_time=2))
        self.wait(2)
        self.play(FadeOut(content), FadeOut(title_group))
