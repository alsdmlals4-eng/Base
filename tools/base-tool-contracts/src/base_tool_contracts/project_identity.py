"""Canonical project identity validation for reviewed localhost tools."""

from __future__ import annotations

from dataclasses import dataclass, field
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import site
import stat
import subprocess
import sys
import tempfile
import zipfile

try:
    import fcntl
except ModuleNotFoundError:  # Windows has no POSIX descriptor-sealing module.
    fcntl = None

from .trusted_files import (
    TrustedFileError,
    open_directory_at_nofollow,
    open_directory_nofollow,
    read_regular_at,
    trusted_git_executable,
)


_PROJECT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ADAPTER = Path("skills/PROJECT_BASE_ADAPTER.json")
_VALIDATOR_FILES = (
    Path("tools/check_project_operating_contract.py"),
    Path("tools/project_operating_contract.py"),
    Path("tools/base_release_index.py"),
    Path("schemas/project-base-adapter-v2.schema.json"),
)
_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=/dev/null",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)


class ProjectIdentityError(ValueError):
    pass


@dataclass(frozen=True)
class ProjectIdentityEvidence:
    project_id: str
    root: Path = field(repr=False)
    repository: str = ""
    engine: str = ""
    root_fingerprint: str = ""
    adapter_sha256: str = ""
    protected_paths: tuple[str, ...] = ()
    validator_sha256: str = ""


def _git(git: Path, repository: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    inherited: tuple[int, ...] = ()
    if repository.parts[:4] == ("/", "proc", "self", "fd") and len(repository.parts) == 5:
        try:
            inherited = (int(repository.parts[-1]),)
        except ValueError:
            inherited = ()
    return subprocess.run(
        [str(git), *_GIT_OVERRIDES, "-C", str(repository), *arguments],
        capture_output=True,
        check=False,
        pass_fds=inherited,
        env={
            "PATH": os.defpath,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C.UTF-8",
        },
    )


def _verified_validator_files(base_fd: int, base_alias: Path, version: str, git: Path) -> dict[Path, bytes]:
    if re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
    lock = Path(f"base-v{'.'.join(version.split('.')[:2])}.lock.json")
    result: dict[Path, bytes] = {}
    for relative in (*_VALIDATOR_FILES, lock):
        try:
            current, _ = read_regular_at(base_fd, relative)
        except TrustedFileError as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED") from error
        committed = _git(git, base_alias, "show", f"HEAD:{relative.as_posix()}")
        if committed.returncode != 0:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        if relative.suffix == ".json":
            try:
                matches = json.loads(current.decode("utf-8")) == json.loads(committed.stdout.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                matches = False
        else:
            matches = current == committed.stdout
        if not matches:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        result[relative] = committed.stdout
    return result


def _assert_no_untracked_validator_modules(base_fd: int, base_alias: Path, git: Path) -> None:
    """Reject checkout modules that could shadow the reviewed validator imports."""
    try:
        tools_fd = open_directory_at_nofollow(base_fd, Path("tools"))
        try:
            names = os.listdir(tools_fd)
        finally:
            os.close(tools_fd)
    except (OSError, TrustedFileError) as error:
        raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED") from error
    importable = {
        name
        for name in names
        if name.endswith((".py", ".pyc", ".pyo", ".so", ".pyd"))
    }
    for name in sorted(importable):
        tracked = _git(git, base_alias, "ls-files", "--error-unmatch", "--", f"tools/{name}")
        if tracked.returncode != 0:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")


def _private_validator_zip(files: dict[Path, bytes]) -> tuple[int, str, str]:
    """Build a sealed validator archive addressed only by its inherited fd."""
    with tempfile.SpooledTemporaryFile(max_size=4 * 1024 * 1024) as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
            for relative, raw in files.items():
                arcname = relative.as_posix()
                if arcname.startswith("tools/"):
                    arcname = arcname.removeprefix("tools/")
                archive.writestr(arcname, raw)
        stream.seek(0)
        return _sealed_memory_file(stream.read(), label="validator-runtime")


def _private_bytes_file(raw: bytes, *, suffix: str) -> tuple[int, str, str]:
    return _sealed_memory_file(raw, label=f"validator{suffix}")


def _sealed_memory_file(raw: bytes, *, label: str) -> tuple[int, str, str]:
    """Create a Linux sealed memfd so child/runtime bytes cannot change pre-exec."""
    if fcntl is None:
        raise ProjectIdentityError("PROJECT_IDENTITY_DESCRIPTOR_RUNTIME_UNAVAILABLE")
    library = ctypes.CDLL(None, use_errno=True)
    create = getattr(library, "memfd_create", None)
    if create is None:
        raise ProjectIdentityError("PROJECT_IDENTITY_DESCRIPTOR_RUNTIME_UNAVAILABLE")
    create.argtypes = (ctypes.c_char_p, ctypes.c_uint)
    create.restype = ctypes.c_int
    descriptor = create(label.encode("ascii"), 0x0001 | 0x0002)
    if descriptor < 0:
        raise ProjectIdentityError("PROJECT_IDENTITY_DESCRIPTOR_RUNTIME_UNAVAILABLE")
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
        # Linux F_ADD_SEALS with SEAL|SHRINK|GROW|WRITE.
        fcntl.fcntl(descriptor, 1033, 0x0001 | 0x0002 | 0x0004 | 0x0008)
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor, f"/proc/self/fd/{descriptor}", hashlib.sha256(raw).hexdigest()
    except Exception as error:
        os.close(descriptor)
        raise ProjectIdentityError("PROJECT_IDENTITY_DESCRIPTOR_RUNTIME_UNAVAILABLE") from error


def _hash_descriptor(descriptor: int) -> str:
    os.lseek(descriptor, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while chunk := os.read(descriptor, 1024 * 1024):
        digest.update(chunk)
    os.lseek(descriptor, 0, os.SEEK_SET)
    return digest.hexdigest()


def validate_project_identity(
    project_root: Path,
    expected_project_id: str | None,
    base_root: Path,
) -> ProjectIdentityEvidence:
    if expected_project_id is not None and _PROJECT_ID.fullmatch(expected_project_id) is None:
        raise ProjectIdentityError("PROJECT_IDENTITY_INVALID_LOCATOR")
    if not Path("/proc/self/fd").is_dir():
        raise ProjectIdentityError("PROJECT_IDENTITY_DESCRIPTOR_RUNTIME_UNAVAILABLE")
    try:
        root_fd = open_directory_nofollow(Path(project_root).absolute())
        base_fd = open_directory_nofollow(Path(base_root).absolute())
    except TrustedFileError as error:
        raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
    try:
        root_alias = Path(f"/proc/self/fd/{root_fd}")
        base_alias = Path(f"/proc/self/fd/{base_fd}")
        try:
            git = trusted_git_executable()
        except TrustedFileError as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED") from error
        top = _git(git, root_alias, "rev-parse", "--show-toplevel")
        if top.returncode != 0:
            raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
        top_path = top.stdout.decode("utf-8", errors="replace").strip()
        try:
            top_fd = open_directory_nofollow(Path(top_path))
            try:
                top_stat = os.fstat(top_fd)
                root_stat_at_start = os.fstat(root_fd)
            finally:
                os.close(top_fd)
        except TrustedFileError as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
        if (top_stat.st_dev, top_stat.st_ino) != (root_stat_at_start.st_dev, root_stat_at_start.st_ino):
            raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED")
        raw, adapter_identity = read_regular_at(root_fd, _ADAPTER)
        try:
            adapter = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID") from error
        if adapter.get("schema_version") != 2:
            raise ProjectIdentityError("IDENTITY_MIGRATION_REQUIRED")
        project = adapter.get("project")
        project_id = project.get("project_id") if isinstance(project, dict) else None
        if not isinstance(project_id, str) or _PROJECT_ID.fullmatch(project_id) is None:
            raise ProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
        repository = project.get("repository") if isinstance(project, dict) else None
        engine = project.get("engine") if isinstance(project, dict) else None
        if (
            project.get("root") != "."
            or not isinstance(repository, str)
            or not repository
            or not isinstance(engine, str)
            or not engine
        ):
            raise ProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
        expected_project_id = expected_project_id or project_id
        if project_id != expected_project_id:
            raise ProjectIdentityError("PROJECT_IDENTITY_MISMATCH")
        base_release = adapter.get("base_release")
        version = base_release.get("version") if isinstance(base_release, dict) else None
        if not isinstance(version, str):
            raise ProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
        validator_files = _verified_validator_files(base_fd, base_alias, version, git)
        _assert_no_untracked_validator_modules(base_fd, base_alias, git)
        validator_digest = hashlib.sha256()
        for relative, content in sorted(validator_files.items(), key=lambda item: item[0].as_posix()):
            validator_digest.update(relative.as_posix().encode())
            validator_digest.update(b"\0")
            validator_digest.update(hashlib.sha256(content).digest())
        adapter_sha = hashlib.sha256(raw).hexdigest()
        runtime_fd, runtime_alias, runtime_sha = _private_validator_zip(validator_files)
        schema_fd, schema_alias, schema_sha = _private_bytes_file(
            validator_files[Path("schemas/project-base-adapter-v2.schema.json")],
            suffix=".json",
        )
        try:
            code = (
                "import runpy,sys; from pathlib import Path; runtime=sys.argv[1]; "
                "site_paths=sys.argv[2].split('\\0'); sys.path[:0]=[runtime,*site_paths]; "
                "import project_operating_contract as contract; contract.ADAPTER_V2_SCHEMA=Path(sys.argv[3]); "
                "sys.argv=['check_project_operating_contract',*sys.argv[4:]]; "
                "runpy.run_module('check_project_operating_contract',run_name='__main__')"
            )
            command = [
                sys.executable, "-I", "-S", "-c", code, runtime_alias,
                "\0".join(site.getsitepackages()),
                schema_alias,
                "--project-root", str(root_alias),
                "--base-repository", str(base_alias),
                "--hub-identity-check",
                "--expected-project-id", expected_project_id,
                "--expected-adapter-sha256", adapter_sha,
            ]
            completed = subprocess.run(
                command,
                cwd=Path(os.path.sep),
                env={
                    "PATH": os.defpath,
                    "PYTHONUTF8": "1",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "BASE_TOOL_TRUSTED_GIT": str(git),
                    "BASE_TOOL_TRUSTED_GIT_ARGS": "1",
                    "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_OPTIONAL_LOCKS": "0",
                    "LC_ALL": "C.UTF-8",
                },
                pass_fds=(root_fd, base_fd, runtime_fd, schema_fd),
                capture_output=True,
                check=False,
            )
            if _hash_descriptor(runtime_fd) != runtime_sha or _hash_descriptor(schema_fd) != schema_sha:
                raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        finally:
            os.close(runtime_fd)
            os.close(schema_fd)
        if completed.returncode != 0:
            raise ProjectIdentityError("PROJECT_IDENTITY_VALIDATOR_BLOCKED")
        raw_after, identity_after = read_regular_at(root_fd, _ADAPTER)
        if raw_after != raw or (adapter_identity.device, adapter_identity.inode) != (identity_after.device, identity_after.inode):
            raise ProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED")
        root_stat = os.fstat(root_fd)
        selected_path = Path(os.path.abspath(project_root))
        try:
            selected_fd = open_directory_nofollow(selected_path)
            try:
                selected_stat = os.fstat(selected_fd)
            finally:
                os.close(selected_fd)
        except TrustedFileError as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED") from error
        if (selected_stat.st_dev, selected_stat.st_ino) != (root_stat.st_dev, root_stat.st_ino):
            raise ProjectIdentityError("PROJECT_IDENTITY_SNAPSHOT_CHANGED")
        protected = adapter.get("protected_paths")
        if not isinstance(protected, list) or not all(isinstance(item, str) for item in protected):
            raise ProjectIdentityError("PROJECT_IDENTITY_ADAPTER_INVALID")
        try:
            vault_fd = open_directory_at_nofollow(root_fd, Path(".asset-vault/library"))
            os.close(vault_fd)
        except TrustedFileError as error:
            raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
        ignored = _git(git, root_alias, "check-ignore", "-q", "--no-index", "--", ".asset-vault/library/.hub-probe")
        if ignored.returncode != 0:
            raise ProjectIdentityError("PROJECT_ASSET_VAULT_NOT_GITIGNORED")
        fingerprint = hashlib.sha256(
            f"{root_stat.st_dev}:{root_stat.st_ino}:{adapter_sha}".encode()
        ).hexdigest()
        return ProjectIdentityEvidence(
            project_id=expected_project_id,
            root=selected_path,
            repository=repository,
            engine=engine,
            root_fingerprint=fingerprint,
            adapter_sha256=adapter_sha,
            protected_paths=tuple(protected),
            validator_sha256=validator_digest.hexdigest(),
        )
    except TrustedFileError as error:
        raise ProjectIdentityError("PROJECT_IDENTITY_PATH_BLOCKED") from error
    finally:
        os.close(root_fd)
        os.close(base_fd)
