from manim import *

class ConceptScene(Scene):
    def construct(self):
        # Robot arm peeling
        knife = Line(ORIGIN, DOWN * 0.8, color=GREY, stroke_width=6)
        knife_handle = Rectangle(width=0.15, height=0.3, color=YELLOW, fill_opacity=0.8).next_to(knife, UP, buff=0)
        knife_group = VGroup(knife, knife_handle).shift(LEFT * 2 + UP * 0.5)

        # Apple/produce
        apple = Circle(radius=0.6, color=RED, fill_opacity=0.5).shift(LEFT * 2 + DOWN * 0.8)
        peel = Arc(radius=0.65, angle=PI/2, color=RED_E, stroke_width=8).shift(LEFT * 1.3 + DOWN * 0.8)

        # Force sensor visualization
        force_arrow = Arrow(knife.get_bottom(), knife.get_bottom() + DOWN * 0.5, color=BLUE, buff=0)
        force_label = Text("Force\n力", font_size=14, font="Noto Sans SC", color=BLUE).next_to(force_arrow, RIGHT, buff=0.1)

        peeling = VGroup(knife_group, apple, peel, force_arrow, force_label)

        # Preference comparison
        traj_a = Rectangle(width=1.5, height=1.2, color=GREEN, fill_opacity=0.2).shift(RIGHT * 1.5 + UP * 0.8)
        check = Text("✓", font_size=40, color=GREEN).move_to(traj_a)
        label_a = Text("Better\n更好", font_size=14, font="Noto Sans SC").next_to(traj_a, DOWN, buff=0.1)

        traj_b = Rectangle(width=1.5, height=1.2, color=RED, fill_opacity=0.2).shift(RIGHT * 1.5 + DOWN * 1.2)
        cross = Text("✗", font_size=40, color=RED).move_to(traj_b)
        label_b = Text("Worse\n较差", font_size=14, font="Noto Sans SC").next_to(traj_b, DOWN, buff=0.1)

        comparison = VGroup(traj_a, check, label_a, traj_b, cross, label_b)

        # Arrow connecting
        arrow = Arrow(peeling.get_right(), comparison.get_left(), color=WHITE, buff=0.3)

        # Title
        title = VGroup(
            Text("Contact-Rich Manipulation via Preference", font_size=24),
            Text("通过偏好学习接触丰富的操作", font="Noto Sans SC", font_size=20, color=GREY_B)
        ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)

        self.add(title, peeling, arrow, comparison)
