from __future__ import annotations

import json
from http.cookiejar import CookieJar
import os
from pathlib import Path
import sys
import time
from urllib.request import HTTPCookieProcessor, Request, build_opener

import pytest

from tool_hub.windows_launcher import WindowsLauncherInstaller


BASE_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows pythonw smoke")
def test_pythonw_launcher_starts_reuses_and_shuts_down_exact_hub(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    local = tmp_path / "Local App Data With Spaces"
    desktop = tmp_path / "Desktop With Spaces"
    desktop.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    installer = WindowsLauncherInstaller(
        BASE_ROOT,
        tmp_path / "projects.json",
        local_app_data=local,
        desktop=desktop,
    )
    installer.install()
    assert installer.desktop_entry.suffix.casefold() == ".lnk"
    config_path = local / "BaseToolHub" / "launcher" / "launcher-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    os.startfile(installer.desktop_entry)
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    status_request = Request(
        "http://127.0.0.1:8764/api/launcher-status",
        headers={"X-Hub-Launcher-Token": config["launcher_token"]},
    )
    deadline = time.monotonic() + 60
    while True:
        try:
            with opener.open(status_request, timeout=1) as response:
                first = json.load(response)
            break
        except OSError:
            if time.monotonic() >= deadline:
                pytest.fail("desktop .lnk did not start the exact Tool Hub")
            time.sleep(0.1)
    os.startfile(installer.desktop_entry)
    time.sleep(1)
    with opener.open(status_request, timeout=5) as response:
        second = json.load(response)

    assert first["process_id"] == second["process_id"]

    with opener.open("http://127.0.0.1:8764/api/config", timeout=5) as response:
        browser_config = json.load(response)
    shutdown = Request(
        "http://127.0.0.1:8764/api/shutdown",
        data=b"{}",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Origin": "http://127.0.0.1:8764",
            "X-Hub-CSRF": browser_config["csrf_token"],
        },
    )
    with opener.open(shutdown, timeout=5) as response:
        assert json.load(response) == {"state": "SHUTTING_DOWN"}
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            opener.open("http://127.0.0.1:8764/api/catalog", timeout=0.3).close()
        except OSError:
            break
        time.sleep(0.1)
    else:
        pytest.fail("pythonw Tool Hub still owned port 8764 after authenticated shutdown")
    # The authenticated shutdown is the only normal owner; no PID from the browser is killed here.
