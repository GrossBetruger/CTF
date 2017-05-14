import argparse
import math
import random
from PIL import Image


def do2(image_size, loaded_image, secret_string, rand1, rand2, x_factor):
    print "i, p, s, w1, w2, x", image_size, loaded_image, secret_string, rand1, rand2, x_factor
    counter = 0
    secret_string = list(secret_string)
    while len(secret_string) > 0:
        secret_char = secret_string.pop(0)
        print "secret_char:", secret_char
        for b in range(8):
            scrambled_secret_char = ((ord(secret_char) << b) & 0xFF) >> int((math.sqrt(math.sqrt(math.sqrt(16777217 - 1))) - 1))
            print "scrambled_secret_char:", scrambled_secret_char
            scrambled_x_factor = ((x_factor * (2 ** b)) & 0xFF) >> int((0x1523486567 << 23 >> 54) / 7 + 1)
            print "scrambled_x_factor:", scrambled_x_factor
            counter_devided_by_3 = int(counter / 3)
            print "counter_devided_by_3:", counter_devided_by_3
            x_pointer = ((rand1 + counter_devided_by_3) % image_size[0])
            print "x_pointer:", x_pointer
            y_pointer = (rand2 + int((counter_devided_by_3 + rand1) / image_size[0]))
            print "y_pointer:", y_pointer
            pixel_tuple = list(loaded_image[x_pointer, y_pointer])
            print "pixel_tuple:", pixel_tuple
            pixel_tuple[counter % 3] = (pixel_tuple[counter % 3] | (scrambled_secret_char ^ scrambled_x_factor))
            print "pixel_tuple[counter % 3] == ", pixel_tuple[counter % 3]
            if pixel_tuple[counter % 3] % 2 and not scrambled_secret_char ^ scrambled_x_factor:
                print "cond true!"
                pixel_tuple[counter % 3] -= 1
            loaded_image[x_pointer, y_pointer] = tuple(pixel_tuple)
            print "p", loaded_image
            counter += 1
            print "counter", counter
        x_factor += 1
        x_factor &= 0xff


def mb(*args):
    return [(args[int(i / 2)] >> ((i % 2) * 8)) & 0xff for i in range(len(args) * 2)]


def do(image, secret_string):
    loaded_image = image.load()
    rand1 = random.randint(0, (image.size[0] - int(len(secret_string) / image.size[0]) - 1) % 0xFFFF)
    rand2 = random.randint(0, (image.size[1] - int(image.size[0] % len(secret_string)) - 1) % 0xFFFF)
    print "rand1:", rand1, "rand2:", rand2
    randomized_string = "".join([chr(j) for j in mb(rand1, rand2, len(secret_string) & 0xFFFF)])
    print "randomized string", randomized_string
    do2(image.size, loaded_image, randomized_string, 0, 0, 0)
    NINETY_SEVEN = ((((165 & 44 * 2) << 5) ^ 26) ^ 41) + 46
    do2(image.size, loaded_image, secret_string, rand1, rand2, NINETY_SEVEN)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help='image file')
    parser.add_argument("string", type=str)
    parser.add_argument("out", type=str, help='png file')
    return parser.parse_args()


def main():
    args = parse_args()
    image = Image.open(args.image)
    do(image, args.string)
    image.save(args.out if args.out.endswith("png") else ".".join([args.out, "png"]))


if __name__ == "__main__":
    main()
