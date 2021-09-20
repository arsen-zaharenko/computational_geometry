'''
Дано:
Пусть S некоторая заданная константа и P = {p1(x1, y1), p2(x2, y2), … ,pn(xn, yn)} – произвольное множество точек на плоскости.

Необходимо реализовать анимацию, в которой точки движутся с постоянными скоростями и направлениями. 
Как только периметр выпуклой оболочки становится больше чем S все вершины оболочки меняют свои скорости на противоположные.

Примечания: 
На каждом шаге анимации строится выпуклая оболочка алгоритмом “Quick Hull”.
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

def line_segments(vertices):
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments

def determinant(point_1, point_2, point_0):
	det = (point_2[0] - point_1[0])*(point_0[1] - point_1[1]) - (point_0[0] - point_1[0])*(point_2[1] - point_1[1])
	return det

def quickhull_recur(points, p_l, p_r):
    if not points:
        return []
    if len(points) == 1:
        return [points[0].coords]
    
    p_m = max(points, key=lambda p: abs(determinant(p.coords, p_l.coords, p_r.coords)))
    P1 = [p for p in points if determinant(p.coords, p_r.coords, p_m.coords) > 0]
    P2 = [p for p in points if determinant(p.coords, p_m.coords, p_l.coords) > 0]

    CH = quickhull_recur(P1, p_m, p_r)
    CH.append(p_m.coords)
    CH += quickhull_recur(P2, p_l, p_m)

    return CH

def quickhull(points):
    CH = []
    
    p_l = min(points, key=lambda p: p.coords[0])
    p_r = max(points, key=lambda p: p.coords[0])
    
    right_points = [p for p in points if determinant(p.coords, p_l.coords, p_r.coords) > 0]
    left_points = [p for p in points if determinant(p.coords, p_l.coords, p_r.coords) < 0]

    CH.append(p_l.coords)
    CH += quickhull_recur(right_points, p_r, p_l)
    CH.append(p_r.coords)
    CH += quickhull_recur(left_points, p_l, p_r)
    return CH

def line_segment_length(point_1, point_2):
	return sqrt((point_1[0] - point_2[0]) * (point_1[0] - point_2[0]) + (point_1[1] - point_2[1]) * (point_1[1] - point_2[1]))

def perimeter(line_segments):
	p = 0
	for i in range(len(line_segments)):
		p += line_segment_length(line_segments[i][0], line_segments[i][1])
	return p

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(points, S):
	plt.ion()
	plt.clf()

	flag = False

	while True:
		if (flag):
			sleep(1)
		else:
			sleep(0.01)

		plt.scatter(250, 250)
		plt.scatter(-250, -250)
		plt.scatter(-250, 250)
		plt.scatter(250, -250)

		CH = quickhull(points)
		
		l_s = line_segments(CH)	

		CH_perimeter = perimeter(l_s)

		plt.xlabel(f'S: {S}   CH perimeter: {round(CH_perimeter, 2)}')
			
		for i in points:
				plt.scatter(i.coords[0], i.coords[1])

		for i in range(len(CH) - 1):
			draw_line_segment(CH[i], CH[i + 1])
		draw_line_segment(CH[0], CH[-1])

		if S >= CH_perimeter:
			for i in points:
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
			flag = False
		else:
			for i in points:
				i.velocity *= -1
				i.coords = [i.coords[0] + i.velocity * i.cos, i.coords[1] + i.velocity * i.sin]
			flag = True

		plt.draw()
		plt.gcf().canvas.flush_events()

		plt.clf()		

	plt.ioff()
	plt.show()
	
def main():
	S = 1000     
	points = [Point(randint(-50, 50),randint(-50, 50), random() * 6.28, randint(5, 8)) for i in range(10)]
	
	plot_task(points, S)

if __name__ == '__main__':
	main()