"""Project-bound process supervision for reviewed Tool Hub children."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import signal
import socket
import stat
import subprocess
import tempfile
import threading
import time
from typing import Any, Callable, Iterable, Iterator
from urllib.request import urlopen

from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry, ProjectFigmaRegistry
from base_tool_contracts.trusted_files import TrustedFileError, read_regular_portable_nofollow

from .adapters import AdapterError, LaunchSpec, bind_launch_spec, build_launch_spec
from .environment import EnvironmentError, LaunchContext, ensure_runtime_directory
from .launcher import ChildIdentity, ChildPublicView, LaunchError
from .projects import ProjectBinding, ProjectBindingError, ProjectLocator
from .windows_process_owner import (
    CREATE_NO_WINDOW,
    CREATE_SUSPENDED,
    WindowsJobOwner,
    WindowsOwnershipError,
)


_POSIX_PROCESS_GROUPS = os.name == "posix" and hasattr(os, "killpg")
_WINDOWS_JOB_OBJECTS = os.name == "nt"
_PUBLIC_STATES = frozenset(
    {
        "REGISTERED",
        "PREFLIGHT",
        "STARTING",
        "RUNNING",
        "UNHEALTHY",
        "STOPPING",
        "STOPPED",
        "START_FAILED",
        "BLOCKED_TOOL",
        "BLOCKED_PROJECT",
        "BLOCKED_CONFIGURATION",
        "BLOCKED_PLATFORM",
        "BLOCKED_MACHINE_OWNERSHIP",
    }
)
_MAX_STATUS_BYTES = 64 * 1024
_MAX_LOG_TAIL_BYTES = 4096
_MAX_PUBLIC_LOG_CHARS = 1024
_MAX_LOG_FILE_BYTES = 64 * 1024
_MAX_RETAINED_PUBLIC_STATES = 256


def default_machine_lock_address() -> tuple[str, int]:
    """Return one loopback ownership endpoint shared by every OS user."""
    return ("127.0.0.1", 47640)


@dataclass
class _Child:
    process: subprocess.Popen[bytes]
    process_group_id: int
    identity: ChildIdentity
    spec: LaunchSpec
    launch_dir: Path
    log_path: Path
    project_root: Path
    log_tail: bytearray
    log_lock: threading.Lock
    log_thread: threading.Thread | None = None
    state: str = "RUNNING"
    windows_owner: WindowsJobOwner | None = None


@dataclass
class _KeyLock:
    lock: threading.Lock
    users: int = 0


class ProcessSupervisor:
    """Own one authenticated process tree for each reviewed tool/project key."""

    def __init__(
        self,
        runtime_root: Path,
        base_root: Path,
        locator: ProjectLocator,
        tools: Iterable[dict[str, object]],
        *,
        machine_lock_root: Path | None = None,
        python_executable: Path | None = None,
        spec_builder: Callable[[dict[str, object], ProjectBinding, LaunchContext], LaunchSpec] = build_launch_spec,
        spec_binder: Callable[[LaunchSpec], LaunchSpec] = bind_launch_spec,
        binding_resolver: Callable[[str, str], ProjectBinding] | None = None,
        startup_timeout: float = 10.0,
        health_timeout: float = 10.0,
        stop_timeout: float = 3.0,
        poll_interval: float = 0.05,
    ) -> None:
        self.runtime_root = Path(runtime_root).absolute()
        self.machine_lock_root = (
            Path(machine_lock_root).absolute() if machine_lock_root is not None else None
        )
        self.base_root = Path(base_root).absolute()
        self.locator = locator
        self.tools = {str(tool["tool_id"]): tool for tool in tools}
        default_python = (
            self.base_root / ".venv" / "Scripts" / "python.exe"
            if os.name == "nt"
            else self.base_root / ".venv" / "bin" / "python"
        )
        self.python_executable = Path(python_executable or default_python)
        self.spec_builder = spec_builder
        self.spec_binder = spec_binder
        self.binding_resolver = binding_resolver or self._binding
        self.startup_timeout = startup_timeout
        self.health_timeout = health_timeout
        self.stop_timeout = stop_timeout
        self.poll_interval = poll_interval
        self._children: dict[tuple[str, str], _Child] = {}
        self._states: dict[tuple[str, str], ChildPublicView] = {}
        self._locks: dict[tuple[str, str], _KeyLock] = {}
        self._locks_guard = threading.Lock()
        self._machine_lock_stream: Any | None = None
        self._machine_lock_socket: socket.socket | None = None
        self._machine_guard = threading.Lock()
        self._started_process_count = 0
        self._lifecycle = threading.Condition()
        self._closing = False
        self._in_flight_starts = 0

    @property
    def started_process_count(self) -> int:
        return self._started_process_count

    @contextmanager
    def _locked_key(self, key: tuple[str, str]) -> Iterator[None]:
        with self._locks_guard:
            entry = self._locks.setdefault(key, _KeyLock(threading.Lock()))
            entry.users += 1
        entry.lock.acquire()
        try:
            yield
        finally:
            entry.lock.release()
            with self._locks_guard:
                entry.users -= 1
                if entry.users == 0 and key not in self._children:
                    self._locks.pop(key, None)

    def _set_state(
        self,
        key: tuple[str, str],
        state: str,
        *,
        url: str | None = None,
        log_tail: str = "",
    ) -> ChildPublicView:
        if state not in _PUBLIC_STATES:
            raise RuntimeError("invalid supervisor state")
        view = ChildPublicView(key[0], key[1], state, url, log_tail)
        if key not in self._states and len(self._states) >= _MAX_RETAINED_PUBLIC_STATES:
            stale = next((candidate for candidate in self._states if candidate not in self._children), None)
            if stale is not None:
                self._states.pop(stale, None)
        self._states[key] = view
        return view

    def _acquire_machine_lock(self) -> None:
        with self._machine_guard:
            if self._machine_lock_stream is not None or self._machine_lock_socket is not None:
                return
            if os.name == "nt" or self.machine_lock_root is None:
                if os.sys.platform not in {"linux", "win32"}:
                    raise LaunchError("Tool Hub machine ownership is unavailable on this platform")
                owner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    owner.bind(default_machine_lock_address())
                    owner.listen(1)
                except OSError as error:
                    owner.close()
                    raise LaunchError("Tool Hub machine ownership is already held") from error
                self._machine_lock_socket = owner
                return
            runtime = ensure_runtime_directory(self.machine_lock_root)
            lock_path = runtime / "machine.lock"
            flags = os.O_RDWR | os.O_CREAT
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            try:
                descriptor = os.open(lock_path, flags, 0o600)
                os.fchmod(descriptor, 0o600)
                metadata = os.fstat(descriptor)
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.geteuid():
                    raise OSError("unsafe lock")
                stream = os.fdopen(descriptor, "r+b", closefd=True)
                if _POSIX_PROCESS_GROUPS:
                    import fcntl

                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._machine_lock_stream = stream
            except (BlockingIOError, OSError, EnvironmentError) as error:
                try:
                    stream.close()  # type: ignore[possibly-undefined]
                except (NameError, OSError):
                    pass
                raise LaunchError("Tool Hub machine ownership is already held") from error

    def _release_machine_lock(self) -> None:
        with self._machine_guard:
            stream = self._machine_lock_stream
            self._machine_lock_stream = None
            owner = self._machine_lock_socket
            self._machine_lock_socket = None
            if stream is not None:
                stream.close()
            if owner is not None:
                owner.close()

    @staticmethod
    def _drain_bounded_log(
        source: Any,
        descriptor: int,
        tail: bytearray,
        tail_lock: threading.Lock,
    ) -> None:
        try:
            with source, os.fdopen(descriptor, "r+b", buffering=0) as destination:
                while True:
                    chunk = source.read(8192)
                    if not chunk:
                        break
                    with tail_lock:
                        tail.extend(chunk)
                        if len(tail) > _MAX_LOG_FILE_BYTES:
                            del tail[:-_MAX_LOG_FILE_BYTES]
                        snapshot = bytes(tail)
                    destination.seek(0)
                    destination.write(snapshot)
                    destination.truncate()
        except OSError:
            pass

    def _binding(self, tool_id: str, project_id: str) -> ProjectBinding:
        binding = self.locator.resolve(project_id)
        if tool_id == "qa-evidence-studio":
            return binding
        figma = ProjectFigmaRegistry.load(
            self.base_root / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
        )
        try:
            anchors = ApprovedAnchorRegistry.load(
                binding.root / ApprovedAnchorRegistry.CANONICAL_RELATIVE_PATH
            )
        except AnchorEvidenceError as error:
            raise ProjectBindingError("PROJECT_ANCHOR_EVIDENCE_UNAVAILABLE") from error
        return self.locator.preflight_visual(project_id, figma, anchors)

    def _new_launch_directory(self, tool_id: str, project_id: str) -> Path:
        runtime = ensure_runtime_directory(self.runtime_root)
        path = Path(
            tempfile.mkdtemp(
                prefix=f"launch-{tool_id}-{project_id}-",
                dir=runtime,
            )
        )
        if os.name != "nt":
            os.chmod(path, 0o700)
        return path

    @staticmethod
    def _expected_for(tool_id: str, expected: dict[str, str], process_id: int) -> dict[str, object]:
        if tool_id == "qa-evidence-studio":
            return {
                "tool_id": expected["tool_id"],
                "project_id": expected["project_id"],
                "launch_nonce": expected["launch_nonce"],
                "process_id": process_id,
            }
        return {**expected, "process_id": process_id}

    @staticmethod
    def _matches(payload: dict[str, Any], expected: dict[str, object]) -> bool:
        return all(payload.get(name) == value for name, value in expected.items())

    def _read_startup(self, child: _Child, expected: dict[str, object]) -> dict[str, Any]:
        deadline = time.monotonic() + self.startup_timeout
        while time.monotonic() < deadline:
            if child.process.poll() is not None:
                raise LaunchError("child exited before startup identity report")
            if os.path.lexists(child.spec.startup_file):
                break
            time.sleep(self.poll_interval)
        else:
            raise LaunchError("child startup identity timeout")
        if os.name == "nt":
            try:
                raw, _ = read_regular_portable_nofollow(
                    child.spec.startup_file,
                    max_bytes=_MAX_STATUS_BYTES,
                )
                payload = json.loads(raw)
            except (TrustedFileError, ValueError, json.JSONDecodeError) as error:
                raise LaunchError("child startup identity was malformed") from error
        else:
            descriptor = -1
            try:
                descriptor = os.open(
                    child.spec.startup_file,
                    os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0),
                )
                metadata = os.fstat(descriptor)
                if (
                    not stat.S_ISREG(metadata.st_mode)
                    or metadata.st_uid != os.geteuid()
                    or metadata.st_size > _MAX_STATUS_BYTES
                ):
                    raise ValueError("unsafe")
                while metadata.st_nlink == 2 and time.monotonic() < deadline:
                    if child.process.poll() is not None:
                        raise LaunchError("child exited before startup identity report")
                    time.sleep(self.poll_interval)
                    metadata = os.fstat(descriptor)
                if metadata.st_nlink != 1:
                    raise ValueError("unsafe link count")
                raw = os.read(descriptor, _MAX_STATUS_BYTES + 1)
                if len(raw) > _MAX_STATUS_BYTES or len(raw) != metadata.st_size:
                    raise ValueError("oversized or changed")
                payload = json.loads(raw)
            except (OSError, ValueError, json.JSONDecodeError) as error:
                raise LaunchError("child startup identity was malformed") from error
            finally:
                if descriptor >= 0:
                    os.close(descriptor)
        if not isinstance(payload, dict) or not self._matches(payload, expected):
            raise LaunchError("child startup identity did not match the requested binding")
        port = payload.get("port")
        if not isinstance(port, int) or not 0 < port < 65536:
            raise LaunchError("child startup identity reported an invalid port")
        return payload

    def _fetch_status(self, child: _Child, *, timeout: float = 0.5) -> dict[str, Any]:
        path = str(self.tools[child.identity.tool_id].get("health_path", "/api/status"))
        if path != "/api/status":
            raise LaunchError("reviewed health path is invalid")
        with urlopen(f"http://127.0.0.1:{child.identity.port}{path}", timeout=timeout) as response:
            raw = response.read(_MAX_STATUS_BYTES + 1)
        if len(raw) > _MAX_STATUS_BYTES:
            raise LaunchError("child health response was oversized")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise LaunchError("child health response was malformed")
        return payload

    def _health_expected(self, child: _Child, expected: dict[str, object]) -> dict[str, object]:
        return expected

    def _wait_for_health(self, child: _Child, expected: dict[str, object]) -> dict[str, Any]:
        deadline = time.monotonic() + self.health_timeout
        last_error: Exception | None = None
        health_expected = self._health_expected(child, expected)
        while time.monotonic() < deadline:
            if child.process.poll() is not None:
                raise LaunchError("child exited before authenticated health confirmation")
            try:
                status = self._fetch_status(child)
                if not self._matches(status, health_expected) or status.get("status") != "ready":
                    raise LaunchError("child health identity did not match startup identity")
                if child.identity.tool_id == "qa-evidence-studio" and not status.get("root_fingerprint"):
                    raise LaunchError("child health contract was incomplete")
                return status
            except LaunchError:
                raise
            except Exception as error:
                last_error = error
                time.sleep(self.poll_interval)
        raise LaunchError("child authenticated health timeout") from last_error

    def _sanitized_log_tail(self, child: _Child) -> str:
        with child.log_lock:
            raw = bytes(child.log_tail[-_MAX_LOG_TAIL_BYTES:])
        value = raw.decode("utf-8", errors="replace")
        secrets_to_redact = [
            str(self.base_root),
            str(self.runtime_root),
            str(child.launch_dir),
            str(child.project_root),
            str(child.spec.expected_identity.get("launch_nonce", "")),
        ]
        for secret in sorted((item for item in secrets_to_redact if item), key=len, reverse=True):
            value = value.replace(secret, "<redacted>")
        value = re.sub(r"<redacted>(?:[/\\][^\r\n]*)?", "<redacted>", value)
        value = re.sub(r"(?<![:\w])/(?:[^\r\n\"']+)", "<path>", value)
        value = "".join(character if character in "\n\t" or character.isprintable() else "?" for character in value)
        return value[-_MAX_PUBLIC_LOG_CHARS:]

    @staticmethod
    def _group_exists(process_group_id: int) -> bool:
        try:
            os.killpg(process_group_id, 0)
            return True
        except ProcessLookupError:
            return False

    def _terminate_group(
        self,
        process: subprocess.Popen[bytes],
        process_group_id: int,
        windows_owner: WindowsJobOwner | None = None,
    ) -> None:
        if windows_owner is not None:
            try:
                windows_owner.terminate()
                try:
                    process.wait(timeout=self.stop_timeout)
                except subprocess.TimeoutExpired as error:
                    raise LaunchError("Windows child Job Object did not terminate") from error
            except WindowsOwnershipError as error:
                raise LaunchError("Windows child Job Object termination failed") from error
            finally:
                windows_owner.close()
            return
        if not _POSIX_PROCESS_GROUPS:
            raise LaunchError("process tree ownership is unavailable on this platform")
        try:
            os.killpg(process_group_id, signal.SIGTERM)
        except ProcessLookupError:
            process.poll()
            return
        deadline = time.monotonic() + self.stop_timeout
        while time.monotonic() < deadline and self._group_exists(process_group_id):
            process.poll()
            time.sleep(self.poll_interval)
        if self._group_exists(process_group_id):
            try:
                os.killpg(process_group_id, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if process.poll() is None:
            try:
                process.wait(timeout=self.stop_timeout)
            except subprocess.TimeoutExpired as error:
                raise LaunchError("child process group did not terminate") from error

    def _cleanup_failed_child(self, child: _Child) -> None:
        try:
            self._terminate_group(
                child.process,
                child.process_group_id,
                child.windows_owner,
            )
        finally:
            if child.log_thread is not None:
                child.log_thread.join(timeout=self.stop_timeout)
            try:
                child.spec.startup_file.unlink()
            except FileNotFoundError:
                pass

    def start(self, tool_id: str, project_id: str) -> ChildIdentity:
        if tool_id not in self.tools:
            raise LaunchError("tool is not registered")
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise LaunchError("project identity is invalid")
        with self._lifecycle:
            if self._closing:
                raise LaunchError("Tool Hub supervisor is closing")
            self._in_flight_starts += 1
        try:
            return self._start(tool_id, project_id)
        finally:
            with self._lifecycle:
                self._in_flight_starts -= 1
                self._lifecycle.notify_all()

    def _start(self, tool_id: str, project_id: str) -> ChildIdentity:
        key = (tool_id, project_id)
        with self._locked_key(key):
            tool = self.tools[tool_id]
            self._set_state(key, "REGISTERED")
            existing = self._children.get(key)
            if existing is not None:
                if existing.process.poll() is not None:
                    self._set_state(key, "UNHEALTHY", url=existing.identity.url)
                    raise LaunchError("child is unhealthy")
                try:
                    status = self._fetch_status(existing)
                except Exception as error:
                    self._set_state(key, "UNHEALTHY", url=existing.identity.url)
                    raise LaunchError("child is unhealthy") from error
                expected = self._expected_for(
                    tool_id, dict(existing.spec.expected_identity), existing.process.pid
                )
                if (
                    not self._matches(status, self._health_expected(existing, expected))
                    or status.get("status") != "ready"
                ):
                    self._set_state(key, "UNHEALTHY", url=existing.identity.url)
                    raise LaunchError("child is unhealthy")
                return existing.identity
            if not (_POSIX_PROCESS_GROUPS or _WINDOWS_JOB_OBJECTS):
                self._set_state(key, "BLOCKED_PLATFORM")
                raise LaunchError("process tree ownership is not implemented on this platform")
            try:
                self._acquire_machine_lock()
            except LaunchError:
                self._set_state(key, "BLOCKED_MACHINE_OWNERSHIP")
                raise
            self._set_state(key, "PREFLIGHT")
            try:
                binding = self.binding_resolver(tool_id, project_id)
            except ProjectBindingError as error:
                self._set_state(key, "BLOCKED_PROJECT")
                raise LaunchError(str(error)) from error
            except (AnchorEvidenceError, ValueError) as error:
                self._set_state(key, "BLOCKED_CONFIGURATION")
                raise LaunchError("visual project configuration is unavailable") from error
            launch_dir: Path | None = None
            child: _Child | None = None
            try:
                launch_dir = self._new_launch_directory(tool_id, project_id)
                context = LaunchContext(
                    self.base_root,
                    launch_dir,
                    self.python_executable,
                    secrets.token_urlsafe(32),
                )
                spec = self.spec_builder(tool, binding, context)
                if os.path.lexists(spec.startup_file):
                    raise LaunchError("child startup report path is already present")
                log_path = launch_dir / "child.log"
                log_descriptor = os.open(
                    log_path,
                    os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                )
                try:
                    bound_spec = self.spec_binder(spec)
                except Exception:
                    os.close(log_descriptor)
                    raise
                self._set_state(key, "STARTING")
                process: subprocess.Popen[bytes] | None = None
                windows_owner: WindowsJobOwner | None = None
                try:
                    if _WINDOWS_JOB_OBJECTS:
                        process = subprocess.Popen(
                            list(bound_spec.argv),
                            shell=False,
                            cwd=bound_spec.cwd,
                            env=dict(bound_spec.env),
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            close_fds=True,
                            creationflags=CREATE_SUSPENDED | CREATE_NO_WINDOW,
                        )
                        self._started_process_count += 1
                        windows_owner = WindowsJobOwner()
                        windows_owner.attach_and_resume(process.pid)
                    else:
                        process = subprocess.Popen(
                            list(bound_spec.argv),
                            shell=False,
                            cwd=bound_spec.cwd,
                            env=dict(bound_spec.env),
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            start_new_session=True,
                            pass_fds=bound_spec.pass_fds,
                        )
                        self._started_process_count += 1
                except Exception:
                    if windows_owner is not None:
                        try:
                            windows_owner.terminate()
                        except WindowsOwnershipError:
                            pass
                        windows_owner.close()
                    if process is not None and process.poll() is None:
                        try:
                            process.terminate()
                            process.wait(timeout=self.stop_timeout)
                        except (OSError, subprocess.TimeoutExpired):
                            pass
                    os.close(log_descriptor)
                    raise
                finally:
                    if not _WINDOWS_JOB_OBJECTS:
                        for descriptor in bound_spec.pass_fds:
                            os.close(descriptor)
                assert process is not None
                placeholder = ChildIdentity(
                    tool_id,
                    project_id,
                    1,
                    process.pid,
                    str(spec.expected_identity["launch_nonce"]),
                    "",
                    {},
                )
                log_tail = bytearray()
                log_lock = threading.Lock()
                child = _Child(
                    process,
                    process.pid,
                    placeholder,
                    spec,
                    launch_dir,
                    log_path,
                    binding.root,
                    log_tail,
                    log_lock,
                    log_thread=None,
                    state="STARTING",
                    windows_owner=windows_owner,
                )
                log_thread = threading.Thread(
                    target=self._drain_bounded_log,
                    args=(process.stdout, log_descriptor, log_tail, log_lock),
                    daemon=True,
                )
                child.log_thread = log_thread
                log_thread.start()
                expected = self._expected_for(tool_id, dict(spec.expected_identity), process.pid)
                startup = self._read_startup(child, expected)
                port = int(startup["port"])
                identity = ChildIdentity(
                    tool_id,
                    project_id,
                    port,
                    process.pid,
                    str(spec.expected_identity["launch_nonce"]),
                    f"http://127.0.0.1:{port}",
                    {},
                )
                child.identity = identity
                status = self._wait_for_health(child, expected)
                identity = ChildIdentity(
                    tool_id,
                    project_id,
                    port,
                    process.pid,
                    str(spec.expected_identity["launch_nonce"]),
                    f"http://127.0.0.1:{port}",
                    status,
                )
                child.identity = identity
                child.state = "RUNNING"
                self._children[key] = child
                self._set_state(key, "RUNNING", url=identity.url)
                return identity
            except (AdapterError, EnvironmentError) as error:
                if launch_dir is not None:
                    shutil.rmtree(launch_dir, ignore_errors=True)
                self._set_state(key, "BLOCKED_CONFIGURATION")
                raise LaunchError("reviewed launch configuration is unavailable") from error
            except Exception as error:
                if child is not None:
                    self._cleanup_failed_child(child)
                tail = self._sanitized_log_tail(child) if child is not None else ""
                self._set_state(key, "START_FAILED", log_tail=tail)
                if isinstance(error, LaunchError):
                    message = str(error)
                else:
                    message = "child start failed"
                if tail:
                    message = f"{message}: {tail}"
                if launch_dir is not None:
                    shutil.rmtree(launch_dir, ignore_errors=True)
                raise LaunchError(message) from error

    def view(self, tool_id: str, project_id: str) -> ChildPublicView:
        if tool_id not in self.tools:
            return ChildPublicView(tool_id, project_id, "BLOCKED_TOOL")
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            return ChildPublicView(tool_id, project_id, "BLOCKED_PROJECT")
        key = (tool_id, project_id)
        child = self._children.get(key)
        if child is not None and child.process.poll() is not None and child.state == "RUNNING":
            child.state = "UNHEALTHY"
            return self._set_state(
                key,
                "UNHEALTHY",
                url=child.identity.url,
                log_tail=self._sanitized_log_tail(child),
            )
        return self._states.get(key, ChildPublicView(tool_id, project_id, "REGISTERED"))

    def stop(self, tool_id: str, project_id: str) -> ChildPublicView:
        if tool_id not in self.tools:
            raise LaunchError("tool is not registered")
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise LaunchError("project identity is invalid")
        key = (tool_id, project_id)
        with self._locked_key(key):
            child = self._children.get(key)
            if child is None:
                return self._set_state(key, "STOPPED")
            if child.process.poll() is not None:
                child.state = "UNHEALTHY"
                self._terminate_group(
                    child.process,
                    child.process_group_id,
                    child.windows_owner,
                )
                self._children.pop(key, None)
                view = self._set_state(key, "UNHEALTHY", log_tail=self._sanitized_log_tail(child))
                shutil.rmtree(child.launch_dir, ignore_errors=True)
                return view
            expected = self._expected_for(tool_id, dict(child.spec.expected_identity), child.process.pid)
            try:
                status = self._fetch_status(child)
            except Exception as error:
                self._set_state(key, "UNHEALTHY", url=child.identity.url)
                raise LaunchError("child stop ownership could not be authenticated") from error
            if not self._matches(status, self._health_expected(child, expected)):
                self._set_state(key, "UNHEALTHY", url=child.identity.url)
                raise LaunchError("child stop ownership did not match")
            self._set_state(key, "STOPPING", url=child.identity.url)
            self._terminate_group(
                child.process,
                child.process_group_id,
                child.windows_owner,
            )
            if child.log_thread is not None:
                child.log_thread.join(timeout=self.stop_timeout)
            child.state = "STOPPED"
            self._children.pop(key, None)
            shutil.rmtree(child.launch_dir, ignore_errors=True)
            return self._set_state(key, "STOPPED")

    def stop_all(self) -> None:
        with self._lifecycle:
            self._closing = True
            while self._in_flight_starts:
                self._lifecycle.wait()
        failures: list[LaunchError] = []
        for tool_id, project_id in list(self._children):
            try:
                self.stop(tool_id, project_id)
            except LaunchError as error:
                failures.append(error)
        if not self._children:
            self._release_machine_lock()
        if failures:
            raise LaunchError("Tool Hub could not stop all authenticated children") from failures[0]
