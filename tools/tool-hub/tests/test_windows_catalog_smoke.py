from __future__ import annotations

import json
from http.cookiejar import CookieJar
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import HTTPCookieProcessor, Request, build_opener
from urllib.error import HTTPError

import pytest
from fastapi.testclient import TestClient

from base_tool_contracts import validate_windows_project_identity
from base_tool_contracts.windows_project_identity import WindowsProjectIdentityError
from test_projects import make_project
from tool_hub.app import create_app


BASE_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows process smoke")
def test_windows_process_starts_and_serves_blocked_catalog(tmp_path: Path) -> None:
    managed = tmp_path / "Documents" / "GitHub"
    projects = (
        make_project(managed / "Coc-Fiction", "coc-fiction"),
        make_project(managed / "omenward", "omenward"),
    )
    for project, remote in zip(
        projects,
        (
            "https://github.com/alsdmlals4-eng/Coc-Fiction.git",
            "https://github.com/alsdmlals4-eng/omenward.git",
        ),
        strict=True,
    ):
        subprocess.run(["git", "-C", str(project), "remote", "set-url", "origin", remote], check=True)
    try:
        validate_windows_project_identity(projects[0], "coc-fiction", BASE_ROOT)
    except WindowsProjectIdentityError as error:
        pytest.fail(f"Windows identity preflight failed: {error}: {error._diagnostic}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    environment = os.environ.copy()
    environment["USERPROFILE"] = str(tmp_path)
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
        env=environment,
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
        for project_id in ("coc-fiction", "omenward"):
            request = Request(
                f"http://127.0.0.1:{port}/api/projects/{project_id}/onboard",
                data=b"{}",
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
            assert registered == {
                "project_id": project_id,
                "local_state": "REGISTERED",
                "action_label": "연결됨",
            }

        with opener.open(f"http://127.0.0.1:{port}/api/catalog", timeout=20) as response:
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


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows Git clone smoke")
def test_windows_onboarding_discovers_one_project_and_really_clones_another(
    tmp_path: Path,
) -> None:
    managed = tmp_path / "Documents" / "GitHub"
    discovered = make_project(managed / "Coc-Fiction", "coc-fiction")
    subprocess.run(
        [
            "git",
            "-C",
            str(discovered),
            "remote",
            "set-url",
            "origin",
            "https://github.com/alsdmlals4-eng/Coc-Fiction.git",
        ],
        check=True,
    )
    fixture = make_project(tmp_path / "fixture-remote" / "omenward", "omenward")
    adapter = json.loads(
        (fixture / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8")
    )
    protected_baseline = adapter["protected_baseline"]["commit"]

    def real_git_clone(repository_url: str, destination: Path) -> None:
        subprocess.run(
            ["git", "clone", "--no-local", "--", str(fixture), str(destination)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(destination), "remote", "set-url", "origin", repository_url],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(destination),
                "update-ref",
                "refs/remotes/origin/main",
                protected_baseline,
            ],
            check=True,
        )

    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            onboarding_home=tmp_path,
            managed_project_root=managed,
            onboarding_clone_runner=real_git_clone,
        )
    )
    client.headers["Origin"] = "http://testserver"
    client.headers["X-Hub-CSRF"] = client.get("/api/config").json()["csrf_token"]

    found = client.post("/api/projects/coc-fiction/onboard", json={})
    cloned = client.post("/api/projects/omenward/onboard", json={})

    assert found.status_code == 200
    assert cloned.status_code == 200
    assert (managed / "omenward" / ".git").is_dir()
    assert subprocess.run(
        ["git", "-C", str(managed / "omenward"), "rev-parse", "--is-inside-work-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip() == "true"
