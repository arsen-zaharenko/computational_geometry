'''
Дано: P = {p1(x1, y1), p2(x2, y2), … ,pn(xn, yn)} – простой многоугольник;
p0(x0, y0) – точка.

Надо: Используя “лучевой тест” определить положение точки p0
относительно многоугольника P.

Примечания: в качестве результата выдается сообщение и картинка с
изображением точки и многоугольника с подписанными вершинами.
Первым этапом реализовать “габаритный тест”.
В случае попадания луча в вершину многоугольника обрабатывать эту
ситуацию (не генерировать новый луч).
'''

import matplotlib.pyplot as plt
from sys import exit
from point_position import point, check_point
from line_segments_intersection import define_line_segments_intersection
from simple_polygon import line_segments, define_polygon

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
		return 'не '

def next(i, n):
	if (i == n):
		return 0
	return i + 1

def prev(i, n):
	if i:
		return i - 1
	return n

def ray_test(vertices, point):
	if point_on_side(vertices, point):
		return ''
	q = [min(i[0] for i in vertices) - 1, point[1]]
	s = 0
	i = 0
	n = len(vertices) - 1
	while i <= n:
		j = next(i, n)
		if point == vertices[i] or point == vertices[j]:
		 	return ''
		if define_line_segments_intersection(point, q, vertices[i], vertices[j]) == 'пересекаются':
			if define_point_on_line_segment(point, q, vertices[i]):
				while determinant(point, q, vertices[j]) == 0:
					j = next(j, n)
				k = prev(i, n)
				while determinant(point, q, vertices[k]) == 0:
					k = prev(k, n)
				if determinant(point, q, vertices[j]) * determinant(point, q, vertices[k]) < 0:
					s += 1
				if j < i:
					break
				i = j
				continue
			if define_point_on_line_segment(point, q, vertices[j]):
				i += 1
				continue
			s += 1
		i += 1
	if s % 2:
		return ''
	return 'не '

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(vertices, point):
	d_t = dimensional_test(vertices, point)
	
	if (d_t == 'не '):
		plt.xlabel(f'Точка P {d_t}лежит в многоугольнике.')
	else:
		plt.xlabel(f'Точка P {ray_test(vertices, point)}лежит в многоугольнике.')
	
	plt.scatter(point[0], point[1], label = f'P ({point[0]},{point[1]})')
	for i in range(len(vertices) - 1):
		draw_line_segment(vertices[i], vertices[i + 1])
	draw_line_segment(vertices[0], vertices[-1])
	plt.legend()
	plt.show()

def main():
	P = point()
	vertices = []

	for i in range(int(input('Введите количество вершин простого многоугольника: '))):
			print('Введите вершину:')
			vertices.append([int(input('x: ')), int(input('y: '))])
	if define_polygon(vertices) != '':
	 	exit('Были введены вершины не простого многоугольника.')

	# test
	# P = [4,4]
	# vertices = [[1,1],[2,5],[3,3],[4,7],[5,2],[6,5],[8,5],[9,4],[10,6],[11,5],[12,5],[13,5],[13,1],[13,-1]]
	
	plot_task(vertices, P)
	
if __name__ == '__main__':
	main()
