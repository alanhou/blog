from manim import *

class SupernovaScene(Scene):
    def construct(self):
        # Title
        title = Text("SUPERNOVA: General Reasoning via RLVR", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The RLVR Ceiling", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # STEM vs General Reasoning
        stem_box = Rectangle(width=3, height=1.5, color=GREEN, fill_opacity=0.3)
        stem_label = Text("STEM\nReasoning", font_size=18)
        stem_label.move_to(stem_box)
        stem_group = VGroup(stem_box, stem_label)
        stem_group.shift(LEFT * 3)

        stem_score = Text("+50%", font_size=24, color=GREEN, weight=BOLD)
        stem_score.next_to(stem_box, DOWN, buff=0.3)

        general_box = Rectangle(width=3, height=1.5, color=RED, fill_opacity=0.3)
        general_label = Text("General\nReasoning", font_size=18)
        general_label.move_to(general_box)
        general_group = VGroup(general_box, general_label)
        general_group.shift(RIGHT * 3)

        general_score = Text("-8%", font_size=24, color=RED, weight=BOLD)
        general_score.next_to(general_box, DOWN, buff=0.3)

        self.play(
            FadeIn(stem_group),
            FadeIn(general_group)
        )
        self.play(
            Write(stem_score),
            Write(general_score)
        )
        self.wait(1)

        problem_text = Text("RLVR works for STEM, fails for general reasoning", font_size=18, color=RED)
        problem_text.next_to(general_score, DOWN, buff=0.5)
        self.play(Write(problem_text))
        self.wait(1)

        self.play(
            FadeOut(problem_title),
            FadeOut(stem_group), FadeOut(general_group),
            FadeOut(stem_score), FadeOut(general_score),
            FadeOut(problem_text)
        )

        # The Insight
        insight_title = Text("The Insight", font_size=28, color=BLUE)
        insight_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(insight_title))
        self.wait(0.3)

        insight_text = VGroup(
            Text("Instruction datasets already contain", font_size=20),
            Text("rich reasoning patterns!", font_size=20, color=GREEN),
            Text("", font_size=16),
            Text("Challenge: Data Curation", font_size=22, color=YELLOW),
            Text("Not Data Generation", font_size=22, color=YELLOW)
        ).arrange(DOWN, buff=0.25)
        insight_text.next_to(insight_title, DOWN, buff=0.5)

        self.play(Write(insight_text, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(insight_title), FadeOut(insight_text))

        # Three-Stage Pipeline
        pipeline_title = Text("SUPERNOVA Pipeline", font_size=28, color=GREEN)
        pipeline_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(pipeline_title))
        self.wait(0.3)

        # Three stages
        stage1 = Rectangle(width=6, height=0.8, color=PURPLE, fill_opacity=0.3)
        stage1_label = Text("1. Task Selection (utility ranking)", font_size=16)
        stage1_label.move_to(stage1)
        stage1_group = VGroup(stage1, stage1_label)
        stage1_group.shift(UP * 1.2)

        stage2 = Rectangle(width=6, height=0.8, color=BLUE, fill_opacity=0.3)
        stage2_label = Text("2. Task Mixing (micro > macro)", font_size=16)
        stage2_label.move_to(stage2)
        stage2_group = VGroup(stage2, stage2_label)

        stage3 = Rectangle(width=6, height=0.8, color=ORANGE, fill_opacity=0.3)
        stage3_label = Text("3. Data Interventions (quality > augmentation)", font_size=16)
        stage3_label.move_to(stage3)
        stage3_group = VGroup(stage3, stage3_label)
        stage3_group.shift(DOWN * 1.2)

        arrow1 = Arrow(stage1.get_bottom(), stage2.get_top(), buff=0.1)
        arrow2 = Arrow(stage2.get_bottom(), stage3.get_top(), buff=0.1)

        self.play(FadeIn(stage1_group))
        self.play(Create(arrow1), FadeIn(stage2_group))
        self.play(Create(arrow2), FadeIn(stage3_group))
        self.wait(1.5)

        self.play(
            FadeOut(pipeline_title),
            FadeOut(stage1_group), FadeOut(stage2_group), FadeOut(stage3_group),
            FadeOut(arrow1), FadeOut(arrow2)
        )

        # Results
        results_title = Text("Results on BBEH", font_size=28, color=YELLOW)
        results_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(results_title))
        self.wait(0.3)

        # Bar chart
        baseline_bar = Rectangle(width=0.8, height=1.5, color=BLUE, fill_opacity=0.7)
        baseline_bar.shift(LEFT * 2 + DOWN * 0.5)
        baseline_bar.align_to(DOWN * 2, DOWN)
        baseline_label = Text("Baseline\n15.4%", font_size=16)
        baseline_label.next_to(baseline_bar, DOWN, buff=0.2)

        supernova_bar = Rectangle(width=0.8, height=2.5, color=GREEN, fill_opacity=0.7)
        supernova_bar.shift(RIGHT * 2 + DOWN * 0.5)
        supernova_bar.align_to(DOWN * 2, DOWN)
        supernova_label = Text("SUPERNOVA\n19.9%", font_size=16)
        supernova_label.next_to(supernova_bar, DOWN, buff=0.2)

        improvement = Text("+29.4%", font_size=24, color=GREEN, weight=BOLD)
        improvement.next_to(supernova_bar, UP, buff=0.2)

        self.play(
            GrowFromEdge(baseline_bar, DOWN),
            Write(baseline_label)
        )
        self.play(
            GrowFromEdge(supernova_bar, DOWN),
            Write(supernova_label)
        )
        self.play(Write(improvement))
        self.wait(1.5)

        self.play(
            FadeOut(results_title),
            FadeOut(baseline_bar), FadeOut(baseline_label),
            FadeOut(supernova_bar), FadeOut(supernova_label),
            FadeOut(improvement)
        )

        # Key Insights
        insights_title = Text("Key Insights", font_size=28, color=PURPLE)
        insights_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(insights_title))
        self.wait(0.3)

        insights = VGroup(
            Text("✓ Task selection is critical", font_size=20, color=GREEN),
            Text("✓ Micro mixing > macro mixing", font_size=20, color=GREEN),
            Text("✓ Quality > augmentation", font_size=20, color=GREEN),
            Text("✓ RLVR extends beyond STEM", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        insights.next_to(insights_title, DOWN, buff=0.5)

        self.play(Write(insights, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(insights_title), FadeOut(insights))

        # Conclusion
        conclusion = VGroup(
            Text("SUPERNOVA:", font_size=28, color=YELLOW),
            Text("Curate, Don't Generate", font_size=24, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
