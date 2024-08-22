import logging
import os
import sys
import msvcrt
import atexit

logger = logging.getLogger(__name__)


class SingleInstance:
    """Ensure only 1 instance of the app is running."""

    def __init__(self, lockfile):
        self._lockfile = lockfile
        self.fd = None

        try:
            logger.info("Attempting to open lockfile")
            self.fd = open(self._lockfile, "w")
            msvcrt.locking(self.fd.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            logger.info("An instance of the application is already running")
            sys.exit("An instance of the app is already running.")

        atexit.register(self.release_lock)

    def release_lock(self):
        if self.fd:
            logger.info("App shutting down, removing lockfile")
            msvcrt.locking(self.fd.fileno(), msvcrt.LK_UNLCK, 1)
            self.fd.close()
            os.remove(self._lockfile)
