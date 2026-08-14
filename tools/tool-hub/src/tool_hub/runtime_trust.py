"""Launch-time identity pins for reviewed Studio code and its Python environment."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import sys

from base_tool_contracts.trusted_files import (
    TrustedFileError,
    normalized_line_endings,
    open_directory_nofollow,
    read_regular_at,
    read_regular_nofollow,
    read_regular_portable_nofollow,
    run_portable_git,
    run_trusted_git,
)


class RuntimeTrustError(ValueError):
    pass


def _descriptor_runtime_supported() -> bool:
    return sys.platform == "linux" and Path("/proc/self/fd").is_dir()


def _reparse_or_link(path: Path) -> bool:
    metadata = path.lstat()
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(
        reparse and getattr(metadata, "st_file_attributes", 0) & reparse
    )


def _assert_plain_directory(path: Path) -> Path:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    try:
        for part in absolute.parts[1:]:
            current = current / part
            metadata = current.lstat()
            if _reparse_or_link(current) or not stat.S_ISDIR(metadata.st_mode):
                raise RuntimeTrustError("reviewed runtime path crosses a link or reparse point")
    except OSError as error:
        raise RuntimeTrustError("reviewed runtime path is unavailable") from error
    return absolute


def _portable_git(root: Path, *arguments: str):
    try:
        return run_portable_git(root, *arguments)
    except TrustedFileError as error:
        raise RuntimeTrustError("reviewed Git identity is unavailable") from error


def assert_committed_file(base_root: Path, relative: Path) -> bytes:
    root = Path(base_root).absolute()
    if not _descriptor_runtime_supported():
        try:
            current, _ = read_regular_portable_nofollow(
                root / relative,
                max_bytes=16 * 1024 * 1024,
            )
            committed = _portable_git(root, "show", f"HEAD:{relative.as_posix()}")
            if committed.returncode != 0 or normalized_line_endings(current) != normalized_line_endings(
                committed.stdout
            ):
                raise RuntimeTrustError("reviewed registry owner differs from committed bytes")
            return current
        except TrustedFileError as error:
            raise RuntimeTrustError("reviewed registry owner cannot be read safely") from error
    descriptor = open_directory_nofollow(root)
    try:
        current, _ = read_regular_at(descriptor, relative, max_bytes=16 * 1024 * 1024)
        committed = run_trusted_git(descriptor, "show", f"HEAD:{relative.as_posix()}")
        if committed.returncode != 0 or normalized_line_endings(current) != normalized_line_endings(
            committed.stdout
        ):
            raise RuntimeTrustError("reviewed registry owner differs from committed bytes")
        return current
    except TrustedFileError as error:
        raise RuntimeTrustError("reviewed registry owner cannot be read safely") from error
    finally:
        os.close(descriptor)


def _source_records(base_root: Path, owner_relative: str) -> list[tuple[str, str, Path]]:
    roots = (Path(owner_relative), Path("tools/base-tool-contracts/src"))
    if _descriptor_runtime_supported():
        descriptor = open_directory_nofollow(base_root)
        try:
            result = run_trusted_git(
                descriptor,
                "ls-tree",
                "-r",
                "-z",
                "HEAD",
                "--",
                *(item.as_posix() for item in roots),
            )
        finally:
            os.close(descriptor)
    else:
        result = _portable_git(
            base_root,
            "ls-tree",
            "-r",
            "-z",
            "HEAD",
            "--",
            *(item.as_posix() for item in roots),
        )
    if result.returncode != 0:
        raise RuntimeTrustError("reviewed source Git identity is unavailable")
    records: list[tuple[str, str, Path]] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_name = raw.split(b"\t", 1)
            mode, object_type, blob_sha = metadata.decode("ascii").split()
            relative = Path(raw_name.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            raise RuntimeTrustError("reviewed source Git identity is malformed") from error
        if object_type != "blob" or mode == "120000":
            raise RuntimeTrustError("reviewed source cannot contain links")
        records.append((mode, blob_sha, relative))
    if not records:
        raise RuntimeTrustError("reviewed source is not committed")
    return records


def _committed_source_digest(base_root: Path, owner_relative: str) -> str:
    root = Path(base_root).absolute()
    records = _source_records(root, owner_relative)
    tracked = {relative.as_posix() for _, _, relative in records}
    for runtime_root in (
        root / owner_relative / "src",
        root / owner_relative / "web",
        root / "tools/base-tool-contracts/src",
    ):
        if not runtime_root.exists():
            continue
        _assert_plain_directory(runtime_root)
        for candidate in runtime_root.rglob("*"):
            try:
                if _reparse_or_link(candidate):
                    raise RuntimeTrustError("reviewed source contains a linked runtime path")
                if (
                    candidate.is_dir()
                    or "__pycache__" in candidate.parts
                    or any(part.endswith(".egg-info") for part in candidate.parts)
                ):
                    continue
            except OSError as error:
                raise RuntimeTrustError("reviewed source cannot be read safely") from error
            relative = candidate.relative_to(root)
            if relative.as_posix() not in tracked:
                raise RuntimeTrustError("reviewed source contains an uncommitted runtime file")

    digest = hashlib.sha256()
    if _descriptor_runtime_supported():
        descriptor = open_directory_nofollow(root)
        try:
            for mode, blob_sha, relative in sorted(records, key=lambda item: item[2].as_posix()):
                current, identity = read_regular_at(descriptor, relative, max_bytes=16 * 1024 * 1024)
                committed = run_trusted_git(descriptor, "cat-file", "blob", blob_sha)
                if committed.returncode != 0:
                    raise RuntimeTrustError("reviewed source Git blob is unavailable")
                if (
                    ("100755" if identity.mode & stat.S_IXUSR else "100644") != mode
                    or normalized_line_endings(current) != normalized_line_endings(committed.stdout)
                ):
                    raise RuntimeTrustError("reviewed source differs from committed bytes")
                _update_source_digest(digest, mode, blob_sha, relative)
        except TrustedFileError as error:
            raise RuntimeTrustError("reviewed source cannot be read safely") from error
        finally:
            os.close(descriptor)
    else:
        for mode, blob_sha, relative in sorted(records, key=lambda item: item[2].as_posix()):
            try:
                current, _ = read_regular_portable_nofollow(
                    root / relative,
                    max_bytes=16 * 1024 * 1024,
                )
            except TrustedFileError as error:
                raise RuntimeTrustError("reviewed source cannot be read safely") from error
            committed = _portable_git(root, "cat-file", "blob", blob_sha)
            if committed.returncode != 0 or normalized_line_endings(current) != normalized_line_endings(
                committed.stdout
            ):
                raise RuntimeTrustError("reviewed source differs from committed bytes")
            _update_source_digest(digest, mode, blob_sha, relative)
    return digest.hexdigest()


def _update_source_digest(digest, mode: str, blob_sha: str, relative: Path) -> None:
    digest.update(mode.encode("ascii"))
    digest.update(b"\0")
    digest.update(blob_sha.encode("ascii"))
    digest.update(b"\0")
    digest.update(relative.as_posix().encode("utf-8"))
    digest.update(b"\0")


def _site_packages(base_root: Path) -> Path:
    root = Path(base_root).absolute() / ".venv"
    if os.name == "nt":
        return root / "Lib" / "site-packages"
    return root / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"


def _environment_digest(base_root: Path, interpreter: Path) -> tuple[str, str]:
    try:
        executable = Path(interpreter).absolute()
        if _descriptor_runtime_supported():
            executable = executable.resolve(strict=True)
            executable_bytes, _ = read_regular_nofollow(executable, max_bytes=64 * 1024 * 1024)
        else:
            executable_bytes, _ = read_regular_portable_nofollow(
                executable,
                max_bytes=64 * 1024 * 1024,
            )
        interpreter_sha256 = hashlib.sha256(executable_bytes).hexdigest()
        site_packages = _site_packages(base_root)
        _assert_plain_directory(site_packages)
        digest = hashlib.sha256()
        digest.update(interpreter_sha256.encode("ascii"))
        if _descriptor_runtime_supported():
            descriptor = open_directory_nofollow(site_packages)
            try:
                for candidate in sorted(site_packages.rglob("*"), key=lambda item: item.as_posix()):
                    if candidate.is_symlink():
                        raise RuntimeTrustError("reviewed Python environment contains a linked path")
                    if candidate.is_dir() or "__pycache__" in candidate.parts:
                        continue
                    relative = candidate.relative_to(site_packages)
                    raw, identity = read_regular_at(descriptor, relative, max_bytes=16 * 1024 * 1024)
                    _update_environment_digest(digest, relative, raw, stat.S_IMODE(identity.mode))
            finally:
                os.close(descriptor)
        else:
            for candidate in sorted(site_packages.rglob("*"), key=lambda item: item.as_posix()):
                if _reparse_or_link(candidate):
                    raise RuntimeTrustError("reviewed Python environment contains a linked path")
                if candidate.is_dir() or "__pycache__" in candidate.parts:
                    continue
                relative = candidate.relative_to(site_packages)
                raw, identity = read_regular_portable_nofollow(
                    candidate,
                    max_bytes=16 * 1024 * 1024,
                )
                _update_environment_digest(digest, relative, raw, stat.S_IMODE(identity.mode))
        return interpreter_sha256, digest.hexdigest()
    except (OSError, TrustedFileError) as error:
        raise RuntimeTrustError("reviewed Python environment cannot be read safely") from error


def _update_environment_digest(digest, relative: Path, raw: bytes, mode: int) -> None:
    digest.update(relative.as_posix().encode("utf-8"))
    digest.update(b"\0")
    digest.update(str(mode).encode("ascii"))
    digest.update(b"\0")
    digest.update(hashlib.sha256(raw).digest())


def capture_runtime_pins(base_root: Path, owner_relative: str, interpreter: Path) -> dict[str, str]:
    source_sha256 = _committed_source_digest(base_root, owner_relative)
    interpreter_sha256, environment_sha256 = _environment_digest(base_root, interpreter)
    return {
        "_source_sha256": source_sha256,
        "_interpreter_sha256": interpreter_sha256,
        "_environment_sha256": environment_sha256,
    }


def assert_runtime_pins(
    base_root: Path,
    owner_relative: str,
    interpreter: Path,
    expected: dict[str, object],
) -> None:
    current = capture_runtime_pins(base_root, owner_relative, interpreter)
    if current["_source_sha256"] != expected.get("_source_sha256"):
        raise RuntimeTrustError("reviewed source identity changed before launch")
    if current["_interpreter_sha256"] != expected.get("_interpreter_sha256"):
        raise RuntimeTrustError("reviewed interpreter identity changed before launch")
    if current["_environment_sha256"] != expected.get("_environment_sha256"):
        raise RuntimeTrustError("reviewed Python environment identity changed before launch")
