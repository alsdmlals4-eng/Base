#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.loop_contracts.bundle_validation import validate_bundle, validate_completion


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capsule", type=Path)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument(
        "--phase",
        choices=("readiness", "completion"),
        default="readiness",
        help="readiness preserves the existing start gate; completion adds closure/evidence/readback gates",
    )
    args = parser.parse_args()
    findings = (
        validate_bundle(args.capsule)
        if args.phase == "readiness"
        else validate_completion(args.capsule)
    )
    if args.format == "json":
        print(json.dumps([item.to_dict() for item in findings], ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.code}: {item.path}: {item.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
