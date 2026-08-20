#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.project_integration_capsule import Finding, validate_capsule


def _utf8_safe_text(value: str) -> str:
    utf8_safe = value.encode("utf-8", errors="backslashreplace").decode("utf-8")
    return "".join(
        f"\\x{ord(character):02x}"
        if ord(character) < 32 or ord(character) == 127
        else character
        for character in utf8_safe
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a read-only Project Integration Capsule against its exact local worktree."
    )
    parser.add_argument("capsule", type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args()

    try:
        findings = validate_capsule(
            args.capsule,
            project_root=args.project_root,
            schema_only=args.schema_only,
        )
    except Exception as error:  # Fail closed as machine-readable output at the CLI boundary.
        findings = [
            Finding(
                "VALIDATOR_INTERNAL_ERROR",
                "/",
                f"{type(error).__name__}: {error}",
            )
        ]
    if args.format == "json":
        print(
            json.dumps(
                [finding.to_dict() for finding in findings],
                ensure_ascii=True,
                indent=2,
            )
        )
    else:
        for finding in findings:
            print(
                _utf8_safe_text(
                    f"{finding.code}: {finding.path}: {finding.message}"
                )
            )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
