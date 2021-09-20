'''
Дано:
Пусть D некоторая заданная константа и P = {p1(x1, y1), p2(x2, y2), … , pn(xn, yn)} – произвольное множество точек на плоскости.

Необходимо реализовать анимацию, в которой точки движутся с постоянными скоростями и направлениями.
Как только расстояние между двумя точками становиться больше чем D эти две точки меняют свои скорости на противоположные.

Примечания: 
На каждом шаге анимации необходимо находить две самые удаленные точки, используя алгоритм отыскания “диаметра множества”.
Первым шагом этого алгоритма является построение выпуклой оболочки, которое необходимо реализовать “алгоритмом Джарвиса”. 
'''

import matplotlib.pyplot as plt
from random import randint, random
from numpy import sin, cos, sqrt
from time import sleep

class Point:
	def __init__(self, x, y, alfa, v):
		self.coords = [x, y] 
		self.velocity = v
		self.cos = cos(alfa)
		self.sin = sin(alfa)  	

def vector(point_1, point_2):
	return [point_2[0] - point_1[0], point_2[1] - point_1[1]]

def scalar_product(vector_1, vector_2):
	return vector_1[0]*vector_2[0] + vector_1[1]*vector_2[1]

def cos_angle(vector_1, vector_2):
	if vector_1 == [0, 0] or vector_2 == [0, 0]:
		return 2
	return scalar_product(vector_1, vector_2) / (sqrt(scalar_product(vector_1, vector_1) * scalar_product(vector_2, vector_2)))

def determinant(point_1, point_2, point_0):
	det = (point_2[0] - point_1[0])*(point_0[1] - point_1[1]) - (point_0[0] - point_1[0])*(point_2[1] - point_1[1])
	return det

def next(i, n):
	if (i == n):
		return 0
	return i + 1

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def min_point(points):
	y_min = min(i.coords[1] for i in points)
	min_points = []
	for i in points:
		if i.coords[1] == y_min:
			min_points.append(i)
	if len(min_points) == 1:
		return min_points[0]
	p = [min(i.coords[0] for i in min_points), y_min]
	for i in points:
		if i.coords == p:
			return i 

def max_point(points):
	y_max = max(i.coords[1] for i in points)
	max_points = []
	for i in points:
		if i.coords[1] == y_max:
			max_points.append(i)
	if len(max_points) == 1:
		return max_points[0]
	p = [max(i.coords[0] for i in max_points), y_max]
	for i in points:
		if i.coords == p:
			return i			

def line_segment_length(point_1, point_2):
	return sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def rightest_point(points, point):
	active_point = [point.coords[0], point.coords[1]]
	higher_than_active  = []
	for i in points:
		if i.coords[1] > active_point[1]:
			higher_than_active.append(i.coords)
	rightest_points = [[i, cos_angle([1, 0], vector(active_point, i))] for i in higher_than_active]
	rightest_points.sort(reverse = True, key = lambda point: point[1])
	rightest_point = rightest_points[0][0]

	for i in points:
		if i.coords == rightest_point:
			return i

def leftist_point(points, point):
	active_point = [point.coords[0], point.coords[1]]
	lower_than_active  = []
	for i in points:
		if i.coords[1] < active_point[1]:
			lower_than_active.append(i.coords)
	leftist_points = [[i, cos_angle([-1, 0], vector(active_point, i))] for i in lower_than_active]
	leftist_points.sort(reverse = True, key = lambda point: point[1])
	leftist_point = leftist_points[0][0]

	for i in points:
		if i.coords == leftist_point:
			return i

def diameter_of_set(points):
	pairs = []
	n = len(points) - 1
	
	p_n = n
	p = p_n
	q = next(p, n) 
	
	while abs(determinant(points[p], points[next(p, n)], points[next(q, n)])) > abs(determinant(points[p], points[next(p, n)], points[q])):
		q = next(q, n)

	q_0 = q
	p_0 = 0
	
	while q != p_0:
		p = next(p, n)
		pairs.append([points[p], points[q]])
		while abs(determinant(points[p], points[next(p, n)], points[next(q, n)])) > abs(determinant(points[p], points[next(p, n)], points[q])) and q != p_0:
			q = next(q, n)
			if [p, q] != [q_0, p_0]:
				pairs.append([points[p], points[q]])
		if abs(determinant(points[p], points[next(p, n)], points[next(q, n)])) == abs(determinant(points[p], points[next(p, n)], points[q])):
			if [p, q] != [q_0, p_n]:
				pairs.append([points[p], points[next(q, n)]])

	max_distance = 0
	diameter = 0
	
	for i in pairs:
		distance = line_segment_length(i[0], i[1])
		if distance > max_distance:
			max_distance = distance
			diameter = i

	return diameter

def jarvis(points):
	lowest_point = min_point(points)
	highest_point = max_point(points)
	CH = [lowest_point]
	while CH[-1] != highest_point:
		CH.append(rightest_point(points, CH[-1]))
	while CH[-1] != lowest_point:
		CH.append(leftist_point(points, CH[-1]))
	CH.pop()
	CH = [i.coords for i in CH]
	return CH

def plot_task(points, D):
	plt.ion()
	plt.clf()

	while True:

		sleep(0.01)

		plt.scatter(250, 250)
		plt.scatter(-250, -250)
		plt.scatter(-250, 250)
		plt.scatter(250, -250)

		CH = jarvis(points)
		
		diameter = diameter_of_set(CH)		

		diameter_length = line_segment_length(diameter[0], diameter[1])

		draw_line_segment(diameter[0], diameter[1])

		plt.xlabel(f'D: {D}   CH diameter: {round(diameter_length, 2)}')
			
		for i in points:
				plt.scatter(i.coords[0], i.coords[1])

		for i in range(len(CH) - 1):
			draw_line_segment(CH[i], CH[i + 1])
		draw_line_segment(CH[0], CH[-1])

		if D >= diameter_length:
			for i in points:
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
		else:
			for i in points:
				if i.coords == diameter[0] or i.coords == diameter[1]:
					i.velocity *= -1
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]

		plt.draw()
		plt.gcf().canvas.flush_events()

		plt.clf()		

	plt.ioff()
	plt.show()
	
def main():
	D = 400     
	points = [Point(randint(-50, 50),randint(-50, 50), random() * 6.28, randint(5, 8)) for i in range(20)]
	
	plot_task(points, D)

if __name__ == '__main__':
	main()