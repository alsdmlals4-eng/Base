#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


REQUIRED_CONTEXT = "ci-gate"


@dataclass(frozen=True)
class PullRequestState:
    head_sha: str
    base_ref: str
    merge_commit_sha: str | None


def _environment(environment: Mapping[str, str] | None) -> dict[str, str]:
    if environment is None:
        return dict(os.environ)
    return dict(environment)


def _run(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    environment: Mapping[str, str] | None = None,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    values = [str(value) for value in command]
    return subprocess.run(
        values,
        cwd=cwd,
        env=_environment(environment),
        capture_output=capture_output,
        text=True,
        check=False,
    )


def _require_success(
    result: subprocess.CompletedProcess[str],
    description: str,
) -> subprocess.CompletedProcess[str]:
    if result.returncode == 0:
        return result
    detail = (result.stderr or result.stdout or "").strip()
    suffix = f": {detail}" if detail else ""
    raise RuntimeError(f"{description} failed{suffix}")


def read_pull_request(
    repo: str,
    pr: int,
    *,
    environment: Mapping[str, str] | None = None,
) -> PullRequestState:
    result = _require_success(
        _run(
            ("gh", "api", f"repos/{repo}/pulls/{pr}"),
            environment=environment,
        ),
        "GitHub pull request lookup",
    )
    try:
        payload = json.loads(result.stdout)
        if payload.get("state") != "open":
            raise RuntimeError("pull request must be open")
        head_sha = payload["head"]["sha"]
        base_ref = payload["base"]["ref"]
        merge_commit_sha = payload.get("merge_commit_sha")
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("GitHub pull request response is incomplete") from error
    if not isinstance(head_sha, str) or not head_sha:
        raise RuntimeError("GitHub pull request head SHA is missing")
    if not isinstance(base_ref, str) or not base_ref:
        raise RuntimeError("GitHub pull request base ref is missing")
    if merge_commit_sha is not None and not isinstance(merge_commit_sha, str):
        raise RuntimeError("GitHub pull request merge SHA is invalid")
    return PullRequestState(head_sha, base_ref, merge_commit_sha)


def ci_gate_check_exists(
    repo: str,
    sha: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> bool:
    result = _require_success(
        _run(
            ("gh", "api", f"repos/{repo}/commits/{sha}/check-runs"),
            environment=environment,
        ),
        f"GitHub Check Run lookup for {sha}",
    )
    try:
        payload = json.loads(result.stdout)
        check_runs = payload["check_runs"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("GitHub Check Run response is incomplete") from error
    if not isinstance(check_runs, list):
        raise RuntimeError("GitHub Check Run response is invalid")
    return any(
        isinstance(check, dict) and check.get("name") == REQUIRED_CONTEXT
        for check in check_runs
    )


def _git_output(
    root: Path,
    *args: str,
    environment: Mapping[str, str] | None = None,
) -> str:
    result = _require_success(
        _run(("git", *args), cwd=root, environment=environment),
        f"git {' '.join(args)}",
    )
    return result.stdout.strip()


def assert_clean_exact_head(
    root: Path,
    expected_head: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> None:
    actual_head = _git_output(root, "rev-parse", "HEAD", environment=environment)
    if actual_head != expected_head:
        raise RuntimeError(
            f"local HEAD {actual_head} does not match PR head {expected_head}"
        )
    status = _git_output(root, "status", "--porcelain", environment=environment)
    if status:
        raise RuntimeError("worktree must be clean before publishing fallback evidence")


def assert_base_is_ancestor(
    root: Path,
    base: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> None:
    _require_success(
        _run(("git", "fetch", "origin", base), cwd=root, environment=environment),
        f"git fetch origin {base}",
    )
    result = _run(
        ("git", "merge-base", "--is-ancestor", f"origin/{base}", "HEAD"),
        cwd=root,
        environment=environment,
    )
    if result.returncode != 0:
        raise RuntimeError(f"local HEAD is not up to date with origin/{base}")


def _assert_no_ci_gate_check(
    repo: str,
    sha: str | None,
    *,
    environment: Mapping[str, str] | None = None,
) -> None:
    if sha and ci_gate_check_exists(repo, sha, environment=environment):
        raise RuntimeError(
            f"{REQUIRED_CONTEXT} Check Run already exists for {sha}; "
            "LOCAL_FALLBACK cannot replace REMOTE_CI"
        )


def publish_success_status(
    repo: str,
    sha: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> None:
    _require_success(
        _run(
            (
                "gh",
                "api",
                "--method",
                "POST",
                f"repos/{repo}/statuses/{sha}",
                "-f",
                "state=success",
                "-f",
                f"context={REQUIRED_CONTEXT}",
                "-f",
                "description=LOCAL_FALLBACK validated exact head SHA",
            ),
            environment=environment,
        ),
        "GitHub commit status publish",
    )


def run_local_fallback(
    root: Path,
    repo: str,
    pr: int,
    base: str,
    trusted_history_commit: str,
    python: str,
    *,
    environment: Mapping[str, str] | None = None,
) -> int:
    repository_root = root.resolve()
    env = _environment(environment)

    _require_success(
        _run(("gh", "auth", "status"), environment=env),
        "GitHub authentication check",
    )

    initial_pr = read_pull_request(repo, pr, environment=env)
    if initial_pr.base_ref != base:
        raise RuntimeError(
            f"PR base {initial_pr.base_ref} does not match expected base {base}"
        )

    original_head = initial_pr.head_sha
    assert_clean_exact_head(repository_root, original_head, environment=env)
    assert_base_is_ancestor(repository_root, base, environment=env)
    _assert_no_ci_gate_check(repo, original_head, environment=env)
    _assert_no_ci_gate_check(repo, initial_pr.merge_commit_sha, environment=env)

    validation = _run(
        (
            python,
            "tools/run_local_validation.py",
            "--trusted-history-commit",
            trusted_history_commit,
        ),
        cwd=repository_root,
        environment=env,
        capture_output=False,
    )
    if validation.returncode != 0:
        return validation.returncode

    assert_clean_exact_head(repository_root, original_head, environment=env)
    current_pr = read_pull_request(repo, pr, environment=env)
    if current_pr.base_ref != base:
        raise RuntimeError("PR base changed during local validation")
    if current_pr.head_sha != original_head:
        raise RuntimeError("PR head changed during local validation")

    _assert_no_ci_gate_check(repo, original_head, environment=env)
    _assert_no_ci_gate_check(repo, current_pr.merge_commit_sha, environment=env)
    publish_success_status(repo, original_head, environment=env)

    print("LOCAL FALLBACK CI GATE: PASS")
    print("mode: LOCAL_FALLBACK")
    print(f"head_sha: {original_head}")
    print(f"required_context: {REQUIRED_CONTEXT}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--trusted-history-commit", required=True)
    parser.add_argument("--base", default="main")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    try:
        return run_local_fallback(
            repository_root,
            args.repo,
            args.pr,
            args.base,
            args.trusted_history_commit,
            args.python,
        )
    except RuntimeError as error:
        print(f"LOCAL FALLBACK CI GATE: BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
