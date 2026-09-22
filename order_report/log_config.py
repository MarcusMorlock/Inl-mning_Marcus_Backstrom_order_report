"""Logging configuration"""

import logging
from pathlib import Path


LOGGER_NAME ="order_report"
DEFAULT_LOG_FILE = "order_report.log"




def configure_log(log_name: str = LOGGER_NAME, log_file: str = DEFAULT_LOG_FILE) -> None:
    """"""
    order_logger = logging.getLogger(log_name)

    if any(isinstance(h, logging.FileHandler) for h in order_logger.handlers):
        return

    order_logger.setLevel(logging.DEBUG)
    order_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    order_logger.addHandler(console_handler)
    order_logger.addHandler(file_handler)
