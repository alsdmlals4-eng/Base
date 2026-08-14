from __future__ import annotations

from .job import JobContractError, LocalA2Job
from .repositories import ManagedRepositoryError
from .runtime import LocalRuntimeError


class LocalExecutorService:
    def __init__(
        self,
        *,
        control_plane: object,
        runtime: object,
        trusted_author: str,
        required_label: str,
    ) -> None:
        self.control_plane = control_plane
        self.runtime = runtime
        self.trusted_author = trusted_author
        self.required_label = required_label

    def preflight(self) -> dict[str, str]:
        self.control_plane.preflight()
        self.runtime.preflight()
        return {"status": "READY", "code": "LOCAL_EXECUTOR_READY"}

    def _public_base(self, job: LocalA2Job) -> dict[str, object]:
        return {
            "issue_number": job.issue_number,
            "target_repository": job.target_repository,
            "base_runtime_sha": job.base_runtime_sha,
            "authority_sha": job.authority_sha,
            "run_id": job.run_id,
            "provider_mode": "REAL",
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }

    def once(self) -> dict[str, object]:
        issues = self.control_plane.list_open_jobs()
        job: LocalA2Job | None = None
        for issue in issues:
            try:
                job = LocalA2Job.from_issue(
                    issue,
                    trusted_author=self.trusted_author,
                    required_label=self.required_label,
                )
                break
            except JobContractError:
                continue
        if job is None:
            return {"status": "IDLE", "code": "NO_ELIGIBLE_JOB"}

        public = self._public_base(job)
        try:
            receipt = self.runtime.execute(job)
        except (LocalRuntimeError, ManagedRepositoryError) as exc:
            public.update({"status": "BLOCKED", "code": exc.code})
            self.control_plane.publish_terminal(job.issue_number, public, close=True)
            return {"status": "BLOCKED", "code": exc.code, "issue_number": job.issue_number}

        public.update(
            {
                "status": "PASS",
                "code": "A2_WAITING_INTEGRATION",
                "a2_state": receipt["state"],
                "a2_receipt_digest": receipt["receipt_digest"],
            }
        )
        self.control_plane.publish_terminal(job.issue_number, public, close=True)
        return {"status": "PASS", "code": "A2_WAITING_INTEGRATION", "issue_number": job.issue_number}
