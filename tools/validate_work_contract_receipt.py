from __future__ import annotations

"""Fail closed validation for repository-owned L1+ work-contract receipts."""

import argparse
import json
from pathlib import Path
from typing import Any


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
    """Return all contract errors; an empty list means the receipt is valid."""
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]

    errors: list[str] = []
    work_level = receipt.get("work_level")
    if work_level not in {"L0", "L1", "L2", "L3", "L4"}:
        errors.append("work_level must be one of L0, L1, L2, L3, L4")

    benchmark = receipt.get("benchmark_preflight_receipt")
    if not isinstance(benchmark, dict):
        errors.append("benchmark_preflight_receipt is required")
    else:
        state = benchmark.get("state")
        if state not in BENCHMARK_STATES:
            errors.append("benchmark_preflight_receipt.state is invalid")
        if state in {"PASS", "REUSED_EVIDENCE"}:
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
                    if entry.get("disposition") not in DISPOSITIONS:
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
                if item.get("classification") not in HYGIENE_CLASSIFICATIONS:
                    errors.append(
                        f"context_configuration_hygiene.inventory[{index}].classification is invalid"
                    )
                if item.get("removal_proposed") is True:
                    if item.get("references_and_consumers_zero_before_removal") is not True:
                        errors.append("references_and_consumers_zero_before_removal is required")
                    if item.get("git_recoverable_removal_and_readback") is not True:
                        errors.append("git_recoverable_removal_and_readback is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WORK CONTRACT RECEIPT: FAIL\n- cannot read JSON receipt: {exc}")
        return 2
    errors = validate_receipt(receipt)
    if errors:
        print("WORK CONTRACT RECEIPT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("WORK CONTRACT RECEIPT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
