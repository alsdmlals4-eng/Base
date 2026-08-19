from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def classify_path(manifest: dict, part: dict | None, path: str, integration: bool) -> tuple[bool, str]:
    protected = manifest["control_plane"]["protected_write_paths"]
    if matches_any(path, protected):
        if integration:
            return True, "CONTROL_PLANE_INTEGRATION_WRITE"
        return False, "CONTROL_PLANE_WRITE_FORBIDDEN"
    if integration:
        owners = [p["part_id"] for p in manifest["parts"] if matches_any(path, p["owned_write_paths"] + p.get("allowed_new_paths", []))]
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
    protected = set(manifest.get("control_plane", {}).get("protected_write_paths", []))
    for part in parts:
        skills.extend(part.get("owned_skill_ids", []))
        context = ROOT / part.get("context_pack", "")
        if not context.exists():
            errors.append(f"missing context pack: {context}")
        for pattern in part.get("owned_write_paths", []):
            if pattern in protected:
                errors.append(f"{part['part_id']} owns protected pattern {pattern}")
            previous = paths.setdefault(pattern, part["part_id"])
            if previous != part["part_id"]:
                errors.append(f"duplicate owned pattern {pattern}: {previous}/{part['part_id']}")
    if len(skills) != len(set(skills)):
        errors.append("duplicate skill ownership")
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
