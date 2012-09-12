from __future__ import division

from mandel_shared import *


def mandel(rfd, wfd, size, max_iteration, x_center, y_center, zoom):
    rows = []
    for j in xrange(size):
        cols = []
        for i in xrange(size):
            x = convert_x2r(i, x_center, size, zoom)
            y = convert_y2i(j, y_center, size, zoom)

            a, b = (0.0, 0.0)
            iteration = 0

            while (a ** 2 + b ** 2 <= 4.0 and iteration < max_iteration):
                a, b = a ** 2 - b ** 2 + x, 2 * a * b + y
                iteration += 1

            color_value = 0
            if iteration != max_iteration:
                color_value = 255 - (iteration * 10 % 255)

            cols.append(chr(color_value))
        rows.append(''.join(cols))

    return ''.join(rows)
