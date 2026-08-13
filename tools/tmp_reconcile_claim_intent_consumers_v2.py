#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/tmp_reconcile_claim_intent_consumers.py"


def load_module():
    spec = importlib.util.spec_from_file_location("claim_intent_consumer_reconciliation", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    original = module.insert_test_class

    def safe_insert(path: str, marker: str, block: str) -> None:
        block = block.replace('required = "\n".join', "required = chr(10).join")
        block = block.replace('prompt + "\n" + required', "prompt + chr(10) + required")
        original(path, marker, block)

    module.insert_test_class = safe_insert
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
