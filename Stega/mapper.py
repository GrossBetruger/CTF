from PIL import Image

def load_image(name):
	return Image.open(name)


def print_map(image_access, layout, search_mode=True):
	for i in range(layout[0]):
		for j in  range(layout[1]):
			if search_mode:
				if  image_access[i, j] != (255, 255, 255, 0):
					print image_access[i, j]
				else:
					continue

			print image_access[i, j]

if __name__ == "__main__":
	secret = load_image("secret.png")
	secret_access = secret.load()
	print_map(secret_access, secret.size)

