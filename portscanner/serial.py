import itertools

from .socketutil import scan


def Scanner(host, lower=1, upper=64*1024, concurrency=None):
    return itertools.imap(scan, ((host, port) for port in xrange(lower, upper)))

