from __future__ import annotations

from types import SimpleNamespace
from pathlib import Path
import threading

import pytest
from fastapi.testclient import TestClient

from test_figma_delivery import png_bytes
from test_projects import BASE_ROOT, make_project
from tool_hub.app import create_app
from tool_hub.delivery_supervisor import ProcessSupervisor
from tool_hub.environment import LaunchContext, child_environment
from tool_hub.launcher import LaunchError
from tool_hub.projects import ProjectLocator


DELIVERY_TOKEN_ENV = "BASE_TOOL_HUB_DELIVERY_TOKEN"
DELIVERY_ORIGIN_ENV = "BASE_TOOL_HUB_DELIVERY_ORIGIN"


def test_child_environment_injects_private_hub_delivery_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(DELIVERY_TOKEN_ENV, "attacker-parent-token")
    monkeypatch.setenv(DELIVERY_ORIGIN_ENV, "http://attacker.invalid")
    context = LaunchContext(
        tmp_path,
        tmp_path / "runtime",
        tmp_path / ".venv" / "bin" / "python",
        "n" * 43,
        hub_origin="http://127.0.0.1:8764",
        delivery_token="d" * 43,
    )

    environment = child_environment(context, "a" * 64, "b" * 64)

    assert environment[DELIVERY_TOKEN_ENV] == "d" * 43
    assert environment[DELIVERY_ORIGIN_ENV] == "http://127.0.0.1:8764"
    assert environment[DELIVERY_TOKEN_ENV] != environment["BASE_TOOL_HUB_LAUNCH_NONCE"]


def test_supervisor_delivery_token_is_bound_to_one_running_child(tmp_path: Path) -> None:
    token = "private-child-token-12345678901234567890"
    supervisor = ProcessSupervisor(
        tmp_path / "runtime",
        tmp_path / "base",
        ProjectLocator(tmp_path / "projects.json"),
        [],
        hub_origin="http://127.0.0.1:8764",
    )
    key = ("expression-studio", "coc-fiction")
    child = SimpleNamespace(
        process=SimpleNamespace(poll=lambda: None),
        spec=SimpleNamespace(env={DELIVERY_TOKEN_ENV: token}),
        identity=SimpleNamespace(tool_id=key[0], project_id=key[1]),
    )
    supervisor._children[key] = child
    supervisor._set_state(key, "RUNNING")

    assert supervisor.authorize_delivery_token(token) == key
    with pytest.raises(LaunchError, match="delivery credential"):
        supervisor.authorize_delivery_token("wrong-token")

    supervisor._set_state(key, "STOPPING")
    with pytest.raises(LaunchError, match="delivery credential"):
        supervisor.authorize_delivery_token(token)

    supervisor._set_state(key, "RUNNING")
    child.process = SimpleNamespace(poll=lambda: 1)
    with pytest.raises(LaunchError, match="delivery credential"):
        supervisor.authorize_delivery_token(token)


def test_public_log_tail_redacts_private_delivery_token(tmp_path: Path) -> None:
    token = "private-child-token-12345678901234567890"
    supervisor = ProcessSupervisor(
        tmp_path / "runtime",
        tmp_path / "base",
        ProjectLocator(tmp_path / "projects.json"),
        [],
        hub_origin="http://127.0.0.1:8764",
    )
    child = SimpleNamespace(
        log_tail=bytearray(f"startup error token={token}\n".encode("utf-8")),
        log_lock=threading.Lock(),
        launch_dir=tmp_path / "runtime" / "launch",
        project_root=tmp_path / "project",
        spec=SimpleNamespace(
            env={DELIVERY_TOKEN_ENV: token},
            expected_identity={"launch_nonce": "n" * 43},
        ),
    )

    public = supervisor._sanitized_log_tail(child)

    assert token not in public
    assert "<redacted>" in public


def _registered_hub(tmp_path: Path) -> TestClient:
    project = make_project(tmp_path / "Project", "coc-fiction")
    app = create_app(
        BASE_ROOT,
        tmp_path / "machine-projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        launch_supported=False,
    )
    client = TestClient(app)
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]
    registered = client.post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(project)},
    )
    assert registered.status_code == 201
    return client


def test_internal_studio_delivery_requires_live_child_token_and_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _registered_hub(tmp_path)
    private_token = "private-child-token-12345678901234567890"

    def authorize(self: ProcessSupervisor, token: str) -> tuple[str, str]:
        if token != private_token:
            raise LaunchError("studio delivery credential is invalid")
        return ("expression-studio", "coc-fiction")

    monkeypatch.setattr(ProcessSupervisor, "authorize_delivery_token", authorize)
    payload = png_bytes(2, 1)

    unauthorized = client.post(
        "/internal/studio-delivery/run-confirmed",
        content=payload,
        headers={"Content-Type": "image/png"},
    )
    assert unauthorized.status_code == 401

    headers = {
        "Authorization": f"Bearer {private_token}",
        "Content-Type": "image/png",
    }
    first = client.post("/internal/studio-delivery/run-confirmed", content=payload, headers=headers)
    second = client.post("/internal/studio-delivery/run-confirmed", content=payload, headers=headers)

    assert first.status_code == 201, first.text
    assert second.status_code == 200, second.text
    assert second.json()["delivery_id"] == first.json()["delivery_id"]
    assert first.json()["tool_id"] == "expression-studio"
    assert first.json()["project_id"] == "coc-fiction"
    assert first.json()["tool_route_id"] == "character_expression_runs"
    assert first.json()["target_node_name"] == "Expression Runs"
    assert "figma_file_key" not in first.text
    assert "project_root" not in first.text
    assert client.app.state.figma_delivery.public_status("coc-fiction")["pending_count"] == 1

    changed = client.post(
        "/internal/studio-delivery/run-confirmed",
        content=png_bytes(1, 1),
        headers=headers,
    )
    assert changed.status_code == 409
    assert changed.json()["detail"] == "DELIVERY_RUN_CONTENT_MISMATCH"
