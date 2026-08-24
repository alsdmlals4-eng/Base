#!/usr/bin/env python3
from __future__ import annotations

import os


ALWAYS_REQUIRED = (
    ("classify-changes", "CLASSIFY_RESULT"),
    ("docs-validation", "DOCS_RESULT"),
)
CONDITIONAL = (
    ("core-regression", "CORE_REQUIRED", "CORE_REGRESSION_RESULT"),
    ("ubuntu-contract", "CONTRACT_REQUIRED", "CONTRACT_RESULT"),
    ("publication-validation", "PUBLICATION_REQUIRED", "PUBLICATION_RESULT"),
    ("platform-smoke-windows", "WINDOWS_REQUIRED", "WINDOWS_RESULT"),
)
INPUT_NAMES = (
    "CLASSIFY_RESULT",
    "DOCS_RESULT",
    "CORE_REQUIRED",
    "CORE_REGRESSION_RESULT",
    "CONTRACT_REQUIRED",
    "CONTRACT_RESULT",
    "PUBLICATION_REQUIRED",
    "PUBLICATION_RESULT",
    "WINDOWS_REQUIRED",
    "WINDOWS_RESULT",
)


def evaluate(environment: dict[str, str]) -> list[str]:
    errors = [
        f"missing environment variable: {name}"
        for name in INPUT_NAMES
        if name not in environment
    ]
    if errors:
        return errors

    for _, required_name, _ in CONDITIONAL:
        if environment[required_name] not in {"true", "false"}:
            errors.append(
                f"invalid required flag: {required_name}="
                f"{environment[required_name]!r}; expected 'true' or 'false'"
            )

    for job_name, result_name in ALWAYS_REQUIRED:
        if environment[result_name] != "success":
            errors.append(
                f"required job failed or was not executed: {job_name} "
                f"(result={environment[result_name]})"
            )

    for job_name, required_name, result_name in CONDITIONAL:
        if (
            environment[required_name] == "true"
            and environment[result_name] != "success"
        ):
            errors.append(
                f"required job failed or was not executed: {job_name} "
                f"(result={environment[result_name]})"
            )
    return errors


def main() -> int:
    errors = evaluate(dict(os.environ))
    if errors:
        print("CI REQUIRED GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CI REQUIRED GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
