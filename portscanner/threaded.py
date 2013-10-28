from Queue import Queue
from threading import Thread

from .socketutil import scan


class ThreadedPortScanIter(object):
    def __init__(self, queue, manager):
        self.manager = manager
        self.queue = queue

    def next(self):
        for item in iter(self.queue.get, self.manager.SENTINEL):
            self.queue.task_done()
            return item
        raise StopIteration

    def __iter__(self):
        return self


class ThreadedPortScannerManager(object):
    SENTINEL = "STOP"

    def __init__(self, host):
        self.host = host
        self.complete = False

    def _thread_factory(self, in_queue, out_queue):
        t = Thread(target=self._scan, args=(in_queue, out_queue))
        t.daemon = True
        return t

    def _scan(self, in_queue, out_queue):
        for port in iter(in_queue.get, self.SENTINEL):

            out_queue.put(scan((self.host, port)))
            in_queue.task_done()
        in_queue.task_done()

    def __call__(self, lower, upper, concurrency, in_queue, out_queue):
        """
        @type in_queue Queue
        @param in_queue: Queue in which to feed ports
        """

        pool = [self._thread_factory(in_queue, out_queue)
                for _ in xrange(0, concurrency)]
        map(lambda t: t.start(), pool)

        for port in xrange(lower, upper):
            in_queue.put(port)

        for _ in pool:
            in_queue.put(self.SENTINEL)

        in_queue.join()
        out_queue.put(self.SENTINEL)


def Scanner(host, lower=1, upper=64*1024, concurrency=5):
    in_queue = Queue()
    out_queue = Queue()
    manager = ThreadedPortScannerManager(host)
    t = Thread(target=manager, kwargs={
        "lower": lower,
        "upper": upper,
        "concurrency": concurrency,
        "in_queue": in_queue,
        "out_queue": out_queue
    })
    t.daemon = True
    t.start()
    return ThreadedPortScanIter(out_queue, manager)