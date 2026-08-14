from __future__ import annotations

from typing import Any

from .contract import parse_shadow_request
from .kernel import ShadowKernel as _BaseShadowKernel
from .models import Finding, FindingCode, RunState, ShadowOutcome, ShadowRequest
from .paths import UnsafePath, UnsafeSymlink, resolve_project_path
from .storage import (
    LeaseLedgerCorruptError,
    ReceiptCorruptError,
    StateStorage,
    UnsafeStateTreeError,
)


class ShadowKernel(_BaseShadowKernel):
    """Fail-closed guard layer for trusted state and authority evidence."""

    def shadow(self, request_value: object) -> ShadowOutcome:
        validated_state_root, state_findings = self._validated_state_root()
        if validated_state_root is None:
            return ShadowOutcome(RunState.BLOCKED_PROJECT_ISOLATION, state_findings)

        request, contract_findings = parse_shadow_request(request_value)
        if request is None:
            return ShadowOutcome(RunState.BLOCKED_INVALID_CONTRACT, contract_findings)

        storage = StateStorage(validated_state_root)
        existing_receipt = False
        try:
            existing_receipt = storage.receipt_exists(request.project_id, request.run_id)
            if existing_receipt:
                storage.read_receipt(request.project_id, request.run_id)
        except ReceiptCorruptError as error:
            return ShadowOutcome(
                RunState.BLOCKED_INVALID_CONTRACT,
                (Finding(FindingCode.RECEIPT_CORRUPT, str(error)),),
                (RunState.CREATED.value,),
            )
        except UnsafeStateTreeError as error:
            return ShadowOutcome(
                RunState.BLOCKED_PROJECT_ISOLATION,
                (Finding(FindingCode.UNSAFE_STATE_ROOT, str(error), str(validated_state_root)),),
                (RunState.CREATED.value,),
            )

        try:
            outcome = super().shadow(request_value)
        except LeaseLedgerCorruptError as error:
            return ShadowOutcome(
                RunState.BLOCKED_LEASE_CONFLICT,
                (Finding(FindingCode.LEASE_LEDGER_CORRUPT, str(error)),),
                (RunState.CREATED.value,),
            )

        if outcome.state is RunState.BLOCKED_RECEIPT_EXISTS and not existing_receipt:
            try:
                storage.read_receipt(request.project_id, request.run_id)
            except ReceiptCorruptError as error:
                return ShadowOutcome(
                    RunState.BLOCKED_INVALID_CONTRACT,
                    (Finding(FindingCode.RECEIPT_CORRUPT, str(error)),),
                    outcome.transitions,
                )
            except UnsafeStateTreeError as error:
                return ShadowOutcome(
                    RunState.BLOCKED_PROJECT_ISOLATION,
                    (Finding(FindingCode.UNSAFE_STATE_ROOT, str(error), str(validated_state_root)),),
                    outcome.transitions,
                )
        return outcome

    def _isolation_findings(self, request: ShadowRequest) -> tuple[Finding, ...]:
        findings = list(super()._isolation_findings(request))
        unsafe_reference_paths = {
            finding.path
            for finding in findings
            if finding.code in {
                FindingCode.UNSAFE_PROJECT_PATH,
                FindingCode.UNSAFE_SYMLINK,
            }
            and finding.path is not None
        }
        for reference in request.references:
            if reference.path in unsafe_reference_paths:
                continue
            try:
                confined = resolve_project_path(self.project_root, reference.path)
            except (OSError, UnsafePath, UnsafeSymlink):
                continue
            if not confined.physical.is_file():
                findings.append(
                    Finding(
                        FindingCode.REFERENCE_MISSING,
                        "authority reference is missing or is not a file",
                        reference.path,
                    )
                )
        return tuple(findings)
