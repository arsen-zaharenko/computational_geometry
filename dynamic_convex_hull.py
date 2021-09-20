'''
Дано:
P = {p1(x1, y1), p2(x2, y2), … , pn(xn, yn)} – произвольное множество точек на плоскости,
причем точки в множестве генерируются не сразу, а последовательно одна за другой.

Необходимо реализовать построение выпуклой оболочки для каждого из состояний множества P и создать соответствующую анимацию.

Примечания: 
Задача решается алгоритмом "Динамической выпуклой оболочки".
'''

import matplotlib.pyplot as plt
from random import randint, random
from numpy import sin, cos, sqrt
from time import sleep

def point():
	return [randint(-40, 40),randint(-40, 40)]

def line_segments(vertices):
	if len(vertices) == 0:
		return []
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments	

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

def next(i, n):
	if (i == n):
		return 0
	return i + 1

def prev(i, n):
	if i:
		return i - 1
	return n

def visible_points(point, CH):
	i = 0
	n = len(CH) - 1

	right_point = []
	left_point = []

	while i <= n:
		if check_point(point, CH[i], CH[next(i, n)]) <= 0 and check_point(point, CH[i], CH[prev(i, n)]) < 0:
			right_point = CH[i]
			break
		i += 1

	i = 0

	while i <= n:
		if check_point(point, CH[i], CH[next(i, n)]) >= 0 and check_point(point, CH[i], CH[prev(i, n)]) > 0:
			left_point = CH[i]
			break
		i += 1

	return [left_point, right_point]

def dynamic_convex_hull(new_point, P, CH):
	if len(P) == 1:
		CH.append(P[0])
		return CH

	if len(P) == 2:
		if new_point == P[0]:
			return CH
		else:
			CH.append(new_point)
			return CH

	if len(P) == 3:
		if P[0] == P[1] == new_point:
			return CH
		elif P[0] == P[1] != new_point or P[0] == new_point != P[1] or P[1] == new_point != P[0]:
			return CH
		elif P[0] != P[1] != new_point and check_point(P[0], P[1], new_point):
			if check_point(P[0], P[1], new_point) < 0:
				CH.append(new_point)
				return CH
			else:
				CH = [P[0], new_point, P[1]]
				return CH
		else:
			CH = [min_point(P), max_point(P)]
			return CH
	else:
		v_p = visible_points(new_point, CH)

		if v_p == [[],[]]:
			return CH

		left_point = v_p[0]
		right_point = v_p[1]

		if right_point == []:
			left_point_index = CH.index(left_point)
			if left_point_index == len(CH) - 1:
				right_point = CH[0]
			else:
				right_point = CH[left_point_index + 1]			
		elif left_point == []:
			right_point_index = CH.index(right_point)
			if right_point_index == 0:
				left_point = CH[-1]
			else:
				left_point = CH[right_point_index - 1]

		left_point_index = CH.index(left_point)
		right_point_index = CH.index(right_point)

		if left_point_index == len(CH) - 1 and right_point_index == 0:
			CH.append(new_point)
			return CH
		elif left_point_index + 1 == right_point_index:
			CH.insert(right_point_index, new_point)
			return CH
		elif left_point_index < right_point_index:
			new_CH = []

			for i in CH:
				new_CH.append(i)
				if i == CH[left_point_index]:
					break
			
			new_CH.append(new_point)

			i = right_point_index

			while i < len(CH):
				new_CH.append(CH[i])
				i += 1

			return new_CH
		else:
			new_CH = []

			i = right_point_index

			while i <= left_point_index:
				new_CH.append(CH[i])
				i += 1

			new_CH.append(new_point)
			return new_CH

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(points):
	plt.ion()

	P = []
	CH = []

	i = 0

	while i < len(points):
		plt.clf()

		plt.scatter(45, 45)
		plt.scatter(45, -45)
		plt.scatter(-45, 45)
		plt.scatter(-45, -45)

		if points[i] not in P:

			P.append(points[i])

			new_point = points[i]

			CH = dynamic_convex_hull(new_point, P, CH)

			l_s = line_segments(CH)

		for j in range(len(P)):
			plt.scatter(P[j][0], P[j][1])
		plt.scatter(new_point[0], new_point[1])

		if len(CH):
			for j in range(len(CH) - 1):
				draw_line_segment(CH[j], CH[j + 1])
			draw_line_segment(CH[0], CH[-1])

		i += 1

		plt.draw()
		plt.gcf().canvas.flush_events()

		sleep(0.3)		

	plt.ioff()
	plt.show()
	
def main():   
	points = [point() for i in range(20)]

	plot_task(points)

if __name__ == '__main__':
	main()