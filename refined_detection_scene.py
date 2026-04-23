from manim import *

class RefinedDetectionScene(Scene):
    def construct(self):
        title = Text("Refined Detection for Gumbel Watermarking", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        content = VGroup(
            Text("Gumbel Watermarking:", font_size=22, color=BLUE),
            Text("Embeds detectable patterns in LLM outputs", font_size=18),
            Text("", font_size=14),
            Text("Challenge:", font_size=22, color=RED),
            Text("Detection accuracy vs robustness", font_size=18),
            Text("", font_size=14),
            Text("Refined Detection:", font_size=22, color=GREEN),
            Text("Improved statistical methods", font_size=18)
        ).arrange(DOWN, buff=0.2)
        self.play(Write(content, run_time=2.5))
        self.wait(2)
        self.play(FadeOut(content), FadeOut(title))
