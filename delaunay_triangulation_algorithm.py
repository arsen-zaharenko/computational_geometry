'''
Дано:
P = {p1(x1, y1), p2(x2, y2), … , pn(xn, yn)} – произвольное множество точек на плоскости.

Надо: реализовать построение триангуляции Делоне (любым алгоритмом). 
'''

import matplotlib.pyplot as plt
from random import randint
from graham_algorithm import *

def point():
	return [randint(0, 10),randint(0, 10)]

def line_segments(vertices):
	if len(vertices) == 0:
		return []
	line_segments = []
	for i in range(len(vertices) - 1):
		line_segments.append([vertices[i], vertices[i + 1]])
	line_segments.append([vertices[-1], vertices[0]])
	return line_segments	

def delaunay_triangulation(points):
	gr = graham_test(points)
	P = gr[0]
	CH = gr[1]
	l_s = line_segments(CH)

	# E = 3V - out_V - 3
	edge_limit = 3 * len(points) - len(CH) - 3

	triangulation = []
	triangulation += l_s

	new_edge = []

	for side in l_s:

		base = side

		p_m = min(P, key=lambda p: cos_angle(vector(p, base[0]), vector(p, base[1])))

		if [p_m, base[0]] in triangulation or [base[0], p_m] in triangulation:
			pass
		else:
			triangulation.append([p_m, base[0]])
			new_edge.append([p_m, base[0]]) 

		if [base[1], p_m] in triangulation or [p_m, base[1]] in triangulation:
			pass
		else:
			triangulation.append([base[1], p_m])
			new_edge.append([base[1], p_m])

	if len(triangulation) == edge_limit:
		return triangulation

	new_edge_loop = []
	for i in new_edge:
		new_edge_loop.append(i)

	while True:
		for side in new_edge:

			base = side

			p_m = min(P, key=lambda p: cos_angle(vector(p, base[0]), vector(p, base[1])))

			if [p_m, base[0]] in triangulation or [base[0], p_m] in triangulation:
				pass
			else:
				triangulation.append([p_m, base[0]])
				new_edge.append([p_m, base[0]]) 

			if [base[1], p_m] in triangulation or [p_m, base[1]] in triangulation:
				pass
			else:
				triangulation.append([base[1], p_m])
				new_edge.append([base[1], p_m])

		if len(triangulation) == edge_limit:
			return triangulation

def plot_task(points):
	for i in points:
		plt.scatter(i[0], i[1])
	
	d_t = delaunay_triangulation(points)

	for i in d_t:
		draw_line_segment(i[0], i[1])

def main(): 
	points = [point() for i in range(10)]

	# tests
	# 1
	#points = [[1, 3], [7, 2], [7, 10], [0, 2], [7, 6], [10, 0], [2, 3], [4, 8], [6, 2], [2, 4]]
	# 2
	#points = [[8,0], [8,1], [10,7], [2,8], [1,4], [4,2], [0,2]]
	# 3
	#points = [[0,0], [3,0], [6,3], [2,2], [-2,2], [0,3], [2,5], [4,4], [4,7], [-3,4], [0,6], [-2,8]]
	# 4
	#points = [[6, 7], [1, 9], [8, 9], [4, 4], [6, 4], [7, 7], [2, 8], [5, 6], [9, 5], [9, 6]]
	# 5
	#points = [[0, 3], [3, 0], [8, 10], [2, 2], [8, 6], [9, 8], [7, 1], [7, 10], [8, 1], [1, 5]]
	# 6
	#points = [[0,0],[1,1],[0,2],[-2,2],[-5,-1],[-5,-5],[0,-10],[6,-10],[13,-3],[13,5]]

	plot_task(points)

	plt.show()

if __name__ == '__main__':
	main()