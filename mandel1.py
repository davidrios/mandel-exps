from __future__ import division


def mandel(size, max_iteration, x_center, y_center, zoom):
    rows = []
    for j in xrange(size):
        cols = []
        for i in xrange(size):
            x = x_center + zoom * float(i - size / 2) / size
            y = y_center + zoom * float(j - size / 2) / size

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
