"""Fail-closed repair path for a reviewed Windows Tool Hub runtime update."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
from typing import Callable

from .windows_launcher import (
    LauncherError,
    ShortcutBuilder,
    WindowsLauncherInstaller,
    _assert_plain_parents,
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
        static_changed = (
            _root_fingerprint(root) != payload["root_fingerprint"]
            or project_config_fingerprint(project_config) != payload["project_config_fingerprint"]
            or _sha256(pythonw) != payload["pythonw_sha256"]
            or _sha256(git) != payload["git_sha256"]
            or _sha256(installed_launcher) != payload["launcher_sha256"]
        )
    except OSError as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    if static_changed:
        raise LauncherError("LAUNCHER_UPDATE_REQUIRED")
    return payload


def repair_installed_launcher(
    config_path: Path,
    *,
    run: Callable[[Path], int] = run_installed_launcher,
    desktop: Path | None = None,
    shortcut_builder: ShortcutBuilder = _default_shortcut_builder,
) -> int:
    """Reissue only launcher-owned artifacts after reviewed Base runtime drift."""
    config_path = Path(config_path).absolute()
    payload = _load_repair_seed(config_path)
    root = Path(str(payload["base_root"])).absolute()
    project_config = Path(str(payload["project_config"])).absolute()
    git = Path(str(payload["git_executable"])).absolute()
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
        raise LauncherError("LAUNCHER_UPDATE_REQUIRED")
    owner.install()
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
