from __future__ import annotations

import os
from pathlib import Path
import sys

import pytest

from base_tool_contracts import trusted_files
from tool_hub.adapters import bind_launch_spec, build_launch_spec
from tool_hub.environment import LaunchContext
from tool_hub.projects import ProjectBinding
from tool_hub.registry import load_reviewed_tools


pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows reviewed launch contract")
BASE_ROOT = Path(__file__).resolve().parents[3]


def project(tmp_path: Path) -> ProjectBinding:
    root = tmp_path / "Project With Spaces"
    root.mkdir()
    return ProjectBinding(
        project_id="demo-game",
        root=root,
        repository="owner/demo-game",
        engine="Godot 4.7",
        fingerprint="b" * 64,
        adapter_sha256="a" * 64,
        protected_paths=("project.godot",),
        validator_sha256="c" * 64,
    )


def test_windows_registry_marks_reviewed_tools_launch_supported() -> None:
    tools = load_reviewed_tools(BASE_ROOT)

    assert {tool["_launch_supported"] for tool in tools} == {True}
    assert all(len(str(tool["_source_sha256"])) == 64 for tool in tools)
    assert all(len(str(tool["_interpreter_sha256"])) == 64 for tool in tools)
    assert all(len(str(tool["_environment_sha256"])) == 64 for tool in tools)


def test_windows_build_launch_spec_uses_reviewed_venv_without_proc_descriptors(tmp_path: Path) -> None:
    tool = next(tool for tool in load_reviewed_tools(BASE_ROOT) if tool["tool_id"] == "expression-studio")
    interpreter = BASE_ROOT / ".venv" / "Scripts" / "python.exe"
    context = LaunchContext(BASE_ROOT, tmp_path / "runtime", interpreter, "n" * 43)

    spec = build_launch_spec(tool, project(tmp_path), context)
    bound = bind_launch_spec(spec)

    assert Path(bound.argv[0]).samefile(interpreter)
    assert bound.cwd == BASE_ROOT / "tools" / "expression-studio"
    assert bound.pass_fds == ()
    assert not any("/proc/self/fd" in value for value in map(str, bound.argv))
    assert "OPENAI_API_KEY" not in bound.env
    assert "CODEX_HOME" not in bound.env
    assert bound.env.get("SystemRoot") or bound.env.get("WINDIR")


def test_windows_child_preserves_only_standard_git_locator_variables(tmp_path: Path) -> None:
    tool = next(tool for tool in load_reviewed_tools(BASE_ROOT) if tool["tool_id"] == "expression-studio")
    context = LaunchContext(
        BASE_ROOT,
        tmp_path / "runtime",
        BASE_ROOT / ".venv" / "Scripts" / "python.exe",
        "n" * 43,
    )

    environment = build_launch_spec(tool, project(tmp_path), context).env

    for name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        if value := os.environ.get(name):
            assert environment.get(name) == value
    assert environment["PATH"] == os.defpath
    assert "OPENAI_API_KEY" not in environment
    assert "CODEX_HOME" not in environment


def test_windows_portable_git_uses_reviewed_executable_resolver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reviewed = trusted_files.trusted_git_executable()
    original_which = trusted_files.shutil.which

    def reviewed_only(name: str, path: str | None = None) -> str | None:
        if path is None:
            return None
        return original_which(name, path=path)

    monkeypatch.setattr(trusted_files.shutil, "which", reviewed_only)

    completed = trusted_files.run_portable_git(BASE_ROOT, "rev-parse", "--git-dir")

    assert completed.returncode == 0


def test_windows_site_packages_path_is_lib_site_packages(tmp_path: Path) -> None:
    tool = next(tool for tool in load_reviewed_tools(BASE_ROOT) if tool["tool_id"] == "qa-evidence-studio")
    context = LaunchContext(
        BASE_ROOT,
        tmp_path / "runtime",
        BASE_ROOT / ".venv" / "Scripts" / "python.exe",
        "n" * 43,
    )

    spec = build_launch_spec(tool, project(tmp_path), context)
    code_index = spec.argv.index("-c")
    site_packages = Path(spec.argv[code_index + 4])

    assert site_packages == BASE_ROOT / ".venv" / "Lib" / "site-packages"
    assert site_packages.is_dir()
