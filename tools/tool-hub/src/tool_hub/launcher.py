"""Typed launcher for the first Tool Hub vertical slice."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
from typing import Any
from urllib.request import urlopen

from .projects import ProjectBinding


class LaunchError(RuntimeError):
    pass


@dataclass(frozen=True)
class ChildIdentity:
    tool_id: str
    project_id: str
    port: int
    process_id: int
    launch_nonce: str
    url: str
    status: dict[str, Any]
    state: str = "RUNNING"

    def public_view(self) -> dict[str, object]:
        return {
            "tool_id": self.tool_id,
            "project_id": self.project_id,
            "url": self.url,
            "status": self.state,
        }


@dataclass(frozen=True)
class ChildPublicView:
    tool_id: str
    project_id: str
    status: str
    url: str | None = None
    log_tail: str = ""

    def public_view(self) -> dict[str, object]:
        value: dict[str, object] = {
            "tool_id": self.tool_id,
            "project_id": self.project_id,
            "status": self.status,
        }
        if self.url is not None:
            value["url"] = self.url
        if self.log_tail:
            value["log_tail"] = self.log_tail
        return value


class QaEvidenceLauncher:
    def __init__(self, runtime_root: Path, *, python_executable: Path | None = None) -> None:
        self.runtime_root = runtime_root
        self.python_executable = python_executable or Path(sys.executable)
        self._children: dict[tuple[str, str], tuple[subprocess.Popen[bytes], ChildIdentity]] = {}

    def child_environment(self) -> dict[str, str]:
        allowed: dict[str, str] = {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        for name in ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "LANG", "LC_ALL"):
            value = os.environ.get(name)
            if value:
                allowed[name] = value
        return allowed

    def _read_status(self, identity: dict[str, Any], process: subprocess.Popen[bytes]) -> dict[str, Any]:
        url = f"http://127.0.0.1:{identity['port']}/api/status"
        deadline = time.monotonic() + 10
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise LaunchError("QA child exited before authenticated health confirmation")
            try:
                with urlopen(url, timeout=0.5) as response:
                    payload = json.loads(response.read())
                if isinstance(payload, dict):
                    return payload
            except Exception as error:  # bounded retry around a local startup race
                last_error = error
                time.sleep(0.05)
        raise LaunchError("QA child did not become healthy before timeout") from last_error

    def start(self, binding: ProjectBinding) -> ChildIdentity:
        key = ("qa-evidence-studio", binding.project_id)
        existing = self._children.get(key)
        if existing and existing[0].poll() is None:
            return existing[1]
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        nonce = secrets.token_urlsafe(32)
        startup_file = self.runtime_root / f"qa-{binding.project_id}-{secrets.token_hex(8)}.json"
        command = [
            str(self.python_executable),
            "-m",
            "qa_evidence_studio.app",
            "--project-root",
            str(binding.root),
            "--project-id",
            binding.project_id,
            "--port",
            "0",
            "--launch-nonce",
            nonce,
            "--startup-file",
            str(startup_file),
        ]
        process = subprocess.Popen(
            command,
            shell=False,
            env=self.child_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not startup_file.is_file():
                if process.poll() is not None:
                    raise LaunchError("QA child exited before startup identity report")
                time.sleep(0.05)
            if not startup_file.is_file():
                raise LaunchError("QA child did not publish startup identity")
            try:
                startup = json.loads(startup_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise LaunchError("QA child startup identity was malformed") from error
            expected = {
                "tool_id": "qa-evidence-studio",
                "project_id": binding.project_id,
                "launch_nonce": nonce,
                "process_id": process.pid,
            }
            if any(startup.get(name) != value for name, value in expected.items()):
                raise LaunchError("QA child startup identity did not match the requested binding")
            port = startup.get("port")
            if not isinstance(port, int) or not 0 < port < 65536:
                raise LaunchError("QA child reported an invalid loopback port")
            status = self._read_status(startup, process)
            if any(status.get(name) != value for name, value in expected.items()):
                raise LaunchError("QA child health identity did not match the startup report")
            if status.get("root_fingerprint") is None or status.get("status") != "ready":
                raise LaunchError("QA child health contract is incomplete")
            identity = ChildIdentity(
                "qa-evidence-studio",
                binding.project_id,
                port,
                process.pid,
                nonce,
                f"http://127.0.0.1:{port}",
                status,
            )
            self._children[key] = (process, identity)
            return identity
        except Exception:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            raise
        finally:
            try:
                startup_file.unlink()
            except FileNotFoundError:
                pass

    def stop_all(self) -> None:
        for process, _ in self._children.values():
            if process.poll() is None:
                process.terminate()
        for process, _ in self._children.values():
            if process.poll() is None:
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
        self._children.clear()
