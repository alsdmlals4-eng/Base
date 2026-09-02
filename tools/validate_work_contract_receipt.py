from __future__ import annotations

"""Fail closed validation for repository-owned L1+ work-contract receipts."""

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

if __package__:
    from .project_work_tracking import choice, render_tracking, validate_tracking
else:
    from project_work_tracking import choice, render_tracking, validate_tracking

BENCHMARK_STATES = {"PASS", "REUSED_EVIDENCE", "NOT_APPLICABLE", "BLOCKED_UNVERIFIED"}
DISPOSITIONS = {"ADOPT", "ADAPT", "REJECT"}
HYGIENE_CLASSIFICATIONS = {"ACTIVE_OWNER", "COMPATIBILITY", "ARCHIVE", "OBSOLETE_CANDIDATE", "UNKNOWN_UNVERIFIED"}
PROMPT_CONTEXT_AUTHORITIES = {
    "CURRENT_USER_INSTRUCTION",
    "PROJECT_REPOSITORY_CANON",
    "BASE_CONTRACT",
    "ACTUAL_IMPLEMENTATION_EVIDENCE",
    "REFERENCE_ONLY",
    "UNTRUSTED_CONTEXT",
}
PROMPT_APPROVAL_AUTHORITIES = {
    "CURRENT_USER_MESSAGE",
    "REPOSITORY_APPROVED_DECISION",
}
PROMPT_APPROVAL_STATES = {
    "AWAITING_USER_CONFIRMATION",
    "CONFIRMED",
    "REUSED_APPROVAL",
    "NOT_APPLICABLE",
}
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
_EXACT_SHA = re.compile(r"[0-9a-f]{40}\Z")
_EXACT_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_RENDER_MISSING_HEAD = "0" * 40
_RENDER_UNTRUSTED_RECORDED_HEAD = "1" * 40


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def _text_list(value: Any) -> bool:
    return _nonempty_list(value) and all(_nonempty_string(item) for item in value)


def compute_prompt_contract_sha256(gate: object) -> str | None:
    """Digest the exact prompt contract and conflict scan; this is drift detection, not identity proof."""
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
    phase: str,
) -> list[str]:
    """Validate prompt preparation and execution authorization for one root receipt."""
    if gate is None and work_level == "L0":
        return []
    if gate is None:
        return ["prompt_approval_gate is required for L1+ execution"]
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
            errors.append(f"{prefix}.approval.state must be NOT_APPLICABLE when applicability is NOT_APPLICABLE")
        elif not _nonempty_string(approval.get("reason_not_applicable")):
            errors.append(f"{prefix}.approval.reason_not_applicable is required")
        return errors
    if applicability != "REQUIRED":
        errors.append(f"{prefix}.applicability must be REQUIRED")

    contract = gate.get("contract")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}.contract must be an object")
    else:
        for field in ("direction_anchor", "task_and_success"):
            if not _nonempty_string(contract.get(field)):
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
                if not _nonempty_string(source.get("source")):
                    errors.append(f"{source_prefix}.source is required")
                if not choice(source.get("authority"), PROMPT_CONTEXT_AUTHORITIES):
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
    if not choice(state, PROMPT_APPROVAL_STATES):
        errors.append(f"{prefix}.approval.state is invalid")
        return errors

    if not _nonempty_string(approval.get("confirmation_question")):
        errors.append(f"{prefix}.approval.confirmation_question is required")
    if not _nonempty_string(approval.get("approved_contract_summary")):
        errors.append(f"{prefix}.approval.approved_contract_summary is required")
    if approval.get("scope_changed_since_approval") is not False:
        errors.append(f"{prefix}.approval.scope_changed_since_approval must be false")

    execution_phase = phase in {"start", "resume", "closeout"}
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
        errors.append(f"{prefix}.approval.state NOT_APPLICABLE requires applicability NOT_APPLICABLE")
        return errors

    if not _nonempty_string(approval.get("approval_reference")):
        errors.append(f"{prefix}.approval.approval_reference is required")
    if not choice(approval.get("approval_reference_authority"), PROMPT_APPROVAL_AUTHORITIES):
        errors.append(f"{prefix}.approval.approval_reference_authority is invalid")

    approved_digest = approval.get("approved_contract_sha256")
    if not isinstance(approved_digest, str) or _EXACT_SHA256.fullmatch(approved_digest) is None:
        errors.append(f"{prefix}.approval.approved_contract_sha256 must be an exact lowercase SHA-256")
    else:
        actual_digest = compute_prompt_contract_sha256(gate)
        if actual_digest is None or approved_digest != actual_digest:
            errors.append(f"{prefix}.approval.approved_contract_sha256 does not match current prompt contract")

    return errors


def _render_inputs(
    board: dict[str, Any],
    *,
    phase: str,
    expected_head_sha: str | None,
) -> tuple[dict[str, Any], str | None]:
    """Apply trusted-head relabeling only to the final closeout phase."""
    if phase != "closeout":
        return board, None
    if isinstance(expected_head_sha, str) and _EXACT_SHA.fullmatch(expected_head_sha) is not None:
        return board, expected_head_sha

    rendered = copy.deepcopy(board)
    work_items = rendered.get("work_items")
    if isinstance(work_items, list):
        for task in work_items:
            if isinstance(task, dict) and task.get("status") == "DONE":
                task["verified_head_sha"] = _RENDER_UNTRUSTED_RECORDED_HEAD
    return rendered, _RENDER_MISSING_HEAD


def validate_receipt(receipt: object) -> list[str]:
    """Historical record shape only; execution callers use validate_execution_receipt."""
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]
    errors: list[str] = []
    work_level = receipt.get("work_level")
    if not choice(work_level, {"L0", "L1", "L2", "L3", "L4"}):
        errors.append("work_level must be one of L0, L1, L2, L3, L4")
    benchmark = receipt.get("benchmark_preflight_receipt")
    if not isinstance(benchmark, dict):
        errors.append("benchmark_preflight_receipt is required")
    else:
        state = benchmark.get("state")
        if not choice(state, BENCHMARK_STATES):
            errors.append("benchmark_preflight_receipt.state is invalid")
        if choice(state, {"PASS", "REUSED_EVIDENCE"}):
            entries = benchmark.get("entries")
            if not _nonempty_list(entries):
                errors.append(f"benchmark_preflight_receipt.entries is required for {state}")
            else:
                for index, entry in enumerate(entries):
                    if not isinstance(entry, dict):
                        errors.append(f"benchmark_preflight_receipt.entries[{index}] must be an object")
                        continue
                    for field in ("source_and_evidence", "observed_pattern", "project_fit_and_difference"):
                        if not _nonempty_string(entry.get(field)):
                            errors.append(f"benchmark_preflight_receipt.entries[{index}].{field} is required")
                    if not choice(entry.get("disposition"), DISPOSITIONS):
                        errors.append(f"benchmark_preflight_receipt.entries[{index}].disposition must be ADOPT, ADAPT, or REJECT")
        elif state == "NOT_APPLICABLE":
            if work_level != "L0":
                errors.append("NOT_APPLICABLE is restricted to L0")
            if not _nonempty_string(benchmark.get("reason_not_applicable")):
                errors.append("reason_not_applicable is required for NOT_APPLICABLE")
        elif state == "BLOCKED_UNVERIFIED" and not _nonempty_list(benchmark.get("blocked_sources")):
            errors.append("blocked_sources is required for BLOCKED_UNVERIFIED")
    hygiene = receipt.get("context_configuration_hygiene")
    if not isinstance(hygiene, dict):
        errors.append("context_configuration_hygiene is required")
    else:
        if not _nonempty_string(hygiene.get("scope")):
            errors.append("context_configuration_hygiene.scope is required")
        inventory = hygiene.get("inventory")
        if not _nonempty_list(inventory):
            errors.append("context_configuration_hygiene.inventory is required")
        else:
            for index, item in enumerate(inventory):
                if not isinstance(item, dict):
                    errors.append(f"context_configuration_hygiene.inventory[{index}] must be an object")
                    continue
                for field in ("path", "owner_or_provenance", "references_and_consumers"):
                    if not _nonempty_string(item.get(field)):
                        errors.append(f"context_configuration_hygiene.inventory[{index}].{field} is required")
                if not choice(item.get("classification"), HYGIENE_CLASSIFICATIONS):
                    errors.append(f"context_configuration_hygiene.inventory[{index}].classification is invalid")
                if item.get("removal_proposed") is True:
                    if item.get("references_and_consumers_zero_before_removal") is not True:
                        errors.append("references_and_consumers_zero_before_removal is required")
                    if item.get("git_recoverable_removal_and_readback") is not True:
                        errors.append("git_recoverable_removal_and_readback is required")
    return errors


def validate_execution_receipt(
    receipt: object,
    *,
    phase: str = "start",
    expected_source_sha: str | None = None,
    expected_head_sha: str | None = None,
) -> list[str]:
    """Execution readiness requires prompt approval plus trusted source and verified-subject HEAD values."""
    errors = validate_receipt(receipt)
    if not isinstance(receipt, dict):
        return errors
    if not choice(phase, {"prepare", "start", "resume", "closeout"}):
        errors.append("phase must be prepare, start, resume or closeout")

    work_level = receipt.get("work_level")
    if isinstance(work_level, str):
        errors.extend(
            validate_prompt_approval_gate(
                receipt.get("prompt_approval_gate"),
                work_level=work_level,
                phase=phase,
            )
        )

    benchmark = receipt.get("benchmark_preflight_receipt")
    if isinstance(benchmark, dict) and benchmark.get("state") == "BLOCKED_UNVERIFIED":
        errors.append("BLOCKED_UNVERIFIED benchmark is a record, not execution authorization")

    if receipt.get("work_level") != "L0" or "project_work_kanban" in receipt:
        if expected_source_sha is None:
            errors.append("expected_source_sha from the trusted fresh-read caller is required for execution")
        tracking_phase = "inspect" if phase == "prepare" else phase
        errors.extend(
            validate_tracking(
                receipt.get("project_work_kanban"),
                phase=tracking_phase,
                expected_source_sha=expected_source_sha,
                expected_head_sha=expected_head_sha,
            )
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--phase", choices=("prepare", "start", "resume", "closeout"), default="start")
    parser.add_argument("--expected-source-sha", help="Exact source SHA supplied by the trusted caller; required for L1+")
    parser.add_argument("--expected-head-sha", help="Exact verified-subject HEAD supplied independently by the trusted caller; required for closeout")
    parser.add_argument("--render-markdown", action="store_true", help="Print shape-validated derived prompt and PM views; preparation or blocked execution remains non-authorizing")
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"WORK CONTRACT RECEIPT: FAIL\n- cannot read JSON receipt: {exc}")
        return 2

    errors = validate_execution_receipt(
        receipt,
        phase=args.phase,
        expected_source_sha=args.expected_source_sha,
        expected_head_sha=args.expected_head_sha,
    )
    gate = receipt.get("prompt_approval_gate") if isinstance(receipt, dict) else None
    digest = compute_prompt_contract_sha256(gate)

    if errors:
        print("WORK CONTRACT RECEIPT: FAIL")
        for error in errors:
            print(f"- {error}")
        board = receipt.get("project_work_kanban") if isinstance(receipt, dict) else None
        shape_errors = (
            validate_tracking(
                board,
                phase="inspect",
                expected_source_sha=args.expected_source_sha,
            )
            if isinstance(board, dict)
            else ["project_work_kanban is unavailable"]
        )
        if args.render_markdown:
            print("EXECUTION AUTHORIZED: NO")
            if digest is not None:
                print(f"PROMPT CONTRACT SHA256: {digest}")
        if args.render_markdown and isinstance(board, dict) and not shape_errors:
            render_board, render_head = _render_inputs(
                board,
                phase=args.phase,
                expected_head_sha=args.expected_head_sha,
            )
            print("PM VIEW: INFORMATION ONLY; EXECUTION BLOCKED")
            print(
                render_tracking(
                    render_board,
                    expected_head_sha=render_head,
                    execution_authorized=False,
                )
            )
        return 1

    if args.phase == "prepare":
        print("WORK CONTRACT RECEIPT: PASS (preparation only; recorded evidence)")
        print("EXECUTION AUTHORIZED: NO")
        if digest is not None:
            print(f"PROMPT CONTRACT SHA256: {digest}")
    else:
        print(f"WORK CONTRACT RECEIPT: PASS (execution phase={args.phase}; recorded evidence only)")
        print("EXECUTION AUTHORIZED: YES")

    if args.render_markdown and isinstance(receipt.get("project_work_kanban"), dict):
        render_board, render_head = _render_inputs(
            receipt["project_work_kanban"],
            phase=args.phase,
            expected_head_sha=args.expected_head_sha,
        )
        print(
            render_tracking(
                render_board,
                expected_head_sha=render_head,
                execution_authorized=args.phase != "prepare",
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
