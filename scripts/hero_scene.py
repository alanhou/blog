from manim import *

class HeroScene(Scene):
    def construct(self):
        # Title
        title_en = Text("Force-Aware Imitation + Preference Learning", font_size=28, weight=BOLD)
        title_zh = Text("力感知模仿 + 偏好学习", font="Noto Sans SC", font_size=24, color=GREY_B)
        title = VGroup(title_en, title_zh).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.5)

        # Stage 1: Imitation Learning
        stage1_label = VGroup(
            Text("Stage 1: Imitation", font_size=22, color=BLUE),
            Text("阶段1：模仿", font="Noto Sans SC", font_size=18, color=BLUE_B)
        ).arrange(DOWN, buff=0.1)

        human_demo = Circle(radius=0.4, color=GREEN, fill_opacity=0.3)
        human_text = Text("Human\n人类", font_size=16, font="Noto Sans SC").move_to(human_demo)
        human = VGroup(human_demo, human_text)

        arrow1 = Arrow(ORIGIN, RIGHT * 1.5, color=WHITE, buff=0.1)

        robot_box = Rectangle(width=1.5, height=1.0, color=BLUE, fill_opacity=0.2)
        robot_text = VGroup(
            Text("Force-Aware", font_size=14),
            Text("Policy", font_size=14),
            Text("力感知策略", font="Noto Sans SC", font_size=12, color=GREY_B)
        ).arrange(DOWN, buff=0.05).move_to(robot_box)
        robot = VGroup(robot_box, robot_text)

        stage1 = VGroup(human, arrow1, robot).arrange(RIGHT, buff=0.3)

        # Stage 2: Preference Refinement
        stage2_label = VGroup(
            Text("Stage 2: Preference", font_size=22, color=YELLOW),
            Text("阶段2：偏好", font="Noto Sans SC", font_size=18, color=YELLOW_B)
        ).arrange(DOWN, buff=0.1)

        traj_box = Rectangle(width=1.2, height=0.8, color=GREY, fill_opacity=0.2)
        traj_text = Text("Trajectories\n轨迹对", font_size=14, font="Noto Sans SC").move_to(traj_box)
        trajectories = VGroup(traj_box, traj_text)

        arrow2 = Arrow(ORIGIN, RIGHT * 1.2, color=WHITE, buff=0.1)

        reward_box = Rectangle(width=1.3, height=0.8, color=YELLOW, fill_opacity=0.2)
        reward_text = VGroup(
            Text("Reward", font_size=14),
            Text("Model", font_size=14),
            Text("奖励模型", font="Noto Sans SC", font_size=12, color=GREY_B)
        ).arrange(DOWN, buff=0.05).move_to(reward_box)
        reward = VGroup(reward_box, reward_text)

        arrow3 = Arrow(ORIGIN, RIGHT * 1.2, color=WHITE, buff=0.1)

        refined_box = Rectangle(width=1.3, height=0.8, color=GREEN, fill_opacity=0.2)
        refined_text = VGroup(
            Text("Refined", font_size=14),
            Text("Policy", font_size=14),
            Text("优化策略", font="Noto Sans SC", font_size=12, color=GREY_B)
        ).arrange(DOWN, buff=0.05).move_to(refined_box)
        refined = VGroup(refined_box, refined_text)

        stage2 = VGroup(trajectories, arrow2, reward, arrow3, refined).arrange(RIGHT, buff=0.2)

        # Layout
        stage1_label.next_to(stage1, UP, buff=0.3)
        stage2_label.next_to(stage2, UP, buff=0.3)

        stage1_group = VGroup(stage1_label, stage1).move_to(UP * 1.2)
        stage2_group = VGroup(stage2_label, stage2).move_to(DOWN * 1.5)

        # Connecting arrow
        connect_arrow = Arrow(stage1.get_bottom(), stage2.get_top(), color=GREY, buff=0.2)

        self.add(title, stage1_group, stage2_group, connect_arrow)
