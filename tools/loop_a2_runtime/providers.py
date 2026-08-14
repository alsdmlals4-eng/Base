from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .protocol import ReviewResult, RunRequest, WorkerResult


class BuilderProvider(Protocol):
    def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult: ...


class CriticProvider(Protocol):
    def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult: ...


@dataclass
class FakeBuilder:
    changed_paths: tuple[str, ...]
    status: str = "COMPLETED"
    calls: int = 0

    def invoke(self, request: RunRequest, *, repair_cycle: int) -> WorkerResult:
        self.calls += 1
        return WorkerResult.from_dict({
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "role": "BUILDER",
            "status": self.status,
            "changed_paths": list(self.changed_paths),
            "summary": "Fake Builder completed; deterministic verification remains authoritative.",
            "usage": {"turns": 1},
            "errors": [] if self.status == "COMPLETED" else [{"code": "PROVIDER_FAILURE", "message": "fake failure"}],
        })


@dataclass
class FakeCritic:
    verdict: str = "PASS"
    finding_codes: tuple[str, ...] = ()
    checked_requirement_ids: tuple[str, ...] = ()
    repeat: bool = False
    calls: int = 0

    def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult:
        self.calls += 1
        findings = [
            {
                "code": code,
                "severity": "P1",
                "message": "Fake Critic finding.",
                "paths": list(worker_result.changed_paths),
                "requirement_ids": list(self.checked_requirement_ids),
            }
            for code in self.finding_codes
        ]
        return ReviewResult.from_dict({
            "schema_version": 1,
            "contract_role": "LOOP_A2_REVIEW_RESULT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "role": "CRITIC",
            "verdict": self.verdict,
            "findings": findings,
            "checked_requirement_ids": list(self.checked_requirement_ids),
        })
