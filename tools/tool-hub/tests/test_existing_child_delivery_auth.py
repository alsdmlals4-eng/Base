from pathlib import Path
from types import SimpleNamespace

import pytest

from tool_hub.delivery_supervisor import ProcessSupervisor
from tool_hub.launcher import ChildIdentity, LaunchError
from tool_hub.projects import ProjectLocator


DELIVERY_TOKEN_ENV = "BASE_TOOL_HUB_DELIVERY_TOKEN"
_PRIVATE_TOKEN = "private-child-token-12345678901234567890"


def test_reusing_healthy_child_restores_running_state_and_delivery_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    key = ("expression-studio", "coc-fiction")
    token = _PRIVATE_TOKEN
    expected_identity = {
        "tool_id": key[0],
        "project_id": key[1],
        "launch_nonce": "n" * 43,
        "adapter_sha256": "a" * 64,
        "root_fingerprint": "b" * 64,
    }
    identity = ChildIdentity(
        key[0],
        key[1],
        64211,
        19436,
        expected_identity["launch_nonce"],
        "http://127.0.0.1:64211",
        {**expected_identity, "process_id": 19436, "status": "ready"},
    )
    child = SimpleNamespace(
        process=SimpleNamespace(pid=19436, poll=lambda: None),
        spec=SimpleNamespace(
            env={DELIVERY_TOKEN_ENV: token},
            expected_identity=expected_identity,
        ),
        identity=identity,
        state="RUNNING",
    )
    supervisor = ProcessSupervisor(
        tmp_path / "runtime",
        tmp_path / "base",
        ProjectLocator(tmp_path / "projects.json"),
        [{"tool_id": key[0], "health_path": "/api/status"}],
        hub_origin="http://127.0.0.1:8764",
    )
    supervisor._children[key] = child
    supervisor._set_state(key, "RUNNING", url=identity.url)
    monkeypatch.setattr(
        supervisor,
        "_fetch_status",
        lambda _: {**expected_identity, "process_id": 19436, "status": "ready"},
    )
    started_before = supervisor.started_process_count

    reused = supervisor.start(*key)

    assert reused is identity
    assert supervisor.started_process_count == started_before
    assert supervisor.view(*key).status == "RUNNING"
    assert supervisor.authorize_delivery_token(token) == key
    with pytest.raises(LaunchError, match="delivery credential"):
        supervisor.authorize_delivery_token("wrong-token")
