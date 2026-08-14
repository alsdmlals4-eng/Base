import os
from pathlib import Path
import stat

import pytest

from tool_hub.environment import EnvironmentError, LaunchContext, child_environment


def _context(tmp_path: Path) -> LaunchContext:
    return LaunchContext(
        base_root=Path(__file__).resolve().parents[3],
        runtime_root=tmp_path / "runtime",
        python_executable=Path(__file__).resolve().parents[3] / ".venv" / "bin" / "python",
        launch_nonce="n" * 43,
    )


def test_child_environment_is_clean_private_and_contains_only_hub_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Removing the clean builder must not leak provider or Codex credentials to an import child."""
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-cross")
    monkeypatch.setenv("CODEX_HOME", "/must/not/cross")

    environment = child_environment(_context(tmp_path), "a" * 64, "b" * 64)

    assert environment["PYTHONDONTWRITEBYTECODE"] == "1"
    assert environment["BASE_TOOL_HUB_LAUNCH_NONCE"] == "n" * 43
    assert environment["BASE_TOOL_HUB_ADAPTER_SHA256"] == "a" * 64
    assert environment["BASE_TOOL_HUB_ROOT_FINGERPRINT"] == "b" * 64
    assert "OPENAI_API_KEY" not in environment
    assert "CODEX_HOME" not in environment
    assert Path(environment["PYTHONPYCACHEPREFIX"]).is_dir()
    assert not any(Path(environment["PYTHONPYCACHEPREFIX"]).iterdir())
    assert stat.S_IMODE(Path(environment["PYTHONPYCACHEPREFIX"]).stat().st_mode) == 0o700


def test_child_environment_rejects_a_replaced_python_cache_directory(tmp_path: Path) -> None:
    """A symlinked cache can make import mode execute attacker-selected bytecode."""
    context = _context(tmp_path)
    cache = context.runtime_root / "pycache"
    cache.parent.mkdir()
    (tmp_path / "outside").mkdir()
    cache.symlink_to(tmp_path / "outside", target_is_directory=True)

    with pytest.raises(EnvironmentError, match="cache"):
        child_environment(context, "a" * 64, "b" * 64)


def test_child_environment_rejects_a_symlinked_runtime_parent(tmp_path: Path) -> None:
    """A replaced runtime parent must not host a child cache or startup report."""
    outside = tmp_path / "outside"
    outside.mkdir()
    runtime = tmp_path / "runtime"
    runtime.symlink_to(outside, target_is_directory=True)
    context = LaunchContext(
        base_root=Path(__file__).resolve().parents[3],
        runtime_root=runtime,
        python_executable=Path(__file__).resolve().parents[3] / ".venv" / "bin" / "python",
        launch_nonce="n" * 43,
    )

    with pytest.raises(EnvironmentError, match="runtime"):
        child_environment(context, "a" * 64, "b" * 64)
