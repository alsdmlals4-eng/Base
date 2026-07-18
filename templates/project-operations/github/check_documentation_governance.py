#!/usr/bin/env python3
"""Validate project documentation governance rules.

Usage:
  python tools/check_documentation_governance.py \
    --config .github/documentation-governance.json \
    --base "$BASE_SHA" --head "$HEAD_SHA"

The checker uses only the Python standard library so projects can run it in a
minimal GitHub Actions environment. Project-specific paths and enforcement
levels belong in the JSON configuration, not in this script.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CANONICAL_RE = re.compile(r"^\s*canonical_path:\s*[\"']?([^\"'#\n]+)", re.MULTILINE)
ASSET_ID_RE = re.compile(r"^\s*-\s*asset_id:\s*[\"']?([^\"'#\n]+)", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=".github/documentation-governance.json",
        help="Path to the JSON configuration.",
    )
    parser.add_argument("--base", default=os.environ.get("BASE_SHA", ""))
    parser.add_argument("--head", default=os.environ.get("HEAD_SHA", "HEAD"))
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"JSON file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON file {path}: {exc}")


def has_ignored_segment(path: Path, ignored: set[str]) -> bool:
    lowered = {part.lower() for part in path.parts}
    return any(segment.lower() in lowered for segment in ignored)


def iter_active_files(root: Path, roots: Iterable[str], ignored: set[str]) -> Iterable[Path]:
    for configured in roots:
        start = root / configured
        if not start.exists():
            continue
        if start.is_file():
            if not has_ignored_segment(start.relative_to(root), ignored):
                yield start
            continue
        for path in start.rglob("*"):
            if path.is_file() and not has_ignored_segment(path.relative_to(root), ignored):
                yield path


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return target.split("#", 1)[0]


def check_markdown_links(root: Path, markdown_roots: list[str], ignored: set[str]) -> list[str]:
    errors: list[str] = []
    for path in iter_active_files(root, markdown_roots, ignored):
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: unable to decode Markdown as UTF-8: {exc}")
            continue
        for raw in LINK_RE.findall(text):
            target = normalize_link_target(raw)
            if not target or target.startswith(
                ("http://", "https://", "mailto:", "data:", "sandbox:", "#")
            ):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path}: link escapes repository: {raw}")
                continue
            if not candidate.exists():
                errors.append(f"{path}: missing local link target: {raw}")
    return errors


def check_required_paths(root: Path, required: list[str]) -> list[str]:
    return [f"Required path missing: {item}" for item in required if not (root / item).exists()]


def check_forbidden_names(
    root: Path,
    active_roots: list[str],
    ignored: set[str],
    patterns: list[str],
) -> list[str]:
    compiled = [re.compile(pattern) for pattern in patterns]
    errors: list[str] = []
    for path in iter_active_files(root, active_roots, ignored):
        relative = path.relative_to(root)
        if any(pattern.search(path.name) for pattern in compiled):
            errors.append(f"Forbidden active filename: {relative}")
    return errors


def check_asset_manifests(root: Path, manifests: list[str]) -> list[str]:
    errors: list[str] = []
    canonical_owner: dict[str, str] = {}
    asset_ids: set[str] = set()

    for manifest_name in manifests:
        manifest = root / manifest_name
        if not manifest.exists():
            errors.append(f"Asset manifest missing: {manifest_name}")
            continue
        text = manifest.read_text(encoding="utf-8")

        for asset_id in (match.strip() for match in ASSET_ID_RE.findall(text)):
            if not asset_id:
                continue
            if asset_id in asset_ids:
                errors.append(f"Duplicate asset_id across manifests: {asset_id}")
            asset_ids.add(asset_id)

        for canonical in (match.strip() for match in CANONICAL_RE.findall(text)):
            if not canonical:
                continue
            owner = canonical_owner.get(canonical)
            if owner:
                errors.append(
                    f"Duplicate canonical_path: {canonical} in {owner} and {manifest_name}"
                )
            else:
                canonical_owner[canonical] = manifest_name

            candidate = root / canonical
            if not candidate.exists():
                errors.append(
                    f"{manifest_name}: canonical_path does not exist: {canonical}"
                )
    return errors


def content_digest(root: Path, relative_paths: list[str]) -> tuple[str, list[str]]:
    digest = hashlib.sha256()
    errors: list[str] = []

    for relative in sorted(set(relative_paths)):
        path = root / relative
        if not path.exists():
            errors.append(f"Publication input missing: {relative}")
            continue
        if not path.is_file():
            errors.append(f"Publication input is not a file: {relative}")
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")

    return digest.hexdigest(), errors


def check_pdf_header(path: Path) -> bool:
    try:
        return path.read_bytes()[:5] == b"%PDF-"
    except OSError:
        return False


def load_publications(root: Path, manifest_name: str) -> tuple[list[dict], list[str]]:
    if not manifest_name:
        return [], []

    manifest = root / manifest_name
    if not manifest.exists():
        return [], [f"Publication manifest missing: {manifest_name}"]

    try:
        data = load_json(manifest)
    except SystemExit as exc:
        return [], [str(exc)]

    publications = data.get("publications", [])
    if not isinstance(publications, list):
        return [], [f"{manifest_name}: 'publications' must be a list"]
    return publications, []


def check_publications(
    root: Path,
    manifest_name: str,
    enforce: bool,
    require_human_review: bool = False,
) -> tuple[list[str], list[dict]]:
    publications, errors = load_publications(root, manifest_name)
    seen_ids: set[str] = set()
    seen_outputs: set[str] = set()

    for item in publications:
        if not isinstance(item, dict):
            errors.append(f"{manifest_name}: each publication must be an object")
            continue

        publication_id = str(item.get("publication_id", "")).strip()
        output_pdf = str(item.get("output_pdf", "")).strip()
        source_files = item.get("source_files", [])
        image_paths = item.get("approved_image_paths", [])
        status = str(item.get("status", "NOT_BUILT")).upper()
        role = str(item.get("role", "")).strip()
        expected_digest = str(item.get("content_sha256", "")).strip().lower()
        automated_render_review = str(
            item.get("automated_render_review", item.get("visual_review", "NOT_RUN"))
        ).upper()
        human_visual_review = str(item.get("human_visual_review", "NOT_RUN")).upper()

        if not publication_id:
            errors.append(f"{manifest_name}: publication_id is required")
        elif publication_id in seen_ids:
            errors.append(f"Duplicate publication_id: {publication_id}")
        seen_ids.add(publication_id)

        if role != "read_only_derivative":
            errors.append(
                f"{publication_id or manifest_name}: role must be read_only_derivative"
            )

        if not isinstance(source_files, list) or not source_files:
            errors.append(f"{publication_id}: source_files must contain at least one path")
            source_files = []
        if not isinstance(image_paths, list):
            errors.append(f"{publication_id}: approved_image_paths must be a list")
            image_paths = []

        inputs = [str(path) for path in source_files + image_paths]
        actual_digest, digest_errors = content_digest(root, inputs)
        errors += [f"{publication_id}: {error}" for error in digest_errors]

        if output_pdf:
            if output_pdf in seen_outputs:
                errors.append(f"Duplicate output_pdf: {output_pdf}")
            seen_outputs.add(output_pdf)
        elif enforce or status == "CURRENT":
            errors.append(f"{publication_id}: output_pdf is required")

        output_path = root / output_pdf if output_pdf else None
        if status == "CURRENT" or enforce:
            if not output_path or not output_path.exists():
                errors.append(f"{publication_id}: PDF missing: {output_pdf}")
            elif not check_pdf_header(output_path):
                errors.append(f"{publication_id}: output is not a valid PDF header: {output_pdf}")

            if not expected_digest:
                errors.append(f"{publication_id}: CURRENT publication requires content_sha256")
            elif not digest_errors and expected_digest != actual_digest:
                errors.append(
                    f"{publication_id}: publication inputs changed; expected {expected_digest}, "
                    f"actual {actual_digest}"
                )

            if automated_render_review != "PASSED":
                errors.append(
                    f"{publication_id}: CURRENT publication requires "
                    "automated_render_review=PASSED"
                )
            if require_human_review and human_visual_review != "PASSED":
                errors.append(
                    f"{publication_id}: this gate requires human_visual_review=PASSED"
                )

        allowed = {"NOT_BUILT", "CURRENT", "STALE", "FAILED", "MISSING_ASSET"}
        if status not in allowed:
            errors.append(f"{publication_id}: unsupported publication status: {status}")
        if enforce and status != "CURRENT":
            errors.append(f"{publication_id}: publication enforcement requires status=CURRENT")

    return errors, publications


def git_changed_files(root: Path, base: str, head: str) -> list[str]:
    if not base or set(base) == {"0"}:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches_any(path: str, globs: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in globs)


def check_change_rules(changed: list[str], rules: list[dict]) -> list[str]:
    errors: list[str] = []
    changed_set = set(changed)

    for rule in rules:
        sources = rule.get("source_globs", [])
        if not any(matches_any(path, sources) for path in changed):
            continue

        required_all = rule.get("required_all", [])
        required_any = rule.get("required_any", [])

        missing_all = [path for path in required_all if path not in changed_set]
        if missing_all:
            errors.append(
                f"Change rule '{rule.get('name', 'unnamed')}' requires updates: "
                + ", ".join(missing_all)
            )

        if required_any and not any(path in changed_set for path in required_any):
            errors.append(
                f"Change rule '{rule.get('name', 'unnamed')}' requires at least one: "
                + ", ".join(required_any)
            )
    return errors


def check_publication_changes(
    changed: list[str],
    manifest_name: str,
    publications: list[dict],
    enforce: bool,
) -> list[str]:
    if not changed or not manifest_name:
        return []

    errors: list[str] = []
    changed_set = set(changed)

    for item in publications:
        if not isinstance(item, dict):
            continue
        publication_id = str(item.get("publication_id", "unnamed"))
        inputs = [
            str(path)
            for path in item.get("source_files", []) + item.get("approved_image_paths", [])
        ]
        if not any(path in changed_set for path in inputs):
            continue

        output_pdf = str(item.get("output_pdf", ""))
        if manifest_name not in changed_set:
            errors.append(
                f"{publication_id}: source or approved image changed; update {manifest_name}"
            )
        if enforce and output_pdf and output_pdf not in changed_set:
            errors.append(
                f"{publication_id}: source or approved image changed; regenerate {output_pdf}"
            )

    return errors


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    config = load_json(root / args.config)
    ignored = set(config.get("ignored_segments", []))

    errors: list[str] = []
    errors += check_required_paths(root, config.get("required_paths", config.get("required_files", [])))
    errors += check_forbidden_names(
        root,
        config.get("active_roots", []),
        ignored,
        config.get("forbidden_active_name_patterns", []),
    )
    errors += check_markdown_links(
        root,
        config.get("markdown_link_roots", []),
        ignored,
    )
    errors += check_asset_manifests(root, config.get("asset_manifests", []))

    publication_manifest = str(config.get("publication_manifest", ""))
    enforce_publications = bool(config.get("enforce_publications", False))
    publication_errors, publications = check_publications(
        root,
        publication_manifest,
        enforce_publications,
        bool(config.get("require_human_publication_visual_review", False)),
    )
    errors += publication_errors

    try:
        changed = git_changed_files(root, args.base, args.head)
    except RuntimeError as exc:
        errors.append(f"Unable to inspect changed files: {exc}")
        changed = []

    errors += check_change_rules(changed, config.get("change_rules", []))
    errors += check_publication_changes(
        changed,
        publication_manifest,
        publications,
        enforce_publications,
    )

    if errors:
        print("Documentation governance failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentation governance passed.")
    if changed:
        print(f"Checked {len(changed)} changed file(s).")
    if publications:
        print(f"Checked {len(publications)} publication(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
