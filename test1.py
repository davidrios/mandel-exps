import os
import select
import multiprocessing
import sys
from array import array

worker_map = {}
worker_map_r = {}


def render_row(y):
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
            color_value = 255 #- (iteration * 10 % 255)

        res.append(chr(color_value))
    return ''.join(res)


def do_row(fy):
    local_abs = abs
    two_over_size = 2.0 / size
    xr_offs = range(7, -1, -1)
    xr_iter = range(50)

    result = array('B')
    for x in range(size):
        byte_acc = 0
        for offset in xr_offs:
            z = 0j
            c = two_over_size * (x - offset) + fy

            for i in xr_iter:
                z = z * z + c
                if local_abs(z) >= 2:
                    break
            else:
                byte_acc += 1 << offset

        result.append(byte_acc)

    if x != size - 1:
        result.append(byte_acc)

    return result.tostring()

if __name__ == '__main__':
    size = int(sys.argv[1])
    x_center = -1.0
    y_center = 0.0
    zoom = 4.0
    max_iteration = 50
    out = sys.stdout
    out.write(('P4\n%d %d\n' % (size, size)).encode('ASCII'))
    for i in range(size):
        out.write(render_row(y_center + zoom * float(i - size / 2) / size))
    sys.exit(0)

    completed_total = 0
    completed = {}

    workers = 1#multiprocessing.cpu_count() * 16
    rworkers = range(workers)
    for i in rworkers:
        r, w = os.pipe()
        worker_map[i] = r, w
        worker_map_r[r] = i, w

    pid = os.fork()
    if pid > 0:
        poll = select.poll()
        for i in rworkers:
            poll.register(worker_map[i][0], select.POLLIN)
        while True:
            evs = poll.poll()
            for fd, flags in evs:
                row, data = os.read(fd, size + 7).split(':', 1)
                completed_total += 1
                completed[int(row, 16)] = data
            if completed_total == size:
                out = sys.stdout
                out.write(('P4\n%d %d\n' % (size, size)).encode('ASCII'))
                for row, data in completed.iteritems():
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
            os.write(worker_map[worker][1], ('%06x:' % y) + render_row(1.0 + 3 * float(i - size / 2) / size))
