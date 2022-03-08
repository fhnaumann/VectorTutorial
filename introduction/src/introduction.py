from tkinter import TOP
from manim import *
import time

class SimpleGraph(VectorScene):
	def construct(self):
		axes = Axes(x_range=[-6, 6], x_length=12, y_range=[-6, 6], y_length=12)
		axes.add_coordinates()
		self.add(
			axes.get_x_axis().set_color(BLUE), 
			axes.get_y_axis().set_color(GREEN), 
			axes.get_x_axis_label(label="x").set_color(BLUE), 
			axes.get_y_axis_label(label="y").set_color(GREEN).shift(UP*2.5))
		vec = self.add_vector([4, 2], animate=False).set_color(PURPLE)
		self.label_vector(vector=vec, label=MathTex(r"\vec{v}=\begin{bmatrix}4 \\ 2\end{bmatrix}", color=PURPLE), animate=False)

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
			axes.get_x_axis_label("z (South)").set_color(BLUE), 
			axes.get_y_axis_label("x (East)", buff=0.3).shift(UP*1.75).set_color(RED), 
			axes.get_z_axis_label("y").shift(RIGHT*0.25, UP*0.5).set_color(GREEN))
		
		x = 2
		y = 3
		z = 3
		vector = Vector(fromMC([x, y, z])).set_color(PURPLE)
		self.add(vector)
		self.add(Text(text="v", color=PURPLE).rotate(90*DEGREES, axis=X_AXIS).next_to(vector.get_midpoint()))
		self.add(vector.coordinate_label(n_dim=3, color=PURPLE).rotate(90*DEGREES, axis=X_AXIS))
		self.add(Vector(fromMC([0,0,z])).set_color(BLUE))
		self.add(Vector(fromMC([x,0,0])).set_color(RED).shift(RIGHT*z))
		self.add(Vector(fromMC([0,y,0])).set_color(GREEN).shift(RIGHT*z, UP*x))
		# self.begin_ambient_camera_rotation(rate=PI/10, about="gamma")
		# self.wait(10)
		# self.stop_ambient_camera_rotation()


def fromMC(vector):
	return [vector[2], vector[0], vector[1]]