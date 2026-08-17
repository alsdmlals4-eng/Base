"""Per-user Windows desktop launcher installer and no-console runtime."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import subprocess
import tempfile
import time
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import webbrowser

from base_tool_contracts.trusted_files import trusted_git_executable


class LauncherError(RuntimeError):
    pass


_REASON = re.compile(r"^[A-Z0-9_]{1,80}$")


@dataclass(frozen=True)
class LauncherInstallation:
    state: str
    desktop_entry: str = "Base Tool Hub.lnk"

    def public_view(self) -> dict[str, str]:
        return {"state": self.state, "desktop_entry": self.desktop_entry}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _root_fingerprint(root: Path) -> str:
    metadata = root.stat()
    return hashlib.sha256(f"{root.absolute()}:{metadata.st_dev}:{metadata.st_ino}".encode()).hexdigest()


def project_config_fingerprint(path: Path) -> str:
    normalized = os.path.normcase(os.path.abspath(path))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    temporary = Path(raw)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        try:
            path.chmod(0o600)
        except OSError:
            pass
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _assert_plain_parents(path: Path) -> None:
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for parent in reversed(path.absolute().parents):
        try:
            metadata = parent.lstat()
        except OSError as error:
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID") from error
        if stat.S_ISLNK(metadata.st_mode) or (
            reparse and getattr(metadata, "st_file_attributes", 0) & reparse
        ):
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID")


def hub_runtime_fingerprint(root: Path) -> str:
    root = Path(root).absolute()
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
    candidates: set[Path] = set()
    for relative_root in relative_roots:
        directory = root / relative_root
        if not directory.is_dir() or directory.is_symlink():
            continue
        for candidate in directory.rglob("*"):
            if candidate.is_symlink():
                raise LauncherError("LAUNCHER_INSTALLATION_INVALID")
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
        raise LauncherError("LAUNCHER_INSTALLATION_INVALID")
    digest = hashlib.sha256()
    total = 0
    for relative in sorted(candidates, key=lambda item: item.as_posix()):
        candidate = root / relative
        _assert_plain_parents(candidate)
        metadata = candidate.lstat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 16 * 1024 * 1024:
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID")
        raw = candidate.read_bytes()
        total += len(raw)
        if total > 128 * 1024 * 1024:
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID")
        digest.update(relative.as_posix().encode("utf-8") + b"\0" + raw)
    return digest.hexdigest()


ShortcutBuilder = Callable[[Path, Path, Path], bytes]


def _write_windows_shell_link(
    destination: Path,
    target: Path,
    arguments: str,
    working_directory: Path,
) -> None:
    """Create one Shell Link through the in-process Windows COM contract."""
    if os.name != "nt":
        raise LauncherError("BLOCKED_PLATFORM")
    import ctypes
    import uuid
    from ctypes import wintypes

    class GUID(ctypes.Structure):
        _fields_ = (
            ("Data1", ctypes.c_uint32),
            ("Data2", ctypes.c_uint16),
            ("Data3", ctypes.c_uint16),
            ("Data4", ctypes.c_ubyte * 8),
        )

    def guid(value: str) -> GUID:
        return GUID.from_buffer_copy(uuid.UUID(value).bytes_le)

    def failed(result: int) -> bool:
        return result < 0

    def invoke(interface, index: int, result_type, argument_types, *values):
        table = ctypes.cast(
            interface,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p)),
        ).contents
        method = ctypes.WINFUNCTYPE(
            result_type,
            ctypes.c_void_p,
            *argument_types,
        )(table[index])
        return method(interface, *values)

    ole32 = ctypes.OleDLL("ole32")
    ole32.CoInitializeEx.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
    ole32.CoInitializeEx.restype = ctypes.c_long
    ole32.CoUninitialize.argtypes = ()
    ole32.CoUninitialize.restype = None
    ole32.CoCreateInstance.argtypes = (
        ctypes.POINTER(GUID),
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.POINTER(GUID),
        ctypes.POINTER(ctypes.c_void_p),
    )
    ole32.CoCreateInstance.restype = ctypes.c_long

    initialized = False
    shell_link = ctypes.c_void_p()
    persist_file = ctypes.c_void_p()
    try:
        initialization = ole32.CoInitializeEx(None, 2)
        if initialization in (0, 1):
            initialized = True
        elif ctypes.c_uint32(initialization).value != 0x80010106:
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")

        clsid_shell_link = guid("00021401-0000-0000-C000-000000000046")
        iid_shell_link = guid("000214F9-0000-0000-C000-000000000046")
        created = ole32.CoCreateInstance(
            ctypes.byref(clsid_shell_link),
            None,
            1,
            ctypes.byref(iid_shell_link),
            ctypes.byref(shell_link),
        )
        if failed(created) or not shell_link.value:
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")

        setters = (
            (20, (ctypes.c_wchar_p,), str(target)),
            (11, (ctypes.c_wchar_p,), arguments),
            (9, (ctypes.c_wchar_p,), str(working_directory)),
            (7, (ctypes.c_wchar_p,), "Base Tool Hub"),
            (15, (ctypes.c_int,), 7),
        )
        for index, argument_types, value in setters:
            if failed(invoke(shell_link, index, ctypes.c_long, argument_types, value)):
                raise LauncherError("LAUNCHER_SHORTCUT_FAILED")

        iid_persist_file = guid("0000010B-0000-0000-C000-000000000046")
        queried = invoke(
            shell_link,
            0,
            ctypes.c_long,
            (ctypes.POINTER(GUID), ctypes.POINTER(ctypes.c_void_p)),
            ctypes.byref(iid_persist_file),
            ctypes.byref(persist_file),
        )
        if failed(queried) or not persist_file.value:
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")
        saved = invoke(
            persist_file,
            6,
            ctypes.c_long,
            (ctypes.c_wchar_p, wintypes.BOOL),
            str(destination),
            True,
        )
        if failed(saved):
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")
    except (OSError, TypeError, ValueError) as error:
        raise LauncherError("LAUNCHER_SHORTCUT_FAILED") from error
    finally:
        if persist_file.value:
            invoke(persist_file, 2, ctypes.c_ulong, ())
        if shell_link.value:
            invoke(shell_link, 2, ctypes.c_ulong, ())
        if initialized:
            ole32.CoUninitialize()


def _default_shortcut_builder(pythonw: Path, launcher: Path, working: Path) -> bytes:
    """Build a direct per-user .lnk with the native Windows Shell Link owner."""
    if os.name != "nt":
        raise LauncherError("BLOCKED_PLATFORM")
    working.mkdir(parents=True, exist_ok=True)
    temporary = working / f".desktop-{secrets.token_hex(12)}.lnk"
    try:
        _write_windows_shell_link(
            temporary,
            pythonw,
            f'"{launcher}"',
            working,
        )
        shortcut_metadata = temporary.lstat()
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if (
            not stat.S_ISREG(shortcut_metadata.st_mode)
            or stat.S_ISLNK(shortcut_metadata.st_mode)
            or (reparse and getattr(shortcut_metadata, "st_file_attributes", 0) & reparse)
            or shortcut_metadata.st_size > 1024 * 1024
        ):
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")
        shortcut = temporary.read_bytes()
        if not shortcut or len(shortcut) > 1024 * 1024:
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")
        return shortcut
    except OSError as error:
        raise LauncherError("LAUNCHER_SHORTCUT_FAILED") from error
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _default_desktop(platform: str) -> Path:
    if platform != "win32":
        return Path.home() / "Desktop"
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, "Desktop")
        return Path(os.path.expandvars(str(value)))
    except (OSError, ImportError):
        one_drive = os.environ.get("OneDrive")
        return Path(one_drive) / "Desktop" if one_drive else Path.home() / "Desktop"


class WindowsLauncherInstaller:
    def __init__(
        self,
        base_root: Path,
        project_config: Path,
        *,
        local_app_data: Path | None = None,
        desktop: Path | None = None,
        platform: str | None = None,
        shortcut_builder: ShortcutBuilder = _default_shortcut_builder,
        git_executable: Path | None = None,
    ) -> None:
        self.base_root = Path(base_root).absolute()
        self.project_config = Path(project_config).absolute()
        self.platform = platform or ("win32" if os.name == "nt" else os.name)
        local_value = local_app_data or Path(os.environ.get("LOCALAPPDATA", ""))
        self.local_app_data = Path(local_value).absolute()
        self.desktop = Path(desktop or _default_desktop(self.platform)).absolute()
        self.shortcut_builder = shortcut_builder
        self.git_executable = Path(git_executable).absolute() if git_executable else None
        self.launcher_root = self.local_app_data / "BaseToolHub" / "launcher"
        self.config_path = self.launcher_root / "launcher-config.json"
        self.launcher_path = self.launcher_root / "Base Tool Hub.pyw"
        self.desktop_entry = self.desktop / "Base Tool Hub.lnk"
        self.legacy_desktop_entry = self.desktop / "Base Tool Hub.pyw"

    @property
    def pythonw(self) -> Path:
        return self.base_root / ".venv" / "Scripts" / "pythonw.exe"

    @property
    def template(self) -> Path:
        return self.base_root / "tools" / "tool-hub" / "src" / "tool_hub" / "windows_launcher_entry.pyw"

    def _regular(self, path: Path) -> None:
        _assert_plain_parents(path)
        try:
            metadata = path.lstat()
        except OSError as error:
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID") from error
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or stat.S_ISLNK(metadata.st_mode)
            or (reparse and getattr(metadata, "st_file_attributes", 0) & reparse)
        ):
            raise LauncherError("LAUNCHER_INSTALLATION_INVALID")

    def status(self) -> str:
        if self.platform != "win32":
            return "BLOCKED_PLATFORM"
        try:
            self.legacy_desktop_entry.lstat()
        except FileNotFoundError:
            pass
        except OSError:
            return "REPAIR_REQUIRED"
        else:
            return "REPAIR_REQUIRED"
        if not self.config_path.is_file() or not self.desktop_entry.is_file():
            return "NOT_INSTALLED"
        try:
            payload = _load_config(self.config_path)
            if _sha256(self.desktop_entry) != payload["desktop_entry_sha256"]:
                return "UPDATE_REQUIRED"
            return "INSTALLED"
        except LauncherError as error:
            if str(error) == "LAUNCHER_UPDATE_REQUIRED":
                return "UPDATE_REQUIRED"
            return "REPAIR_REQUIRED"
        except (OSError, ValueError):
            return "REPAIR_REQUIRED"

    def install(self) -> LauncherInstallation:
        if self.platform != "win32":
            raise LauncherError("BLOCKED_PLATFORM")
        git = self.git_executable or trusted_git_executable()
        for path in (self.pythonw, self.template, git):
            self._regular(path)
        self.desktop.mkdir(parents=True, exist_ok=True)
        self.launcher_root.mkdir(parents=True, exist_ok=True)
        template_bytes = self.template.read_bytes()
        legacy_present = False
        try:
            legacy_metadata = self.legacy_desktop_entry.lstat()
        except FileNotFoundError:
            pass
        except OSError as error:
            raise LauncherError("LAUNCHER_LEGACY_CONFLICT") from error
        else:
            reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
            if (
                not stat.S_ISREG(legacy_metadata.st_mode)
                or stat.S_ISLNK(legacy_metadata.st_mode)
                or (reparse and getattr(legacy_metadata, "st_file_attributes", 0) & reparse)
                or legacy_metadata.st_size > 1024 * 1024
                or self.legacy_desktop_entry.read_bytes() != template_bytes
            ):
                raise LauncherError("LAUNCHER_LEGACY_CONFLICT")
            legacy_present = True
        token = secrets.token_urlsafe(32)
        if self.config_path.is_file():
            try:
                previous = _load_config(self.config_path)
                if previous["project_config_fingerprint"] == project_config_fingerprint(
                    self.project_config
                ):
                    token = str(previous["launcher_token"])
            except (LauncherError, OSError, ValueError):
                pass
        _atomic_write(self.launcher_path, template_bytes)
        shortcut_bytes = self.shortcut_builder(
            self.pythonw,
            self.launcher_path,
            self.launcher_root,
        )
        if not shortcut_bytes or len(shortcut_bytes) > 1024 * 1024:
            raise LauncherError("LAUNCHER_SHORTCUT_FAILED")
        payload = {
            "schema_version": 1,
            "base_root": str(self.base_root),
            "project_config": str(self.project_config),
            "project_config_fingerprint": project_config_fingerprint(self.project_config),
            "pythonw": str(self.pythonw),
            "port": 8764,
            "root_fingerprint": _root_fingerprint(self.base_root),
            "pythonw_sha256": _sha256(self.pythonw),
            "git_executable": str(git),
            "git_sha256": _sha256(git),
            "hub_runtime_fingerprint": hub_runtime_fingerprint(self.base_root),
            "launcher_sha256": hashlib.sha256(template_bytes).hexdigest(),
            "desktop_entry_sha256": hashlib.sha256(shortcut_bytes).hexdigest(),
            "launcher_token": token,
        }
        _atomic_write(self.config_path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode())
        _atomic_write(self.desktop_entry, shortcut_bytes)
        if legacy_present:
            try:
                self.legacy_desktop_entry.unlink()
            except OSError as error:
                raise LauncherError("LAUNCHER_LEGACY_CONFLICT") from error
        return LauncherInstallation("INSTALLED")


def _load_config(path: Path) -> dict[str, object]:
    try:
        if path.is_symlink() or path.stat().st_size > 64 * 1024:
            raise LauncherError("LAUNCHER_CONFIG_INVALID")
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LauncherError("LAUNCHER_CONFIG_INVALID") from error
    required = {"base_root", "project_config", "project_config_fingerprint", "pythonw", "git_executable", "port", "root_fingerprint", "pythonw_sha256", "git_sha256", "launcher_sha256", "desktop_entry_sha256", "launcher_token", "hub_runtime_fingerprint"}
    if payload.get("schema_version") != 1 or not required.issubset(payload):
        raise LauncherError("LAUNCHER_CONFIG_INVALID")
    if payload["port"] != 8764:
        raise LauncherError("LAUNCHER_CONFIG_INVALID")
    root = Path(str(payload["base_root"])).absolute()
    project_config = Path(str(payload["project_config"])).absolute()
    pythonw = Path(str(payload["pythonw"])).absolute()
    git = Path(str(payload["git_executable"])).absolute()
    installed_launcher = path.parent / "Base Tool Hub.pyw"
    if (
        _root_fingerprint(root) != payload["root_fingerprint"]
        or project_config_fingerprint(project_config) != payload["project_config_fingerprint"]
        or _sha256(pythonw) != payload["pythonw_sha256"]
        or _sha256(git) != payload["git_sha256"]
        or _sha256(installed_launcher) != payload["launcher_sha256"]
        or hub_runtime_fingerprint(root) != payload["hub_runtime_fingerprint"]
    ):
        raise LauncherError("LAUNCHER_UPDATE_REQUIRED")
    return payload


def _probe(payload: dict[str, object]) -> bool | None:
    request = Request(
        f"http://127.0.0.1:{payload['port']}/api/launcher-status",
        headers={"X-Hub-Launcher-Token": str(payload["launcher_token"])},
    )
    try:
        with urlopen(request, timeout=0.7) as response:
            status = json.load(response)
    except HTTPError:
        return None
    except URLError:
        return False
    except (OSError, json.JSONDecodeError):
        return None
    return bool(
        status.get("tool_id") == "base-tool-hub"
        and status.get("root_fingerprint") == payload["root_fingerprint"]
        and status.get("project_config_fingerprint") == payload["project_config_fingerprint"]
        and status.get("hub_runtime_fingerprint") == payload["hub_runtime_fingerprint"]
        and status.get("port") == payload["port"]
    ) or None


def _try_acquire_launcher_lock(path: Path) -> int | None:
    descriptor = os.open(
        path,
        os.O_RDWR | os.O_CREAT | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    try:
        if os.fstat(descriptor).st_size == 0:
            os.write(descriptor, b"0")
            os.fsync(descriptor)
        os.lseek(descriptor, 0, os.SEEK_SET)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return descriptor
    except (ImportError, OSError):
        os.close(descriptor)
        return None


def _release_launcher_lock(descriptor: int) -> None:
    try:
        os.lseek(descriptor, 0, os.SEEK_SET)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_UN)
    finally:
        os.close(descriptor)


def _spawn(payload: dict[str, object]) -> subprocess.Popen[bytes]:
    environment = {
        "PATH": os.pathsep.join(
            (
                str(Path(str(payload["pythonw"])).parent),
                str(Path(str(payload["git_executable"])).parent),
            )
        ),
        "PYTHONUTF8": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "BASE_TOOL_HUB_LAUNCHER_TOKEN": str(payload["launcher_token"]),
    }
    for name in (
        "SYSTEMROOT",
        "WINDIR",
        "ProgramFiles",
        "ProgramFiles(x86)",
        "LOCALAPPDATA",
        "USERPROFILE",
        "TEMP",
        "TMP",
    ):
        if value := os.environ.get(name):
            environment[name] = value
    flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        [
            str(payload["pythonw"]), "-m", "tool_hub.app",
            "--base-root", str(payload["base_root"]),
            "--project-config", str(payload["project_config"]),
            "--port", str(payload["port"]),
        ],
        cwd=str(payload["base_root"]),
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        creationflags=flags,
    )
    return process


def run_installed_launcher(
    config_path: Path,
    *,
    probe: Callable[[dict[str, object]], bool | None] = _probe,
    spawn: Callable[[dict[str, object]], None] = _spawn,
    open_browser: Callable[[str], object] = webbrowser.open,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    config_path = Path(config_path)
    payload = _load_config(config_path)
    health = probe(payload)
    if health is None:
        raise LauncherError("PORT_IDENTITY_CONFLICT")
    if health is True:
        open_browser(f"http://127.0.0.1:{payload['port']}")
        return 0

    lock_path = config_path.parent / ".launcher.lock"
    lock_descriptor: int | None = None
    try:
        lock_descriptor = _try_acquire_launcher_lock(lock_path)
        if lock_descriptor is None:
            for _ in range(100):
                sleep(0.1)
                health = probe(payload)
                if health is True:
                    open_browser(f"http://127.0.0.1:{payload['port']}")
                    return 0
                if health is None:
                    raise LauncherError("PORT_IDENTITY_CONFLICT")
            raise LauncherError("LAUNCHER_BUSY")

        health = probe(payload)
        if health is None:
            raise LauncherError("PORT_IDENTITY_CONFLICT")
        process = spawn(payload) if health is False else None
        for _ in range(100):
            sleep(0.1)
            if process is not None and hasattr(process, "poll") and process.poll() is not None:
                raise LauncherError("HUB_START_FAILED")
            health = probe(payload)
            if health is True:
                break
            if health is None:
                raise LauncherError("PORT_IDENTITY_CONFLICT")
        else:
            raise LauncherError("HUB_START_TIMEOUT")
        open_browser(f"http://127.0.0.1:{payload['port']}")
        return 0
    finally:
        if lock_descriptor is not None:
            _release_launcher_lock(lock_descriptor)


def _show_native_error(message: str) -> None:
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "Base Tool Hub", 0x10)
    except Exception:
        pass


def _report_launcher_error(error: Exception) -> str:
    raw = str(error)
    reason = raw if _REASON.fullmatch(raw) else "LAUNCHER_START_FAILED"
    logs = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "BaseToolHub" / "logs"
    diagnostic = logs / "launcher-error.log"
    try:
        _atomic_write(diagnostic, (reason + "\n").encode("utf-8"))
    except OSError:
        pass
    return f"Base Tool Hub를 시작하지 못했습니다.\n오류 코드: {reason}\n진단 폴더: {logs}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return run_installed_launcher(args.config)
    except Exception as error:
        _show_native_error(_report_launcher_error(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
