from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class RunState(str, Enum):
    CREATED = "CREATED"
    PREFLIGHT = "PREFLIGHT"
    AUTHORITY_SYNCED = "AUTHORITY_SYNCED"
    CONTRACT_VALIDATED = "CONTRACT_VALIDATED"
    COVERAGE_INITIALIZED = "COVERAGE_INITIALIZED"
    LEASE_ACQUIRED = "LEASE_ACQUIRED"
    SHADOW_RUNNING = "SHADOW_RUNNING"
    SHADOW_VERIFIED = "SHADOW_VERIFIED"
    ADVERSARIAL_REVIEWED = "ADVERSARIAL_REVIEWED"
    SHADOW_COMPLETE = "SHADOW_COMPLETE"

    BLOCKED_INVALID_CONTRACT = "BLOCKED_INVALID_CONTRACT"
    BLOCKED_STALE_SHA = "BLOCKED_STALE_SHA"
    BLOCKED_PROJECT_ISOLATION = "BLOCKED_PROJECT_ISOLATION"
    BLOCKED_COVERAGE = "BLOCKED_COVERAGE"
    BLOCKED_VISUAL = "BLOCKED_VISUAL"
    BLOCKED_DRIFT = "BLOCKED_DRIFT"
    BLOCKED_LEASE_CONFLICT = "BLOCKED_LEASE_CONFLICT"
    BLOCKED_DUPLICATE_INPUT = "BLOCKED_DUPLICATE_INPUT"
    BLOCKED_NO_PROGRESS = "BLOCKED_NO_PROGRESS"
    BLOCKED_BUDGET = "BLOCKED_BUDGET"
    BLOCKED_RECEIPT_EXISTS = "BLOCKED_RECEIPT_EXISTS"


class FindingCode(str, Enum):
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_CONTRACT = "INVALID_CONTRACT"
    UNSAFE_AUTONOMY = "UNSAFE_AUTONOMY"
    DUPLICATE_NORMALIZED_PATH = "DUPLICATE_NORMALIZED_PATH"
    STALE_MAIN_SHA = "STALE_MAIN_SHA"
    CROSS_PROJECT_REFERENCE = "CROSS_PROJECT_REFERENCE"
    UNSAFE_PROJECT_PATH = "UNSAFE_PROJECT_PATH"
    UNSAFE_SYMLINK = "UNSAFE_SYMLINK"
    UNSAFE_STATE_ROOT = "UNSAFE_STATE_ROOT"
    REFERENCE_MISSING = "REFERENCE_MISSING"
    UNAPPROVED_REQUIREMENT = "UNAPPROVED_REQUIREMENT"
    UNMAPPED_REQUIREMENT = "UNMAPPED_REQUIREMENT"
    UNAPPROVED_COVERAGE_ENTRY = "UNAPPROVED_COVERAGE_ENTRY"
    INCOMPLETE_COVERAGE = "INCOMPLETE_COVERAGE"
    UNAPPROVED_EXTRA_OUTPUT = "UNAPPROVED_EXTRA_OUTPUT"
    MISSING_REQUIRED_EVIDENCE = "MISSING_REQUIRED_EVIDENCE"
    USER_DECISION_REQUIRED = "USER_DECISION_REQUIRED"
    PLANNING_CONFLICT = "PLANNING_CONFLICT"
    VISUAL_LOCK_MISMATCH = "VISUAL_LOCK_MISMATCH"
    LEASE_CONFLICT = "LEASE_CONFLICT"
    LEASE_LEDGER_CORRUPT = "LEASE_LEDGER_CORRUPT"
    DUPLICATE_INPUT = "DUPLICATE_INPUT"
    NO_PROGRESS = "NO_PROGRESS"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    RECEIPT_EXISTS = "RECEIPT_EXISTS"
    RECEIPT_CORRUPT = "RECEIPT_CORRUPT"


@dataclass(frozen=True, slots=True)
class Finding:
    code: FindingCode
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code.value,
            "message": self.message,
        }
        if self.path is not None:
            payload["path"] = self.path
        return payload


@dataclass(frozen=True, slots=True)
class CoverageEntry:
    requirement_id: str
    tasks: tuple[str, ...]
    outputs: tuple[str, ...]
    tests: tuple[str, ...]
    evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Reference:
    project_id: str
    kind: str
    path: str


@dataclass(frozen=True, slots=True)
class Budgets:
    max_transitions: int
    max_repeated_failures: int


@dataclass(frozen=True, slots=True)
class ShadowRequest:
    schema_version: int
    contract_role: str
    project_id: str
    run_id: str
    package_id: str
    source_main_sha: str
    observed_main_sha: str
    planning_status: str
    visual_impact: str
    visual_status: str
    planning_drift: str
    visual_drift: str
    approved_requirements: tuple[str, ...]
    package_requirement_ids: tuple[str, ...]
    coverage: tuple[CoverageEntry, ...]
    allowed_paths: tuple[str, ...]
    changed_paths: tuple[str, ...]
    required_evidence: tuple[str, ...]
    resource_locks: tuple[str, ...]
    references: tuple[Reference, ...]
    budgets: Budgets
    autonomy: str
    a3_auto_merge_allowlist: tuple[str, ...]
    scheduler_runtime_provider: str
    raw: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ShadowOutcome:
    state: RunState
    findings: tuple[Finding, ...]
    transitions: tuple[str, ...] = ()
    semantic_input_digest: str | None = None
    receipt_digest: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "state": self.state.value,
            "findings": [finding.to_dict() for finding in self.findings],
            "transitions": list(self.transitions),
        }
        if self.semantic_input_digest is not None:
            payload["semantic_input_digest"] = self.semantic_input_digest
        if self.receipt_digest is not None:
            payload["receipt_digest"] = self.receipt_digest
        return payload
