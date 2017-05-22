# -*- coding: utf-8 -*-
import argparse
import math
import random
from PIL import Image
from collections import defaultdict, OrderedDict
import json
import string

DEFAULT_BYTE = 255

LAST_DIRTY_X_VAL = 399

DIRTY_X_VAL = 293

DIRTY_Y_VAL = 25

default_pixel = list((255, 255, 255, 0))
FLAG = "flag{cant_you_see_hiding_in_plain_sight}"

def do2(image_size, loaded_image, secret_string, rand1, rand2, x_factor):
    print "i, p, s, w1, w2, x", image_size, loaded_image, secret_string, rand1, rand2, x_factor
    counter = 0
    secret_string = list(secret_string)
    while len(secret_string) > 0:
        print "iteration"
        secret_char = secret_string.pop(0)
        print "secret_char:", secret_char
        for b in range(8):
            print "inner loop"
            scrambled_secret_char = ((ord(secret_char) << b) & 0xFF) >> 7 # zero or one (<=127. 0, >=128, 1)
            print "scrambled_secret_char:", scrambled_secret_char
            scrambled_x_factor = ((x_factor * (2 ** b)) & 0xFF) >> 7 # zero or one (<=127. 0, >=128, 1)
            print "scrambled_x_factor:", scrambled_x_factor
            counter_devided_by_3 = int(counter / 3) # 0 0 0 1 1 1 2 2...
            print "counter_devided_by_3:", counter_devided_by_3
            x_pointer = ((rand1 + counter_devided_by_3) % image_size[0]) # starts 0, jumps 1 every 3
            print "x_pointer:", x_pointer
            y_pointer = (rand2 + int((counter_devided_by_3 + rand1) / image_size[0]))
            print "y_pointer:", y_pointer
            pixel_tuple = list(loaded_image[x_pointer, y_pointer])
            print "before:", pixel_tuple[counter % 3]
            before = pixel_tuple[counter % 3] # my line
            print "pixel_tuple:", pixel_tuple
            pixel_tuple[counter % 3] = (pixel_tuple[counter % 3] | (scrambled_secret_char ^ scrambled_x_factor)) # + 1 | + 0
            print "pixel_tuple[counter % 3] == ", pixel_tuple[counter % 3], ",counter % 3 == ", counter % 3, "xor == ", scrambled_secret_char ^ scrambled_x_factor # counter%3, 0 1 2
            print "after:", pixel_tuple[counter % 3]
            print "same:", before == pixel_tuple[counter % 3]
            if pixel_tuple[counter % 3] % 2 and not scrambled_secret_char ^ scrambled_x_factor:
                print "cond true!"
                pixel_tuple[counter % 3] -= 1
            loaded_image[x_pointer, y_pointer] = tuple(pixel_tuple)
            print "p", loaded_image
            counter += 1
            print "counter", counter
        x_factor += 1
        x_factor &= 0xff


def guess(vector, b_factor, x_factor, key_range_min=0x20, key_range_max=0x7e):
    for key in [chr(i) for i in range(key_range_min, key_range_max)]:
        predicate_vector = []
        for b in range(b_factor, b_factor+3):
            scrambled_x_factor = ((x_factor * (2 ** b)) & 0xFF) >> 7
            scrambled_secret_char = ((ord(key) << b) & 0xFF) >> 7
            predicate_vector.append(bool(scrambled_x_factor ^ scrambled_secret_char))

        if vector == predicate_vector:
            return key



def test_encoding(pixel_tuple, encoder):
    for i in range(3):
        if not encoder[i]:
            pixel_tuple[i] = pixel_tuple[i] + 1
    return pixel_tuple == default_pixel



def rev_do2(image_size, loaded_image, flag, x_factor=97):

    full_key = []
    counter = 0
    secret_string = list(flag)
    while len(secret_string) > 0:
        secret_char = secret_string.pop(0)
        for b in range(8):
            counter_devided_by_3 = int(counter / 3)  # 0 0 0 1 1 1 2 2...
            x_offset = DIRTY_X_VAL
            x_pointer = ((x_offset + counter_devided_by_3) % image_size[0]) # image_size[0] = 1116
            y_pointer = DIRTY_Y_VAL
            pixel_tuple_dirty = list(loaded_image[x_pointer, y_pointer])

            if counter % 3  == 0:
                encoder = encode_pixel(pixel_tuple_dirty)
                lucky_guess = guess(encoder, b, x_factor, key_range_min=ord(secret_char), key_range_max=256)
                full_key.append(lucky_guess)
                assert test_encoding(pixel_tuple_dirty, encoder)

            counter += 1
        x_factor += 1
        x_factor &= 0xff

    raw = full_key
    print raw
    good = ""
    indices = [2,5,7,10,13,15,18,21,23,26,29,31,34,37,39,42,45,47,50,53,55,58,61,63,66,69,71,74,77,79,82,85,87,90,93,95,98,101,103,106, 108]
    for i in range(len(raw)):
        # print indices[i], len(raw)
        if indices[i] > len(raw):
            break
        if raw[indices[i]]:
            good += raw[indices[i]]
        else: good += raw[indices[i]-1]

    return good


def pixel_taker(loaded_image, y, x_min, x_max):
    pixels = []
    for x in range(x_min, x_max+1):
        pixel_tuple_dirty = list(loaded_image[x, y])
        for p in pixel_tuple_dirty[:-1]:
            pixels.append(p)
    return pixels

def guess_char(guess, loaded_image, x_factor=97, offset=0):
    guess = ord(guess)
    flat_pixels = pixel_taker(loaded_image, DIRTY_Y_VAL, DIRTY_X_VAL, LAST_DIRTY_X_VAL)[offset:]
    counter = 0
    vector = xor(guess, x_factor)
    # print vector
    while counter < 8:
        # print "counter", counter
        # print counter, guess
        pred = vector[counter]
        # print "pred", pred
        current_byte = flat_pixels[counter]
        # print "current byte", current_byte
        # original_byte = current_byte + 1 if not pred else current_byte -1
        if current_byte == 254 and pred:
            # "bad char", chr(guess)
            return False
        elif current_byte == DEFAULT_BYTE and not pred:
            # "bad char", chr(guess)
            return False
        if counter == 7:
            # print "good char!", chr(guess)
            return True
        counter += 1
        # print


def infer_key(loaded_image):
    x_factor = 97
    offset = 0
    while True:
        for c in [chr(i) for i in range(20, 0x7e)]:
            guess = guess_char(c, loaded_image, x_factor=x_factor, offset=offset)
            if guess:
                print c,
                offset += 8
                x_factor += 1
                break


def mb(*args):
    return [(args[int(i / 2)] >> ((i % 2) * 8)) & 0xff for i in range(len(args) * 2)]


def do(image, secret_string):
    loaded_image = image.load()
    print "image layout x:", image.size[0] # 1116
    print "image layout y:", image.size[1] # 1143
    rand1 = random.randint(0, (image.size[0] - int(len(secret_string) / image.size[0]) - 1) % 0xFFFF) # ~~ 0, 1116
    rand2 = random.randint(0, (image.size[1] - int(image.size[0] % len(secret_string)) - 1) % 0xFFFF) # ~~ 0, 1143
    print "rand1:", rand1, "rand2:", rand2
    randomized_string = "".join([chr(j) for j in mb(rand1, rand2, len(secret_string) & 0xFFFF)])
    print "randomized string", randomized_string
    do2(image.size, loaded_image, randomized_string, 0, 0, 0) # NO RAND FACTORS
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

def load_changed():
    with open("changed", "r") as f:
        return OrderedDict(sorted(json.load(f).items(), key=lambda a: a[0]))

def get_pixel(x_val):
    found = load_changed().get(str(x_val))
    return found or list((255, 255, 255, 0))


def encode_pixel(pixel):
    return [x != 254 for x in pixel[:3]]


def create_flag(flag=""):
    options = []
    for c in [chr(i) for i in range(0, 256)]:

        try:
            temp = rev_do2(image.size, loaded, flag+c)
            options.append((len(set(temp[-3:])), c))
        except:
            pass
    choosen = list(sorted(options))[0][1]
    flag += choosen
    print flag
    return create_flag(flag)


def xfactor_calc():
    def inner():
        for x_factor in range(97, 0x7e):
            array = []
            for b in range(8):
                array.append(((x_factor * (2 ** b)) & 0xFF) >> 7)
            yield x_factor, array
    return list(inner())

def xor(a, b):
    binary = bin(a ^ b)[2:]
    return [bool(int(x)) for x in "0" * (8-len(binary)) + binary]


def key_calc():
    def inner():
        for secret_char in [chr(i) for i in range(97, 0x7e)]:
            array = []
            for b in range(8):
                array.append(((ord(secret_char) << b) & 0xFF) >> 7 )
            yield secret_char, array
    return list(inner())


if __name__ == "__main__":
    image = Image.open('secret.png')
    loaded = image.load()
    # print guess_char("a", loaded)
    # quit()
    infer_key(loaded)
    quit()
    for c in [chr(i) for i in range(20, 0x7e)]:
        if guess_char(c, loaded):
            print c, guess_char(c, loaded)
    quit()

    pixels = pixel_taker(loaded, 25, 293, 399)
    while pixels:
        print [pixels.pop(0) for _ in range(3)]
    quit()

    print xor(97, 0)
    # quit()

    print vals
    for x, y in vals:
        print x, int("".join([str(i) for i in y]),2)
    print "CHARS"

    vals = key_calc()
    print vals
    for x, y in vals:
        print ord(x), int("".join([str(i) for i in y]), 2)

    quit()
    # print rev_do2(image.size, loaded, flag=FLAG)
    # quit()
    print rev_do2(image.size, loaded, FLAG)
    quit()

    for c in [chr(i) for i in range(0, 256)]:
        try:
            raw = rev_do2(image.size, loaded, FLAG+c)
            if raw:
                print raw
        except:
            pass

    quit()
    main()
