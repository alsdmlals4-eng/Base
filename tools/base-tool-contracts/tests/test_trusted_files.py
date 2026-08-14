from __future__ import annotations

import os
from pathlib import Path

from base_tool_contracts import trusted_files


def test_windows_git_search_uses_standard_install_and_absolute_path_entries(tmp_path: Path) -> None:
    program_files = tmp_path / "Program Files"
    path_entry = tmp_path / "custom-git" / "cmd"
    search = trusted_files._trusted_git_search_path(
        {
            "ProgramFiles": str(program_files),
            "PATH": ";".join((".", "relative", str(path_entry))),
        },
        platform="nt",
    ).split(";")

    assert str(program_files / "Git" / "cmd") in search
    assert str(path_entry) in search
    assert "." not in search
    assert "relative" not in search
