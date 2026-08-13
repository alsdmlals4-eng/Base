#!/usr/bin/env python3
"""Explicit, non-overwriting PROJECT_BASE_ADAPTER v1 to v2 migration."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import project_operating_contract as contract


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--input", default="skills/PROJECT_BASE_ADAPTER.json")
    parser.add_argument("--output", default="skills/MIGRATED_PROJECT_BASE_ADAPTER_V2.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    source = contract.safe_repository_path(root, args.input, "v1 adapter input")
    target = contract.safe_repository_path(root, args.output, "v2 adapter output")
    if source == target:
        parser.error("v2 migration output must not overwrite the v1 source")
    migrated = contract.migrate_adapter_v1_to_v2(contract.load_object(source), project_id=args.project_id)
    content = contract.canonical_json(migrated)
    if args.check:
        if not target.is_file() or target.read_bytes() != content:
            parser.error("v2 migration output is missing or stale")
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    parent = contract.safe_repository_path(root, target.parent.relative_to(root), "v2 adapter output parent")
    parent_descriptor = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        try:
            descriptor = os.open(
                target.name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                0o600,
                dir_fd=parent_descriptor,
            )
        except FileExistsError:
            parser.error("v2 migration output already exists; use a new path or --check")
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
    finally:
        os.close(parent_descriptor)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
