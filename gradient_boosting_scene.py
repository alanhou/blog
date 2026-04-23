from manim import *

class GradientBoostingScene(Scene):
    def construct(self):
        # Title
        title = Text("Gradient Boosting in Attention", font_size=32)
        subtitle = Text("Second-Guessing Success", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("One-Pass Attention Problem", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Show one-pass flow
        input_box = Rectangle(width=1.5, height=0.8, color=BLUE, fill_opacity=0.3)
        input_label = Text("Input", font_size=14)
        input_label.move_to(input_box)
        input_group = VGroup(input_box, input_label)
        input_group.shift(LEFT * 4)

        attn_box = Rectangle(width=2, height=0.8, color=GREEN, fill_opacity=0.3)
        attn_label = Text("Attention", font_size=14)
        attn_label.move_to(attn_box)
        attn_group = VGroup(attn_box, attn_label)

        output_box = Rectangle(width=1.5, height=0.8, color=ORANGE, fill_opacity=0.3)
        output_label = Text("Output", font_size=14)
        output_label.move_to(output_box)
        output_group = VGroup(output_box, output_label)
        output_group.shift(RIGHT * 4)

        arrow1 = Arrow(input_box.get_right(), attn_box.get_left(), buff=0.1)
        arrow2 = Arrow(attn_box.get_right(), output_box.get_left(), buff=0.1)

        error_text = Text("Error? No fix!", font_size=18, color=RED)
        error_text.next_to(attn_box, DOWN, buff=0.5)

        self.play(
            FadeIn(input_group),
            FadeIn(attn_group),
            FadeIn(output_group)
        )
        self.play(Create(arrow1), Create(arrow2))
        self.play(Write(error_text))
        self.wait(1.5)

        self.play(
            FadeOut(problem_title),
            FadeOut(input_group), FadeOut(attn_group), FadeOut(output_group),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(error_text)
        )

        # The Solution: Two-Pass
        solution_title = Text("Gradient-Boosted Attention (GBA)", font_size=26, color=GREEN)
        solution_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Two-pass architecture
        pass1 = Rectangle(width=2.5, height=1, color=BLUE, fill_opacity=0.3)
        pass1_label = Text("Pass 1\n(Initial)", font_size=14)
        pass1_label.move_to(pass1)
        pass1_group = VGroup(pass1, pass1_label)
        pass1_group.shift(LEFT * 2.5 + UP * 0.8)

        residual = Rectangle(width=2, height=0.8, color=YELLOW, fill_opacity=0.3)
        residual_label = Text("Residual\nError", font_size=14)
        residual_label.move_to(residual)
        residual_group = VGroup(residual, residual_label)
        residual_group.shift(LEFT * 2.5 + DOWN * 1)

        pass2 = Rectangle(width=2.5, height=1, color=PURPLE, fill_opacity=0.3)
        pass2_label = Text("Pass 2\n(Correction)", font_size=14)
        pass2_label.move_to(pass2)
        pass2_group = VGroup(pass2, pass2_label)
        pass2_group.shift(RIGHT * 2.5 + DOWN * 1)

        final = Rectangle(width=2, height=0.8, color=GREEN, fill_opacity=0.3)
        final_label = Text("Final\nOutput", font_size=14)
        final_label.move_to(final)
        final_group = VGroup(final, final_label)
        final_group.shift(RIGHT * 2.5 + UP * 0.8)

        # Arrows
        arrow_res = Arrow(pass1.get_bottom(), residual.get_top(), buff=0.1)
        arrow_pass2 = Arrow(residual.get_right(), pass2.get_left(), buff=0.1)
        arrow_combine = Arrow(pass2.get_top(), final.get_bottom(), buff=0.1)
        arrow_direct = Arrow(pass1.get_right(), final.get_left(), buff=0.1)

        self.play(FadeIn(pass1_group))
        self.play(Create(arrow_res), FadeIn(residual_group))
        self.play(Create(arrow_pass2), FadeIn(pass2_group))
        self.play(
            Create(arrow_combine),
            Create(arrow_direct),
            FadeIn(final_group)
        )
        self.wait(1.5)

        self.play(
            FadeOut(solution_title),
            FadeOut(pass1_group), FadeOut(residual_group),
            FadeOut(pass2_group), FadeOut(final_group),
            FadeOut(arrow_res), FadeOut(arrow_pass2),
            FadeOut(arrow_combine), FadeOut(arrow_direct)
        )

        # Analogy
        analogy_title = Text("Master Chef Analogy", font_size=28, color=BLUE)
        analogy_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(analogy_title))
        self.wait(0.3)

        analogy = VGroup(
            Text("Apprentice (Pass 1):", font_size=20, color=BLUE),
            Text("  Makes base soup", font_size=18),
            Text("", font_size=14),
            Text("Master Chef (Pass 2):", font_size=20, color=PURPLE),
            Text("  Tastes & corrects", font_size=18),
            Text("", font_size=14),
            Text("Gate: Adds just enough!", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        analogy.next_to(analogy_title, DOWN, buff=0.5)

        self.play(Write(analogy, run_time=2.5))
        self.wait(1.5)

        self.play(FadeOut(analogy_title), FadeOut(analogy))

        # Results
        results_title = Text("Results", font_size=28, color=YELLOW)
        results_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(results_title))
        self.wait(0.3)

        results = VGroup(
            Text("WikiText-103 Benchmark", font_size=22),
            Text("", font_size=16),
            Text("-4.3 PPL Reduction", font_size=26, color=GREEN, weight=BOLD),
            Text("", font_size=16),
            Text("vs Standard Attention", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        results.next_to(results_title, DOWN, buff=0.5)

        self.play(Write(results, run_time=2))
        self.wait(2)

        self.play(FadeOut(results_title), FadeOut(results))

        # Conclusion
        conclusion = VGroup(
            Text("From One-Pass", font_size=24),
            Text("to", font_size=20),
            Text("Self-Correcting Attention", font_size=24, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
