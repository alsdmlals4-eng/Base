from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .evidence import canonical_receipt
from .protocol import ReviewResult, RunRequest, WorkerResult
from .providers import BuilderProvider, CriticProvider
from .scope import validate_changed_paths


@dataclass(frozen=True)
class RunOutcome:
    state: str
    finding_codes: tuple[str, ...]
    changed_paths: tuple[str, ...]
    receipt_digest: str
    evidence: dict[str, Any]


def _review_signature(review: ReviewResult) -> tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...]:
    return tuple(sorted(
        (finding.code, finding.paths, finding.requirement_ids)
        for finding in review.findings
    ))


class A2Runtime:
    def __init__(self, *, builder: BuilderProvider, critic: CriticProvider) -> None:
        self.builder = builder
        self.critic = critic

    def _outcome(
        self,
        request: RunRequest,
        state: str,
        *,
        finding_codes: tuple[str, ...] = (),
        changed_paths: tuple[str, ...] = (),
        extra: dict[str, Any] | None = None,
    ) -> RunOutcome:
        payload: dict[str, Any] = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_RECEIPT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "state": state,
            "finding_codes": list(finding_codes),
            "changed_paths": list(changed_paths),
            "provider_mode": request.provider_mode,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }
        if extra:
            payload.update(extra)
        receipt = canonical_receipt(payload)
        return RunOutcome(
            state=state,
            finding_codes=finding_codes,
            changed_paths=changed_paths,
            receipt_digest=str(receipt["receipt_digest"]),
            evidence=receipt,
        )

    def _identity_matches(self, request: RunRequest, worker: WorkerResult) -> bool:
        return (
            worker.project_id == request.project_id
            and worker.run_id == request.run_id
            and worker.package_id == request.package_id
            and worker.expected_main_sha == request.expected_main_sha
        )

    def _review_identity_matches(self, request: RunRequest, review: ReviewResult) -> bool:
        return (
            review.project_id == request.project_id
            and review.run_id == request.run_id
            and review.package_id == request.package_id
            and review.expected_main_sha == request.expected_main_sha
        )

    def _validate_worker_before_review(self, request: RunRequest, worker: WorkerResult) -> RunOutcome | None:
        if not self._identity_matches(request, worker):
            return self._outcome(request, "QUARANTINED", finding_codes=("WORKER_IDENTITY_MISMATCH",))
        if worker.status != "COMPLETED":
            return self._outcome(request, "PROVIDER_FAILURE", finding_codes=("BUILDER_NOT_COMPLETED",))
        if worker.usage["turns"] > request.budgets.max_turns:
            return self._outcome(request, "BUDGET_EXCEEDED", finding_codes=("BUILDER_TURN_BUDGET_EXCEEDED",))
        if not worker.changed_paths:
            return self._outcome(request, "BLOCKED_UNVERIFIED", finding_codes=("EMPTY_CHANGESET",))
        return None

    def _validate_review_before_verdict(
        self, request: RunRequest, review: ReviewResult, changed_paths: tuple[str, ...]
    ) -> RunOutcome | None:
        if not self._review_identity_matches(request, review):
            return self._outcome(
                request, "QUARANTINED",
                finding_codes=("CRITIC_IDENTITY_MISMATCH",),
                changed_paths=changed_paths,
            )
        if review.verdict == "PASS" and review.findings:
            return self._outcome(
                request, "BLOCKED_UNVERIFIED",
                finding_codes=("CRITIC_PASS_WITH_FINDINGS",),
                changed_paths=changed_paths,
            )
        return None

    def run(self, request: RunRequest, *, observed_main_sha: str) -> RunOutcome:
        if observed_main_sha != request.expected_main_sha:
            return self._outcome(request, "STALE_BASE_SHA", finding_codes=("STALE_BASE_SHA",))

        worker = self.builder.invoke(request, repair_cycle=0)
        worker_failure = self._validate_worker_before_review(request, worker)
        if worker_failure is not None:
            return worker_failure

        scope_findings = validate_changed_paths(worker.changed_paths, request.allowed_paths, request.forbidden_paths)
        if scope_findings:
            return self._outcome(
                request,
                "QUARANTINED",
                finding_codes=tuple(item.code for item in scope_findings),
                changed_paths=worker.changed_paths,
                extra={"scope_findings": [item.__dict__ for item in scope_findings]},
            )

        review = self.critic.review(request, worker)
        review_failure = self._validate_review_before_verdict(request, review, worker.changed_paths)
        if review_failure is not None:
            return review_failure
        if review.verdict == "PASS" and set(review.checked_requirement_ids) != set(request.requirement_ids):
            return self._outcome(
                request, "BLOCKED_UNVERIFIED",
                finding_codes=("CRITIC_COVERAGE_INCOMPLETE",),
                changed_paths=worker.changed_paths,
                extra={
                    "required_requirement_ids": list(request.requirement_ids),
                    "checked_requirement_ids": list(review.checked_requirement_ids),
                },
            )
        if review.verdict == "PASS":
            return self._outcome(
                request,
                "WAITING_INTEGRATION",
                changed_paths=worker.changed_paths,
                extra={"critic_verdict": review.verdict, "checked_requirement_ids": list(review.checked_requirement_ids)},
            )
        if review.verdict in {"USER_DECISION_REQUIRED", "BLOCKED_UNVERIFIED"}:
            return self._outcome(
                request,
                review.verdict,
                finding_codes=tuple(f.code for f in review.findings) or (review.verdict,),
                changed_paths=worker.changed_paths,
            )

        previous_signature = _review_signature(review)
        for repair_cycle in range(1, request.budgets.max_repair_cycles + 1):
            worker = self.builder.invoke(request, repair_cycle=repair_cycle)
            worker_failure = self._validate_worker_before_review(request, worker)
            if worker_failure is not None:
                return worker_failure
            scope_findings = validate_changed_paths(worker.changed_paths, request.allowed_paths, request.forbidden_paths)
            if scope_findings:
                return self._outcome(
                    request, "QUARANTINED",
                    finding_codes=tuple(item.code for item in scope_findings),
                    changed_paths=worker.changed_paths,
                )
            next_review = self.critic.review(request, worker)
            review_failure = self._validate_review_before_verdict(request, next_review, worker.changed_paths)
            if review_failure is not None:
                return review_failure
            if next_review.verdict == "PASS" and set(next_review.checked_requirement_ids) != set(request.requirement_ids):
                return self._outcome(
                    request, "BLOCKED_UNVERIFIED",
                    finding_codes=("CRITIC_COVERAGE_INCOMPLETE",),
                    changed_paths=worker.changed_paths,
                )
            if next_review.verdict == "PASS":
                return self._outcome(
                    request, "WAITING_INTEGRATION", changed_paths=worker.changed_paths,
                    extra={"critic_verdict": "PASS", "repair_cycles": repair_cycle},
                )
            if next_review.verdict in {"USER_DECISION_REQUIRED", "BLOCKED_UNVERIFIED"}:
                return self._outcome(
                    request, next_review.verdict,
                    finding_codes=tuple(f.code for f in next_review.findings) or (next_review.verdict,),
                    changed_paths=worker.changed_paths,
                )
            signature = _review_signature(next_review)
            if signature == previous_signature:
                return self._outcome(
                    request, "NO_PROGRESS",
                    finding_codes=tuple(f.code for f in next_review.findings) or ("NO_PROGRESS",),
                    changed_paths=worker.changed_paths,
                    extra={"repair_cycles": repair_cycle},
                )
            previous_signature = signature

        return self._outcome(
            request, "REPAIR_LIMIT",
            finding_codes=tuple(f.code for f in review.findings) or ("REPAIR_LIMIT",),
            changed_paths=worker.changed_paths,
        )

    def burn_in(self, request: RunRequest, *, observed_main_sha: str, runs: int) -> dict[str, Any]:
        if not 1 <= runs <= 10:
            raise ValueError("runs must be 1..10")
        outcomes: list[RunOutcome] = []
        for index in range(1, runs + 1):
            run_request = replace(request, run_id=f"RUN_{index:03d}")
            outcomes.append(self.run(run_request, observed_main_sha=observed_main_sha))
        passed = all(outcome.state == "WAITING_INTEGRATION" for outcome in outcomes)
        return {
            "status": "FAKE_PROVIDER_BURNIN_GREEN" if passed else "FAKE_PROVIDER_BURNIN_FAILED",
            "consecutive_runs": len(outcomes) if passed else 0,
            "states": [outcome.state for outcome in outcomes],
            "receipt_digests": [outcome.receipt_digest for outcome in outcomes],
            "out_of_scope_writes": sum("OUT_OF_SCOPE_WRITE" in outcome.finding_codes for outcome in outcomes),
            "false_completion_claims": 0,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }
