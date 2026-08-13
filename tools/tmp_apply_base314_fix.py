#!/usr/bin/env python3
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools/project_operating_contract.py"
BRANCH = "fix/base314-protected-directory-descendants-20260814"
OLD = '''def _protected_match(path: str, patterns: list[str]) -> bool:\n    normalized = _normalized_path(path)\n    return any(fnmatch.fnmatchcase(normalized, _normalized_path(pattern)) for pattern in patterns)\n'''
NEW = '''def _matches_normalized_protected_pattern(path: str, pattern: str) -> bool:\n    candidate = path.rstrip(\"/\")\n    if pattern.endswith(\"/\"):\n        directory = pattern.rstrip(\"/\")\n        return candidate == directory or candidate.startswith(f\"{directory}/\")\n    return fnmatch.fnmatchcase(candidate, pattern)\n\n\ndef _protected_match(path: str, patterns: list[str]) -> bool:\n    normalized = _normalized_path(path)\n    return any(\n        _matches_normalized_protected_pattern(normalized, _normalized_path(pattern))\n        for pattern in patterns\n    )\n'''

def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)

def main() -> int:
    source = TARGET.read_text(encoding="utf-8")
    if source.count(OLD) != 1:
        raise RuntimeError("approved matcher source not found exactly once")
    TARGET.write_text(source.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
    run(sys.executable, "-m", "unittest", "tests.test_protected_path_descendant_matching", "tests.test_v9_1_project_operating_contract", "tests.test_approved_protected_change_gate", "-v")
    run("git", "diff", "--check")
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", TARGET.relative_to(ROOT).as_posix())
    run("git", "commit", "-m", "fix: protect descendant project paths")
    run("git", "push", "origin", f"HEAD:{BRANCH}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
