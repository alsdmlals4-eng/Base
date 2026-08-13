#!/usr/bin/env python3
"""Check a review record against repository facts."""

from __future__ import annotations

import fnmatch
import json
import subprocess
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def normalize_path(value: str, field: str, errors: list[str], *, allow_dot: bool = False) -> str | None:
    normalized = value.replace("\\", "/")
    path = Path(normalized)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{field} must stay repository-relative: {value}")
        return None
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized:
        if allow_dot:
            return "."
        errors.append(f"{field} must not be empty")
        return None
    if normalized == "." and not allow_dot:
        errors.append(f"{field} must identify a repository path")
        return None
    return normalized


def escape_brackets(pattern: str) -> str:
    return pattern.replace("[", "[[]").replace("]", "[]]")


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, escape_brackets(pattern)) for pattern in patterns)


def repository_state(root: Path, base_ref: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    subject: dict[str, Any] = {
        "base_ref": base_ref,
        "base_sha": None,
        "head_sha": None,
        "changed_files": [],
    }
    try:
        top = Path(run_git(root, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
        if top != root.resolve():
            errors.append("root is not the repository top-level")
        base_sha = run_git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}").stdout.strip()
        head_sha = run_git(root, "rev-parse", "HEAD").stdout.strip()
        subject["base_sha"] = base_sha
        subject["head_sha"] = head_sha
        ancestor = run_git(root, "merge-base", "--is-ancestor", base_sha, head_sha, check=False)
        if ancestor.returncode != 0:
            errors.append("trusted base is not an ancestor of current HEAD")
        dirty = run_git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
        if dirty:
            errors.append("worktree must be clean before review record checking")
        changed = sorted({line.strip().replace("\\", "/") for line in run_git(
            root,
            "diff",
            "--name-only",
            "--diff-filter=ACDMRTUXB",
            f"{base_sha}...{head_sha}",
        ).stdout.splitlines() if line.strip()})
        subject["changed_files"] = changed
        if not changed:
            errors.append("no changed files exist between trusted base and current HEAD")
    except (OSError, subprocess.CalledProcessError) as error:
        errors.append(f"repository state unavailable: {error}")
    return subject, errors


def check_record(root: Path, record_path: Path, base_ref: str) -> tuple[dict[str, Any], list[str]]:
    root = root.resolve()
    if not record_path.is_absolute():
        record_path = root / record_path
    try:
        record = read_json(record_path)
    except (OSError, json.JSONDecodeError) as error:
        message = f"record unavailable: {error}"
        return {"state": "FAIL", "errors": [message]}, [message]
    subject, errors = repository_state(root, base_ref)
    return {"state": "PENDING" if not errors else "FAIL", "record": record, "subject": subject, "errors": errors}, errors
