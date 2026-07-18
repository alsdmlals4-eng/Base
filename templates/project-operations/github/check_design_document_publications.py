#!/usr/bin/env python3
"""Validate JSON design-document sources and generated DOCX/PDF/diagram publications."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ACTIVE_STATUSES = {"ACTIVE", "CURRENT"}
INACTIVE_STATUSES = {"HOLD", "BACKUP", "REMOVAL_CANDIDATE", "NOT_INSTALLED"}
ALLOWED_STATUSES = ACTIVE_STATUSES | INACTIVE_STATUSES
IGNORED_SEGMENTS = {"[백업]", "[보류]", "[제거 후보]", "archive", "hold", "deprecated"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/documentation-governance.json")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"JSON file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON file {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"JSON root must be an object: {path}")
    return data


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def repo_relative(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def check_header(path: Path, header: bytes) -> bool:
    try:
        return path.read_bytes()[: len(header)] == header
    except OSError:
        return False


def check_forbidden_markdown_bibles(root: Path, config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    design_root = root / str(config.get("design_root", "[기획서]"))
    if not design_root.is_dir():
        return errors
    forbidden_names = set(
        config.get(
            "forbidden_markdown_design_bible_names",
            ["DISCIPLINE_BIBLE.md", "PROJECT_MASTER_PLAN.md"],
        )
    )
    suffixes = tuple(config.get("forbidden_markdown_design_bible_suffixes", ["_기획서.md"]))
    for path in design_root.rglob("*.md"):
        relative_parts = set(path.relative_to(design_root).parts)
        if relative_parts & IGNORED_SEGMENTS:
            continue
        if path.name in forbidden_names or path.name.endswith(suffixes):
            errors.append(
                f"Active Markdown design bible is forbidden: {repo_relative(root, path)}; "
                "use a structured JSON source and generate DOCX/PDF"
            )
    return errors


def check_path_hash(
    errors: list[str],
    root: Path,
    base: Path,
    relative: str,
    expected: str,
    label: str,
    header: bytes | None = None,
) -> None:
    path = resolve(base, relative)
    if not path.is_file():
        errors.append(f"{label} missing: {relative}")
        return
    if header is not None and not check_header(path, header):
        errors.append(f"{label} has invalid file header: {relative}")
    actual = digest(path)
    if str(expected).lower() != actual:
        errors.append(f"{label} hash mismatch: {relative}; actual {actual}")
    try:
        path.relative_to(root)
    except ValueError:
        errors.append(f"{label} must stay inside repository: {relative}")


def check_manifest(
    root: Path,
    registry_dir: Path,
    entry: dict[str, Any],
    config: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    manifest_path = resolve(registry_dir, str(entry.get("publication_manifest", "")))
    if not manifest_path.is_file():
        return [f"Publication manifest missing for {entry.get('document_id')}: {manifest_path}"]
    try:
        manifest = load_json(manifest_path)
    except SystemExit as exc:
        return [str(exc)]

    source_path = resolve(registry_dir, str(entry.get("source_json", "")))
    if not source_path.is_file():
        return [f"Source JSON missing for {entry.get('document_id')}: {source_path}"]
    if manifest.get("publication_id") != entry.get("document_id"):
        errors.append(f"{manifest_path}: publication_id does not match registry")
    if manifest.get("role") != "human-readable-derivative":
        errors.append(f"{manifest_path}: role must be human-readable-derivative")
    if manifest.get("status") != "CURRENT":
        errors.append(f"{manifest_path}: status must be CURRENT")
    if manifest.get("automated_render_review") != "PASSED":
        errors.append(f"{manifest_path}: automated_render_review must be PASSED")
    if int(manifest.get("rendered_page_count", 0) or 0) < 1:
        errors.append(f"{manifest_path}: rendered_page_count must be at least 1")
    if bool(config.get("require_human_design_document_visual_review", False)) and manifest.get(
        "human_visual_review"
    ) != "PASSED":
        errors.append(f"{manifest_path}: human_visual_review must be PASSED")
    expected_source_hash = digest(source_path)
    if str(manifest.get("source_sha256", "")).lower() != expected_source_hash:
        errors.append(
            f"{manifest_path}: source JSON changed; expected source_sha256 {expected_source_hash}"
        )

    generator_rel = str(entry.get("generator", "")).strip()
    generator_path = root / generator_rel
    if not generator_path.is_file():
        errors.append(f"Generator missing: {generator_rel}")
    else:
        expected = digest(generator_path)
        if str(manifest.get("generator_sha256", "")).lower() != expected:
            errors.append(f"{manifest_path}: generator changed; rebuild publication")
    diagram_generator_rel = str(config.get("design_document_diagram_generator", "tools/design_document_diagrams.py"))
    diagram_generator_path = root / diagram_generator_rel
    if not diagram_generator_path.is_file():
        errors.append(f"Diagram generator missing: {diagram_generator_rel}")
    else:
        expected = digest(diagram_generator_path)
        if str(manifest.get("diagram_generator_sha256", "")).lower() != expected:
            errors.append(f"{manifest_path}: diagram generator changed; rebuild publication")

    check_path_hash(
        errors,
        root,
        registry_dir,
        str(manifest.get("output_docx", "")),
        str(manifest.get("output_docx_sha256", "")),
        "DOCX",
        b"PK",
    )
    check_path_hash(
        errors,
        root,
        registry_dir,
        str(manifest.get("output_pdf", "")),
        str(manifest.get("output_pdf_sha256", "")),
        "PDF",
        b"%PDF-",
    )

    diagrams = manifest.get("generated_diagrams", {})
    if not isinstance(diagrams, dict) or not diagrams:
        errors.append(f"{manifest_path}: generated_diagrams must contain image assets")
    else:
        for relative, expected in diagrams.items():
            check_path_hash(errors, root, registry_dir, str(relative), str(expected), "Diagram")
            if Path(str(relative)).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                errors.append(f"Unsupported diagram format: {relative}")

    visuals = manifest.get("approved_visuals", {})
    if not isinstance(visuals, dict):
        errors.append(f"{manifest_path}: approved_visuals must be an object")
    else:
        for relative, expected in visuals.items():
            check_path_hash(errors, root, registry_dir, str(relative), str(expected), "Approved visual")

    return errors


def check_registry(root: Path, config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    registry_rel = str(config.get("design_document_registry", "")).strip()
    enforce = bool(config.get("enforce_design_document_publications", False))
    if not registry_rel:
        return ["design_document_registry is required"] if enforce else []
    registry_path = root / registry_rel
    if not registry_path.is_file():
        return [f"Design document registry missing: {registry_rel}"] if enforce else []
    try:
        registry = load_json(registry_path)
    except SystemExit as exc:
        return [str(exc)]
    registry_dir = registry_path.parent
    human = registry.get("human_presentation", {})
    if enforce:
        expected = {
            "primary_reading_format": "PDF",
            "editable_review_format": "DOCX",
            "diagram_assets_required": True,
            "approved_visuals_embedded": True,
            "markdown_design_bibles_allowed": False,
        }
        if not isinstance(human, dict):
            errors.append(f"{registry_rel}: human_presentation must be an object")
            human = {}
        for key, value in expected.items():
            if human.get(key) != value:
                errors.append(f"{registry_rel}: human_presentation.{key} must be {value!r}")

    documents = registry.get("documents", [])
    if not isinstance(documents, list):
        return errors + [f"{registry_rel}: documents must be a list"]
    active = [item for item in documents if isinstance(item, dict) and str(item.get("status", "")).upper() in ACTIVE_STATUSES]
    if enforce and not active:
        errors.append(f"{registry_rel}: at least one active design document is required")

    seen: set[str] = set()
    coverage: set[str] = set()
    for index, entry in enumerate(documents):
        label = f"{registry_rel}: documents[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        document_id = str(entry.get("document_id", "")).strip()
        if not document_id:
            errors.append(f"{label}.document_id is required")
            continue
        if document_id in seen:
            errors.append(f"Duplicate document_id: {document_id}")
        seen.add(document_id)
        status = str(entry.get("status", "")).upper()
        if status not in ALLOWED_STATUSES:
            errors.append(f"{document_id}: unsupported status {status}")
        if status not in ACTIVE_STATUSES:
            continue

        covered = entry.get("responsibility_coverage", [entry.get("discipline")])
        if not isinstance(covered, list) or not all(isinstance(item, str) and item.strip() for item in covered):
            errors.append(f"{document_id}: responsibility_coverage must be a non-empty string list")
        else:
            coverage.update(covered)

        required_fields = (
            "source_json",
            "output_docx",
            "output_pdf",
            "asset_dir",
            "publication_manifest",
            "generator",
        )
        for field in required_fields:
            if not str(entry.get(field, "")).strip():
                errors.append(f"{document_id}: {field} is required")
        source_path = resolve(registry_dir, str(entry.get("source_json", "")))
        if source_path.is_file():
            try:
                source = load_json(source_path)
                if source.get("document_id") != document_id:
                    errors.append(f"{document_id}: source JSON document_id mismatch")
                if not str(source.get("title", "")).strip():
                    errors.append(f"{document_id}: source JSON title is required")
                if not str(source.get("discipline", "")).strip():
                    errors.append(f"{document_id}: source JSON discipline is required")
                if str(source.get("status", "")).upper() not in ACTIVE_STATUSES:
                    errors.append(f"{document_id}: active registry entry requires active source JSON status")
            except SystemExit as exc:
                errors.append(str(exc))
        else:
            errors.append(f"{document_id}: source JSON missing: {repo_relative(root, source_path)}")
        errors += check_manifest(root, registry_dir, entry, config)

    required_coverage = config.get(
        "required_design_document_coverage",
        registry.get("required_responsibility_coverage", []),
    )
    for responsibility in required_coverage:
        if responsibility not in coverage:
            errors.append(f"Missing active design document responsibility coverage: {responsibility}")

    return errors


def main() -> int:
    options = parse_args()
    root = Path.cwd().resolve()
    config = load_json(root / options.config)
    errors = check_forbidden_markdown_bibles(root, config)
    errors += check_registry(root, config)
    if errors:
        print("Design document publication governance failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Design document publication governance passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
