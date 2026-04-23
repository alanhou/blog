from manim import *

class OpenVLThinkerV2Scene(Scene):
    def construct(self):
        # Title
        title = Text("OpenVLThinkerV2", font_size=36)
        subtitle = Text("Gaussian GRPO (G²RPO)", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("Multi-Task GRPO Problem", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Show imbalanced tasks
        task1 = Rectangle(width=2, height=0.8, color=BLUE, fill_opacity=0.3)
        task1_label = Text("Math\n(sparse)", font_size=14)
        task1_label.move_to(task1)
        task1_group = VGroup(task1, task1_label)
        task1_group.shift(LEFT * 3 + UP * 0.5)

        task2 = Rectangle(width=2, height=0.8, color=GREEN, fill_opacity=0.3)
        task2_label = Text("Grounding\n(dense)", font_size=14)
        task2_label.move_to(task2)
        task2_group = VGroup(task2, task2_label)
        task2_group.shift(LEFT * 3 + DOWN * 0.5)

        # Gradient sizes
        grad1 = Arrow(task1.get_right(), task1.get_right() + RIGHT * 3, color=BLUE, buff=0)
        grad1_label = Text("Large gradient", font_size=14, color=BLUE)
        grad1_label.next_to(grad1, UP, buff=0.1)

        grad2 = Arrow(task2.get_right(), task2.get_right() + RIGHT * 0.5, color=GREEN, buff=0)
        grad2_label = Text("Small gradient", font_size=14, color=GREEN)
        grad2_label.next_to(grad2, DOWN, buff=0.1)

        imbalance_text = Text("Inter-task imbalance!", font_size=20, color=RED)
        imbalance_text.shift(RIGHT * 2.5 + DOWN * 1.5)

        self.play(
            FadeIn(task1_group),
            FadeIn(task2_group)
        )
        self.play(
            Create(grad1), Write(grad1_label),
            Create(grad2), Write(grad2_label)
        )
        self.play(Write(imbalance_text))
        self.wait(1.5)

        self.play(
            FadeOut(problem_title),
            FadeOut(task1_group), FadeOut(task2_group),
            FadeOut(grad1), FadeOut(grad1_label),
            FadeOut(grad2), FadeOut(grad2_label),
            FadeOut(imbalance_text)
        )

        # The Solution: Optimal Transport
        solution_title = Text("G²RPO: Optimal Transport", font_size=28, color=GREEN)
        solution_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Show distribution transformation
        before_dist = VGroup(
            Text("Any Distribution", font_size=18),
            Text("(heavy-tail, bimodal)", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        before_box = SurroundingRectangle(before_dist, color=RED, buff=0.3)
        before_group = VGroup(before_box, before_dist)
        before_group.shift(LEFT * 3)

        after_dist = VGroup(
            Text("N(0,1)", font_size=24, color=GREEN, weight=BOLD),
            Text("Standard Normal", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        after_box = SurroundingRectangle(after_dist, color=GREEN, buff=0.3)
        after_group = VGroup(after_box, after_dist)
        after_group.shift(RIGHT * 3)

        transform_arrow = Arrow(before_box.get_right(), after_box.get_left(), buff=0.1, color=YELLOW)
        transform_label = Text("Optimal\nTransport", font_size=16, color=YELLOW)
        transform_label.next_to(transform_arrow, UP)

        self.play(FadeIn(before_group))
        self.play(
            Create(transform_arrow),
            Write(transform_label)
        )
        self.play(FadeIn(after_group))
        self.wait(1.5)

        self.play(
            FadeOut(solution_title),
            FadeOut(before_group),
            FadeOut(after_group),
            FadeOut(transform_arrow),
            FadeOut(transform_label)
        )

        # Key Benefits
        benefits_title = Text("Key Benefits", font_size=28, color=BLUE)
        benefits_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(benefits_title))
        self.wait(0.3)

        benefits = VGroup(
            Text("✓ Inter-task gradient equity", font_size=20, color=GREEN),
            Text("✓ Outlier robustness", font_size=20, color=GREEN),
            Text("✓ Symmetric updates", font_size=20, color=GREEN),
            Text("✓ All tasks → N(0,1)", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        benefits.next_to(benefits_title, DOWN, buff=0.5)

        self.play(Write(benefits, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(benefits_title), FadeOut(benefits))

        # Results
        results_title = Text("Results", font_size=28, color=YELLOW)
        results_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(results_title))
        self.wait(0.3)

        results = VGroup(
            Text("MMMU: 71.6%", font_size=22, color=GREEN),
            Text("MathVista: 79.5%", font_size=22, color=GREEN),
            Text("", font_size=16),
            Text("+18.9% over baseline", font_size=24, color=YELLOW, weight=BOLD),
            Text("", font_size=16),
            Text("Surpasses GPT-4o & Gemini 2.5 Pro", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        results.next_to(results_title, DOWN, buff=0.5)

        self.play(Write(results, run_time=2.5))
        self.wait(2)

        self.play(FadeOut(results_title), FadeOut(results))

        # Conclusion
        conclusion = VGroup(
            Text("G²RPO:", font_size=28, color=GREEN),
            Text("Balanced Multi-Task Learning", font_size=24)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
