from distutils.command.build_scripts import first_line_re
from telnetlib import DO
from tkinter import TOP
from manim import *
import time
import math

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
		self.show_dot_product_values()

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

def setup_2d_axes(scene):
	axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
	axes.add_coordinates()
	scene.add(
		axes.get_x_axis().set_color(RED), 
		axes.get_y_axis().set_color(BLUE), 
		axes.get_x_axis_label(label="x").set_color(RED), 
		axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5))
	return axes

def fromMC(vector):
	return [vector[2], vector[0], vector[1]]