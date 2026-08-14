from __future__ import annotations

import logging
from pathlib import Path

from tool_hub.app import configure_bounded_runtime_logging


def test_runtime_log_rotates_at_the_reviewed_size(tmp_path: Path) -> None:
    handler = configure_bounded_runtime_logging(tmp_path)
    logger = logging.getLogger("tool_hub.runtime_test")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.INFO)
    try:
        for _ in range(1400):
            logger.info("x" * 1024)
    finally:
        handler.close()
        logger.handlers = []

    logs = sorted(tmp_path.glob("tool-hub.log*"))
    assert 1 <= len(logs) <= 3
    assert all(path.stat().st_size <= 1024 * 1024 for path in logs)
