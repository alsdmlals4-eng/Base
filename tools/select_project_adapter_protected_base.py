#!/usr/bin/env python3
"""Select the trusted protected baseline for project-adapter pull-request validation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ADAPTER_PATH = "skills/PROJECT_BASE_ADAPTER.json"
FULL_SHA = re.compile(r"[0-9a-f]{40}")


class BaselineSelectionError(ValueError):
    """A fail-closed trusted-baseline selection error."""


def _git(project_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(project_root), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _require_commit(project_root: Path, commit: str, label: str) -> str:
    if not FULL_SHA.fullmatch(commit):
        raise BaselineSelectionError(f"{label} must be a full lowercase 40-hex commit SHA")
    if _git(project_root, "cat-file", "-e", f"{commit}^{{commit}}").returncode:
        raise BaselineSelectionError(f"{label} is not available in the project repository: {commit}")
    return commit


def _require_ancestor(project_root: Path, ancestor: str, descendant: str, label: str) -> None:
    if _git(project_root, "merge-base", "--is-ancestor", ancestor, descendant).returncode:
        raise BaselineSelectionError(f"{label} is not an ancestor of {descendant}: {ancestor}")


def _adapter_changed(project_root: Path, pull_request_base: str) -> bool:
    result = _git(
        project_root,
        "diff",
        "--name-only",
        "--no-renames",
        f"{pull_request_base}...HEAD",
        "--",
        ADAPTER_PATH,
    )
    if result.returncode:
        raise BaselineSelectionError(
            "Cannot compare the pull-request head with its immutable base for adapter changes"
        )
    return ADAPTER_PATH in {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _baseline_recorded_at_base(project_root: Path, pull_request_base: str) -> str:
    result = _git(project_root, "show", f"{pull_request_base}:{ADAPTER_PATH}")
    if result.returncode:
        raise BaselineSelectionError(
            f"The immutable pull-request base does not contain {ADAPTER_PATH}"
        )
    try:
        payload = json.loads(result.stdout)
        baseline = payload["protected_baseline"]["commit"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise BaselineSelectionError(
            "The immutable pull-request base adapter has no valid protected_baseline.commit"
        ) from error
    if not isinstance(baseline, str):
        raise BaselineSelectionError(
            "The immutable pull-request base adapter protected_baseline.commit must be a string"
        )
    return _require_commit(project_root, baseline, "Recorded protected baseline")


def select_protected_base(project_root: Path, pull_request_base: str) -> str:
    root = project_root.resolve()
    base = _require_commit(root, pull_request_base, "Pull-request base")
    head_result = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
    if head_result.returncode:
        raise BaselineSelectionError("Cannot resolve the pull-request HEAD commit")
    head = _require_commit(root, head_result.stdout.strip(), "Pull-request HEAD")
    _require_ancestor(root, base, head, "Pull-request base")

    if _adapter_changed(root, base):
        # Adapter migration PR: trust the immutable pull-request base as the new protected baseline.
        return base

    # Normal PR: trust the baseline recorded by the adapter at the immutable pull-request base.
    baseline = _baseline_recorded_at_base(root, base)
    _require_ancestor(root, baseline, base, "Recorded protected baseline")
    return baseline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--pull-request-base", required=True)
    options = parser.parse_args()
    try:
        selected = select_protected_base(options.project_root, options.pull_request_base)
    except BaselineSelectionError as error:
        print(f"Project adapter baseline selection failed: {error}", file=sys.stderr)
        return 1
    print(selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
