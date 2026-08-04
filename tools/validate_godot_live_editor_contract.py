from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


TERMINAL_TASK_STATES = {"COMPLETED", "FAILED", "CANCELLED", "STALE"}


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def validate_manifest_semantics(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list):
        return ["CAPABILITY_CATALOG_INVALID"]

    counts: dict[str, int] = {}
    indexed: dict[str, list[Mapping[str, Any]]] = {}
    for capability in capabilities:
        if not isinstance(capability, Mapping):
            errors.append("CAPABILITY_CATALOG_INVALID")
            continue
        capability_id = capability.get("capability_id")
        if not isinstance(capability_id, str) or not capability_id:
            errors.append("CAPABILITY_ID_INVALID")
            continue
        counts[capability_id] = counts.get(capability_id, 0) + 1
        indexed.setdefault(capability_id, []).append(capability)

    if any(count > 1 for count in counts.values()):
        errors.append("DUPLICATE_CAPABILITY_ID")

    framework = manifest.get("project_test_framework")
    if isinstance(framework, Mapping) and framework.get("state") == "CONFIGURED":
        runner_id = framework.get("runner_capability_id")
        matches = indexed.get(runner_id, []) if isinstance(runner_id, str) else []
        if len(matches) != 1:
            errors.append("PROJECT_TEST_RUNNER_NOT_DECLARED")
        else:
            runner = matches[0]
            evidence = runner.get("evidence_outputs")
            if not isinstance(evidence, list) or "TEST_RESULT" not in evidence:
                errors.append("PROJECT_TEST_RUNNER_EVIDENCE_INVALID")
            if runner.get("execution_path") not in {"CLI_HEADLESS", "EDITOR_PLUGIN"}:
                errors.append("PROJECT_TEST_RUNNER_EXECUTION_PATH_INVALID")

    return _unique(errors)


def validate_operation_semantics(envelope: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    approval = envelope.get("approval")
    if isinstance(approval, Mapping) and approval.get("state") == "APPROVED":
        binding = approval.get("token_binding")
        expected = {
            "project_fingerprint": envelope.get("project_fingerprint"),
            "capability_id": envelope.get("capability_id"),
            "request_hash": envelope.get("request_hash"),
            "effect_class": envelope.get("effect_class"),
        }
        if not isinstance(binding, Mapping) or any(
            binding.get(key) != value for key, value in expected.items()
        ):
            errors.append("APPROVAL_TOKEN_MISMATCH")

    task = envelope.get("task")
    if isinstance(task, Mapping) and task.get("state") in TERMINAL_TASK_STATES:
        binding = task.get("result_binding")
        expected = {
            "project_fingerprint": envelope.get("project_fingerprint"),
            "capability_id": envelope.get("capability_id"),
            "operation_id": envelope.get("operation_id"),
            "task_id": task.get("task_id"),
        }
        if not isinstance(binding, Mapping) or any(
            binding.get(key) != value for key, value in expected.items()
        ):
            errors.append("TASK_RESULT_STALE")
        else:
            result = envelope.get("result")
            result_hash = result.get("result_hash") if isinstance(result, Mapping) else None
            if binding.get("result_hash") != result_hash:
                errors.append("TASK_RESULT_HASH_MISMATCH")

    return _unique(errors)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Godot live-editor semantic bindings."
    )
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--operation", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    if args.manifest is not None:
        errors.extend(validate_manifest_semantics(_load(args.manifest)))
    if args.operation is not None:
        errors.extend(validate_operation_semantics(_load(args.operation)))
    errors = _unique(errors)
    print(
        json.dumps(
            {"status": "PASS" if not errors else "FAIL", "errors": errors},
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
