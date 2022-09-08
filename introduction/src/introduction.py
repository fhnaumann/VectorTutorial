import re
from telnetlib import DO
from tkinter import TOP
from turtle import Vec2D
from manim import *
import time
import math
import numpy as np
from darcula_style import DarculaStyle
from MyCode import MyCode


class SimpleGraph(VectorScene):
	def construct(self):
		axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(RED), 
			axes.get_y_axis().set_color(GREEN), 
			axes.get_x_axis_label(label="x").set_color(RED), 
			axes.get_y_axis_label(label="y").set_color(GREEN).shift(UP*2.5))
		vec = self.add_vector([4, 2], animate=False).set_color(PURPLE)
		self.label_vector(vector=vec, label=MathTex(r"\vec{v}=\begin{bmatrix}4 \\ 2\end{bmatrix}", color=PURPLE), animate=False)

class SimpleGraphWithFields(VectorScene):
	def construct(self):

		plane = NumberPlane(x_range=[-6, 6, 1], x_length=12, y_range=[-6, 6, 1], y_length=12).set_color(GREEN)
		plane.get_x_axis().set_color(RED)
		plane.get_y_axis().set_color(GREEN)
		self.add(plane)
		axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(RED), 
			axes.get_y_axis().set_color(BLUE), 
			axes.get_x_axis_label(label="x").set_color(RED), 
			axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5))
		

		vec = self.add_vector([3, 2], animate=False).set_color(PURPLE)
		self.label_vector(vector=vec, label=MathTex(r"\vec{v}=\begin{bmatrix}3 \\ 2\end{bmatrix}", color=PURPLE), animate=False)
		self.add(Square(side_length=1)
			.set_color(ORANGE)
			.shift(
				axes.c2p(*(RIGHT*vec.get_x()*2.34)), 
				axes.c2p(*(UP*vec.get_y()*2.5))
			)
		)

class Simple3DGraph(ThreeDScene):
	def construct(self):
		self.set_camera_orientation(phi=45*DEGREES, theta=-45*DEGREES)
		# self.set_camera_orientation(gamma=45*DEGREES)

		axes = ThreeDAxes()
		axes.add_coordinates()
		# Minecraft (red) X -> Manim Y
		# Minecraft (green) Y -> Manim Z
		# Minecraft (blue) Z -> Manim X
		axes.x_axis.set_color(BLUE)
		axes.z_axis.set_color(GREEN)
		axes.y_axis.set_color(RED)
		self.add(axes, 
			axes.get_x_axis_label("z").set_color(BLUE), 
			axes.get_y_axis_label("x", buff=0.3).shift(UP*1.75).set_color(RED), 
			axes.get_z_axis_label("y").shift(RIGHT*0.25, UP*0.5).set_color(GREEN))
		
		x = 2
		y = 3
		z = 3
		vector = Vector(axes.c2p(*fromMC([x, y, z]))).set_color(PURPLE)
		self.add(vector)
		self.add(Text(text="v", color=PURPLE).rotate(90*DEGREES, axis=X_AXIS).next_to(vector.get_midpoint()))
		self.add(vector.coordinate_label(n_dim=3, color=PURPLE).rotate(90*DEGREES, axis=X_AXIS))
		self.add(Vector(axes.c2p(*fromMC([0,0,z]))).set_color(BLUE))
		self.add(Vector(axes.c2p(*fromMC([x,0,0]))).set_color(RED).shift(axes.c2p(*(RIGHT*z))))
		self.add(Vector(axes.c2p(*fromMC([0,y,0]))).set_color(GREEN).shift(axes.c2p(*(RIGHT*z)), axes.c2p(*(UP*x))))
		# self.begin_ambient_camera_rotation(rate=PI/10, about="gamma")
		# self.wait(10)
		# self.stop_ambient_camera_rotation()


class UnderstandOrigin(VectorScene):
	def construct(self):
		axes = setup_2d_axes(self)
		playerLoc = self.add_vector([3, 2], animate=False).set_color(PURPLE)
		player_loc_label = self.label_vector(vector=playerLoc, label=MathTex(r"loc=\begin{bmatrix}3 \\ 2\end{bmatrix}", color=PURPLE), animate=False)
		playerDir = self.add_vector([0, 1], animate=False).set_color(ORANGE).shift(axes.c2p(playerLoc.get_x()*2, playerLoc.get_y()*2))
		player_dir_label = self.label_vector(vector=playerDir, label=MathTex(r"dir=\begin{bmatrix}0 \\ 1\end{bmatrix}", color=ORANGE), animate=False).shift(axes.c2p(playerLoc.get_x()*3.35, playerLoc.get_y()*2))
		line1 = DashedLine(start=[0,0,0], end=[3,3,0]).add_tip().set_color(GRAY)
		self.add(line1)

		self.play(FadeOut(player_loc_label, player_dir_label, line1))
		self.play(playerDir.animate.move_to([0, 0.5, 0]))
		self.wait()

		line2 = DashedLine(start=[0,0,0], end=[3,1,0]).add_tip().set_color(GRAY)
		lookingFor = self.add_vector([0, -1], animate=False).set_color(YELLOW)
		# looking_for_label = self.label_vector(vector=lookingFor, label=Tex("goal", color=YELLOW), animate=False).shift(axes.c2p(playerLoc.get_x()*2, playerLoc.get_y()*2))
		
		self.play(Create(lookingFor))
		self.play(lookingFor.animate.shift(axes.c2p(playerLoc.get_x()*2, playerLoc.get_y()*2)))
		self.play(FadeIn(line2))
		

class Addition(VectorScene):
	def construct(self):
		# self.simple_addition()
		self.triple_addition()
	
	def triple_addition(self):
		axes = setup_2d_axes(self)
		vec1 = self.add_vector([3,1], animate=False).set_color(GREEN)
		vec2 = self.add_vector([-1,-2], animate=False).set_color(ORANGE)
		vec3 = self.add_vector([-3,4], animate=False).set_color(YELLOW)
		self.wait()
		self.play(vec2.animate.move_to(axes.c2p(*(vec1.get_end() + vec2.get_end()/2))))
		self.wait()
		self.play(vec3.animate.move_to(axes.c2p(*(vec2.get_end() + vec3.get_end()/2))))
		self.wait()
		self.add_vector(vec3.get_end(), animate=True, color=PURPLE)
		self.wait(2)
	
	def simple_addition(self):
		axes = setup_2d_axes(self)
		vec1 = self.add_vector([3,1], animate=False).set_color(GREEN)
		vec2 = self.add_vector([2,3], animate=False).set_color(ORANGE)
		self.wait()
		self.play(vec2.animate.move_to(axes.c2p(*(vec1.get_end() + vec2.get_end()/2))))
		self.wait()
		vec3 = self.add_vector(vec2.get_end(), animate=True, color=PURPLE)
		self.wait(2)

class Subtraction(VectorScene):
	def construct(self):
		self.simple_subtraction()

	def simple_subtraction(self):
		axes = setup_2d_axes(self)
		vec1 = self.add_vector([3,1], animate=False).set_color(GREEN)
		vec2 = self.add_vector([2,3], animate=False).set_color(ORANGE)
		self.wait()
		self.play(Transform(vec2, Vector([-2,-3]).set_color(ORANGE)))
		self.wait()
		self.play(vec2.animate.move_to(axes.c2p(*(vec1.get_end() + vec2.get_end()/2))))
		self.wait()
		self.add_vector(vec2.get_end(), animate=True, color=PURPLE)
		self.wait(2)

class DotProduct(VectorScene):
	def construct(self):
		# self.simple_dot_product()
		# self.show_dot_product_values()

		axes = Axes(x_range=[-2,2], x_length=12, y_range=[-2,2], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(RED), 
			axes.get_y_axis().set_color(BLUE), 
			axes.get_x_axis_label(label="x").set_color(RED), 
			axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5)
		)

		theta_tracker = ValueTracker(1)

		fixed_coords = axes.c2p(*[1/2,math.sqrt(3)/2])
		fixed_vec = self.add_vector(fixed_coords, animate=False).set_color(GREEN)
		rotating_vec = fixed_vec.copy().rotate(0.1*DEGREES).set_color(ORANGE)
		theta_tex = MathTex(r"\theta="+str(int(theta_tracker.get_value()))+r"^{\circ}", color=PURPLE).move_to(Angle(fixed_vec, rotating_vec, radius=0.5+3*SMALL_BUFF, other_angle=False).point_from_proportion(0.5))
		
		def dot_result(vec1, vec2):
			res = np.array(axes.p2c(vec1.get_end())) @ np.array(axes.p2c(vec2.get_end()))
			return str(round(res, 2))
		
		dot_tex = MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", "=", dot_result(fixed_vec, rotating_vec)).shift(UR*3)
		dot_tex.set_color_by_tex(tex=r"\vec{a}", color=GREEN)
		dot_tex.set_color_by_tex(tex=r"\vec{b}", color=ORANGE)
		dot_tex.set_color_by_tex(tex=dot_result(fixed_vec, rotating_vec), color=PURPLE)
		angle = Angle(fixed_vec, rotating_vec, radius=0.5, other_angle=False)
		self.add(rotating_vec, angle, theta_tex, dot_tex)

		rotating_vec.add_updater(
			lambda x: x.become(fixed_vec.copy()).set_color(ORANGE).rotate(theta_tracker.get_value() * DEGREES,about_point=ORIGIN)
		)

		angle.add_updater(
			lambda x: x.become(Angle(fixed_vec, rotating_vec, radius=0.5, other_angle=False if theta_tracker.get_value() < 180 else True, color=PURPLE))
		)
		theta_tex.add_updater(
			lambda x: x.become(
				MathTex(r"\theta="+str(int(theta_tracker.get_value() if theta_tracker.get_value() <= 180 else 360-theta_tracker.get_value())) + r"^{\circ}", color=PURPLE)
				)
				.move_to(Angle(fixed_vec, rotating_vec, radius=0.5+3*SMALL_BUFF, other_angle=False if theta_tracker.get_value() < 180 else True)
					.point_from_proportion(0.5)
				)
		)
		
		def update_dot_text(x):
			dot_res = dot_result(fixed_vec, rotating_vec)
			math_tex = MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", "=", dot_res)
			math_tex.set_color_by_tex(tex=r"\vec{a}", color=GREEN)
			math_tex.set_color_by_tex(tex=r"\vec{b}", color=ORANGE)
			math_tex.set_color_by_tex(tex=dot_res, color=PURPLE)
			x.become(math_tex).shift(UR*3)

		dot_tex.add_updater(update_dot_text)
		self.play(theta_tracker.animate.set_value(180), run_time=5)
		self.wait()
		self.play(theta_tracker.animate.set_value(360), run_time=5)





	def show_dot_product_values(self):
		axes = Axes(x_range=[-2,2], x_length=12, y_range=[-2,2], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(RED), 
			axes.get_y_axis().set_color(BLUE), 
			axes.get_x_axis_label(label="x").set_color(RED), 
			axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5)
		)
		fixed_coords = axes.c2p(*[1/2,math.sqrt(3)/2])
		fixed = self.add_vector(fixed_coords, animate=False)
		rotating = fixed.copy().rotate(0.1*DEGREES)
		self.add(rotating)
		rotating_ref = rotating.copy()
		theta_tracker = ValueTracker(0)
		angle = Angle(fixed, rotating, other_angle=True)
		self.add(fixed, rotating, angle)

		# rotating.add_updater(
		# 	lambda x: x.become(rotating_ref.copy()).rotate(
		# 		theta_tracker.get_value() * DEGREES, about_point=ORIGIN
		# 	)
		# )
		# angle.add_updater(
		# 	lambda x: x.become(Angle(fixed, rotating, other_angle=theta_tracker.get_value()>180))
		# )
		
		self.play(theta_tracker.animate.set_value(90), run_time=1)
		self.wait()
		self.play(theta_tracker.animate.set_value(180), run_time=1)
		self.wait()
		self.play(theta_tracker.animate.set_value(270), run_time=1)
		self.wait()
		self.play(theta_tracker.animate.set_value(360), run_time=1)

	def simple_dot_product(self):
		axes = setup_2d_axes(self)
		onto = self.add_vector([4,1], animate=False).set_color(GREEN)
		self.label_vector(onto, label=MathTex(r"\vec{a}", color=GREEN), animate=False)
		squashing = self.add_vector([1,2], animate=False).set_color(ORANGE)
		self.label_vector(squashing, label=MathTex(r"\vec{b}", color=ORANGE), animate=False)
		self.wait()
		dot_product = np.dot([1,2], [4,1])
		projection_length = dot_product/np.linalg.norm([4,1])
		percent = projection_length/np.linalg.norm([4,1])
		ending = axes.c2p(4*percent, 1*percent, 0)
		dotted_line = DashedLine(start=[1,2,0], end=ending).set_color(GRAY)
		line_on_origin = np.array([ending[0]-1, ending[1]-2, 0]) # represents the dotted_line from the origin (not drawn)
		ending_vector = Vector(ending).set_color(PURPLE)
		self.play(Transform(squashing.copy(), ending_vector), Write(MathTex(r"\vec{b_{a}}").set_color(PURPLE).next_to(ending_vector, direction=DOWN*0.15)), Create(dotted_line), run_time=3)

		rotation = math.acos(np.dot([4,1], [5,0])/(np.linalg.norm([4,1])*np.linalg.norm([5,0])))
		angle = Arc(radius=0.3, angle=PI/2, arc_center=ending).set_color(GRAY).rotate(angle=rotation, about_point=ending)

		self.play(Create(angle), Create(Dot([ending[0] + 0.08, ending[1] + 0.15, 0], radius=0.02).set_color(GRAY)))

		
		first_brace = BraceBetweenPoints(point_1=ORIGIN, point_2=ending).set_color(PURPLE).shift(line_on_origin*0.5)
		first_length = MathTex(r"\lvert\lvert\vec{b_{a}}\right\rVert", color=PURPLE).next_to(first_brace, direction=DOWN*0.4)
		self.play(FadeIn(first_brace), Write(first_length))
		
		print(line_on_origin)
		second_brace = BraceBetweenPoints(point_1=ORIGIN, point_2=[4,1,0]).set_color(GREEN).shift(line_on_origin*1.2)
		second_length = MathTex(r"\lvert\lvert\vec{a}\right\rVert", color=GREEN).next_to(second_brace, direction=DOWN*0.4)
		self.play(FadeIn(second_brace), Write(second_length))

		equation = MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", r"=", r"\lvert\lvert", r"\vec{b_{a}}", r"\right\rVert", r"\cdot", r"\lvert\lvert", r"\vec{a}", r"\rvert\rvert").scale(1.5).shift(DOWN*4.5, RIGHT*3.5)
		
		equation = MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", r"=", r"\lvert\lvert\vec{b_{a}}\right\rVert", r"\cdot", r"\lvert\lvert\vec{a}\rvert\rvert").scale(1.5).shift(DOWN*4.5, RIGHT*3.5)
		
		
		equation.set_color_by_tex(tex=r"\vec{a}", color=GREEN)
		equation.set_color_by_tex(tex=r"\lvert\lvert\vec{a}\rvert\rvert", color=GREEN)
		equation.set_color_by_tex(tex=r"\vec{b}", color=ORANGE)
		equation.set_color_by_tex(tex=r"\vec{b_{a}}", color=PURPLE)
		equation.set_color_by_tex(tex=r"\lvert\lvert\vec{b_{a}}\right\rVert", color=PURPLE)
		self.play(Write(equation))
		self.wait()

class CrossProduct(ThreeDScene):
	def construct(self):
		# x -> z
		# y -> x
		# z -> y
		axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1])
		axes.get_x_axis().set_color(BLUE)
		axes.get_y_axis().set_color(RED)
		axes.get_z_axis().set_color(GREEN)
		axis_labels = VGroup(
			axes.get_x_axis_label("z").set_color(BLUE), 
			axes.get_y_axis_label("x").set_color(RED).shift(UP*1.9), 
			axes.get_z_axis_label("y").set_color(GREEN).flip(axis=Z_AXIS))
		self.add(axis_labels)
		self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
		self.add(axes)
		vec1 = Vector(direction=axes.c2p(*fromMC(3,0,1, normalize=True))).set_color(ORANGE)
		vec2 = Vector(direction=axes.c2p(*fromMC(-0.5,2,1, normalize=True))).set_color(TEAL)
		vec3 = Vector(direction=axes.c2p(*fromMC(-2,-3.5,6, normalize=True))).set_color(PURPLE)
		self.add(vec1, vec2)
		self.begin_ambient_camera_rotation(rate=0.1)
		self.wait()
		self.play(GrowArrow(vec3))
		self.wait(3)
		self.play(
			Transform(vec1, Vector(direction=axes.c2p(*fromMC(1,0,0))).set_color(ORANGE)),
			Transform(vec2, Vector(direction=axes.c2p(*fromMC(0,1,0))).set_color(TEAL)),
			Transform(vec3, Vector(direction=axes.c2p(*fromMC(0,0,1))).set_color(PURPLE))
		)
		self.wait()

class EntityLookAtPlayer1(VectorScene):
	def construct(self):
		axes, labels = setup_2d_axes(self)
		steve_head = ImageMobject("steve_head.png").scale(0.1).move_to(axes.c2p(-3,-1))
		sheep_head = ImageMobject("sheep_head.jpg").scale(0.1).move_to(axes.c2p(2,5))
		player_vec = Vector(np.array([-3,-1])).set_color(GREEN)
		sheep_vec =  Vector(np.array([2,5])).set_color(ORANGE)
		# player_vec = self.add_vector([-3,-1], animate=True, color=GREEN)#.set_color(GREEN)
		# sheep_vec = self.add_vector([2,5], animate=True, color=ORANGE)#.set_color(ORANGE)
		from_player = Vector([-2,-5]).set_color(ORANGE)
		subtract_vec = Vector([-5,-6]).set_color(PURPLE)
		math_animation = Group(axes, labels, steve_head, sheep_head, player_vec, sheep_vec, from_player, subtract_vec).scale(0.6).shift(LEFT*3)

		print(Code.styles_list)
		codeTest = Code(file_name="EntityLookAtPlayer.java", background="window", style='dracula', line_spacing=1).scale(0.7).shift(RIGHT*2.1 + DOWN*2)

		self.add(axes, labels)

		self.play(Write(codeTest), run_time=0.5)

		self.wait()
		self.play(FadeIn(steve_head), FadeIn(sheep_head))
		self.bring_to_back(steve_head, sheep_head)
		self.wait()

		marker = SurroundingRectangle(codeTest.code.chars[0])
		self.play(FadeIn(marker), run_time=0.5)
		self.play(GrowArrow(player_vec))
		self.play(Transform(marker, SurroundingRectangle(codeTest.code.chars[1])), run_time=0.5)
		self.play(GrowArrow(sheep_vec))
		self.wait()
		self.play(Transform(marker, SurroundingRectangle(codeTest.code.chars[2])), run_time=0.5)
		self.play(Transform(sheep_vec, from_player))
		self.wait()
		self.play(ApplyMethod(sheep_vec.put_start_and_end_on, axes.c2p(-3,-1), axes.c2p(-5,-6)), run_time=2)
		# self.play(sheep_vec.animate.move_to(axes.c2p(*(player_vec.get_end() + sheep_vec.get_end()/2))), run_time=2)
		self.wait()
		self.play(GrowArrow(subtract_vec))
		# subtract_vec = self.add_vector([-5,-6], animate=True, color=PURPLE).shift(UP*1.5)
		self.wait()
		self.play(Transform(marker, SurroundingRectangle(codeTest.code.chars[3:])), run_time=0.5)
		self.play(ApplyMethod(subtract_vec.put_start_and_end_on, axes.c2p(2,5), axes.c2p(-3,-1)), run_time=2)
		self.wait(2)

def setup_2d_axes(scene):
	axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
	axes.add_coordinates()
	labels = VGroup(axes.get_x_axis().set_color(RED), 
		axes.get_y_axis().set_color(BLUE), 
		axes.get_x_axis_label(label="x").set_color(RED), 
		axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5))
	return axes, labels

def fromMC(vector):
	return [vector[2], vector[0], vector[1]]
def fromMC(*coords, normalize=False):
	in_manim = [coords[2], coords[0], coords[1]]
	if normalize:
		length = math.sqrt(in_manim[0] * in_manim[0] + in_manim[1] * in_manim[1] + in_manim[2] * in_manim[2])
		in_manim = [in_manim[0] / length, in_manim[1] / length, in_manim[2] / length]
	return in_manim