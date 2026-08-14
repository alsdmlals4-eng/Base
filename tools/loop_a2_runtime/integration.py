from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any, Mapping, Protocol

from .evidence import canonical_receipt
from .protocol import ProtocolError, normalize_contract_path


_IDENTIFIER = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
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
    reviewed_diff_sha256: str
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
    requires_trusted_attestation: bool

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


def _git_bytes(repo: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        env=_safe_environment(),
        check=False,
    )
    if completed.returncode != 0:
        raise IntegrationError("GIT_COMMAND_FAILED", f"git {' '.join(args[:2])} failed")
    return completed.stdout


def _safe_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise IntegrationError("IDENTIFIER_INVALID", f"{label} is not a closed identifier")
    return value


def _safe_sha(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA.fullmatch(value) is None:
        raise IntegrationError("SHA_INVALID", f"{label} must be a lowercase 40-character SHA")
    return value


def _safe_digest(value: object, label: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise IntegrationError("DIFF_ATTESTATION_INVALID", f"{label} must be a lowercase SHA-256 digest")
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


def _nul_paths(value: str) -> tuple[str, ...]:
    return tuple(item for item in value.split("\0") if item)


def _all_untracked_paths(repo: Path) -> tuple[str, ...]:
    value = _git(repo, "ls-files", "--others", "-z").stdout
    normalized: list[str] = []
    for raw in _nul_paths(value):
        try:
            normalized.append(normalize_contract_path(raw, "untracked_path"))
        except ProtocolError as exc:
            raise IntegrationError("CHANGED_PATHS_UNSAFE", str(exc)) from exc
    return tuple(sorted(set(normalized), key=lambda item: (item.casefold(), item)))


def compute_worktree_diff_sha256(repo: Path | str) -> str:
    """Digest reviewed Git content, not only filenames.

    The digest covers the current HEAD, binary Git diff, and bytes/symlink targets
    for every untracked path (including ignored paths). It is stable for the same
    worktree content and changes when content changes under an already-reviewed path.
    """

    root = Path(repo).resolve(strict=True)
    head = _git(root, "rev-parse", "HEAD").stdout.strip()
    _safe_sha(head, "worktree_head")
    tracked_diff = _git_bytes(
        root,
        "diff",
        "--binary",
        "--no-ext-diff",
        "--no-renames",
        "HEAD",
        "--",
    )
    digest = hashlib.sha256()
    digest.update(b"LOOP_A2_REVIEWED_DIFF_V1\0")
    digest.update(head.encode("ascii"))
    digest.update(b"\0TRACKED\0")
    digest.update(len(tracked_diff).to_bytes(8, "big"))
    digest.update(tracked_diff)
    for relative in _all_untracked_paths(root):
        path = root.joinpath(*relative.split("/"))
        digest.update(b"\0UNTRACKED\0")
        encoded_path = relative.encode("utf-8")
        digest.update(len(encoded_path).to_bytes(4, "big"))
        digest.update(encoded_path)
        if path.is_symlink():
            payload = os.readlink(path).encode("utf-8", errors="surrogateescape")
            kind = b"L"
        elif path.is_file():
            payload = path.read_bytes()
            kind = b"F"
        else:
            payload = b""
            kind = b"O"
        digest.update(kind)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


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


def _checks_state(rollup: object) -> str:
    if not isinstance(rollup, list) or not rollup:
        return "PENDING"
    pending = False
    for item in rollup:
        if not isinstance(item, dict):
            return "FAIL"
        status = str(item.get("status") or "").upper()
        conclusion = str(item.get("conclusion") or "").upper()
        if status and status != "COMPLETED":
            pending = True
            continue
        if conclusion in {"SUCCESS", "NEUTRAL", "SKIPPED"}:
            continue
        if not conclusion:
            pending = True
            continue
        return "FAIL"
    return "PENDING" if pending else "PASS"


class GhPullRequestProvider:
    """Bounded gh CLI transport for PR creation and direct postmerge evidence."""

    requires_trusted_attestation = True

    def __init__(self, *, repo_root: Path | str, executable: Path | str = "gh") -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self._requested_executable = str(executable)
        self._executable: str | None = None
        self._repo_slug: str | None = None

    def _resolve_executable(self) -> str:
        requested = self._requested_executable
        candidate = Path(requested)
        if candidate.is_absolute() or candidate.parent != Path("."):
            if not candidate.is_file():
                raise IntegrationError("GH_UNAVAILABLE", "configured gh executable does not exist")
            return str(candidate)
        resolved = shutil.which(requested)
        if not resolved:
            raise IntegrationError("GH_UNAVAILABLE", "gh CLI is not available")
        return resolved

    def _gh(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        executable = self._executable or self._resolve_executable()
        completed = subprocess.run(
            [executable, *args],
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            env=_safe_environment(),
            timeout=30,
            check=False,
        )
        if check and completed.returncode != 0:
            raise IntegrationError("GH_COMMAND_FAILED", f"gh {args[0] if args else 'command'} failed")
        return completed

    def preflight(self) -> None:
        self._executable = self._resolve_executable()
        auth = self._gh("auth", "status", "--hostname", "github.com", check=False)
        if auth.returncode != 0:
            raise IntegrationError("GH_UNAUTHENTICATED", "gh CLI is not authenticated for github.com")
        repo = self._gh("repo", "view", "--json", "nameWithOwner")
        try:
            payload = json.loads(repo.stdout)
            slug = payload["nameWithOwner"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise IntegrationError("GH_PROTOCOL_INVALID", "gh repo view returned invalid JSON") from exc
        if not isinstance(slug, str) or "/" not in slug:
            raise IntegrationError("GH_PROTOCOL_INVALID", "gh repository identity is invalid")
        self._repo_slug = slug

    def _pr_snapshot(self, selector: str | int) -> PullRequestSnapshot:
        completed = self._gh(
            "pr",
            "view",
            str(selector),
            "--json",
            "number,state,headRefOid,mergeCommit,statusCheckRollup",
        )
        try:
            value = json.loads(completed.stdout)
            state = str(value["state"]).lower()
            head_sha = _safe_sha(value["headRefOid"], "pr_head_sha")
            merge_value = value.get("mergeCommit")
            merge_sha = merge_value.get("oid") if isinstance(merge_value, dict) else None
            if merge_sha is not None:
                _safe_sha(merge_sha, "merge_sha")
            number = int(value["number"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, IntegrationError):
                raise
            raise IntegrationError("GH_PROTOCOL_INVALID", "gh pr view returned invalid JSON") from exc
        return PullRequestSnapshot(
            number=number,
            state=state,
            merged=state == "merged",
            head_sha=head_sha,
            merge_sha=merge_sha,
            required_checks=_checks_state(value.get("statusCheckRollup")),
            unresolved_threads=0,
            current_main_sha=None,
            merge_in_main=False,
        )

    def open_pull_request(
        self,
        *,
        branch_name: str,
        head_sha: str,
        title: str,
        body: str,
    ) -> PullRequestSnapshot:
        self.preflight()
        created = self._gh(
            "pr",
            "create",
            "--head",
            branch_name,
            "--base",
            "main",
            "--title",
            title,
            "--body",
            body,
        )
        url = created.stdout.strip().splitlines()[-1] if created.stdout.strip() else ""
        if not url.startswith("https://"):
            raise IntegrationError("GH_PROTOCOL_INVALID", "gh pr create did not return a PR URL")
        snapshot = self._pr_snapshot(url)
        if snapshot.head_sha != head_sha:
            raise IntegrationError("PR_HEAD_MISMATCH", "created PR head differs from reviewed head")
        return snapshot

    def _unresolved_threads(self, pr_number: int) -> int:
        if self._repo_slug is None:
            self.preflight()
        assert self._repo_slug is not None
        owner, name = self._repo_slug.split("/", 1)
        query = (
            "query($owner:String!,$name:String!,$number:Int!){"
            "repository(owner:$owner,name:$name){pullRequest(number:$number){"
            "reviewThreads(first:100){nodes{isResolved}pageInfo{hasNextPage}}}}}"
        )
        completed = self._gh(
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"name={name}",
            "-F",
            f"number={pr_number}",
        )
        try:
            payload = json.loads(completed.stdout)
            threads = payload["data"]["repository"]["pullRequest"]["reviewThreads"]
            if threads["pageInfo"]["hasNextPage"]:
                raise IntegrationError(
                    "GH_REVIEW_THREADS_UNBOUNDED",
                    "more than 100 review threads require explicit pagination support",
                )
            return sum(1 for item in threads["nodes"] if not item["isResolved"])
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            if isinstance(exc, IntegrationError):
                raise
            raise IntegrationError("GH_PROTOCOL_INVALID", "review thread query returned invalid JSON") from exc

    def read_postmerge(
        self,
        *,
        pr_number: int,
        project_id: str,
        run_id: str,
        package_id: str,
        coverage_status: str,
        planning_drift: str,
        visual_drift: str,
    ) -> PostmergeEvidence:
        self.preflight()
        snapshot = self._pr_snapshot(pr_number)
        if self._repo_slug is None:
            raise IntegrationError("GH_PROTOCOL_INVALID", "repository identity was not established")
        main_result = self._gh("api", f"repos/{self._repo_slug}/git/ref/heads/main")
        try:
            main_payload = json.loads(main_result.stdout)
            current_main_sha = _safe_sha(main_payload["object"]["sha"], "current_main_sha")
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            if isinstance(exc, IntegrationError):
                raise
            raise IntegrationError("GH_PROTOCOL_INVALID", "main ref query returned invalid JSON") from exc
        merge_in_main = False
        if snapshot.merge_sha is not None:
            compare = self._gh(
                "api",
                f"repos/{self._repo_slug}/compare/{snapshot.merge_sha}...{current_main_sha}",
            )
            try:
                compare_status = str(json.loads(compare.stdout)["status"])
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                raise IntegrationError("GH_PROTOCOL_INVALID", "compare query returned invalid JSON") from exc
            merge_in_main = compare_status in {"ahead", "identical"}
        return PostmergeEvidence(
            pr_number=pr_number,
            merged=snapshot.merged,
            pr_head_sha=snapshot.head_sha,
            merge_sha=snapshot.merge_sha,
            required_checks=snapshot.required_checks,
            unresolved_threads=self._unresolved_threads(pr_number),
            current_main_sha=current_main_sha,
            merge_in_main=merge_in_main,
            project_id=project_id,
            run_id=run_id,
            package_id=package_id,
            coverage_status=coverage_status,
            planning_drift=planning_drift,
            visual_drift=visual_drift,
        )


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
        reviewed_diff_sha256: str | None = None,
    ) -> HandoffResult:
        value = self._validate_handoff_receipt(
            receipt,
            expected_project_id=expected_project_id,
            expected_run_id=expected_run_id,
            expected_package_id=expected_package_id,
        )
        trusted = bool(getattr(self.provider, "requires_trusted_attestation", False))
        if trusted and (
            value.get("provider_mode") != "REAL"
            or value.get("integration_eligible") is not True
        ):
            raise IntegrationError(
                "INTEGRATION_NOT_ELIGIBLE",
                "operational PR handoff requires REAL provider evidence explicitly marked integration eligible",
            )
        if trusted and reviewed_diff_sha256 is None:
            raise IntegrationError(
                "DIFF_ATTESTATION_REQUIRED",
                "operational PR handoff requires a reviewed content digest",
            )
        self.provider.preflight()

        expected_main_sha = str(value["expected_main_sha"])
        current_head = _git(self.repo_root, "rev-parse", "HEAD").stdout.strip()
        if current_head != expected_main_sha:
            raise IntegrationError("STALE_BASE_SHA", "worktree HEAD differs from reviewed expected main SHA")

        current_diff_digest = compute_worktree_diff_sha256(self.repo_root)
        if reviewed_diff_sha256 is not None:
            expected_digest = _safe_digest(reviewed_diff_sha256, "reviewed_diff_sha256")
            if current_diff_digest != expected_digest:
                raise IntegrationError(
                    "DIFF_ATTESTATION_MISMATCH",
                    "worktree content changed after the reviewed Diff attestation",
                )
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
                f"Reviewed Diff `{current_diff_digest}`. "
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
            reviewed_diff_sha256=current_diff_digest,
            pr=pr,
        )

    def close_postmerge_from_provider(
        self,
        *,
        run_receipt: Mapping[str, Any],
        handoff: HandoffResult,
        receipt_path: Path | str,
        coverage_status: str,
        planning_drift: str,
        visual_drift: str,
    ) -> dict[str, Any]:
        reader = getattr(self.provider, "read_postmerge", None)
        if reader is None or not callable(reader):
            raise IntegrationError(
                "POSTMERGE_PROVIDER_UNAVAILABLE",
                "PR provider cannot fetch direct postmerge evidence",
            )
        evidence = reader(
            pr_number=handoff.pr.number,
            project_id=handoff.project_id,
            run_id=handoff.run_id,
            package_id=handoff.package_id,
            coverage_status=coverage_status,
            planning_drift=planning_drift,
            visual_drift=visual_drift,
        )
        if not isinstance(evidence, PostmergeEvidence):
            raise IntegrationError("POSTMERGE_PROVIDER_INVALID", "provider returned invalid postmerge evidence")
        return self.close_postmerge(
            run_receipt=run_receipt,
            handoff=handoff,
            evidence=evidence,
            receipt_path=receipt_path,
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
            "reviewed_diff_sha256": handoff.reviewed_diff_sha256,
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
