from __future__ import annotations

"""Validate one source-aware prompt contract before L1+ execution.

This module checks recorded shape, authority vocabulary, conflict state, approval
state, and contract drift. It does not prove the identity or authority of the
human or repository actor referenced by an approval locator.
"""

import hashlib
import json
import re
import unicodedata
from typing import Any


PROMPT_CONTEXT_AUTHORITIES = frozenset(
    {
        "CURRENT_USER_INSTRUCTION",
        "PROJECT_REPOSITORY_CANON",
        "BASE_CONTRACT",
        "ACTUAL_IMPLEMENTATION_EVIDENCE",
        "REFERENCE_ONLY",
        "UNTRUSTED_CONTEXT",
    }
)
PROMPT_APPROVAL_AUTHORITIES = frozenset(
    {
        "CURRENT_USER_MESSAGE",
        "REPOSITORY_APPROVED_DECISION",
    }
)
PROMPT_APPROVAL_STATES = frozenset(
    {
        "AWAITING_USER_CONFIRMATION",
        "CONFIRMED",
        "REUSED_APPROVAL",
        "NOT_APPLICABLE",
    }
)
_REQUIRED_CONFLICT_TRUE = (
    "anchor_matches_task",
    "anchor_matches_output",
    "source_authority_preserved",
    "hard_constraints_preserved",
    "protected_scope_visible",
    "user_decisions_visible",
    "counterevidence_preserved",
    "unverified_claims_labeled",
    "untrusted_context_cannot_authorize",
)
_EXACT_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_SENTINEL_TEXT = frozenset({"TODO", "TBD", "N/A"})
_ALLOWED_TEXT_CONTROL_CHARACTERS = frozenset("\n\r\t")


def _text(value: Any) -> bool:
    """Accept substantive prompt text and reject unfilled or hidden placeholders."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped or stripped.upper() in _SENTINEL_TEXT:
        return False
    if stripped.startswith("<") and stripped.endswith(">"):
        return False
    return not any(
        unicodedata.category(character) in {"Cc", "Cf", "Cs"}
        and character not in _ALLOWED_TEXT_CONTROL_CHARACTERS
        for character in value
    )


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def _text_list(value: Any) -> bool:
    return _nonempty_list(value) and all(_text(item) for item in value)


def _choice(value: Any, allowed: frozenset[str]) -> bool:
    return isinstance(value, str) and value in allowed


def compute_prompt_contract_sha256(gate: object) -> str | None:
    """Digest the exact prompt contract and conflict scan.

    This is deterministic drift detection. It is not an approval signature or
    identity proof.
    """
    if not isinstance(gate, dict):
        return None
    contract = gate.get("contract")
    conflict_scan = gate.get("conflict_scan")
    if not isinstance(contract, dict) or not isinstance(conflict_scan, dict):
        return None
    try:
        canonical = json.dumps(
            {"contract": contract, "conflict_scan": conflict_scan},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_prompt_approval_gate(
    gate: object,
    *,
    work_level: str,
    phase: object,
) -> list[str]:
    """Return fail-closed findings for one root receipt prompt gate."""
    if gate is None and work_level == "L0":
        return []
    if gate is None:
        return [
            "prompt_approval_gate is required for L1+ preparation or execution; "
            "see skills/managing-project-intake-and-work-contract/references/"
            "prompt-approval-execution-gate.md"
        ]
    if not isinstance(gate, dict):
        return ["prompt_approval_gate must be an object"]

    errors: list[str] = []
    prefix = "prompt_approval_gate"

    if type(gate.get("schema_version")) is not int or gate.get("schema_version") != 1:
        errors.append(f"{prefix}.schema_version must be 1")

    applicability = gate.get("applicability")
    if applicability == "NOT_APPLICABLE":
        if work_level != "L0":
            errors.append(f"{prefix}.applicability NOT_APPLICABLE is restricted to L0")
        approval = gate.get("approval")
        if not isinstance(approval, dict) or approval.get("state") != "NOT_APPLICABLE":
            errors.append(
                f"{prefix}.approval.state must be NOT_APPLICABLE when applicability is NOT_APPLICABLE"
            )
        elif not _text(approval.get("reason_not_applicable")):
            errors.append(f"{prefix}.approval.reason_not_applicable is required")
        return errors
    if applicability != "REQUIRED":
        errors.append(f"{prefix}.applicability must be REQUIRED")

    contract = gate.get("contract")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}.contract must be an object")
    else:
        for field in ("direction_anchor", "task_and_success"):
            if not _text(contract.get(field)):
                errors.append(f"{prefix}.contract.{field} is required")
        for field in ("constraints_and_protected_scope", "output_and_validation"):
            if not _text_list(contract.get(field)):
                errors.append(f"{prefix}.contract.{field} must be a nonempty text list")
        sources = contract.get("context_and_sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}.contract.context_and_sources must be a nonempty list")
        else:
            for index, source in enumerate(sources):
                source_prefix = f"{prefix}.contract.context_and_sources[{index}]"
                if not isinstance(source, dict):
                    errors.append(f"{source_prefix} must be an object")
                    continue
                if not _text(source.get("source")):
                    errors.append(f"{source_prefix}.source is required")
                if not _choice(source.get("authority"), PROMPT_CONTEXT_AUTHORITIES):
                    errors.append(f"{source_prefix}.authority is invalid")

    conflict_scan = gate.get("conflict_scan")
    if not isinstance(conflict_scan, dict):
        errors.append(f"{prefix}.conflict_scan must be an object")
    else:
        for field in _REQUIRED_CONFLICT_TRUE:
            if conflict_scan.get(field) is not True:
                errors.append(f"{prefix}.conflict_scan.{field} must be true")
        if conflict_scan.get("later_instruction_conflict") is not False:
            errors.append(f"{prefix}.conflict_scan.later_instruction_conflict must be false")
        unresolved = conflict_scan.get("unresolved_material_decisions")
        if not isinstance(unresolved, list):
            errors.append(f"{prefix}.conflict_scan.unresolved_material_decisions must be a list")
        elif unresolved:
            errors.append(f"{prefix}.conflict_scan.unresolved_material_decisions must be empty")

    approval = gate.get("approval")
    if not isinstance(approval, dict):
        errors.append(f"{prefix}.approval must be an object")
        return errors

    state = approval.get("state")
    if not _choice(state, PROMPT_APPROVAL_STATES):
        errors.append(f"{prefix}.approval.state is invalid")
        return errors

    if not _text(approval.get("confirmation_question")):
        errors.append(f"{prefix}.approval.confirmation_question is required")
    if not _text(approval.get("approved_contract_summary")):
        errors.append(f"{prefix}.approval.approved_contract_summary is required")
    if approval.get("scope_changed_since_approval") is not False:
        errors.append(f"{prefix}.approval.scope_changed_since_approval must be false")

    execution_phase = isinstance(phase, str) and phase in {"start", "resume", "closeout"}
    if state == "AWAITING_USER_CONFIRMATION":
        if execution_phase:
            errors.append(f"{prefix}.approval: {phase} requires CONFIRMED or REUSED_APPROVAL")
        for field in (
            "approval_reference",
            "approval_reference_authority",
            "approved_contract_sha256",
        ):
            if approval.get(field) is not None:
                errors.append(f"{prefix}.approval.{field} must be null while awaiting confirmation")
        return errors

    if state == "NOT_APPLICABLE":
        errors.append(
            f"{prefix}.approval.state NOT_APPLICABLE requires applicability NOT_APPLICABLE"
        )
        return errors

    if not _text(approval.get("approval_reference")):
        errors.append(f"{prefix}.approval.approval_reference is required")
    if not _choice(
        approval.get("approval_reference_authority"), PROMPT_APPROVAL_AUTHORITIES
    ):
        errors.append(f"{prefix}.approval.approval_reference_authority is invalid")

    approved_digest = approval.get("approved_contract_sha256")
    if not isinstance(approved_digest, str) or _EXACT_SHA256.fullmatch(approved_digest) is None:
        errors.append(
            f"{prefix}.approval.approved_contract_sha256 must be an exact lowercase SHA-256"
        )
    else:
        actual_digest = compute_prompt_contract_sha256(gate)
        if actual_digest is None or approved_digest != actual_digest:
            errors.append(
                f"{prefix}.approval.approved_contract_sha256 does not match current prompt contract"
            )

    return errors
