"""General utilities."""

import contextlib
import csv
import io
import json
import os
import signal
import socket
import threading
import urllib.error
import urllib.request
from typing import Generator, MutableMapping


class DB:
    """Manufacturer database class."""

    def __init__(self, path: str) -> None:
        self.path = path

    def get(self) -> dict[str, str]:
        """The manufacturer database."""
        with contextlib.suppress(OSError, json.JSONDecodeError):
            with open(self.path, encoding='utf-8') as file:
                return json.load(file)
        return {}

    def dump(self, headers: MutableMapping[str, str]) -> None:
        """Dump the manufacturer database."""
        request = urllib.request.Request(
            'https://standards-oui.ieee.org/oui/oui.csv', headers=headers
        )

        with contextlib.suppress(urllib.error.URLError):
            with urllib.request.urlopen(request) as response:  # nosec
                reader = csv.reader(io.StringIO(response.read().decode()))

                next(reader)  # Skip the headers

                db = {
                    row[1].lower(): row[2] for row in reader
                }

            with contextlib.suppress(OSError):
                with open(self.path, 'w', encoding='utf-8') as file:
                    json.dump(db, file, separators=(',', ':'))


def get_devices() -> list[str]:
    """Return a list of network devices."""
    names = []

    for _, name in socket.if_nameindex():
        if name == 'lo':
            continue

        operstate = os.path.join('/sys/class/net', name, 'operstate')

        with contextlib.suppress(OSError), open(operstate, 'rb') as file:
            if file.readline().rstrip() == b'up':
                names.append(name)

    return names


@contextlib.contextmanager
def ignore(signum: signal.Signals) -> Generator[None, None, None]:
    """Ignore the given signal during the execution."""
    handler = signal.getsignal(signum)
    tsig(signum, signal.SIG_IGN)
    yield
    tsig(signum, handler)


def tsig(signum: signal.Signals, handler) -> None:
    """Thread-safe signal."""
    if threading.current_thread() is not threading.main_thread():
        return
    # https://github.com/python/cpython/issues/67584
    with contextlib.suppress(TypeError):
        signal.signal(signum, handler)
