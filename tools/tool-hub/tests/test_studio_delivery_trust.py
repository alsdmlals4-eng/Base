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
_PRIVATE_TOKEN = "private-child-token-12345678901234567890"


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
    token = _PRIVATE_TOKEN
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
    token = _PRIVATE_TOKEN
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


def _authorize_expression_child(monkeypatch: pytest.MonkeyPatch) -> None:
    def authorize(self: ProcessSupervisor, token: str) -> tuple[str, str]:
        if token != _PRIVATE_TOKEN:
            raise LaunchError("studio delivery credential is invalid")
        return ("expression-studio", "coc-fiction")

    monkeypatch.setattr(ProcessSupervisor, "authorize_delivery_token", authorize)


def _studio_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_PRIVATE_TOKEN}",
        "Content-Type": "image/png",
    }


def test_internal_studio_delivery_requires_live_child_token_and_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _registered_hub(tmp_path)
    _authorize_expression_child(monkeypatch)
    payload = png_bytes(2, 1)

    unauthorized = client.post(
        "/internal/studio-delivery/run-confirmed",
        content=payload,
        headers={"Content-Type": "image/png"},
    )
    assert unauthorized.status_code == 401

    first = client.post("/internal/studio-delivery/run-confirmed", content=payload, headers=_studio_headers())
    second = client.post("/internal/studio-delivery/run-confirmed", content=payload, headers=_studio_headers())

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
        headers=_studio_headers(),
    )
    assert changed.status_code == 409
    assert changed.json()["detail"] == "DELIVERY_RUN_CONTENT_MISMATCH"


def test_unpaired_confirm_creates_one_reusable_project_pairing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _registered_hub(tmp_path)
    _authorize_expression_child(monkeypatch)
    payload = png_bytes(2, 1)

    first = client.post("/internal/studio-delivery/run-pairing", content=payload, headers=_studio_headers())
    retry = client.post("/internal/studio-delivery/run-pairing", content=payload, headers=_studio_headers())

    assert first.status_code == 201, first.text
    body = first.json()
    assert body["bridge_state"] == "PAIRING_REQUIRED"
    assert body["delivery_state"] == "DELIVERY_PENDING"
    assert body["figma_url"].startswith("https://www.figma.com/design/")
    assert len(body["pairing_code"]) == 6
    assert body["pairing_expires_at"] > 0
    assert retry.json()["pairing_code"] == body["pairing_code"]
    for forbidden in ("figma_file_key", "project_root", "generation_area_node_id"):
        assert forbidden not in first.text


def test_internal_delivery_status_reflects_bridge_pair_and_verified_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _registered_hub(tmp_path)
    _authorize_expression_child(monkeypatch)
    queued = client.post(
        "/internal/studio-delivery/run-verified",
        content=png_bytes(2, 1),
        headers=_studio_headers(),
    ).json()

    paired = client.post(
        "/bridge/pair",
        json={"pairing_code": queued["pairing_code"], "bridge_version": "bridge-test"},
    )
    assert paired.status_code == 200, paired.text
    bridge_auth = {"Authorization": f"Bearer {paired.json()['token']}"}
    claimed = client.get("/bridge/jobs/next", headers=bridge_auth).json()
    assert claimed["delivery_id"] == queued["delivery_id"]
    receipt = client.post(
        f"/bridge/jobs/{queued['delivery_id']}/receipt",
        json={
            "created_node_id": "999:1000",
            "created_node_name": claimed["node_name"],
            "target_node_id": claimed["target_node_id"],
            "content_sha256": claimed["content_sha256"],
            "bridge_version": "bridge-test",
            "image_hash": "figma-image-hash",
        },
        headers=bridge_auth,
    )
    assert receipt.status_code == 200, receipt.text

    status = client.get(
        f"/internal/studio-delivery/{queued['delivery_id']}/status",
        headers={"Authorization": f"Bearer {_PRIVATE_TOKEN}"},
    )

    assert status.status_code == 200, status.text
    body = status.json()
    assert body["status"] == "DELIVERED_VERIFIED"
    assert body["bridge_state"] == "BRIDGE_PAIRED"
    assert body["delivery_state"] == "FIGMA_DELIVERED_VERIFIED"
    assert body["delivery_id"] == queued["delivery_id"]
    assert body["tool_route_id"] == "character_expression_runs"
    assert body["target_node_name"] == "Expression Runs"
    assert body["figma_url"].startswith("https://www.figma.com/design/")
    assert "pairing_code" not in body
