from __future__ import annotations

import json
import os
import subprocess
from typing import Callable, Mapping, Sequence


_SAFE_ENV = (
    "PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "TMPDIR",
    "LANG", "LC_ALL", "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA",
)
_PUBLIC_FIELDS = (
    "status", "code", "issue_number", "target_repository", "base_runtime_sha",
    "authority_sha", "run_id", "a2_state", "a2_receipt_digest", "provider_mode",
    "a3_auto_merge", "scheduler",
)


class ControlPlaneError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


def _environment() -> dict[str, str]:
    result: dict[str, str] = {}
    for key in _SAFE_ENV:
        value = os.environ.get(key)
        if value:
            result[key] = value
    return result


def sanitize_public_receipt(value: Mapping[str, object]) -> dict[str, object]:
    result: dict[str, object] = {
        "schema_version": 1,
        "contract_role": "LOOP_A2_LOCAL_JOB_RECEIPT",
    }
    for key in _PUBLIC_FIELDS:
        item = value.get(key)
        if isinstance(item, (str, int, bool)) and not isinstance(item, bytes):
            result[key] = item
    return result


Runner = Callable[..., subprocess.CompletedProcess[str]]


class GhControlPlane:
    def __init__(
        self,
        *,
        control_repository: str,
        required_label: str,
        gh_executable: str = "gh",
        runner: Runner = subprocess.run,
        output_limit_bytes: int = 1_000_000,
        timeout_seconds: int = 30,
    ) -> None:
        if not control_repository or control_repository.count("/") != 1:
            raise ValueError("control_repository must be owner/name")
        if not required_label:
            raise ValueError("required_label must be non-empty")
        if not gh_executable:
            raise ValueError("gh_executable must be non-empty")
        if output_limit_bytes < 1024:
            raise ValueError("output_limit_bytes must be at least 1024")
        if not 1 <= timeout_seconds <= 120:
            raise ValueError("timeout_seconds must be 1..120")
        self.control_repository = control_repository
        self.required_label = required_label
        self.gh_executable = gh_executable
        self.runner = runner
        self.output_limit_bytes = output_limit_bytes
        self.timeout_seconds = timeout_seconds

    def _run(self, argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        try:
            return self.runner(
                list(argv),
                text=True,
                capture_output=True,
                shell=False,
                env=_environment(),
                timeout=self.timeout_seconds,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ControlPlaneError("GH_EXECUTION_FAILED", "GitHub CLI could not complete") from exc

    def _bounded_stdout(self, completed: subprocess.CompletedProcess[str], *, failure_code: str) -> str:
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        if (
            len(stdout.encode("utf-8", errors="replace")) > self.output_limit_bytes
            or len(stderr.encode("utf-8", errors="replace")) > self.output_limit_bytes
        ):
            raise ControlPlaneError("GH_OUTPUT_LIMIT", "GitHub CLI output exceeded the bounded limit")
        if completed.returncode != 0:
            raise ControlPlaneError(failure_code, "GitHub CLI operation failed")
        return stdout

    def preflight(self) -> None:
        completed = self._run((self.gh_executable, "auth", "status", "--hostname", "github.com"))
        self._bounded_stdout(completed, failure_code="GH_AUTH_REQUIRED")
        completed = self._run(
            (
                self.gh_executable,
                "label",
                "create",
                self.required_label,
                "--repo",
                self.control_repository,
                "--color",
                "5319E7",
                "--description",
                "Bounded unattended Loop A2 local execution job",
                "--force",
            )
        )
        self._bounded_stdout(completed, failure_code="GH_QUEUE_LABEL_SETUP_FAILED")

    def list_open_jobs(self) -> tuple[dict[str, object], ...]:
        completed = self._run(
            (
                self.gh_executable, "issue", "list", "--repo", self.control_repository,
                "--state", "open", "--label", self.required_label, "--limit", "100",
                "--json", "number,author,labels,body",
            )
        )
        stdout = self._bounded_stdout(completed, failure_code="GH_ISSUE_LIST_FAILED")
        try:
            value = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise ControlPlaneError("GH_ISSUE_LIST_INVALID", "GitHub issue list was not JSON") from exc
        if not isinstance(value, list) or len(value) > 100 or any(not isinstance(item, dict) for item in value):
            raise ControlPlaneError("GH_ISSUE_LIST_INVALID", "GitHub issue list shape was invalid")
        return tuple(dict(item) for item in value)

    def publish_terminal(self, issue_number: int, receipt: Mapping[str, object], *, close: bool) -> None:
        if isinstance(issue_number, bool) or not isinstance(issue_number, int) or issue_number <= 0:
            raise ValueError("issue_number must be positive")
        body = "```json\n" + json.dumps(sanitize_public_receipt(receipt), ensure_ascii=False, sort_keys=True) + "\n```"
        completed = self._run(
            (
                self.gh_executable, "issue", "comment", str(issue_number), "--repo",
                self.control_repository, "--body", body,
            )
        )
        self._bounded_stdout(completed, failure_code="GH_RECEIPT_PUBLISH_FAILED")
        if not close:
            return
        completed = self._run(
            (
                self.gh_executable, "issue", "close", str(issue_number), "--repo",
                self.control_repository, "--reason", "completed",
            )
        )
        self._bounded_stdout(completed, failure_code="GH_JOB_CLOSE_FAILED")
