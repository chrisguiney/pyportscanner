from . import threaded, threadpool, process, serial

implementations = {
    "threaded": threaded.Scanner,
    "process": process.Scanner,
    "threadpool": threadpool.Scanner,
    "serial": serial.Scanner,
}