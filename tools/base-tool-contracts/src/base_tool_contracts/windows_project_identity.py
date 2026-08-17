"""Portable project identity validation for Windows registration."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import site
import stat
import subprocess
import sys
import tempfile
import zipfile

from .trusted_files import portable_subprocess_creationflags


_PROJECT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ADAPTER = Path("skills/PROJECT_BASE_ADAPTER.json")
_VALIDATOR_FILES = (
    Path("tools/check_project_operating_contract.py"),
    Path("tools/project_operating_contract.py"),
    Path("tools/base_release_index.py"),
    Path("schemas/project-base-adapter-v2.schema.json"),
)
_MAX_CONTRACT_BYTES = 16 * 1024 * 1024
_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
    "-c", "core.autocrlf=true",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)


class WindowsProjectIdentityError(ValueError):
    def __init__(self, code: str, *, diagnostic: str = "") -> None:
        super().__init__(code)
        self._diagnostic = diagnostic


@dataclass(frozen=True)
class WindowsProjectIdentityEvidence:
    project_id: str
    root: Path
    repository: str
    engine: str
    root_fingerprint: str
    adapter_sha256: str
    protected_paths: tuple[str, ...]
    validator_sha256: str


@dataclass(frozen=True)
class _PortableIdentity:
    device: int
    inode: int
    size: int


def _is_reparse(metadata: os.stat_result) -> bool:
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(
        reparse_flag and getattr(metadata, "st_file_attributes", 0) & reparse_flag
    )


def _absolute_nofollow(path: Path, *, directory: bool) -> tuple[Path, os.stat_result]:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    try:
        for part in absolute.parts[1:]:
            current /= part
            metadata = current.lstat()
            if _is_reparse(metadata):
                raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
        metadata = absolute.lstat()
    except (OSError, ValueError) as error:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
    expected = stat.S_ISDIR(metadata.st_mode) if directory else stat.S_ISREG(metadata.st_mode)
    if not expected:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
    return absolute, metadata


def _read_regular(path: Path) -> tuple[bytes, _PortableIdentity]:
    absolute, before = _absolute_nofollow(path, directory=False)
    if before.st_size > _MAX_CONTRACT_BYTES:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(absolute, flags)
        try:
            held = os.fstat(descriptor)
            if not stat.S_ISREG(held.st_mode) or held.st_size > _MAX_CONTRACT_BYTES:
                raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
            chunks: list[bytes] = []
            remaining = _MAX_CONTRACT_BYTES + 1
            while remaining:
                chunk = os.read(descriptor, min(1024 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
        finally:
            os.close(descriptor)
        after = absolute.lstat()
    except OSError as error:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
    raw = b"".join(chunks)
    identities = {
        (item.st_dev, item.st_ino, item.st_size)
        for item in (before, held, after)
    }
    if len(raw) > _MAX_CONTRACT_BYTES or len(identities) != 1 or _is_reparse(after):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED")
    return raw, _PortableIdentity(held.st_dev, held.st_ino, held.st_size)


def _trusted_git() -> Path:
    candidate = shutil.which("git")
    if not candidate:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
    absolute, _ = _absolute_nofollow(Path(candidate), directory=False)
    return absolute


def _git(git: Path, repository: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [str(git), *_GIT_OVERRIDES, "-C", str(repository), *arguments],
        capture_output=True,
        check=False,
        creationflags=portable_subprocess_creationflags(),
        env={
            "PATH": str(git.parent),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )


def _semantic_json_equal(left: bytes, right: bytes) -> bool:
    try:
        return json.loads(left.decode("utf-8")) == json.loads(right.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False


def _verified_validator_files(
    base_root: Path,
    version: str,
    git: Path,
) -> dict[Path, bytes]:
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
    lock = Path(f"base-v{'.'.join(version.split('.')[:2])}.lock.json")
    result: dict[Path, bytes] = {}
    for relative in (*_VALIDATOR_FILES, lock):
        current, _ = _read_regular(base_root / relative)
        committed = _git(git, base_root, "show", f"HEAD:{relative.as_posix()}")
        if committed.returncode != 0:
            raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        matches = (
            _semantic_json_equal(current, committed.stdout)
            if relative.suffix == ".json"
            else current.replace(b"\r\n", b"\n") == committed.stdout.replace(b"\r\n", b"\n")
        )
        if not matches:
            raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        result[relative] = committed.stdout
    for candidate in (base_root / "tools").iterdir():
        if candidate.suffix.lower() not in {".py", ".pyc", ".pyo", ".pyd", ".so"}:
            continue
        tracked = _git(
            git,
            base_root,
            "ls-files",
            "--error-unmatch",
            "--",
            candidate.relative_to(base_root).as_posix(),
        )
        if tracked.returncode != 0:
            raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
    return result


def _run_validator(
    project_root: Path,
    base_root: Path,
    expected_project_id: str,
    adapter_sha256: str,
    files: dict[Path, bytes],
    git: Path,
) -> str:
    digest = hashlib.sha256()
    for relative, raw in sorted(files.items(), key=lambda item: item[0].as_posix()):
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(raw).digest())
    with tempfile.TemporaryDirectory(prefix="base-tool-hub-validator-") as raw_runtime:
        runtime = Path(raw_runtime)
        try:
            runtime.chmod(0o700)
        except OSError:
            pass
        archive_path = runtime / "validator.zip"
        schema_path = runtime / "project-base-adapter-v2.schema.json"
        with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_STORED) as archive:
            for relative, raw in files.items():
                arcname = relative.as_posix()
                if arcname.startswith("tools/"):
                    arcname = arcname.removeprefix("tools/")
                archive.writestr(arcname, raw)
        schema_path.write_bytes(files[Path("schemas/project-base-adapter-v2.schema.json")])
        archive_before = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        schema_before = hashlib.sha256(schema_path.read_bytes()).hexdigest()
        code = (
            "import runpy,sys; from pathlib import Path; runtime=sys.argv[1]; "
            "site_paths=sys.argv[2].split(sys.argv[3]); sys.path[:0]=[runtime,*site_paths]; "
            "import project_operating_contract as contract; contract.ADAPTER_V2_SCHEMA=Path(sys.argv[4]); "
            "sys.argv=['check_project_operating_contract',*sys.argv[5:]]; "
            "runpy.run_module('check_project_operating_contract',run_name='__main__')"
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-I",
                "-S",
                "-c",
                code,
                str(archive_path),
                os.pathsep.join(site.getsitepackages()),
                os.pathsep,
                str(schema_path),
                "--project-root",
                str(project_root),
                "--base-repository",
                str(base_root),
                "--hub-identity-check",
                "--expected-project-id",
                expected_project_id,
                "--expected-adapter-sha256",
                adapter_sha256,
            ],
            cwd=base_root.anchor,
            env={
                "PATH": str(git.parent),
                "PYTHONUTF8": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                "BASE_TOOL_TRUSTED_GIT": str(git),
                "BASE_TOOL_TRUSTED_GIT_ARGS": "1",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_OPTIONAL_LOCKS": "0",
            },
            capture_output=True,
            check=False,
            creationflags=portable_subprocess_creationflags(),
        )
        if (
            hashlib.sha256(archive_path.read_bytes()).hexdigest() != archive_before
            or hashlib.sha256(schema_path.read_bytes()).hexdigest() != schema_before
        ):
            raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        if completed.returncode != 0:
            diagnostic = completed.stderr.decode("utf-8", errors="replace")[-2000:]
            for private_path, label in (
                (str(project_root), "<PROJECT_ROOT>"),
                (str(base_root), "<BASE_ROOT>"),
                (str(runtime), "<PRIVATE_RUNTIME>"),
            ):
                diagnostic = diagnostic.replace(private_path, label)
            raise WindowsProjectIdentityError(
                "PROJECT_IDENTITY_VALIDATOR_BLOCKED",
                diagnostic=diagnostic,
            )
    return digest.hexdigest()


def validate_windows_project_identity(
    project_root: Path,
    expected_project_id: str,
    base_root: Path,
) -> WindowsProjectIdentityEvidence:
    if _PROJECT_ID.fullmatch(expected_project_id) is None:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_INVALID_LOCATOR")
    root, root_before = _absolute_nofollow(project_root, directory=True)
    base, _ = _absolute_nofollow(base_root, directory=True)
    git = _trusted_git()
    top = _git(git, root, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
    top_value = top.stdout.decode("utf-8", errors="replace").strip()
    if os.path.normcase(os.path.realpath(top_value)) != os.path.normcase(os.path.realpath(root)):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")

    raw, adapter_identity = _read_regular(root / _ADAPTER)
    try:
        adapter = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID") from error
    if adapter.get("schema_version") != 2:
        raise WindowsProjectIdentityError("IDENTITY_MIGRATION_REQUIRED")
    project = adapter.get("project")
    project_id = project.get("project_id") if isinstance(project, dict) else None
    repository = project.get("repository") if isinstance(project, dict) else None
    engine = project.get("engine") if isinstance(project, dict) else None
    if (
        not isinstance(project_id, str)
        or _PROJECT_ID.fullmatch(project_id) is None
        or project_id != expected_project_id
    ):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_MISMATCH")
    if (
        project.get("root") != "."
        or not isinstance(repository, str)
        or not repository
        or not isinstance(engine, str)
        or not engine
    ):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
    committed = _git(git, root, "show", f"HEAD:{_ADAPTER.as_posix()}")
    if committed.returncode != 0 or not _semantic_json_equal(raw, committed.stdout):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
    if _git(git, root, "diff", "--cached", "--quiet", "--", _ADAPTER.as_posix()).returncode != 0:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")

    base_release = adapter.get("base_release")
    version = base_release.get("version") if isinstance(base_release, dict) else None
    if not isinstance(version, str):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
    validator_files = _verified_validator_files(base, version, git)
    adapter_sha = hashlib.sha256(raw).hexdigest()
    validator_sha = _run_validator(
        root,
        base,
        expected_project_id,
        adapter_sha,
        validator_files,
        git,
    )

    raw_after, adapter_after = _read_regular(root / _ADAPTER)
    try:
        root_after = root.lstat()
    except OSError as error:
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED") from error
    if (
        raw_after != raw
        or adapter_after != adapter_identity
        or _is_reparse(root_after)
        or (root_after.st_dev, root_after.st_ino) != (root_before.st_dev, root_before.st_ino)
    ):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED")

    _absolute_nofollow(root / ".asset-vault" / "library", directory=True)
    ignored = _git(
        git,
        root,
        "check-ignore",
        "-q",
        "--no-index",
        "--",
        ".asset-vault/library/.hub-probe",
    )
    if ignored.returncode != 0:
        raise WindowsProjectIdentityError("PROJECT_ASSET_VAULT_NOT_GITIGNORED")
    protected = adapter.get("protected_paths")
    if not isinstance(protected, list) or not all(isinstance(item, str) for item in protected):
        raise WindowsProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
    fingerprint = hashlib.sha256(
        f"{root_after.st_dev}:{root_after.st_ino}:{adapter_sha}".encode("utf-8")
    ).hexdigest()
    return WindowsProjectIdentityEvidence(
        project_id=project_id,
        root=root,
        repository=repository,
        engine=engine,
        root_fingerprint=fingerprint,
        adapter_sha256=adapter_sha,
        protected_paths=tuple(protected),
        validator_sha256=validator_sha,
    )
