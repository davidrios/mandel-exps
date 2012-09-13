import asynchat
import json
from random import choice

from mpmath import mp


class BaseHandler(asynchat.async_chat):
    _name = None

    def __init__(self, *args, **kwargs):
        asynchat.async_chat.__init__(self, *args, **kwargs)
        self.set_terminator('.END')
        self.ibuffer = []
        self.odata = None

    def push(self, command, data=None):
        ndata = [command]
        if data:
            ndata.append(data)
        ndata.append(self.get_terminator())
        return asynchat.async_chat.push(self, ''.join(ndata))

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)


class WorkerServerCommand(object):
    AUTH = '\x01'
    GET = '\x02'
    PUT = '\x03'


class WorkerCommand(object):
    PROC = '\x01'
    WAIT = '\x02'
    RESET = '\x03'


class WorkerServerJob(object):
    def __init__(self, size, iter_max, x_center, y_center, zoom):
        self.size = size
        self.iter_max = iter_max
        self.x_center = x_center
        self.y_center = y_center
        self.zoom = zoom
        self.created = range(size)
        self.completed = []
        self.pending = []

    def next(self, workers):
        rows = []
        for i in range(workers):
            row = choice(self.created)
            try:
                self.created.remove(row)
                rows.append(row)
            except ValueError:
                break
        if len(rows) < 1:
            raise StopIteration('no jobs left')

        self.pending.extend(rows)
        req = json.dumps(dict(r=rows, s=self.size, i=self.iter_max, x=str(self.x_center),
                              y=str(self.y_center), z=str(self.zoom), p=mp.dps))
        return WorkerCommand.PROC + req

    def report(self, rows, success):
        if success:
            for row in rows:
                self.pending.remove(row)
                self.completed.append(row)
        else:
            for row in rows:
                self.pending.remove(row)
                self.created.append(row)

    def is_completed(self):
        return len(self.completed) == self.size
