from __future__ import division
import os
import select
import multiprocessing
import sys

worker_map = {}


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
    parallel = len(sys.argv) >= 5 and float(sys.argv[4]) or 0.2
    x_center = -1.0
    y_center = 0.0

    completed_total = 0
    completed = {}

    workers = multiprocessing.cpu_count()
    rworkers = range(workers)
    for i in rworkers:
        r, w = os.pipe()
        worker_map[i] = r, w

    pid = os.fork()
    if pid > 0:
        rfds = [p[0] for p in worker_map.values()]
        incomplete = {}
        buf_size = size + 3
        while True:
            r, w, x = select.select(rfds, [], [], .1)
            for fd in r:
                rawdata = os.read(fd, buf_size - len(incomplete.get(fd, '')))
                if len(rawdata) < buf_size:
                    rawdata = incomplete[fd] = incomplete.get(fd, '') + rawdata
                if len(rawdata) == buf_size:
                    incomplete[fd] = ''
                    row, data = rawdata[:3], rawdata[3:]
                    completed_total += 1
                    row = ord(row[0]) << 16 | ord(row[1]) << 8 | ord(row[2])
                    completed[row] = data
            if completed_total == size:
                out = sys.stdout
                out.write("P5\n%d %d\n255\n" % (size, size))
                for data in completed.values():
                    out.write(data)
                break
    else:
        worker = -1
        for worker in rworkers[:-1]:
            pid = os.fork()
            if pid > 0:
                break
        else:
            worker += 1

        for y in range(worker, size, workers):
            row = chr(y >> 16 & 0xff) + chr(y >> 8 & 0xff) + chr(y & 0xff)
            data = render_row(((y_center + zoom * float(y - size / 2) / size),
                               size, max_iteration, x_center, zoom))
            os.write(worker_map[worker][1], row + data)
