from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"
DEFAULT_SKILL_REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def active_skill_ids(path: Path = DEFAULT_SKILL_REGISTRY) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("skills", [])
    if not isinstance(rows, list):
        raise ValueError("SKILL_REGISTRY skills must be a list")
    result: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("SKILL_REGISTRY entries must be objects")
        if row.get("status") == "ACTIVE":
            skill_id = row.get("skill_id")
            if not isinstance(skill_id, str) or not skill_id:
                raise ValueError("ACTIVE skill must have a non-empty skill_id")
            if skill_id in result:
                raise ValueError(f"duplicate ACTIVE skill_id in registry: {skill_id}")
            result.add(skill_id)
    return result


def matches(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return fnmatch.fnmatchcase(path, pattern)


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(matches(path, pattern) for pattern in patterns)


def find_part(manifest: dict, part_id: str) -> dict:
    for part in manifest["parts"]:
        if part["part_id"] == part_id:
            return part
    raise KeyError(part_id)


def matching_part_ids(manifest: dict, path: str) -> list[str]:
    owners: list[str] = []
    for part in manifest["parts"]:
        patterns = part.get("owned_write_paths", []) + part.get("allowed_new_paths", [])
        if matches_any(path, patterns):
            owners.append(part["part_id"])
    return owners


def classify_path(manifest: dict, part: dict | None, path: str, integration: bool) -> tuple[bool, str]:
    protected = manifest["control_plane"]["protected_write_paths"]
    if matches_any(path, protected):
        if integration:
            return True, "CONTROL_PLANE_INTEGRATION_WRITE"
        return False, "CONTROL_PLANE_WRITE_FORBIDDEN"
    if integration:
        owners = matching_part_ids(manifest, path)
        return True, "PART_OWNED:" + ",".join(owners) if owners else "UNASSIGNED_INTEGRATION_REVIEW_REQUIRED"
    assert part is not None
    if matches_any(path, part["owned_write_paths"] + part.get("allowed_new_paths", [])):
        return True, "PART_OWNED"
    return False, "OUT_OF_PARTITION_WRITE"


def changed_files(base: str, head: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(3)
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git ls-files failed")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    parts = manifest.get("parts", [])
    ids = [p.get("part_id") for p in parts]
    if ids != [f"P{i:02d}" for i in range(1, 10)]:
        errors.append(f"part ids/order invalid: {ids}")
    if manifest.get("control_plane", {}).get("write_authority") != "INTEGRATION_ONLY":
        errors.append("control plane write_authority must be INTEGRATION_ONLY")

    skills: list[str] = []
    paths: dict[str, str] = {}
    protected_patterns = manifest.get("control_plane", {}).get("protected_write_paths", [])
    protected_exact = set(protected_patterns)
    for part in parts:
        part_id = part.get("part_id", "UNKNOWN")
        skills.extend(part.get("owned_skill_ids", []))
        context = ROOT / part.get("context_pack", "")
        if not context.exists():
            errors.append(f"missing context pack: {context}")
        learning_log = ROOT / part.get("learning_log", "")
        if not learning_log.exists():
            errors.append(f"missing learning log for {part_id}: {learning_log}")
        for pattern in part.get("owned_write_paths", []):
            if pattern in protected_exact:
                errors.append(f"{part_id} owns protected exact pattern {pattern}")
            previous = paths.setdefault(pattern, part_id)
            if previous != part_id:
                errors.append(f"duplicate owned pattern {pattern}: {previous}/{part_id}")

    assigned = set(skills)
    try:
        active = active_skill_ids()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"cannot read active Skill registry: {error}")
        active = set()
    if len(skills) != len(assigned):
        errors.append("duplicate skill ownership")
    missing = sorted(active - assigned)
    extra = sorted(assigned - active)
    if missing:
        errors.append(f"ACTIVE skills missing partition owner: {missing}")
    if extra:
        errors.append(f"partition owns non-ACTIVE/unknown skills: {extra}")

    try:
        files = tracked_files()
    except RuntimeError as error:
        errors.append(str(error))
        files = []
    for path in files:
        if matches_any(path, protected_patterns):
            continue
        owners = matching_part_ids(manifest, path)
        unique_owners = sorted(set(owners))
        if len(unique_owners) > 1:
            errors.append(f"semantic path overlap {path}: {unique_owners}")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Base partition write scope")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--part", help="P01..P09 worker mode")
    mode.add_argument("--integration", action="store_true", help="Integration audit mode")
    parser.add_argument("--validate-manifest", action="store_true")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--files", nargs="*")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = load_manifest(Path(args.manifest))
    if args.validate_manifest:
        errors = validate_manifest(manifest)
        if errors:
            for error in errors:
                print(f"MANIFEST_ERROR {error}")
            return 3
        print("BASE_PARTITION_MANIFEST: PASS")
        if not args.part and not args.integration and args.files is None and args.base is None:
            return 0
    if not args.part and not args.integration:
        print("ERROR: choose --part or --integration", file=sys.stderr)
        return 3
    try:
        part = None if args.integration else find_part(manifest, args.part)
    except KeyError:
        print(f"ERROR: unknown part {args.part}", file=sys.stderr)
        return 3
    if args.files is not None:
        files = args.files
    else:
        if not args.base:
            print("ERROR: --base is required when --files is not supplied", file=sys.stderr)
            return 3
        files = changed_files(args.base, args.head)
    failures = 0
    for path in files:
        allowed, reason = classify_path(manifest, part, path, args.integration)
        status = "PASS" if allowed else "FAIL"
        print(f"{status}\t{reason}\t{path}")
        failures += 0 if allowed else 1
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
