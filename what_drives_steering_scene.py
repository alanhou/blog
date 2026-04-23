from manim import *

class WhatDrivesSteeringScene(Scene):
    def construct(self):
        # Title
        title = Text("What Drives Representation Steering?", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Black Box Problem", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Steering vector as black box
        input_box = Rectangle(width=2, height=1, color=BLUE)
        input_label = Text("Steering\nVector", font_size=16)
        input_label.move_to(input_box)
        input_group = VGroup(input_box, input_label)
        input_group.shift(LEFT * 3)

        black_box = Rectangle(width=2.5, height=1.5, color=GRAY, fill_opacity=0.8)
        question = Text("???", font_size=40, color=WHITE)
        question.move_to(black_box)
        black_box_group = VGroup(black_box, question)

        output_box = Rectangle(width=2, height=1, color=GREEN)
        output_label = Text("Behavior\nChange", font_size=16)
        output_label.move_to(output_box)
        output_group = VGroup(output_box, output_label)
        output_group.shift(RIGHT * 3)

        arrow1 = Arrow(input_box.get_right(), black_box.get_left(), buff=0.1)
        arrow2 = Arrow(black_box.get_right(), output_box.get_left(), buff=0.1)

        self.play(
            FadeIn(input_group),
            FadeIn(black_box_group),
            FadeIn(output_group)
        )
        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        self.play(
            FadeOut(problem_title),
            FadeOut(input_group),
            FadeOut(black_box_group),
            FadeOut(output_group),
            FadeOut(arrow1),
            FadeOut(arrow2)
        )

        # Key Finding: OV Circuit Dominance
        finding_title = Text("Key Finding: OV Circuit Dominance", font_size=26, color=GREEN)
        finding_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(finding_title))
        self.wait(0.3)

        # Attention circuits
        qk_circuit = Rectangle(width=3, height=1.2, color=BLUE, fill_opacity=0.3)
        qk_label = Text("QK Circuit\n(Attention Scores)", font_size=16)
        qk_label.move_to(qk_circuit)
        qk_group = VGroup(qk_circuit, qk_label)
        qk_group.shift(LEFT * 2.5 + DOWN * 0.5)

        ov_circuit = Rectangle(width=3, height=1.2, color=ORANGE, fill_opacity=0.3)
        ov_label = Text("OV Circuit\n(Output-Value)", font_size=16)
        ov_label.move_to(ov_circuit)
        ov_group = VGroup(ov_circuit, ov_label)
        ov_group.shift(RIGHT * 2.5 + DOWN * 0.5)

        # Impact scores
        qk_impact = Text("-8.75%", font_size=20, color=BLUE)
        qk_impact.next_to(qk_circuit, DOWN, buff=0.3)

        ov_impact = Text("-72%", font_size=24, color=RED, weight=BOLD)
        ov_impact.next_to(ov_circuit, DOWN, buff=0.3)

        self.play(
            FadeIn(qk_group),
            FadeIn(ov_group)
        )
        self.play(
            Write(qk_impact),
            Write(ov_impact)
        )
        self.wait(1)

        # Highlight OV dominance
        highlight = SurroundingRectangle(ov_group, color=YELLOW, buff=0.2)
        dominance_text = Text("Dominates!", font_size=20, color=YELLOW)
        dominance_text.next_to(ov_impact, DOWN, buff=0.3)

        self.play(Create(highlight), Write(dominance_text))
        self.wait(1)

        self.play(
            FadeOut(finding_title),
            FadeOut(qk_group), FadeOut(ov_group),
            FadeOut(qk_impact), FadeOut(ov_impact),
            FadeOut(highlight), FadeOut(dominance_text)
        )

        # Circuit Localization
        localization_title = Text("Circuit Localization", font_size=28, color=BLUE)
        localization_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(localization_title))
        self.wait(0.3)

        # Show sparse circuit
        full_model = Rectangle(width=6, height=3, color=GRAY, fill_opacity=0.2)
        full_label = Text("Full Model\n(100% edges)", font_size=18)
        full_label.move_to(full_model)
        full_group = VGroup(full_model, full_label)
        full_group.shift(LEFT * 2.5)

        sparse_circuit = Rectangle(width=2, height=3, color=GREEN, fill_opacity=0.5)
        sparse_label = Text("Circuit\n(~10%)", font_size=18)
        sparse_label.move_to(sparse_circuit)
        sparse_group = VGroup(sparse_circuit, sparse_label)
        sparse_group.shift(RIGHT * 2.5)

        arrow = Arrow(full_model.get_right(), sparse_circuit.get_left(), buff=0.1)
        arrow_label = Text("85% behavior\nrecovered", font_size=16, color=GREEN)
        arrow_label.next_to(arrow, UP)

        self.play(FadeIn(full_group))
        self.play(
            Create(arrow),
            FadeIn(sparse_group),
            Write(arrow_label)
        )
        self.wait(1.5)

        self.play(
            FadeOut(localization_title),
            FadeOut(full_group),
            FadeOut(sparse_group),
            FadeOut(arrow),
            FadeOut(arrow_label)
        )

        # Sparsification
        sparsity_title = Text("Extreme Sparsity", font_size=28, color=PURPLE)
        sparsity_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(sparsity_title))
        self.wait(0.3)

        sparsity_facts = VGroup(
            Text("• 90-99% dimensions can be zeroed", font_size=20),
            Text("• Performance mostly retained", font_size=20),
            Text("• Different methods converge to", font_size=20),
            Text("  shared low-dimensional subspace", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        sparsity_facts.next_to(sparsity_title, DOWN, buff=0.5)

        self.play(Write(sparsity_facts, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(sparsity_title), FadeOut(sparsity_facts))

        # Conclusion
        conclusion = VGroup(
            Text("Steering Vectors:", font_size=26),
            Text("Highly Localized (~10% edges)", font_size=22, color=GREEN),
            Text("OV Circuit Dominant (72% impact)", font_size=22, color=ORANGE),
            Text("Extremely Sparse (90-99% zeros)", font_size=22, color=PURPLE)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
