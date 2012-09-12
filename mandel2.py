from __future__ import division
import os
import select
import multiprocessing

from mandel_shared import *

worker_map = {}


def render_row(args):
    y, size, max_iteration, x_center, zoom = args

    res = []
    for i in range(size):
        x = convert_x2r(i, x_center, size, zoom)

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


def mandel(size, max_iteration, x_center, y_center, zoom):
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
                return ''.join(completed.values())
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
            data = render_row((convert_y2i(y, y_center, size, zoom),
                               size, max_iteration, x_center, zoom))
            os.write(worker_map[worker][1], row + data)
