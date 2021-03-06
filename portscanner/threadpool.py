from multiprocessing.pool import ThreadPool

from .socketutil import scan


def Scanner(host, lower=1, upper=64*1024, concurrency=5):
    pool = ThreadPool(concurrency)
    return pool.imap_unordered(scan, ((host, port) for port in xrange(lower, upper)))
