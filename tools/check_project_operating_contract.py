#!/usr/bin/env python3
"""Validate a Base project contract against project and Base repositories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import project_operating_contract as contract
from base_release_index import install_release_lock_paths


install_release_lock_paths(contract)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument(
        "--protected-base",
        default="",
        help="trusted external baseline commit; it must exactly equal the adapter record",
    )
    parser.add_argument("--check", action="store_true", help="require generated views to be current")
    parser.add_argument("--hub-identity-check", action="store_true")
    parser.add_argument("--expected-project-id", default="")
    parser.add_argument("--expected-adapter-sha256", default="")
    options = parser.parse_args()
    if options.hub_identity_check:
        if not options.expected_project_id or not options.expected_adapter_sha256:
            parser.error("Hub identity check requires exact project ID and adapter SHA-256")
        errors = contract.hub_identity_errors(
            options.project_root,
            options.base_repository,
            expected_project_id=options.expected_project_id,
            expected_adapter_sha256=options.expected_adapter_sha256,
        )
    else:
        errors = contract.validation_errors(
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
