from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import subprocess
from urllib.error import HTTPError

import pytest

from tool_hub.windows_launcher import (
    LauncherError,
    WindowsLauncherInstaller,
    run_installed_launcher,
)
import tool_hub.windows_launcher as launcher_module


def make_base(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "Base With Spaces"
    pythonw = root / ".venv" / "Scripts" / "pythonw.exe"
    pythonw.parent.mkdir(parents=True)
    pythonw.write_bytes(b"fake pythonw")
    owner = root / "tools" / "tool-hub" / "src" / "tool_hub"
    owner.mkdir(parents=True)
    (owner / "app.py").write_text("# reviewed app\n", encoding="utf-8")
    template = owner / "windows_launcher_entry.pyw"
    reviewed_template = Path(launcher_module.__file__).with_name("windows_launcher_entry.pyw")
    template.write_bytes(reviewed_template.read_bytes())
    return root, pythonw


def installer(tmp_path: Path, *, platform: str = "win32"):
    root, pythonw = make_base(tmp_path)
    git = tmp_path / "Git" / "cmd" / "git.exe"
    git.parent.mkdir(parents=True)
    git.write_bytes(b"fake git")
    local = tmp_path / "Local App Data"
    desktop = tmp_path / "Desktop"
    desktop.mkdir()
    return WindowsLauncherInstaller(
        root,
        tmp_path / "projects.json",
        local_app_data=local,
        desktop=desktop,
        platform=platform,
        shortcut_builder=lambda *_: b"reviewed Windows shortcut",
        git_executable=git,
    ), root, pythonw, local, desktop


def test_installer_writes_fixed_private_config_and_desktop_entry(tmp_path: Path) -> None:
    owner, root, pythonw, local, desktop = installer(tmp_path)

    result = owner.install()
    config = json.loads((local / "BaseToolHub" / "launcher" / "launcher-config.json").read_text(encoding="utf-8"))

    assert result.public_view() == {"state": "INSTALLED", "desktop_entry": "Base Tool Hub.lnk"}
    assert config["base_root"] == str(root)
    assert config["pythonw"] == str(pythonw)
    assert config["git_executable"].endswith("git.exe")
    assert len(config["hub_runtime_fingerprint"]) == 64
    assert config["port"] == 8764
    assert len(config["launcher_token"]) >= 32
    assert (desktop / "Base Tool Hub.lnk").read_bytes() == b"reviewed Windows shortcut"
    assert "OPENAI_API_KEY" not in json.dumps(config)


def test_reinstall_for_a_different_project_config_rotates_identity(tmp_path: Path) -> None:
    owner, root, _, local, desktop = installer(tmp_path)
    owner.install()
    config_path = local / "BaseToolHub" / "launcher" / "launcher-config.json"
    first = json.loads(config_path.read_text(encoding="utf-8"))
    second_owner = WindowsLauncherInstaller(
        root,
        tmp_path / "different-projects.json",
        local_app_data=local,
        desktop=desktop,
        platform="win32",
        shortcut_builder=lambda *_: b"reviewed Windows shortcut",
        git_executable=Path(first["git_executable"]),
    )

    second_owner.install()
    second = json.loads(config_path.read_text(encoding="utf-8"))

    assert first["launcher_token"] != second["launcher_token"]
    assert first["project_config_fingerprint"] != second["project_config_fingerprint"]


def test_installed_bootstrap_validates_interpreter_before_spawning(tmp_path: Path) -> None:
    owner, _, pythonw, _, _ = installer(tmp_path)
    owner.install()
    namespace = runpy.run_path(str(owner.launcher_path), run_name="launcher_entry_test")
    pythonw.write_bytes(b"changed before desktop launch")

    with pytest.raises(RuntimeError, match="LAUNCHER_UPDATE_REQUIRED"):
        namespace["_validated_config"](owner.config_path, owner.launcher_path)


def test_installer_is_idempotent_and_does_not_depend_on_global_pyw_association(tmp_path: Path) -> None:
    owner, *_ = installer(tmp_path)
    assert owner.install().state == "INSTALLED"
    first_token = json.loads(owner.config_path.read_text(encoding="utf-8"))["launcher_token"]
    assert owner.install().state == "INSTALLED"
    assert json.loads(owner.config_path.read_text(encoding="utf-8"))["launcher_token"] == first_token

    unsupported, *_ = installer(tmp_path / "unsupported", platform="linux")
    with pytest.raises(LauncherError, match="BLOCKED_PLATFORM"):
        unsupported.install()

def test_installer_status_detects_changed_runtime_bytes(tmp_path: Path) -> None:
    owner, root, pythonw, _, _ = installer(tmp_path)
    owner.install()
    assert owner.status() == "INSTALLED"

    pythonw.write_bytes(b"changed")

    assert owner.status() == "UPDATE_REQUIRED"

    owner.install()
    (root / "tools" / "tool-hub" / "src" / "tool_hub" / "app.py").write_text(
        "# changed reviewed app\n", encoding="utf-8"
    )
    assert owner.status() == "UPDATE_REQUIRED"


def test_installer_status_rejects_a_changed_desktop_shortcut(tmp_path: Path) -> None:
    owner, *_ = installer(tmp_path)
    owner.install()
    assert owner.status() == "INSTALLED"

    owner.desktop_entry.write_bytes(b"changed shortcut")

    assert owner.status() == "UPDATE_REQUIRED"


def test_installer_migrates_the_exact_legacy_desktop_pyw(tmp_path: Path) -> None:
    owner, root, *_ = installer(tmp_path)
    legacy = owner.desktop / "Base Tool Hub.pyw"
    legacy.write_bytes(owner.template.read_bytes())

    owner.install()

    assert not legacy.exists()
    assert owner.desktop_entry.is_file()
    assert owner.status() == "INSTALLED"


def test_installer_rejects_a_tampered_legacy_desktop_pyw(tmp_path: Path) -> None:
    owner, *_ = installer(tmp_path)
    legacy = owner.desktop / "Base Tool Hub.pyw"
    legacy.write_bytes(b"tampered legacy launcher")

    with pytest.raises(LauncherError, match="LAUNCHER_LEGACY_CONFLICT"):
        owner.install()

    assert not owner.desktop_entry.exists()
    assert owner.status() == "REPAIR_REQUIRED"


def test_launcher_reuses_exact_health_or_starts_detached_before_opening_browser(tmp_path: Path) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    config = local / "BaseToolHub" / "launcher" / "launcher-config.json"
    events: list[str] = []

    assert run_installed_launcher(
        config,
        probe=lambda _: True,
        spawn=lambda _: events.append("spawn"),
        open_browser=lambda _: events.append("browser"),
        sleep=lambda _: None,
    ) == 0
    assert events == ["browser"]

    attempts = iter([False, False, True])
    events.clear()
    assert run_installed_launcher(
        config,
        probe=lambda _: next(attempts),
        spawn=lambda _: events.append("spawn"),
        open_browser=lambda _: events.append("browser"),
        sleep=lambda _: None,
    ) == 0
    assert events == ["spawn", "browser"]


def test_launcher_does_not_spawn_when_the_exact_port_has_a_wrong_identity(tmp_path: Path) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    events: list[str] = []

    with pytest.raises(LauncherError, match="PORT_IDENTITY_CONFLICT"):
        run_installed_launcher(
            local / "BaseToolHub" / "launcher" / "launcher-config.json",
            probe=lambda _: None,
            spawn=lambda _: events.append("spawn"),
            open_browser=lambda _: events.append("browser"),
            sleep=lambda _: None,
        )

    assert events == []


def test_http_error_from_an_occupied_port_is_an_identity_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(*args, **kwargs):
        raise HTTPError("http://127.0.0.1:8764", 403, "forbidden", {}, None)

    monkeypatch.setattr(launcher_module, "urlopen", denied)

    assert launcher_module._probe({"port": 8764, "launcher_token": "x", "root_fingerprint": "y"}) is None


def test_second_double_click_waits_for_the_lock_owner_instead_of_spawning(tmp_path: Path) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    config = local / "BaseToolHub" / "launcher" / "launcher-config.json"
    lock = launcher_module._try_acquire_launcher_lock(config.parent / ".launcher.lock")
    assert lock is not None
    attempts = iter([False, True])
    events: list[str] = []

    try:
        run_installed_launcher(
            config,
            probe=lambda _: next(attempts),
            spawn=lambda _: events.append("spawn"),
            open_browser=lambda _: events.append("browser"),
            sleep=lambda _: None,
        )
    finally:
        launcher_module._release_launcher_lock(lock)

    assert events == ["browser"]


def test_stale_launcher_lock_file_does_not_block_a_future_launch(tmp_path: Path) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    config = local / "BaseToolHub" / "launcher" / "launcher-config.json"
    (config.parent / ".launcher.lock").write_text("stale process", encoding="utf-8")
    attempts = iter([False, False, True])
    events: list[str] = []

    run_installed_launcher(
        config,
        probe=lambda _: next(attempts),
        spawn=lambda _: events.append("spawn"),
        open_browser=lambda _: events.append("browser"),
        sleep=lambda _: None,
    )

    assert events == ["spawn", "browser"]


def test_detached_spawn_keeps_only_the_reviewed_python_and_git_search_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    payload = json.loads((local / "BaseToolHub" / "launcher" / "launcher-config.json").read_text(encoding="utf-8"))
    captured: dict[str, object] = {}

    class Process:
        def __init__(self, argv, **kwargs):
            captured.update({"argv": argv, **kwargs})

    monkeypatch.setattr(launcher_module.subprocess, "Popen", Process)
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    launcher_module._spawn(payload)

    search = str(captured["env"]["PATH"]).split(os.pathsep)  # type: ignore[index]
    assert str(Path(payload["pythonw"]).parent) in search
    assert str(Path(payload["git_executable"]).parent) in search
    assert captured["stdout"] is subprocess.DEVNULL
    assert captured["stderr"] is subprocess.DEVNULL


def test_launcher_detects_a_child_that_exits_before_health(tmp_path: Path) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()

    class Exited:
        def poll(self):
            return 7

    with pytest.raises(LauncherError, match="HUB_START_FAILED"):
        run_installed_launcher(
            local / "BaseToolHub" / "launcher" / "launcher-config.json",
            probe=lambda _: False,
            spawn=lambda _: Exited(),
            open_browser=lambda _: None,
            sleep=lambda _: None,
        )


def test_desktop_bootstrap_rejects_a_linked_config_parent(tmp_path: Path) -> None:
    owner, _, _, _, _ = installer(tmp_path)
    owner.install()
    namespace = runpy.run_path(str(owner.launcher_path), run_name="launcher_entry_test")
    linked_parent = tmp_path / "linked-launcher"
    linked_parent.symlink_to(owner.config_path.parent, target_is_directory=True)

    with pytest.raises(RuntimeError, match="LAUNCHER_CONFIG_INVALID"):
        namespace["_validated_config"](linked_parent / owner.config_path.name, owner.launcher_path)


def test_no_console_launcher_reports_a_bounded_error_and_log_location(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = tmp_path / "Local App Data"
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    shown: list[str] = []
    monkeypatch.setattr(launcher_module, "_show_native_error", lambda message: shown.append(message))

    assert launcher_module.main(["--config", str(tmp_path / "missing-config.json")]) == 1

    assert shown and "LAUNCHER_CONFIG_INVALID" in shown[0]
    assert "진단 폴더" in shown[0]
    diagnostic = local / "BaseToolHub" / "logs" / "launcher-error.log"
    assert diagnostic.stat().st_size < 4096
    assert str(tmp_path) not in diagnostic.read_text(encoding="utf-8")


def test_desktop_bootstrap_reports_a_launcher_child_import_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner, _, _, local, _ = installer(tmp_path)
    owner.install()
    namespace = runpy.run_path(str(owner.launcher_path), run_name="launcher_entry_test")
    shown: list[str] = []

    class FailedChild:
        def wait(self, timeout: float) -> int:
            assert timeout <= 30
            return 7

    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setattr(namespace["subprocess"], "Popen", lambda *args, **kwargs: FailedChild())
    namespace["main"].__globals__["_show_error"] = lambda reason: shown.append(reason)

    assert namespace["main"]() == 1
    assert shown == ["LAUNCHER_CHILD_FAILED"]
