from __future__ import annotations

"""Fail closed validation for repository-owned L1+ work-contract receipts."""

import argparse
import json
from pathlib import Path
from typing import Any

if __package__:
    from .project_work_tracking import choice, render_tracking, validate_tracking
else:
    from project_work_tracking import choice, render_tracking, validate_tracking


BENCHMARK_STATES = {"PASS", "REUSED_EVIDENCE", "NOT_APPLICABLE", "BLOCKED_UNVERIFIED"}
DISPOSITIONS = {"ADOPT", "ADAPT", "REJECT"}
HYGIENE_CLASSIFICATIONS = {
    "ACTIVE_OWNER",
    "COMPATIBILITY",
    "ARCHIVE",
    "OBSOLETE_CANDIDATE",
    "UNKNOWN_UNVERIFIED",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def validate_receipt(receipt: object) -> list[str]:
    """Validate the historical record shape, NOT readiness to execute a task.

    The CLI and execution callers must use validate_execution_receipt instead.
    """
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
                    for field in (
                        "source_and_evidence",
                        "observed_pattern",
                        "project_fit_and_difference",
                    ):
                        if not _nonempty_string(entry.get(field)):
                            errors.append(
                                f"benchmark_preflight_receipt.entries[{index}].{field} is required"
                            )
                    if not choice(entry.get("disposition"), DISPOSITIONS):
                        errors.append(
                            f"benchmark_preflight_receipt.entries[{index}].disposition must be ADOPT, ADAPT, or REJECT"
                        )
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
                        errors.append(
                            f"context_configuration_hygiene.inventory[{index}].{field} is required"
                        )
                if not choice(item.get("classification"), HYGIENE_CLASSIFICATIONS):
                    errors.append(
                        f"context_configuration_hygiene.inventory[{index}].classification is invalid"
                    )
                if item.get("removal_proposed") is True:
                    if item.get("references_and_consumers_zero_before_removal") is not True:
                        errors.append("references_and_consumers_zero_before_removal is required")
                    if item.get("git_recoverable_removal_and_readback") is not True:
                        errors.append("git_recoverable_removal_and_readback is required")
    return errors


def validate_execution_receipt(receipt: object, *, phase: str = "start", expected_source_sha: str | None = None) -> list[str]:
    """Check execution readiness plus the existing PM operational receipt."""
    errors = validate_receipt(receipt)
    if not isinstance(receipt, dict):
        return errors
    if not choice(phase, {"start", "resume", "closeout"}):
        errors.append("phase must be start, resume or closeout")
    benchmark = receipt.get("benchmark_preflight_receipt")
    if isinstance(benchmark, dict) and benchmark.get("state") == "BLOCKED_UNVERIFIED":
        errors.append("BLOCKED_UNVERIFIED benchmark is a record, not execution authorization")
    if receipt.get("work_level") != "L0" or "project_work_kanban" in receipt:
        errors.extend(validate_tracking(receipt.get("project_work_kanban"), phase=phase, expected_source_sha=expected_source_sha))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--phase", choices=("start", "resume", "closeout"), default="start")
    parser.add_argument("--expected-source-sha", help="Exact source SHA supplied by the trusted caller")
    parser.add_argument("--render-markdown", action="store_true", help="Print a derived PM view after successful validation")
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"WORK CONTRACT RECEIPT: FAIL\n- cannot read JSON receipt: {exc}")
        return 2
    errors = validate_execution_receipt(receipt, phase=args.phase, expected_source_sha=args.expected_source_sha)
    if errors:
        print("WORK CONTRACT RECEIPT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"WORK CONTRACT RECEIPT: PASS (execution phase={args.phase}; recorded evidence only)")
    if args.render_markdown and isinstance(receipt.get("project_work_kanban"), dict):
        print(render_tracking(receipt["project_work_kanban"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
