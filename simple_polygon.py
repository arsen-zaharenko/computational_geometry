'''
Дано: P = {p1(x1, y1), p2(x2, y2), … ,pn(xn, yn)}

Надо: Определить является ли многоугольник P простым многоугольником?

Примечания: в качестве результата выдается сообщение и картинка с
изображением многоугольника с подписанными вершинами.
'''

import matplotlib.pyplot as plt
from random import randint
from line_segments_intersection import define_line_segments_intersection

def point():
	return [randint(-100, 100), randint(-100, 100)] 

def line_segments(vertices):
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments

def define_polygon(vertices):
	l_s = line_segments(vertices)
	for i in range(len(l_s)):
		if (i == 0):
			for j in range(2, len(l_s) - 1, 2):
				result = define_line_segments_intersection(l_s[i][0], l_s[i][1], l_s[j][0], l_s[j][1])
				if (result == 'пересекаются'):
					return 'не '
		else:
			for j in range(i + 2, len(l_s), 2):
				define_line_segments_intersection(l_s[i][0], l_s[i][1], l_s[j][0], l_s[j][1])
				result = define_line_segments_intersection(l_s[i][0], l_s[i][1], l_s[j][0], l_s[j][1])
				if (result == 'пересекаются'):
					return 'не '
	return ''

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(vertices):
	for i in range(len(vertices) - 1):
		draw_line_segment(vertices[i], vertices[i + 1])
	draw_line_segment(vertices[0], vertices[-1])
	plt.xlabel(f'Многоугольник {define_polygon(vertices)}является простым')
	define_polygon(vertices)
	plt.show()

def main():
	vertices = []
	for i in range(randint(4, 7)):
		vertices.append(point())

	plot_task(vertices)