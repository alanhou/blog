from manim import *

class TPOScene(Scene):
    def construct(self):
        # Title
        title = Text("Target Policy Optimization (TPO)", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Coupling Problem", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        problem_text = VGroup(
            Text("Standard Policy Gradient:", font_size=20),
            Text("", font_size=14),
            Text("What to learn + How to learn", font_size=18, color=YELLOW),
            Text("= Coupled together", font_size=18, color=YELLOW),
            Text("", font_size=14),
            Text("→ Overshooting/Undershooting", font_size=18, color=RED)
        ).arrange(DOWN, buff=0.2)
        problem_text.next_to(problem_title, DOWN, buff=0.5)

        self.play(Write(problem_text, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(problem_title), FadeOut(problem_text))

        # TPO Solution
        solution_title = Text("TPO: Decouple the Two", font_size=28, color=GREEN)
        solution_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Two phases
        phase1 = Rectangle(width=5, height=2, color=BLUE, fill_opacity=0.2)
        phase1_title = Text("Phase 1: What to Learn", font_size=20, color=BLUE)
        phase1_title.move_to(phase1.get_top() + DOWN * 0.3)
        phase1_desc = VGroup(
            Text("Construct target", font_size=16),
            Text("distribution q", font_size=16),
            Text("q ∝ p^old × exp(u)", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.15)
        phase1_desc.move_to(phase1.get_center() + DOWN * 0.2)
        phase1_group = VGroup(phase1, phase1_title, phase1_desc)
        phase1_group.shift(LEFT * 3)

        phase2 = Rectangle(width=5, height=2, color=PURPLE, fill_opacity=0.2)
        phase2_title = Text("Phase 2: How to Learn", font_size=20, color=PURPLE)
        phase2_title.move_to(phase2.get_top() + DOWN * 0.3)
        phase2_desc = VGroup(
            Text("Fit policy to target", font_size=16),
            Text("via cross-entropy", font_size=16),
            Text("minimize -Σq log p", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.15)
        phase2_desc.move_to(phase2.get_center() + DOWN * 0.2)
        phase2_group = VGroup(phase2, phase2_title, phase2_desc)
        phase2_group.shift(RIGHT * 3)

        arrow = Arrow(phase1.get_right(), phase2.get_left(), buff=0.1, color=YELLOW)

        self.play(FadeIn(phase1_group))
        self.play(Create(arrow))
        self.play(FadeIn(phase2_group))
        self.wait(2)

        self.play(
            FadeOut(solution_title),
            FadeOut(phase1_group),
            FadeOut(phase2_group),
            FadeOut(arrow)
        )

        # Key Benefits
        benefits_title = Text("Key Benefits", font_size=28, color=YELLOW)
        benefits_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(benefits_title))
        self.wait(0.3)

        benefits = VGroup(
            Text("✓ Explicit target distribution", font_size=20, color=GREEN),
            Text("✓ No clipping needed", font_size=20, color=GREEN),
            Text("✓ No KL penalties in loss", font_size=20, color=GREEN),
            Text("✓ Supervised learning step", font_size=20, color=GREEN),
            Text("", font_size=16),
            Text("Better on sparse rewards!", font_size=22, color=YELLOW, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        benefits.next_to(benefits_title, DOWN, buff=0.5)

        self.play(Write(benefits, run_time=2.5))
        self.wait(2)

        self.play(FadeOut(benefits_title), FadeOut(benefits))

        # Conclusion
        conclusion = VGroup(
            Text("TPO:", font_size=28, color=GREEN),
            Text("Decouple What from How", font_size=24)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
