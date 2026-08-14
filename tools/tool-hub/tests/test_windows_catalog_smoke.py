from __future__ import annotations

import json
from http.cookiejar import CookieJar
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import HTTPCookieProcessor, Request, build_opener
from urllib.error import HTTPError

import pytest

from test_projects import make_project


BASE_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows process smoke")
def test_windows_process_starts_and_serves_blocked_catalog(tmp_path: Path) -> None:
    projects = (
        make_project(tmp_path / "Coc Fiction Project With Spaces", "coc-fiction"),
        make_project(tmp_path / "Omenward Project With Spaces", "omenward"),
    )
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
        opener = build_opener(HTTPCookieProcessor(CookieJar()))
        while time.monotonic() < deadline:
            if process.poll() is not None:
                output = process.stdout.read() if process.stdout is not None else ""
                pytest.fail(f"Tool Hub exited before Windows catalog smoke: {output[-2000:]}")
            try:
                with opener.open(f"http://127.0.0.1:{port}/api/catalog", timeout=1) as response:
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
        with opener.open(f"http://127.0.0.1:{port}/api/config", timeout=2) as response:
            config = json.load(response)
        for project_id, project_root in zip(("coc-fiction", "omenward"), projects, strict=True):
            body = json.dumps(
                {"project_id": project_id, "project_root": str(project_root)}
            ).encode("utf-8")
            request = Request(
                f"http://127.0.0.1:{port}/api/projects",
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Origin": f"http://127.0.0.1:{port}",
                    "X-Hub-CSRF": str(config["csrf_token"]),
                },
            )
            try:
                with opener.open(request, timeout=20) as response:
                    registered = json.load(response)
            except HTTPError as error:
                detail = error.read().decode("utf-8", errors="replace")
                pytest.fail(f"Windows project registration returned HTTP {error.code}: {detail}")
            assert registered["project_id"] == project_id

        with opener.open(f"http://127.0.0.1:{port}/api/catalog", timeout=2) as response:
            registered_catalog = json.load(response)
        assert [project["project_id"] for project in registered_catalog["projects"]] == [
            "coc-fiction",
            "omenward",
        ]
        assert all(
            tool["launch_state"] == "BLOCKED_PLATFORM"
            for tool in registered_catalog["tools"]
        )
        serialized = json.dumps(registered_catalog)
        assert all(str(project_root) not in serialized for project_root in projects)
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
