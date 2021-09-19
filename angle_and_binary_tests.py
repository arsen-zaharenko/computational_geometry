'''
Дано:
P = {p1(x1, y1), p2(x2, y2), … ,pn(xn, yn)} – простой многоугольник;
Q = {q1(x1, y1), q2(x2, y2), … ,qm(xm, ym)} – выпуклый многоугольник;

Многоугольник P находится внутри многоугольника Q. 
Между этими многоугольниками (внутри Q и снаружи P) заданы k точек множества S.
Создать анимацию движения точек S внутри многоугольника Q с отражением от его стенок.
При попадании точки внутрь многоугольника P скорость ее движения обнуляется.

При выполнении задания должны быть реализованы следующие алгоритмы:
- “угловой тест” через октаны для определения положения точки относительно простого многоугольника;
- “бинарный тест” для определения положения точки относительно выпуклого многоугольника. 

Примечания: Начальные скорости движения точек можно задать как vi= (v*cos(ai), v*sin(ai)),
где ai – случайный угол от 0 до 2π, v – величина скорости. 
При переходе от кадра к кадру положение точки изменяется на вектор vi.
Если положение некоторой точки Si в следующем кадре должно оказаться за пределами выпуклого многоугольника Q
(т.е. отрезки [Si,Si + vi] и некоторый [qj, qj+1] пересекаются),
то из текущего положения точки Si осуществляем ее отражение.
Отражение – это замена вектора скорости.
'''

import matplotlib.pyplot as plt
from random import randint, random
from numpy import sin, cos
from time import sleep

class Point:
	def __init__(self, x, y, alfa, v):
		self.coords = [x, y] 
		self.velocity = v
		self.cos = cos(alfa)
		self.sin = sin(alfa)  

def line_segments(vertices):
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments	

def vector(point_1, point_2):
	return [point_2[0] - point_1[0], point_2[1] - point_1[1]]

def reflected_vector(a, b):
	s_p_1 = scalar_product(a, b)
	s_p_2 = scalar_product(b, b)
	return vector(a, [2 * s_p_1 / s_p_2 * b[0], 2 * s_p_1 / s_p_2 * b[1]])

def scalar_product(vector_1, vector_2):
	return vector_1[0]*vector_2[0] + vector_1[1]*vector_2[1]

def determinant(point_1, point_2, point_0):
	det = (point_2[0] - point_1[0])*(point_0[1] - point_1[1]) - (point_0[0] - point_1[0])*(point_2[1] - point_1[1])
	return det

def check_point(point_1, point_2, point_0):
	det = determinant(point_1, point_2, point_0)
	if (det == 0):
		return 0
	elif (det > 0):
		return -1
	else:
		return 1

def zero_dets(point_1, point_2, point_3, point_4):
	P1P3 = vector(point_1, point_3)
	P1P4 = vector(point_1, point_4)
	P2P3 = vector(point_2, point_3)
	P2P4 = vector(point_2, point_4)
	P3P1 = vector(point_3, point_1)
	P3P2 = vector(point_3, point_2)
	P4P1 = vector(point_4, point_1)
	P4P2 = vector(point_4, point_2)
	sp_1 = scalar_product(P1P3, P1P4)
	sp_2 = scalar_product(P2P3, P2P4)
	sp_3 = scalar_product(P3P1, P3P2)
	sp_4 = scalar_product(P4P1, P4P2)
	if (sp_1 < 0 or sp_2 < 0 or sp_3 < 0 or sp_4 < 0):
		return 1	

def define_line_segments_intersection(point_1, point_2, point_3, point_4):
	det_1 = determinant(point_3, point_4, point_1)
	det_2 = determinant(point_3, point_4, point_2)
	det_3 = determinant(point_1, point_2, point_3)
	det_4 = determinant(point_1, point_2, point_4)
	if (det_1 == det_2 == det_3 == det_4 == 0):
		z_d = zero_dets(point_1, point_2, point_3, point_4)
		if z_d:
			return 1	
	elif (det_1*det_2 <= 0 and det_3*det_4 <= 0):
		return 1
	else:
		return 0

def define_point_on_line_segment(point_1, point_2, point_0):
	if check_point(point_1, point_2, point_0):
		return 0
	if (point_0[0] - point_2[0]) * (point_1[1] - point_2[1]) == (point_1[0] - point_2[0]) * (point_0[1] - point_2[1]):		
		if point_1[0] - point_2[0] != 0:
			p = (point_0[0] - point_2[0]) / (point_1[0] - point_2[0])
			if 0 <= p <= 1:
				return 1
		if point_0[0] == point_1[0]:
			return 1
	return 0

def point_on_side(vertices, point):
	l_s = line_segments(vertices)
	for i in l_s:
		if define_point_on_line_segment(i[0], i[1], point):
			return 1
	return 0

def dimensional_test(vertices, point):
	x_min = min(i[0] for i in vertices)
	x_max = max(i[0] for i in vertices)
	y_min = min(i[1] for i in vertices)
	y_max = max(i[1] for i in vertices)
	if (point[0] < x_min or point[0] > x_max or point[1] < y_min or point[1] > y_max):
		return 0

def next(i, n):
	if (i == n):
		return 0
	return i + 1

def define_octan(point):
	if 0 <= point[1] < point[0]:
		return 1
	if 0 < point[0] <= point[1]:
		return 2
	if 0 <= -point[0] < point[1]:
		return 3
	if 0 < point[1] <= -point[0]:
		return 4
	if 0 <= -point[1] < -point[0]:
		return 5
	if 0 < -point[0] <= -point[1]:
		return 6
	if 0 <= point[0] < -point[1]:
		return 7
	if 0 < -point[1] <= point[0]:
		return 8

def angle_test(vertices, point):
	if dimensional_test(vertices, point) == 0:
		return 0
	if point_on_side(vertices, point):
		return 1
	s = 0
	i = 0
	n = len(vertices) - 1
	while i <= n:
		j = next(i, n)
		octan_1 = define_octan(vector(point, vertices[i]))
		octan_2 = define_octan(vector(point, vertices[j]))
		delta = octan_2 - octan_1
		if delta > 4:
			delta -= 8
		if delta < -4:
			delta += 8
		if delta == -4 or delta == 4:
			det = determinant(vertices[i], vertices[j], point)
			if det > 0:
				delta = -4
			elif det < 0:
				delta = 4
			else:
				return 1
		i += 1
		s += delta
	if s == -8 or s == 8:
		return 1
	if s == 0:
		return 0
	return -1

def binary_test(vertices, point):
	if check_point(vertices[0], vertices[1], point) != check_point(vertices[0], vertices[1], vertices[-1]) or check_point(vertices[0], vertices[-1], point) != check_point(vertices[0], vertices[-1], vertices[1]):
		return 0
	start = 1
	end = len(vertices) - 1
	while end - start > 1:
		sep = int ((start + end) / 2 if (start + end) % 2 == 0 else (start + end + 1) / 2)
		if check_point(vertices[0], vertices[sep], point) != check_point(vertices[0], vertices[sep], vertices[start]):
			start = sep
		else:
			end = sep
	if check_point(vertices[start], vertices[end], point) != check_point(vertices[start], vertices[end], vertices[0]):
		return 0
	return 1 

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

def plot_task(P, Q, points):
	plt.ion()
	
	s = 0

	for i in points:
		s += i.velocity 

	while s:
		plt.clf()

		s = 0

		for i in points:
			s += i.velocity 

		for i in range(len(P) - 1):
			draw_line_segment(P[i], P[i + 1])
		draw_line_segment(P[0], P[-1])
		for i in range(len(Q) - 1):
			draw_line_segment(Q[i], Q[i + 1])
		draw_line_segment(Q[0], Q[-1])

		for i in points:
			if angle_test(P, i.coords) or not binary_test(Q, i.coords):
				i.velocity = 0
				plt.scatter(i.coords[0], i.coords[1])
			else:
				i = define_reflection(Q, i)
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
				plt.scatter(i.coords[0], i.coords[1])					

		plt.draw()
		plt.gcf().canvas.flush_events()

		sleep(0.0001)
	
	plt.ioff()
	plt.show()
	
def main():     
	P = [[30, 0], [10, 10], [0, 30], [-10, 10], [-30, 0], [-10, -10], [0, -30], [10, -10]]
	Q = [[80, 0], [70, 40], [40, 70], [0, 80], [-40, 70], [-70, 40],[-80, 0], [-70, -40], [-40, -70], [0, -80], [40, -70], [70, -40]]
	points = []

	i = 0
	while i < 5:
		point = Point(randint(-40, 40),randint(-40, 40), random() * 6.28, randint(5, 8))
		if not angle_test(P, point.coords):
			points.append(point)
			i += 1

	plot_task(P, Q, points)

if __name__ == '__main__':
	main()