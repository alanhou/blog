from manim import *

class DemystifyingOPDScene(Scene):
    def construct(self):
        title = Text("Demystifying OPD", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Problem
        problem = VGroup(
            Text("On-Policy Distillation Problem:", font_size=24, color=RED),
            Text("", font_size=14),
            Text("Repetitive tokens → Length inflation", font_size=20),
            Text("→ Training collapse", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.2)
        self.play(Write(problem))
        self.wait(1.5)
        self.play(FadeOut(problem))

        # Solution
        solution = VGroup(
            Text("Stable-OPD Solution:", font_size=24, color=GREEN),
            Text("", font_size=14),
            Text("✓ Divergence constraint", font_size=20, color=GREEN),
            Text("✓ Rollout mixture", font_size=20, color=GREEN),
            Text("", font_size=14),
            Text("Prevents repetition saturation", font_size=18)
        ).arrange(DOWN, buff=0.2)
        self.play(Write(solution))
        self.wait(2)
        self.play(FadeOut(solution), FadeOut(title))
