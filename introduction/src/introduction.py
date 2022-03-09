from tkinter import TOP
from manim import *
import time

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
				axes.c2p(*(RIGHT*vec.get_x()*1.675)), 
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
		axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(RED), 
			axes.get_y_axis().set_color(BLUE), 
			axes.get_x_axis_label(label="x").set_color(RED), 
			axes.get_y_axis_label(label="z").set_color(BLUE).shift(UP*2.5))
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
		

def fromMC(vector):
	return [vector[2], vector[0], vector[1]]