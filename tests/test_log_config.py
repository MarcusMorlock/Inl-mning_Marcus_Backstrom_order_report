"""Test logging functions"""

import pytest
import logging
import re

from pathlib import Path
from log_config import configure_log, LOGGER_NAME

TEST_LOG_FILE = "tests/test_logs/test_run.log"

#Clear global logging handlers
@pytest.fixture(autouse=True)
def cleanup_logger():
    test_logger = logging.getLogger(LOGGER_NAME)
    for handler in test_logger.handlers[:]:
        test_logger.removeHandler(handler)
        handler.close()

    yield

    for handler in test_logger.handlers[:]:
        test_logger.removeHandler(handler)
        handler.close()


def test_configure_log_formatting_pattern(tmp_path: Path) -> None:
    test_log_file = tmp_path / "test_run.log"

    configure_log(log_name=LOGGER_NAME, log_file=str(test_log_file))

    logger = logging.getLogger(LOGGER_NAME)
    message = "Test log output on disk"
    logger.info(message)

    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()

    content = test_log_file.read_text(encoding="utf-8").strip()
    expected_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| INFO \| order_report \| Test log output on disk$"

    assert re.match(expected_pattern, content) is not None

def test_configure_log_creates_file_and_writes(tmp_path: Path) -> None:
    
    test_log_file = tmp_path / "test_run.log"

    configure_log(log_name=LOGGER_NAME, log_file=str(test_log_file))

    logger = logging.getLogger(LOGGER_NAME)
    message = "Test log output on disk"
    logger.info(message)

    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()

    assert test_log_file.exists()
    assert message in test_log_file.read_text(encoding="utf-8")


def test_configure_log_prevent_duplicate_handlers(tmp_path: Path, caplog) -> None:
    temp_file = tmp_path / "duplicate_check.log"

    
    configure_log(log_name=LOGGER_NAME, log_file=str(temp_file))
    configure_log(log_name=LOGGER_NAME, log_file=str(temp_file))

    logger = logging.getLogger(LOGGER_NAME)

    with caplog.at_level(logging.INFO):
        logger.info("Single event check")

    assert caplog.text.count("Single event check") == 1

