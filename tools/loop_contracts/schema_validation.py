from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .findings import Finding

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"

def validate_schema(name: str, instance: dict[str, object], path: str) -> list[Finding]:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    findings: list[Finding] = []
    for error in Draft202012Validator(schema).iter_errors(instance):
        pointer = "/".join(str(part) for part in error.absolute_path)
        findings.append(Finding("SCHEMA_INVALID", error.message, f"{path}#{pointer}"))
    return findings
