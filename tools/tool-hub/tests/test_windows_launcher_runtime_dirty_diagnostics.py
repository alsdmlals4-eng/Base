from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

import pytest

import tool_hub.windows_launcher as launcher_module
import tool_hub.windows_launcher_repair as repair_module


def _same_head() -> bytes:
    return b"a" * 40 + b"\n"


def test_git_diff_check_failure_is_not_reported_as_runtime_dirty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    same = _same_head()
    results = iter(
        [
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 2, stdout=b"", stderr=b"fatal: synthetic check failure\n"),
        ]
    )
    monkeypatch.setattr(repair_module.subprocess, "run", lambda *args, **kwargs: next(results))

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_GIT_CHECK_FAILED"):
        repair_module._assert_reviewed_runtime(Path("C:/Base"), Path("C:/Git/git.exe"))


def test_real_runtime_dirty_writes_only_reviewed_relative_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    same = _same_head()
    results = iter(
        [
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess(
                [],
                1,
                stdout=b"tools/tool-hub/web/app.js\x00tools/tool-hub/src/tool_hub/app.py\x00",
                stderr=b"",
            ),
        ]
    )
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(repair_module.subprocess, "run", lambda *args, **kwargs: next(results))

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_RUNTIME_DIRTY"):
        repair_module._assert_reviewed_runtime(Path("C:/Base"), Path("C:/Git/git.exe"))

    diagnostic = tmp_path / "BaseToolHub" / "logs" / "launcher-runtime-dirty.log"
    assert diagnostic.read_text(encoding="utf-8") == (
        "LAUNCHER_RUNTIME_DIRTY\n"
        "tools/tool-hub/web/app.js\n"
        "tools/tool-hub/src/tool_hub/app.py\n"
    )


def test_runtime_dirty_diagnostic_rejects_out_of_scope_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    same = _same_head()
    results = iter(
        [
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 1, stdout=b"docs/private.txt\x00", stderr=b""),
        ]
    )
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(repair_module.subprocess, "run", lambda *args, **kwargs: next(results))

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_GIT_CHECK_FAILED"):
        repair_module._assert_reviewed_runtime(Path("C:/Base"), Path("C:/Git/git.exe"))

    assert not (tmp_path / "BaseToolHub" / "logs" / "launcher-runtime-dirty.log").exists()


def test_runtime_dirty_diagnostic_rejects_non_nul_terminated_git_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    same = _same_head()
    results = iter(
        [
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 1, stdout=b"tools/tool-hub/web/app.js", stderr=b""),
        ]
    )
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(repair_module.subprocess, "run", lambda *args, **kwargs: next(results))

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_GIT_CHECK_FAILED"):
        repair_module._assert_reviewed_runtime(Path("C:/Base"), Path("C:/Git/git.exe"))

    assert not (tmp_path / "BaseToolHub" / "logs" / "launcher-runtime-dirty.log").exists()


def test_runtime_dirty_requires_at_least_one_reviewed_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    same = _same_head()
    results = iter(
        [
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 0, stdout=same, stderr=b""),
            subprocess.CompletedProcess([], 1, stdout=b"", stderr=b""),
        ]
    )
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(repair_module.subprocess, "run", lambda *args, **kwargs: next(results))

    with pytest.raises(launcher_module.LauncherError, match="LAUNCHER_GIT_CHECK_FAILED"):
        repair_module._assert_reviewed_runtime(Path("C:/Base"), Path("C:/Git/git.exe"))

    assert not (tmp_path / "BaseToolHub" / "logs" / "launcher-runtime-dirty.log").exists()


def test_reviewed_runtime_accepts_crlf_only_worktree_representation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    git_name = shutil.which("git")
    assert git_name is not None
    git = Path(git_name)
    root = tmp_path / "Base"
    root.mkdir()

    def run_git(*arguments: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [str(git), "-C", str(root), *arguments],
            check=True,
            capture_output=True,
        )

    subprocess.run([str(git), "init", str(root)], check=True, capture_output=True)
    run_git("config", "user.email", "tool-hub-test@example.invalid")
    run_git("config", "user.name", "Tool Hub Test")
    run_git("config", "core.autocrlf", "false")

    relative = "tools/tool-hub/src/tool_hub/windows_launcher_repair.py"
    target = root / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(b"line_one = 1\nline_two = 2\n")
    run_git("add", relative)
    run_git("commit", "-m", "fixture")
    head = run_git("rev-parse", "HEAD").stdout.strip().decode("ascii")
    run_git("update-ref", "refs/remotes/origin/main", head)

    target.write_bytes(b"line_one = 1\r\nline_two = 2\r\n")
    raw = subprocess.run(
        [
            str(git),
            "-c",
            "core.autocrlf=false",
            "-C",
            str(root),
            "diff",
            "--quiet",
            "--no-ext-diff",
            "HEAD",
            "--",
            relative,
        ],
        check=False,
        capture_output=True,
    )
    assert raw.returncode == 1

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    repair_module._assert_reviewed_runtime(root, git)
