'''
Дано: Точки p1(x1, y1), p2(x2, y2), p0(x0, y0)

Надо: Определить положение точки p0 относительно прямой, проходящей
через точки p1 и p2 (“на прямой” или “левее”, “правее” прямой). Направление
на прямой от p1 к p2.

Примечания: в качестве результата выдается сообщение о положении точки
и картинка с изображением трех подписанных точек и прямой. 
'''

import matplotlib.pyplot as plt
from random import randint

def point():
	return [randint(-100, 100), randint(-100, 100)] 

def determinant(point_1, point_2, point_0):
	return (point_2[0] - point_1[0])*(point_0[1] - point_1[1]) - (point_0[0] - point_1[0])*(point_2[1] - point_1[1])

def check_point(point_1, point_2, point_0):
	det = determinant(point_1, point_2, point_0)
	if (det == 0):
		return 0
	elif (det > 0):
		return -1
	else:
		return 1

def define_point_place(point_1, point_2, point_0):
	check = check_point(point_1, point_2, point_0)
	if (check == 0):
		return 'на'
	elif (check == 1):
		return 'правее'
	else:
		return 'левее'

def plot_task(P1, P2, P0):
	plt.scatter(P1[0], P1[1], label = f'P1 ({P1[0]},{P1[1]})')
	plt.scatter(P2[0], P2[1], label = f'P2 ({P2[0]},{P2[1]})')
	plt.scatter(P0[0], P0[1], label = f'P0 ({P0[0]},{P0[1]})')
	plt.legend()
	plt.axline(P1, P2)
	plt.xlabel(f'Точка P0 {define_point_place(P1, P2, P0)} прямой P1P2')
	plt.show()

def main():
	P1 = point()
	P2 = point()
	while P1 == P2:
		P2 = point()
	P0 = point()
	
	plot_task(P1, P2, P0)
	
if __name__ == '__main__':
	main()
