from __future__ import annotations

import json
from pathlib import Path
import runpy

import pytest

import tool_hub.windows_launcher as launcher_module
import tool_hub.windows_launcher_repair as repair_module
from test_windows_launcher import installer


def test_desktop_bootstrap_routes_reviewed_runtime_drift_to_repair_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner, root, _, local, _ = installer(tmp_path)
    owner.install()
    namespace = runpy.run_path(str(owner.launcher_path), run_name="launcher_entry_test")
    (root / "tools" / "tool-hub" / "src" / "tool_hub" / "app.py").write_text(
        "# reviewed app after pull\n",
        encoding="utf-8",
    )
    commands: list[list[str]] = []
    shown: list[str] = []

    class CompletedChild:
        def wait(self, timeout: float) -> int:
            assert timeout <= 30
            return 0

    def popen(argv, **kwargs):
        commands.append([str(item) for item in argv])
        return CompletedChild()

    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setattr(namespace["subprocess"], "Popen", popen)
    namespace["main"].__globals__["_show_error"] = lambda reason: shown.append(reason)

    assert namespace["main"]() == 0
    assert shown == []
    assert len(commands) == 1
    assert commands[0][1:4] == ["-m", "tool_hub.windows_launcher_repair", "--config"]
    assert commands[0][4] == str(owner.config_path)


def test_repair_path_reissues_current_launcher_then_runs_it(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner, root, _, _, _ = installer(tmp_path)
    owner.install()
    config_path = owner.config_path
    before = json.loads(config_path.read_text(encoding="utf-8"))
    (root / "tools" / "tool-hub" / "src" / "tool_hub" / "app.py").write_text(
        "# reviewed app after pull\n",
        encoding="utf-8",
    )

    events: list[str] = []
    real_install = repair_module.WindowsLauncherInstaller.install

    def recording_install(self):
        events.append("install")
        return real_install(self)

    monkeypatch.setattr(repair_module.WindowsLauncherInstaller, "install", recording_install)
    result = repair_module.repair_installed_launcher(
        config_path,
        run=lambda path: events.append(f"run:{path}") or 0,
        desktop=owner.desktop,
        shortcut_builder=lambda *_: b"reviewed Windows shortcut",
    )

    after = json.loads(config_path.read_text(encoding="utf-8"))
    assert result == 0
    assert events == ["install", f"run:{config_path}"]
    assert after["launcher_token"] == before["launcher_token"]
    assert after["hub_runtime_fingerprint"] != before["hub_runtime_fingerprint"]
    assert owner.status() == "INSTALLED"


def test_repair_path_rejects_interpreter_tamper_before_reinstall(
    tmp_path: Path,
) -> None:
    owner, _, pythonw, _, _ = installer(tmp_path)
    owner.install()
    pythonw.write_bytes(b"tampered interpreter")

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_UPDATE_REQUIRED"):
        repair_module.repair_installed_launcher(
            owner.config_path,
            run=lambda _: 0,
            desktop=owner.desktop,
            shortcut_builder=lambda *_: b"reviewed Windows shortcut",
        )
