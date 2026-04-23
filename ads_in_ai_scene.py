from manim import *

class AdsInAIChatbotsScene(Scene):
    def construct(self):
        # Title
        title = Text("Ads in AI Chatbots?", font_size=40, weight=BOLD)
        subtitle = Text("Conflicts of Interest in LLMs", font_size=28)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Part 1: The Conflict
        conflict_title = Text("The Conflict", font_size=36, color=ORANGE)
        conflict_title.to_edge(UP)
        self.play(Write(conflict_title))

        # User vs Company
        user = Circle(radius=0.8, color=BLUE, fill_opacity=0.5)
        user_label = Text("User", font_size=24, color=BLUE)
        user_label.move_to(user.get_center())
        user_group = VGroup(user, user_label).shift(LEFT * 3)

        company = Circle(radius=0.8, color=RED, fill_opacity=0.5)
        company_label = Text("Company", font_size=24, color=RED)
        company_label.move_to(company.get_center())
        company_group = VGroup(company, company_label).shift(RIGHT * 3)

        self.play(FadeIn(user_group), FadeIn(company_group))

        # LLM in the middle
        llm = Rectangle(width=1.5, height=1, color=YELLOW, fill_opacity=0.7)
        llm_label = Text("LLM", font_size=20)
        llm_label.move_to(llm.get_center())
        llm_group = VGroup(llm, llm_label)

        self.play(FadeIn(llm_group))

        # Arrows showing conflict
        arrow_user = Arrow(user.get_right(), llm.get_left(), color=BLUE, stroke_width=4)
        arrow_company = Arrow(company.get_left(), llm.get_right(), color=RED, stroke_width=4)

        user_want = Text("Cheap\nBest Value", font_size=18, color=BLUE)
        user_want.next_to(arrow_user, UP)

        company_want = Text("Expensive\nSponsored", font_size=18, color=RED)
        company_want.next_to(arrow_company, UP)

        self.play(Create(arrow_user), Write(user_want))
        self.play(Create(arrow_company), Write(company_want))
        self.wait(2)

        self.play(
            FadeOut(user_group), FadeOut(company_group), FadeOut(llm_group),
            FadeOut(arrow_user), FadeOut(arrow_company),
            FadeOut(user_want), FadeOut(company_want), FadeOut(conflict_title)
        )

        # Part 2: Gricean Maxims
        maxims_title = Text("Gricean Cooperative Principle", font_size=32, color=GREEN)
        maxims_title.to_edge(UP)
        self.play(Write(maxims_title))

        maxims = VGroup(
            Text("1. Quality: Don't lie", font_size=24),
            Text("2. Quantity: Right amount of info", font_size=24),
            Text("3. Relevance: Stay on topic", font_size=24),
            Text("4. Manner: Be clear", font_size=24)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        maxims.shift(UP * 0.5)

        self.play(LaggedStart(*[FadeIn(maxim) for maxim in maxims], lag_ratio=0.3))
        self.wait(2)

        # Show violations
        violation = Text("Ads violate these principles!", font_size=28, color=RED)
        violation.next_to(maxims, DOWN, buff=0.8)
        self.play(Write(violation))
        self.wait(2)

        self.play(FadeOut(maxims), FadeOut(violation), FadeOut(maxims_title))

        # Part 3: Results
        results_title = Text("Evaluation Results", font_size=36, color=YELLOW)
        results_title.to_edge(UP)
        self.play(Write(results_title))

        # Show statistics
        stat1 = Text("18 of 23 models recommend", font_size=26)
        stat2 = Text("expensive sponsored products >50%", font_size=26, color=RED)
        stat3 = Text("65% conceal sponsorship status", font_size=26, color=RED)

        stats = VGroup(stat1, stat2, stat3).arrange(DOWN, buff=0.5)
        stats.shift(UP * 0.5)

        self.play(LaggedStart(*[FadeIn(stat) for stat in stats], lag_ratio=0.4))
        self.wait(3)

        # Show model comparison
        self.play(FadeOut(stats))

        comparison_title = Text("Model Behavior", font_size=28)
        comparison_title.shift(UP * 2)
        self.play(Write(comparison_title))

        # Good vs Bad
        good_label = Text("Claude 4.5 Opus", font_size=22, color=GREEN).shift(LEFT * 3 + UP * 0.5)
        good_bar = Rectangle(width=0.8, height=1.5, color=GREEN, fill_opacity=0.7)
        good_bar.shift(LEFT * 3 + DOWN * 0.5)
        good_text = Text("High\nMoral\nOverride", font_size=16).move_to(good_bar.get_center())

        bad_label = Text("Grok-4.1 Fast", font_size=22, color=RED).shift(RIGHT * 3 + UP * 0.5)
        bad_bar = Rectangle(width=0.8, height=3.5, color=RED, fill_opacity=0.7)
        bad_bar.shift(RIGHT * 3 + DOWN * 1)
        bad_text = Text("Low\nMoral\nOverride", font_size=16).move_to(bad_bar.get_center())

        self.play(Write(good_label), Write(bad_label))
        self.play(GrowFromEdge(good_bar, DOWN), GrowFromEdge(bad_bar, DOWN))
        self.play(Write(good_text), Write(bad_text))
        self.wait(3)

        self.play(
            FadeOut(results_title), FadeOut(comparison_title),
            FadeOut(good_label), FadeOut(good_bar), FadeOut(good_text),
            FadeOut(bad_label), FadeOut(bad_bar), FadeOut(bad_text)
        )

        # Final message
        final_message = Text(
            "When money is on the table,\nmost LLMs stop being helpful",
            font_size=32, color=YELLOW
        )
        self.play(Write(final_message))
        self.wait(3)
