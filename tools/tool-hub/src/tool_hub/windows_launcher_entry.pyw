"""Standalone no-console bootstrap for the reviewed Tool Hub launcher."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess


_REASON = re.compile(r"^[A-Z0-9_]{1,80}$")
_REQUIRED = {
    "base_root", "project_config", "project_config_fingerprint", "pythonw",
    "git_executable", "port", "root_fingerprint", "pythonw_sha256",
    "git_sha256", "launcher_sha256", "launcher_token", "hub_runtime_fingerprint",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _root_fingerprint(root: Path) -> str:
    metadata = root.stat()
    return hashlib.sha256(f"{root.absolute()}:{metadata.st_dev}:{metadata.st_ino}".encode()).hexdigest()


def _project_config_fingerprint(path: Path) -> str:
    normalized = os.path.normcase(os.path.abspath(path))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _regular(path: Path, *, max_bytes: int) -> None:
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for parent in reversed(path.absolute().parents):
        parent_metadata = parent.lstat()
        if stat.S_ISLNK(parent_metadata.st_mode) or (
            reparse and getattr(parent_metadata, "st_file_attributes", 0) & reparse
        ):
            raise RuntimeError("LAUNCHER_CONFIG_INVALID")
    metadata = path.lstat()
    if (
        not stat.S_ISREG(metadata.st_mode)
        or stat.S_ISLNK(metadata.st_mode)
        or (reparse and getattr(metadata, "st_file_attributes", 0) & reparse)
        or metadata.st_size > max_bytes
    ):
        raise RuntimeError("LAUNCHER_CONFIG_INVALID")


def _hub_runtime_fingerprint(root: Path) -> str:
    relative_roots = (
        Path("tools/tool-hub/src/tool_hub"),
        Path("tools/tool-hub/web"),
        Path("tools/base-tool-contracts/src"),
    )
    fixed = (
        Path("tools/TOOL_REGISTRY.json"),
        Path("schemas/base-tool-registry-v1.schema.json"),
        Path("tools/validate_tool_registry.py"),
    )
    candidates = set()
    for relative_root in relative_roots:
        directory = root / relative_root
        if not directory.is_dir() or directory.is_symlink():
            continue
        for candidate in directory.rglob("*"):
            if candidate.is_symlink():
                raise RuntimeError("LAUNCHER_CONFIG_INVALID")
            if (
                candidate.is_file()
                and "__pycache__" not in candidate.parts
                and not any(part.endswith(".egg-info") for part in candidate.parts)
            ):
                candidates.add(candidate.relative_to(root))
    candidates.update(relative for relative in fixed if (root / relative).is_file())
    required = {
        Path("tools/tool-hub/src/tool_hub/app.py"),
        Path("tools/tool-hub/src/tool_hub/windows_launcher_entry.pyw"),
    }
    if not required.issubset(candidates):
        raise RuntimeError("LAUNCHER_CONFIG_INVALID")
    digest = hashlib.sha256()
    total = 0
    for relative in sorted(candidates, key=lambda item: item.as_posix()):
        candidate = root / relative
        _regular(candidate, max_bytes=16 * 1024 * 1024)
        raw = candidate.read_bytes()
        total += len(raw)
        if total > 128 * 1024 * 1024:
            raise RuntimeError("LAUNCHER_CONFIG_INVALID")
        digest.update(relative.as_posix().encode("utf-8") + b"\0" + raw)
    return digest.hexdigest()


def _validated_config(config_path: Path, launcher_path: Path) -> dict[str, object]:
    try:
        _regular(config_path, max_bytes=64 * 1024)
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1 or not _REQUIRED.issubset(payload):
            raise RuntimeError("LAUNCHER_CONFIG_INVALID")
        if payload["port"] != 8764:
            raise RuntimeError("LAUNCHER_CONFIG_INVALID")
        root = Path(str(payload["base_root"])).absolute()
        project_config = Path(str(payload["project_config"])).absolute()
        pythonw = Path(str(payload["pythonw"])).absolute()
        git = Path(str(payload["git_executable"])).absolute()
        for path in (pythonw, git, launcher_path):
            _regular(path, max_bytes=128 * 1024 * 1024)
        if (
            _root_fingerprint(root) != payload["root_fingerprint"]
            or _project_config_fingerprint(project_config) != payload["project_config_fingerprint"]
            or _sha256(pythonw) != payload["pythonw_sha256"]
            or _sha256(git) != payload["git_sha256"]
            or _sha256(launcher_path) != payload["launcher_sha256"]
        ):
            raise RuntimeError("LAUNCHER_UPDATE_REQUIRED")
        payload["_runtime_update_required"] = (
            _hub_runtime_fingerprint(root) != payload["hub_runtime_fingerprint"]
        )
        return payload
    except RuntimeError:
        raise
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise RuntimeError("LAUNCHER_CONFIG_INVALID") from error


def _show_error(reason: str) -> None:
    code = reason if _REASON.fullmatch(reason) else "LAUNCHER_START_FAILED"
    log_folder = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "BaseToolHub" / "logs"
    try:
        log_folder.mkdir(parents=True, exist_ok=True)
        (log_folder / "bootstrap-error.log").write_text(code + "\n", encoding="utf-8")
    except OSError:
        pass
    message = f"Base Tool Hub를 시작하지 못했습니다.\n오류 코드: {code}\n진단 폴더: {log_folder}"
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "Base Tool Hub", 0x10)
    except Exception:
        pass


def main() -> int:
    config_path = Path(os.environ["LOCALAPPDATA"]) / "BaseToolHub" / "launcher" / "launcher-config.json"
    try:
        payload = _validated_config(config_path, Path(__file__).absolute())
        repair_required = bool(payload.pop("_runtime_update_required", False))
        mode = "--repair-config" if repair_required else "--config"
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        process = subprocess.Popen(
            [str(payload["pythonw"]), "-m", "tool_hub.windows_launcher", mode, str(config_path)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=flags,
        )
        try:
            return_code = process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.terminate()
            _show_error("LAUNCHER_CHILD_TIMEOUT")
            return 1
        if return_code != 0:
            _show_error("LAUNCHER_CHILD_FAILED")
            return 1
        return 0
    except Exception as error:
        _show_error(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
