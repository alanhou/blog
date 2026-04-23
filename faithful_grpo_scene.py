from manim import *

class FaithfulGRPOScene(Scene):
    def construct(self):
        # Title
        title = Text("Faithful GRPO", font_size=36)
        subtitle = Text("Constrained Policy Optimization", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Accuracy-Faithfulness Gap", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Show the tradeoff
        accuracy = Text("High Accuracy ✓", font_size=22, color=GREEN)
        accuracy.shift(UP * 0.5)

        but_text = Text("BUT", font_size=24, color=YELLOW, weight=BOLD)
        but_text.next_to(accuracy, DOWN, buff=0.3)

        problems = VGroup(
            Text("• Logical inconsistency", font_size=18, color=RED),
            Text("• Visual ungroundedness", font_size=18, color=RED),
            Text("• Flawed reasoning", font_size=18, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problems.next_to(but_text, DOWN, buff=0.3)

        self.play(Write(accuracy))
        self.play(Write(but_text))
        self.play(Write(problems, run_time=1.5))
        self.wait(1)

        self.play(
            FadeOut(problem_title),
            FadeOut(accuracy),
            FadeOut(but_text),
            FadeOut(problems)
        )

        # Two Failure Modes
        failure_title = Text("Two Failure Modes", font_size=28, color=ORANGE)
        failure_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(failure_title))
        self.wait(0.3)

        # Mode 1
        mode1 = Rectangle(width=5.5, height=2, color=BLUE, fill_opacity=0.2)
        mode1_label = Text("1. Logical Inconsistency", font_size=18, color=BLUE)
        mode1_label.move_to(mode1.get_top() + DOWN * 0.3)
        mode1_desc = Text("Reasoning → Answer A\nFinal Answer: B", font_size=16)
        mode1_desc.move_to(mode1.get_center() + DOWN * 0.3)
        mode1_group = VGroup(mode1, mode1_label, mode1_desc)
        mode1_group.shift(LEFT * 3.2)

        # Mode 2
        mode2 = Rectangle(width=5.5, height=2, color=PURPLE, fill_opacity=0.2)
        mode2_label = Text("2. Visual Ungroundedness", font_size=18, color=PURPLE)
        mode2_label.move_to(mode2.get_top() + DOWN * 0.3)
        mode2_desc = Text("Reasoning contradicts\nvisual evidence", font_size=16)
        mode2_desc.move_to(mode2.get_center() + DOWN * 0.3)
        mode2_group = VGroup(mode2, mode2_label, mode2_desc)
        mode2_group.shift(RIGHT * 3.2)

        self.play(
            FadeIn(mode1_group),
            FadeIn(mode2_group)
        )
        self.wait(1.5)

        self.play(
            FadeOut(failure_title),
            FadeOut(mode1_group),
            FadeOut(mode2_group)
        )

        # The Solution
        solution_title = Text("Faithful GRPO Solution", font_size=28, color=GREEN)
        solution_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Constrained optimization
        constraints = VGroup(
            Text("Hard Constraints:", font_size=22, color=YELLOW),
            Text("", font_size=16),
            Text("✓ Logical consistency", font_size=20, color=GREEN),
            Text("✓ Visual grounding", font_size=20, color=GREEN),
            Text("", font_size=16),
            Text("Enforced during optimization", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        constraints.next_to(solution_title, DOWN, buff=0.5)

        self.play(Write(constraints, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(solution_title), FadeOut(constraints))

        # Results
        results_title = Text("Results", font_size=28, color=YELLOW)
        results_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(results_title))
        self.wait(0.3)

        # Before/After comparison
        before_box = Rectangle(width=3, height=2.5, color=RED, fill_opacity=0.2)
        before_label = Text("GRPO", font_size=20, color=RED)
        before_label.move_to(before_box.get_top() + DOWN * 0.3)
        before_stats = VGroup(
            Text("Inconsistency:", font_size=16),
            Text("24.5%", font_size=24, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        before_stats.move_to(before_box.get_center())
        before_group = VGroup(before_box, before_label, before_stats)
        before_group.shift(LEFT * 3)

        after_box = Rectangle(width=3, height=2.5, color=GREEN, fill_opacity=0.2)
        after_label = Text("Faithful GRPO", font_size=20, color=GREEN)
        after_label.move_to(after_box.get_top() + DOWN * 0.3)
        after_stats = VGroup(
            Text("Inconsistency:", font_size=16),
            Text("1.7%", font_size=24, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        after_stats.move_to(after_box.get_center())
        after_group = VGroup(after_box, after_label, after_stats)
        after_group.shift(RIGHT * 3)

        arrow = Arrow(before_box.get_right(), after_box.get_left(), buff=0.2, color=YELLOW)
        improvement = Text("14x reduction!", font_size=18, color=YELLOW)
        improvement.next_to(arrow, UP)

        self.play(FadeIn(before_group))
        self.play(
            Create(arrow),
            Write(improvement),
            FadeIn(after_group)
        )
        self.wait(2)

        self.play(
            FadeOut(results_title),
            FadeOut(before_group),
            FadeOut(after_group),
            FadeOut(arrow),
            FadeOut(improvement)
        )

        # Conclusion
        conclusion = VGroup(
            Text("Faithful GRPO:", font_size=28, color=GREEN),
            Text("Accuracy + Trustworthy Reasoning", font_size=24)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
