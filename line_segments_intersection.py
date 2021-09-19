'''
Дано: Точки
p1(x1, y1), p2(x2, y2),
p3(x3, y3), p4(x4, y4)

Надо: Определить пересекаются ли отрезки p1p2 и p3p4?

Примечания: в качестве результата выдается сообщение о положении
отрезков и картинка с изображением отрезков. 
'''

import matplotlib.pyplot as plt
from random import randint

def point():
	return [randint(-100, 100), randint(-100, 100)]

def determinant(point_1, point_2, point_0):
	return (point_2[0] - point_1[0])*(point_0[1] - point_1[1]) - (point_0[0] - point_1[0])*(point_2[1] - point_1[1])

def vector(point_1, point_2):
	return [point_2[0] - point_1[0], point_2[1] - point_1[1]]

def scalar_product(vector_1, vector_2):
	return vector_1[0]*vector_2[0] + vector_1[1]*vector_2[1]

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
		return 'пересекаются'

def define_line_segments_intersection(point_1, point_2, point_3, point_4):
	det_1 = determinant(point_3, point_4, point_1)
	det_2 = determinant(point_3, point_4, point_2)
	det_3 = determinant(point_1, point_2, point_3)
	det_4 = determinant(point_1, point_2, point_4)
	if (det_1 == det_2 == det_3 == det_4 == 0):
		z_d = zero_dets(point_1, point_2, point_3, point_4)
		if (z_d == 'пересекаются'):
			return 'пересекаются'	
	elif (det_1*det_2 <= 0 and det_3*det_4 <= 0):
		return 'пересекаются'
	else:
		return 'не пересекаются'

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]])

def plot_task(P1, P2, P3, P4):
	plt.scatter(P1[0], P1[1], label = f'P1 ({P1[0]},{P1[1]})')
	plt.scatter(P2[0], P2[1], label = f'P2 ({P2[0]},{P2[1]})')
	plt.scatter(P3[0], P3[1], label = f'P3 ({P3[0]},{P3[1]})')
	plt.scatter(P4[0], P4[1], label = f'P4 ({P4[0]},{P4[1]})')
	plt.legend()
	draw_line_segment(P1, P2)
	draw_line_segment(P3, P4)
	plt.xlabel(f'Отрезки P1P2 и P3P4 {define_line_segments_intersection(P1, P2, P3, P4)}')
	plt.show()

def main():
	P1 = point()
	P2 = point()
	while P1 == P2:
		P2 = point()
	P3 = point()
	P4 = point()
	while P3 == P4:
		P4 = point()

	plot_task(P1, P2, P3, P4)
	
if __name__ == '__main__':
	main()
