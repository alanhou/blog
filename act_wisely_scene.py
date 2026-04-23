from manim import *

class ActWiselyScene(Scene):
    def construct(self):
        # Title
        title = Text("Act Wisely: Meta-Cognitive Tool Use", font_size=36, weight=BOLD)
        subtitle = Text("Hierarchical Decoupled Policy Optimization", font_size=24)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Part 1: The Problem - Blind Tool Invocation
        problem_title = Text("The Problem: Blind Tool Invocation", font_size=32, color=RED)
        problem_title.to_edge(UP)
        self.play(Write(problem_title))

        # Show agent with tools
        agent = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        agent_label = Text("Agent", font_size=20).next_to(agent, DOWN, buff=0.2)
        agent_group = VGroup(agent, agent_label).shift(LEFT * 4)

        # Tools
        tools = VGroup()
        tool_names = ["Crop", "Search", "Code", "Web"]
        for i, name in enumerate(tool_names):
            tool = Rectangle(width=1, height=0.6, color=YELLOW, fill_opacity=0.3)
            tool_text = Text(name, font_size=16)
            tool_text.move_to(tool.get_center())
            tool_group = VGroup(tool, tool_text)
            tool_group.shift(RIGHT * (i * 1.5 - 1.5) + UP * 0.5)
            tools.add(tool_group)

        self.play(FadeIn(agent_group))
        self.play(LaggedStart(*[FadeIn(tool) for tool in tools], lag_ratio=0.2))

        # Show excessive tool calls
        arrows = VGroup()
        for tool in tools:
            arrow = Arrow(agent.get_center(), tool.get_center(), color=RED, stroke_width=3)
            arrows.add(arrow)

        self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.1))

        problem_text = Text("98% tool usage rate!", font_size=24, color=RED)
        problem_text.next_to(tools, DOWN, buff=1)
        self.play(Write(problem_text))
        self.wait(2)

        self.play(FadeOut(agent_group), FadeOut(tools), FadeOut(arrows),
                  FadeOut(problem_text), FadeOut(problem_title))

        # Part 2: Reward Coupling Problem
        coupling_title = Text("Reward Coupling Problem", font_size=32, color=ORANGE)
        coupling_title.to_edge(UP)
        self.play(Write(coupling_title))

        # Show coupled reward formula
        coupled_formula = MathTex(
            r"R = ", r"\text{Accuracy}", r" + ", r"\alpha \times ", r"\text{Efficiency}",
            font_size=36
        )
        coupled_formula.shift(UP * 1.5)
        self.play(Write(coupled_formula))

        # Show the problem
        problem_box = Rectangle(width=8, height=2, color=RED, stroke_width=3)
        problem_box.shift(DOWN * 1)

        problem_lines = VGroup(
            Text("Variance entanglement", font_size=24),
            Text("Gradient interference", font_size=24),
            Text("Optimization dilemma", font_size=24)
        ).arrange(DOWN, buff=0.3)
        problem_lines.move_to(problem_box.get_center())

        self.play(Create(problem_box))
        self.play(LaggedStart(*[FadeIn(line) for line in problem_lines], lag_ratio=0.3))
        self.wait(2)

        self.play(FadeOut(coupled_formula), FadeOut(problem_box),
                  FadeOut(problem_lines), FadeOut(coupling_title))

        # Part 3: HDPO Solution
        solution_title = Text("HDPO: Hierarchical Decoupled Optimization", font_size=32, color=GREEN)
        solution_title.to_edge(UP)
        self.play(Write(solution_title))

        # Show two separate channels
        channel1_box = Rectangle(width=5, height=2.5, color=BLUE, stroke_width=3)
        channel1_box.shift(LEFT * 3 + UP * 0.5)
        channel1_title = Text("Accuracy Channel", font_size=24, color=BLUE)
        channel1_title.next_to(channel1_box, UP, buff=0.2)
        channel1_content = VGroup(
            Text("All rollouts", font_size=18),
            Text("↓", font_size=24),
            Text("Global advantage", font_size=18),
            Text("↓", font_size=24),
            Text("Accuracy loss", font_size=18)
        ).arrange(DOWN, buff=0.1)
        channel1_content.move_to(channel1_box.get_center())

        channel2_box = Rectangle(width=5, height=2.5, color=YELLOW, stroke_width=3)
        channel2_box.shift(RIGHT * 3 + UP * 0.5)
        channel2_title = Text("Efficiency Channel", font_size=24, color=YELLOW)
        channel2_title.next_to(channel2_box, UP, buff=0.2)
        channel2_content = VGroup(
            Text("Correct rollouts only", font_size=18),
            Text("↓", font_size=24),
            Text("Conditional advantage", font_size=18),
            Text("↓", font_size=24),
            Text("Efficiency loss", font_size=18)
        ).arrange(DOWN, buff=0.1)
        channel2_content.move_to(channel2_box.get_center())

        self.play(Create(channel1_box), Write(channel1_title))
        self.play(LaggedStart(*[FadeIn(line) for line in channel1_content], lag_ratio=0.2))
        self.wait(1)

        self.play(Create(channel2_box), Write(channel2_title))
        self.play(LaggedStart(*[FadeIn(line) for line in channel2_content], lag_ratio=0.2))
        self.wait(2)

        # Show combination
        combine_arrow1 = Arrow(channel1_box.get_bottom(), DOWN * 2, color=BLUE)
        combine_arrow2 = Arrow(channel2_box.get_bottom(), DOWN * 2, color=YELLOW)
        combine_point = Dot(point=DOWN * 2, color=GREEN, radius=0.15)

        self.play(Create(combine_arrow1), Create(combine_arrow2))
        self.play(FadeIn(combine_point, scale=2))

        final_formula = MathTex(
            r"L = w_{acc} \times L_{acc} + w_{tool} \times L_{tool}",
            font_size=32, color=GREEN
        )
        final_formula.next_to(combine_point, DOWN, buff=0.5)
        self.play(Write(final_formula))
        self.wait(2)

        self.play(FadeOut(channel1_box), FadeOut(channel1_title), FadeOut(channel1_content),
                  FadeOut(channel2_box), FadeOut(channel2_title), FadeOut(channel2_content),
                  FadeOut(combine_arrow1), FadeOut(combine_arrow2), FadeOut(combine_point),
                  FadeOut(final_formula), FadeOut(solution_title))

        # Part 4: Results
        results_title = Text("Results: Metis Model", font_size=32, color=GREEN)
        results_title.to_edge(UP)
        self.play(Write(results_title))

        # Before and After comparison
        before_label = Text("Before", font_size=28, color=RED).shift(LEFT * 3 + UP * 1.5)
        after_label = Text("After", font_size=28, color=GREEN).shift(RIGHT * 3 + UP * 1.5)

        self.play(Write(before_label), Write(after_label))

        # Tool usage bars
        before_bar = Rectangle(width=0.8, height=4.9, color=RED, fill_opacity=0.7)
        before_bar.shift(LEFT * 3 + DOWN * 0.5)
        before_text = Text("98%", font_size=24).next_to(before_bar, DOWN)
        before_label2 = Text("Tool Usage", font_size=18).next_to(before_text, DOWN)

        after_bar = Rectangle(width=0.8, height=0.1, color=GREEN, fill_opacity=0.7)
        after_bar.shift(RIGHT * 3 + DOWN * 2.9)
        after_text = Text("2%", font_size=24).next_to(after_bar, DOWN)
        after_label2 = Text("Tool Usage", font_size=18).next_to(after_text, DOWN)

        self.play(GrowFromEdge(before_bar, DOWN), Write(before_text), Write(before_label2))
        self.play(GrowFromEdge(after_bar, DOWN), Write(after_text), Write(after_label2))

        # Accuracy improvement
        accuracy_text = Text("Accuracy: 88.7% → 91.1%", font_size=28, color=GREEN)
        accuracy_text.shift(DOWN * 1)
        self.play(Write(accuracy_text))
        self.wait(3)

        # Final message
        self.play(
            FadeOut(results_title), FadeOut(before_label), FadeOut(after_label),
            FadeOut(before_bar), FadeOut(before_text), FadeOut(before_label2),
            FadeOut(after_bar), FadeOut(after_text), FadeOut(after_label2),
            FadeOut(accuracy_text)
        )

        final_message = Text("Meta-cognitive wisdom:\nKnow when NOT to use tools",
                           font_size=36, color=BLUE)
        self.play(Write(final_message))
        self.wait(3)
