from asyncore import *
import select


def poll4(timeout=0.0, map=None):
    if map is None:
        map = socket_map
    if timeout is not None:
        # timeout is in milliseconds
        timeout = int(timeout*1000)
    pollster = select.poll()
    if map:
        for fd, obj in map.items():
            flags = 0
            if obj.readable():
                flags |= select.POLLIN | select.POLLPRI
            if obj.writable():
                flags |= select.POLLOUT
            if flags:
                # Only check for exceptions if object was either readable
                # or writable.
                flags |= select.POLLERR | select.POLLHUP | select.POLLNVAL
                pollster.register(fd, flags)
        try:
            r = pollster.poll(timeout)
        except select.error, err:
            if err.args[0] != EINTR:
                raise
            r = []
        for fd, flags in r:
            obj = map.get(fd)
            if obj is None:
                continue
            readwrite(obj, flags)


def loop_kqueue(timeout=0.0, map=None):
    if map is None:
        map = socket_map
    if timeout is not None:
        # timeout is in milliseconds
        timeout = int(timeout*1000)

    kq = select.kqueue()
    if map:
        evs = []
        for fd, obj in map.items():
            flags = select.KQ_EV_ADD | select.KQ_EV_CLEAR
            if obj.readable():
                evs.append(select.kevent(fd, filter=select.KQ_FILTER_READ, flags=flags))
            if obj.writable():
                evs.append(select.kevent(fd, filter=select.KQ_FILTER_WRITE, flags=flags))
        r_evs = kq.control(evs, 100, timeout)
        for ev in r_evs:
            obj = map.get(ev.ident)
            if obj is None:
                continue
            try:
                if ev.filter == select.KQ_FILTER_READ:
                    obj.handle_read_event()
                if ev.filter == select.KQ_FILTER_WRITE:
                    obj.handle_write_event()
            except socket.error, e:
                if e.args[0] not in (EBADF, ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED):
                    obj.handle_error()
                else:
                    obj.handle_close()
            except _reraised_exceptions:
                raise
            except:
                obj.handle_error()


def loop_epoll(timeout=0.0, map=None):
    if map is None:
        map = socket_map
    if timeout is not None:
        # timeout is in milliseconds
        timeout = int(timeout*1000)
    pollster = select.epoll()
    if map:
        for fd, obj in map.items():
            flags = 0
            if obj.readable():
                flags |= select.EPOLLIN | select.EPOLLPRI
            if obj.writable():
                flags |= select.EPOLLOUT
            if flags:
                # Only check for exceptions if object was either readable
                # or writable.
                flags |= select.EPOLLERR | select.EPOLLHUP | select.EPOLLET
                pollster.register(fd, flags)
        r = pollster.poll(timeout)
        for fd, flags in r:
            obj = map.get(fd)
            if obj is None:
                continue
            readwrite(obj, flags)


def loop(timeout=30.0, map=None, count=None):
    if map is None:
        map = socket_map

    if hasattr(select, 'kqueue'):
        print 'using kqueue'
        poll_fun = loop_kqueue
    elif hasattr(select, 'epoll'):
        print 'using epoll'
        poll_fun = loop_kqueue
    else:
        print 'using select'
        poll_fun = poll

    if count is None:
        while map:
            poll_fun(timeout, map)

    else:
        while map and count > 0:
            poll_fun(timeout, map)
            count = count - 1
