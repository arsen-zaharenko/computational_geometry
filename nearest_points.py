'''
Дано:
P = {p1(x1, y1), p2(x2, y2), … , pn(xn, yn)} – произвольное множество точек на плоскости,
внутри прямоугольника A(xA, yA), B(xA, yB), C(xc, yB), D(xC, yA).
R — некоторое фиксированное число.

Надо: создать анимацию движения шариков (кругов радиуса R) с центрами в точках из P.
При столкновении со стороной из ABCD шарики отражаются.
При столкновении двух шаров друг с другом их скорости меняются на противоположные.

Примечания: на каждом кадре анимации реализуется алгоритм поиска двух ближайших элементов в множестве P.
Если расстояние между найденными ближайшими элементами меньше чем 2* R, то считаем, что шарики столкнулись. 
'''

import matplotlib.pyplot as plt
from random import randint, random
from numpy import sin, cos, sqrt
from time import sleep
from line_segments_intersection import *
from angle_and_binary_tests import *

class Point:
	def __init__(self, x, y, alfa, v, r):
		self.coords = [x, y] 
		self.velocity = v
		self.cos = cos(alfa)
		self.sin = sin(alfa)  
		self.radius = r

def line_segments(vertices):
	if len(vertices) == 0:
		return []
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments	

def line_segment_length(point_1, point_2):
	return sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def define_reflection(vertices, point):
	origin_point = point
	point_1 = point.coords
	point_2 = [point.coords[0] + point.velocity * point.cos, point.coords[1] + point.velocity * point.sin]
	l_s = line_segments(vertices)
	for l in l_s:
		if define_line_segments_intersection(point_1, point_2, l[0], l[1]):
			r_v = reflected_vector([point.cos, point.sin], vector(l[0], l[1]))
			point.cos = r_v[0]
			point.sin = r_v[1]  
			return point
	return origin_point

def reflected_vector(a, b):
	s_p_1 = scalar_product(a, b)
	s_p_2 = scalar_product(b, b)
	return vector(a, [2 * s_p_1 / s_p_2 * b[0], 2 * s_p_1 / s_p_2 * b[1]])

def brute_force(points):
	min_d = float('inf')
	nearest_points = []
	for i in range(len(points)):
		for j in range(i + 1, len(points)):
			if line_segment_length(points[i].coords, points[j].coords) < min_d:
				min_d = line_segment_length(points[i].coords, points[j].coords)
				nearest_points = [points[i], points[j]]
  
	return [nearest_points, min_d]

def divide_and_conquer(X, Y):
	if len(X) <= 3:
		return brute_force(X)
	else:
		sep = len(X) // 2
		x_sep = X[sep].coords[0]

		X_L = []
		X_R = []

		for i in range(sep + 1):
			X_L.append(X[i])
		for i in range(sep + 1, len(X)):
			X_R.append(X[i])

		Y_L = []
		Y_R = []

		for p in Y:
			if p.coords[0] <= X[sep].coords[0]:
				Y_L.append(p)
			else:
				Y_R.append(p)

		d_a_c_left = divide_and_conquer(X_L, Y_L)[0]
		d_a_c_right = divide_and_conquer(X_R, Y_R)[0]

		d_l = 0
		d_r = 0
		d = 0

		if d_a_c_left == []:
			d = line_segment_length(d_a_c_right[0].coords, d_a_c_right[1].coords)
		elif d_a_c_right == []:
			d = line_segment_length(d_a_c_left[0].coords, d_a_c_left[1].coords)
		else:
			d_l = line_segment_length(d_a_c_left[0].coords, d_a_c_left[1].coords)
			d_r = line_segment_length(d_a_c_right[0].coords, d_a_c_right[1].coords)

			d = min(d_l, d_r)

		nearest_points = []
		if d == d_r:
			nearest_points = d_a_c_right
		else:
			nearest_points = d_a_c_left

		Y_d = []
		for p in Y:
			if abs(p.coords[0] - x_sep) <= d:
				Y_d.append(p)

		i = 0
		while i < len(Y_d) - 1 and i < 7:
			new_d = line_segment_length(Y_d[i].coords, Y_d[i + 1].coords)
			if new_d <= d:
				d = new_d
				nearest_points = [Y_d[i], Y_d[i + 1]]
			i += 1

		return [nearest_points, d]

def nearest_points(points):
	if len(points) < 2:
		print('Мало точек')
		sys.exit(-1)

	X = sorted(points, key=lambda point: (point.coords[0], point.coords[1]))
	Y = sorted(points, key=lambda point: (point.coords[1], point.coords[0]))

	d_a_c = divide_and_conquer(X, Y)

	nearest_points = d_a_c[0]
	d = d_a_c[1]

	return [nearest_points, d]

def plot_task(points, R):
	plt.ion()
	plt.clf()

	while True:
		EDGE = [[80, 0], [70, 40], [40, 70], [0, 80], [-40, 70], [-70, 40],[-80, 0], [-70, -40], [-40, -70], [0, -80], [40, -70], [70, -40]]
		
		for i in range(len(EDGE) - 1):
			draw_line_segment(EDGE[i], EDGE[i + 1])
		draw_line_segment(EDGE[0], EDGE[-1])		

		for i in points:
			plt.scatter(i.coords[0], i.coords[1], s = (i.radius*2)**2)

		n_p = nearest_points(points)

		min_edge = n_p[0]
		min_d = n_p[1]

		draw_line_segment(min_edge[0].coords, min_edge[1].coords)
		plt.xlabel(f'Расстояние между объектами: {round(min_d - (min_edge[0].radius + min_edge[1].radius)*3/100/0.0625, 2)}    2*R: {2*R}')

		if 2*R <= min_d:
			for i in points:
				i = define_reflection(EDGE, i)
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
				if not binary_test(EDGE, i.coords):
				 	i.coords = [0, 0]
		else:
			for i in points:	
				if i in min_edge:
					i.velocity *= -1
				i = define_reflection(EDGE, i)
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
				if not binary_test(EDGE, i.coords):
				 	i.coords = [0, 0]				
		
		plt.draw()
		plt.gcf().canvas.flush_events()

		sleep(0.03)

		plt.clf()		

	plt.ioff()
	plt.show()

def main(): 
	# 1 segment = 0.0625 cm => 0.0625 * 100/3 = R
	R_in_segments = 4
	R = 100/3 * 0.0625 * R_in_segments
	points = [Point(randint(-40, 40), randint(-40, 40), random() * 6.28, randint(8, 10), R) for i in range(7)]
		
	plot_task(points, R_in_segments)

	plt.show()

if __name__ == '__main__':
	main()