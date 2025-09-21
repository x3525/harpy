"""Active/passive ARP discovery tool."""

import atexit
import os
import signal
import socket
import sys
import threading

from harpy.cli import Namespace, parser
from harpy.consts import CLS, GGP, LOGO, PORT, UA, WAIT_PRINT
from harpy.globs import controller, interrupts, sent
from harpy.handlers import Echo, Is
from harpy.net import Sender, Sniffer
from harpy.utils import DB, ignore, tsig


def start() -> list[threading.Thread]:
    """Start the program."""
    tsig(signal.SIGINT, stop)

    opts = parser.parse_args(namespace=Namespace())

    Echo.disable()

    sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(GGP))

    atexit.register(sock.close)

    sock.setblocking(False)  # Non-blocking mode

    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except OSError:
        pass
    finally:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((opts.device, PORT))

    db = DB(os.path.join(os.path.expanduser('~'), '.oui.json'))

    if opts.db:
        db.dump(headers={'User-Agent': UA})

    threads = []  # type: list[threading.Thread]

    network = opts.range

    sniffer = Sniffer(sock, network, db.get(), opts.F, opts.S)
    threads.append(sniffer)

    if not opts.p:
        sender = Sender(sock, network, opts.node, opts.sleep, opts.f, opts.R)
        threads.append(sender)

    for thread in threads:
        thread.start()

    while not controller.wait(WAIT_PRINT):  # Non-blocking wait
        with ignore(signal.SIGINT):
            print(CLS, *LOGO, *sniffer, opts() + '>\t' + sent.get(), sep='\n')

    return threads


def stop(*args) -> None:
    """Stop the program."""
    tsig(signal.SIGINT, signal.SIG_IGN)
    controller.set()


def join(threads: list[threading.Thread]) -> None:
    """Join all threads."""
    for thread in threads:
        thread.join()


def log() -> None:
    """Print the interrupt messages, if any."""
    for message in interrupts:
        print(message)


def main() -> None:
    """Entry point."""
    if not Is.atty(sys.stdin, sys.stdout, sys.stderr):
        return
    if not Is.fore():
        return
    if not Is.root():
        parser.print_help()
        return

    join(start())

    log()


if __name__ == '__main__':
    main()
