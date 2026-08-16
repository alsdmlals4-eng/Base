from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time

import pytest

from tool_hub.adapters import LaunchSpec
from tool_hub.projects import ProjectBinding
from tool_hub.supervisor import ProcessSupervisor


pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows process ownership contract")


CHILD = r'''
import json, os, subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
startup, tool_id, project_id, nonce, adapter, fingerprint = sys.argv[1:]
identity = {
    "tool_id": tool_id,
    "project_id": project_id,
    "process_id": os.getpid(),
    "launch_nonce": nonce,
    "adapter_sha256": adapter,
    "root_fingerprint": fingerprint,
}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {**identity, "status": "ready"}
        encoded = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
identity["port"] = server.server_address[1]
descendant = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(60)"])
with open(startup + ".descendant", "x", encoding="utf-8") as stream:
    stream.write(str(descendant.pid))
with open(startup, "x", encoding="utf-8") as stream:
    json.dump(identity, stream)
server.serve_forever()
'''


TOOLS = (
    {
        "tool_id": "expression-studio",
        "health_path": "/api/status",
        "owner_path": "unused",
        "launch_adapter": "unused",
        "capabilities": [],
    },
)


class Specs:
    def __call__(self, tool, project, context) -> LaunchSpec:
        startup = context.runtime_root / "startup.json"
        expected = {
            "tool_id": str(tool["tool_id"]),
            "project_id": project.project_id,
            "launch_nonce": context.launch_nonce,
            "adapter_sha256": project.adapter_sha256,
            "root_fingerprint": project.fingerprint,
        }
        argv = (
            sys.executable,
            "-I",
            "-c",
            CHILD,
            str(startup),
            str(tool["tool_id"]),
            project.project_id,
            context.launch_nonce,
            project.adapter_sha256,
            project.fingerprint,
        )
        return LaunchSpec(argv, context.runtime_root, dict(os.environ), startup, expected)


def binding(root: Path, project_id: str) -> ProjectBinding:
    return ProjectBinding(
        project_id,
        root,
        f"owner/{project_id}",
        "Godot 4.7",
        "a" * 64,
        "b" * 64,
    )


def process_alive(pid: int) -> bool:
    import ctypes
    from ctypes import wintypes

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return False
    try:
        code = wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
            return False
        return code.value == STILL_ACTIVE
    finally:
        kernel32.CloseHandle(handle)


def wait_gone(pid: int, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not process_alive(pid):
            return
        time.sleep(0.05)
    raise AssertionError(f"process {pid} remained alive")


def test_windows_supervisor_owns_and_stops_descendant_tree(tmp_path: Path) -> None:
    owner = ProcessSupervisor(
        tmp_path / "runtime",
        tmp_path,
        locator=None,  # binding_resolver owns the test binding
        tools=TOOLS,
        python_executable=Path(sys.executable),
        spec_builder=Specs(),
        spec_binder=lambda spec: spec,
        binding_resolver=lambda tool_id, project_id: binding(tmp_path, project_id),
        startup_timeout=5.0,
        health_timeout=5.0,
        stop_timeout=2.0,
        poll_interval=0.02,
    )
    child = None
    descendant_pid = None
    try:
        child = owner.start("expression-studio", "windows-game")
        startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
        descendant_pid = int(Path(str(startup) + ".descendant").read_text(encoding="utf-8"))

        assert child.state == "RUNNING"
        assert process_alive(child.process_id)
        assert process_alive(descendant_pid)

        stopped = owner.stop("expression-studio", "windows-game")
        assert stopped.status == "STOPPED"
        wait_gone(child.process_id)
        wait_gone(descendant_pid)
    finally:
        try:
            owner.stop_all()
        except Exception:
            pass
        if child is not None:
            wait_gone(child.process_id)
        if descendant_pid is not None:
            wait_gone(descendant_pid)
