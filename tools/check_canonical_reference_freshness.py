#!/usr/bin/env python3
"""Check canonical-reference freshness and change propagation."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".toml", ".txt"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=".github/reference-freshness.json")
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--root", default=".")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Reference freshness config not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON file {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"JSON root must be an object: {path}")
    return data


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def iter_text_files(root: Path, scan_globs: list[str], ignore_globs: list[str]) -> list[Path]:
    files: set[Path] = set()
    for pattern in scan_globs:
        for candidate in root.glob(pattern):
            if not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
                continue
            relative = candidate.relative_to(root).as_posix()
            if matches_any(relative, ignore_globs):
                continue
            files.add(candidate)
    return sorted(files)


def parse_legacy_aliases(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    aliases: set[str] = set()
    table_row = re.compile(r"^\|\s*`([^`]+)`\s*\|")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = table_row.match(line)
        if match:
            aliases.add(match.group(1).strip())
    return aliases


def git_changed_files(root: Path, base: str, head: str) -> set[str]:
    if not base:
        return set()
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "git diff failed")
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def check_legacy_references(root: Path, files: list[Path], aliases: set[str], allowed_globs: list[str]) -> list[str]:
    errors: list[str] = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        if matches_any(relative, allowed_globs):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for alias in sorted(aliases):
            old_path = f"skills/{alias}/SKILL.md"
            if re.search(rf"(?<![a-z0-9-]){re.escape(alias)}(?![a-z0-9-])", text):
                errors.append(f"Legacy skill id remains in active file: {relative} -> {alias}")
            if old_path in text:
                errors.append(f"Deleted skill path remains in active file: {relative} -> {old_path}")
    return errors


def check_forbidden_tokens(root: Path, files: list[Path], rules: list[dict]) -> list[str]:
    errors: list[str] = []
    for rule in rules:
        token = str(rule.get("token", ""))
        if not token:
            continue
        allowed = [str(item) for item in rule.get("allowed_globs", [])]
        for path in files:
            relative = path.relative_to(root).as_posix()
            if matches_any(relative, allowed):
                continue
            if token in path.read_text(encoding="utf-8", errors="replace"):
                errors.append(f"Forbidden stale token: {relative} -> {token}")
    return errors


def check_canonical_reference_rules(root: Path, rules: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, rule in enumerate(rules):
        label = str(rule.get("name") or f"canonical_reference_rules[{index}]")
        canonical = str(rule.get("canonical_path", "")).strip()
        if not canonical:
            errors.append(f"{label}: canonical_path is required")
            continue
        if not (root / canonical).is_file():
            errors.append(f"{label}: canonical source missing: {canonical}")
        tokens = [str(item) for item in rule.get("reference_tokens", []) if str(item)]
        consumers = [str(item) for item in rule.get("required_consumers", []) if str(item)]
        if not tokens:
            errors.append(f"{label}: reference_tokens must not be empty")
        for consumer in consumers:
            path = root / consumer
            if not path.is_file():
                errors.append(f"{label}: required consumer missing: {consumer}")
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if tokens and not any(token in text for token in tokens):
                errors.append(f"{label}: consumer does not reference current canonical source: {consumer}")
    return errors


def check_coupled_changes(changed: set[str], rules: list[dict]) -> list[str]:
    if not changed:
        return []
    errors: list[str] = []
    for index, rule in enumerate(rules):
        label = str(rule.get("name") or f"coupled_change_rules[{index}]")
        when = [str(item) for item in rule.get("when_changed", []) if str(item)]
        require_all = [str(item) for item in rule.get("require_all_changed", []) if str(item)]
        require_any = [str(item) for item in rule.get("require_any_changed", []) if str(item)]
        triggered = sorted(path for path in changed if matches_any(path, when))
        if not triggered:
            continue
        missing_all = [
            pattern for pattern in require_all
            if not any(fnmatch.fnmatch(path, pattern) for path in changed)
        ]
        if missing_all:
            errors.append(f"{label}: source change {triggered} requires changed companions {missing_all}")
        if require_any and not any(
            fnmatch.fnmatch(path, pattern)
            for path in changed
            for pattern in require_any
        ):
            errors.append(
                f"{label}: source change {triggered} requires at least one changed companion from {require_any}"
            )
    return errors


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    config = load_json(root / args.config)
    if config.get("schema_version") != 1:
        raise SystemExit("reference freshness config schema_version must be 1")

    files = iter_text_files(
        root,
        [str(item) for item in config.get("scan_globs", [])],
        [str(item) for item in config.get("ignore_globs", [])],
    )
    aliases_path = str(config.get("legacy_aliases_path", "")).strip()
    aliases = parse_legacy_aliases(root / aliases_path) if aliases_path else set()

    errors: list[str] = []
    errors.extend(check_legacy_references(
        root,
        files,
        aliases,
        [str(item) for item in config.get("allowed_legacy_globs", [])],
    ))
    errors.extend(check_forbidden_tokens(root, files, config.get("forbidden_tokens", [])))
    errors.extend(check_canonical_reference_rules(root, config.get("canonical_reference_rules", [])))
    changed = git_changed_files(root, args.base, args.head)
    errors.extend(check_coupled_changes(changed, config.get("coupled_change_rules", [])))

    if errors:
        print("REFERENCE FRESHNESS CHECK: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REFERENCE FRESHNESS CHECK: PASS")
    print(f"- scanned_files: {len(files)}")
    print(f"- legacy_aliases: {len(aliases)}")
    print(f"- changed_files: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
