import sys


def run(size, max_iteration, canvas, out=sys.stdout):
    x_center = -1.39965
    y_center = 0.0

    out.write("P5\n%d %d\n255\n" % (size, size))
    for j in xrange(size):
        for i in xrange(size):
            x = x_center + canvas * float(i - size / 2) / size
            y = y_center + canvas * float(j - size / 2) / size

            a, b = (0.0, 0.0)
            iteration = 0

            while (a ** 2 + b ** 2 <= 4.0 and iteration < max_iteration):
                a, b = a ** 2 - b ** 2 + x, 2 * a * b + y
                iteration += 1

            if iteration == max_iteration:
                color_value = 0
            else:
                color_value = 255 #- (iteration * 10 % 255)

            out.write(chr(color_value))

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]),
        len(sys.argv) >= 4 and float(sys.argv[3]) or 4.0)
