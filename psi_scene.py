from manim import *

class PSIScene(Scene):
    def construct(self):
        # Title
        title = Text("PSI: Shared State for AI Instruments", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # The Problem
        problem_title = Text("The Fragmentation Problem", font_size=28, color=RED)
        problem_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problem_title))
        self.wait(0.3)

        # Siloed apps
        app1 = Rectangle(width=1.5, height=1.2, color=BLUE, fill_opacity=0.3)
        app1_label = Text("Health\nTracker", font_size=14)
        app1_label.move_to(app1)
        app1_group = VGroup(app1, app1_label)
        app1_group.shift(LEFT * 3.5)

        app2 = Rectangle(width=1.5, height=1.2, color=GREEN, fill_opacity=0.3)
        app2_label = Text("Parking\nApp", font_size=14)
        app2_label.move_to(app2)
        app2_group = VGroup(app2, app2_label)

        app3 = Rectangle(width=1.5, height=1.2, color=ORANGE, fill_opacity=0.3)
        app3_label = Text("Calendar", font_size=14)
        app3_label.move_to(app3)
        app3_group = VGroup(app3, app3_label)
        app3_group.shift(RIGHT * 3.5)

        self.play(
            FadeIn(app1_group),
            FadeIn(app2_group),
            FadeIn(app3_group)
        )
        self.wait(0.5)

        # Show isolation with X marks
        x1 = Text("✗", font_size=40, color=RED).move_to(app1_group.get_center() + UP * 0.8)
        x2 = Text("✗", font_size=40, color=RED).move_to(app2_group.get_center() + UP * 0.8)
        x3 = Text("✗", font_size=40, color=RED).move_to(app3_group.get_center() + UP * 0.8)

        isolation_text = Text("No cross-app reasoning!", font_size=20, color=RED)
        isolation_text.next_to(app2_group, DOWN, buff=1)

        self.play(
            Write(x1), Write(x2), Write(x3),
            Write(isolation_text)
        )
        self.wait(1)

        self.play(
            FadeOut(problem_title),
            FadeOut(app1_group), FadeOut(app2_group), FadeOut(app3_group),
            FadeOut(x1), FadeOut(x2), FadeOut(x3),
            FadeOut(isolation_text)
        )

        # PSI Solution
        solution_title = Text("PSI Solution: Shared Context Bus", font_size=28, color=GREEN)
        solution_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(solution_title))
        self.wait(0.3)

        # Shared context bus
        bus = Rectangle(width=8, height=1, color=YELLOW, fill_opacity=0.5)
        bus_label = Text("Personal Context Bus", font_size=18, color=BLACK)
        bus_label.move_to(bus)
        bus_group = VGroup(bus, bus_label)
        bus_group.move_to(ORIGIN)

        # Connected instruments
        inst1 = Rectangle(width=1.5, height=1, color=BLUE, fill_opacity=0.3)
        inst1_label = Text("Health", font_size=14)
        inst1_label.move_to(inst1)
        inst1_group = VGroup(inst1, inst1_label)
        inst1_group.next_to(bus, UP, buff=0.5).shift(LEFT * 2.5)

        inst2 = Rectangle(width=1.5, height=1, color=GREEN, fill_opacity=0.3)
        inst2_label = Text("Parking", font_size=14)
        inst2_label.move_to(inst2)
        inst2_group = VGroup(inst2, inst2_label)
        inst2_group.next_to(bus, UP, buff=0.5)

        inst3 = Rectangle(width=1.5, height=1, color=ORANGE, fill_opacity=0.3)
        inst3_label = Text("Calendar", font_size=14)
        inst3_label.move_to(inst3)
        inst3_group = VGroup(inst3, inst3_label)
        inst3_group.next_to(bus, UP, buff=0.5).shift(RIGHT * 2.5)

        # Chat agent
        chat = Rectangle(width=2, height=1, color=PURPLE, fill_opacity=0.3)
        chat_label = Text("Chat\nAgent", font_size=14)
        chat_label.move_to(chat)
        chat_group = VGroup(chat, chat_label)
        chat_group.next_to(bus, DOWN, buff=0.5)

        self.play(FadeIn(bus_group))
        self.wait(0.3)

        # Arrows connecting to bus
        arrow1 = Arrow(inst1.get_bottom(), bus.get_top() + LEFT * 2.5, color=BLUE, buff=0.1)
        arrow2 = Arrow(inst2.get_bottom(), bus.get_top(), color=GREEN, buff=0.1)
        arrow3 = Arrow(inst3.get_bottom(), bus.get_top() + RIGHT * 2.5, color=ORANGE, buff=0.1)
        arrow4 = Arrow(bus.get_bottom(), chat.get_top(), color=PURPLE, buff=0.1)

        self.play(
            FadeIn(inst1_group), FadeIn(inst2_group), FadeIn(inst3_group),
            FadeIn(chat_group)
        )
        self.play(
            Create(arrow1), Create(arrow2), Create(arrow3), Create(arrow4)
        )
        self.wait(1)

        self.play(
            FadeOut(solution_title),
            FadeOut(bus_group),
            FadeOut(inst1_group), FadeOut(inst2_group), FadeOut(inst3_group),
            FadeOut(chat_group),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(arrow4)
        )

        # Three Layers
        layers_title = Text("PSI Architecture: 3 Layers", font_size=28, color=BLUE)
        layers_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(layers_title))
        self.wait(0.3)

        # Layer boxes
        layer1 = Rectangle(width=7, height=1, color=PURPLE, fill_opacity=0.3)
        layer1_label = Text("1. Generation Layer", font_size=18)
        layer1_label.move_to(layer1)
        layer1_group = VGroup(layer1, layer1_label)
        layer1_group.shift(UP * 1.5)

        layer2 = Rectangle(width=7, height=1, color=YELLOW, fill_opacity=0.3)
        layer2_label = Text("2. Shared Context Layer", font_size=18)
        layer2_label.move_to(layer2)
        layer2_group = VGroup(layer2, layer2_label)

        layer3 = Rectangle(width=7, height=1, color=GREEN, fill_opacity=0.3)
        layer3_label = Text("3. Interaction Layer (GUI + Chat)", font_size=18)
        layer3_label.move_to(layer3)
        layer3_group = VGroup(layer3, layer3_label)
        layer3_group.shift(DOWN * 1.5)

        self.play(
            FadeIn(layer1_group),
            FadeIn(layer2_group),
            FadeIn(layer3_group)
        )
        self.wait(1.5)

        self.play(
            FadeOut(layers_title),
            FadeOut(layer1_group),
            FadeOut(layer2_group),
            FadeOut(layer3_group)
        )

        # Key Benefits
        benefits_title = Text("Key Benefits", font_size=28, color=YELLOW)
        benefits_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(benefits_title))
        self.wait(0.3)

        benefits = VGroup(
            Text("✓ Cross-module reasoning", font_size=20, color=GREEN),
            Text("✓ Persistent GUI instruments", font_size=20, color=GREEN),
            Text("✓ Synchronized chat + visual", font_size=20, color=GREEN),
            Text("✓ Person-scoped state", font_size=20, color=GREEN),
            Text("✓ Local integration (no wiring)", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        benefits.next_to(benefits_title, DOWN, buff=0.5)

        self.play(Write(benefits, run_time=2))
        self.wait(1.5)

        self.play(FadeOut(benefits_title), FadeOut(benefits))

        # Conclusion
        conclusion = VGroup(
            Text("PSI: From Fragmented Apps", font_size=26),
            Text("to Coherent Instruments", font_size=26, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        conclusion.move_to(ORIGIN)

        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(title))
