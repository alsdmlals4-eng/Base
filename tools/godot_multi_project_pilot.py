import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from tools.godot_project_pilot_descriptor import (
    BehaviorCheck,
    ProjectPilotDescriptor,
    load_descriptor,
)
from tools.godot_project_pilot_evidence import (
    EvidenceVerificationError,
    VerifiedRuntimeEvidence,
    verify_runtime_evidence,
    write_final_evidence,
)
from tools.godot_project_pilot_workspace import (
    compare_inventories,
    copy_to_workspace,
    inventory_tracked_files,
    materialize_runtime_workspace,
)


_MAX_CAPTURE_BYTES = 1024 * 1024
_SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class ProcessRecord:
    argv: tuple[str, ...]
    returncode: int
    stdout_sha256: str
    stderr_sha256: str
    stdout_excerpt: str
    stderr_excerpt: str
    stdout_truncated: bool
    stderr_truncated: bool


def argv_for_check(check: BehaviorCheck, godot_bin: Path) -> list[str]:
    if check.kind == "PYTHON_UNITTEST_MODULE":
        return [sys.executable, "-m", "unittest", check.target, "-v"]
    if check.kind == "PYTHON_PYTEST_PATH":
        return [sys.executable, "-m", "pytest", check.target, "-q"]
    if check.kind == "GODOT_SCRIPT":
        return [str(Path(godot_bin)), "--headless", "--path", ".", "--script", check.target]
    raise ValueError(f"UNSUPPORTED_BEHAVIOR_CHECK: {check.kind}")


def processes_for_descriptor(
    descriptor: ProjectPilotDescriptor,
    godot_bin: Path,
) -> list[list[str]]:
    if not descriptor.is_runtime_project:
        return []
    return [argv_for_check(check, godot_bin) for check in descriptor.behavior_checks]


def _bounded_text(payload: bytes) -> tuple[str, bool]:
    truncated = len(payload) > _MAX_CAPTURE_BYTES
    retained = payload[:_MAX_CAPTURE_BYTES]
    return retained.decode("utf-8", errors="replace"), truncated


def _as_bytes(value: bytes | str | None) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8", errors="replace")


def _bounded_environment(home: Path) -> dict[str, str]:
    home = Path(home).resolve()
    home.mkdir(parents=True, exist_ok=True)
    return {
        "HOME": str(home),
        "TMPDIR": str(home),
        "TMP": str(home),
        "TEMP": str(home),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "PATH": os.environ.get("PATH", ""),
        "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
    }


def _process_record(
    argv: Sequence[str],
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> ProcessRecord:
    stdout_excerpt, stdout_truncated = _bounded_text(stdout)
    stderr_excerpt, stderr_truncated = _bounded_text(stderr)
    return ProcessRecord(
        argv=tuple(str(value) for value in argv),
        returncode=returncode,
        stdout_sha256=hashlib.sha256(stdout).hexdigest(),
        stderr_sha256=hashlib.sha256(stderr).hexdigest(),
        stdout_excerpt=stdout_excerpt,
        stderr_excerpt=stderr_excerpt,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
    )


def _run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: int,
) -> ProcessRecord:
    with tempfile.TemporaryDirectory(prefix="base-c0-process-") as temporary:
        try:
            completed = subprocess.run(
                list(argv),
                cwd=str(Path(cwd).resolve()),
                env=_bounded_environment(Path(temporary)),
                check=False,
                capture_output=True,
                shell=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            return _process_record(
                argv,
                124,
                _as_bytes(exc.stdout),
                _as_bytes(exc.stderr) + b"\nPROCESS_TIMEOUT",
            )
    return _process_record(
        argv,
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )


def run_behavior_check(
    check: BehaviorCheck,
    project_root: Path,
    godot_bin: Path,
) -> ProcessRecord:
    return _run_process(
        argv_for_check(check, godot_bin),
        cwd=project_root,
        timeout_seconds=check.timeout_seconds,
    )


def _git_text(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(Path(root).resolve()), *args],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise ValueError(f"GIT_IDENTITY_FAILED: {completed.stderr.strip()}")
    return completed.stdout.strip()


def _repository_from_remote(value: str) -> str:
    normalized = value.strip().removesuffix(".git")
    if normalized.startswith("git@github.com:"):
        return normalized.split(":", 1)[1]
    marker = "github.com/"
    if marker in normalized:
        return normalized.split(marker, 1)[1]
    raise ValueError(f"REPOSITORY_IDENTITY_UNSUPPORTED: {value}")


def _record_dict(record: ProcessRecord) -> dict[str, object]:
    return asdict(record)


def _verify_base_pin(
    base_root: Path,
    expected: str,
    descriptor: ProjectPilotDescriptor,
) -> None:
    if not _SHA40_RE.fullmatch(expected):
        raise ValueError("BASE_PILOT_COMMIT_MISMATCH: invalid workflow input")
    actual = _git_text(base_root, "rev-parse", "HEAD")
    if actual != expected or descriptor.base_pilot_commit != expected:
        raise ValueError(
            "BASE_PILOT_COMMIT_MISMATCH: workflow, descriptor, and checkout differ"
        )


def _write_failure_marker(
    output: Path,
    descriptor: ProjectPilotDescriptor,
    source_commit: str,
    exc: BaseException,
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "failure.json").write_text(
        json.dumps(
            {
                "code": str(exc),
                "repository": descriptor.repository,
                "source_commit": source_commit,
                "base_pilot_commit": descriptor.base_pilot_commit,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def run_pilot(
    base_root: Path,
    source_root: Path,
    descriptor_path: Path,
    godot_bin: Path,
    output_dir: Path,
    source_commit: str,
    expected_base_commit: str,
) -> int:
    base = Path(base_root).resolve()
    source = Path(source_root).resolve()
    output = Path(output_dir).resolve()
    descriptor = load_descriptor(
        Path(descriptor_path),
        base / "schemas/godot-project-pilot-v1.schema.json",
    )
    _verify_base_pin(base, expected_base_commit, descriptor)
    if _git_text(source, "rev-parse", "HEAD") != source_commit:
        raise ValueError("SOURCE_COMMIT_MISMATCH")
    remote_repository = _repository_from_remote(
        _git_text(source, "config", "--get", "remote.origin.url")
    )
    if remote_repository != descriptor.repository:
        raise ValueError(
            f"REPOSITORY_IDENTITY_MISMATCH: {remote_repository} != {descriptor.repository}"
        )

    before = inventory_tracked_files(source)
    process_records: list[ProcessRecord] = []
    for check in descriptor.behavior_checks:
        record = run_behavior_check(check, source, godot_bin)
        process_records.append(record)
        if record.returncode != 0:
            after = inventory_tracked_files(source)
            write_final_evidence(
                output,
                repository=descriptor.repository,
                source_commit=source_commit,
                base_pilot_commit=descriptor.base_pilot_commit,
                project_state=descriptor.project_state,
                result="FAIL",
                source_before=before,
                source_after=after,
                changed_paths=compare_inventories(before, after),
                runtime=None,
                legacy_mutation_authority="NOT_RUN",
                process_records=[_record_dict(value) for value in process_records],
            )
            return 3

    if not descriptor.is_runtime_project:
        after = inventory_tracked_files(source)
        changed = compare_inventories(before, after)
        write_final_evidence(
            output,
            repository=descriptor.repository,
            source_commit=source_commit,
            base_pilot_commit=descriptor.base_pilot_commit,
            project_state=descriptor.project_state,
            result="NOT_APPLICABLE" if not changed else "FAIL",
            source_before=before,
            source_after=after,
            changed_paths=changed,
            runtime=None,
            legacy_mutation_authority="NOT_APPLICABLE",
            process_records=[_record_dict(value) for value in process_records],
        )
        return 0 if not changed else 4

    runtime: VerifiedRuntimeEvidence | None = None
    preserved_autoloads: tuple[str, ...] = ()
    legacy_state = (
        "ABSENT"
        if not descriptor.legacy_editor_plugins and not descriptor.legacy_autoloads
        else "DISABLED_IN_WORKSPACE_ONLY"
    )
    try:
        with tempfile.TemporaryDirectory(prefix="base-godot-project-pilot-") as temporary:
            workspace = Path(temporary) / "project"
            copy_to_workspace(source, workspace)
            materialized = materialize_runtime_workspace(
                base,
                workspace,
                descriptor,
                source_commit,
            )
            preserved_autoloads = materialized.transform_report.preserved_autoloads
            godot_record = _run_process(
                [
                    str(Path(godot_bin).resolve()),
                    "--editor",
                    "--headless",
                    "--path",
                    str(workspace),
                    "--quit-after",
                    "600",
                ],
                cwd=workspace,
                timeout_seconds=180,
            )
            process_records.append(godot_record)
            if godot_record.returncode != 0:
                raise ValueError("GODOT_PROJECT_PILOT_FAILED")
            runtime_path = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            runtime = verify_runtime_evidence(workspace, runtime_path)
            if runtime.repository != descriptor.repository:
                raise EvidenceVerificationError("RUNTIME_REPOSITORY_MISMATCH")
            if runtime.source_commit != source_commit:
                raise EvidenceVerificationError("RUNTIME_SOURCE_COMMIT_MISMATCH")
            if runtime.base_pilot_commit != descriptor.base_pilot_commit:
                raise EvidenceVerificationError("RUNTIME_BASE_COMMIT_MISMATCH")
    except (OSError, ValueError) as exc:
        after = inventory_tracked_files(source)
        changed = compare_inventories(before, after)
        _write_failure_marker(output, descriptor, source_commit, exc)
        write_final_evidence(
            output,
            repository=descriptor.repository,
            source_commit=source_commit,
            base_pilot_commit=descriptor.base_pilot_commit,
            project_state=descriptor.project_state,
            result="FAIL",
            source_before=before,
            source_after=after,
            changed_paths=changed,
            runtime=None,
            legacy_mutation_authority=legacy_state,
            preserved_autoloads=preserved_autoloads,
            process_records=[_record_dict(value) for value in process_records],
        )
        if changed:
            return 4
        if isinstance(exc, EvidenceVerificationError):
            return 5
        return 3

    after = inventory_tracked_files(source)
    changed = compare_inventories(before, after)
    write_final_evidence(
        output,
        repository=descriptor.repository,
        source_commit=source_commit,
        base_pilot_commit=descriptor.base_pilot_commit,
        project_state=descriptor.project_state,
        result="PASS" if not changed else "FAIL",
        source_before=before,
        source_after=after,
        changed_paths=changed,
        runtime=runtime,
        legacy_mutation_authority=legacy_state,
        preserved_autoloads=preserved_autoloads,
        process_records=[_record_dict(value) for value in process_records],
    )
    return 0 if not changed else 4


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a bounded Base C0 Godot project Pilot"
    )
    parser.add_argument("--base-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--expected-base-commit", required=True)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--godot-bin", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        return run_pilot(
            base_root=arguments.base_root,
            source_root=arguments.source_root,
            descriptor_path=arguments.descriptor,
            godot_bin=arguments.godot_bin,
            output_dir=arguments.output_dir,
            source_commit=arguments.source_commit,
            expected_base_commit=arguments.expected_base_commit,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
