#!/usr/bin/env python3
"""Validate project documentation governance rules.

Usage:
  python tools/check_documentation_governance.py \
    --config .github/documentation-governance.json \
    --base "$BASE_SHA" --head "$HEAD_SHA"
"""

from __future__ import annotations

import argparse
import fnmatch
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


def load_config(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Configuration not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON configuration {path}: {exc}")


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
        text = path.read_text(encoding="utf-8")
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


def check_required_files(root: Path, required: list[str]) -> list[str]:
    return [f"Required file missing: {item}" for item in required if not (root / item).exists()]


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


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    config = load_config(root / args.config)
    ignored = set(config.get("ignored_segments", []))

    errors: list[str] = []
    errors += check_required_files(root, config.get("required_files", []))
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

    try:
        changed = git_changed_files(root, args.base, args.head)
    except RuntimeError as exc:
        errors.append(f"Unable to inspect changed files: {exc}")
        changed = []

    errors += check_change_rules(changed, config.get("change_rules", []))

    if errors:
        print("Documentation governance failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentation governance passed.")
    if changed:
        print(f"Checked {len(changed)} changed file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
