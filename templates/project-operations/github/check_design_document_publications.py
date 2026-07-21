#!/usr/bin/env python3
"""Validate schema v3 design sources and policy-driven publications."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from markdown_it import MarkdownIt


ACTIVE_STATUSES = {"ACTIVE", "CURRENT", "SUPPORT"}
IGNORED_SEGMENTS = {"[백업]", "[보류]", "[제거 후보]", "archive", "hold", "deprecated"}
PUBLICATION_POLICIES = {"source_only", "milestone_sync", "always_sync"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/documentation-governance.json")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def validate_schema(data: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label} {location}: {error.message}")
    return errors


def check_hash(path: Path, expected: Any, label: str, header: bytes | None = None) -> list[str]:
    if not path.is_file():
        return [f"{label} missing: {path}"]
    errors = []
    if header and path.read_bytes()[: len(header)] != header:
        errors.append(f"{label} has invalid file header: {path}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if str(expected).lower() != actual:
        errors.append(f"{label} hash mismatch: {path}; actual {actual}")
    return errors


def validate_markdown(path: Path, entry: dict[str, Any]) -> list[str]:
    errors = []
    source = path.read_text(encoding="utf-8")
    if re.search(r"</?[A-Za-z][^>]*>", source):
        errors.append(f"Raw HTML is forbidden in Markdown source: {path}")
    tokens = MarkdownIt("commonmark", {"html": False}).enable("table").parse(source)
    headings: list[tuple[int, str]] = []
    mermaid_count = 0
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and index + 1 < len(tokens):
            headings.append((int(token.tag[1:]), tokens[index + 1].content.strip()))
        if token.type == "fence" and token.info.strip().lower() == "mermaid":
            mermaid_count += 1
        if token.type == "inline":
            for child in token.children or []:
                if child.type == "image" and (child.attrGet("src") or "").startswith(("http://", "https://", "//")):
                    errors.append(f"Remote Markdown image is forbidden: {child.attrGet('src')}")
    h1 = [text for level, text in headings if level == 1]
    if len(h1) != 1 or h1[0] != entry["title"]:
        errors.append(f"Markdown H1 must match Registry title {entry['title']!r}: {path}")
    required = entry.get("required_sections") or ["목표", "배경과 의도", "범위", "규칙과 제약", "검증과 완료 기준"]
    h2 = {text for level, text in headings if level == 2}
    for section in required:
        if section not in h2:
            errors.append(f"Markdown required section missing: {section} ({path})")
    if entry.get("diagram_policy") == "mermaid" and mermaid_count == 0:
        errors.append(f"diagram_policy=mermaid requires Mermaid source: {path}")
    return errors


def check_manifest(
    root: Path,
    registry_dir: Path,
    entry: dict[str, Any],
    config: dict[str, Any],
    *,
    require_current: bool,
) -> list[str]:
    errors: list[str] = []
    manifest_value = entry.get("publication_manifest")
    if not manifest_value:
        return [f"Publication manifest path missing for {entry['document_id']}"] if require_current else []
    manifest_path = resolve(registry_dir, str(manifest_value))
    if not manifest_path.is_file():
        return [f"Publication manifest missing for {entry['document_id']}: {manifest_path}"] if require_current else []
    try:
        manifest = load_json(manifest_path)
    except ValueError as exc:
        return [str(exc)]
    schema_dir = root / "schemas"
    errors += validate_schema(manifest, schema_dir / "publication-manifest-v3.schema.json", str(manifest_path))
    if manifest.get("publication_id") != entry["document_id"]:
        errors.append(f"{manifest_path}: publication_id does not match Registry")
    if manifest.get("source_path") != entry["source_path"] or manifest.get("source_format") != entry["source_format"]:
        errors.append(f"{manifest_path}: source path/format does not match Registry")
    sync_status = manifest.get("sync_status")
    if require_current and sync_status != "CURRENT":
        errors.append(f"{manifest_path}: sync_status must be CURRENT")
    if not require_current and sync_status != "CURRENT":
        return errors
    if manifest.get("automated_render_review") != "PASSED":
        errors.append(f"{manifest_path}: automated_render_review must be PASSED")
    if bool(config.get("require_human_design_document_visual_review", False)) and manifest.get("human_visual_review") != "PASSED":
        errors.append(f"{manifest_path}: human_visual_review must be PASSED")
    source_path = resolve(registry_dir, entry["source_path"])
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if manifest.get("source_sha256") != source_hash:
        errors.append(f"{manifest_path}: source changed; rebuild publication")
    generator_path = root / str(entry["generator"])
    errors += check_hash(generator_path, manifest.get("generator_sha256"), "Generator")
    pdf_path = resolve(registry_dir, str(manifest.get("output_pdf", "")))
    errors += check_hash(pdf_path, manifest.get("output_pdf_sha256"), "PDF", b"%PDF-")
    docx_value = manifest.get("output_docx")
    if docx_value:
        errors += check_hash(resolve(registry_dir, str(docx_value)), manifest.get("output_docx_sha256"), "DOCX", b"PK")
    elif manifest.get("output_docx_sha256") is not None:
        errors.append(f"{manifest_path}: output_docx_sha256 must be null when output_docx is null")
    if manifest.get("human_visual_review") == "PASSED":
        if manifest.get("human_visual_review_pdf_sha256") != manifest.get("output_pdf_sha256"):
            errors.append(f"{manifest_path}: human review PDF hash must match the current PDF")
    elif manifest.get("human_visual_review_pdf_sha256") is not None:
        errors.append(f"{manifest_path}: unreviewed PDF must not retain a human review hash")
    for field in ("generated_assets", "approved_visuals", "source_images", "mermaid_sources", "mermaid_svg", "mermaid_png"):
        values = manifest.get(field, {})
        if not isinstance(values, dict):
            errors.append(f"{manifest_path}: {field} must be an object")
            continue
        for relative, expected in values.items():
            errors += check_hash(resolve(registry_dir, relative), expected, field)
    return errors


def check_registry(root: Path, config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    registry_rel = str(config.get("design_document_registry", "")).strip()
    enforce = bool(config.get("enforce_design_document_publications", False))
    require_milestone = bool(config.get("require_milestone_design_document_publications", False))
    if not registry_rel:
        return ["design_document_registry is required"] if enforce else []
    registry_path = root / registry_rel
    if not registry_path.is_file():
        return [f"Design document registry missing: {registry_rel}"] if enforce else []
    registry = load_json(registry_path)
    if registry.get("schema_version") != 3:
        return [f"{registry_rel}: schema v3 is required; follow docs/migrations/v2.2.0-to-v3.0.0.md"]
    errors += validate_schema(registry, root / "schemas/design-document-registry-v3.schema.json", registry_rel)
    registry_dir = registry_path.parent
    documents = registry.get("documents", [])
    active = [entry for entry in documents if isinstance(entry, dict) and entry.get("status") in ACTIVE_STATUSES]
    if enforce and not active:
        errors.append(f"{registry_rel}: at least one active design document is required")
    seen: set[str] = set()
    coverage: set[str] = set()
    registered_markdown: set[Path] = set()
    for entry in documents:
        if not isinstance(entry, dict):
            continue
        document_id = entry.get("document_id")
        if document_id in seen:
            errors.append(f"Duplicate document_id: {document_id}")
        seen.add(document_id)
        if entry.get("status") not in ACTIVE_STATUSES:
            continue
        policy = entry.get("publication_policy")
        if policy not in PUBLICATION_POLICIES:
            errors.append(f"{document_id}: unsupported publication_policy {policy!r}")
            continue
        coverage.update(entry.get("responsibility_coverage", []))
        source_path = resolve(registry_dir, entry["source_path"])
        if not source_path.is_file():
            errors.append(f"{document_id}: source missing: {source_path}")
            continue
        if entry["source_format"] == "json":
            try:
                source = load_json(source_path)
                if source.get("schema_version") != 3:
                    errors.append(f"{source_path}: structured source schema v3 is required")
                errors += validate_schema(source, root / "schemas/structured-design-document-v3.schema.json", str(source_path))
                if source.get("document_id") != document_id or source.get("title") != entry.get("title"):
                    errors.append(f"{document_id}: source JSON identity does not match Registry")
            except ValueError as exc:
                errors.append(str(exc))
        else:
            registered_markdown.add(source_path)
            errors += validate_markdown(source_path, entry)
        if policy == "always_sync":
            errors += check_manifest(root, registry_dir, entry, config, require_current=True)
        elif policy == "milestone_sync":
            errors += check_manifest(root, registry_dir, entry, config, require_current=require_milestone)
    for responsibility in config.get("required_design_document_coverage", registry.get("required_responsibility_coverage", [])):
        if responsibility not in coverage:
            errors.append(f"Missing active design document responsibility coverage: {responsibility}")
    design_root = root / str(config.get("design_root", "[기획서]"))
    if design_root.is_dir():
        for path in design_root.rglob("*.md"):
            if set(path.relative_to(design_root).parts) & IGNORED_SEGMENTS:
                continue
            if (path.name.endswith("_기획서.md") or path.name in {"DISCIPLINE_BIBLE.md", "PROJECT_MASTER_PLAN.md"}) and path.resolve() not in registered_markdown:
                errors.append(f"Unregistered active Markdown design source: {path}")
    return errors


def main() -> int:
    options = parse_args()
    root = Path.cwd().resolve()
    try:
        config = load_json(root / options.config)
        errors = check_registry(root, config)
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("Design document publication governance failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Design document publication governance passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
