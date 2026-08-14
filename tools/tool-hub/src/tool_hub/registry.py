"""Read the single reviewed Base tool registry owner."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from types import ModuleType

from .runtime_trust import RuntimeTrustError, assert_committed_file, capture_runtime_pins


class HubRegistryError(ValueError):
    pass


_GIT_OVERRIDES = (
    "-c", "core.fsmonitor=false",
    "-c", "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
    "-c", "filter.lfs.required=false",
    "-c", "filter.lfs.smudge=cat",
    "-c", "filter.lfs.clean=cat",
)


def _descriptor_launch_supported() -> bool:
    return sys.platform == "linux" and Path("/proc/self/fd").is_dir()


def _portable_regular_bytes(root: Path, relative: Path) -> bytes:
    """Read a bounded catalog file while rejecting links and Windows reparse points."""
    current = root
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for index, part in enumerate(relative.parts):
        current = current / part
        metadata = current.lstat()
        if stat.S_ISLNK(metadata.st_mode) or (
            reparse_flag and getattr(metadata, "st_file_attributes", 0) & reparse_flag
        ):
            raise RuntimeTrustError("reviewed catalog path crosses a link")
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(metadata.st_mode):
            raise RuntimeTrustError("reviewed catalog parent is not a directory")
    before = current.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > 16 * 1024 * 1024:
        raise RuntimeTrustError("reviewed catalog file is not a bounded regular file")
    raw = current.read_bytes()
    after = current.lstat()
    if (
        (before.st_dev, before.st_ino, before.st_size)
        != (after.st_dev, after.st_ino, after.st_size)
        or len(raw) > 16 * 1024 * 1024
    ):
        raise RuntimeTrustError("reviewed catalog file changed while being read")
    return raw


def _portable_committed_file(root: Path, relative: Path) -> bytes:
    """Validate catalog bytes on platforms without the Linux descriptor runtime."""
    current = _portable_regular_bytes(root, relative)
    git_value = shutil.which("git")
    if not git_value:
        raise RuntimeTrustError("reviewed catalog Git identity is unavailable")
    git = Path(git_value).absolute()
    metadata = git.lstat()
    if not stat.S_ISREG(metadata.st_mode) or git.is_symlink():
        raise RuntimeTrustError("reviewed catalog Git executable is invalid")
    committed = subprocess.run(
        [str(git), *_GIT_OVERRIDES, "-C", str(root), "show", f"HEAD:{relative.as_posix()}"],
        capture_output=True,
        check=False,
        env={
            "PATH": os.environ.get("PATH", os.defpath),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )
    if committed.returncode != 0:
        raise RuntimeTrustError("reviewed catalog Git blob is unavailable")
    if relative.suffix == ".json":
        try:
            matches = json.loads(current.decode("utf-8")) == json.loads(
                committed.stdout.decode("utf-8")
            )
        except (UnicodeDecodeError, json.JSONDecodeError):
            matches = False
    else:
        matches = current.replace(b"\r\n", b"\n") == committed.stdout.replace(b"\r\n", b"\n")
    if not matches:
        raise RuntimeTrustError("reviewed catalog differs from committed bytes")
    return current


def load_reviewed_tools(
    base_root: Path,
    *,
    launch_supported: bool | None = None,
) -> tuple[dict[str, object], ...]:
    root = base_root.resolve()
    supported = _descriptor_launch_supported() if launch_supported is None else launch_supported
    try:
        validator_relative = Path("tools/validate_tool_registry.py")
        committed_reader = assert_committed_file if supported else _portable_committed_file
        validator_bytes = committed_reader(root, validator_relative)
        committed_reader(root, Path("tools/TOOL_REGISTRY.json"))
        committed_reader(root, Path("schemas/base-tool-registry-v1.schema.json"))
    except RuntimeTrustError as error:
        raise HubRegistryError("reviewed tool registry is invalid") from error
    validator_path = root / "tools" / "validate_tool_registry.py"
    module = ModuleType("base_tool_registry_validator")
    module.__file__ = str(validator_path)
    exec(compile(validator_bytes, str(validator_path), "exec"), module.__dict__)
    try:
        reviewed = module.load_registry(base_root, base_root / "tools" / "TOOL_REGISTRY.json")
        interpreter = root / ".venv" / "bin" / "python"
        pinned: list[dict[str, object]] = []
        for raw in reviewed:
            tool = dict(raw)
            tool["_launch_supported"] = supported
            if supported:
                tool.update(capture_runtime_pins(root, str(tool["owner_path"]), interpreter))
            pinned.append(tool)
        return tuple(pinned)
    except (OSError, ValueError, RuntimeTrustError) as error:
        raise HubRegistryError("reviewed tool registry is invalid") from error
