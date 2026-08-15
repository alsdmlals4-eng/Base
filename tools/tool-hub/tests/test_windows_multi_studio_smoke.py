from __future__ import annotations

import ctypes
import sys

import pytest

import test_multi_studio_smoke as portable_smoke


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


def test_windows_four_process_import_workflows_are_project_isolated(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(portable_smoke, "assert_process_exited", assert_windows_process_exited)

    portable_smoke.test_linux_four_process_import_workflows_are_project_isolated(tmp_path)
