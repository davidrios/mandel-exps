import os
import select
# from mpmath import mp, mpf

# mp.dps = 300


def get_params(fd):
    r = select.select([fd], [], [])[0][0]
    print os.read(r, 100)
    return (1, 2, 3)


def convert_x2r(x, x_center, size, zoom):
    return x_center + zoom * (x - size / 2.0) / size


def convert_y2i(y, y_center, size, zoom):
    return y_center + zoom * (y - size / 2.0) / size
