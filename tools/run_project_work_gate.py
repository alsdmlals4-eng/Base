#!/usr/bin/env python3
"""Run the Base-current PM gate against a target project without installing Base there.

This tool is read-only. It verifies the exact Base checkout, verifies that the
caller-supplied project revisions exist, reads a receipt from a file or stdin,
and delegates receipt semantics to the canonical Base validators.
"""
from __future__ import annotations

import os
import sys

# Do not let the target project, current directory, PYTHONPATH, or user site
# shadow stdlib/Base modules used by this trust-boundary entrypoint.
if not sys.flags.isolated:
    os.execv(
        sys.executable,
        [sys.executable, "-I", os.path.abspath(__file__), *sys.argv[1:]],
    )

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
REQUIRED_BASE_FILES = (
    "tools/run_project_work_gate.py",
    "tools/validate_work_contract_receipt.py",
    "tools/project_work_tracking.py",
)
SHA = re.compile(r"[0-9a-f]{40}\Z")
MAX_RECEIPT_BYTES = 2_000_000


class BootstrapError(RuntimeError):
    """Expected fail-closed bootstrap error."""


def _git(root: Path, *args: str, text: bool = True) -> subprocess.CompletedProcess[Any]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            text=text,
            capture_output=True,
            check=False,
            timeout=20,
            env={
                **os.environ,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_TERMINAL_PROMPT": "0",
            },
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BootstrapError(f"git command unavailable: {type(exc).__name__}") from exc


def _exact_sha(value: str | None, label: str) -> str:
    if not isinstance(value, str) or SHA.fullmatch(value) is None:
        raise BootstrapError(f"{label} must be an exact lowercase 40-character SHA")
    return value


def _repository_root(path: Path, label: str) -> Path:
    if not path.exists() or not path.is_dir() or path.is_symlink():
        raise BootstrapError(f"{label} is missing, not a directory, or a symlink")
    resolved = path.resolve()
    result = _git(resolved, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise BootstrapError(f"{label} is not a Git repository root")
    try:
        discovered = Path(result.stdout.strip()).resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise BootstrapError(f"{label} repository root is unreadable") from exc
    if discovered != resolved:
        raise BootstrapError(f"{label} must identify the exact Git repository root")
    return resolved


def _commit_exists(root: Path, sha: str, label: str) -> None:
    result = _git(root, "cat-file", "-e", f"{sha}^{{commit}}")
    if result.returncode != 0:
        raise BootstrapError(f"{label} commit is unavailable in the target repository: {sha}")


def _verify_base(expected_sha: str) -> None:
    base_root = _repository_root(ROOT, "Base checkout")
    head = _git(base_root, "rev-parse", "HEAD")
    if head.returncode != 0 or head.stdout.strip() != expected_sha:
        actual = head.stdout.strip() if head.returncode == 0 else "UNAVAILABLE"
        raise BootstrapError(
            f"Base checkout HEAD does not match trusted expected Base SHA: "
            f"{actual} != {expected_sha}"
        )

    tracked = _git(
        base_root,
        "ls-files",
        "--error-unmatch",
        "--",
        *REQUIRED_BASE_FILES,
    )
    if tracked.returncode != 0:
        raise BootstrapError("Base bootstrap executable files are not all tracked")

    for diff_args in (
        ("diff", "--quiet", "HEAD", "--", *REQUIRED_BASE_FILES),
        ("diff", "--cached", "--quiet", "HEAD", "--", *REQUIRED_BASE_FILES),
    ):
        if _git(base_root, *diff_args).returncode != 0:
            raise BootstrapError("Base bootstrap executable files differ from HEAD")

    for relative in REQUIRED_BASE_FILES:
        committed = _git(base_root, "show", f"{expected_sha}:{relative}", text=False)
        if committed.returncode != 0:
            raise BootstrapError(f"Base bootstrap executable is missing at expected SHA: {relative}")
        try:
            actual = (base_root / relative).read_bytes()
        except OSError as exc:
            raise BootstrapError(f"Base bootstrap executable is unreadable: {relative}") from exc
        if actual != committed.stdout:
            raise BootstrapError(
                f"Base bootstrap executable bytes differ from expected SHA: {relative}"
            )


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BootstrapError(f"cannot load verified Base module: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise BootstrapError(
            f"verified Base module failed to load: {path.name}: {type(exc).__name__}"
        ) from exc
    return module


def _load_validators() -> tuple[ModuleType, ModuleType]:
    tracking = _load_module("project_work_tracking", TOOLS / "project_work_tracking.py")
    validator = _load_module(
        "base_current_validate_work_contract_receipt",
        TOOLS / "validate_work_contract_receipt.py",
    )
    return tracking, validator


def _read_receipt(value: str) -> tuple[object, str]:
    if value == "-":
        source = "stdin"
        try:
            payload = sys.stdin.read(MAX_RECEIPT_BYTES + 1)
        except (OSError, UnicodeError) as exc:
            raise BootstrapError(f"cannot read receipt from stdin: {type(exc).__name__}") from exc
        if len(payload.encode("utf-8", errors="replace")) > MAX_RECEIPT_BYTES:
            raise BootstrapError("receipt exceeds the 2000000-byte safety limit")
    else:
        path = Path(value).expanduser()
        source = str(path.resolve(strict=False))
        try:
            if path.is_symlink():
                raise BootstrapError("receipt path must not be a symlink")
            size = path.stat().st_size
            if size > MAX_RECEIPT_BYTES:
                raise BootstrapError("receipt exceeds the 2000000-byte safety limit")
            payload = path.read_text(encoding="utf-8")
        except BootstrapError:
            raise
        except (OSError, UnicodeError) as exc:
            raise BootstrapError(f"cannot read receipt JSON: {type(exc).__name__}") from exc
    try:
        return json.loads(payload), source
    except json.JSONDecodeError as exc:
        raise BootstrapError(
            f"cannot parse receipt JSON at line {exc.lineno} column {exc.colno}"
        ) from exc


def _identity_lines(
    *,
    base_sha: str,
    project_root: Path,
    project_source_sha: str,
    verified_head_sha: str | None,
    receipt_source: str,
) -> list[str]:
    lines = [
        f"base_sha={base_sha}",
        f"project_root={project_root}",
        f"project_source_sha={project_source_sha}",
        f"receipt_source={receipt_source}",
    ]
    if verified_head_sha is not None:
        lines.append(f"project_verified_head_sha={verified_head_sha}")
    return lines


def _render_failed_board(
    *,
    receipt: object,
    validator: ModuleType,
    tracking: ModuleType,
    phase: str,
    project_source_sha: str,
    verified_head_sha: str | None,
) -> str | None:
    board = receipt.get("project_work_kanban") if isinstance(receipt, dict) else None
    if not isinstance(board, dict):
        return None
    shape_errors = tracking.validate_tracking(
        board,
        phase="inspect",
        expected_source_sha=project_source_sha,
    )
    if shape_errors:
        return None
    render_board, render_head = validator._render_inputs(
        board,
        phase=phase,
        expected_head_sha=verified_head_sha,
    )
    return "\n".join(
        (
            "PM VIEW: INFORMATION ONLY; EXECUTION BLOCKED",
            tracking.render_tracking(
                render_board,
                expected_head_sha=render_head,
                execution_authorized=False,
            ),
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expected-base-sha",
        required=True,
        help="Exact Base checkout SHA independently fresh-read by the caller",
    )
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument(
        "--project-source-sha",
        required=True,
        help="Exact target-project source SHA independently fresh-read by the caller",
    )
    parser.add_argument(
        "--verified-head-sha",
        help="Exact target-project verified subject HEAD; required only for closeout",
    )
    parser.add_argument("--receipt", required=True, help="UTF-8 JSON receipt path, or - for stdin")
    parser.add_argument(
        "--phase",
        choices=("start", "resume", "closeout"),
        default="start",
    )
    parser.add_argument("--render-markdown", action="store_true")
    args = parser.parse_args()

    receipt: object | None = None
    receipt_source = "UNREAD"
    project_root = args.project_root.resolve(strict=False)
    try:
        expected_base_sha = _exact_sha(args.expected_base_sha, "expected Base SHA")
        project_source_sha = _exact_sha(args.project_source_sha, "project source SHA")
        if args.phase == "closeout":
            verified_head_sha = _exact_sha(
                args.verified_head_sha,
                "verified project HEAD",
            )
        elif args.verified_head_sha is not None:
            raise BootstrapError("verified project HEAD is accepted only for closeout")
        else:
            verified_head_sha = None

        _verify_base(expected_base_sha)
        project_root = _repository_root(args.project_root, "target project")
        _commit_exists(project_root, project_source_sha, "project source")
        if verified_head_sha is not None:
            _commit_exists(project_root, verified_head_sha, "verified project HEAD")

        receipt, receipt_source = _read_receipt(args.receipt)
        tracking, validator = _load_validators()
        errors = validator.validate_execution_receipt(
            receipt,
            phase=args.phase,
            expected_source_sha=project_source_sha,
            expected_head_sha=verified_head_sha,
        )

        identity = _identity_lines(
            base_sha=expected_base_sha,
            project_root=project_root,
            project_source_sha=project_source_sha,
            verified_head_sha=verified_head_sha,
            receipt_source=receipt_source,
        )
        if errors:
            print("BASE CURRENT PROJECT WORK BOOTSTRAP: FAIL")
            for line in identity:
                print(line)
            for error in errors:
                print(f"- {error}")
            if args.render_markdown:
                rendered = _render_failed_board(
                    receipt=receipt,
                    validator=validator,
                    tracking=tracking,
                    phase=args.phase,
                    project_source_sha=project_source_sha,
                    verified_head_sha=verified_head_sha,
                )
                if rendered:
                    print(rendered)
            return 1

        print("BASE CURRENT PROJECT WORK BOOTSTRAP: PASS")
        for line in identity:
            print(line)
        print(
            f"WORK CONTRACT RECEIPT: PASS "
            f"(execution phase={args.phase}; recorded evidence only)"
        )
        if args.render_markdown and isinstance(receipt, dict):
            board = receipt.get("project_work_kanban")
            if isinstance(board, dict):
                render_board, render_head = validator._render_inputs(
                    board,
                    phase=args.phase,
                    expected_head_sha=verified_head_sha,
                )
                print(
                    tracking.render_tracking(
                        render_board,
                        expected_head_sha=render_head,
                    )
                )
        return 0
    except BootstrapError as exc:
        print("BASE CURRENT PROJECT WORK BOOTSTRAP: FAIL")
        print(f"project_root={project_root}")
        print(f"receipt_source={receipt_source}")
        print(f"- {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
