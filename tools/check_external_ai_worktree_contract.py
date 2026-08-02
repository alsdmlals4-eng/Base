#!/usr/bin/env python3
"""Validate an external-AI worktree contract against actual Git state."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path("schemas/external-ai-worktree-contract-v1.schema.json")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(
    root: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def normalize_relative(value: str, field: str, errors: list[str]) -> str | None:
    path = Path(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{field} must be a repository-relative path: {value}")
        return None
    normalized = path.as_posix()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized or normalized == ".":
        errors.append(f"{field} must not be empty")
        return None
    return normalized


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def git_paths(
    worktree: Path,
    start_commit: str,
) -> tuple[set[str], set[str], list[str]]:
    errors: list[str] = []
    committed: set[str] = set()
    dirty: set[str] = set()
    commands = [
        ("committed", ["diff", "--name-only", f"{start_commit}...HEAD"]),
        ("unstaged", ["diff", "--name-only"]),
        ("staged", ["diff", "--cached", "--name-only"]),
        ("untracked", ["ls-files", "--others", "--exclude-standard"]),
    ]
    for label, arguments in commands:
        try:
            result = run_git(worktree, *arguments)
        except (OSError, subprocess.CalledProcessError) as error:
            errors.append(f"unable to inspect {label} paths: {error}")
            continue
        values = {
            line.strip().replace("\\", "/")
            for line in result.stdout.splitlines()
            if line.strip()
        }
        if label == "committed":
            committed |= values
        else:
            dirty |= values
    return committed, dirty, errors


def validate_contract(root: Path, contract_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        contract = load_json(contract_path)
        schema = load_json(root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as error:
        return [f"contract or schema unavailable: {error}"]

    for error in sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: list(item.path),
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema {location}: {error.message}")
    if errors:
        return errors

    worktree_rel = normalize_relative(
        contract["worktree_path"],
        "worktree_path",
        errors,
    )
    read_patterns: list[str] = []
    write_patterns: list[str] = []
    protected_patterns: list[str] = []
    for field, values, target in (
        ("allowlist.read", contract["allowlist"]["read"], read_patterns),
        ("allowlist.write", contract["allowlist"]["write"], write_patterns),
        ("protected_paths", contract["protected_paths"], protected_patterns),
    ):
        for value in values:
            normalized = normalize_relative(value, field, errors)
            if normalized is not None:
                target.append(normalized)
    if errors:
        return errors

    assert worktree_rel is not None
    if not worktree_rel.startswith(".worktrees/"):
        errors.append("worktree_path must be under .worktrees/")
    if contract["task_branch"] == contract["base_branch"]:
        errors.append("task_branch must differ from base_branch")
    if not contract["task_branch"].startswith("ai/deepseek-"):
        errors.append("task_branch must use the ai/deepseek- prefix")
    if contract["result_state"] != "REVIEW_PENDING":
        errors.append("external AI result_state must remain REVIEW_PENDING")

    try:
        ignored = run_git(root, "check-ignore", "-q", ".worktrees/", check=False)
        if ignored.returncode != 0:
            errors.append(".worktrees/ is not ignored by git")
        repository_root = Path(
            run_git(root, "rev-parse", "--show-toplevel").stdout.strip()
        ).resolve()
        if repository_root != root.resolve():
            errors.append("root is not the repository top-level")
    except (OSError, subprocess.CalledProcessError) as error:
        return [*errors, f"repository state unavailable: {error}"]

    worktree = (root / worktree_rel).resolve()
    if not worktree.is_dir():
        return [*errors, f"worktree does not exist: {worktree_rel}"]
    try:
        actual_top = Path(
            run_git(worktree, "rev-parse", "--show-toplevel").stdout.strip()
        ).resolve()
        actual_branch = run_git(worktree, "branch", "--show-current").stdout.strip()
        run_git(worktree, "cat-file", "-e", f"{contract['start_commit']}^{{commit}}")
        ancestor = run_git(
            worktree,
            "merge-base",
            "--is-ancestor",
            contract["start_commit"],
            "HEAD",
            check=False,
        )
        if ancestor.returncode != 0:
            errors.append("start_commit is not an ancestor of worktree HEAD")
    except (OSError, subprocess.CalledProcessError) as error:
        return [*errors, f"worktree git state unavailable: {error}"]

    if actual_top != worktree:
        errors.append("worktree_path does not resolve to the worktree top-level")
    if actual_branch != contract["task_branch"]:
        errors.append(
            f"actual worktree branch {actual_branch!r} does not match "
            f"task_branch {contract['task_branch']!r}"
        )

    committed, dirty, path_errors = git_paths(worktree, contract["start_commit"])
    errors.extend(path_errors)
    for path in sorted(committed | dirty):
        if matches(path, protected_patterns):
            errors.append(f"protected path changed: {path}")
        if not matches(path, write_patterns):
            errors.append(f"changed path is outside write allowlist: {path}")

    if contract["cleanup_requested"]:
        if contract["integration_state"] != "APPROVED_INTEGRATED":
            errors.append("cleanup requires integration_state APPROVED_INTEGRATED")
        if dirty:
            errors.append(
                f"cleanup is blocked by dirty or untracked paths: {sorted(dirty)}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--contract", type=Path, required=True)
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    contract_path = arguments.contract
    if not contract_path.is_absolute():
        contract_path = root / contract_path
    errors = validate_contract(root, contract_path)
    if errors:
        print("EXTERNAL_AI_WORKTREE_STATUS: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EXTERNAL_AI_WORKTREE_STATUS: PASS")
    print("RESULT_STATE: REVIEW_PENDING")
    return 0


if __name__ == "__main__":
    sys.exit(main())
