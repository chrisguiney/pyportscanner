import argparse

from portscanner import implementations
from portscanner import serial as default


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--low", help="Low bound for port scan", type=int, default=1)
    parser.add_argument("--high", help="High bound for port scan", type=int, default=60*1024)
    parser.add_argument("--concurrency", help="Level of concurrency desired.  Not applicable if "
                                              "'serial' is chosen as implementation (default)",
                        type=int, default=5)
    parser.add_argument("--impl", help="Implementation to use.  Options are: serial, process, threaded, and threadpool",
                        default="serial")
    parser.add_argument("--verbose", help="Print each individual port status as it has been scanned",
                        action="store_true")
    parser.add_argument("host", help="Host to scan")

    args = parser.parse_args()

    ps = implementations.get(args.impl, default)(host=args.host, lower=args.low,
                                                 upper=args.high, concurrency=args.concurrency)

    open_ports = []

    for result in ps:
        if args.verbose:
            print result
        if result.open:
            open_ports.append(result)

    if len(open_ports) > 0:
        print "Open ports found: [%s]" % ", ".join([str(x.port) for x in open_ports])
    else:
        print "No open ports"

if __name__ == "__main__":
    main()