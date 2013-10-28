import socket


def is_open(host, port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def scan(hostport):
    host, port = hostport
    return ScanResult(port, is_open(host, port))


class ScanResult(object):
    def __init__(self, port, result):
        self.port = port
        self.result = result

    @property
    def open(self):
        return self.result


    def __str__(self):
        return "%s: %s" % (self.port, self.result)