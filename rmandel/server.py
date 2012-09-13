import argparse
import asyncore
import logging
import os
import socket
import sys

from shared import Command, BaseHandler

logger = logging.getLogger(__name__)

JOBS = []
COMPLETED_JOBS = {}
JOBS_TOTAL = 0
COMPLETED_TOTAL = 0


class ServerHandler(BaseHandler):
    def __init__(self, sock, addr):
        BaseHandler.__init__(self, sock=sock)
        logger.info('client connecting from %s' % addr)
        self.client_addr = addr

    def found_terminator(self):
        global COMPLETED_TOTAL
        command = BaseHandler.found_terminator(self)

        if command == Command.GET:
            try:
                job = JOBS.next()
            except StopIteration:
                self.announce('no jobs left')
                self.close()
                # self.push(command='nojobs')
                return
            self.announce('sending job %s' % repr(job))
            self.push(command='job', data=job)
        elif command == Command.PUT:
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
        else:
            logger.warn('received invalid command (%s) from %s' % (command, self.client_addr))


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        logger.debug('listening to workers at %s:%s' % (host, port))

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            ServerHandler(sock, addr, lambda: self.close())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mandelbrot processing server.')
    parser.add_argument('-l', '--log', dest='log_level', action='store', type=lambda s: s.upper(),
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO',
                        help='Logging level.')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    s = Server('127.0.0.1', 15005)
    logger.info('server running')
    asyncore.loop()
