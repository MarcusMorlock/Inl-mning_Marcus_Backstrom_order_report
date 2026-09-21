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

    





#Create folder in case folder don´t already exist.
# Path(log_file).parent.mkdir(parents=True, exist_ok=True)


# """Central configuration of packets logging."""

# import logging


# LOGGER_NAME = "temperature_tools"


# def configure_logging() -> None:
#     """Configure logging for temperature_tools."""
#     package_logger = logging.getLogger(LOGGER_NAME)

#     if package_logger.handlers:
#         return

#     package_logger.setLevel(logging.DEBUG)
#     package_logger.propagate = False

#     formatter = logging.Formatter(
#         "%(asctime)s | %(levelname)s | "
#         "%(name)s | %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )

#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#     console_handler.setFormatter(formatter)

#     file_handler = logging.FileHandler(
#         "temperature_tools.log",
#         encoding="utf-8",
#     )
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(formatter)

#     package_logger.addHandler(console_handler)
#     package_logger.addHandler(file_handler)