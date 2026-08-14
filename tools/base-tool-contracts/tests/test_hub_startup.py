import json
import os
from pathlib import Path
import threading

import pytest


def test_hub_identity_is_read_only_from_the_child_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    from base_tool_contracts import hub_identity_from_environment

    monkeypatch.setenv("BASE_TOOL_HUB_LAUNCH_NONCE", "n" * 43)
    monkeypatch.setenv("BASE_TOOL_HUB_ADAPTER_SHA256", "a" * 64)
    monkeypatch.setenv("BASE_TOOL_HUB_ROOT_FINGERPRINT", "b" * 64)

    identity = hub_identity_from_environment()

    assert identity.launch_nonce == "n" * 43
    assert identity.adapter_sha256 == "a" * 64
    assert identity.root_fingerprint == "b" * 64


def test_startup_report_requires_a_private_parent_and_new_regular_file(tmp_path: Path) -> None:
    from base_tool_contracts import HubStartupError, write_startup_report

    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    report = private / "startup.json"
    payload = {"tool_id": "expression-studio", "port": 12345}

    write_startup_report(report, payload)

    assert json.loads(report.read_text(encoding="utf-8")) == payload
    assert report.stat().st_mode & 0o777 == 0o600
    with pytest.raises(HubStartupError, match="already exists"):
        write_startup_report(report, payload)

    public = tmp_path / "public"
    public.mkdir(mode=0o755)
    with pytest.raises(HubStartupError, match="private"):
        write_startup_report(public / "startup.json", payload)


def test_startup_report_rejects_a_symlinked_parent(tmp_path: Path) -> None:
    from base_tool_contracts import HubStartupError, write_startup_report

    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    alias = tmp_path / "alias"
    alias.symlink_to(private, target_is_directory=True)

    with pytest.raises(HubStartupError, match="private|symlink"):
        write_startup_report(alias / "startup.json", {"tool_id": "sprite-animation-studio"})


def test_startup_report_is_not_visible_until_the_json_is_complete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import base_tool_contracts.hub_startup as startup_module

    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    report = private / "startup.json"
    entered_write = threading.Event()
    release_write = threading.Event()
    real_write = startup_module.os.write

    def delayed_write(descriptor: int, raw: bytes) -> int:
        entered_write.set()
        assert release_write.wait(timeout=2)
        return real_write(descriptor, raw)

    monkeypatch.setattr(startup_module.os, "write", delayed_write)
    worker = threading.Thread(
        target=startup_module.write_startup_report,
        args=(report, {"tool_id": "expression-studio", "port": 12345}),
    )
    worker.start()
    try:
        assert entered_write.wait(timeout=2)
        assert not report.exists()
    finally:
        release_write.set()
        worker.join(timeout=2)

    assert not worker.is_alive()
    assert json.loads(report.read_text(encoding="utf-8"))["port"] == 12345


def test_loopback_listener_reports_the_actual_ephemeral_port() -> None:
    from base_tool_contracts import open_loopback_listener

    listener = open_loopback_listener(0)
    try:
        host, port = listener.getsockname()
        assert host == "127.0.0.1"
        assert 0 < port < 65536
    finally:
        listener.close()
