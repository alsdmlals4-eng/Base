from pathlib import Path
import subprocess

import base_tool_contracts.trusted_files as trusted_files
import base_tool_contracts.windows_project_identity as windows_identity


NO_WINDOW = 0x08000000


def _completed(command):
    return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")


def test_portable_git_applies_the_platform_creation_flags(monkeypatch) -> None:
    captured = {}
    fake_git = Path("C:/Program Files/Git/cmd/git.exe")

    monkeypatch.setattr(trusted_files, "trusted_git_executable", lambda: fake_git)
    monkeypatch.setattr(
        trusted_files,
        "portable_subprocess_creationflags",
        lambda: NO_WINDOW,
        raising=False,
    )

    def fake_run(command, **kwargs):
        captured.update(kwargs)
        return _completed(command)

    monkeypatch.setattr(trusted_files.subprocess, "run", fake_run)

    trusted_files.run_portable_git(Path("C:/repo"), "status", "--porcelain")

    assert captured["creationflags"] == NO_WINDOW


def test_windows_identity_git_applies_the_platform_creation_flags(monkeypatch) -> None:
    captured = {}

    monkeypatch.setattr(
        windows_identity,
        "portable_subprocess_creationflags",
        lambda: NO_WINDOW,
        raising=False,
    )

    def fake_run(command, **kwargs):
        captured.update(kwargs)
        return _completed(command)

    monkeypatch.setattr(windows_identity.subprocess, "run", fake_run)

    windows_identity._git(Path("C:/Git/git.exe"), Path("C:/repo"), "rev-parse", "HEAD")

    assert captured["creationflags"] == NO_WINDOW
