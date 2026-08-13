#!/usr/bin/env python3
"""Check a review record against repository facts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_record(root: Path, record_path: Path) -> tuple[dict[str, Any], list[str]]:
    if not record_path.is_absolute():
        record_path = root / record_path
    try:
        record = read_json(record_path)
    except (OSError, json.JSONDecodeError) as error:
        message = f"record unavailable: {error}"
        return {"state": "FAIL", "errors": [message]}, [message]
    return {"state": "PENDING", "record": record, "errors": []}, []
