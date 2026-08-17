"""Fail-closed repair path for a reviewed Windows Tool Hub runtime update."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Callable

from base_tool_contracts.trusted_files import portable_subprocess_creationflags

from .windows_launcher import (
    LauncherError,
    ShortcutBuilder,
    WindowsLauncherInstaller,
    _assert_plain_parents,
    _atomic_write,
    _default_shortcut_builder,
    _report_launcher_error,
    _root_fingerprint,
    _sha256,
    _show_native_error,
    project_config_fingerprint,
    run_installed_launcher,
)


_REQUIRED = {
    "base_root",
    "project_config",
    "project_config_fingerprint",
    "pythonw",
    "git_executable",
    "port",
    "root_fingerprint",
    "pythonw_sha256",
    "git_sha256",
    "launcher_sha256",
    "desktop_entry_sha256",
    "launcher_token",
    "hub_runtime_fingerprint",
}
_RUNTIME_PATHS = (
    "tools/tool-hub/src/tool_hub",
    "tools/tool-hub/web",
    "tools/base-tool-contracts/src",
    "tools/TOOL_REGISTRY.json",
    "schemas/base-tool-registry-v1.schema.json",
    "tools/validate_tool_registry.py",
)


def _regular(path: Path, *, max_bytes: int) -> None:
    _assert_plain_parents(path)
    try:
        metadata = path.lstat()
    except OSError as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if (
        not stat.S_ISREG(metadata.st_mode)
        or stat.S_ISLNK(metadata.st_mode)
        or (reparse and getattr(metadata, "st_file_attributes", 0) & reparse)
        or metadata.st_size > max_bytes
    ):
        raise LauncherError("LAUNCHER_CONFIG_INVALID")


def _git(git: Path, root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [
            str(git),
            "-c",
            "core.fsmonitor=false",
            "-c",
            "core.hooksPath=",
            "-c",
            "credential.helper=",
            "-C",
            str(root),
            *arguments,
        ],
        capture_output=True,
        check=False,
        creationflags=portable_subprocess_creationflags(),
        env={
            "PATH": str(git.parent),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_EXTERNAL_DIFF": "",
        },
    )


def _assert_reviewed_runtime(root: Path, git: Path) -> None:
    head = _git(git, root, "rev-parse", "--verify", "HEAD")
    remote = _git(git, root, "rev-parse", "--verify", "refs/remotes/origin/main")
    if (
        head.returncode != 0
        or remote.returncode != 0
        or len(head.stdout.strip()) != 40
        or len(remote.stdout.strip()) != 40
        or head.stdout.strip() != remote.stdout.strip()
    ):
        raise LauncherError("LAUNCHER_MAIN_NOT_SYNCED")

    changed = _git(git, root, "diff", "--quiet", "--no-ext-diff", "HEAD", "--", *_RUNTIME_PATHS)
    if changed.returncode != 0:
        raise LauncherError("LAUNCHER_RUNTIME_DIRTY")

    untracked = _git(git, root, "ls-files", "--others", "--", *_RUNTIME_PATHS)
    if untracked.returncode != 0:
        raise LauncherError("LAUNCHER_UPDATE_REQUIRED")
    for raw in untracked.stdout.decode("utf-8", errors="strict").splitlines():
        candidate = Path(raw)
        if "__pycache__" in candidate.parts or any(part.endswith(".egg-info") for part in candidate.parts):
            continue
        raise LauncherError("LAUNCHER_RUNTIME_UNTRACKED")


def _load_repair_seed(path: Path) -> dict[str, object]:
    path = Path(path).absolute()
    if (
        path.name != "launcher-config.json"
        or path.parent.name != "launcher"
        or path.parent.parent.name != "BaseToolHub"
    ):
        raise LauncherError("LAUNCHER_CONFIG_INVALID")
    _regular(path, max_bytes=64 * 1024)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    if payload.get("schema_version") != 1 or not _REQUIRED.issubset(payload):
        raise LauncherError("LAUNCHER_CONFIG_INVALID")
    if payload["port"] != 8764:
        raise LauncherError("LAUNCHER_CONFIG_INVALID")

    root = Path(str(payload["base_root"])).absolute()
    project_config = Path(str(payload["project_config"])).absolute()
    pythonw = Path(str(payload["pythonw"])).absolute()
    git = Path(str(payload["git_executable"])).absolute()
    installed_launcher = path.parent / "Base Tool Hub.pyw"
    for candidate in (pythonw, git, installed_launcher):
        _regular(candidate, max_bytes=128 * 1024 * 1024)
    try:
        if _root_fingerprint(root) != payload["root_fingerprint"]:
            raise LauncherError("LAUNCHER_ROOT_IDENTITY_CHANGED")
        if project_config_fingerprint(project_config) != payload["project_config_fingerprint"]:
            raise LauncherError("LAUNCHER_PROJECT_CONFIG_CHANGED")
        if _sha256(pythonw) != payload["pythonw_sha256"]:
            raise LauncherError("LAUNCHER_PYTHON_CHANGED")
        if _sha256(git) != payload["git_sha256"]:
            raise LauncherError("LAUNCHER_GIT_CHANGED")
        if _sha256(installed_launcher) != payload["launcher_sha256"]:
            raise LauncherError("LAUNCHER_BOOTSTRAP_CHANGED")
    except LauncherError:
        raise
    except OSError as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    return payload


def repair_installed_launcher(
    config_path: Path,
    *,
    run: Callable[[Path], int] = run_installed_launcher,
    reviewed_runtime: Callable[[Path, Path], None] = _assert_reviewed_runtime,
    desktop: Path | None = None,
    shortcut_builder: ShortcutBuilder = _default_shortcut_builder,
) -> int:
    """Reissue only launcher-owned artifacts after reviewed Base runtime drift."""
    config_path = Path(config_path).absolute()
    payload = _load_repair_seed(config_path)
    root = Path(str(payload["base_root"])).absolute()
    project_config = Path(str(payload["project_config"])).absolute()
    git = Path(str(payload["git_executable"])).absolute()
    reviewed_runtime(root, git)
    local_app_data = config_path.parents[2]
    owner = WindowsLauncherInstaller(
        root,
        project_config,
        local_app_data=local_app_data,
        desktop=desktop,
        platform="win32",
        shortcut_builder=shortcut_builder,
        git_executable=git,
    )
    if owner.config_path != config_path:
        raise LauncherError("LAUNCHER_CONFIG_INVALID")
    _regular(owner.desktop_entry, max_bytes=1024 * 1024)
    if _sha256(owner.desktop_entry) != payload["desktop_entry_sha256"]:
        raise LauncherError("LAUNCHER_SHORTCUT_CHANGED")
    owner.install()
    try:
        refreshed = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    refreshed["launcher_token"] = str(payload["launcher_token"])
    _atomic_write(
        config_path,
        (json.dumps(refreshed, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return run(config_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return repair_installed_launcher(args.config)
    except Exception as error:
        _show_native_error(_report_launcher_error(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
