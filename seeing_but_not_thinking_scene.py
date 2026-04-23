from manim import *

class SeeingButNotThinkingScene(Scene):
    def construct(self):
        # Title
        title = Text("Seeing but Not Thinking", font_size=36)
        subtitle = Text("Routing Distraction in Multimodal MoE", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Problem", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Visual vs Text comparison
        visual_box = Rectangle(width=2.5, height=1.5, color=BLUE)
        visual_label = Text("Image Input", font_size=16)
        visual_label.move_to(visual_box)
        visual_group = VGroup(visual_box, visual_label)
        visual_group.shift(LEFT * 3.5 + DOWN * 0.5)

        text_box = Rectangle(width=2.5, height=1.5, color=GREEN)
        text_label = Text("Text Input", font_size=16)
        text_label.move_to(text_box)
        text_group = VGroup(text_box, text_label)
        text_group.shift(RIGHT * 3.5 + DOWN * 0.5)

        # Results
        visual_result = Text("✗ Wrong\nReasoning", font_size=18, color=RED)
        visual_result.next_to(visual_box, DOWN, buff=0.3)

        text_result = Text("✓ Correct\nReasoning", font_size=18, color=GREEN)
        text_result.next_to(text_box, DOWN, buff=0.3)

        self.play(
            FadeIn(visual_group),
            FadeIn(text_group)
        )
        self.play(
            Write(visual_result),
            Write(text_result)
        )
        self.wait(1)

        # Clear
        self.play(
            FadeOut(problem_title),
            FadeOut(visual_group),
            FadeOut(text_group),
            FadeOut(visual_result),
            FadeOut(text_result)
        )

        # MoE Architecture
        arch_title = Text("MoE Layer Structure", font_size=28, color=BLUE)
        arch_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(arch_title))
        self.wait(0.3)

        # Three layer types
        early_layer = Rectangle(width=6, height=0.8, color=PURPLE, fill_opacity=0.3)
        early_label = Text("Early Layers: Visual Experts", font_size=16)
        early_label.move_to(early_layer)
        early_group = VGroup(early_layer, early_label)
        early_group.shift(UP * 1)

        middle_layer = Rectangle(width=6, height=0.8, color=YELLOW, fill_opacity=0.3)
        middle_label = Text("Middle Layers: Reasoning Experts", font_size=16)
        middle_label.move_to(middle_layer)
        middle_group = VGroup(middle_layer, middle_label)

        terminal_layer = Rectangle(width=6, height=0.8, color=PURPLE, fill_opacity=0.3)
        terminal_label = Text("Terminal Layers: Visual Experts", font_size=16)
        terminal_label.move_to(terminal_layer)
        terminal_group = VGroup(terminal_layer, terminal_label)
        terminal_group.shift(DOWN * 1)

        self.play(
            FadeIn(early_group),
            FadeIn(middle_group),
            FadeIn(terminal_group)
        )
        self.wait(1)

        # Highlight middle layer problem
        problem_arrow = Arrow(start=RIGHT * 3.5, end=middle_layer.get_right(), color=RED)
        problem_text = Text("Routing\nDistraction!", font_size=18, color=RED)
        problem_text.next_to(problem_arrow, RIGHT)

        self.play(
            Create(problem_arrow),
            Write(problem_text)
        )
        self.wait(1)

        self.play(
            FadeOut(arch_title),
            FadeOut(early_group),
            FadeOut(middle_group),
            FadeOut(terminal_group),
            FadeOut(problem_arrow),
            FadeOut(problem_text)
        )

        # Routing Distraction Mechanism
        mech_title = Text("Routing Distraction", font_size=28, color=ORANGE)
        mech_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(mech_title))
        self.wait(0.3)

        # Show routing divergence
        explanation = VGroup(
            Text("Visual inputs cause:", font_size=20),
            Text("• Routing divergence in middle layers", font_size=18),
            Text("• Under-activation of reasoning experts", font_size=18),
            Text("• Correct perception, wrong reasoning", font_size=18),
            Text("", font_size=16),
            Text("68-73% of failures are reasoning errors", font_size=18, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        explanation.next_to(mech_title, DOWN, buff=0.5)

        self.play(Write(explanation, run_time=2.5))
        self.wait(1.5)

        self.play(FadeOut(mech_title), FadeOut(explanation))

        # Solution
        solution_title = Text("Solution: Routing-Guided Intervention", font_size=28, color=GREEN)
        solution_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Intervention steps
        steps = VGroup(
            Text("1. Identify domain experts by activation", font_size=18),
            Text("2. Measure routing divergence (JSD)", font_size=18),
            Text("3. Guide routing to activate reasoning experts", font_size=18),
            Text("", font_size=16),
            Text("Result: +3.17% accuracy improvement", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(solution_title, DOWN, buff=0.5)

        self.play(Write(steps, run_time=2))
        self.wait(1.5)

        # Clear for conclusion
        self.play(
            FadeOut(solution_title),
            FadeOut(steps)
        )

        # Conclusion
        conclusion = VGroup(
            Text("Key Insight:", font_size=28, color=YELLOW),
            Text("Visual inputs distract routing", font_size=22),
            Text("from task-relevant experts", font_size=22),
            Text("in middle layers", font_size=22)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
