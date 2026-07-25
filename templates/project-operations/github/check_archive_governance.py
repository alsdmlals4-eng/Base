from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ADAPTER_SCHEMA = "schemas/archive-retention-adapter-v1.schema.json"
MANIFEST_SCHEMA = "schemas/archive-manifest-v1.schema.json"
SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _relative_repo_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _schema_errors(instance: object, schema: object, label: str) -> list[str]:
    errors = Draft202012Validator(schema).iter_errors(instance)
    return [
        f"{label} schema: {'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(errors, key=lambda item: list(item.path))
    ]


def _markdown_body(text: str) -> str:
    stripped = text.lstrip("\ufeff")
    if stripped.startswith("---\n"):
        closing = stripped.find("\n---\n", 4)
        if closing >= 0:
            stripped = stripped[closing + 5 :]
    return stripped.strip()


def validate_archive_governance(
    root: Path, adapter_path: Path, manifest_path: Path
) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    try:
        adapter = _load_json(adapter_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"adapter parse: {error}"]
    try:
        manifest = _load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"manifest parse: {error}"]

    try:
        adapter_schema = _load_json(root / ADAPTER_SCHEMA)
        manifest_schema = _load_json(root / MANIFEST_SCHEMA)
    except (OSError, json.JSONDecodeError) as error:
        return [f"schema parse: {error}"]

    errors.extend(_schema_errors(adapter, adapter_schema, "adapter"))
    errors.extend(_schema_errors(manifest, manifest_schema, "manifest"))
    if errors:
        return sorted(errors)

    paths = adapter["paths"]
    for field in (
        "archive_root",
        "archive_readme",
        "archive_manifest",
    ):
        if not _relative_repo_path(paths[field]):
            errors.append(f"unsafe repository path: {field} -> {paths[field]}")
    for field in (
        "active_canon_roots",
        "inactive_skill_roots",
        "generated_derivative_roots",
        "protected_evidence_roots",
    ):
        for value in paths[field]:
            if not _relative_repo_path(value):
                errors.append(f"unsafe repository path: {field} -> {value}")

    archive_root = (root / paths["archive_root"]).resolve()
    readme = (root / paths["archive_readme"]).resolve()
    declared_manifest = (root / paths["archive_manifest"]).resolve()
    if not archive_root.is_dir():
        errors.append(f"archive root missing: {paths['archive_root']}")
    if not readme.is_file():
        errors.append(f"archive readme missing: {paths['archive_readme']}")
    if not declared_manifest.is_file():
        errors.append(f"archive manifest missing: {paths['archive_manifest']}")
    if declared_manifest != manifest_path.resolve():
        errors.append("manifest argument does not match adapter paths.archive_manifest")

    for active in paths["active_canon_roots"]:
        active_path = (root / active).resolve()
        try:
            active_path.relative_to(archive_root)
        except ValueError:
            pass
        else:
            errors.append(f"active canon root is inside archive root: {active}")

    seen_paths: set[str] = set()
    for record in manifest["records"]:
        current_path = record["current_path"]
        if current_path in seen_paths:
            errors.append(f"duplicate manifest current_path: {current_path}")
        seen_paths.add(current_path)
        if not _relative_repo_path(current_path):
            errors.append(f"unsafe manifest current_path: {current_path}")
            continue

        current = root / current_path
        if not current.is_file():
            errors.append(f"manifest current_path missing: {current_path}")
        elif current.suffix.lower() == ".md" and not _markdown_body(
            current.read_text(encoding="utf-8", errors="replace")
        ):
            errors.append(f"archived Markdown body is empty: {current_path}")

        for replacement in record["superseded_by"]:
            if replacement.startswith("external:"):
                continue
            if not _relative_repo_path(replacement) or not (root / replacement).exists():
                errors.append(
                    f"superseded_by target missing or unsafe: {current_path} -> {replacement}"
                )

    if archive_root.is_dir():
        for path in sorted(item for item in archive_root.rglob("*") if item.is_file()):
            if path.suffix.lower() not in {".md", ".json", ".txt", ".yml", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"secret-like material in archive: {path.relative_to(root)}")
                    break

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    errors = validate_archive_governance(
        root,
        root / args.adapter,
        root / args.manifest,
    )
    if errors:
        print("Archive governance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Archive governance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
