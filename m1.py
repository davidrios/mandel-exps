import sys
import math


def run(n, level, sx=None, sy=None):
    out = sys.stdout
    out.write("P5\n%d %d\n255\n" % (n, n))

    if sx is None:
        sx = 3 - 2j

    if sy is None:
        sy = 3 - 1.5j

    for y0 in range(n):
        for x0 in range(n):
            # y0 and x0 are in pixel integers
            # x  and y  are real number coordinates
            x = sx.imag + x0 * sx.real / n
            y = sy.imag + y0 * sy.real / n

            z = complex(0, 0)
            c = complex(x, y)
            for i in range(level):
                z = z * z + c

            absz = abs(z)
            if (absz < 2):
                out.write(chr(0))
            else:
                if math.isnan(absz):
                    out.write(chr(255))
                else:
                    out.write(chr(int(absz * 255)))

    out.close()


if __name__ == '__main__':
    if len(sys.argv) == 5:
        run(int(sys.argv[1]), int(sys.argv[2]), complex(sys.argv[3]), complex(sys.argv[4]))
    else:
        run(int(sys.argv[1]), int(sys.argv[2]))
