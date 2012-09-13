import asynchat


class Command(object):
    GET = '\x01'
    PUT = '\x02'
    PROC = '\x03'
    WAIT = '\x04'
    RESET = '\x05'


class BaseHandler(asynchat.async_chat):
    _name = None

    def __init__(self, *args, **kwargs):
        asynchat.async_chat.__init__(self, *args, **kwargs)
        self.set_terminator('.END')
        self.ibuffer = []
        self.odata = None
        self.idata = None

    def push(self, command, data=None):
        ndata = [command]
        if data:
            ndata.append(data)
        ndata.append(self.get_terminator())
        return asynchat.async_chat.push(self, ''.join(ndata))

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):
        self.idata = ''.join(self.ibuffer)
        self.ibuffer = []
        return self.idata[0]
