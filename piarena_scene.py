from manim import *

class PIArenaScene(Scene):
    def construct(self):
        # Title
        title = Text("PIArena", font_size=40)
        subtitle = Text("Prompt Injection Evaluation Platform", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Fragmentation Problem", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        problems = VGroup(
            Text("• Fragmented evaluation", font_size=20, color=RED),
            Text("• Static attacks only", font_size=20, color=RED),
            Text("• No unified platform", font_size=20, color=RED),
            Text("• Limited extensibility", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problems.next_to(problem_title, DOWN, buff=0.5)

        self.play(Write(problems, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(problem_title), FadeOut(problems))

        # PIArena Architecture
        arch_title = Text("PIArena: 4 Modules", font_size=28, color=GREEN)
        arch_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(arch_title))
        self.wait(0.3)

        # Four modules
        module1 = Rectangle(width=2.5, height=0.8, color=BLUE, fill_opacity=0.3)
        module1_label = Text("Benchmark", font_size=14)
        module1_label.move_to(module1)
        module1_group = VGroup(module1, module1_label)
        module1_group.shift(UP * 1.5 + LEFT * 3)

        module2 = Rectangle(width=2.5, height=0.8, color=RED, fill_opacity=0.3)
        module2_label = Text("Attack", font_size=14)
        module2_label.move_to(module2)
        module2_group = VGroup(module2, module2_label)
        module2_group.shift(UP * 1.5 + RIGHT * 3)

        module3 = Rectangle(width=2.5, height=0.8, color=GREEN, fill_opacity=0.3)
        module3_label = Text("Defense", font_size=14)
        module3_label.move_to(module3)
        module3_group = VGroup(module3, module3_label)
        module3_group.shift(DOWN * 0.5 + LEFT * 3)

        module4 = Rectangle(width=2.5, height=0.8, color=YELLOW, fill_opacity=0.3)
        module4_label = Text("Evaluator", font_size=14)
        module4_label.move_to(module4)
        module4_group = VGroup(module4, module4_label)
        module4_group.shift(DOWN * 0.5 + RIGHT * 3)

        # Arrows showing flow
        arrow1 = Arrow(module1.get_right(), module2.get_left(), buff=0.1)
        arrow2 = Arrow(module2.get_bottom(), module3.get_top(), buff=0.1)
        arrow3 = Arrow(module3.get_right(), module4.get_left(), buff=0.1)

        self.play(
            FadeIn(module1_group),
            FadeIn(module2_group),
            FadeIn(module3_group),
            FadeIn(module4_group)
        )
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3)
        )
        self.wait(1.5)

        self.play(
            FadeOut(arch_title),
            FadeOut(module1_group), FadeOut(module2_group),
            FadeOut(module3_group), FadeOut(module4_group),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3)
        )

        # Key Innovation: Adaptive Attacks
        innovation_title = Text("Strategy-Based Adaptive Attack", font_size=26, color=PURPLE)
        innovation_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(innovation_title))
        self.wait(0.3)

        innovation = VGroup(
            Text("Phase 1: Generate diverse candidates", font_size=18),
            Text("  (10 rewriting strategies)", font_size=16, color=GRAY),
            Text("", font_size=14),
            Text("Phase 2: Feedback-guided optimization", font_size=18),
            Text("  • Detected → optimize for stealth", font_size=16, color=BLUE),
            Text("  • Ignored → optimize for imperativeness", font_size=16, color=ORANGE),
            Text("  • Unclear → general refinement", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        innovation.next_to(innovation_title, DOWN, buff=0.5)

        self.play(Write(innovation, run_time=2.5))
        self.wait(2)

        self.play(FadeOut(innovation_title), FadeOut(innovation))

        # Key Findings
        findings_title = Text("Key Findings", font_size=28, color=YELLOW)
        findings_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(findings_title))
        self.wait(0.3)

        findings = VGroup(
            Text("✓ Unified plug-and-play platform", font_size=20, color=GREEN),
            Text("✓ Adaptive attacks reveal weaknesses", font_size=20, color=GREEN),
            Text("✓ State-of-art defenses have limits", font_size=20, color=ORANGE),
            Text("", font_size=16),
            Text("Defending prompt injection", font_size=22, color=RED),
            Text("remains fundamentally challenging", font_size=22, color=RED)
        ).arrange(DOWN, buff=0.25)
        findings.next_to(findings_title, DOWN, buff=0.5)

        self.play(Write(findings, run_time=2.5))
        self.wait(2)

        self.play(FadeOut(findings_title), FadeOut(findings))

        # Conclusion
        conclusion = VGroup(
            Text("PIArena:", font_size=28, color=GREEN),
            Text("Systematic Prompt Injection", font_size=24),
            Text("Evaluation at Scale", font_size=24)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
