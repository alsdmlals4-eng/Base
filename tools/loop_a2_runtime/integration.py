from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping, Protocol

from .evidence import canonical_receipt
from .protocol import ProtocolError, normalize_contract_path


_IDENTIFIER = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_SAFE_ENV_KEYS = (
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "HOME",
    "USERPROFILE",
)


class IntegrationError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class PullRequestSnapshot:
    number: int
    state: str
    merged: bool
    head_sha: str
    merge_sha: str | None
    required_checks: str
    unresolved_threads: int
    current_main_sha: str | None
    merge_in_main: bool


@dataclass(frozen=True)
class HandoffResult:
    project_id: str
    run_id: str
    package_id: str
    run_receipt_digest: str
    branch_name: str
    reviewed_head_sha: str
    pr: PullRequestSnapshot


@dataclass(frozen=True)
class PostmergeEvidence:
    pr_number: int
    merged: bool
    pr_head_sha: str
    merge_sha: str | None
    required_checks: str
    unresolved_threads: int
    current_main_sha: str
    merge_in_main: bool
    project_id: str
    run_id: str
    package_id: str
    coverage_status: str
    planning_drift: str
    visual_drift: str


class PullRequestProvider(Protocol):
    def preflight(self) -> None:
        ...

    def open_pull_request(
        self,
        *,
        branch_name: str,
        head_sha: str,
        title: str,
        body: str,
    ) -> PullRequestSnapshot:
        ...


def _safe_environment() -> dict[str, str]:
    result = {
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
    }
    for key in _SAFE_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            result[key] = value
    return result


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        env=_safe_environment(),
        check=False,
    )
    if check and completed.returncode != 0:
        raise IntegrationError("GIT_COMMAND_FAILED", f"git {' '.join(args[:2])} failed")
    return completed


def _safe_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise IntegrationError("IDENTIFIER_INVALID", f"{label} is not a closed identifier")
    return value


def _safe_sha(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise IntegrationError("SHA_INVALID", f"{label} must be a lowercase 40-character SHA")
    return value


def _verify_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(receipt)
    digest = value.pop("receipt_digest", None)
    if not isinstance(digest, str):
        raise IntegrationError("RECEIPT_DIGEST_MISSING", "run receipt digest is missing")
    expected = canonical_receipt(value)["receipt_digest"]
    if digest != expected:
        raise IntegrationError("RECEIPT_DIGEST_MISMATCH", "run receipt digest does not match its payload")
    value["receipt_digest"] = digest
    return value


def _changed_paths(repo: Path) -> tuple[str, ...]:
    tracked = _git(repo, "diff", "--name-only", "--no-renames", "-z", "HEAD", "--").stdout
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z").stdout
    ignored = _git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "-z").stdout
    ignored_paths = tuple(item for item in ignored.split("\0") if item)
    if ignored_paths:
        raise IntegrationError(
            "IGNORED_UNTRACKED_WRITE",
            "reviewed worktree contains ignored untracked files that cannot be handed off without force-add",
        )
    values = {item for item in (tracked + untracked).split("\0") if item}
    normalized: list[str] = []
    for value in values:
        try:
            normalized.append(normalize_contract_path(value, "changed_path"))
        except ProtocolError as exc:
            raise IntegrationError("CHANGED_PATHS_UNSAFE", str(exc)) from exc
    return tuple(sorted(normalized, key=lambda item: (item.casefold(), item)))


def _receipt_changed_paths(receipt: Mapping[str, Any]) -> tuple[str, ...]:
    raw = receipt.get("changed_paths")
    if not isinstance(raw, list) or not raw:
        raise IntegrationError("CHANGED_PATHS_INVALID", "run receipt must contain a non-empty changed_paths array")
    normalized: list[str] = []
    for item in raw:
        if not isinstance(item, str):
            raise IntegrationError("CHANGED_PATHS_INVALID", "changed_paths entries must be strings")
        try:
            normalized.append(normalize_contract_path(item, "changed_path"))
        except ProtocolError as exc:
            raise IntegrationError("CHANGED_PATHS_UNSAFE", str(exc)) from exc
    if len({item.casefold() for item in normalized}) != len(normalized):
        raise IntegrationError("CHANGED_PATHS_INVALID", "changed_paths contains normalized duplicates")
    return tuple(sorted(normalized, key=lambda item: (item.casefold(), item)))


def _branch_name(project_id: str, run_id: str) -> str:
    project = _safe_identifier(project_id, "project_id").casefold()
    run = _safe_identifier(run_id, "run_id").casefold()
    return f"loop-a2/{project}/{run}"


class A2Integration:
    def __init__(self, *, repo_root: Path | str, provider: PullRequestProvider) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        probe = _git(self.repo_root, "rev-parse", "--git-dir", check=False)
        if probe.returncode != 0:
            raise IntegrationError("GIT_REPOSITORY_INVALID", "repo_root is not a Git repository")
        self.provider = provider

    def _validate_handoff_receipt(
        self,
        receipt: Mapping[str, Any],
        *,
        expected_project_id: str,
        expected_run_id: str,
        expected_package_id: str,
    ) -> dict[str, Any]:
        expected_project_id = _safe_identifier(expected_project_id, "expected_project_id")
        expected_run_id = _safe_identifier(expected_run_id, "expected_run_id")
        expected_package_id = _safe_identifier(expected_package_id, "expected_package_id")
        value = _verify_receipt(receipt)
        if value.get("contract_role") != "LOOP_A2_RUN_RECEIPT":
            raise IntegrationError("RECEIPT_ROLE_INVALID", "handoff requires LOOP_A2_RUN_RECEIPT")
        if value.get("state") != "WAITING_INTEGRATION":
            raise IntegrationError("HANDOFF_STATE_INVALID", "handoff requires WAITING_INTEGRATION")
        if value.get("finding_codes") != []:
            raise IntegrationError("HANDOFF_FINDINGS_PRESENT", "handoff receipt must contain no findings")
        if value.get("critic_verdict") != "PASS":
            raise IntegrationError("HANDOFF_CRITIC_INVALID", "handoff requires critic PASS")
        expected = (expected_project_id, expected_run_id, expected_package_id)
        actual = (value.get("project_id"), value.get("run_id"), value.get("package_id"))
        if actual != expected:
            raise IntegrationError("HANDOFF_IDENTITY_MISMATCH", "receipt identity differs from requested handoff")
        _safe_identifier(value.get("project_id"), "project_id")
        _safe_identifier(value.get("run_id"), "run_id")
        _safe_identifier(value.get("package_id"), "package_id")
        _safe_sha(value.get("expected_main_sha"), "expected_main_sha")
        return value

    def handoff(
        self,
        *,
        receipt: Mapping[str, Any],
        expected_project_id: str,
        expected_run_id: str,
        expected_package_id: str,
    ) -> HandoffResult:
        value = self._validate_handoff_receipt(
            receipt,
            expected_project_id=expected_project_id,
            expected_run_id=expected_run_id,
            expected_package_id=expected_package_id,
        )
        self.provider.preflight()

        expected_main_sha = str(value["expected_main_sha"])
        current_head = _git(self.repo_root, "rev-parse", "HEAD").stdout.strip()
        if current_head != expected_main_sha:
            raise IntegrationError("STALE_BASE_SHA", "worktree HEAD differs from reviewed expected main SHA")

        actual_paths = _changed_paths(self.repo_root)
        reviewed_paths = _receipt_changed_paths(value)
        if actual_paths != reviewed_paths:
            raise IntegrationError(
                "CHANGED_PATHS_MISMATCH",
                f"actual changed paths {actual_paths!r} differ from reviewed paths {reviewed_paths!r}",
            )

        branch_name = _branch_name(expected_project_id, expected_run_id)
        exists = _git(
            self.repo_root,
            "show-ref",
            "--verify",
            "--quiet",
            f"refs/heads/{branch_name}",
            check=False,
        )
        if exists.returncode == 0:
            raise IntegrationError("HANDOFF_BRANCH_EXISTS", "generated handoff branch already exists")

        _git(self.repo_root, "switch", "-c", branch_name)
        _git(self.repo_root, "add", "-A")
        staged = _git(self.repo_root, "diff", "--cached", "--name-only", "--no-renames", "-z").stdout
        staged_paths = tuple(
            sorted(
                (normalize_contract_path(item, "staged_path") for item in staged.split("\0") if item),
                key=lambda item: (item.casefold(), item),
            )
        )
        if staged_paths != reviewed_paths:
            raise IntegrationError("STAGED_PATHS_MISMATCH", "staged paths differ from reviewed changed paths")

        _git(
            self.repo_root,
            "commit",
            "-m",
            f"loop-a2: {expected_project_id} {expected_run_id} {expected_package_id}",
        )
        reviewed_head_sha = _git(self.repo_root, "rev-parse", "HEAD").stdout.strip()
        _safe_sha(reviewed_head_sha, "reviewed_head_sha")
        _git(
            self.repo_root,
            "push",
            "origin",
            f"HEAD:refs/heads/{branch_name}",
        )
        pr = self.provider.open_pull_request(
            branch_name=branch_name,
            head_sha=reviewed_head_sha,
            title=f"loop-a2: {expected_project_id} {expected_run_id}",
            body=(
                f"Automated A2 handoff for `{expected_project_id}` / `{expected_run_id}` / "
                f"`{expected_package_id}`. Reviewed receipt `{value['receipt_digest']}`. "
                "Merge is intentionally not performed by the integration layer."
            ),
        )
        if pr.head_sha != reviewed_head_sha:
            raise IntegrationError("PR_HEAD_MISMATCH", "PR provider returned a different head SHA")
        return HandoffResult(
            project_id=expected_project_id,
            run_id=expected_run_id,
            package_id=expected_package_id,
            run_receipt_digest=str(value["receipt_digest"]),
            branch_name=branch_name,
            reviewed_head_sha=reviewed_head_sha,
            pr=pr,
        )

    def close_postmerge(
        self,
        *,
        run_receipt: Mapping[str, Any],
        handoff: HandoffResult,
        evidence: PostmergeEvidence,
        receipt_path: Path | str,
    ) -> dict[str, Any]:
        run_value = _verify_receipt(run_receipt)
        if run_value.get("state") != "WAITING_INTEGRATION":
            raise IntegrationError("CLOSURE_RUN_STATE_INVALID", "closure requires WAITING_INTEGRATION source receipt")
        if str(run_value.get("receipt_digest")) != handoff.run_receipt_digest:
            raise IntegrationError("CLOSURE_RECEIPT_MISMATCH", "handoff does not refer to this run receipt")
        identity = (handoff.project_id, handoff.run_id, handoff.package_id)
        if identity != (evidence.project_id, evidence.run_id, evidence.package_id):
            raise IntegrationError("CLOSURE_IDENTITY_MISMATCH", "postmerge evidence identity differs from handoff")
        if evidence.pr_number != handoff.pr.number:
            raise IntegrationError("CLOSURE_PR_MISMATCH", "postmerge evidence refers to another PR")
        if not evidence.merged:
            raise IntegrationError("PR_NOT_MERGED", "PR is not merged")
        if evidence.pr_head_sha != handoff.reviewed_head_sha:
            raise IntegrationError("PR_HEAD_MISMATCH", "merged PR head differs from reviewed handoff head")
        if evidence.merge_sha is None:
            raise IntegrationError("MERGE_SHA_MISSING", "merged PR has no merge SHA")
        _safe_sha(evidence.merge_sha, "merge_sha")
        _safe_sha(evidence.current_main_sha, "current_main_sha")
        if evidence.required_checks != "PASS":
            raise IntegrationError("REQUIRED_CHECKS_NOT_PASS", "required checks are not all PASS")
        if evidence.unresolved_threads != 0:
            raise IntegrationError("UNRESOLVED_REVIEW_THREADS", "review threads remain unresolved")
        if not evidence.merge_in_main:
            raise IntegrationError("MERGE_NOT_IN_MAIN", "merge SHA is not contained in current main")
        if evidence.coverage_status != "COMPLETE":
            raise IntegrationError("COVERAGE_INCOMPLETE", "Requirement Coverage is not complete")
        if evidence.planning_drift not in {"NO_DRIFT", "MINOR_TECHNICAL_DRIFT"}:
            raise IntegrationError("PLANNING_DRIFT", "Planning Drift is not clean")
        if evidence.visual_drift not in {"NOT_APPLICABLE", "NO_DRIFT", "MINOR_TECHNICAL_DRIFT"}:
            raise IntegrationError("VISUAL_DRIFT", "Visual Drift is not clean")

        path = Path(receipt_path)
        if path.exists():
            raise IntegrationError("CLOSURE_EXISTS", "immutable closure receipt already exists")
        payload = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_POSTMERGE_RECEIPT",
            "project_id": handoff.project_id,
            "run_id": handoff.run_id,
            "package_id": handoff.package_id,
            "state": "CLOSED",
            "run_receipt_digest": handoff.run_receipt_digest,
            "reviewed_head_sha": handoff.reviewed_head_sha,
            "pr_number": evidence.pr_number,
            "merge_sha": evidence.merge_sha,
            "current_main_sha": evidence.current_main_sha,
            "required_checks": "PASS",
            "unresolved_threads": 0,
            "coverage_status": evidence.coverage_status,
            "planning_drift": evidence.planning_drift,
            "visual_drift": evidence.visual_drift,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }
        closed = canonical_receipt(payload)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("x", encoding="utf-8") as handle:
                json.dump(closed, handle, ensure_ascii=False, sort_keys=True, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError as exc:
            raise IntegrationError("CLOSURE_EXISTS", "immutable closure receipt appeared concurrently") from exc
        return closed
