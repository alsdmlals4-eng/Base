from pathlib import Path

from tool_hub.launcher import QaEvidenceLauncher
from tool_hub.projects import ProjectLocator
from test_projects import make_project


def test_real_child_reports_exact_project_and_nonce(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces", "demo-game")
    binding = ProjectLocator(tmp_path / "projects.json").register(project, "demo-game")
    launcher = QaEvidenceLauncher(tmp_path / "runtime")
    try:
        child = launcher.start(binding)

        assert child.tool_id == "qa-evidence-studio"
        assert child.project_id == "demo-game"
        assert child.port > 0
        assert child.process_id > 0
        assert child.url.startswith("http://127.0.0.1:")
        assert child.status["launch_nonce"] == child.launch_nonce
        assert child.status["project_id"] == "demo-game"
        assert child.public_view()["status"] == "RUNNING"
    finally:
        launcher.stop_all()


def test_repeat_start_is_idempotent_and_two_projects_are_isolated(tmp_path: Path) -> None:
    left = ProjectLocator(tmp_path / "left.json").register(
        make_project(tmp_path / "left", "left-game"),
        "left-game",
    )
    right = ProjectLocator(tmp_path / "right.json").register(
        make_project(tmp_path / "right", "right-game"),
        "right-game",
    )
    launcher = QaEvidenceLauncher(tmp_path / "runtime")
    try:
        first = launcher.start(left)
        repeated = launcher.start(left)
        second = launcher.start(right)

        assert repeated.process_id == first.process_id
        assert repeated.port == first.port
        assert second.process_id != first.process_id
        assert second.port != first.port
        assert second.project_id == "right-game"
    finally:
        launcher.stop_all()


def test_child_environment_does_not_inherit_provider_secrets(tmp_path: Path, monkeypatch) -> None:
    binding = ProjectLocator(tmp_path / "projects.json").register(
        make_project(tmp_path / "project", "demo-game"),
        "demo-game",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-cross")
    monkeypatch.setenv("CODEX_HOME", "/must/not/cross")
    launcher = QaEvidenceLauncher(tmp_path / "runtime")

    environment = launcher.child_environment()

    assert "OPENAI_API_KEY" not in environment
    assert "CODEX_HOME" not in environment
    assert environment["PYTHONUTF8"] == "1"
