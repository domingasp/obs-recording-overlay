import logging
import os
from pathlib import Path
import sys


def setup_logging():
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s"
    )

    log_dir = "./"
    if getattr(sys, "frozen", False):
        log_dir_path = Path(
            os.path.join(os.getenv("LOCALAPPDATA"), "OBS Recording Overlay", "Logs")
        )
        log_dir_path.mkdir(parents=True, exist_ok=True)
        log_dir = log_dir_path.as_posix()

    file_handler = logging.FileHandler(os.path.join(log_dir, "logfile.log"))
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    root_logger.setLevel(logging.INFO)
