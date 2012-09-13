import argparse
import asyncore
import logging
import os
import socket
import sys
import uuid

from shared import WorkerServerCommand, BaseHandler

logger = logging.getLogger(__name__)

PASSWD = 'cXo*82$@3['
JOBS = []


class WorkerServer(asyncore.dispatcher):
    class Handler(BaseHandler):
        def __init__(self, sock, addr, client_id, auth_callback, close_callback):
            self.is_authenticated = False
            self.client_addr = addr
            self.client_id = client_id
            self.auth_callback = auth_callback
            self.close_callback = close_callback
            self.worker_count = 0
            self.idata = None

            BaseHandler.__init__(self, sock=sock)
            logger.debug('%s: handler created' % client_id)

        def handle_close(self):
            self.close_callback(self.client_id)
            BaseHandler.handle_close(self)
            logger.info('%s: closed' % self.client_id)

        def collect_incoming_data(self, data):
            logger.debug('%s: collected %s bytes of data' % (self.client_id, len(data)))
            logger.debug('%s: data is %s' % (self.client_id, repr(data)))
            self.ibuffer.append(data)
            if not self.is_authenticated and len(''.join(self.ibuffer)) > 12 + len(self.get_terminator()):
                logger.warn('%s: received more data than authorized before authentication, closing.' % self.client_id)
                self.close()
                return

        def found_terminator(self):
            self.idata = ''.join(self.ibuffer)
            logger.debug('%s: received message with size %s' % (self.client_id, len(self.idata)))
            self.ibuffer = []
            if len(self.idata) < 1:
                logger.warn('%s: received empty data, closing.' % self.client_id)
                self.close()
                return

            command = self.idata[0]

            if not self.is_authenticated:
                if command != WorkerServerCommand.AUTH:
                    logger.warn('%s: not trying to authenticate, closing.' % self.client_id)
                    self.close()
                    return

                if self.idata[1:11] != PASSWD:
                    logger.warn('%s: received invalid auth key, closing.' % self.client_id)
                    self.close()
                    return

                self.worker_count = ord(self.idata[11])
                self.is_authenticated = True
                self.auth_callback(self.client_id)
                logger.info('%s: connected with %s workers' % (self.client_id, self.worker_count))
                return

            if command == WorkerServerCommand.GET:
                logger.info('%s: received jobs request' % self.client_id)
                # try:
                #     job = JOBS.next()
                # except StopIteration:
                #     self.announce('no jobs left')
                #     self.close()
                #     # self.push(command='nojobs')
                #     return
                # self.announce('sending job %s' % repr(job))
                # self.push(command='job', data=job)
            elif command == WorkerServerCommand.PUT:
                logger.info('%s: receiving completed jobs' % self.client_id)
                # try:
                #     data = self.idata['data']
                # except KeyError:
                #     self.announce('no data sent')
                #     return
                # self.announce('received report')
                # COMPLETED_JOBS[data['job']] = data['data']
                # COMPLETED_TOTAL += 1
                # if COMPLETED_TOTAL == JOBS_TOTAL:
                #     self.nojobs_callback()
            else:
                logger.warn('%s: sent invalid command' % self.client_id)

    def __init__(self, host, port):
        self.clients = {}
        self.client_auth_callback = lambda id: self.handle_client_auth(id)
        self.client_close_callback = lambda id: self.handle_client_close(id)
        self.worker_count = 0

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        logger.info('listening to workers at %s:%s' % (host, port))

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            logger.warn('accept pair is None')
            return

        sock, addr = pair
        id = str(uuid.uuid4())
        logger.info('connection from %s, client id is %s' % (addr, id))
        self.clients[id] = self.Handler(sock, addr, id,
                                        self.client_auth_callback,
                                        self.client_close_callback)

    def handle_client_auth(self, id):
        logger.debug('client %s authenticated' % id)
        self.worker_count += self.clients[id].worker_count
        logger.debug('total workers increased to %s' % self.worker_count)

    def handle_client_close(self, id):
        logger.debug('client %s closed' % id)
        client = self.clients[id]
        del self.clients[id]
        self.worker_count -= client.worker_count
        logger.debug('total workers decreased to %s' % self.worker_count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mandelbrot processing server.')
    parser.add_argument('-l', '--log', dest='log_level', action='store', type=lambda s: s.upper(),
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='WARNING',
                        help='Logging level.')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(module)s:%(levelname)s: %(message)s',
                        level=args.log_level)

    s = WorkerServer('127.0.0.1', 15005)
    logger.info('server running')
    asyncore.loop()
