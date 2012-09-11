from __future__ import division
import asyncore
import asynchat
import os
import socket
import sys
import json
from multiprocessing import cpu_count

import asynloop

JOBS = []
COMPLETED_JOBS = {}
JOBS_TOTAL = 0
COMPLETED_TOTAL = 0
TERMINATOR = '.END'


class BaseHandler(asynchat.async_chat):
    _name = None

    def __init__(self, *args, **kwargs):
        asynchat.async_chat.__init__(self, *args, **kwargs)
        self.set_terminator(TERMINATOR)
        self.ibuffer = []
        self.odata = None
        self.idata = None

    def push(self, command, data=None):
        ndata = dict(command=command, data=data)
        return asynchat.async_chat.push(self, json.dumps(ndata) + self.get_terminator())

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):
        self.idata = json.loads(''.join(self.ibuffer))
        self.ibuffer = []

        try:
            command = self.idata['command']
        except KeyError:
            self.announce('no command given')
            return

        return command

    def announce(self, msg):
        print '%s: %s' % (self._name, msg)
        pass


class ServerHandler(BaseHandler):
    def __init__(self, sock, addr, nojobs_callback):
        BaseHandler.__init__(self, sock=sock)
        self._name = 'server'
        self.announce('client connecting')
        self.nojobs_callback = nojobs_callback

    def found_terminator(self):
        global COMPLETED_TOTAL
        command = BaseHandler.found_terminator(self)

        if command == 'get':
            try:
                job = JOBS.next()
            except StopIteration:
                self.announce('no jobs left')
                self.close()
                # self.push(command='nojobs')
                return
            self.announce('sending job %s' % repr(job))
            self.push(command='job', data=job)
        elif command == 'report':
            try:
                data = self.idata['data']
            except KeyError:
                self.announce('no data sent')
                return
            self.announce('received report')
            COMPLETED_JOBS[data['job']] = data['data']
            COMPLETED_TOTAL += 1
            if COMPLETED_TOTAL == JOBS_TOTAL:
                self.nojobs_callback()
        elif command == 'terminate':
            self.close()
        else:
            self.announce('invalid command')


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        print 'creating server at %s:%s' % (host, port)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            ServerHandler(sock, addr, lambda: self.close())


class Client(BaseHandler):
    def __init__(self, host, port, clientNum):
        BaseHandler.__init__(self)
        self._name = 'client %s' % clientNum
        self.announce('connecting')
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.get_job()

    def found_terminator(self):
        command = BaseHandler.found_terminator(self)

        if command == 'job':
            try:
                job = self.idata['data']
            except KeyError:
                self.announce('no data sent')
                return
            self.announce('got job %s' % repr(job))
            # self.announce('sending report')
            self.push(command='report', data=dict(job=job[0], data=render_row(job)))
            self.get_job()

    def handle_close(self):
        self.announce('closed connection')
        self.close()

    def get_job(self):
        # self.announce('get job')
        self.push(command='get')


def render_row(args):
    row, y, size, max_iteration, x_center, zoom = args

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

        res.append(color_value)
    return res

if __name__ == '__main__':
    size = int(sys.argv[1])
    max_iteration = int(sys.argv[2])
    zoom = len(sys.argv) >= 4 and float(sys.argv[3]) or 4.0
    parallel = len(sys.argv) >= 5 and float(sys.argv[4]) or 0.2
    x_center = -1.0
    y_center = 0.0

    JOBS = ((i, (y_center + zoom * float(i - size / 2) / size),
             size, max_iteration, x_center, zoom) for i in range(size))
    JOBS_TOTAL = size

    if not parallel:
        res = map(render_row, JOBS)
    else:
        # JOBS = (i for i in xrange(10))
        pid = os.fork()
        if pid > 0:
            Server('127.0.0.1', 15005)
            asynloop.loop()
        else:
            clientNum = 0
            for cpu in range(int(parallel * cpu_count()) - 1):
                clientNum += 1
                pid = os.fork()
                if pid > 0:
                    break
            else:
                clientNum += 1

            Client('127.0.0.1', 15005, clientNum)
            asynloop.loop()
