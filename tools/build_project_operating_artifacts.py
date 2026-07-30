#!/usr/bin/env python3
"""Generate or check Base v9.1 project operating views."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_operating_contract import ContractError, write_or_check_artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument(
        "--protected-base",
        default="",
        help="trusted external baseline commit; it must exactly equal the adapter record",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    options = parser.parse_args()
    try:
        mismatches = write_or_check_artifacts(
            options.project_root.resolve(),
            options.base_repository.resolve(),
            check=options.check,
            protected_base=options.protected_base,
        )
    except ContractError as error:
        print(f"Project operating artifact generation failed: {error}", file=sys.stderr)
        return 1
    if options.check:
        print("Project operating generated artifacts are current")
    else:
        print(f"Project operating generated artifacts written: {len(mismatches)} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
