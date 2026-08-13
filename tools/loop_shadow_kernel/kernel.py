from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .canonical import digest_json, semantic_payload
from .contract import parse_shadow_request
from .models import Finding, FindingCode, RunState, ShadowOutcome, ShadowRequest
from .paths import UnsafePath, UnsafeSymlink, resolve_project_path, validate_state_root
from .state_machine import HAPPY_PATH, REQUIRED_TRANSITIONS, StateMachine, TransitionBudgetExceeded
from .storage import (
    LeaseLedgerBusyError,
    ReceiptCorruptError,
    ReceiptExistsError,
    StateStorage,
    UnsafeStateTreeError,
)


class ShadowKernel:
    def __init__(self, project_root: Path | str, state_root: Path | str, *, now: str | None = None) -> None:
        self.project_root = Path(project_root)
        self.state_root = Path(state_root)
        self.now = now or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _validated_state_root(self) -> tuple[Path | None, tuple[Finding, ...]]:
        try:
            return validate_state_root(self.project_root, self.state_root), ()
        except (OSError, UnsafePath, UnsafeSymlink) as error:
            return None, (
                Finding(
                    FindingCode.UNSAFE_STATE_ROOT,
                    str(error),
                    str(self.state_root),
                ),
            )

    def validate(self, request_value: object) -> ShadowOutcome:
        state_root, state_findings = self._validated_state_root()
        if state_root is None:
            return ShadowOutcome(RunState.BLOCKED_PROJECT_ISOLATION, state_findings)

        request, contract_findings = parse_shadow_request(request_value)
        if request is None:
            return ShadowOutcome(RunState.BLOCKED_INVALID_CONTRACT, contract_findings)

        state, findings = self._evaluate_static(request)
        if state is not None:
            return ShadowOutcome(state, findings, (RunState.CREATED.value,))
        return ShadowOutcome(
            RunState.CONTRACT_VALIDATED,
            (),
            (
                RunState.CREATED.value,
                RunState.PREFLIGHT.value,
                RunState.AUTHORITY_SYNCED.value,
                RunState.CONTRACT_VALIDATED.value,
            ),
            semantic_input_digest=digest_json(semantic_payload(request.raw)),
        )

    def shadow(self, request_value: object) -> ShadowOutcome:
        validated_state_root, state_findings = self._validated_state_root()
        if validated_state_root is None:
            return ShadowOutcome(RunState.BLOCKED_PROJECT_ISOLATION, state_findings)

        request, contract_findings = parse_shadow_request(request_value)
        if request is None:
            return ShadowOutcome(RunState.BLOCKED_INVALID_CONTRACT, contract_findings)

        storage = StateStorage(validated_state_root)
        try:
            if storage.receipt_exists(request.project_id, request.run_id):
                return ShadowOutcome(
                    RunState.BLOCKED_RECEIPT_EXISTS,
                    (
                        Finding(
                            FindingCode.RECEIPT_EXISTS,
                            "immutable receipt already exists for this run_id",
                            request.run_id,
                        ),
                    ),
                    (RunState.CREATED.value,),
                )
        except UnsafeStateTreeError as error:
            return ShadowOutcome(
                RunState.BLOCKED_PROJECT_ISOLATION,
                (Finding(FindingCode.UNSAFE_STATE_ROOT, str(error), str(validated_state_root)),),
            )

        semantic_digest = digest_json(semantic_payload(request.raw))
        try:
            prior_receipts = tuple(storage.iter_receipts(request.project_id))
        except ReceiptCorruptError as error:
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_INVALID_CONTRACT,
                (Finding(FindingCode.RECEIPT_CORRUPT, str(error)),),
            )
        except UnsafeStateTreeError as error:
            return ShadowOutcome(
                RunState.BLOCKED_PROJECT_ISOLATION,
                (Finding(FindingCode.UNSAFE_STATE_ROOT, str(error), str(validated_state_root)),),
            )
        if any(
            receipt.get("semantic_input_digest") == semantic_digest
            and receipt.get("state") == RunState.SHADOW_COMPLETE.value
            for receipt in prior_receipts
        ):
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_DUPLICATE_INPUT,
                (
                    Finding(
                        FindingCode.DUPLICATE_INPUT,
                        "a successful receipt already covers this semantic input",
                    ),
                ),
            )

        repeated_failures = sum(
            1
            for receipt in prior_receipts
            if receipt.get("semantic_input_digest") == semantic_digest
            and isinstance(receipt.get("state"), str)
            and str(receipt["state"]).startswith("BLOCKED_")
            and receipt.get("state") != RunState.BLOCKED_NO_PROGRESS.value
        )
        if repeated_failures >= request.budgets.max_repeated_failures:
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_NO_PROGRESS,
                (
                    Finding(
                        FindingCode.NO_PROGRESS,
                        f"same semantic input failed {repeated_failures} times without new evidence",
                    ),
                ),
            )

        state, findings = self._evaluate_static(request)
        if state is not None:
            return self._persist_block(storage, request, semantic_digest, state, findings)

        try:
            conflicts = storage.acquire_leases(
                request.project_id,
                request.run_id,
                request.resource_locks,
            )
        except LeaseLedgerBusyError as error:
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_LEASE_CONFLICT,
                (Finding(FindingCode.LEASE_CONFLICT, str(error)),),
            )
        except UnsafeStateTreeError as error:
            return ShadowOutcome(
                RunState.BLOCKED_PROJECT_ISOLATION,
                (Finding(FindingCode.UNSAFE_STATE_ROOT, str(error), str(validated_state_root)),),
            )
        if conflicts:
            findings = tuple(
                Finding(
                    FindingCode.LEASE_CONFLICT,
                    f"resource {item['resource']} is owned by {item['run_id']}",
                    item["resource"],
                )
                for item in conflicts
            )
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_LEASE_CONFLICT,
                findings,
            )

        machine = StateMachine(max_transitions=request.budgets.max_transitions)
        try:
            for target in HAPPY_PATH:
                machine.advance(target)
        except TransitionBudgetExceeded as error:
            storage.release_leases(request.project_id, request.run_id)
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_BUDGET,
                (Finding(FindingCode.BUDGET_EXCEEDED, str(error)),),
                transitions=machine.history,
            )

        product_snapshot = self._product_snapshot(request)
        try:
            storage.release_leases(request.project_id, request.run_id)
        except LeaseLedgerBusyError as error:
            return self._persist_block(
                storage,
                request,
                semantic_digest,
                RunState.BLOCKED_LEASE_CONFLICT,
                (Finding(FindingCode.LEASE_CONFLICT, f"lease release failed: {error}"),),
                transitions=machine.history,
            )
        receipt = self._receipt_payload(
            request,
            semantic_digest,
            RunState.SHADOW_COMPLETE,
            (),
            machine.history,
            product_snapshot=product_snapshot,
        )
        try:
            signed = storage.write_receipt(receipt)
        except ReceiptExistsError:
            return ShadowOutcome(
                RunState.BLOCKED_RECEIPT_EXISTS,
                (Finding(FindingCode.RECEIPT_EXISTS, "receipt appeared concurrently", request.run_id),),
                machine.history,
                semantic_input_digest=semantic_digest,
            )

        return ShadowOutcome(
            RunState.SHADOW_COMPLETE,
            (),
            machine.history,
            semantic_input_digest=semantic_digest,
            receipt_digest=str(signed["receipt_digest"]),
        )

    def status(self, project_id: str, run_id: str) -> dict[str, Any]:
        validated_state_root, findings = self._validated_state_root()
        if validated_state_root is None:
            raise ValueError(findings[0].message)
        return StateStorage(validated_state_root).read_receipt(project_id, run_id)

    def leases(self, project_id: str) -> list[dict[str, str]]:
        validated_state_root, findings = self._validated_state_root()
        if validated_state_root is None:
            raise ValueError(findings[0].message)
        return StateStorage(validated_state_root).read_leases(project_id)

    def acquire_test_lease(self, project_id: str, run_id: str, resource: str) -> None:
        validated_state_root, findings = self._validated_state_root()
        if validated_state_root is None:
            raise ValueError(findings[0].message)
        conflicts = StateStorage(validated_state_root).acquire_leases(
            project_id,
            run_id,
            (resource,),
        )
        if conflicts:
            raise ValueError(f"test lease conflicts with {conflicts[0]['run_id']}")

    def _evaluate_static(self, request: ShadowRequest) -> tuple[RunState | None, tuple[Finding, ...]]:
        if request.budgets.max_transitions < REQUIRED_TRANSITIONS:
            return (
                RunState.BLOCKED_BUDGET,
                (
                    Finding(
                        FindingCode.BUDGET_EXCEEDED,
                        f"max_transitions={request.budgets.max_transitions} is below required {REQUIRED_TRANSITIONS}",
                    ),
                ),
            )

        if request.source_main_sha != request.observed_main_sha:
            return (
                RunState.BLOCKED_STALE_SHA,
                (
                    Finding(
                        FindingCode.STALE_MAIN_SHA,
                        "observed main SHA differs from the approved package source SHA",
                    ),
                ),
            )

        isolation_findings = self._isolation_findings(request)
        if isolation_findings:
            return RunState.BLOCKED_PROJECT_ISOLATION, isolation_findings

        coverage_findings = self._coverage_findings(request)
        if coverage_findings:
            return RunState.BLOCKED_COVERAGE, coverage_findings

        if request.planning_drift in {"PLANNING_CONFLICT", "UNVERIFIED"}:
            return (
                RunState.BLOCKED_DRIFT,
                (
                    Finding(
                        FindingCode.PLANNING_CONFLICT,
                        f"planning drift status is {request.planning_drift}",
                    ),
                ),
            )

        visual_findings = self._visual_findings(request)
        if visual_findings:
            return RunState.BLOCKED_VISUAL, visual_findings

        return None, ()

    def _isolation_findings(self, request: ShadowRequest) -> tuple[Finding, ...]:
        findings: list[Finding] = []
        for reference in request.references:
            if reference.project_id != request.project_id:
                findings.append(
                    Finding(
                        FindingCode.CROSS_PROJECT_REFERENCE,
                        f"reference belongs to {reference.project_id}, not {request.project_id}",
                        reference.path,
                    )
                )
            try:
                resolve_project_path(self.project_root, reference.path)
            except UnsafeSymlink as error:
                findings.append(Finding(FindingCode.UNSAFE_SYMLINK, str(error), reference.path))
            except (OSError, UnsafePath) as error:
                findings.append(Finding(FindingCode.UNSAFE_PROJECT_PATH, str(error), reference.path))

        checked_paths = set(request.allowed_paths) | set(request.changed_paths)
        checked_paths.update(output for entry in request.coverage for output in entry.outputs)
        for path in sorted(checked_paths):
            try:
                resolve_project_path(self.project_root, path)
            except UnsafeSymlink as error:
                findings.append(Finding(FindingCode.UNSAFE_SYMLINK, str(error), path))
            except (OSError, UnsafePath) as error:
                findings.append(Finding(FindingCode.UNSAFE_PROJECT_PATH, str(error), path))
        return tuple(findings)

    @staticmethod
    def _coverage_findings(request: ShadowRequest) -> tuple[Finding, ...]:
        findings: list[Finding] = []
        approved = set(request.approved_requirements)
        package = set(request.package_requirement_ids)
        entries_by_id = {entry.requirement_id: entry for entry in request.coverage}
        coverage_ids = set(entries_by_id)

        for requirement_id in sorted(package - approved):
            findings.append(
                Finding(
                    FindingCode.UNAPPROVED_REQUIREMENT,
                    f"package requirement is not approved: {requirement_id}",
                )
            )
        for requirement_id in sorted(package - coverage_ids):
            findings.append(
                Finding(
                    FindingCode.UNMAPPED_REQUIREMENT,
                    f"package requirement has no coverage entry: {requirement_id}",
                )
            )
        for requirement_id in sorted(coverage_ids - package):
            findings.append(
                Finding(
                    FindingCode.UNAPPROVED_COVERAGE_ENTRY,
                    f"coverage entry is outside the package: {requirement_id}",
                )
            )

        allowed = set(request.allowed_paths)
        mapped_outputs: set[str] = set()
        all_evidence: set[str] = set()
        for entry in request.coverage:
            if not entry.tasks or not entry.outputs or not entry.tests or not entry.evidence:
                findings.append(
                    Finding(
                        FindingCode.INCOMPLETE_COVERAGE,
                        f"coverage is incomplete for {entry.requirement_id}",
                    )
                )
            all_evidence.update(entry.evidence)
            for output in entry.outputs:
                mapped_outputs.add(output)
                if output not in allowed:
                    findings.append(
                        Finding(
                            FindingCode.UNAPPROVED_EXTRA_OUTPUT,
                            f"coverage output is not allowed: {output}",
                            output,
                        )
                    )

        for changed_path in request.changed_paths:
            if changed_path not in allowed or changed_path not in mapped_outputs:
                findings.append(
                    Finding(
                        FindingCode.UNAPPROVED_EXTRA_OUTPUT,
                        f"changed path is not both allowed and requirement-mapped: {changed_path}",
                        changed_path,
                    )
                )

        for evidence in sorted(set(request.required_evidence) - all_evidence):
            findings.append(
                Finding(
                    FindingCode.MISSING_REQUIRED_EVIDENCE,
                    f"required evidence is not mapped: {evidence}",
                )
            )
        return tuple(findings)

    @staticmethod
    def _visual_findings(request: ShadowRequest) -> tuple[Finding, ...]:
        if request.visual_impact == "NEW_VISUAL_REQUIRED":
            return (
                Finding(
                    FindingCode.USER_DECISION_REQUIRED,
                    "new visual design requires a human-approved Visual Lock",
                ),
            )
        if request.visual_impact == "NONE":
            if request.visual_status != "VISUAL_NOT_APPLICABLE" or request.visual_drift != "NOT_APPLICABLE":
                return (
                    Finding(
                        FindingCode.VISUAL_LOCK_MISMATCH,
                        "visual impact NONE requires VISUAL_NOT_APPLICABLE / NOT_APPLICABLE",
                    ),
                )
            return ()
        if request.visual_impact == "EXISTING_LOCKED":
            if request.visual_status != "VISUAL_LOCKED" or request.visual_drift not in {
                "NO_DRIFT",
                "MINOR_TECHNICAL_DRIFT",
            }:
                return (
                    Finding(
                        FindingCode.VISUAL_LOCK_MISMATCH,
                        "existing visual work must remain inside a verified Visual Lock",
                    ),
                )
        return ()

    def _product_snapshot(self, request: ShadowRequest) -> dict[str, str]:
        snapshot: dict[str, str] = {}
        for path in sorted(request.changed_paths):
            confined = resolve_project_path(self.project_root, path)
            if confined.physical.is_file():
                snapshot[path] = hashlib.sha256(confined.physical.read_bytes()).hexdigest()
            else:
                snapshot[path] = "MISSING"
        return snapshot

    def _persist_block(
        self,
        storage: StateStorage,
        request: ShadowRequest,
        semantic_digest: str,
        state: RunState,
        findings: tuple[Finding, ...],
        *,
        transitions: tuple[str, ...] = (RunState.CREATED.value,),
    ) -> ShadowOutcome:
        receipt = self._receipt_payload(
            request,
            semantic_digest,
            state,
            findings,
            transitions,
            product_snapshot={},
        )
        try:
            signed = storage.write_receipt(receipt)
        except ReceiptExistsError:
            return ShadowOutcome(
                RunState.BLOCKED_RECEIPT_EXISTS,
                (Finding(FindingCode.RECEIPT_EXISTS, "receipt appeared concurrently", request.run_id),),
                transitions,
                semantic_input_digest=semantic_digest,
            )
        return ShadowOutcome(
            state,
            findings,
            transitions,
            semantic_input_digest=semantic_digest,
            receipt_digest=str(signed["receipt_digest"]),
        )

    def _receipt_payload(
        self,
        request: ShadowRequest,
        semantic_digest: str,
        state: RunState,
        findings: tuple[Finding, ...],
        transitions: tuple[str, ...],
        *,
        product_snapshot: Mapping[str, str],
    ) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "contract_role": "LOOP_SHADOW_RECEIPT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "source_main_sha": request.source_main_sha,
            "semantic_input_digest": semantic_digest,
            "state": state.value,
            "findings": [finding.to_dict() for finding in findings],
            "transitions": list(transitions),
            "created_at": self.now,
            "mode": "SHADOW",
            "product_mutation": "NONE",
            "model_invocation": "NONE",
            "network": "DENIED",
            "a3_auto_merge": "DISABLED",
            "scheduler_runtime_provider": "NOT_CONFIGURED",
            "product_snapshot": dict(sorted(product_snapshot.items())),
        }
