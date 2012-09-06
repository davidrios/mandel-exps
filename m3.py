import sys
from ctypes import *


def run(res, iter):
    res = c_int(res)
    iter = c_int(iter)

    s = create_string_buffer('\000' * (255 + res.value ** 2))
    libmandel = CDLL('libmandel.dylib')
    libmandel.mandel(s, res, iter, c_double(1.0))

    return s.value

if __name__ == '__main__':
    sys.stdout.write(run(int(sys.argv[1]), int(sys.argv[2])))
