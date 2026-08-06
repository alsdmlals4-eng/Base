#!/usr/bin/env python3
"""Validate a project contract and narrowly reconcile an externally approved protected-path change."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

import project_operating_contract as contract
from base_release_index import install_release_lock_paths


install_release_lock_paths(contract)

ROOT = Path(__file__).resolve().parents[1]
APPROVAL_SCHEMA = ROOT / "schemas/project-protected-change-approval-v1.schema.json"
PROTECTED_PREFIX = "Protected-path changes detected: "


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def _schema_errors(document: dict[str, Any]) -> list[str]:
    schema = json.loads(APPROVAL_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document),
        key=lambda item: list(item.path),
    )
    return [
        "Protected change approval "
        + (".".join(str(part) for part in error.path) or "<root>")
        + f": {error.message}"
        for error in errors
    ]


def validate_approval_document(
    document: dict[str, Any],
    *,
    protected_base: str,
    changed_paths: list[str],
    externally_approved: bool,
) -> list[str]:
    errors = _schema_errors(document)
    if errors:
        return errors
    if not externally_approved:
        errors.append("Protected change approval requires external GitHub approval metadata")
    if document["protected_base_commit"] != protected_base:
        errors.append(
            "Protected change approval baseline mismatch: "
            f"{document['protected_base_commit']} != {protected_base}"
        )
    decisions = document["decision_ids"]
    if not decisions or any(not str(value).strip() for value in decisions):
        errors.append("Protected change approval requires at least one Decision ID")
    approved = sorted(_normalize_path(value) for value in document["approved_paths"])
    changed = sorted(_normalize_path(value) for value in changed_paths)
    if approved != changed:
        errors.append(
            "Protected change approval must exactly equal the detected protected paths: "
            f"approved={approved}, detected={changed}"
        )
    return errors


def _protected_error_paths(error: str) -> list[str] | None:
    if not error.startswith(PROTECTED_PREFIX):
        return None
    values = [item.strip() for item in error.removeprefix(PROTECTED_PREFIX).split(",")]
    if not values or any(not value for value in values):
        return None
    return sorted(_normalize_path(value) for value in values)


def reconcile_contract_errors(
    contract_errors: list[str],
    *,
    approved_paths: list[str],
) -> list[str]:
    expected = sorted(_normalize_path(value) for value in approved_paths)
    remaining: list[str] = []
    reconciled = 0
    for error in contract_errors:
        paths = _protected_error_paths(error)
        if paths is not None and paths == expected and reconciled == 0:
            reconciled += 1
            continue
        remaining.append(error)
    if reconciled != 1:
        return list(contract_errors)
    return remaining


def _generated_artifact_errors(project_root: Path, base_repository: Path) -> list[str]:
    try:
        artifacts = contract.build_artifacts(project_root, base_repository, prevalidated=True)
    except contract.ContractError as error:
        return [str(error)]
    mismatches = [
        path
        for path, content in artifacts.items()
        if not path.is_file() or path.read_bytes() != content
    ]
    if not mismatches:
        return []
    names = ", ".join(path.relative_to(project_root).as_posix() for path in mismatches)
    return [f"Generated view manual modification or stale output detected: {names}"]


def validate_project_contract(
    *,
    project_root: Path,
    base_repository: Path,
    protected_base: str,
    approval_document: dict[str, Any] | None,
    externally_approved: bool,
    check_generated: bool,
) -> list[str]:
    errors = contract.validation_errors(
        project_root,
        base_repository,
        protected_base=protected_base,
        check_generated=False,
    )
    if approval_document is not None:
        protected_errors = [error for error in errors if _protected_error_paths(error) is not None]
        if len(protected_errors) != 1:
            errors.append(
                "Protected change approval requires exactly one detected protected-path error"
            )
        else:
            changed_paths = _protected_error_paths(protected_errors[0]) or []
            approval_errors = validate_approval_document(
                approval_document,
                protected_base=protected_base,
                changed_paths=changed_paths,
                externally_approved=externally_approved,
            )
            if approval_errors:
                errors.extend(approval_errors)
            else:
                errors = reconcile_contract_errors(
                    errors,
                    approved_paths=approval_document["approved_paths"],
                )
    elif externally_approved:
        errors.append("External approval metadata cannot be used without an approval manifest")

    if not errors and check_generated:
        errors.extend(_generated_artifact_errors(project_root, base_repository))
    return errors


def _load_approval(project_root: Path, value: str) -> dict[str, Any]:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe protected change approval path: {value}")
    root = project_root.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Unsafe protected change approval path: {value}")
    if not target.is_file():
        raise ValueError(f"Protected change approval file does not exist: {value}")
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Protected change approval root must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--base-repository", type=Path, required=True)
    parser.add_argument("--protected-base", required=True)
    parser.add_argument("--approval", default="")
    parser.add_argument("--external-approval", choices=("true", "false"), default="false")
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()

    if not re.fullmatch(r"[0-9a-f]{40}", options.protected_base):
        print("Approved project operating contract validation failed:", file=sys.stderr)
        print("- --protected-base must be an exact 40-character SHA", file=sys.stderr)
        return 1

    project_root = options.project_root.resolve()
    base_repository = options.base_repository.resolve()
    approval_document: dict[str, Any] | None = None
    load_errors: list[str] = []
    if options.approval:
        try:
            approval_document = _load_approval(project_root, options.approval)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            load_errors.append(str(error))

    errors = load_errors or validate_project_contract(
        project_root=project_root,
        base_repository=base_repository,
        protected_base=options.protected_base,
        approval_document=approval_document,
        externally_approved=options.external_approval == "true",
        check_generated=options.check,
    )

    if errors:
        print("Approved project operating contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Approved project operating contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
