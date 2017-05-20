from PIL import Image
import numpy as np 


def load_image(name):
	return Image.open(name)

def plusminus1(num1, num2):
	return num1 == (num2 + 1) or num1 == (num2 - 1) 

def print_map(image_access, layout, search_mode=True):
	last_access_sum = 0
	for i in range(layout[0]):
		for j in  range(layout[1]):
			if search_mode:
				if (plusminus1(sum(image_access[i, j]), last_access_sum)):
					print image_access[i, j]
					last_access_sum = sum(image_access[i, j])
				else:
					last_access_sum = sum(image_access[i, j])
					continue

def scan_y(image_access, y_size, x_val=0):
	for y in range(y_size):
		print image_access[x_val, y]



def scan_x(image_access, x_size, y_const=0, every=False):
	for x in range(x_size):
		pixels = image_access[x, y_const]
		if pixels not in [(255, 255, 255, 0)] or every:
			print x,  ":", pixels, ","


def scan_y_std(image_access, layout):
	last_access_sum = 0
	for y in  range(layout[1]):
		x_0_values = []
		x_1_values = []
		x_2_values = []
		for x in range(layout[0]):
			x_0_values.append(image_access[x, y][0])
			x_1_values.append(image_access[x, y][1])
			x_2_values.append(image_access[x, y][2])
		yield y, np.std(x_0_values) + np.std(x_1_values) + np.std(x_2_values)

			# print image_access[i, j]
"""
according to std calculations y_dimension 25, in x values (293 - 399) contains the secret key
which gives a range of 106 deformed pixels, closest factor of 8 is 112 (14 string keys * inner loop(8) = 112)
"""
if __name__ == "__main__":
	secret = load_image("secret.png")
	secret_access = secret.load()
	# scan_x(secret_access, secret.size[0]) # 16 rows of x different than default

	scan_x(secret_access, secret.size[0], 25, every=1)
	quit()
	for i in scan_y_std(secret_access, secret.size):
		if i[1] < 1 and i[1] > 0:
			print i
	# print_map(secret_access, secret.size)

