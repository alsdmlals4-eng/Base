from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


Violation = dict[str, Any]


def _select_records(document: Any, selector: str) -> list[Any]:
    if selector in ("", "$"):
        value = document
    else:
        if not selector.startswith("$."):
            raise ValueError(f"unsupported records selector: {selector}")
        value = document
        for part in selector[2:].split("."):
            if not isinstance(value, dict) or part not in value:
                return []
            value = value[part]
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return []


def _violation(
    *,
    path: str,
    record: str,
    field: str,
    code: str,
    message: str,
) -> Violation:
    return {
        "path": path,
        "record": record,
        "field": field,
        "code": code,
        "message": message,
    }


def validate_manifest(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate JSON records without mutating project data.

    Supported contracts are deliberately small: required fields, enum membership,
    duplicate IDs, and cross-file ID references. More domain-specific balance or
    migration rules belong to project adapters rather than this shared validator.
    """

    root = Path(root)
    violations: list[Violation] = []
    file_specs = manifest.get("files", [])
    loaded: dict[str, dict[str, Any]] = {}

    for file_spec in file_specs:
        rel_path = str(file_spec["path"])
        source_path = root / rel_path
        try:
            document = json.loads(source_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            violations.append(
                _violation(
                    path=rel_path,
                    record="$",
                    field="",
                    code="FILE_NOT_FOUND",
                    message="configured data file does not exist",
                )
            )
            loaded[rel_path] = {"records": [], "spec": file_spec}
            continue
        except json.JSONDecodeError as exc:
            violations.append(
                _violation(
                    path=rel_path,
                    record="$",
                    field="",
                    code="INVALID_JSON",
                    message=f"invalid JSON at line {exc.lineno} column {exc.colno}",
                )
            )
            loaded[rel_path] = {"records": [], "spec": file_spec}
            continue

        records = _select_records(document, str(file_spec.get("records", "$")))
        loaded[rel_path] = {"records": records, "spec": file_spec}

        id_field = file_spec.get("id_field")
        seen_ids: dict[Any, int] = {}
        required_fields = tuple(file_spec.get("required_fields", ()))
        enum_fields = file_spec.get("enum_fields", {})

        for index, record in enumerate(records):
            record_locator = f"$[{index}]"
            if not isinstance(record, dict):
                violations.append(
                    _violation(
                        path=rel_path,
                        record=record_locator,
                        field="",
                        code="RECORD_NOT_OBJECT",
                        message="record must be a JSON object",
                    )
                )
                continue

            for field in required_fields:
                if field not in record:
                    violations.append(
                        _violation(
                            path=rel_path,
                            record=record_locator,
                            field=str(field),
                            code="MISSING_REQUIRED_FIELD",
                            message="required field is missing",
                        )
                    )

            for field, allowed_values in enum_fields.items():
                if field in record and record[field] not in allowed_values:
                    violations.append(
                        _violation(
                            path=rel_path,
                            record=record_locator,
                            field=str(field),
                            code="INVALID_ENUM",
                            message=f"value {record[field]!r} is not in the allowed enum",
                        )
                    )

            if id_field and id_field in record:
                record_id = record[id_field]
                if record_id in seen_ids:
                    violations.append(
                        _violation(
                            path=rel_path,
                            record=record_locator,
                            field=str(id_field),
                            code="DUPLICATE_ID",
                            message=f"duplicate id {record_id!r}; first seen at index {seen_ids[record_id]}",
                        )
                    )
                else:
                    seen_ids[record_id] = index

    target_ids: dict[tuple[str, str], set[Any]] = {}
    for rel_path, payload in loaded.items():
        records = payload["records"]
        spec = payload["spec"]
        id_fields = {str(spec.get("id_field", "id"))}
        for ref in manifest.get("references", []):
            if str(ref.get("target_file")) == rel_path:
                id_fields.add(str(ref.get("target_id_field", "id")))
        for id_field in id_fields:
            target_ids[(rel_path, id_field)] = {
                record[id_field]
                for record in records
                if isinstance(record, dict) and id_field in record
            }

    for ref in manifest.get("references", []):
        source_file = str(ref["source_file"])
        source_field = str(ref["field"])
        target_file = str(ref["target_file"])
        target_id_field = str(ref.get("target_id_field", "id"))
        allow_null = bool(ref.get("allow_null", False))
        targets = target_ids.get((target_file, target_id_field), set())

        for index, record in enumerate(loaded.get(source_file, {}).get("records", [])):
            if not isinstance(record, dict) or source_field not in record:
                continue
            value = record[source_field]
            if value is None and allow_null:
                continue
            values = value if isinstance(value, list) else [value]
            for candidate in values:
                if candidate is None and allow_null:
                    continue
                if candidate not in targets:
                    violations.append(
                        _violation(
                            path=source_file,
                            record=f"$[{index}]",
                            field=source_field,
                            code="DANGLING_REFERENCE",
                            message=f"reference {candidate!r} not found in {target_file}.{target_id_field}",
                        )
                    )

    violations.sort(
        key=lambda item: (
            str(item["path"]),
            str(item["record"]),
            str(item["field"]),
            str(item["code"]),
            str(item["message"]),
        )
    )
    checked_records = sum(len(payload["records"]) for payload in loaded.values())
    return {
        "ok": not violations,
        "checked_files": len(file_specs),
        "checked_records": checked_records,
        "violations": violations,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate project JSON schema/cross-reference contracts")
    parser.add_argument("manifest", type=Path, help="JSON validation manifest")
    parser.add_argument("--root", type=Path, default=None, help="project/data root; defaults to manifest directory")
    args = parser.parse_args(argv)

    manifest_path: Path = args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = args.root if args.root is not None else manifest_path.parent
    report = validate_manifest(root, manifest)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
