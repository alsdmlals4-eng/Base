from __future__ import annotations

import copy
import hashlib
import json
import unicodedata
from typing import Any, Mapping


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def semantic_payload(raw: Mapping[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(dict(raw))
    payload.pop("run_id", None)

    for key in (
        "approved_requirements",
        "package_requirement_ids",
        "required_evidence",
        "resource_locks",
    ):
        values = payload.get(key)
        if isinstance(values, list):
            payload[key] = sorted(values)

    for key in ("allowed_paths", "changed_paths"):
        values = payload.get(key)
        if isinstance(values, list):
            payload[key] = sorted(
                normalize_text(item.replace("\\", "/")) if isinstance(item, str) else item
                for item in values
            )

    coverage = payload.get("coverage")
    if isinstance(coverage, list):
        normalized_coverage: list[Any] = []
        for item in coverage:
            if not isinstance(item, dict):
                normalized_coverage.append(item)
                continue
            normalized_item = copy.deepcopy(item)
            for key in ("tasks", "tests", "evidence"):
                values = normalized_item.get(key)
                if isinstance(values, list):
                    normalized_item[key] = sorted(values)
            outputs = normalized_item.get("outputs")
            if isinstance(outputs, list):
                normalized_item["outputs"] = sorted(
                    normalize_text(output.replace("\\", "/"))
                    if isinstance(output, str)
                    else output
                    for output in outputs
                )
            normalized_coverage.append(normalized_item)
        payload["coverage"] = sorted(
            normalized_coverage,
            key=lambda item: str(item.get("requirement_id", "")) if isinstance(item, dict) else "",
        )

    references = payload.get("references")
    if isinstance(references, list):
        normalized_references: list[Any] = []
        for item in references:
            if not isinstance(item, dict):
                normalized_references.append(item)
                continue
            normalized_item = copy.deepcopy(item)
            path = normalized_item.get("path")
            if isinstance(path, str):
                normalized_item["path"] = normalize_text(path.replace("\\", "/"))
            normalized_references.append(normalized_item)
        payload["references"] = sorted(
            normalized_references,
            key=lambda item: (
                str(item.get("project_id", "")),
                str(item.get("kind", "")),
                str(item.get("path", "")),
            )
            if isinstance(item, dict)
            else ("", "", ""),
        )

    return payload
