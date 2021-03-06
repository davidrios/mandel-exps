from __future__ import division
import sys
from multiprocessing import Pool, cpu_count


def render_row(args):
    y, size, max_iteration, x_center, zoom = args

    res = []
    for i in range(size):
        x = x_center + zoom * float(i - size / 2) / size

        a, b = (0.0, 0.0)
        iteration = 0

        while (a ** 2 + b ** 2 <= 4.0 and iteration < max_iteration):
            a, b = a ** 2 - b ** 2 + x, 2 * a * b + y
            iteration += 1

        if iteration == max_iteration:
            color_value = 0
        else:
            color_value = 255 - (iteration * 10 % 255)

        res.append(chr(color_value))
    return ''.join(res)

if __name__ == '__main__':
    size = int(sys.argv[1])
    max_iteration = int(sys.argv[2])
    zoom = len(sys.argv) >= 4 and float(sys.argv[3]) or 4.0
    parallel = len(sys.argv) >= 5 and float(sys.argv[4]) or 0
    x_center = -1.0
    y_center = 0.0

    sys.stdout.write("P5\n%d %d\n255\n" % (size, size))
    if parallel:
        p = Pool(int(cpu_count() * parallel))
        sys.stdout.write(''.join(
            p.map(render_row,
                  (((y_center + zoom * float(i - size / 2) / size),
                    size, max_iteration, x_center, zoom) for i in range(size)))))
    else:
        for y in range(size):
            data = render_row(((y_center + zoom * float(y - size / 2) / size),
                               size, max_iteration, x_center, zoom))
            sys.stdout.write(data)
