#!/usr/bin/env python3
"""Migrate a legacy project adapter to the canonical Base project contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import project_operating_contract as contract
from base_release_index import install_release_lock_paths


install_release_lock_paths(contract)

LEGACY_ARCHIVE_ROOT = Path("docs/archive/base-v9-legacy-inputs")


def preserved_compatibility_inputs(project_root: Path, *, write: bool) -> dict[str, str]:
    """Archive legacy adapters once before their public paths become generated views."""
    inputs: dict[str, str] = {}
    for view in contract.COMPATIBILITY_VIEWS:
        source = contract.safe_repository_path(project_root, view, "legacy compatibility view")
        if not source.is_file():
            continue
        current = contract.load_object(source)
        if current.get("artifact_role") == "GENERATED_COMPATIBILITY_VIEW":
            archive = contract.safe_repository_path(
                project_root, LEGACY_ARCHIVE_ROOT / view.name, "legacy compatibility archive"
            )
            if not archive.is_file():
                raise contract.ContractError(
                    f"Generated compatibility view has no preserved legacy input: {view.as_posix()}"
                )
            inputs[view.as_posix()] = archive.relative_to(project_root).as_posix()
            continue
        archive = contract.safe_repository_path(
            project_root, LEGACY_ARCHIVE_ROOT / view.name, "legacy compatibility archive"
        )
        raw = source.read_bytes()
        if archive.exists():
            if not archive.is_file() or archive.read_bytes() != raw:
                raise contract.ContractError(
                    f"Legacy compatibility archive mismatch: {archive.relative_to(project_root)}"
                )
        elif write:
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(raw)
        else:
            raise contract.ContractError(
                f"Legacy compatibility archive is missing: {archive.relative_to(project_root)}"
            )
        inputs[view.as_posix()] = archive.relative_to(project_root).as_posix()
    return inputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument("--legacy-adapter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-commit", default="")
    parser.add_argument("--release-evidence-commit", default="")
    parser.add_argument(
        "--base-version",
        default="",
        help="Optional exact Base version. Defaults to the newest locally available lock with usable release and evidence pins.",
    )
    parser.add_argument("--protected-baseline-commit", default="")
    parser.add_argument("--protected-authority-kind", default="")
    parser.add_argument("--protected-authority-ref", default="")
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
            raise contract.ContractError(
                "Migration input/output must remain under the approved project root"
            ) from error
        legacy_path = contract.safe_repository_path(
            project_root, legacy_relative, "legacy migration input"
        )
        output = contract.safe_repository_path(project_root, output_relative, "migration output")
        if legacy_path == output:
            raise contract.ContractError("Legacy migration input and output cannot be the same path")
        data = contract.migrated_adapter(
            project_root,
            base_repository,
            contract.load_object(legacy_path),
            legacy_relative.as_posix(),
            options.release_commit,
            options.release_evidence_commit,
            options.protected_baseline_commit,
            options.protected_authority_kind,
            options.protected_authority_ref,
            options.base_version,
        )
        compatibility_inputs = preserved_compatibility_inputs(
            project_root, write=options.write
        )
        data["compatibility"] = {
            "cycle": "ONE_CYCLE",
            "views": sorted(compatibility_inputs),
            "legacy_inputs": compatibility_inputs,
        }
        content = contract.canonical_json(data)
        if options.check:
            if not output.is_file() or output.read_bytes() != content:
                raise contract.ContractError(f"Migrated adapter is stale: {output}")
            health = contract.safe_repository_path(
                project_root,
                Path("docs/PROJECT_OPERATING_HEALTH.json"),
                "initial operating health",
            )
            if not health.is_file():
                raise contract.ContractError("First migration operating health artifact is missing")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
            health = contract.safe_repository_path(
                project_root,
                Path("docs/PROJECT_OPERATING_HEALTH.json"),
                "initial operating health",
            )
            if not health.exists():
                health.parent.mkdir(parents=True, exist_ok=True)
                health.write_bytes(contract.canonical_json(contract.initial_operating_health()))
    except contract.ContractError as error:
        print(f"Project adapter migration failed: {error}", file=sys.stderr)
        return 1
    print("Project adapter migration is current" if options.check else "Project adapter migrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
