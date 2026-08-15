from __future__ import annotations

import ctypes
import sys

import pytest

import test_multi_studio_smoke as linux_smoke


pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="real Windows multi-Studio smoke")


def assert_windows_process_exited(pid: int) -> None:
    process = ctypes.windll.kernel32.OpenProcess(0x00100000, False, pid)
    if not process:
        return
    try:
        result = ctypes.windll.kernel32.WaitForSingleObject(process, 5000)
        assert result == 0, f"child process {pid} remained alive after Tool Hub shutdown"
    finally:
        ctypes.windll.kernel32.CloseHandle(process)


def test_windows_two_projects_run_expression_and_sprite_without_cross_wiring(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(linux_smoke, "assert_process_exited", assert_windows_process_exited)

    linux_smoke.test_two_projects_can_run_expression_and_sprite_without_cross_wiring(tmp_path)
