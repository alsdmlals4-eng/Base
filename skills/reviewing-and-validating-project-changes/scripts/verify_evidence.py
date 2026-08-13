#!/usr/bin/env python3
"""Compatibility entrypoint for the canonical review-evidence verifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "tools/check_review_evidence.py"
SPEC = importlib.util.spec_from_file_location("check_review_evidence", CANONICAL)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"unable to load canonical verifier: {CANONICAL}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

check_record = MODULE.check_record
main = MODULE.main


if __name__ == "__main__":
    raise SystemExit(main())
