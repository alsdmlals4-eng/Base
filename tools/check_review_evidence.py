#!/usr/bin/env python3
"""Check a review record against exact Git state and freshly run checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
OWNER = Path("skills/reviewing-and-validating-project-changes")
RECORD_SCHEMA = OWNER / "contracts/review-record.schema.json"
RESULT_SCHEMA = OWNER / "contracts/review-result.schema.json"
LEVELS = {"STATIC": 0, "TEST": 1, "RUNTIME": 2, "RENDER": 3, "HUMAN": 4}
TAIL_LIMIT = 4000


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(
    root: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def schema_errors(document: Any, schema: Any, label: str) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: [str(part) for part in item.path],
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label} schema {location}: {error.message}")
    return errors


def normalize_path(
    value: str,
    field: str,
    errors: list[str],
    *,
    allow_dot: bool = False,
) -> str | None:
    normalized = value.replace("\\", "/")
    path = Path(normalized)
    if (
        path.is_absolute()
        or ".." in path.parts
        or re.match(r"^[A-Za-z]:/", normalized) is not None
    ):
        errors.append(f"{field} must stay repository-relative: {value}")
        return None
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized:
        if allow_dot:
            return "."
        errors.append(f"{field} must not be empty")
        return None
    if normalized == "." and not allow_dot:
        errors.append(f"{field} must identify a repository path")
        return None
    return normalized


def glob_pattern_to_regex(pattern: str) -> re.Pattern[str]:
    """Compile repository globs where `*` never crosses `/` and brackets are literal."""

    normalized = pattern.replace("\\", "/")
    pieces = ["^"]
    index = 0
    while index < len(normalized):
        if normalized.startswith("**/", index):
            pieces.append("(?:.*/)?")
            index += 3
            continue
        if normalized.startswith("**", index):
            pieces.append(".*")
            index += 2
            continue
        character = normalized[index]
        if character == "*":
            pieces.append("[^/]*")
        elif character == "?":
            pieces.append("[^/]")
        else:
            pieces.append(re.escape(character))
        index += 1
    pieces.append("$")
    return re.compile("".join(pieces))


def matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(
        glob_pattern_to_regex(pattern).fullmatch(normalized) is not None
        for pattern in patterns
    )


def tail(value: str) -> str:
    return value if len(value) <= TAIL_LIMIT else value[-TAIL_LIMIT:]


def empty_result(record_path: Path, base_ref: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_role": "REVIEW_EVIDENCE_RESULT",
        "record_path": record_path.as_posix(),
        "subject": {
            "base_ref": base_ref,
            "base_sha": None,
            "head_sha": None,
            "changed_files": [],
        },
        "gates": {
            "implementation": {
                "status": "FAIL",
                "mapped_acceptance_ids": [],
                "actual_changed_paths": [],
            },
            "verification": {"status": "NOT_RUN", "checks": []},
            "intent": {
                "status": "BLOCKED_UNVERIFIED",
                "acceptance_results": [],
            },
            "integration": {
                "status": "BLOCKED_UNVERIFIED",
                "reason": (
                    "Pre-merge review cannot prove merged PR state, merge SHA, "
                    "post-merge main readback, or post-merge required checks."
                ),
            },
        },
        "claims": [],
        "final_status": "FAIL",
        "errors": [],
    }


def unique_ids(
    records: Sequence[dict[str, Any]],
    field: str,
    label: str,
    errors: list[str],
) -> set[str]:
    values: set[str] = set()
    for record in records:
        value = record[field]
        if value in values:
            errors.append(f"duplicate {label}: {value}")
        values.add(value)
    return values


def resolve_working_directory(
    root: Path,
    value: str,
    check_id: str,
    errors: list[str],
) -> tuple[str, Path | None]:
    normalized = normalize_path(
        value,
        f"check {check_id} working_directory",
        errors,
        allow_dot=True,
    )
    if normalized is None:
        return value, None
    candidate = (root / normalized).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        errors.append(f"check {check_id} working_directory escapes repository: {value}")
        return normalized, None
    if not candidate.is_dir():
        errors.append(f"check {check_id} working_directory does not exist: {normalized}")
        return normalized, None
    return normalized, candidate


def resolve_argv(argv: Sequence[str]) -> list[str]:
    return [sys.executable if value == "{python}" else value for value in argv]


def program_allowed(program: str, allowed_programs: Sequence[str]) -> bool:
    resolved_python = str(Path(sys.executable).resolve())
    candidate = Path(program)
    candidate_value = str(candidate.resolve()) if candidate.is_absolute() else program
    if candidate_value == resolved_python:
        return True
    for allowed in allowed_programs:
        allowed_path = Path(allowed)
        if allowed_path.is_absolute() and candidate.is_absolute():
            if candidate.resolve() == allowed_path.resolve():
                return True
        elif program == allowed:
            return True
    return False


def observed_level(declared: str, approved: str | None) -> str:
    ceiling = approved or "TEST"
    return declared if LEVELS[declared] <= LEVELS[ceiling] else ceiling


def run_checks(
    root: Path,
    checks: Sequence[dict[str, Any]],
    *,
    execute_checks: bool,
    allowed_programs: Sequence[str],
    approved_levels: Mapping[str, str],
) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    for check in checks:
        check_id = check["check_id"]
        argv = resolve_argv(check["argv"])
        working_directory, cwd = resolve_working_directory(
            root,
            check["working_directory"],
            check_id,
            errors,
        )
        result = {
            "check_id": check_id,
            "argv": argv,
            "working_directory": working_directory,
            "declared_level": check["declared_level"],
            "observed_level": None,
            "status": "NOT_RUN",
            "exit_code": None,
            "duration_ms": 0,
            "stdout_tail": "",
            "stderr_tail": "",
            "acceptance_ids": list(check["acceptance_ids"]),
        }
        results.append(result)
        if not execute_checks:
            continue
        if cwd is None:
            result["status"] = "FAIL"
            continue
        if not program_allowed(argv[0], allowed_programs):
            errors.append(f"check {check_id} program is not approved: {argv[0]}")
            result["status"] = "FAIL"
            continue
        environment = dict(os.environ)
        environment.setdefault("PYTHONDONTWRITEBYTECODE", "1")
        environment.setdefault("PYTHONUTF8", "1")
        started = time.monotonic()
        try:
            completed = subprocess.run(
                argv,
                cwd=cwd,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=check["timeout_seconds"],
            )
            result["duration_ms"] = max(
                0,
                int((time.monotonic() - started) * 1000),
            )
            result["exit_code"] = completed.returncode
            result["stdout_tail"] = tail(completed.stdout)
            result["stderr_tail"] = tail(completed.stderr)
            combined = f"{completed.stdout}\n{completed.stderr}"
            missing = [
                marker
                for marker in check["markers"]
                if marker not in combined
            ]
            if completed.returncode != 0:
                result["status"] = "FAIL"
                errors.append(
                    f"check {check_id} failed with exit code {completed.returncode}"
                )
            elif missing:
                result["status"] = "FAIL"
                for marker in missing:
                    errors.append(
                        f"check {check_id} missing required marker: {marker}"
                    )
            else:
                result["status"] = "PASS"
                result["observed_level"] = observed_level(
                    check["declared_level"],
                    approved_levels.get(check_id),
                )
        except subprocess.TimeoutExpired as error:
            result["duration_ms"] = max(
                0,
                int((time.monotonic() - started) * 1000),
            )
            result["status"] = "FAIL"
            result["stdout_tail"] = tail(error.stdout or "")
            result["stderr_tail"] = tail(error.stderr or "")
            errors.append(
                f"check {check_id} timed out after {check['timeout_seconds']} seconds"
            )
        except OSError as error:
            result["duration_ms"] = max(
                0,
                int((time.monotonic() - started) * 1000),
            )
            result["status"] = "FAIL"
            result["stderr_tail"] = str(error)
            errors.append(f"check {check_id} could not start: {error}")
    if not execute_checks:
        errors.append(
            "declared checks were not executed; rerun with --execute-checks"
        )
    return results, errors


def repository_state(root: Path, base_ref: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    subject: dict[str, Any] = {
        "base_ref": base_ref,
        "base_sha": None,
        "head_sha": None,
        "changed_files": [],
    }
    try:
        top = Path(
            run_git(root, "rev-parse", "--show-toplevel").stdout.strip()
        ).resolve()
        if top != root.resolve():
            errors.append("root is not the repository top-level")
        base_sha = run_git(
            root,
            "rev-parse",
            "--verify",
            f"{base_ref}^{{commit}}",
        ).stdout.strip()
        head_sha = run_git(root, "rev-parse", "HEAD").stdout.strip()
        subject["base_sha"] = base_sha
        subject["head_sha"] = head_sha
        ancestor = run_git(
            root,
            "merge-base",
            "--is-ancestor",
            base_sha,
            head_sha,
            check=False,
        )
        if ancestor.returncode != 0:
            errors.append("trusted base is not an ancestor of current HEAD")
        dirty = run_git(
            root,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout.splitlines()
        if dirty:
            errors.append("worktree must be clean before review record checking")
        changed = sorted(
            {
                line.strip().replace("\\", "/")
                for line in run_git(
                    root,
                    "diff",
                    "--name-only",
                    "--diff-filter=ACDMRTUXB",
                    f"{base_sha}...{head_sha}",
                ).stdout.splitlines()
                if line.strip()
            }
        )
        subject["changed_files"] = changed
        if not changed:
            errors.append(
                "no changed files exist between trusted base and current HEAD"
            )
    except (OSError, subprocess.CalledProcessError) as error:
        errors.append(f"repository state unavailable: {error}")
    return subject, errors


def repository_state_changed(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    after_errors: Sequence[str],
) -> list[str]:
    details: list[str] = []
    if after_errors:
        details.extend(f"post-check: {error}" for error in after_errors)
    for field in ("base_sha", "head_sha", "changed_files"):
        if before.get(field) != after.get(field):
            details.append(
                f"post-check {field} changed: "
                f"expected {before.get(field)!r}, observed {after.get(field)!r}"
            )
    if details:
        return ["repository state changed during checks", *details]
    return []


def check_record(
    root: Path,
    record_path: Path,
    base_ref: str,
    *,
    execute_checks: bool,
    allowed_programs: Sequence[str] = (),
    approved_levels: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    root = root.resolve()
    approved_levels = approved_levels or {}
    if not record_path.is_absolute():
        record_path = root / record_path
    record_path = record_path.resolve()
    if record_path != root and root not in record_path.parents:
        result = empty_result(record_path, base_ref)
        errors = ["review record must stay inside the repository"]
        result["errors"] = errors
        return result, errors

    result = empty_result(record_path, base_ref)
    contract_errors: list[str] = []
    implementation_errors: list[str] = []
    intent_errors: list[str] = []
    claim_errors: list[str] = []

    try:
        record = read_json(record_path)
        record_schema = read_json(ROOT / RECORD_SCHEMA)
        result_schema = read_json(ROOT / RESULT_SCHEMA)
    except (OSError, json.JSONDecodeError) as error:
        errors = [f"record or schema unavailable: {error}"]
        result["errors"] = errors
        return result, errors

    contract_errors.extend(
        schema_errors(record, record_schema, "review record")
    )
    if contract_errors:
        result["errors"] = contract_errors
        return result, contract_errors

    claims: list[dict[str, Any]] = record["claims"]
    acceptance: list[dict[str, Any]] = record["acceptance"]
    checks: list[dict[str, Any]] = record["checks"]
    unique_ids(claims, "claim_id", "claim_id", contract_errors)
    acceptance_ids = unique_ids(
        acceptance,
        "intent_id",
        "intent_id",
        contract_errors,
    )
    check_ids = unique_ids(checks, "check_id", "check_id", contract_errors)

    for check_id, level in approved_levels.items():
        if check_id not in check_ids:
            contract_errors.append(
                f"level approval references unknown check: {check_id}"
            )
        if level not in {"RUNTIME", "RENDER"}:
            contract_errors.append(
                f"level approval for {check_id} must be RUNTIME or RENDER: {level}"
            )
    for claim in claims:
        for intent_id in claim["acceptance_ids"]:
            if intent_id not in acceptance_ids:
                contract_errors.append(
                    f"claim {claim['claim_id']} references unknown acceptance: "
                    f"{intent_id}"
                )
        for check_id in claim["check_ids"]:
            if check_id not in check_ids:
                contract_errors.append(
                    f"claim {claim['claim_id']} references unknown check: "
                    f"{check_id}"
                )
    for check in checks:
        for intent_id in check["acceptance_ids"]:
            if intent_id not in acceptance_ids:
                contract_errors.append(
                    f"check {check['check_id']} covers unknown acceptance: "
                    f"{intent_id}"
                )
    if contract_errors:
        result["errors"] = contract_errors
        return result, contract_errors

    subject, git_errors = repository_state(root, base_ref)
    result["subject"] = subject
    changed_files = subject["changed_files"]

    allowed_patterns: list[str] = []
    protected_patterns: list[str] = []
    for field, values, target in (
        (
            "scope.allowed_changed_paths",
            record["scope"]["allowed_changed_paths"],
            allowed_patterns,
        ),
        (
            "scope.protected_paths",
            record["scope"]["protected_paths"],
            protected_patterns,
        ),
    ):
        for value in values:
            normalized = normalize_path(value, field, implementation_errors)
            if normalized is not None:
                target.append(normalized)

    for path in changed_files:
        if not matches(path, allowed_patterns):
            implementation_errors.append(
                f"changed path is outside allowed scope: {path}"
            )
        if matches(path, protected_patterns):
            implementation_errors.append(f"protected path changed: {path}")

    acceptance_path_state: dict[str, str] = {}
    mapped_ids: list[str] = []
    for item in acceptance:
        intent_id = item["intent_id"]
        before_error_count = len(implementation_errors)
        for value in item["implementation_paths"]:
            normalized = normalize_path(
                value,
                f"acceptance {intent_id} implementation_paths",
                implementation_errors,
            )
            if normalized is None:
                continue
            if normalized not in changed_files:
                implementation_errors.append(
                    f"acceptance {intent_id} implementation path is not changed: "
                    f"{normalized}"
                )
            elif not (root / normalized).is_file():
                implementation_errors.append(
                    f"acceptance {intent_id} implementation path is not a file "
                    f"at HEAD: {normalized}"
                )
        if len(implementation_errors) == before_error_count:
            acceptance_path_state[intent_id] = "PASS"
            mapped_ids.append(intent_id)
        else:
            acceptance_path_state[intent_id] = "FAIL"

    implementation_status = (
        "PASS" if not git_errors and not implementation_errors else "FAIL"
    )
    result["gates"]["implementation"] = {
        "status": implementation_status,
        "mapped_acceptance_ids": mapped_ids,
        "actual_changed_paths": changed_files,
    }

    check_results, check_errors = run_checks(
        root,
        checks,
        execute_checks=execute_checks,
        allowed_programs=allowed_programs,
        approved_levels=approved_levels,
    )
    if execute_checks:
        post_subject, post_errors = repository_state(root, base_ref)
        check_errors.extend(
            repository_state_changed(subject, post_subject, post_errors)
        )

    if not execute_checks:
        check_status = "NOT_RUN"
    elif check_errors or any(
        item["status"] != "PASS" for item in check_results
    ):
        check_status = "FAIL"
    else:
        check_status = "PASS"
    result["gates"]["verification"] = {
        "status": check_status,
        "checks": check_results,
    }

    check_by_id = {item["check_id"]: item for item in check_results}
    acceptance_results: list[dict[str, Any]] = []
    for item in acceptance:
        intent_id = item["intent_id"]
        successful_levels = [
            check["observed_level"]
            for check in check_results
            if check["status"] == "PASS"
            and check["observed_level"] is not None
            and intent_id in check["acceptance_ids"]
        ]
        required = item["required_level"]
        observed = (
            max(successful_levels, key=LEVELS.__getitem__)
            if successful_levels
            else None
        )
        if check_status != "PASS" or observed is None:
            status = "BLOCKED_UNVERIFIED"
            intent_errors.append(
                f"acceptance {intent_id} has no stable successful check evidence"
            )
        elif LEVELS[observed] < LEVELS[required]:
            status = "FAIL"
            intent_errors.append(
                f"acceptance {intent_id} evidence ceiling violation: "
                f"required {required}, observed {observed}"
            )
        else:
            status = "PASS"
        acceptance_results.append(
            {
                "intent_id": intent_id,
                "required_level": required,
                "observed_level": observed,
                "status": status,
            }
        )

    if all(item["status"] == "PASS" for item in acceptance_results):
        intent_status = "PASS"
    elif any(item["status"] == "FAIL" for item in acceptance_results):
        intent_status = "FAIL"
    else:
        intent_status = "BLOCKED_UNVERIFIED"
    result["gates"]["intent"] = {
        "status": intent_status,
        "acceptance_results": acceptance_results,
    }

    acceptance_by_id = {
        item["intent_id"]: item for item in acceptance_results
    }
    claim_results: list[dict[str, Any]] = []
    for claim in claims:
        acceptance_ok = all(
            acceptance_path_state.get(intent_id) == "PASS"
            and acceptance_by_id.get(intent_id, {}).get("status") == "PASS"
            for intent_id in claim["acceptance_ids"]
        )
        checks_ok = all(
            check_by_id.get(check_id, {}).get("status") == "PASS"
            for check_id in claim["check_ids"]
        )
        if claim["claim_type"] == "IMPLEMENTATION":
            verified = (
                implementation_status == "PASS"
                and check_status == "PASS"
                and intent_status == "PASS"
                and acceptance_ok
                and checks_ok
                and bool(claim["acceptance_ids"])
                and bool(claim["check_ids"])
            )
        else:
            verified = (
                check_status == "PASS"
                and checks_ok
                and bool(claim["check_ids"])
            )
        status = "CLAIM_VERIFIED" if verified else "CLAIM_UNVERIFIED"
        if not verified:
            claim_errors.append(
                f"material claim {claim['claim_id']} remains {status}"
            )
        claim_results.append(
            {
                "claim_id": claim["claim_id"],
                "status": status,
                "evidence_ids": [
                    *claim["acceptance_ids"],
                    *claim["check_ids"],
                ],
            }
        )
    result["claims"] = claim_results

    all_errors = [
        *contract_errors,
        *git_errors,
        *implementation_errors,
        *check_errors,
        *intent_errors,
        *claim_errors,
    ]
    result["final_status"] = (
        "PASS"
        if not all_errors
        and implementation_status == "PASS"
        and check_status == "PASS"
        and intent_status == "PASS"
        else "FAIL"
    )
    result["errors"] = all_errors

    generated_errors = schema_errors(
        result,
        result_schema,
        "review result",
    )
    if generated_errors:
        all_errors.extend(generated_errors)
        result["errors"] = all_errors
        result["final_status"] = "FAIL"
    return result, all_errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--execute-checks", action="store_true")
    parser.add_argument("--allow-program", action="append", default=[])
    parser.add_argument(
        "--approve-level",
        action="append",
        default=[],
        metavar="CHECK_ID=RUNTIME|RENDER",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    approvals: dict[str, str] = {}
    for value in arguments.approve_level:
        check_id, separator, level = value.partition("=")
        if (
            not separator
            or not check_id
            or level not in {"RUNTIME", "RENDER"}
        ):
            parser.error(
                "--approve-level must use CHECK_ID=RUNTIME or CHECK_ID=RENDER"
            )
        approvals[check_id] = level

    root = arguments.root.resolve()
    record_path = arguments.record
    if not record_path.is_absolute():
        record_path = root / record_path
    result, errors = check_record(
        root,
        record_path,
        arguments.base_ref,
        execute_checks=arguments.execute_checks,
        allowed_programs=tuple(arguments.allow_program),
        approved_levels=approvals,
    )

    if arguments.output is not None:
        output = arguments.output
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"REVIEW_EVIDENCE_STATUS: {result['final_status']}")
    print(f"BASE_SHA: {result['subject']['base_sha'] or 'UNRESOLVED'}")
    print(f"HEAD_SHA: {result['subject']['head_sha'] or 'UNRESOLVED'}")
    for gate in ("implementation", "verification", "intent", "integration"):
        print(f"{gate.upper()}_GATE: {result['gates'][gate]['status']}")
    for error in errors:
        print(f"- {error}")
    return 0 if result["final_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
