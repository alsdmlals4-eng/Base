#!/usr/bin/env python3
"""Validate a Base v9.1 project contract against project and Base repositories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_operating_contract import validation_errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument("--protected-base", default="")
    parser.add_argument("--check", action="store_true", help="require generated views to be current")
    options = parser.parse_args()
    errors = validation_errors(
        options.project_root.resolve(),
        options.base_repository.resolve(),
        protected_base=options.protected_base,
        check_generated=options.check,
    )
    if errors:
        print("Project operating contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Project operating contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
