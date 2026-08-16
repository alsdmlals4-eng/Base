from __future__ import annotations

import os
from pathlib import Path
import shutil
from typing import Iterable, Mapping


_WINDOWS_WRAPPER_SUFFIXES = frozenset((".cmd", ".bat"))
_WINDOWS_NATIVE_SUFFIXES = frozenset((".exe", ".com"))
_CMD_METACHARACTERS = frozenset("&|<>^()%!")


def _existing_file(value: str | None) -> str | None:
    if not value:
        return None
    candidate = Path(value)
    try:
        if not candidate.is_file():
            return None
        return str(candidate.resolve(strict=True))
    except (OSError, RuntimeError):
        return None


def _resolve_windows_codex(environment: Mapping[str, str]) -> str:
    appdata = environment.get("APPDATA", "").strip()
    if appdata:
        for name in ("codex.cmd", "codex.bat"):
            candidate = _existing_file(str(Path(appdata) / "npm" / name))
            if candidate is not None:
                return candidate

    path_value = environment.get("PATH", "")
    for name in ("codex.exe", "codex.com", "codex.cmd", "codex.bat"):
        candidate = _existing_file(shutil.which(name, path=path_value))
        if candidate is not None:
            return candidate

    raise FileNotFoundError("codex")


def _contains_cmd_metacharacter(value: str) -> bool:
    return any(character in value for character in _CMD_METACHARACTERS)


def build_codex_command(
    arguments: Iterable[str],
    *,
    environment: Mapping[str, str] | None = None,
) -> list[str]:
    """Build one shell-free Codex process argv for the current platform.

    On Windows, npm commonly installs Codex as ``codex.cmd``. Python cannot
    execute that wrapper directly with ``shell=False``, so the wrapper is
    invoked through the exact command processor while Python itself continues
    to avoid shell expansion. Native executables and non-Windows hosts remain
    direct.
    """

    values = [str(item) for item in arguments]
    if os.name != "nt":
        return ["codex", *values]

    env = os.environ if environment is None else environment
    executable = _resolve_windows_codex(env)
    suffix = Path(executable).suffix.casefold()

    if suffix in _WINDOWS_NATIVE_SUFFIXES:
        return [executable, *values]
    if suffix not in _WINDOWS_WRAPPER_SUFFIXES:
        raise ValueError("Codex Windows launcher has an unsupported file type")

    if any(_contains_cmd_metacharacter(value) for value in (executable, *values)):
        raise ValueError("Codex Windows wrapper command contains cmd metacharacters")

    path_value = env.get("PATH", "")
    command_processor = _existing_file(env.get("COMSPEC"))
    if command_processor is None:
        command_processor = _existing_file(shutil.which("cmd.exe", path=path_value))
    if command_processor is None:
        raise FileNotFoundError("cmd.exe")

    return [
        command_processor,
        "/d",
        "/s",
        "/c",
        "call",
        executable,
        *values,
    ]
