from manim import *

class ClawBenchScene(Scene):
    def construct(self):
        # Title
        title = Text("ClawBench: Real-World AI Agent Benchmark", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem: Sandbox vs Reality
        problem_title = Text("The Sandbox Illusion", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Sandbox benchmarks
        sandbox = Rectangle(width=3, height=2, color=BLUE)
        sandbox_label = Text("Sandbox\nBenchmarks", font_size=18)
        sandbox_label.move_to(sandbox)
        sandbox_group = VGroup(sandbox, sandbox_label)
        sandbox_group.shift(LEFT * 3)

        sandbox_score = Text("65-75%", font_size=24, color=GREEN)
        sandbox_score.next_to(sandbox, DOWN)

        # Real world
        real = Rectangle(width=3, height=2, color=ORANGE)
        real_label = Text("Real-World\nTasks", font_size=18)
        real_label.move_to(real)
        real_group = VGroup(real, real_label)
        real_group.shift(RIGHT * 3)

        real_score = Text("33%", font_size=24, color=RED)
        real_score.next_to(real, DOWN)

        self.play(
            FadeIn(sandbox_group),
            FadeIn(real_group)
        )
        self.play(
            Write(sandbox_score),
            Write(real_score)
        )
        self.wait(1)

        # Clear for next section
        self.play(
            FadeOut(problem_title),
            FadeOut(sandbox_group),
            FadeOut(real_group),
            FadeOut(sandbox_score),
            FadeOut(real_score)
        )

        # ClawBench Overview
        overview_title = Text("ClawBench: 153 Real Tasks", font_size=28, color=BLUE)
        overview_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(overview_title))
        self.wait(0.3)

        # Task categories
        categories = VGroup(
            Text("• 144 live platforms", font_size=18),
            Text("• 15 life categories", font_size=18),
            Text("• Daily Life, Shopping, Travel", font_size=18),
            Text("• Dev & Tech, Education, Finance", font_size=18),
            Text("• Real authentication & dynamics", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        categories.next_to(overview_title, DOWN, buff=0.5)

        self.play(Write(categories, run_time=2))
        self.wait(1)

        self.play(FadeOut(overview_title), FadeOut(categories))

        # Results comparison
        results_title = Text("Model Performance", font_size=28, color=YELLOW)
        results_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(results_title))
        self.wait(0.3)

        # Bar chart data
        models = ["Claude\nSonnet 4.6", "GLM-5", "Gemini 3\nFlash", "Claude\nHaiku 4.5", "GPT-5.4"]
        scores = [33.3, 24.2, 19.0, 18.3, 6.5]
        colors = [BLUE, GREEN, ORANGE, PURPLE, RED]

        # Create bars
        bars = VGroup()
        labels = VGroup()

        bar_width = 0.6
        max_height = 2.5
        spacing = 1.2

        for i, (model, score, color) in enumerate(zip(models, scores, colors)):
            # Bar
            bar_height = (score / 100) * max_height
            bar = Rectangle(width=bar_width, height=bar_height, fill_opacity=0.7, color=color)
            bar.shift(LEFT * 3 + RIGHT * i * spacing + DOWN * 0.5)
            bar.align_to(DOWN * 1.5, DOWN)

            # Score label
            score_text = Text(f"{score}%", font_size=14)
            score_text.next_to(bar, UP, buff=0.1)

            # Model label
            model_text = Text(model, font_size=12)
            model_text.next_to(bar, DOWN, buff=0.2)

            bars.add(bar)
            labels.add(VGroup(score_text, model_text))

        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=1.5
        )
        self.play(Write(labels))
        self.wait(1)

        # Highlight best model
        best_highlight = SurroundingRectangle(bars[0], color=YELLOW, buff=0.1)
        best_text = Text("Best: Only 33%!", font_size=20, color=YELLOW)
        best_text.next_to(bars[0], RIGHT, buff=0.5)

        self.play(Create(best_highlight), Write(best_text))
        self.wait(1)

        self.play(
            FadeOut(results_title),
            FadeOut(bars),
            FadeOut(labels),
            FadeOut(best_highlight),
            FadeOut(best_text)
        )

        # Key challenges
        challenges_title = Text("Why Real Tasks Are Hard", font_size=28, color=RED)
        challenges_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(challenges_title))
        self.wait(0.3)

        challenges = VGroup(
            Text("1. Document-grounded extraction", font_size=18),
            Text("2. Multi-step workflows (144 platforms)", font_size=18),
            Text("3. Write-heavy operations (20+ fields)", font_size=18),
            Text("4. Dynamic content & JavaScript", font_size=18),
            Text("5. Auth, CAPTCHA, rate limits", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        challenges.next_to(challenges_title, DOWN, buff=0.5)

        self.play(Write(challenges, run_time=2.5))
        self.wait(1.5)

        # Final message
        self.play(
            FadeOut(challenges_title),
            FadeOut(challenges)
        )

        conclusion = Text(
            "The Reality Gap:\nSandbox ≠ Production",
            font_size=32,
            color=YELLOW
        )
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
