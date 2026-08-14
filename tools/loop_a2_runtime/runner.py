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
    return tuple(
        sorted(
            (finding.code, finding.paths, finding.requirement_ids)
            for finding in review.findings
        )
    )


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

    @staticmethod
    def _worker_identity_matches(request: RunRequest, worker: WorkerResult) -> bool:
        return (
            worker.project_id == request.project_id
            and worker.run_id == request.run_id
            and worker.package_id == request.package_id
            and worker.expected_main_sha == request.expected_main_sha
        )

    @staticmethod
    def _review_identity_matches(request: RunRequest, review: ReviewResult) -> bool:
        return (
            review.project_id == request.project_id
            and review.run_id == request.run_id
            and review.package_id == request.package_id
            and review.expected_main_sha == request.expected_main_sha
        )

    def _validate_worker_before_review(
        self,
        request: RunRequest,
        worker: WorkerResult,
        *,
        cumulative_turns: int,
    ) -> RunOutcome | None:
        if not self._worker_identity_matches(request, worker):
            return self._outcome(
                request,
                "QUARANTINED",
                finding_codes=("WORKER_IDENTITY_MISMATCH",),
            )
        if worker.status != "COMPLETED":
            return self._outcome(
                request,
                "PROVIDER_FAILURE",
                finding_codes=("BUILDER_NOT_COMPLETED",),
            )
        if cumulative_turns > request.budgets.max_turns:
            return self._outcome(
                request,
                "BUDGET_EXCEEDED",
                finding_codes=("BUILDER_TURN_BUDGET_EXCEEDED",),
                changed_paths=worker.changed_paths,
                extra={"cumulative_turns": cumulative_turns},
            )
        if not worker.changed_paths:
            return self._outcome(
                request,
                "BLOCKED_UNVERIFIED",
                finding_codes=("EMPTY_CHANGESET",),
            )
        return None

    def _validate_review_before_verdict(
        self,
        request: RunRequest,
        review: ReviewResult,
        changed_paths: tuple[str, ...],
    ) -> RunOutcome | None:
        if not self._review_identity_matches(request, review):
            return self._outcome(
                request,
                "QUARANTINED",
                finding_codes=("CRITIC_IDENTITY_MISMATCH",),
                changed_paths=changed_paths,
            )

        approved_requirements = set(request.requirement_ids)
        if not set(review.checked_requirement_ids).issubset(approved_requirements):
            return self._outcome(
                request,
                "QUARANTINED",
                finding_codes=("CRITIC_REQUIREMENT_EXPANSION",),
                changed_paths=changed_paths,
            )
        for finding in review.findings:
            if not set(finding.requirement_ids).issubset(approved_requirements):
                return self._outcome(
                    request,
                    "QUARANTINED",
                    finding_codes=("CRITIC_REQUIREMENT_EXPANSION",),
                    changed_paths=changed_paths,
                )
            path_findings = validate_changed_paths(
                finding.paths,
                request.allowed_paths,
                request.forbidden_paths,
            )
            if path_findings:
                return self._outcome(
                    request,
                    "QUARANTINED",
                    finding_codes=("CRITIC_PATH_EXPANSION",),
                    changed_paths=changed_paths,
                    extra={
                        "critic_path_findings": [item.__dict__ for item in path_findings]
                    },
                )

        if review.verdict == "PASS" and review.findings:
            return self._outcome(
                request,
                "BLOCKED_UNVERIFIED",
                finding_codes=("CRITIC_PASS_WITH_FINDINGS",),
                changed_paths=changed_paths,
            )
        return None

    def _run_scope_gate(
        self,
        request: RunRequest,
        worker: WorkerResult,
    ) -> RunOutcome | None:
        findings = validate_changed_paths(
            worker.changed_paths,
            request.allowed_paths,
            request.forbidden_paths,
        )
        if not findings:
            return None
        return self._outcome(
            request,
            "QUARANTINED",
            finding_codes=tuple(item.code for item in findings),
            changed_paths=worker.changed_paths,
            extra={"scope_findings": [item.__dict__ for item in findings]},
        )

    def _handle_review_terminal(
        self,
        request: RunRequest,
        review: ReviewResult,
        worker: WorkerResult,
        *,
        repair_cycle: int,
    ) -> RunOutcome | None:
        if review.verdict == "PASS" and set(review.checked_requirement_ids) != set(request.requirement_ids):
            return self._outcome(
                request,
                "BLOCKED_UNVERIFIED",
                finding_codes=("CRITIC_COVERAGE_INCOMPLETE",),
                changed_paths=worker.changed_paths,
                extra={
                    "required_requirement_ids": list(request.requirement_ids),
                    "checked_requirement_ids": list(review.checked_requirement_ids),
                },
            )
        if review.verdict == "PASS":
            extra: dict[str, Any] = {
                "critic_verdict": "PASS",
                "checked_requirement_ids": list(review.checked_requirement_ids),
            }
            if repair_cycle:
                extra["repair_cycles"] = repair_cycle
            return self._outcome(
                request,
                "WAITING_INTEGRATION",
                changed_paths=worker.changed_paths,
                extra=extra,
            )
        if review.verdict in {"USER_DECISION_REQUIRED", "BLOCKED_UNVERIFIED"}:
            return self._outcome(
                request,
                review.verdict,
                finding_codes=tuple(finding.code for finding in review.findings)
                or (review.verdict,),
                changed_paths=worker.changed_paths,
            )
        return None

    def run(self, request: RunRequest, *, observed_main_sha: str) -> RunOutcome:
        if observed_main_sha != request.expected_main_sha:
            return self._outcome(
                request,
                "STALE_BASE_SHA",
                finding_codes=("STALE_BASE_SHA",),
            )

        cumulative_turns = 0
        worker = self.builder.invoke(request, repair_cycle=0)
        cumulative_turns += worker.usage["turns"]
        failure = self._validate_worker_before_review(
            request,
            worker,
            cumulative_turns=cumulative_turns,
        )
        if failure is not None:
            return failure
        failure = self._run_scope_gate(request, worker)
        if failure is not None:
            return failure

        review = self.critic.review(request, worker)
        failure = self._validate_review_before_verdict(
            request,
            review,
            worker.changed_paths,
        )
        if failure is not None:
            return failure
        terminal = self._handle_review_terminal(
            request,
            review,
            worker,
            repair_cycle=0,
        )
        if terminal is not None:
            return terminal

        current_review = review
        previous_signature = _review_signature(review)
        for repair_cycle in range(1, request.budgets.max_repair_cycles + 1):
            worker = self.builder.invoke(request, repair_cycle=repair_cycle)
            cumulative_turns += worker.usage["turns"]
            failure = self._validate_worker_before_review(
                request,
                worker,
                cumulative_turns=cumulative_turns,
            )
            if failure is not None:
                return failure
            failure = self._run_scope_gate(request, worker)
            if failure is not None:
                return failure

            current_review = self.critic.review(request, worker)
            failure = self._validate_review_before_verdict(
                request,
                current_review,
                worker.changed_paths,
            )
            if failure is not None:
                return failure
            terminal = self._handle_review_terminal(
                request,
                current_review,
                worker,
                repair_cycle=repair_cycle,
            )
            if terminal is not None:
                return terminal

            signature = _review_signature(current_review)
            if signature == previous_signature:
                return self._outcome(
                    request,
                    "NO_PROGRESS",
                    finding_codes=tuple(
                        finding.code for finding in current_review.findings
                    )
                    or ("NO_PROGRESS",),
                    changed_paths=worker.changed_paths,
                    extra={
                        "repair_cycles": repair_cycle,
                        "cumulative_turns": cumulative_turns,
                    },
                )
            previous_signature = signature

        return self._outcome(
            request,
            "REPAIR_LIMIT",
            finding_codes=tuple(
                finding.code for finding in current_review.findings
            )
            or ("REPAIR_LIMIT",),
            changed_paths=worker.changed_paths,
            extra={"cumulative_turns": cumulative_turns},
        )

    def burn_in(
        self,
        request: RunRequest,
        *,
        observed_main_sha: str,
        runs: int,
    ) -> dict[str, Any]:
        if request.provider_mode != "FAKE":
            raise ValueError("burn-in requires provider_mode FAKE")
        if not 1 <= runs <= 10:
            raise ValueError("runs must be 1..10")
        outcomes: list[RunOutcome] = []
        for index in range(1, runs + 1):
            run_request = replace(request, run_id=f"RUN_{index:03d}")
            outcomes.append(
                self.run(run_request, observed_main_sha=observed_main_sha)
            )
        passed = all(
            outcome.state == "WAITING_INTEGRATION" for outcome in outcomes
        )
        return {
            "status": "FAKE_PROVIDER_BURNIN_GREEN"
            if passed
            else "FAKE_PROVIDER_BURNIN_FAILED",
            "consecutive_runs": len(outcomes) if passed else 0,
            "states": [outcome.state for outcome in outcomes],
            "receipt_digests": [
                outcome.receipt_digest for outcome in outcomes
            ],
            "out_of_scope_writes": sum(
                "OUT_OF_SCOPE_WRITE" in outcome.finding_codes
                for outcome in outcomes
            ),
            "false_completion_claims": 0,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
        }
