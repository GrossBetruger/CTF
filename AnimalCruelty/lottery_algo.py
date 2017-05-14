from math import ceil, floor


def round(num):
    if num - int(num) > 0.5:
        return ceil(num)
    else:
        return floor(num)


def lottery(x):
    print x
    x = x / 2.
    print x
    x = int(x) ^ 975782977
    print x

    if (x & 255) > 83:
        print "NORM TRUE"
        x = x + 256
        print x

    x = x / 39.
    print x

    for i in range(3):
        x = x * 33
        print x
        x -= 1
        print x
        x = x / 4.
        print x
        x = int(x) ^ 102
        print x
    print x
    return x


n = 200
for i in range(n):
    for j in range(n):
        assert (i ^ j) == (j ^ i)


def rev_lottery(x):
    for i in range(3):
        print x
        x = int(x) ^ 102
        print x
        x *= 4
        print x
        x += 1
        print x
        x = x / 33.
        print x

    x *= 39
    print x
    if ((int(x) - 256) & 255 > 83):
        print "REV TRUE"
        x -= 256
        print x

    x = int(x) ^ 975782977
    print x
    x *= 2
    print x
    return round(x)

def half_lottery(x):
    for i in range(3):
        x = x * 33
        x -= 1
        x = x / 4
        x = x ^ 102
    return x

def half_rev_lottery(x):
    for i in range(3):
        x = int(x) ^ 102
        x *= 4
        x += 1
        x = round(x/33.)
    return x

def rev_lottery_head(x):
    x *= 39
    if ((int(x) - 256) & 255 > 83):
        x += 256

    x = int(x) ^ 975782977
    x *= 2
    return x

def lottery_head(x):
    x = x / 2.
    x = int(x) ^ 975782977

    if (x & 255) > 83:
        x = x + 256
    x = x / 39.
    return x


if __name__ == "__main__":
    print "REVERSE LOTTERY:\n"
    print rev_lottery(38342)
    print "NORM LOTTERY:\n"
    print lottery(1951570780)
    quit()

    # print rev_lottery_head(38342)
    # print lottery_head(1954491094)
    #
    #
    print half_rev_lottery(38342)
    print half_lottery(72)


