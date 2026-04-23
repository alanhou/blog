from manim import *

class MetaLearningScene(Scene):
    def construct(self):
        # Title
        title = Text("Meta-Learning In-Context", font_size=32)
        subtitle = Text("Training-Free Brain Decoding", font_size=24)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Cross-Subject Barrier", font_size=28, color=RED)
        problem_title.next_to(title_group, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Show per-subject training
        subject1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.3)
        subject1_label = Text("Subject 1", font_size=14)
        subject1_label.move_to(subject1)
        subject1_group = VGroup(subject1, subject1_label)
        subject1_group.shift(LEFT * 4 + UP * 0.5)

        model1 = Rectangle(width=1.5, height=0.8, color=GREEN, fill_opacity=0.3)
        model1_label = Text("Model 1", font_size=12)
        model1_label.move_to(model1)
        model1_group = VGroup(model1, model1_label)
        model1_group.next_to(subject1_group, RIGHT, buff=0.5)

        subject2 = Circle(radius=0.5, color=ORANGE, fill_opacity=0.3)
        subject2_label = Text("Subject 2", font_size=14)
        subject2_label.move_to(subject2)
        subject2_group = VGroup(subject2, subject2_label)
        subject2_group.shift(LEFT * 4 + DOWN * 0.5)

        model2 = Rectangle(width=1.5, height=0.8, color=GREEN, fill_opacity=0.3)
        model2_label = Text("Model 2", font_size=12)
        model2_label.move_to(model2)
        model2_group = VGroup(model2, model2_label)
        model2_group.next_to(subject2_group, RIGHT, buff=0.5)

        arrow1 = Arrow(subject1.get_right(), model1.get_left(), buff=0.1)
        arrow2 = Arrow(subject2.get_right(), model2.get_left(), buff=0.1)

        problem_text = Text("Separate training for each person!", font_size=18, color=RED)
        problem_text.shift(RIGHT * 2.5)

        self.play(
            FadeIn(subject1_group), FadeIn(subject2_group)
        )
        self.play(
            Create(arrow1), Create(arrow2),
            FadeIn(model1_group), FadeIn(model2_group)
        )
        self.play(Write(problem_text))
        self.wait(1.5)

        self.play(
            FadeOut(problem_title),
            FadeOut(subject1_group), FadeOut(subject2_group),
            FadeOut(model1_group), FadeOut(model2_group),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(problem_text)
        )

        # The Insight
        insight_title = Text("The Key Insight", font_size=28, color=BLUE)
        insight_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(insight_title))
        self.wait(0.3)

        insight_text = VGroup(
            Text("Brain decoding is an", font_size=20),
            Text("inverse problem", font_size=24, color=YELLOW, weight=BOLD),
            Text("", font_size=16),
            Text("Learn encoding model first,", font_size=20),
            Text("then invert it for decoding", font_size=20)
        ).arrange(DOWN, buff=0.2)
        insight_text.next_to(insight_title, DOWN, buff=0.5)

        self.play(Write(insight_text, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(insight_title), FadeOut(insight_text))

        # The Solution
        solution_title = Text("In-Context Learning Solution", font_size=28, color=GREEN)
        solution_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Show unified model with in-context examples
        subjects = VGroup(
            Circle(radius=0.4, color=BLUE, fill_opacity=0.3),
            Circle(radius=0.4, color=ORANGE, fill_opacity=0.3),
            Circle(radius=0.4, color=PURPLE, fill_opacity=0.3)
        ).arrange(DOWN, buff=0.3)
        subjects.shift(LEFT * 3.5)

        unified_model = Rectangle(width=2.5, height=2.5, color=GREEN, fill_opacity=0.3)
        unified_label = Text("Unified\nModel", font_size=18)
        unified_label.move_to(unified_model)
        unified_group = VGroup(unified_model, unified_label)
        unified_group.shift(RIGHT * 1)

        arrows = VGroup(
            Arrow(subjects[0].get_right(), unified_model.get_left() + UP * 0.8, buff=0.1),
            Arrow(subjects[1].get_right(), unified_model.get_left(), buff=0.1),
            Arrow(subjects[2].get_right(), unified_model.get_left() + DOWN * 0.8, buff=0.1)
        )

        context_label = Text("Few-shot\nexamples", font_size=14, color=YELLOW)
        context_label.next_to(arrows[1], UP, buff=0.1)

        self.play(FadeIn(subjects))
        self.play(
            *[Create(arrow) for arrow in arrows],
            Write(context_label)
        )
        self.play(FadeIn(unified_group))
        self.wait(1.5)

        self.play(
            FadeOut(solution_title),
            FadeOut(subjects),
            FadeOut(unified_group),
            FadeOut(arrows),
            FadeOut(context_label)
        )

        # Key Benefits
        benefits_title = Text("Key Benefits", font_size=28, color=YELLOW)
        benefits_title.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(benefits_title))
        self.wait(0.3)

        benefits = VGroup(
            Text("✓ Training-free generalization", font_size=20, color=GREEN),
            Text("✓ Cross-subject decoding", font_size=20, color=GREEN),
            Text("✓ Cross-scanner compatibility", font_size=20, color=GREEN),
            Text("✓ Few-shot adaptation", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        benefits.next_to(benefits_title, DOWN, buff=0.5)

        self.play(Write(benefits, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(benefits_title), FadeOut(benefits))

        # Conclusion
        conclusion = VGroup(
            Text("From Per-Subject Training", font_size=24),
            Text("to", font_size=20),
            Text("Training-Free Generalization", font_size=24, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title_group))
