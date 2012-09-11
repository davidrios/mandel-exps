import os
import select
import multiprocessing
import sys
from array import array
from math import ceil

worker_map = {}


def do_row(fy):
    local_abs = abs
    two_over_size = 2.0 / size
    xr_offs = range(7, -1, -1)
    xr_iter = range(50)

    result = array('B')
    for x in range(7, size, 8):
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
    step = 2.0j / size

    completed_total = 0
    completed = {}

    workers = multiprocessing.cpu_count()
    rworkers = range(workers)
    for i in rworkers:
        r, w = os.pipe()
        worker_map[i] = r, w

    pid = os.fork()
    if pid > 0:
        buf_size = int(ceil(size / 8.0) + 3)
        rfds = [p[0] for p in worker_map.values()]
        while True:
            r, w, x = select.select(rfds, [], [], .1)
            for fd in r:
                rawdata = os.read(fd, buf_size)
                row, data = rawdata[:3], rawdata[3:]
                completed_total += 1
                if sys.version[0] == '2':
                    row = ord(row[0]) << 16 | ord(row[1]) << 8 | ord(row[2])
                else:
                    row = row[0] << 16 | row[1] << 8 | row[2]
                completed[row] = data
            if completed_total == size:
                if sys.version[0] == '2':
                    out = sys.stdout
                else:
                    out = sys.stdout.buffer
                out.write(('P4\n%d %d\n' % (size, size)).encode('ASCII'))
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
            row = bytearray([y >> 16 & 0xff, y >> 8 & 0xff, y & 0xff])
            data = do_row(step * y - (1.5 + 1j))
            os.write(worker_map[worker][1], row + data)
