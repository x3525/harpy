"""Various handlers."""

import atexit
import contextlib
import os
import sys
import termios


class Echo:
    """Terminal echo."""

    @staticmethod
    @atexit.register
    def enable() -> None:
        """Enable echo."""
        try:
            attributes = termios.tcgetattr(0)
            attributes[3] |= termios.ECHO
            termios.tcsetattr(0, termios.TCSANOW, attributes)
        except termios.error:
            pass

    @staticmethod
    def disable() -> None:
        """Disable echo."""
        try:
            attributes = termios.tcgetattr(0)
            attributes[3] &= ~termios.ECHO
            termios.tcsetattr(0, termios.TCSANOW, attributes)
        except termios.error:
            pass


class Is:
    """Multiple unrelated "is" questions."""

    @staticmethod
    def atty() -> bool:
        """Test if all file descriptors are connected to a terminal."""
        return all(
            (sys.stdin.isatty(), sys.stdout.isatty(), sys.stderr.isatty())
        )

    @staticmethod
    def fore() -> bool:
        """Test if the program is running in the foreground."""
        with contextlib.suppress(OSError):
            return os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno())
        return False

    @staticmethod
    def root() -> bool:
        """Test if user is root."""
        return os.geteuid() == 0
