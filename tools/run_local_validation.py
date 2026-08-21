#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path


SESSION_PREFIX = "local-validation-"
LOCAL_VALIDATION_REQUIRED_MODULES = (
    "jsonschema",
    "PIL",
    "markdown_it",
    "docx",
    "pypdf",
)


def missing_required_modules() -> tuple[str, ...]:
    return tuple(
        module
        for module in LOCAL_VALIDATION_REQUIRED_MODULES
        if importlib.util.find_spec(module) is None
    )


def default_commands(
    python: str,
    trusted_history_commit: str,
) -> tuple[tuple[str, ...], ...]:
    return (
        (python, "-m", "unittest", "discover", "-s", "tests", "-v"),
        (python, "tools/check_ci_required_gate_topology.py"),
        (python, "tools/build_base_v9_artifacts.py", "--check"),
        (
            python,
            "tools/check_base_v9_integrity.py",
            "--trusted-history-commit",
            trusted_history_commit,
        ),
        (python, "tools/check_skill_system_coverage.py"),
        ("git", "diff", "--check"),
        ("git", "fsck", "--strict"),
    )


def _remove_owned_session(
    repository_root: Path,
    session: Path,
    expected_identity: tuple[int, int],
) -> None:
    temporary_root = (repository_root / ".tmp").resolve()
    candidate = session.resolve()
    if candidate.parent != temporary_root or not candidate.name.startswith(
        SESSION_PREFIX
    ):
        raise ValueError(f"Refusing to remove a non-owned local validation session: {session}")
    if session.exists() or session.is_symlink():
        current = session.lstat()
        current_identity = (current.st_dev, current.st_ino)
        if current_identity != expected_identity:
            raise ValueError(
                f"Refusing to remove a replaced local validation session: {session}"
            )
        shutil.rmtree(candidate)
    try:
        temporary_root.rmdir()
    except OSError:
        pass


def run_validation(
    repository_root: Path,
    commands: Sequence[Sequence[str]],
    environment: Mapping[str, str] | None = None,
) -> int:
    root = repository_root.resolve()
    temporary_root = root / ".tmp"
    if temporary_root.is_symlink():
        raise ValueError(f"Local validation temporary root must not be a symlink: {temporary_root}")
    temporary_root.mkdir(exist_ok=True)
    session = Path(
        tempfile.mkdtemp(prefix=SESSION_PREFIX, dir=temporary_root)
    ).resolve()
    session_stat = session.lstat()
    session_identity = (session_stat.st_dev, session_stat.st_ino)
    child_environment = dict(os.environ if environment is None else environment)
    child_environment.update(
        {name: str(session) for name in ("TMPDIR", "TMP", "TEMP")}
    )
    status = 0
    try:
        for command in commands:
            values = tuple(str(value) for value in command)
            print("+", " ".join(values), flush=True)
            result = subprocess.run(
                values,
                cwd=root,
                env=child_environment,
                check=False,
            )
            if result.returncode:
                status = result.returncode
                break
    finally:
        try:
            _remove_owned_session(root, session, session_identity)
        except Exception as error:
            if not status:
                raise
            print(
                f"Local validation cleanup failed after child exit {status}: {error}",
                file=sys.stderr,
            )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trusted-history-commit", required=True)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    missing = missing_required_modules()
    if missing:
        print(
            "LOCAL_VALIDATION_DEPENDENCY_MISSING: " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "Install pinned dependencies with: "
            f"{sys.executable} -m pip install --requirement "
            ".github/validation-requirements.txt",
            file=sys.stderr,
        )
        return 2
    return run_validation(
        repository_root,
        default_commands(sys.executable, args.trusted_history_commit),
    )


if __name__ == "__main__":
    raise SystemExit(main())
