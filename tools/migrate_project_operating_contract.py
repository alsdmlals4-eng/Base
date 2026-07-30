#!/usr/bin/env python3
"""Migrate a legacy project adapter to the Base v9.1 canonical adapter contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_operating_contract import ContractError, canonical_json, load_object, migrated_adapter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument("--legacy-adapter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    options = parser.parse_args()
    try:
        data = migrated_adapter(
            options.project_root.resolve(),
            options.base_repository.resolve(),
            load_object(options.legacy_adapter.resolve()),
        )
        content = canonical_json(data)
        output = options.output.resolve()
        if options.check:
            if not output.is_file() or output.read_bytes() != content:
                raise ContractError(f"Migrated adapter is stale: {output}")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
    except ContractError as error:
        print(f"Project adapter migration failed: {error}", file=sys.stderr)
        return 1
    print("Project adapter migration is current" if options.check else "Project adapter migrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
