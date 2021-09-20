'''
Дано: 
Координатами своих вершин в 3-х мерном пространстве задан куб.
n(n1, n2, n3) — единичный вектор.

Надо: реализовать анимацию вращения всех точек куба относительно оси
проходящей через начало координат в направлении вектора n.

Должны быть соблюдены следующие условия:
1. Вращения рассчитываются с использованием кватернионов.
2. Результат проектировать на экран двумя способами:
	a. Ортогональной проекцией.
	b. Центральной проекцией.
'''

import matplotlib.pyplot as plt
from numpy import sin, cos, pi
from time import sleep

def quaternion(n):
	rotation_angle = 0.1047
	q = [cos(0.5*rotation_angle),
    sin(0.5*rotation_angle) * n[0],
    sin(0.5*rotation_angle) * n[1],
    sin(0.5*rotation_angle) * n[2]]
	return q

def vector_product(a, b):
    return [a[1]*b[2] - b[1]*a[2], a[2]*b[0] - b[2]*a[0], a[0]*b[1] - b[0]*a[1]]

def rotate(quaternion, point):
    p = [point[0], point[1], point[2]]
    n = [quaternion[1], quaternion[2], quaternion[3]]
    v_p = vector_product(n, p)
    return [p[0]*quaternion[0] + v_p[0],
            p[1]*quaternion[0] + v_p[1],
            p[2]*quaternion[0] + v_p[2]]

def orthogonal_projection(points):
    result = []
    i = [1,0,0]
    j = [0,1,0]
    center = [20, 20, 40]

    for p in points:
        x = (p[0] - center[0]) * i[0] + (p[1] - center[1]) * i[1] + (p[2] - center[2]) * i[2]
        y = (p[0] - center[0]) * j[0] + (p[1] - center[1]) * j[1] + (p[2] - center[2]) * j[2]  
        result.append([x, y])
    return result

def central_projection(points):
    center = [20, 20, 40]
    result = []
    for p in points:
    	x = (p[0] * center[2] - center[0] * p[2]) / (center[2] - p[2])
    	y = (p[1] * center[2] - center[1] * p[2]) / (center[2] - p[2])
    	result.append([x, y])  
    return result

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def draw_cube(cube):
    draw_line_segment(cube[0], cube[1])
    draw_line_segment(cube[1], cube[3])
    draw_line_segment(cube[3], cube[2])
    draw_line_segment(cube[2], cube[0])

    draw_line_segment(cube[4], cube[5])
    draw_line_segment(cube[5], cube[7])
    draw_line_segment(cube[7], cube[6])
    draw_line_segment(cube[6], cube[4])

    draw_line_segment(cube[0], cube[4])
    draw_line_segment(cube[1], cube[5])
    draw_line_segment(cube[2], cube[6])
    draw_line_segment(cube[3], cube[7])

def plot_task(cube, n):
	plt.ion()
	plt.clf()

	q = quaternion(n)


	#ORTHOGONAL PROJECTION
	'''
	axis = orthogonal_projection([[n[0] * -70, n[1] * -70, n[2] * -70], [n[0] * 50, n[1] * 50, n[2] * 50]])

	while True:
		plt.scatter(-80, -80)
		plt.scatter(-80, 30)
		plt.scatter(30, -80)
		plt.scatter(30, 30)

		draw_cube(orthogonal_projection(cube))
		draw_line_segment(axis[0], axis[1])		

		for i in range(0, len(cube)):
			cube[i] = rotate(q, cube[i])	

		plt.draw()
		plt.gcf().canvas.flush_events()	
		plt.show()
		sleep(0.001)
		plt.clf()
	'''	


	# CENTRAL PROJECTION
	'''
	axis = central_projection([[n[0] * -100, n[1] * -100, n[2] * -100], [n[0] * 120, n[1] * 120, n[2] * 120]])

	while True:
		plt.scatter(-150, -150)
		plt.scatter(-150, 100)
		plt.scatter(100, -150)
		plt.scatter(100, 100)

		draw_cube(central_projection(cube))
		draw_line_segment(axis[0], axis[1])		

		for i in range(0, len(cube)):
			cube[i] = rotate(q, cube[i])	

		plt.draw()
		plt.gcf().canvas.flush_events()	
		plt.show()
		sleep(0.001)
		plt.clf()
	'''


	plt.ioff()
	plt.show()

def main(): 
	n = [cos(pi/3), sin(pi/3), 0]

	init_point = [5, 10, 20]
	edge = 10

	cube = [[init_point[0], init_point[1], init_point[2]],
	[init_point[0] + edge, init_point[1], init_point[2]],
	[init_point[0], init_point[1] + edge, init_point[2]],
	[init_point[0] + edge, init_point[1] + edge, init_point[2]],
    [init_point[0], init_point[1], init_point[2] + edge],
    [init_point[0] + edge, init_point[1], init_point[2] + edge],
    [init_point[0], init_point[1] + edge, init_point[2] + edge],
    [init_point[0] + edge, init_point[1] + edge, init_point[2] + edge]]


	plot_task(cube, n)

	plt.show()

if __name__ == '__main__':
	main()