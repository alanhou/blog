from manim import *

class BASScene(Scene):
    def construct(self):
        # Title
        title = Text("BAS: Behavioral Alignment Score", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Calibration Problem", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        problem_text = VGroup(
            Text("ECE (Expected Calibration Error):", font_size=20),
            Text("Measures average calibration", font_size=18, color=GRAY),
            Text("", font_size=14),
            Text("BUT ignores:", font_size=20, color=RED),
            Text("• When to abstain", font_size=18, color=RED),
            Text("• Risk preferences", font_size=18, color=RED),
            Text("• Asymmetric costs", font_size=18, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problem_text.next_to(problem_title, DOWN, buff=0.5)

        self.play(Write(problem_text, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(problem_title), FadeOut(problem_text))

        # BAS Solution
        solution_title = Text("BAS: Answer-or-Abstain Utility", font_size=26, color=GREEN)
        solution_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Utility function
        utility_box = Rectangle(width=7, height=3, color=BLUE, fill_opacity=0.1)
        utility_content = VGroup(
            Text("Utility Function:", font_size=22, color=YELLOW),
            Text("", font_size=14),
            Text("Correct answer: +1", font_size=18, color=GREEN),
            Text("Abstain: 0", font_size=18, color=GRAY),
            Text("Wrong answer: -C", font_size=18, color=RED),
            Text("", font_size=14),
            Text("(C = cost of error)", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        utility_content.move_to(utility_box)
        utility_group = VGroup(utility_box, utility_content)

        self.play(FadeIn(utility_group))
        self.wait(2)

        self.play(FadeOut(solution_title), FadeOut(utility_group))

        # Key Insight
        insight_title = Text("Key Insight", font_size=28, color=BLUE)
        insight_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(insight_title))
        self.wait(0.3)

        insight = VGroup(
            Text("BAS measures utility across", font_size=20),
            Text("ALL risk thresholds", font_size=22, color=YELLOW, weight=BOLD),
            Text("", font_size=14),
            Text("Area Under Utility Curve", font_size=20, color=GREEN),
            Text("", font_size=14),
            Text("Rewards models that know", font_size=18),
            Text("when to abstain", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        insight.next_to(insight_title, DOWN, buff=0.5)

        self.play(Write(insight, run_time=2.5))
        self.wait(2)

        self.play(FadeOut(insight_title), FadeOut(insight))

        # Comparison
        comparison_title = Text("ECE vs BAS", font_size=28, color=YELLOW)
        comparison_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(comparison_title))
        self.wait(0.3)

        ece_box = Rectangle(width=3, height=2, color=BLUE, fill_opacity=0.2)
        ece_label = Text("ECE", font_size=20, color=BLUE)
        ece_label.move_to(ece_box.get_top() + DOWN * 0.3)
        ece_desc = VGroup(
            Text("Average", font_size=16),
            Text("calibration", font_size=16)
        ).arrange(DOWN, buff=0.1)
        ece_desc.move_to(ece_box.get_center())
        ece_group = VGroup(ece_box, ece_label, ece_desc)
        ece_group.shift(LEFT * 3)

        bas_box = Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.2)
        bas_label = Text("BAS", font_size=20, color=GREEN)
        bas_label.move_to(bas_box.get_top() + DOWN * 0.3)
        bas_desc = VGroup(
            Text("Abstention-", font_size=16),
            Text("aware", font_size=16),
            Text("reliability", font_size=16)
        ).arrange(DOWN, buff=0.1)
        bas_desc.move_to(bas_box.get_center())
        bas_group = VGroup(bas_box, bas_label, bas_desc)
        bas_group.shift(RIGHT * 3)

        self.play(FadeIn(ece_group), FadeIn(bas_group))
        self.wait(1.5)

        # Highlight BAS
        highlight = SurroundingRectangle(bas_group, color=YELLOW, buff=0.2)
        better_text = Text("Better for\nhigh-stakes!", font_size=18, color=YELLOW)
        better_text.next_to(bas_group, DOWN, buff=0.5)

        self.play(Create(highlight), Write(better_text))
        self.wait(1.5)

        self.play(
            FadeOut(comparison_title),
            FadeOut(ece_group),
            FadeOut(bas_group),
            FadeOut(highlight),
            FadeOut(better_text)
        )

        # Conclusion
        conclusion = VGroup(
            Text("BAS:", font_size=28, color=GREEN),
            Text("Know When to Stop", font_size=24)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
