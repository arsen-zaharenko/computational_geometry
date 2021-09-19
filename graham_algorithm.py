'''
Дано:
P = {p1(x1, y1), p2(x2, y2), … , pn(xn, yn)} – произвольное множество точек на плоскости.

Надо:
Используя “алгоритм Грехэма” построить выпуклую оболочку множества P.

Примечания: в качестве результата создается анимация в которой отображается ломаная,
построенная по элементам стека, накапливающего вершины выпуклой оболочки
(любое изменение в стеке – это новый кадр анимации). 
'''

import matplotlib.pyplot as plt
from random import randint
from numpy import sqrt
from time import sleep

def point():
	return [randint(-20, 20),randint(-20, 20)]

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

def check_point(point_1, point_2, point_0):
	det = determinant(point_1, point_2, point_0)
	if (det == 0):
		return 0
	elif (det > 0):
		return -1
	else:
		return 1

def min_point(points):
	y_min = min(i[1] for i in points)
	min_points = []
	for i in points:
		if i[1] == y_min:
			min_points.append(i)
	if len(min_points) == 1:
		return min_points[0]
	return [min(i[0] for i in min_points), y_min]

def graham_test(points):
	min_p = min_point(points)
	points_sorted = [[i, cos_angle([1, 0], vector(min_p, i))] for i in points]
	points_sorted.sort(reverse = True, key = lambda point: point[1])
	points_sorted = [i[0] for i in points_sorted]

	CH = [points_sorted[0], points_sorted[1]]

	i = 2

	while i < len(points_sorted):
		plt.clf()

		for j in points_sorted:
			plt.scatter(j[0], j[1])	

		for j in range(len(CH) - 1):
			draw_line_segment(CH[j], CH[j + 1])
		
		if check_point(CH[-2], CH[-1], points_sorted[i]) < 0:
			CH.append(points_sorted[i])
			i += 1
		else:
			CH.pop()

		plt.draw()
		plt.gcf().canvas.flush_events()	
			
		sleep(0.1)

	return [points_sorted, CH]

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(points):
	plt.ion()
	g_t = graham_test(points)
	points_sorted = g_t[0]
	CH = g_t[1]
	plt.clf()
	for i in points_sorted:
		plt.scatter(i[0], i[1])	
	for i in range(len(CH) - 1):
		draw_line_segment(CH[i], CH[i + 1])
	draw_line_segment(CH[0], CH[-1])
	plt.ioff()
	plt.show()
	
def main():     
	points = [point() for i in range(20)]

	plot_task(points)

if __name__ == '__main__':
	main()