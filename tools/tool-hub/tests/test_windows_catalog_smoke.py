from __future__ import annotations

import json
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

import pytest


BASE_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows process smoke")
def test_windows_process_starts_and_serves_blocked_catalog(tmp_path: Path) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "tool_hub.app",
            "--base-root",
            str(BASE_ROOT),
            "--project-config",
            str(tmp_path / "projects.json"),
            "--port",
            str(port),
        ],
        cwd=BASE_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        deadline = time.monotonic() + 20
        payload: dict[str, object] | None = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                output = process.stdout.read() if process.stdout is not None else ""
                pytest.fail(f"Tool Hub exited before Windows catalog smoke: {output[-2000:]}")
            try:
                with urlopen(f"http://127.0.0.1:{port}/api/catalog", timeout=1) as response:
                    payload = json.load(response)
                break
            except OSError:
                time.sleep(0.1)
        assert payload is not None, "Tool Hub did not serve the Windows catalog before timeout"
        assert {
            item["tool_id"]: item["launch_state"]  # type: ignore[index]
            for item in payload["tools"]  # type: ignore[index]
        } == {
            "expression-studio": "BLOCKED_PLATFORM",
            "qa-evidence-studio": "BLOCKED_PLATFORM",
            "sprite-animation-studio": "BLOCKED_PLATFORM",
        }
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
