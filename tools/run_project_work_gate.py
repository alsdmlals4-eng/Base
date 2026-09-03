#!/usr/bin/env python3
"""Run the Base-current PM gate against a target project without installing Base there.

Supported execution is from the exact entrypoint bytes of a caller-selected Base
commit, streamed to isolated Python. The tool is read-only: it verifies a bounded
Base operational closure, validates local commit identities in the target Git
repository, reads one bounded regular-file receipt, and delegates semantics to
the verified Base validator bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from types import ModuleType
from typing import Any, Mapping, Sequence


SHA = re.compile(r"[0-9a-f]{40}\Z")
MAX_RECEIPT_BYTES = 2_000_000
_READ_CHUNK_BYTES = 64 * 1024
TRUSTED_ENTRYPOINT_SOURCE = "commit-stream"
REQUIRED_BASE_CLOSURE = (
    "AGENTS.md",
    "START_HERE.md",
    "docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md",
    "skills/managing-project-intake-and-work-contract/SKILL.md",
    "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
    "templates/project-operations/PROJECT_START_HERE.md",
    "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
    "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
    "tools/run_project_work_gate.py",
    "tools/validate_work_contract_receipt.py",
    "tools/project_work_tracking.py",
)
VERIFIED_MODULE_PATHS = {
    "project_work_tracking": "tools/project_work_tracking.py",
    "base_current_validate_work_contract_receipt": (
        "tools/validate_work_contract_receipt.py"
    ),
}


class BootstrapError(RuntimeError):
    """Expected fail-closed bootstrap error."""


def _exact_sha(value: str | None, label: str) -> str:
    if not isinstance(value, str) or SHA.fullmatch(value) is None:
        raise BootstrapError(
            f"{label} must be an exact lowercase 40-character SHA"
        )
    return value


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _directory_candidate(path: Path, label: str) -> Path:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise BootstrapError(
            f"{label} is missing or unreadable: {type(exc).__name__}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise BootstrapError(f"{label} must be a nonsymlink directory")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise BootstrapError(
            f"{label} cannot be resolved: {type(exc).__name__}"
        ) from exc


def _trusted_git_executable(
    value: Path,
    *,
    base_candidate: Path,
    project_candidate: Path,
) -> Path:
    if not value.is_absolute():
        raise BootstrapError("git executable must be an absolute path")
    try:
        metadata = value.lstat()
    except OSError as exc:
        raise BootstrapError(
            f"git executable is unavailable: {type(exc).__name__}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise BootstrapError(
            "git executable must be a nonsymlink regular file"
        )
    try:
        resolved = value.resolve(strict=True)
    except OSError as exc:
        raise BootstrapError(
            f"git executable cannot be resolved: {type(exc).__name__}"
        ) from exc
    for root in (base_candidate, project_candidate):
        if resolved == root or _is_within(resolved, root):
            raise BootstrapError(
                "git executable must be outside the Base and target project repositories"
            )
    return resolved


def _git_environment() -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
        and key.upper() not in {"PYTHONPATH", "PYTHONHOME"}
    }
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_PROTOCOL_FROM_USER": "0",
            "GIT_PAGER": "cat",
        }
    )
    return environment


def _git(
    executable: Path,
    root: Path,
    *args: str,
    text: bool = True,
    timeout: int = 20,
) -> subprocess.CompletedProcess[Any]:
    command = [
        str(executable),
        "--no-replace-objects",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-c",
        "maintenance.auto=false",
        "-c",
        "gc.auto=0",
        "-c",
        "fetch.writeCommitGraph=false",
        "-c",
        "protocol.file.allow=never",
        "-C",
        str(root),
        *args,
    ]
    try:
        return subprocess.run(
            command,
            text=text,
            capture_output=True,
            check=False,
            timeout=timeout,
            env=_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BootstrapError(
            f"trusted git command unavailable: {type(exc).__name__}"
        ) from exc


def _repository_root(
    path: Path,
    label: str,
    executable: Path,
) -> Path:
    candidate = _directory_candidate(path, label)
    result = _git(executable, candidate, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise BootstrapError(f"{label} is not a Git repository root")
    try:
        discovered = Path(result.stdout.strip()).resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        raise BootstrapError(f"{label} repository root is unreadable") from exc
    if discovered != candidate:
        raise BootstrapError(
            f"{label} must identify the exact Git repository root"
        )
    return candidate


def _require_local_commit(
    executable: Path,
    root: Path,
    sha: str,
    label: str,
) -> None:
    result = _git(executable, root, "cat-file", "-t", sha)
    if result.returncode != 0:
        raise BootstrapError(
            f"{label} commit is unavailable locally in the target repository: {sha}"
        )
    if result.stdout.strip() != "commit":
        raise BootstrapError(
            f"{label} object type must be commit, not {result.stdout.strip() or 'UNKNOWN'}"
        )


def _read_commit_bytes(
    executable: Path,
    root: Path,
    sha: str,
    relative: str,
) -> bytes:
    result = _git(
        executable,
        root,
        "cat-file",
        "blob",
        f"{sha}:{relative}",
        text=False,
    )
    if result.returncode != 0:
        raise BootstrapError(
            f"Base operational authority file is unavailable locally at expected SHA: {relative}"
        )
    return bytes(result.stdout)


def _verify_base_closure(
    executable: Path,
    base_root: Path,
    expected_sha: str,
    entrypoint_sha256: str,
) -> dict[str, bytes]:
    _require_local_commit(
        executable, base_root, expected_sha, "expected Base"
    )
    head = _git(executable, base_root, "rev-parse", "--verify", "HEAD")
    if head.returncode != 0 or head.stdout.strip() != expected_sha:
        actual = head.stdout.strip() if head.returncode == 0 else "UNAVAILABLE"
        raise BootstrapError(
            "Base checkout HEAD does not match trusted expected Base SHA: "
            f"{actual} != {expected_sha}"
        )

    committed: dict[str, bytes] = {}
    for relative in REQUIRED_BASE_CLOSURE:
        expected = _read_commit_bytes(
            executable, base_root, expected_sha, relative
        )
        committed[relative] = expected
        local = base_root / relative
        try:
            metadata = local.lstat()
        except OSError as exc:
            raise BootstrapError(
                f"Base operational authority file is unreadable: {relative}"
            ) from exc
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(
            metadata.st_mode
        ):
            raise BootstrapError(
                f"Base operational authority file must be a nonsymlink regular file: {relative}"
            )
        try:
            actual = local.read_bytes()
        except OSError as exc:
            raise BootstrapError(
                f"Base operational authority file is unreadable: {relative}"
            ) from exc
        if actual != expected:
            raise BootstrapError(
                f"Base operational authority bytes differ from expected SHA: {relative}"
            )

    committed_entrypoint = committed["tools/run_project_work_gate.py"]
    expected_entrypoint_hash = hashlib.sha256(
        committed_entrypoint
    ).hexdigest()
    if entrypoint_sha256 != expected_entrypoint_hash:
        raise BootstrapError(
            "trusted entrypoint hash does not match the expected Base commit"
        )
    return committed


def _load_module_from_bytes(
    name: str,
    raw: bytes,
    origin: str,
) -> ModuleType:
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BootstrapError(
            f"verified Base module is not UTF-8: {origin}"
        ) from exc
    try:
        code = compile(source, origin, "exec", dont_inherit=True)
    except (SyntaxError, ValueError) as exc:
        raise BootstrapError(
            f"verified Base module failed to compile: {origin}: {type(exc).__name__}"
        ) from exc
    module = ModuleType(name)
    module.__file__ = origin
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(code, module.__dict__)
    except Exception as exc:
        raise BootstrapError(
            f"verified Base module failed to load: {origin}: {type(exc).__name__}"
        ) from exc
    return module


def _load_validators(
    committed: Mapping[str, bytes],
    expected_sha: str,
) -> tuple[ModuleType, ModuleType]:
    tracking_path = VERIFIED_MODULE_PATHS["project_work_tracking"]
    validator_path = VERIFIED_MODULE_PATHS[
        "base_current_validate_work_contract_receipt"
    ]
    tracking = _load_module_from_bytes(
        "project_work_tracking",
        committed[tracking_path],
        f"{expected_sha}:{tracking_path}",
    )
    validator = _load_module_from_bytes(
        "base_current_validate_work_contract_receipt",
        committed[validator_path],
        f"{expected_sha}:{validator_path}",
    )
    return tracking, validator


def _decode_receipt(raw: bytes) -> str:
    if len(raw) > MAX_RECEIPT_BYTES:
        raise BootstrapError(
            "receipt exceeds the 2000000-byte safety limit"
        )
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BootstrapError(
            "cannot read receipt JSON: UnicodeDecodeError"
        ) from exc


def _read_regular_receipt(path: Path) -> tuple[str, str]:
    if str(path) == "-":
        raise BootstrapError(
            "stdin receipt mode is not supported; use a bounded regular file"
        )
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise BootstrapError(
            f"cannot read receipt JSON: {type(exc).__name__}"
        ) from exc

    if stat.S_ISLNK(metadata.st_mode):
        raise BootstrapError("receipt path must not be a symlink")
    if not stat.S_ISREG(metadata.st_mode):
        raise BootstrapError("receipt path must be a regular file")
    if metadata.st_size > MAX_RECEIPT_BYTES:
        raise BootstrapError(
            "receipt exceeds the 2000000-byte safety limit"
        )

    flags = os.O_RDONLY
    for name in ("O_BINARY", "O_CLOEXEC", "O_NOFOLLOW", "O_NONBLOCK"):
        flags |= getattr(os, name, 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise BootstrapError(
            f"cannot read receipt JSON: {type(exc).__name__}"
        ) from exc

    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise BootstrapError("receipt path must be a regular file")
        if (
            metadata.st_dev != opened.st_dev
            or metadata.st_ino != opened.st_ino
        ):
            raise BootstrapError(
                "receipt path changed while it was being opened"
            )
        if opened.st_size > MAX_RECEIPT_BYTES:
            raise BootstrapError(
                "receipt exceeds the 2000000-byte safety limit"
            )

        chunks: list[bytes] = []
        remaining = MAX_RECEIPT_BYTES + 1
        while remaining > 0:
            chunk = os.read(
                descriptor, min(_READ_CHUNK_BYTES, remaining)
            )
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
    except BootstrapError:
        raise
    except OSError as exc:
        raise BootstrapError(
            f"cannot read receipt JSON: {type(exc).__name__}"
        ) from exc
    finally:
        os.close(descriptor)

    try:
        resolved = str(path.resolve(strict=True))
    except OSError as exc:
        raise BootstrapError(
            f"cannot resolve receipt JSON: {type(exc).__name__}"
        ) from exc
    return _decode_receipt(raw), resolved


def _reject_json_constant(value: str) -> None:
    raise BootstrapError(
        f"receipt JSON contains unsupported constant: {value}"
    )


def _reject_duplicate_json_keys(
    pairs: Sequence[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise BootstrapError(
                f"receipt JSON contains duplicate key: {key}"
            )
        result[key] = value
    return result


def _read_receipt(value: str) -> tuple[object, str]:
    payload, source = _read_regular_receipt(Path(value).expanduser())
    try:
        return (
            json.loads(
                payload,
                parse_constant=_reject_json_constant,
                object_pairs_hook=_reject_duplicate_json_keys,
            ),
            source,
        )
    except BootstrapError:
        raise
    except json.JSONDecodeError as exc:
        raise BootstrapError(
            f"cannot parse receipt JSON at line {exc.lineno} column {exc.colno}"
        ) from exc


def _json_line_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def _identity_lines(
    *,
    base_sha: str,
    project_root: Path,
    project_source_sha: str,
    verified_head_sha: str | None,
    receipt_source: str,
) -> list[str]:
    values: list[tuple[str, object]] = [
        ("base_sha", base_sha),
        ("project_root", str(project_root)),
        ("project_source_sha", project_source_sha),
        ("receipt_source", receipt_source),
    ]
    if verified_head_sha is not None:
        values.append(
            ("project_verified_head_sha", verified_head_sha)
        )
    return [
        f"{key}={_json_line_value(value)}"
        for key, value in values
    ]


def _render_failed_board(
    *,
    receipt: object,
    validator: ModuleType,
    tracking: ModuleType,
    phase: str,
    project_source_sha: str,
    verified_head_sha: str | None,
) -> str | None:
    board = (
        receipt.get("project_work_kanban")
        if isinstance(receipt, dict)
        else None
    )
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


def _require_ancestry(
    executable: Path,
    project_root: Path,
    source_sha: str,
    verified_head_sha: str,
) -> None:
    result = _git(
        executable,
        project_root,
        "merge-base",
        "--is-ancestor",
        source_sha,
        verified_head_sha,
    )
    if result.returncode == 1:
        raise BootstrapError(
            "project source SHA must be an ancestor of verified project HEAD"
        )
    if result.returncode != 0:
        raise BootstrapError(
            "cannot verify project source-to-closeout ancestry"
        )


def _trusted_stream_invocation() -> bool:
    return bool(sys.argv) and sys.argv[0] == "-"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--entrypoint-source",
        required=True,
        choices=(TRUSTED_ENTRYPOINT_SOURCE,),
    )
    parser.add_argument(
        "--entrypoint-sha256",
        required=True,
        help="SHA-256 computed by the trusted launcher over streamed entrypoint bytes",
    )
    parser.add_argument(
        "--git-executable",
        required=True,
        type=Path,
        help="Absolute prevalidated system Git executable outside both repositories",
    )
    parser.add_argument(
        "--base-root",
        required=True,
        type=Path,
        help="Exact current Base repository root",
    )
    parser.add_argument(
        "--expected-base-sha",
        required=True,
        help="Exact Base SHA independently fresh-read by the caller",
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
    parser.add_argument(
        "--receipt",
        required=True,
        help="Bounded UTF-8 JSON receipt in a nonsymlink regular file",
    )
    parser.add_argument(
        "--phase",
        choices=("start", "resume", "closeout"),
        default="start",
    )
    parser.add_argument("--render-markdown", action="store_true")
    return parser


def main() -> int:
    if not _trusted_stream_invocation():
        print("BASE CURRENT PROJECT WORK BOOTSTRAP: FAIL")
        print(
            "- entrypoint must be executed from an exact Base commit stream "
            "through the documented trusted launcher"
        )
        return 2

    args = _parser().parse_args()
    receipt: object | None = None
    receipt_source = "UNREAD"
    project_root_for_report = args.project_root.resolve(strict=False)

    try:
        if args.entrypoint_source != TRUSTED_ENTRYPOINT_SOURCE:
            raise BootstrapError(
                "entrypoint source must be the exact Base commit stream"
            )
        if not re.fullmatch(r"[0-9a-f]{64}", args.entrypoint_sha256):
            raise BootstrapError(
                "entrypoint SHA-256 must be an exact lowercase 64-character digest"
            )
        expected_base_sha = _exact_sha(
            args.expected_base_sha, "expected Base SHA"
        )
        project_source_sha = _exact_sha(
            args.project_source_sha, "project source SHA"
        )
        if args.phase == "closeout":
            verified_head_sha = _exact_sha(
                args.verified_head_sha,
                "verified project HEAD",
            )
        elif args.verified_head_sha is not None:
            raise BootstrapError(
                "verified project HEAD is accepted only for closeout"
            )
        else:
            verified_head_sha = None

        base_candidate = _directory_candidate(
            args.base_root, "Base checkout"
        )
        project_candidate = _directory_candidate(
            args.project_root, "target project"
        )
        git_executable = _trusted_git_executable(
            args.git_executable,
            base_candidate=base_candidate,
            project_candidate=project_candidate,
        )
        base_root = _repository_root(
            base_candidate, "Base checkout", git_executable
        )
        project_root = _repository_root(
            project_candidate, "target project", git_executable
        )
        project_root_for_report = project_root
        git_executable = _trusted_git_executable(
            git_executable,
            base_candidate=base_root,
            project_candidate=project_root,
        )

        committed = _verify_base_closure(
            git_executable,
            base_root,
            expected_base_sha,
            args.entrypoint_sha256,
        )
        _require_local_commit(
            git_executable,
            project_root,
            project_source_sha,
            "project source",
        )
        if verified_head_sha is not None:
            _require_local_commit(
                git_executable,
                project_root,
                verified_head_sha,
                "verified project HEAD",
            )
            _require_ancestry(
                git_executable,
                project_root,
                project_source_sha,
                verified_head_sha,
            )

        receipt, receipt_source = _read_receipt(args.receipt)
        tracking, validator = _load_validators(
            committed, expected_base_sha
        )
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
                print(f"error={_json_line_value(str(error))}")
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
            "WORK CONTRACT RECEIPT: PASS "
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
        print(
            f"project_root={_json_line_value(str(project_root_for_report))}"
        )
        print(
            f"receipt_source={_json_line_value(receipt_source)}"
        )
        print(f"error={_json_line_value(str(exc))}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
