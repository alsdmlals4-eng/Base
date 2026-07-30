#!/usr/bin/env python3
"""Migrate a legacy project adapter to the Base v9.1 canonical adapter contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_operating_contract import (
    ContractError,
    canonical_json,
    load_object,
    migrated_adapter,
    safe_repository_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument("--legacy-adapter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-commit", default="")
    parser.add_argument("--release-evidence-commit", default="")
    parser.add_argument("--protected-baseline-commit", default="")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    options = parser.parse_args()
    try:
        project_root = options.project_root.resolve()
        base_repository = options.base_repository.resolve()
        try:
            legacy_relative = options.legacy_adapter.resolve().relative_to(project_root)
            output_relative = options.output.resolve().relative_to(project_root)
        except ValueError as error:
            raise ContractError("Migration input/output must remain under the approved project root") from error
        legacy_path = safe_repository_path(project_root, legacy_relative, "legacy migration input")
        output = safe_repository_path(project_root, output_relative, "migration output")
        if legacy_path == output:
            raise ContractError("Legacy migration input and output cannot be the same path")
        data = migrated_adapter(
            project_root,
            base_repository,
            load_object(legacy_path),
            options.release_commit,
            options.release_evidence_commit,
            options.protected_baseline_commit,
        )
        content = canonical_json(data)
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
